from aiogram import types
from bot.handlers.text.base_command_handler import BaseCommandHandler
from database.user_repo import UserRepository


class UnhandledText(BaseCommandHandler):
    async def handle(self, message: types.Message, user: UserRepository, _: dict):
        ...
        
    __call__ = handle
