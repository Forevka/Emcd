from enums.notify_channel import NotifyChannel
from enums.notify_type import NotifyType
from database.notification_repo import NotificationRepository
from typing import Dict, List

from aiogram import exceptions
from asyncpg.connection import Connection
from config import PAYOUTS_CHECK_START_DATETIME, TOKEN
from database.models.account_coin_notification_payout import \
    AccountCoinNotificationPayout
from database.user_repo import UserRepository
from enums.coin import Coin
from enums.lang import Lang
from loguru import logger
from notifier.telegram_notifier import TelegramNotifier
from third_party.emcd_client.client import EmcdClient

from background_service.base_background_service import BaseBackgroundService


class PayoutsMonitorService(BaseBackgroundService[AccountCoinNotificationPayout]):
    async def get_notifier(self,):
        return TelegramNotifier(TOKEN)

    async def get_items_to_process(self, con: Connection) -> List[AccountCoinNotificationPayout]:
        user_repo = UserRepository(con)
        return await user_repo.get_all_account_payouts_to_refresh()

    async def job(self, con: Connection, item: AccountCoinNotificationPayout, notifier: TelegramNotifier, locales: Dict):
        user_repo = UserRepository(con)
        notification_repo = NotificationRepository(con)

        async with EmcdClient(item.account_id, logger) as client:
            user_account = next((acc for acc in await user_repo.get_accounts(item.user_id) if acc.account_id == item.account_id), None)

            payouts = await client.get_payouts(item.coin_id)

            if (payouts is None):
                logger.info('payouts is none')
                return

            user_db = await user_repo.get_user(item.user_id)

            actual_payouts = [
                p for p in payouts.payouts 
                if p.timestamp > PAYOUTS_CHECK_START_DATETIME 
                and p.timestamp > item.notification_update_datetime.timestamp()
                and p.timestamp > item.account_created_datetime.timestamp()
                and p.txid is not None 
                and p.txid != ''
            ]

            if (actual_payouts):
                user_locale = Lang(user_db.lang_id)
                translation = locales[user_locale.name]
                for payout in actual_payouts:
                    is_payout_notified = await user_repo.is_payout_notified(item.id, payout.timestamp,)
                    if (is_payout_notified == False):
                        coin = Coin(item.coin_id)

                        latest_account_data = await client.get_info()
                        if (latest_account_data is None):
                            logger.info('account is none')
                            return

                        latest_coin_data = latest_account_data.get_coins()[item.coin_id]

                        msg_text = translation['new_payout_received'].format(
                            account=user_account.username,
                            link=f'<a href="https://blockchair.com/{coin.name.lower()}/transaction/{payout.txid}">{payout.txid[8:]}</a>',
                            amount=format(payout.amount, '.8f'),
                            current_balance=format(latest_coin_data.balance, '.8f'),
                        )
                        
                        await notification_repo.add(msg_text, NotifyType.Payout, [NotifyChannel.Telegram], user_db.id)
                    
                        await user_repo.mark_payout_as_notified(item.id, payout.timestamp,)
