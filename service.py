import asyncio
from dataclasses import dataclass
from datetime import datetime
import logging
from typing import Dict
from utils.intercept_standart_logger import InterceptStandartHandler

from aiogram import exceptions
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asyncpg.pool import Pool
from loguru import logger

from config import CONNECTION_STRING, ENVIRONMENT, PAYOUTS_CHECK_START_DATETIME, POEDITOR_ID, POEDITOR_TOKEN, TOKEN, Lang
from database.db import get_pool
from database.models.account_coin import AccountCoin
from database.user_repo import UserRepository
from emcd_client.client import EmcdClient
from notifier.telegram_notifier import TelegramNotifier
from utils.utils import load_translations, load_translations_from_file
from enums.coin import Coin

logging.basicConfig(handlers=[InterceptStandartHandler()], level=logging.INFO)
logger.add("logs/service_{time}.log", rotation="12:00", serialize=True)

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
                    blacklisted_workers = [w.worker_id for w in await user_repo.get_blacklisted_workers(account.user_id)]

                    previous_worker_state = await user_repo.get_previous_worker_state_for_account(account.id)
                    for worker in workers:
                        previous_state = next((w for w in previous_worker_state if w.worker_id == worker.worker), None)
                        if (previous_state):
                            if (previous_state.status_id != worker.status_id):
                                logger.info(f'{account.account_id}|{account.coin_id} - worker changed status {worker.worker}')
                                if (worker.worker not in blacklisted_workers):
                                    change_status_descr.append(
                                        WorkerChangeStatusDataModel(
                                            previous_state.status_id,
                                            worker.status_id,
                                            previous_state.worker_id
                                        )
                                    )
                                else:
                                    logger.info(f'{account.account_id}|{account.coin_id} - {worker.worker} blacklisted')
                                    if (worker.status_id == -1):
                                        logger.info(f'{account.account_id}|{account.coin_id} - {worker.worker} dead, need to delete from blacklist')
                                        await user_repo.toggle_worker_blacklist(account.user_id, worker.worker)


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
                
                payouts = await client.get_payouts(account.coin_id)
                user_db = await user_repo.get_user(account.user_id)

                actual_payouts = [
                    p for p in payouts.payouts 
                    if p.timestamp > PAYOUTS_CHECK_START_DATETIME 
                    and p.timestamp > user_db.created_datetime.timestamp() 
                    and p.txid is not None 
                    and p.txid != ''
                ]

                if (actual_payouts):

                    user_locale = Lang(user_db.lang_id)
                    translation = texts[user_locale.name]
                    for payout in actual_payouts:
                        is_payout_notified = await user_repo.is_payout_notified(account.id, payout.timestamp,)
                        if (is_payout_notified == False):
                            coin = Coin(account.coin_id)

                            latest_account_data = await client.get_info()
                            latest_coin_data = latest_account_data.get_coins()[account.coin_id]

                            msg_text = translation['new_payout_received'].format(
                                account=user_account.username,
                                link=f'<a href="https://blockchair.com/{coin.name.lower()}/transaction/{payout.txid}">{payout.txid[8:]}</a>',
                                amount=payout.amount,
                                current_balance=format(latest_coin_data.balance, '.8f'),
                            )
                            try:
                                await notifier.notify(user_db.id, msg_text)
                            except exceptions.TelegramAPIError as e:
                                logger.error(f'aiogram error {e}')
                        
                            await user_repo.mark_payout_as_notified(account.id, payout.timestamp,)
        except Exception as e:
            logger.exception(e)
        finally:
            await pool.release(con)
            logger.info(f'{account.account_id}|{account.coin_id} - Connection was released')


async def job():
    notifier = TelegramNotifier(TOKEN)

    pool = None
    try:
        pool = await get_pool(CONNECTION_STRING)
        locales = await load_translations_from_file()
        if (ENVIRONMENT != 'debug'):
            logger.info('Loading from poeditor')
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
    except Exception as e:
        logger.exception(e)
    finally:
        logger.info(f'Terminating pool')
        if pool is not None:
            await pool.close()

        await notifier.bot.session.close()


if (__name__ == "__main__"):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job, "interval", seconds=30)

    scheduler.start()

    asyncio.get_event_loop().run_forever()
