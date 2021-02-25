from aiogram import types
from config import Lang
from database.user_repo import UserRepository
from keyboard_fabrics import lang_cb

async def cmd_lang(
    message: types.Message, user: UserRepository, _: dict
):
    inline_keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

    inline_keyboard_markup.row(
        types.InlineKeyboardButton(
            "Русский",
            callback_data=lang_cb.new(
                id=Lang.ru.value,
            ),
        ),
    )
    
    inline_keyboard_markup.row(
        types.InlineKeyboardButton(
            "English",
            callback_data=lang_cb.new(
                id=Lang.en.value,
            ),
        ),
    )

    await message.answer(_['choose_lang'], reply_markup=inline_keyboard_markup)
    
