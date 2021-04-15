from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from bot.analytics.log import log_command


class AnalyticMiddleware(BaseMiddleware):
    """
    This middleware writes analytic to influx
    """

    #async def on_pre_process_message(self, message: types.Message, data: dict):
    #    self.logger.info(f"Received message [ID:{message.message_id}] in chat [{message.chat.type}:{message.chat.id}]")

    async def on_post_process_message(self, message: types.Message, results, data: dict):
        if (message.is_command()):
            await log_command(message.from_user.id, message.get_command() or 'unknown')

    '''
    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):

    async def on_post_process_callback_query(self, callback_query, results, data: dict):
    '''