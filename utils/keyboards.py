from aiogram import types
from utils.lang import LangHolder
from utils.keyboard_fabrics import menu_cb

def keyboard_when_account_deleted(_: LangHolder) -> types.InlineKeyboardMarkup:
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

    keyboard_markup.add(
        types.InlineKeyboardButton(
            _["back_to_account_list_button"],
            callback_data=menu_cb.new(
                id="_", type="menu", action="main_menu"
            ),
        ),
    )

    return keyboard_markup