from aiogram.dispatcher.handler import CancelHandler
from enums.user_role import UserRole
from typing import Any
from aiogram.types import Update, User

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class BlackListMiddleware(LifetimeControllerMiddleware):
    """
    BlackList middleware
    """

    def __init__(self,):
        super(BlackListMiddleware, self).__init__()

    async def pre_process(self, message: Any, data: dict, *args, **kwargs,):
        if (isinstance(message, Update)): return

        user = User.get_current()
        if user:
            user_db = await data['user'].get_user(user.id)
            if user_db and user_db.role_id == UserRole.Blocked.value:
                raise CancelHandler()
                