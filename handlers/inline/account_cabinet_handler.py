from config import Coin
import typing
from aiogram import types
from database.user_repo import UserRepository

from keyboard_fabrics import menu_cb, payouts_cb, income_cb, worker_cb, delete_account_cb, notification_cb


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
            callback_data=worker_cb.new(
                id=account_id, page=1, type="s_coin" #s_coin = select_coin shorthand
            ),
        ),
    )

    keyboard_markup.add(
        types.InlineKeyboardButton(
            _["income_stat_button"],
            callback_data=income_cb.new(
                id=account_id, page=1, type="s_coin" #s_coin = select_coin shorthand
            ),
        ),
        types.InlineKeyboardButton(
            _["payouts_stat_button"],
            callback_data=payouts_cb.new(
                id=account_id, page=1, type='s_coin', #s_coin = select_coin shorthand
            ),
        ),
    )
    
    keyboard_markup.add(
        types.InlineKeyboardButton(
            _["notifcation_button"],
            callback_data=notification_cb.new(
                id=account_id, action="_", type='s_coin', #s_coin = select_coin shorthand
            ),
        ),
        types.InlineKeyboardButton(
            _["delete_account"],
            callback_data=delete_account_cb.new(
                id=account_id, action="choose"
            ),
        ),
    )

    
    keyboard_markup.add(
        types.InlineKeyboardButton(
            _["back_to_account_list_button"],
            callback_data=menu_cb.new(
                id="_", type="menu", action="main_menu"
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
