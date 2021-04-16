from typing import Any

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from bot.analytics.log import log_callback_query, log_command, log_text


class AnalyticMiddleware(BaseMiddleware):
    """
    This middleware writes analytic to influx
    """

    async def on_post_process_message(self, message: Any, results, data: dict):
        if (message.is_command()):
            await log_command(message.from_user.id, message.get_command() or 'unknown')
        else:
            if (message.command_code):
                await log_text(message.from_user.id, message.command_code)


    async def on_post_process_callback_query(self, callback_query: types.CallbackQuery, results, data: dict):
        c_data = callback_query.data.split(":")
        await log_callback_query(callback_query.from_user.id, c_data[0])
