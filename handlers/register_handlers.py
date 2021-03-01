from aiogram import Dispatcher

from handlers.callback.register_callback_handlers import \
    register_callback_handlers
from handlers.text.register_command_handlers import register_command_handlers


def register_handlers(dp: Dispatcher):
    register_command_handlers(dp)
    register_callback_handlers(dp)
