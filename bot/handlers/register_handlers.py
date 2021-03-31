from aiogram import Dispatcher
from aiogram.utils.exceptions import MessageNotModified
from bot.handlers.callback.register_callback_handlers import \
    register_callback_handlers
from bot.handlers.exceptions.emcd_api_error import emcd_api_error
from bot.handlers.exceptions.message_not_modified import \
    message_not_modified_handler
from bot.handlers.text.register_command_handlers import \
    register_command_handlers
from third_party.emcd_client.exceptions.exception import EmcdApiException


def register_handlers(dp: Dispatcher):
    register_command_handlers(dp)
    register_callback_handlers(dp)

    dp.register_errors_handler(message_not_modified_handler, exception=MessageNotModified)
    dp.register_errors_handler(emcd_api_error, exception=EmcdApiException)
