import typing

from aiogram import types
from utils.lang import language_map
from enums.lang import Lang
from database.user_repo import UserRepository
from utils.keyboard_fabrics import lang_cb
from utils.utils import grouper


async def lang_list_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    btn_list = []
    inline_keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

    for lang in Lang:
        lang_id = lang.value
        if (lang_id is None):
            continue

        btn_list.append(
            types.InlineKeyboardButton(
                language_map[lang.name],
                callback_data=lang_cb.new(
                    id=lang_id,
                ),
            ),
        )

    for i in grouper(2, btn_list):
        inline_keyboard_markup.row(*i)

    await query.message.edit_text(_['choose_lang'], reply_markup=inline_keyboard_markup)

async def lang_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    from utils.lang import texts
    
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
    
