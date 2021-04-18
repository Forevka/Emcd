from typing import Any
from loguru import logger
from uuid import uuid4
from aiogram import types

from aiogram.dispatcher.middlewares import BaseMiddleware, LifetimeControllerMiddleware

'''
class BotLogger():
    def __init__(self, request_id: Optional[UUID] = None):
        self.request_id = uuid4() if request_id is None else request_id
        self._logger = logger.bind(request_id=request_id)
    
    @property
    def logger_instance(self,):
        return self._logger
'''

class RequestContextMiddleware(BaseMiddleware):
    """
    Provides request_id for any update type
    """

    async def on_pre_process_update(self, update: Any, data: dict, *args, **kwargs,):
        update.logger = logger.bind(request_id=uuid4())
