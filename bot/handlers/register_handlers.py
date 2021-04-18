from bot.handlers.exceptions.all_errors import all_errors
from aiogram import Dispatcher
from aiogram.utils.exceptions import MessageNotModified
from aiohttp.client_exceptions import ClientConnectorError
from bot.handlers.callback.register_callback_handlers import \
    register_callback_handlers
from bot.handlers.exceptions.emcd_api_error import emcd_api_error
from bot.handlers.exceptions.influx_connection_error import \
    influx_connection_error
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
    dp.register_errors_handler(influx_connection_error, exception=ClientConnectorError)

    #handle all other errors 
    #and log them with request_id
    dp.register_errors_handler(all_errors, exception=Exception)