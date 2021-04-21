from aiogram import types
from bot.handlers.text.base_command_handler import BaseCommandHandler
from database.user_repo import UserRepository


class CmdThrow(BaseCommandHandler):
    async def handle(self, message: types.Message, user: UserRepository, _: dict):
        raise ValueError()

    __call__ = handle
    