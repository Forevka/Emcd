from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from bot.analytics.log import log_callback_query, log_command, log_text


class AnalyticMiddleware(BaseMiddleware):
    """
    This middleware writes analytic to influx
    """


    async def on_post_process_message(self, message: types.Message, results, data: dict):
        if (message.is_command()):
            await log_command(message.from_user.id, message.get_command() or 'unknown')
        else:
            from bot.common.lang import reversed_locales
            
            c_user_locale_code = data['c_user_locale_code']
            
            t = message.text.lower()
            if (t in reversed_locales[c_user_locale_code]):
                text_code = reversed_locales.get(c_user_locale_code, {}).get(t, 'unknown')
                await log_text(message.from_user.id, text_code)


    async def on_post_process_callback_query(self, callback_query: types.CallbackQuery, results, data: dict):
        c_data = callback_query.data.split(":")
        await log_callback_query(callback_query.from_user.id, c_data[0])