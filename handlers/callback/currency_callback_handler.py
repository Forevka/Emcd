import typing
from utils.utils import grouper

from aiogram import types
from database.user_repo import UserRepository
from keyboard_fabrics import currency_cb


async def currency_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    currency_list = await user.get_available_currency()

    user_currency = await user.get_user_currency(query.from_user.id)

    inline_keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

    buttons = []

    for curr in currency_list:
        enabled = "❌"
        if (curr.id == user_currency.currency_id):
            enabled = "✅"

        buttons.append(
            types.InlineKeyboardButton(
                f"{enabled} {curr.currency_code}",
                callback_data=currency_cb.new(
                    id=curr.id, action=curr.id != user_currency.currency_id
                ),
            ),
        )

    for b_row in grouper(2, buttons):
        inline_keyboard_markup.row(
            *b_row
        )
    
    await query.message.edit_text(_['curr_list'], reply_markup=inline_keyboard_markup)


async def currency_update_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    new_user_currency = int(callback_data['id'])
    if (callback_data['action'] == 'False'):
        await query.answer(_['curr_update_unable'], show_alert=True)
        return

    await user.update_user_currency(query.from_user.id, new_user_currency)

    currency_list = await user.get_available_currency()

    user_currency = await user.get_user_currency(query.from_user.id)

    inline_keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

    buttons = []

    for curr in currency_list:
        enabled = "❌"
        if (curr.id == user_currency.currency_id):
            enabled = "✅"

        buttons.append(
            types.InlineKeyboardButton(
                f"{enabled} {curr.currency_code}",
                callback_data=currency_cb.new(
                    id=curr.id, action=curr.id != user_currency.currency_id
                ),
            ),
        )

    for b_row in grouper(2, buttons):
        inline_keyboard_markup.row(
            *b_row
        )
    
    await query.message.edit_text(_['curr_list'], reply_markup=inline_keyboard_markup)