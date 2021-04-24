import typing

from aiogram import types
from database.user_repo import UserRepository
from bot.common.keyboard_fabrics import menu_cb


async def cabinet_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    user_accounts = await user.get_accounts(query.from_user.id)

    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)

    message_text = _["cabinet_msg"]
    if len(user_accounts) == 0:
        message_text += "\n\n" + _["add_account"]
    else:
        for i, account in enumerate(user_accounts):
            keyboard_markup.add(
                types.InlineKeyboardButton(
                    f"#{i + 1} - {account.username}",
                    callback_data=menu_cb.new(
                        id=account.account_id, type="account", action="open"
                    ),
                )
            )

    keyboard_markup.add(
        types.InlineKeyboardButton(
            _["add_account_btn"],
            callback_data=menu_cb.new(id="_", type="account", action="new"),
        )
    )

    await query.message.edit_text(
        message_text.format(
            account_count=len(user_accounts),
        ),
        reply_markup=keyboard_markup,
    )
    await query.answer()
