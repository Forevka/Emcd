import logging
import typing
from math import ceil

from aiogram import types
import loguru
from config import PER_PAGE_BLACK_LIST, SELECT_COIN_CB
from database.user_repo import UserRepository
from enums.coin import Coin
from third_party.emcd_client.client import EmcdClient
from bot.common.replies import reply_to_account_not_found
from bot.common.keyboard_fabrics import menu_cb, worker_black_cb
from bot.common.lang import LangHolder
from utils.utils import grouper


async def black_list_callback_handler(
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
        return await reply_to_account_not_found(query.message, _)
        
    btn_list = []

    for coin in await user.get_account_coins(query.from_user.id, account_id):
        if coin.is_active:
            btn_list.append(
                types.InlineKeyboardButton(
                    f"{Coin(coin.coin_id).name}",
                    callback_data=worker_black_cb.new(
                        id=account_id, page=page, type=coin.coin_id, action="_"
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
        _["worker_blacklist_choose_coin"],
        reply_markup=keyboard_markup,
    )

async def black_list_info_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
    logger: logging.Logger,
):
    account_id = callback_data["id"]
    coin_id = callback_data['type']
    action = callback_data['action']
    page = int(callback_data['page'])

    if (action != '_'):
        is_blacklisted = await user.toggle_worker_blacklist(query.from_user.id, action)
        await query.answer(_['worker_blacklisted' if is_blacklisted else 'worker_not_blacklisted'].format(
                worker=action
            )
        )

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

    blacklisted_workers = [w.worker_id for w in await user.get_blacklisted_workers(query.from_user.id)]
    
    workers = None
    async with EmcdClient(account_id) as client:
        workers = await client.get_workers(coin_id)

    if (workers is None):
        await query.answer()
        logger.warning('workers is none')
        return
        
    buttons = []

    buttons_workers = []

    if (page > 1):
        buttons.append(
            types.InlineKeyboardButton(
                _["prev_button"],
                callback_data=worker_black_cb.new(
                    id=account_id, page=page - 1, type=coin_id, action="_"
                ),
            ),
        )

    workers_normalized = workers.get_all_workers(0,)

    buttons.append(
        types.InlineKeyboardButton(
            f"{page}/{ceil(len(workers_normalized) / PER_PAGE_BLACK_LIST)}",
            callback_data="do_nothing"
        ),
    )

    if (workers):
        for worker in workers_normalized[(page - 1) * PER_PAGE_BLACK_LIST: page * PER_PAGE_BLACK_LIST]:
            #message_text += '\n' + format_worker_info(worker, locales)
            buttons_workers.append(
                types.InlineKeyboardButton(
                    worker.worker + (_["blacklist_pointer"] if worker.worker in blacklisted_workers else ""),
                    callback_data=worker_black_cb.new(
                        id=account_id, page=page, type=coin_id, action=worker.worker
                    ),
                ),
            )

        if (len(workers_normalized) > page * PER_PAGE_BLACK_LIST):
            buttons.append(
                types.InlineKeyboardButton(
                    _["next_button"],
                    callback_data=worker_black_cb.new(
                        id=account_id, page=page + 1, type=coin_id, action="_"
                    ),
                ),
            )
    
    for w_row in grouper(2, buttons_workers):
        keyboard_markup.row(*w_row)

    keyboard_markup.row(*buttons)
    
    coins = [coin for coin in await user.get_account_coins(query.from_user.id, account_id) if coin.is_active]
    if (len(coins) == 1): #in case if enabled only one coin we treat them as default
        keyboard_markup.row(
            types.InlineKeyboardButton(
                _["cabinet"],
                callback_data=menu_cb.new(
                    id=account_id, type="account", action="open",
                ),
            ),
        )
    else:
        keyboard_markup.row(
            types.InlineKeyboardButton(
                _["back_to_workers_blacklist"],
                callback_data=worker_black_cb.new(
                    id=account_id, page=page, type=SELECT_COIN_CB, action="_",
                ),
            ),
        )

    await query.message.edit_text(
        _['worker_blacklist_descr'].format(
            b_count=len(blacklisted_workers),
            pointer=_["blacklist_pointer"],
        ),
        reply_markup=keyboard_markup,
    )
    