from aiogram import Dispatcher
from bot.common.keyboard_fabrics import (coin_account_cb, currency_cb,
                                         delete_account_cb, finance_cb,
                                         income_cb, lang_cb, menu_cb,
                                         notification_cb,
                                         notification_payout_cb, payouts_cb,
                                         question_answer_cb, statistic_cb,
                                         worker_black_cb, worker_cb)
from bot.handlers.callback.account_cabinet_handler import \
    account_cabinet_callback_handler
from bot.handlers.callback.add_ccount_handler import \
    add_account_callback_handler
from bot.handlers.callback.black_list_handler import (
    black_list_callback_handler, black_list_info_callback_handler)
from bot.handlers.callback.cabinet_callback_handler import \
    cabinet_callback_handler
from bot.handlers.callback.change_coin_enabled_setting_coins_for_account import \
    change_coin_enabled_setting_coins_for_account
from bot.handlers.callback.change_coins_for_account import \
    change_coins_for_account_callback_handler
from bot.handlers.callback.currency_callback_handler import (
    currency_callback_handler, currency_update_callback_handler)
from bot.handlers.callback.delete_account_callback_handler import (
    delete_account_callback_handler,
    delete_account_confirmation_callback_handler)
from bot.handlers.callback.do_nothing_handler import \
    do_nothing_callback_handler
from bot.handlers.callback.faq_callback import (faq_callback_handler,
                                                faq_info_callback_handler)
from bot.handlers.callback.finance_callback_handler import \
    finance_callback_handler
from bot.handlers.callback.income_callback_handler import (
    income_callback_handler, income_info_callback_handler)
from bot.handlers.callback.lang_callback_handler import (
    lang_callback_handler, lang_list_callback_handler)
from bot.handlers.callback.notification_callback_handler import \
    notificaion_enable_callback_handler
from bot.handlers.callback.notification_payouts_callback_handler import \
    notificaion_payout_enable_callback_handler
from bot.handlers.callback.payouts_callback_handler import (
    payouts_callback_handler, payouts_info_callback_handler)
from bot.handlers.callback.statistic_callback_handler import (
    statistic_callback_handler, statistic_info_callback_handler)
from bot.handlers.callback.worker_callback_handler import (
    worker_callback_handler, worker_info_callback_handler)
from config import SELECT_COIN_CB


def blacklist_menu_group(dp: Dispatcher):
    dp.register_callback_query_handler(
        black_list_callback_handler,
        worker_black_cb.filter(type=SELECT_COIN_CB,),
        state="*"
    )


    dp.register_callback_query_handler(
        black_list_info_callback_handler,
        worker_black_cb.filter(),
        state="*"
    )


def currency_menu_group(dp: Dispatcher):
    dp.register_callback_query_handler(
        currency_callback_handler,
        currency_cb.filter(action="open", id="_",),
        state="*"
    )

    
    dp.register_callback_query_handler(
        currency_update_callback_handler,
        currency_cb.filter(),
        state="*"
    )


def lang_menu_group(dp: Dispatcher):
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

def account_menu_group(dp: Dispatcher):
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
        cabinet_callback_handler,
        menu_cb.filter(id="_", type="menu", action="main_menu"),
        state="*"
    )

    dp.register_callback_query_handler(
        account_cabinet_callback_handler,
        delete_account_cb.filter(action="no"),
        state="*"
    )

def finances_payouts_menu_group(dp: Dispatcher):
    dp.register_callback_query_handler(
        finance_callback_handler,
        finance_cb.filter(type=SELECT_COIN_CB),
        state="*"
    )

    dp.register_callback_query_handler(
        payouts_callback_handler,
        payouts_cb.filter(type=SELECT_COIN_CB),
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

def change_coins_menu_group(dp: Dispatcher):
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

def statistic_menu_group(dp: Dispatcher):
    dp.register_callback_query_handler(
        statistic_callback_handler,
        statistic_cb.filter(type=SELECT_COIN_CB),
        state="*"
    )

    dp.register_callback_query_handler(
        statistic_info_callback_handler,
        statistic_cb.filter(),
        state="*"
    )

def faq_menu_group(dp: Dispatcher):
    dp.register_callback_query_handler(
        faq_callback_handler,
        question_answer_cb.filter(action='page'),
        state="*"
    )

    dp.register_callback_query_handler(
        faq_info_callback_handler,
        question_answer_cb.filter(action='open'),
        state="*"
    )

def income_menu_group(dp: Dispatcher):
    dp.register_callback_query_handler(
        income_callback_handler,
        income_cb.filter(type=SELECT_COIN_CB),
        state="*"
    )

    dp.register_callback_query_handler(
        income_info_callback_handler,
        income_cb.filter(),
        state="*"
    )

def worker_menu_group(dp: Dispatcher):
    dp.register_callback_query_handler(
        worker_callback_handler,
        worker_cb.filter(type=SELECT_COIN_CB),
        state="*"
    )

    dp.register_callback_query_handler(
        worker_info_callback_handler,
        worker_cb.filter(),
        state="*"
    )

def notification_menu_group(dp: Dispatcher):
    dp.register_callback_query_handler(
        notificaion_enable_callback_handler,
        notification_cb.filter(),
        state="*"
    )
    
    dp.register_callback_query_handler(
        notificaion_payout_enable_callback_handler,
        notification_payout_cb.filter(),
        state="*"
    )

def delete_menu_group(dp: Dispatcher):
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

def register_callback_handlers(dp: Dispatcher):
    blacklist_menu_group(dp)
    currency_menu_group(dp)
    lang_menu_group(dp)
    account_menu_group(dp)
    finances_payouts_menu_group(dp)
    change_coins_menu_group(dp)
    statistic_menu_group(dp)
    faq_menu_group(dp)
    income_menu_group(dp)
    worker_menu_group(dp)
    notification_menu_group(dp)
    delete_menu_group(dp)
    
    dp.register_callback_query_handler(
        do_nothing_callback_handler,
        text="do_nothing",
    )
