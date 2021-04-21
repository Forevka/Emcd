from bot.handlers.text.base_command_handler import BaseCommandHandler
from aiogram import types
from database.user_repo import UserRepository

class TextNonPrivateGuard(BaseCommandHandler):
    async def handle(self, message: types.Message, user: UserRepository, _: dict):
        message_text = f'''
        EMCD-Watcher currently support only private messages.
        Please use it only from private conversation with bot.

        If you see this message occasionaly contact with support.
        '''

        await message.answer(message_text)

    __call__ = handle