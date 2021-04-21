from aiogram import Dispatcher
from aiogram.types import ChatType
from bot.common.finite_state_machine import Form
from bot.filters.i18n_command_filter import I18nCommandFilter
from bot.handlers.text.account_id_add_handler import TextAddAccount
from bot.handlers.text.cabinet_command_handler import CmdCabinet
from bot.handlers.text.faq_command_handler import CmdFaq
from bot.handlers.text.group_disable_chat import TextNonPrivateGuard
from bot.handlers.text.lang_command import CmdLang
from bot.handlers.text.locales_command import CmdLocales
from bot.handlers.text.settings_command import CmdSettings
from bot.handlers.text.start_command import CmdStart
from bot.handlers.text.throw_command import CmdThrow
from bot.handlers.text.version_command import CmdVersion


def register_command_handlers(dp: Dispatcher):
    dp.register_message_handler(TextNonPrivateGuard('non_private_guard'), chat_type=[ChatType.GROUP, ChatType.SUPERGROUP,])

    dp.register_message_handler(CmdThrow('throw'), commands=['throw'], state='*')
    dp.register_message_handler(CmdVersion('version'), commands=['version'], state='*')
    dp.register_message_handler(CmdStart('start'), commands=['start'], state='*')
    dp.register_message_handler(CmdLocales('locales'), commands=['locales'], state='*')

    dp.register_message_handler(CmdFaq('faq'), I18nCommandFilter('faq'), state='*')
    dp.register_message_handler(CmdCabinet('cabinet'), I18nCommandFilter('cabinet'), state='*')
    dp.register_message_handler(CmdLang('lang'), I18nCommandFilter('language'), state='*')
    dp.register_message_handler(CmdSettings('settings'), I18nCommandFilter('setting'), state='*')
    
    dp.register_message_handler(TextAddAccount('new_emcd_account'), state=Form.waiting_for_account_id)
