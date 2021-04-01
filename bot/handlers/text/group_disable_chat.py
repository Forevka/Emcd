from aiogram import types
from database.user_repo import UserRepository


async def non_private_message(message: types.Message, user: UserRepository, _: dict):
    message_text = f'''
    EMCD-Watcher currently support only private messages.
    Please use it only from private conversation with bot.

    If you see this message occasionaly contact with support.
    '''

    await message.answer(message_text)
