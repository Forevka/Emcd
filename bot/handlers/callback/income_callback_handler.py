import logging
import typing
from math import ceil

from aiogram import types
from bot.common.keyboard_fabrics import (finance_cb, income_cb, menu_cb,
                                         payouts_cb)
from bot.common.lang import LangHolder
from bot.common.replies import reply_to_account_not_found
from config import PER_PAGE_INCOME, SELECT_COIN_CB
from database.user_repo import UserRepository
from enums.coin import Coin
from third_party.emcd_client.client import EmcdClient
from utils.utils import grouper


async def income_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: LangHolder,
):
    account_id = callback_data["id"]
    page = int(callback_data['page'])

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    
    account = next((acc for acc in await user.get_accounts(query.from_user.id) if str(acc.account_id) == account_id), None,)
    
    if (account is None):
        await query.answer()
        return await reply_to_account_not_found(query.message, _)
        
    btn_list = []

    for coin in await user.get_account_coins(query.from_user.id, account_id):
        if coin.is_active:
            btn_list.append(
                types.InlineKeyboardButton(
                    f"{Coin(coin.coin_id).name}",
                    callback_data=income_cb.new(
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
        _["income_choose_coin"],
        reply_markup=keyboard_markup,
    )
    await query.answer()


async def income_info_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: LangHolder,
    logger: logging.Logger,
):
    account_id = callback_data["id"]
    coind_id = callback_data['type']
    page = int(callback_data['page'])

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    
    account = next((acc for acc in await user.get_accounts(query.from_user.id) if str(acc.account_id) == account_id), None,)

    if (account is None):
        await query.answer()
        return await reply_to_account_not_found(query.message, _)

    incomes = None
    async with EmcdClient(account_id, logger) as client:
        incomes = await client.get_rewards(coind_id)

    if (incomes is None):
        await query.answer()
        logger.warning('incomes is none')
        return

    message_text = _['income']

    buttons = []

    if (page > 1):
        buttons.append(
            types.InlineKeyboardButton(
                _["prev_button"],
                callback_data=income_cb.new(
                    id=account_id, page=page - 1, type=coind_id,
                ),
            ),
        )

    if (incomes.income):
        buttons.append(
            types.InlineKeyboardButton(
                f"{page}/{ceil(len(incomes.income) / PER_PAGE_INCOME)}",
                callback_data="do_nothing"
            ),
        )

    if (incomes):
        for income in incomes.income[(page - 1) * PER_PAGE_INCOME: page * PER_PAGE_INCOME]:
            message_text += '\n' + _['income_template'].format(
                datetime=income.gmt_time,
                amount=format(income.income, '.8f'),
            )

        if (len(incomes.income) > page * PER_PAGE_INCOME):
            buttons.append(
                types.InlineKeyboardButton(
                    _["next_button"],
                    callback_data=income_cb.new(
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
            _["payouts_stat_button"],
            callback_data=payouts_cb.new(
                id=account_id, page=1, type=coind_id,
            ),
        ),
        types.InlineKeyboardButton(
            _['back_to_account_button'],
            callback_data=menu_cb.new(id=account.account_id, type="account", action='open'),
        ) if len(coins) == 1 else types.InlineKeyboardButton(
            _["back_to_income"],
            callback_data=finance_cb.new(
                id=account_id, type=action_type, action=SELECT_COIN_CB, page=page, #id=account_id, type=coin.coin_id, action=, page=page,
            ),
        ),
    )
    
    await query.message.edit_text(
        message_text,
        reply_markup=keyboard_markup,
    )
    await query.answer()
