from aiogram import types
from database.user_repo import UserRepository
from utils.keyboard_fabrics import lang_cb, delete_account_cb, notification_cb, coins_cb, menu_cb, currency_cb


async def cmd_settings(message: types.Message, user: UserRepository, _: dict):
    inline_keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

    inline_keyboard_markup.row(
        types.InlineKeyboardButton(
            _["delete_account"],
            callback_data=delete_account_cb.new(
                id="_", action="choose"
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
            callback_data=notification_cb.new(
                action="_",
            ),
        ),
        types.InlineKeyboardButton(
            _['change_coins_button'],
            callback_data=menu_cb.new(
                id="_", type="account", action="c_coins"
            ),
        ),
    )

    inline_keyboard_markup.row(
        types.InlineKeyboardButton(
            _["curr_list_button"],
            callback_data=currency_cb.new(
                action="open", id="_",
            ),
        ),
    )
    
    await message.answer(_['setting_descr'], reply_markup=inline_keyboard_markup)
