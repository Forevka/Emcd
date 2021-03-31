from utils.common_replies import reply_to_account_not_found
from utils.lang import LangHolder
from config import SELECT_COIN_CB
import typing

from aiogram import types
from database.user_repo import UserRepository
from utils.keyboard_fabrics import finance_cb, menu_cb, statistic_cb, worker_cb, worker_black_cb


async def account_cabinet_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: LangHolder,
):
    # id=account.account_id, type="account", action='open'
    account_id = callback_data["id"]

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    action_type = SELECT_COIN_CB
    
    account = next((acc for acc in await user.get_accounts(query.from_user.id) if str(acc.account_id) == str(account_id)), None,)

    if (account is None):
        return await reply_to_account_not_found(query.message, _)

    coins = [coin for coin in await user.get_account_coins(query.from_user.id, account_id) if coin.is_active]

    if (len(coins) == 1): #in case if enabled only one coin we treat them as default
        action_type = coins[0].coin_id

    keyboard_markup.add(
        types.InlineKeyboardButton(
            _["workers_stat_button"],
            callback_data=worker_cb.new(
                id=account_id, page=1, type=action_type, status_id=3,
            ),
        ),
        types.InlineKeyboardButton(
            _["workers_black_list_button"],
            callback_data=worker_black_cb.new(
                id=account_id, page=1, type=action_type, action="_",
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


    await query.message.edit_text(
        _["account_cabinet"].format(
            account_name=account.username
        ),
        reply_markup=keyboard_markup,
    )
