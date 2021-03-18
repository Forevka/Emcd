from emcd_client.exceptions.exception import EmcdApiException
from handlers.exceptions.emcd_api_error import emcd_api_error
from aiogram import Dispatcher

from handlers.callback.register_callback_handlers import \
    register_callback_handlers
from handlers.text.register_command_handlers import register_command_handlers
from handlers.exceptions.message_not_modified import message_not_modified_handler

from aiogram.utils.exceptions import MessageNotModified

def register_handlers(dp: Dispatcher):
    register_command_handlers(dp)
    register_callback_handlers(dp)

    dp.register_errors_handler(message_not_modified_handler, exception=MessageNotModified)
    dp.register_errors_handler(emcd_api_error, exception=EmcdApiException)