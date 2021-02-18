from config import DEFAULT_LANG
from database.user_repo import UserRepository
from aiogram import types
from asyncpg.connection import Connection

async def cmd_start(message: types.Message, user: UserRepository, _: dict):
    """
    Conversation's entry point
    """

    await user.create(message.from_user.id, int(DEFAULT_LANG.value))

    keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    btns_text = (_['cabinet'], _['faq'])
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))

    await message.answer(_['hello'], reply_markup=keyboard_markup)