import typing
from math import ceil

from aiogram import types
from config import PER_PAGE_WORKERS, SELECT_COIN_CB, WORKER_STATUS_CAROUSEL
from database.user_repo import UserRepository
from enums.coin import Coin
from loguru import logger
from tabulate import tabulate
from third_party.emcd_client.client import EmcdClient
from third_party.emcd_client.models.coin_workers import CoinWorker
from bot.common.replies import reply_to_account_not_found
from bot.common.keyboard_fabrics import menu_cb, worker_cb
from bot.common.lang import LangHolder
from utils.utils import format_rate, grouper


async def worker_callback_handler(
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
                    callback_data=worker_cb.new(
                        id=account_id, page=page, type=coin.coin_id, status_id=3,
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
        _["worker_choose_coin"],
        reply_markup=keyboard_markup,
    )


def format_worker_info(worker: CoinWorker, locales: typing.Dict[str, str]) -> str:
    emoji = "🟢"
    if (worker.status_id == -1):
        emoji = "🔴"

    headers = [locales['hashrate'], 'FPPS']

    table = [
        [locales['current'], format_rate(worker.hashrate)],
        [locales['1_hour'], format_rate(worker.hashrate1_h)],
        [locales['24_hour'], format_rate(worker.hashrate24_h)],
    ]

    return f'{emoji} {worker.worker}\n<code>{tabulate(table, headers, tablefmt="psql")}</code>'

async def worker_info_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    account_id = callback_data["id"]
    coind_id = callback_data['type']
    page = int(callback_data['page'])
    status_id = int(callback_data['status_id'])

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

    workers = None
    async with EmcdClient(account_id) as client:
        workers = await client.get_workers(coind_id)

    if (workers is None):
        await query.answer()
        logger.warning('workers is none')
        return

    message_text = ""

    buttons = []

    if (page > 1):
        buttons.append(
            types.InlineKeyboardButton(
                _["prev_button"],
                callback_data=worker_cb.new(
                    id=account_id, page=page - 1, type=coind_id, status_id=status_id,
                ),
            ),
        )

    workers_normalized = workers.get_all_workers_by_status(0, status_id)

    buttons.append(
        types.InlineKeyboardButton(
            f"{page}/{ceil(len(workers_normalized) / PER_PAGE_WORKERS)}",
            callback_data="do_nothing"
        ),
    )


    locales = {
        'hashrate': _['hashrate'],
        'current': _['current'],
        '1_hour': _['1_hour'],
        '24_hour': _['24_hour'],
    }

    if (workers):
        for worker in workers_normalized[(page - 1) * PER_PAGE_WORKERS: page * PER_PAGE_WORKERS]:
            message_text += '\n' + format_worker_info(worker, locales)

        if (len(workers_normalized) > page * PER_PAGE_WORKERS):
            buttons.append(
                types.InlineKeyboardButton(
                    _["next_button"],
                    callback_data=worker_cb.new(
                        id=account_id, page=page + 1, type=coind_id, status_id=status_id,
                    ),
                ),
            )
        
    keyboard_markup.row(*buttons)
    
    coins = [coin for coin in await user.get_account_coins(query.from_user.id, account_id) if coin.is_active]

    filter_text = _['show_dead_workers']
    new_status_id = WORKER_STATUS_CAROUSEL[status_id]
    if (new_status_id == -1):
        filter_text = _['show_dead_workers']
    elif (new_status_id == 0):
        filter_text = _['show_inactive_workers']
    elif (new_status_id == 1):
        filter_text = _['show_active_workers']
    elif (new_status_id == 3):
        filter_text = _['show_all_workers']

    if (len(coins) == 1): #in case if enabled only one coin we treat them as default
        keyboard_markup.row(
            types.InlineKeyboardButton(
                filter_text,
                callback_data=worker_cb.new(
                    id=account_id, page=page, type=coind_id, status_id=new_status_id,
                ),
            ),
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
                filter_text,
                callback_data=worker_cb.new(
                    id=account_id, page=page, type=coind_id, status_id=new_status_id,
                ),
            ),
            types.InlineKeyboardButton(
                _["back_to_workers"],
                callback_data=worker_cb.new(
                    id=account_id, page=page, type=SELECT_COIN_CB, status_id=status_id,
                ),
            ),
        )
        

    workers_all = workers.get_all_workers(0)

    await query.message.edit_text(
        _['worker_info_descr'].format(
            hashrate=format_rate(workers.total_hashrate.hashrate),
            hashrate1h=format_rate(workers.total_hashrate.hashrate1_h),
            hashrate24h=format_rate(workers.total_hashrate.hashrate24_h),
            total=str(len(workers_all)) + (_['show_workers_filter_pointer'] if status_id == 3 else ''),
            dead=str(len([i for i in workers_all if i.status_id == -1])) + (_['show_workers_filter_pointer'] if status_id == -1 else ''),
            active=str(len([i for i in workers_all if i.status_id == 1])) + (_['show_workers_filter_pointer'] if status_id == 1 else ''),
            inactive=str(len([i for i in workers_all if i.status_id == 0])) + (_['show_workers_filter_pointer'] if status_id == 0 else ''),
            description=message_text,
        ),
        reply_markup=keyboard_markup,
    )

async def worker_info_change_status_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    account_id = callback_data["id"]
    coind_id = callback_data['type']
    page = int(callback_data['page'])
    status_id = int(callback_data['status_id'])
