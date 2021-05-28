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
    message_id: int


class TelegramNotifier(BaseNotifier):
    def __init__(self, token: str):
        self.token = token
        self.bot = Bot(token=token, parse_mode='HTML', validate_token=False)


    async def send_message(self, user_id: int, text: str, con: Connection, reply_markup = None) -> TelegramSendData:
        """
        Safe messages sender
        :param user_id:
        :param text:
        :param disable_notification:
        :return:
        """
        message = None
        try:
            message = await self.bot.send_message(user_id, text, reply_markup=reply_markup)
        except exceptions.BotBlocked:
            logger.warning(f"Target [ID:{user_id}]: blocked by user")
            return TelegramSendData(TelegramSendResult.Blocked, TELEGRAM_DEFAULT_WAIT_TIME, -1)
        except exceptions.ChatNotFound:
            logger.warning(f"Target [ID:{user_id}]: invalid user ID")
            return TelegramSendData(TelegramSendResult.ChatNotFound, TELEGRAM_DEFAULT_WAIT_TIME, -1)
        except exceptions.RetryAfter as e:
            logger.warning(f"Target [ID:{user_id}]: Flood limit is exceeded. Need to wait {e.timeout} seconds.")
            return TelegramSendData(TelegramSendResult.RetryAfter, e.timeout, -1)
            #await asyncio.sleep(e.timeout)
            #return await send_message(user_id, text, notifier, con)  # Recursive call
        except exceptions.UserDeactivated:
            logger.warning(f"Target [ID:{user_id}]: user is deactivated")
            return TelegramSendData(TelegramSendResult.Deactivated, TELEGRAM_DEFAULT_WAIT_TIME, -1)
        except exceptions.TelegramAPIError:
            logger.exception(f"Target [ID:{user_id}]: failed")
            return TelegramSendData(TelegramSendResult.ApiError, TELEGRAM_DEFAULT_WAIT_TIME, -1)
        except Exception as e:
            logger.exception(f"Target [ID:{user_id}]: failed", e)
            return TelegramSendData(TelegramSendResult.Error, TELEGRAM_DEFAULT_WAIT_TIME, -1)
        else:
            logger.info(f"Target [ID:{user_id}]: success")
            return TelegramSendData(TelegramSendResult.Ok, TELEGRAM_DEFAULT_WAIT_TIME, message.message_id)


    async def notify(self, text: str, con: Connection, user_id: int, reply_markup = None) -> TelegramSendData:
        return await self.send_message(user_id, text, con, reply_markup=reply_markup)


    async def close(self,):
        await self.bot.session.close()
