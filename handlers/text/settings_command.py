from aiogram import types
from config import DEFAULT_LANG, Lang
from database.user_repo import UserRepository
from keyboard_fabrics import lang_cb


async def cmd_settings(message: types.Message, user: UserRepository, _: dict):
    inline_keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

    inline_keyboard_markup.row(
        types.InlineKeyboardButton(
            _["delete_account"],
            callback_data=lang_cb.new(
                id=Lang.ru.value,
            ),
        ),
        types.InlineKeyboardButton(
            _['language'],
            callback_data=lang_cb.new(
                id="_",
            ),
        ),
    )

    inline_keyboard_markup.row(
        types.InlineKeyboardButton(
            _["notifcation_button"],
            callback_data=lang_cb.new(
                id=Lang.ru.value,
            ),
        ),
        types.InlineKeyboardButton(
            _['change_coins_button'],
            callback_data=lang_cb.new(
                id=Lang.en.value,
            ),
        ),
    )
    
    await message.answer(_['choose_lang'], reply_markup=inline_keyboard_markup)
