from aiogram import Dispatcher
from bot.filters.rethrow_exception_filter import RethrowExceptionFilter

def bind_filters(dp: Dispatcher):
    # https://t.me/aiogram_ru/535287
    #dp.errors_handlers.once = True

    dp.filters_factory.bind(RethrowExceptionFilter, event_handlers=[
        dp.errors_handlers,
    ])

