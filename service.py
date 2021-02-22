from datetime import datetime
from notifier.telegram_notifier import TelegramNotifier
from asyncpg.pool import Pool
from emcd_client.client import EmcdClient
from models.account_coin import AccountCoin
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

from loguru import logger

from database.db import get_pool
from database.user_repo import UserRepository
from config import Lang, TOKEN, postgres, texts


async def update_account_data(semaphore: asyncio.BoundedSemaphore, account: AccountCoin, pool: Pool, notifier: TelegramNotifier,):
    async with semaphore:
        logger.info(f'{account.account_id}|{account.coin_id} - Scraping workers info')
        con = await pool.acquire()

        now = datetime.now()

        try:
            async with EmcdClient(account.account_id) as client:
                api_account = await client.get_workers(account.coin_id)
                user_repo = UserRepository(con)
                user_account = next((acc for acc in await user_repo.get_accounts(account.user_id) if acc.account_id == account.account_id), None)

                logger.info(f'{account.account_id}|{account.coin_id} - Scraped worker info')
                workers = api_account.get_all_workers(account.id)

                await user_repo.update_account_coin(account.id, account.user_id, account.account_id, account.coin_id, account.address, api_account, account.is_active, now)

                logger.info(f'{account.account_id}|{account.coin_id} - Total workers count {len(workers)}')

                if (workers):

                    previous_worker_state = await user_repo.get_previous_worker_state_for_account(account.id)
                    for worker in workers:
                        previous_state = next((w for w in previous_worker_state if w.worker_id == worker.worker), None)
                        if (previous_state):
                            if (previous_state.status_id != worker.status_id):
                                logger.info(f'{account.account_id}|{account.coin_id} - worker changed status {worker.worker}')

                                user_locale = Lang(previous_state.lang_id)
                                translation = texts[user_locale.name]
                                
                                status_names = translation['status']

                                await notifier.notify(previous_state.user_id, translation['worker_changed_status'].format(account_name=user_account.username, worker_name=previous_state.worker_id, previous_status=status_names[previous_state.status_id], new_status=status_names[worker.status_id]))

                    logger.info(f'{account.account_id}|{account.coin_id} - Clean up worker history {account.id}')
                    await user_repo.cleanup_worker_history_for_account(account.id)

                    logger.info(f'{account.account_id}|{account.coin_id} - Storing to database')

                    await user_repo.store_coin_account_worker_history(workers, now)
                    logger.info(f'{account.account_id}|{account.coin_id} - Stored')
        except Exception as e:
            logger.error(e)
        finally:
            await pool.release(con)
            logger.info(f'{account.account_id}|{account.coin_id} - Connection was released')


async def job():
    notifier = TelegramNotifier(TOKEN)

    pool = await get_pool(**postgres)
    logger.info(f'Job started')
    user_repo = UserRepository(await pool.acquire())
    accounts = await user_repo.get_all_account_to_refresh()
    logger.info(f'Total accounts to scrap {len(accounts)}')
    await pool.release(user_repo.connection)

    semaphore = asyncio.BoundedSemaphore(10)
    tasks = []

    for account in accounts:
        tasks.append(asyncio.ensure_future(update_account_data(semaphore, account, pool, notifier,)))

    await asyncio.gather(*tasks)
    logger.info(f'Terminating pool')
    await pool.close()


if (__name__ == "__main__"):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job, "interval", seconds=10)

    scheduler.start()

    asyncio.get_event_loop().run_forever()