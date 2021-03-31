import typing

from aiogram import types
from database.user_repo import UserRepository
from enums.coin import Coin
from utils.keyboard_fabrics import coin_account_cb
from utils.utils import grouper


async def change_coin_enabled_setting_coins_for_account(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    coin_id = callback_data["id"]

    is_active = callback_data['action'] == 'on'

    await user.change_coin_enabled(query.from_user.id, coin_id, is_active)
    await user.change_account_coin_enabled(query.from_user.id, coin_id, is_active)

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

    btn_list = []


    for coin in await user.get_coins(query.from_user.id,):
        if coin.is_enabled:
            btn_list.append(
                types.InlineKeyboardButton(
                    f"{Coin(coin.coin_id).name} ✅",
                    callback_data=coin_account_cb.new(
                        id=coin.coin_id, action="off"
                    ),
                ),
            )
        else:
            btn_list.append(
                types.InlineKeyboardButton(
                    f"{Coin(coin.coin_id).name} ❌",
                    callback_data=coin_account_cb.new(
                        id=coin.coin_id, action="on"
                    ),
                ),
            )

    for i in grouper(2, btn_list):
        keyboard_markup.add(*i)

    '''
    keyboard_markup.add(
        types.InlineKeyboardButton(
            _['back_to_account_button'],
            callback_data=menu_cb.new(id=account.account_id, type="account", action='open'),
        ),
    )
    '''

    await query.message.edit_text(
        _["coin_list_descr"],
        reply_markup=keyboard_markup,
    )
    await query.answer(_['coin_enabled'] if is_active else _['coin_disabled'])
