import typing

from aiogram import types
from config import Lang
from database.user_repo import UserRepository
from keyboard_fabrics import lang_cb

async def lang_list_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
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

    await query.message.edit_text(_['choose_lang'], reply_markup=inline_keyboard_markup)

async def lang_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    from config import texts
    
    lang_id = int(callback_data["id"])
    lang_name = Lang(lang_id).name

    await user.update_user_lang(query.from_user.id, lang_id)

    _ = texts[lang_name]
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    btns_text = (_['cabinet'], _['faq'])
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))
    keyboard_markup.row(_['setting'])

    await query.message.delete()

    await query.message.answer(_['lang_changed'], reply_markup=keyboard_markup)
    
