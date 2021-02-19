from database.user_repo import UserRepository
from aiogram import types

from keyboard_fabrics import menu_cb

async def cmd_cabinet(message: types.Message, user: UserRepository, _: dict):
    user_accounts = await user.get_accounts(message.from_user.id)
    
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)

    message_text = _['cabinet_msg']
    if (len(user_accounts) == 0):
        message_text += "\n\n" + _['add_account']
    else:
        for i, account in enumerate(user_accounts):
            keyboard_markup.add(
                types.InlineKeyboardButton(
                    f'#{i + 1} - {account.username}',
                    callback_data=menu_cb.new(id=account.account_id, type="account", action='open'),
                )
            )

    keyboard_markup.add(
        types.InlineKeyboardButton(
            _['add_account_btn'],
            callback_data=menu_cb.new(id='_', type="account", action='new'),
        )
    )

    await message.answer(message_text.format(account_count=len(user_accounts)), reply_markup=keyboard_markup)