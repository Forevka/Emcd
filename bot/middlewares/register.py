from aiogram import Dispatcher

from config import ENVIRONMENT

from bot.middlewares.logging_middleware import MyLoggingMiddleware
from bot.middlewares.request_context_middleware import RequestContextMiddleware, UpdateRequestContextMiddleware
from bot.middlewares.analytic_middleware import AnalyticMiddleware
from bot.middlewares.database_provider_middleware import DatabaseProviderMiddleware
from bot.middlewares.i18n_data_provider_midleware import I18nDataProviderMiddleware

def register_middlewares(dp: Dispatcher):
    dp.middleware.setup(UpdateRequestContextMiddleware())
    dp.middleware.setup(RequestContextMiddleware())
    dp.middleware.setup(MyLoggingMiddleware())
    
    if ENVIRONMENT != 'debug':
        dp.middleware.setup(AnalyticMiddleware())
        
    dp.middleware.setup(DatabaseProviderMiddleware(dp))
    dp.middleware.setup(I18nDataProviderMiddleware(dp))