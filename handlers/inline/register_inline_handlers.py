from handlers.inline.delete_account_callback_handler import delete_account_callback_handler, delete_account_confirmation_callback_handler
from handlers.inline.worker_callback_handler import worker_callback_handler, worker_info_callback_handler
from handlers.inline.income_callback_handler import income_callback_handler, income_info_callback_handler
from handlers.inline.payouts_callback_handler import payouts_callback_handler, payouts_info_callback_handler
from handlers.inline.cabinet_callback_handler import cabinet_callback_handler
from handlers.inline.change_coin_enabled_setting_coins_for_account import change_coin_enabled_setting_coins_for_account
from handlers.inline.change_coins_for_account import change_coins_for_account_callback_handler
from handlers.inline.account_cabinet_handler import account_cabinet_callback_handler
from aiogram import Dispatcher

from handlers.inline.add_ccount_handler import add_account_callback_handler

from keyboard_fabrics import menu_cb, coin_account_cb, payouts_cb, income_cb, worker_cb, delete_account_cb


def register_callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        add_account_callback_handler,
        menu_cb.filter(type="account", action="new", id="_"),
        state="*"
    )
    
    dp.register_callback_query_handler(
        account_cabinet_callback_handler,
        menu_cb.filter(type="account", action="open"),
        state="*"
    )

    dp.register_callback_query_handler(
        change_coins_for_account_callback_handler,
        menu_cb.filter(type="account", action="c_coins"),
        state="*"
    )
    
    dp.register_callback_query_handler(
        change_coin_enabled_setting_coins_for_account,
        coin_account_cb.filter(action=['on', 'off']),
        state="*"
    )

    dp.register_callback_query_handler(
        cabinet_callback_handler,
        menu_cb.filter(id="_", type="menu", action="main_menu"),
        state="*"
    )
    
    dp.register_callback_query_handler(
        payouts_callback_handler,
        payouts_cb.filter(type='s_coin'),
        state="*"
    )

    dp.register_callback_query_handler(
        payouts_info_callback_handler,
        payouts_cb.filter(),
        state="*"
    )

    dp.register_callback_query_handler(
        income_callback_handler,
        income_cb.filter(type='s_coin'),
        state="*"
    )

    dp.register_callback_query_handler(
        income_info_callback_handler,
        income_cb.filter(),
        state="*"
    )

    dp.register_callback_query_handler(
        worker_callback_handler,
        worker_cb.filter(type='s_coin'),
        state="*"
    )

    dp.register_callback_query_handler(
        worker_info_callback_handler,
        worker_cb.filter(),
        state="*"
    )
    
    dp.register_callback_query_handler(
        delete_account_callback_handler,
        delete_account_cb.filter(action="choose"),
        state="*"
    )

    dp.register_callback_query_handler(
        delete_account_confirmation_callback_handler,
        delete_account_cb.filter(action="yes"),
        state="*"
    )
    
    dp.register_callback_query_handler(
        account_cabinet_callback_handler,
        delete_account_cb.filter(action="no"),
        state="*"
    )
    
