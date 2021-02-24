import typing

from aiogram import types
from config import Coin
from database.user_repo import UserRepository
from keyboard_fabrics import coin_account_cb, menu_cb
from utils import grouper


async def change_coins_for_account_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    account_id = callback_data["id"]

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

    btn_list = []

    for coin in await user.get_account_coins(query.from_user.id, account_id):
        if coin.is_active:
            btn_list.append(
                types.InlineKeyboardButton(
                    f"{Coin(coin.coin_id).name} ✅",
                    callback_data=coin_account_cb.new(
                        id=coin.id, action="off"
                    ),
                ),
            )
        else:
            btn_list.append(
                types.InlineKeyboardButton(
                    f"{Coin(coin.coin_id).name} ❌",
                    callback_data=coin_account_cb.new(
                        id=coin.id, action="on"
                    ),
                ),
            )

    for i in grouper(2, btn_list):
        keyboard_markup.add(*i)
    
    account = next((acc for acc in await user.get_accounts(query.from_user.id) if str(acc.account_id) == account_id), None,)

    keyboard_markup.add(
        types.InlineKeyboardButton(
            _['back_to_account_button'],
            callback_data=menu_cb.new(id=account.account_id, type="account", action='open'),
        ),
    )
    await query.message.edit_text(
        _["coin_list_descr"].format(
            account_name=account.username
        ),
        reply_markup=keyboard_markup,
    )
