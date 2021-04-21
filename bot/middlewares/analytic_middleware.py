
from typing import Any

from aiogram import types
from aiogram.dispatcher.handler import current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from bot.analytics.log import (log_callback_query, log_command, log_request,
                               log_text)
from bot.handlers.text.base_command_handler import BaseCommandHandler


class AnalyticMiddleware(BaseMiddleware):
    """
    This middleware writes analytic to influx
    """

    async def on_post_process_update(self, update: types.Update, results, data: dict):
        await log_request(update.update_id)

    async def on_process_message(self, message: Any, data: dict):
        handler: BaseCommandHandler = current_handler.get()
        data['analytic_id'] = handler.analytic_id

    async def on_post_process_message(self, message: Any, results, data: dict):
        if (message.is_command()):
            await log_command(message.from_user.id, data['analytic_id'])
        else:
            await log_text(message.from_user.id, data['analytic_id'])


    async def on_post_process_callback_query(self, callback_query: types.CallbackQuery, results, data: dict):
        c_data = callback_query.data.split(":")
        await log_callback_query(callback_query.from_user.id, c_data[0])
