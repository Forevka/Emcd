from aiogram import Bot, Dispatcher

from handlers.text.register_command_handlers import register_command_handlers
from handlers.inline.register_inline_handlers import register_callback_handlers


def register_handlers(dp: Dispatcher):
    register_command_handlers(dp)
    register_callback_handlers(dp)
