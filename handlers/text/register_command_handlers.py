from typing import Text
from aiogram import Bot, Dispatcher

from handlers.text.start_command import cmd_start
from handlers.text.cabinet_command_handler import cmd_cabinet

from config import texts



def register_command_handlers(dp: Dispatcher):
    cabinet_triggers = [texts['ru']['cabinet'], texts['en']['cabinet']]

    dp.register_message_handler(cmd_start, commands=['start'], state='*')
    dp.register_message_handler(cmd_cabinet, text=cabinet_triggers, state='*')