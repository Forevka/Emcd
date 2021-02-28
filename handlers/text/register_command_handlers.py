from handlers.text.locales_command import cmd_locales
from filters.I18nCommandFilter import I18nCommandFilter
from handlers.text.settings_command import cmd_settings
from aiogram import Dispatcher
from finite_state_machine import Form
from handlers.text.account_id_add_handler import account_id_add_handler
from handlers.text.cabinet_command_handler import cmd_cabinet
from handlers.text.lang_command_handler import cmd_lang
from handlers.text.start_command import cmd_start
from handlers.text.version_command import cmd_version


def register_command_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_version, commands=['version'], state='*')
    dp.register_message_handler(cmd_start, commands=['start'], state='*')
    dp.register_message_handler(cmd_locales, commands=['locales'], state='*')

    dp.register_message_handler(cmd_cabinet, I18nCommandFilter('cabinet'), state='*')
    dp.register_message_handler(cmd_lang, I18nCommandFilter('language'), state='*')
    dp.register_message_handler(cmd_settings, I18nCommandFilter('setting'), state='*')
    
    dp.register_message_handler(account_id_add_handler, state=Form.waiting_for_account_id)
