from config import SELECT_COIN_CB
import typing

from aiogram import types
from enums.coin import Coin
from database.user_repo import UserRepository
from emcd_client.client import EmcdClient
from keyboard_fabrics import menu_cb, statistic_cb
from utils import grouper
from babel.numbers import format_currency

PER_PAGE = 5

async def statistic_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    account_id = callback_data["id"]

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    
    account = next((acc for acc in await user.get_accounts(query.from_user.id) if str(acc.account_id) == account_id), None,)
    
    btn_list = []

    for coin in await user.get_account_coins(query.from_user.id, account_id):
        if coin.is_active:
            btn_list.append(
                types.InlineKeyboardButton(
                    f"{Coin(coin.coin_id).name}",
                    callback_data=statistic_cb.new(
                        id=account_id, type=coin.coin_id,
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
        _["statistic_choose_coin"],
        reply_markup=keyboard_markup,
    )


async def statistic_info_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    account_id = callback_data["id"]
    coin_id = callback_data['type']

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    
    account = next((acc for acc in await user.get_accounts(query.from_user.id) if str(acc.account_id) == account_id), None,)

    account_coin = next((i for i in await user.get_account_coins(query.from_user.id, account_id) if i.coin_id == coin_id), None,)
    #incomes = None
    #async with EmcdClient(account_id) as client:
    #    incomes = await client.get_rewards(coin_id)

    buttons = []
    
    coins = [coin for coin in await user.get_account_coins(query.from_user.id, account_id) if coin.is_active]

    if (len(coins) == 1): #in case if enabled only one coin we treat them as default
        buttons.append(
            types.InlineKeyboardButton(
                _["cabinet"],
                callback_data=menu_cb.new(
                    id=account_id, type="account", action="open"
                ),
            ),
        )
    else:
        buttons.append(
            types.InlineKeyboardButton(
                _["back_to_statistic"],
                callback_data=statistic_cb.new(
                    id=account_id, type=SELECT_COIN_CB,
                ),
            ),
        )

    keyboard_markup.row(*buttons)

    account_api = None
    currency = None
    async with EmcdClient(account_id) as client:
        account_api = await client.get_info()
        currency = await client.get_currency()

    coin_info = account_api.get_coins()[coin_id]

    message_text = _['statistic_descr'].format(
        account_name=account.username,
        address=account_coin.address,
        current_balance=coin_info.balance,
        current_balance_dol=format_currency(round(coin_info.balance * currency['USD']['last'], 4), '', locale="en_US"),
        total_paid=coin_info.total_paid,
        total_paid_dol=format_currency(round(coin_info.total_paid * currency['USD']['last'], 4), '', locale="en_US"),
        course_dol=format_currency(round(currency['USD']['last'], 2), '', locale="en_US"),
        course_rub=format_currency(round(currency['RUB']['last'], 2), '', locale="en_US"),
    )

    await query.message.edit_text(
        message_text,
        reply_markup=keyboard_markup,
    )
