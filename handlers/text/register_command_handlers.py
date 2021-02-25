from aiogram import Dispatcher
from config import texts
from finite_state_machine import Form
from handlers.text.account_id_add_handler import account_id_add_handler
from handlers.text.cabinet_command_handler import cmd_cabinet
from handlers.text.lang_command_handler import cmd_lang
from handlers.text.start_command import cmd_start
from handlers.text.version_command import cmd_version


def register_command_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_version, commands=['version'], state='*')

    cabinet_triggers = [texts['ru']['cabinet'], texts['en']['cabinet']]
    language_triggers = [texts['ru']['language'], texts['en']['language']]

    dp.register_message_handler(cmd_start, commands=['start'], state='*')
    dp.register_message_handler(cmd_cabinet, text=cabinet_triggers, state='*')
    dp.register_message_handler(cmd_lang, text=language_triggers, state='*')
    
    dp.register_message_handler(account_id_add_handler, state=Form.waiting_for_account_id)
