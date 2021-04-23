import typing

from aiogram import types
from database.user_repo import UserRepository
from bot.common.replies import reply_to_account_not_found
from bot.common.keyboard_fabrics import delete_account_cb, menu_cb
from bot.common.lang import LangHolder


async def delete_account_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: LangHolder,
):
    account_id = callback_data["id"]

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

    if (account_id == "_"):
        user_accounts = await user.get_accounts(query.from_user.id)
        for i, account in enumerate(user_accounts):
            keyboard_markup.add(
                types.InlineKeyboardButton(
                    f"#{i + 1} - {account.username}",
                    callback_data=delete_account_cb.new(id=account.account_id, action='choose'),
                )
            )
        
        await query.answer()
        return await query.message.edit_text(
            _["choose_account_to_delete"],
            reply_markup=keyboard_markup,
        )
        
    
    account = next((acc for acc in await user.get_accounts(query.from_user.id) if str(acc.account_id) == account_id), None,)
    
    if (account is None):
        await query.answer()
        return await reply_to_account_not_found(query.message, _)

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
    await query.answer()


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
    await query.answer()
