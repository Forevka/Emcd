from config import SELECT_COIN_CB
import typing

from aiogram import types
from enums.coin import Coin
from database.user_repo import UserRepository
from handlers.callback.finance_callback_handler import finance_callback_handler
from keyboard_fabrics import finance_cb, menu_cb, statistic_cb, worker_cb


async def account_cabinet_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    # id=account.account_id, type="account", action='open'
    account_id = callback_data["id"]

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    action_type = SELECT_COIN_CB

    coins = [coin for coin in await user.get_account_coins(query.from_user.id, account_id) if coin.is_active]

    if (len(coins) == 1): #in case if enabled only one coin we treat them as default
        action_type = coins[0].coin_id

    keyboard_markup.add(
        types.InlineKeyboardButton(
            _["workers_stat_button"],
            callback_data=worker_cb.new(
                id=account_id, page=1, type=action_type,
            ),
        ),
    )

    keyboard_markup.add(
        types.InlineKeyboardButton(
            _["statistic_button"],
            callback_data=statistic_cb.new(
                id=account_id, type=action_type,
            ),
        ),
        types.InlineKeyboardButton(
            _["finance_button"],
            callback_data=finance_cb.new(
                id=account_id, type=action_type, action="_" if action_type == SELECT_COIN_CB else "payouts", page=1, #id=account_id, type=coin.coin_id, action=, page=page,
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

    account = next((acc for acc in await user.get_accounts(query.from_user.id) if str(acc.account_id) == account_id), None,)

    await query.message.edit_text(
        _["account_cabinet"].format(
            account_name=account.username
        ),
        reply_markup=keyboard_markup,
    )
