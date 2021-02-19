from config import Coin
from emcd_client.client import EmcdClient
from finite_state_machine import Form
import typing
from aiogram import types
from database.user_repo import UserRepository

from keyboard_fabrics import menu_cb


async def account_cabinet_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    # id=account.account_id, type="account", action='open'
    account_id = callback_data["id"]

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

    keyboard_markup.add(
        types.InlineKeyboardButton(
            _["change_coins_button"],
            callback_data=menu_cb.new(
                id=account_id, type="account", action="c_coins"
            ),
        ),
        types.InlineKeyboardButton(
            _["workers_stat_button"],
            callback_data=menu_cb.new(
                id=account_id, type="account", action="w_stat"
            ),
        ),
    )

    keyboard_markup.add(
        types.InlineKeyboardButton(
            _["income_stat_button"],
            callback_data=menu_cb.new(
                id=account_id, type="account", action="i_stat"
            ),
        ),
        types.InlineKeyboardButton(
            _["payouts_stat_button"],
            callback_data=menu_cb.new(
                id=account_id, type="account", action="p_stat"
            ),
        ),
    )
    
    keyboard_markup.add(
        types.InlineKeyboardButton(
            _["notifcation_button"],
            callback_data=menu_cb.new(
                id=account_id, type="account", action="n_set"
            ),
        ),
        types.InlineKeyboardButton(
            _["delete_account"],
            callback_data=menu_cb.new(
                id=account_id, type="account", action="del"
            ),
        ),
    )

    coins_list = ""
    for coin in await user.get_account_coins(query.from_user.id, account_id):
        if coin.is_active:
            coins_list += f"\n{Coin(coin.coin_id).name}"

    account = next((acc for acc in await user.get_accounts(query.from_user.id) if str(acc.account_id) == account_id), None,)

    await query.message.edit_text(
        _["account_cabinet"].format(
            account_name=account.username, coins_list=coins_list
        ),
        reply_markup=keyboard_markup,
    )
