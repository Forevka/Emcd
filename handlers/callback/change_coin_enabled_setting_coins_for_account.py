import typing

from aiogram import types
from config import Coin
from database.user_repo import UserRepository
from keyboard_fabrics import coin_account_cb, menu_cb
from utils import grouper


async def change_coin_enabled_setting_coins_for_account(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    coin_account_id = int(callback_data["id"])

    is_active = callback_data['action'] == 'on'

    await user.change_coin_enabled(coin_account_id, is_active)

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

    btn_list = []

    coin_account = await user.get_account_coins_by_id(coin_account_id)

    for coin in await user.get_account_coins(query.from_user.id, coin_account.account_id):
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

    account = next((acc for acc in await user.get_accounts(query.from_user.id) if str(acc.account_id) == str(coin_account.account_id)), None,)

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
    await query.answer(_['coin_enabled'] if is_active else _['coin_disabled'])
