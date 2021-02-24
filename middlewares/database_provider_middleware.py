from typing import Any

from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from database.user_repo import UserRepository


class DatabaseProviderMiddleware(LifetimeControllerMiddleware):
    """
    Database provider middleware middleware
    """

    def __init__(self, dp: Dispatcher):
        super(DatabaseProviderMiddleware, self).__init__()
        self.dp = dp

    async def pre_process(self, message: Any, data: dict,):
        data['db'] = await self.dp['db_pool'].acquire()
        data['user'] = UserRepository(data['db'])
    
    async def post_process(self, obj, data, *args):
        if (data['user']):
            data['user'] = None
        if (data['db']):
            await self.dp['db_pool'].release(data['db'])
