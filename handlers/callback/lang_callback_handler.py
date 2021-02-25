import typing

from aiogram import types
from config import Lang
from database.user_repo import UserRepository
from config import texts


async def lang_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    lang_id = int(callback_data["id"])
    lang_name = Lang(lang_id).name

    await user.update_user_lang(query.from_user.id, lang_id)

    _ = texts[lang_name]
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    btns_text = (_['cabinet'], _['faq'])
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))
    keyboard_markup.row(_['language'])

    await query.message.delete()

    await query.message.answer(_['lang_changed'], reply_markup=keyboard_markup)
    
