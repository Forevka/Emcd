from aiogram import Bot
from notifier.base_notifier import BaseNotifier
from asyncpg.connection import Connection


class TelegramNotifier(BaseNotifier):
    def __init__(self, token: str):
        self.token = token
        self.bot = Bot(token=token, parse_mode='HTML', validate_token=False)

    async def notify(self, text: str, con: Connection, user_id: int):
        await self.bot.send_message(user_id, text,)

    async def close(self,):
        await self.bot.close()