import asyncio
from database.models.account_coin_notification_payout import AccountCoinNotificationPayout
import logging
from typing import Dict

from aiogram import exceptions
from aiogram.utils import exceptions
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asyncpg.pool import Pool
from loguru import logger

from config import (CONNECTION_STRING, ENVIRONMENT,
                    PAYOUTS_CHECK_START_DATETIME, POEDITOR_ID, POEDITOR_TOKEN,
                    TOKEN, Lang)
from database.db import get_pool
from database.user_repo import UserRepository
from third_party.emcd_client.client import EmcdClient
from enums.coin import Coin
from notifier.telegram_notifier import TelegramNotifier
from utils.intercept_standart_logger import InterceptStandartHandler
from utils.utils import load_translations, load_translations_from_file

logging.basicConfig(handlers=[InterceptStandartHandler()], level=logging.WARN)
logger.add("logs/payouts_service_{time}.log", rotation="12:00", serialize=True)

async def update_account_data(semaphore: asyncio.BoundedSemaphore, account: AccountCoinNotificationPayout, pool: Pool, notifier: TelegramNotifier, texts: Dict,):
    async with semaphore:
        logger.info(f'{account.account_id}|{account.coin_id} - Scraping payouts info')
        con = await pool.acquire()

        user_repo = UserRepository(con)

        try:
            async with EmcdClient(account.account_id) as client:
                user_account = next((acc for acc in await user_repo.get_accounts(account.user_id) if acc.account_id == account.account_id), None)

                payouts = await client.get_payouts(account.coin_id)

                if (payouts is None):
                    logger.warning('payouts is none')
                    return

                user_db = await user_repo.get_user(account.user_id)

                actual_payouts = [
                    p for p in payouts.payouts 
                    if p.timestamp > PAYOUTS_CHECK_START_DATETIME 
                    and p.timestamp > account.notification_update_datetime.timestamp()
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
                            if (latest_account_data is None):
                                logger.warning('account is none')
                                return

                            latest_coin_data = latest_account_data.get_coins()[account.coin_id]

                            msg_text = translation['new_payout_received'].format(
                                account=user_account.username,
                                link=f'<a href="https://blockchair.com/{coin.name.lower()}/transaction/{payout.txid}">{payout.txid[8:]}</a>',
                                amount=payout.amount,
                                current_balance=format(latest_coin_data.balance, '.8f'),
                            )
                            try:
                                await notifier.notify(user_db.id, msg_text)
                            except (exceptions.BotBlocked, exceptions.UserDeactivated) as e:
                                logger.warning(f'{account.user_id} blocked bot or deactivated they telegram account, disabling notifications')
                                await user_repo.update_notification_setting(account.user_id, False)
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
        accounts = await user_repo.get_all_account_payouts_to_refresh()
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
