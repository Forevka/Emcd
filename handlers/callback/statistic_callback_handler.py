import typing

from aiogram import types
from config import Coin
from database.user_repo import UserRepository
from emcd_client.client import EmcdClient
from keyboard_fabrics import income_cb, menu_cb, statistic_cb
from utils import grouper

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
    '''
    if (page > 1):
        buttons.append(
            types.InlineKeyboardButton(
                _["prev_button"],
                callback_data=income_cb.new(
                    id=account_id, page=page - 1, type=coind_id,
                ),
            ),
        )
    '''

    buttons.append(
        types.InlineKeyboardButton(
            _["back_to_statistic"],
            callback_data=statistic_cb.new(
                id=account_id, type='s_coin',
            ),
        ),
    )

    '''
    if (incomes):
        for income in incomes.income[(page - 1) * PER_PAGE: page * PER_PAGE]:
            message_text += f'\n{income.gmt_time} {_["income_names"][income.type.name.lower()]} {income.total_hashrate} {income.income}'

        if (len(incomes.income) > page * PER_PAGE):
            buttons.append(
                types.InlineKeyboardButton(
                    _["next_button"],
                    callback_data=income_cb.new(
                        id=account_id, page=page + 1, type=coind_id,
                    ),
                ),
            )
    '''
    keyboard_markup.row(*buttons)
    
    message_text = _['statistic_descr'].format(
        account_name=account.username,
        address=account_coin.address,
        current_balance=0.0,
        current_balance_dol=0.0,
        total_paid=0.0,
        total_paid_dol=0.0,
        course_dol=0.0,
        course_rub=0.0,
    )

    await query.message.edit_text(
        message_text,
        reply_markup=keyboard_markup,
    )