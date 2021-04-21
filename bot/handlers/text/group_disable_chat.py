from bot.handlers.text.base_command_handler import BaseCommandHandler
from aiogram import types
from database.user_repo import UserRepository

text_for_non_private = f'''
EMCD-Watcher currently support only private messages.
Please use it only from private conversation with bot.

If you see this message occasionaly contact with support.
'''

class TextNonPrivateGuard(BaseCommandHandler):
    async def handle(self, message: types.Message, user: UserRepository, _: dict):
        await message.answer(text_for_non_private)

    __call__ = handle