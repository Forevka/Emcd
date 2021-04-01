from aiogram import Dispatcher
from bot.filters.I18nCommandFilter import I18nCommandFilter
from bot.handlers.text.account_id_add_handler import account_id_add_handler
from bot.handlers.text.cabinet_command_handler import cmd_cabinet
from bot.handlers.text.faq_command_handler import cmd_faq
from bot.handlers.text.lang_command import cmd_lang
from bot.handlers.text.locales_command import cmd_locales
from bot.handlers.text.settings_command import cmd_settings
from bot.handlers.text.start_command import cmd_start
from bot.handlers.text.version_command import cmd_version
from utils.finite_state_machine import Form


def register_command_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_version, commands=['version'], state='*')
    dp.register_message_handler(cmd_start, commands=['start'], state='*')
    dp.register_message_handler(cmd_locales, commands=['locales'], state='*')

    dp.register_message_handler(cmd_faq, I18nCommandFilter('faq'), state='*')
    dp.register_message_handler(cmd_cabinet, I18nCommandFilter('cabinet'), state='*')
    dp.register_message_handler(cmd_lang, I18nCommandFilter('language'), state='*')
    dp.register_message_handler(cmd_settings, I18nCommandFilter('setting'), state='*')
    
    dp.register_message_handler(account_id_add_handler, state=Form.waiting_for_account_id)
