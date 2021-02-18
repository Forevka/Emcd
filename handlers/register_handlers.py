from aiogram import Bot, Dispatcher

from handlers.text.register_command_handlers import register_command_handlers

def register_handlers(dp: Dispatcher):
    register_command_handlers(dp)
