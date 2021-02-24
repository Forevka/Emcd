import typing

from aiogram import types
from database.user_repo import UserRepository
from keyboard_fabrics import delete_account_cb, menu_cb

PER_PAGE = 5

async def delete_account_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    account_id = callback_data["id"]

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    
    account = next((acc for acc in await user.get_accounts(query.from_user.id) if str(acc.account_id) == account_id), None,)

    keyboard_markup.add(
        types.InlineKeyboardButton(
            _['yes'],
            callback_data=delete_account_cb.new(id=account.account_id, action='yes'),
        ),
        types.InlineKeyboardButton(
            _['no'],
            callback_data=delete_account_cb.new(id=account.account_id, action='no'),
        ),
    )
    
    await query.message.edit_text(
        _["delete_account_descr"].format(account_name=account.username),
        reply_markup=keyboard_markup,
    )


async def delete_account_confirmation_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    account_id = callback_data["id"]
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    
    keyboard_markup.add(
        types.InlineKeyboardButton(
            _["back_to_account_list_button"],
            callback_data=menu_cb.new(
                id="_", type="menu", action="main_menu"
            ),
        ),
    )

    await user.delete_account_notification_settings_account(account_id, query.from_user.id)
    await user.delete_user_account_coin(account_id, query.from_user.id)
    await user.delete_user_account(account_id, query.from_user.id)
    
    await query.message.edit_text(
        _['account_deleted_descr'],
        reply_markup=keyboard_markup,
    )
