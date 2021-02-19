from handlers.inline.change_coin_enabled_setting_coins_for_account import change_coin_enabled_setting_coins_for_account
from handlers.inline.change_coins_for_account import change_coins_for_account_callback_handler
from handlers.inline.account_cabinet_handler import account_cabinet_callback_handler
from finite_state_machine import Form
from aiogram import Bot, Dispatcher

from handlers.inline.add_ccount_handler import add_account_callback_handler

from keyboard_fabrics import menu_cb, coin_account_cb


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
    
