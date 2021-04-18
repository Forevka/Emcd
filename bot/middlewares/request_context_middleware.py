from typing import Any
from loguru import logger
from uuid import uuid4
from aiogram import types

from aiogram.dispatcher.middlewares import BaseMiddleware, LifetimeControllerMiddleware


class UpdateRequestContextMiddleware(BaseMiddleware):
    """
    Provides request_id for update type
    """

    async def on_pre_process_update(self, update: Any, data: dict, *args, **kwargs,):
        logger_instance =  logger.bind(request_id=uuid4())
        update.logger = logger_instance
        data['logger'] = logger_instance

class RequestContextMiddleware(LifetimeControllerMiddleware):
    """
    Provides request_id for any update type
    """
    skip_patterns = ['update', 'error',]

    async def pre_process(self, update: Any, data: dict, *args, **kwargs,):
        data['logger'] = types.Update.get_current().logger