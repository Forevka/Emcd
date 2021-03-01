import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Dict

from aiogram import exceptions
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asyncpg.pool import Pool
from loguru import logger

from config import CONNECTION_STRING, POEDITOR_ID, POEDITOR_TOKEN, TOKEN, Lang
from database.db import get_pool
from database.models.account_coin import AccountCoin
from database.user_repo import UserRepository
from emcd_client.client import EmcdClient
from notifier.telegram_notifier import TelegramNotifier
from utils import load_translations


@dataclass
class WorkerChangeStatusDataModel:
    old_status: int
    new_status: int
    name: str

    def to_description(self, text: str, localisation: Dict[str, str]) -> str:
        return text.format(
            worker_name=self.name, 
            previous_status=localisation[f'status_{self.old_status}'], 
            new_status=localisation[f'status_{self.new_status}'],
        )

async def update_account_data(semaphore: asyncio.BoundedSemaphore, account: AccountCoin, pool: Pool, notifier: TelegramNotifier, texts: Dict,):
    async with semaphore:
        logger.info(f'{account.account_id}|{account.coin_id} - Scraping workers info')
        con = await pool.acquire()

        now = datetime.now()

        message_text = ''

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
                    user_db = await user_repo.get_user(account.user_id)

                    user_locale = Lang(user_db.lang_id)
                    translation = texts[user_locale.name]

                    change_status_descr = []

                    previous_worker_state = await user_repo.get_previous_worker_state_for_account(account.id)
                    for worker in workers:
                        previous_state = next((w for w in previous_worker_state if w.worker_id == worker.worker), None)
                        if (previous_state):
                            if (previous_state.status_id != worker.status_id):
                                logger.info(f'{account.account_id}|{account.coin_id} - worker changed status {worker.worker}')

                                change_status_descr.append(
                                    WorkerChangeStatusDataModel(
                                        previous_state.status_id,
                                        worker.status_id,
                                        previous_state.worker_id
                                    )
                                )

                    logger.info(f'{account.account_id}|{account.coin_id} - Sending notification {account.id}')
                    if (change_status_descr):
                        descr = [st.to_description(translation['worker_changed_status_descr'], translation) for st in change_status_descr]
                        message_text = translation['worker_changed_status_body'].format(account_name=user_account.username, description='\n'.join([i for i in descr]))
                        try:
                            await notifier.notify(user_db.id, message_text)
                        except exceptions.TelegramAPIError as e:
                            logger.error(f'aiogram error {e}')

                    logger.info(f'{account.account_id}|{account.coin_id} - Clean up worker history {account.id}')
                    await user_repo.cleanup_worker_history_for_account(account.id)

                    logger.info(f'{account.account_id}|{account.coin_id} - Storing to database')

                    await user_repo.store_coin_account_worker_history(workers, now)
                    logger.info(f'{account.account_id}|{account.coin_id} - Stored')
        except Exception as e:
            logger.exception(e)
        finally:
            await pool.release(con)
            logger.info(f'{account.account_id}|{account.coin_id} - Connection was released')


async def job():
    notifier = TelegramNotifier(TOKEN)

    pool = await get_pool(CONNECTION_STRING)
    locales = await load_translations(POEDITOR_ID, POEDITOR_TOKEN)
    logger.info(f'Job started')
    user_repo = UserRepository(await pool.acquire())
    accounts = await user_repo.get_all_account_to_refresh()
    logger.info(f'Total accounts to scrap {len(accounts)}')
    await pool.release(user_repo.connection)

    semaphore = asyncio.BoundedSemaphore(10)
    tasks = []

    for account in accounts:
        tasks.append(asyncio.ensure_future(update_account_data(semaphore, account, pool, notifier, locales)))

    await asyncio.gather(*tasks)
    logger.info(f'Terminating pool')
    await pool.close()

    await notifier.bot.session.close()


if (__name__ == "__main__"):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job, "interval", seconds=10)

    scheduler.start()

    asyncio.get_event_loop().run_forever()
