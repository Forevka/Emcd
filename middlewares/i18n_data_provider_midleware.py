from typing import Any

from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from asyncpg.pool import Pool
from config import texts


class I18nDataProviderMiddleware(LifetimeControllerMiddleware):
    """
    Database provider middleware middleware
    """

    def __init__(self, dp: Dispatcher):
        super(I18nDataProviderMiddleware, self).__init__()
        self.dp = dp

    async def pre_process(self, message: Any, data: dict,):
        data['_'] = texts['ru']
