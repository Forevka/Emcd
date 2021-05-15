from config import TELEGRAM_DEFAULT_WAIT_TIME
from dataclasses import dataclass
from aiogram import Bot
from aiogram.utils import exceptions
from asyncpg.connection import Connection
from enums.telegram_send_result import TelegramSendResult
from loguru import logger

from notifier.base_notifier import BaseNotifier

@dataclass
class TelegramSendData:
    result: TelegramSendResult
    wait_time: int


class TelegramNotifier(BaseNotifier):
    def __init__(self, token: str):
        self.token = token
        self.bot = Bot(token=token, parse_mode='HTML', validate_token=False)


    async def send_message(self, user_id: int, text: str, con: Connection) -> TelegramSendData:
        """
        Safe messages sender
        :param user_id:
        :param text:
        :param disable_notification:
        :return:
        """
        try:
            await self.bot.send_message(user_id, text)
        except exceptions.BotBlocked:
            logger.warning(f"Target [ID:{user_id}]: blocked by user")
            return TelegramSendData(TelegramSendResult.Blocked, TELEGRAM_DEFAULT_WAIT_TIME)
        except exceptions.ChatNotFound:
            logger.warning(f"Target [ID:{user_id}]: invalid user ID")
            return TelegramSendData(TelegramSendResult.ChatNotFound, TELEGRAM_DEFAULT_WAIT_TIME)
        except exceptions.RetryAfter as e:
            logger.warning(f"Target [ID:{user_id}]: Flood limit is exceeded. Need to wait {e.timeout} seconds.")
            return TelegramSendData(TelegramSendResult.RetryAfter, e.timeout)
            #await asyncio.sleep(e.timeout)
            #return await send_message(user_id, text, notifier, con)  # Recursive call
        except exceptions.UserDeactivated:
            logger.warning(f"Target [ID:{user_id}]: user is deactivated")
            return TelegramSendData(TelegramSendResult.Deactivated, TELEGRAM_DEFAULT_WAIT_TIME)
        except exceptions.TelegramAPIError:
            logger.exception(f"Target [ID:{user_id}]: failed")
            return TelegramSendData(TelegramSendResult.ApiError, TELEGRAM_DEFAULT_WAIT_TIME)
        except Exception as e:
            logger.exception(f"Target [ID:{user_id}]: failed", e)
            return TelegramSendData(TelegramSendResult.Error, TELEGRAM_DEFAULT_WAIT_TIME)
        else:
            logger.info(f"Target [ID:{user_id}]: success")
            return TelegramSendData(TelegramSendResult.Ok, TELEGRAM_DEFAULT_WAIT_TIME)


    async def notify(self, text: str, con: Connection, user_id: int) -> TelegramSendData:
        return await self.send_message(user_id, text, con)


    async def close(self,):
        await self.bot.session.close()
