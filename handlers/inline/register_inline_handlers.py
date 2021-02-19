from finite_state_machine import Form
from aiogram import Bot, Dispatcher

from handlers.inline.add_ccount_handler import add_account_callback_handler

from keyboard_fabrics import menu_cb


def register_callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        add_account_callback_handler,
        menu_cb.filter(type="account", action="new", id="_"),
        state="*"
    )
