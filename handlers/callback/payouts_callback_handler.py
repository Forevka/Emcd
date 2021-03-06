from config import SELECT_COIN_CB
import typing
from math import ceil

from aiogram import types
from enums.coin import Coin
from database.user_repo import UserRepository
from emcd_client.client import EmcdClient
from keyboard_fabrics import income_cb, menu_cb, payouts_cb, finance_cb
from utils import grouper

PER_PAGE = 3

async def payouts_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    account_id = callback_data["id"]
    page = int(callback_data['page'])

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    
    account = next((acc for acc in await user.get_accounts(query.from_user.id) if str(acc.account_id) == account_id), None,)
    
    btn_list = []

    for coin in await user.get_account_coins(query.from_user.id, account_id):
        if coin.is_active:
            btn_list.append(
                types.InlineKeyboardButton(
                    f"{Coin(coin.coin_id).name}",
                    callback_data=payouts_cb.new(
                        id=account_id, page=page, type=coin.coin_id,
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
        _["payouts_choose_coin"],
        reply_markup=keyboard_markup,
    )


async def payouts_info_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    account_id = callback_data["id"]
    coind_id = callback_data['type']
    page = int(callback_data['page'])

    coin_name = Coin(coind_id).name.lower()

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    
    account = next((acc for acc in await user.get_accounts(query.from_user.id) if str(acc.account_id) == account_id), None,)

    payouts = None
    async with EmcdClient(account_id) as client:
        payouts = await client.get_payouts(coind_id)

    message_text = _['payouts']

    buttons = []

    if (page > 1):
        buttons.append(
            types.InlineKeyboardButton(
                _["prev_button"],
                callback_data=payouts_cb.new(
                    id=account_id, page=page - 1, type=coind_id,
                ),
            ),
        )

    buttons.append(
        types.InlineKeyboardButton(
            f"{page}/{ceil(len(payouts.payouts) / PER_PAGE)}",
            callback_data="do_nothing"
        ),
    )

    if (payouts):
        for payout in payouts.payouts[(page - 1) * PER_PAGE: page * PER_PAGE]:
            message_text += '\n' + _['payouts_template'].format(
                datetime=payout.gmt_time,
                amount=payout.amount,
                transaction_link=f'<a href="https://blockchair.com/{coin_name}/transaction/{payout.txid}">{payout.txid[8:]}</a>'
            )

        if (len(payouts.payouts) > page * PER_PAGE):
            buttons.append(
                types.InlineKeyboardButton(
                    _["next_button"],
                    callback_data=payouts_cb.new(
                        id=account_id, page=page + 1, type=coind_id,
                    ),
                ),
            )
        
    keyboard_markup.row(*buttons)
    action_type = SELECT_COIN_CB

    coins = [coin for coin in await user.get_account_coins(query.from_user.id, account_id) if coin.is_active]

    if (len(coins) == 1): #in case if enabled only one coin we treat them as default
        action_type = coins[0].coin_id

    keyboard_markup.row(
        types.InlineKeyboardButton(
            _["income_stat_button"],
            callback_data=income_cb.new(
                id=account_id, page=1, type=coind_id,
            ),
        ),
        types.InlineKeyboardButton(
            _['back_to_account_button'],
            callback_data=menu_cb.new(id=account.account_id, type="account", action='open'),
        ) if len(coins) == 1 else types.InlineKeyboardButton(
            _["back_to_payouts"],
            callback_data=finance_cb.new(
                id=account_id, type=action_type, action=SELECT_COIN_CB, page=page, #id=account_id, type=coin.coin_id, action=, page=page,
            ),
        ),
    )
    
    await query.message.edit_text(
        message_text,
        reply_markup=keyboard_markup,
        disable_web_page_preview=True,
    )
