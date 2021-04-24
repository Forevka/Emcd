
from typing import Any

import ujson as json
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

    async def on_post_process_message(self, message: types.Message, results, data: dict):
        analytic_id = data.get('analytic_id')
        if analytic_id is None:
            data['logger'].warning(f'{json.dumps(message.to_python())} analytic id was null')
            return

        if (message.is_command()):
            await log_command(message.from_user.id, analytic_id)
        else:
            await log_text(message.from_user.id, analytic_id)


    async def on_post_process_callback_query(self, callback_query: types.CallbackQuery, results, data: dict):
        c_data = callback_query.data.split(":")
        await log_callback_query(callback_query.from_user.id, c_data[0])
