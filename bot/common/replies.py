
from bot.common.lang import LangHolder
from bot.common.keyboards import keyboard_when_account_deleted
from aiogram import types

async def reply_to_account_not_found(message: types.Message, _: LangHolder):
    keyboard_markup = keyboard_when_account_deleted(_)

    return await message.edit_text(
        _["account_not_found_in_db"],
        reply_markup=keyboard_markup,
    )