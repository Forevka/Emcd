from handlers.callback.finance_callback_handler import finance_callback_handler
from handlers.callback.statistic_callback_handler import statistic_callback_handler, statistic_info_callback_handler
from handlers.callback.lang_callback_handler import lang_callback_handler, lang_list_callback_handler
from aiogram import Dispatcher

from handlers.callback.notification_callback_handler import notificaion_enable_callback_handler
from handlers.callback.delete_account_callback_handler import delete_account_callback_handler, delete_account_confirmation_callback_handler
from handlers.callback.worker_callback_handler import worker_callback_handler, worker_info_callback_handler
from handlers.callback.income_callback_handler import income_callback_handler, income_info_callback_handler
from handlers.callback.payouts_callback_handler import payouts_callback_handler, payouts_info_callback_handler
from handlers.callback.cabinet_callback_handler import cabinet_callback_handler
from handlers.callback.change_coin_enabled_setting_coins_for_account import change_coin_enabled_setting_coins_for_account
from handlers.callback.change_coins_for_account import change_coins_for_account_callback_handler
from handlers.callback.account_cabinet_handler import account_cabinet_callback_handler
from handlers.callback.add_ccount_handler import add_account_callback_handler


from keyboard_fabrics import menu_cb, coin_account_cb, payouts_cb, income_cb, worker_cb, delete_account_cb, notification_cb, lang_cb, statistic_cb, finance_cb


def register_callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        finance_callback_handler,
        finance_cb.filter(type='s_coin'),
        state="*"
    )

    dp.register_callback_query_handler(
        lang_list_callback_handler,
        lang_cb.filter(id="_"),
        state="*"
    )

    dp.register_callback_query_handler(
        lang_callback_handler,
        lang_cb.filter(),
        state="*"
    )

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
        finance_cb.filter(action="payouts"),
        state="*"
    )

    dp.register_callback_query_handler(
        payouts_info_callback_handler,
        payouts_cb.filter(),
        state="*"
    )

    dp.register_callback_query_handler(
        statistic_callback_handler,
        statistic_cb.filter(type='s_coin'),
        state="*"
    )

    dp.register_callback_query_handler(
        statistic_info_callback_handler,
        statistic_cb.filter(),
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
        notificaion_enable_callback_handler,
        notification_cb.filter(),
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
    
