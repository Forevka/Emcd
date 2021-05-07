import asyncio
from enums.notify_type import NotifyType
from typing import Dict, List

from asyncpg.connection import Connection
from background_service.base_background_service import BaseBackgroundService
from config import TOKEN
from database.models.notification_queue import NotificationQueue
from database.notification_repo import NotificationRepository
from database.user_repo import UserRepository
from enums.notify_channel import NotifyChannel
from enums.notify_status import NotifyStatus
from enums.telegram_send_result import TelegramSendResult
from loguru import logger
from notifier.telegram_notifier import TelegramNotifier


class TelegramNotificationSenderService(BaseBackgroundService[NotificationQueue]):
    def __init__(self, connection_string: str, max_workers: int = 10,):
        super().__init__(connection_string, max_workers=max_workers)
        self.is_throttled = False

    async def get_notifier(self,):
        return TelegramNotifier(TOKEN)

    async def get_items_to_process(self, con: Connection) -> List[NotificationQueue]:
        repo = NotificationRepository(con)

        self.is_throttled = await repo.is_throttled(NotifyChannel.Telegram.value)
        if (not self.is_throttled):
            return await repo.get_page(NotifyStatus.New.value, NotifyChannel.Telegram.value, 50, 1)

        logger.warning("telegram throttled")
        return []
        

    async def job(self, con: Connection, item: NotificationQueue, notifier: TelegramNotifier, locales: Dict):
        if (self.is_throttled):
            logger.warning(f'already throttled by telegram, skipping loaded items')
            return

        user_repo = UserRepository(con)
        notification_repo = NotificationRepository(con)

        result = await notifier.notify(item.content, con, item.user_id,)

        item.result = result.result.value

        if (result.result not in [TelegramSendResult.RetryAfter]):
            await asyncio.sleep(result.wait_time)

            if (result.result in [TelegramSendResult.Ok]):
                item.status_id = NotifyStatus.Sent.value

            elif (result.result in [TelegramSendResult.Blocked, TelegramSendResult.Deactivated, TelegramSendResult.ChatNotFound,]):
                logger.warning(f'{item.user_id} blocked bot or deactivated they telegram account, disabling notifications')
                item.status_id = NotifyStatus.Failed.value
                if (item.type_id == NotifyType.Payout):
                    await user_repo.update_notification_payouts_setting(item.user_id, False)
                elif (item.type_id == NotifyType.Worker):
                    await user_repo.update_notification_setting(item.user_id, False)
            
            elif (result.result in [TelegramSendResult.ApiError, TelegramSendResult.Error]):
                logger.warning(f'{item.user_id} api error. will try to send in next start')
                item.status_id = NotifyStatus.New.value

        else:
            self.is_throttled = True
            item.status_id = NotifyStatus.New.value
            await notification_repo.create_throttled_record(item.channel_id, result.wait_time)
            
        await notification_repo.update(item)
