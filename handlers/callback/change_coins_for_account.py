import typing

from aiogram import types
from enums.coin import Coin
from database.user_repo import UserRepository
from keyboard_fabrics import coin_account_cb, menu_cb
from utils import grouper


async def change_coins_for_account_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
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
    
    '''keyboard_markup.add(
        types.InlineKeyboardButton(
            _["back_to_account_list_button"],
            callback_data=menu_cb.new(
                id="_", type="menu", action="main_menu"
            ),
        ),
    )'''

    await query.message.edit_text(
        _["coin_list_descr"],
        reply_markup=keyboard_markup,
    )
