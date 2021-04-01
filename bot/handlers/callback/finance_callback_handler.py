import typing

from aiogram import types
from bot.common.keyboard_fabrics import finance_cb, menu_cb
from bot.common.lang import LangHolder
from bot.common.replies import reply_to_account_not_found
from database.user_repo import UserRepository
from enums.coin import Coin
from utils.utils import grouper

PER_PAGE = 5

async def finance_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: LangHolder,
):
    account_id = callback_data["id"]
    page = int(callback_data["page"])

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    
    account = next((acc for acc in await user.get_accounts(query.from_user.id) if str(acc.account_id) == account_id), None,)
    
    if (account is None):
        return await reply_to_account_not_found(query.message, _)
        
    btn_list = []

    for coin in await user.get_account_coins(query.from_user.id, account_id):
        if coin.is_active:
            btn_list.append(
                types.InlineKeyboardButton(
                    f"{Coin(coin.coin_id).name}",
                    callback_data=finance_cb.new(
                        id=account_id, type=coin.coin_id, action="payouts", page=page,
                    ),
                ),
            )

    for i in grouper(2, btn_list):
        keyboard_markup.add(*i)


    keyboard_markup.add(
        types.InlineKeyboardButton(
            _['back_to_account_button'],
            callback_data=menu_cb.new(id=account.account_id, type="account", action='open'),
        ),
    )
    
    await query.message.edit_text(
        _["finance_choose_coin"],
        reply_markup=keyboard_markup,
    )
