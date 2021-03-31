from utils.lang import LangHolder
from typing import Any
from aiogram.types import Update

from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from config import DEFAULT_LANG
from enums.lang import Lang


class I18nDataProviderMiddleware(LifetimeControllerMiddleware):
    """
    I18n lang holder provider middleware middleware
    """

    def __init__(self, dp: Dispatcher):
        super(I18nDataProviderMiddleware, self).__init__()
        self.dp = dp

    async def pre_process(self, message: Any, data: dict, *args, **kwargs,):
        if (isinstance(message, Update)): return

        user = await data['user'].get_user(message.from_user.id)
        if (user):
            message.c_user_locale_code = Lang(user.lang_id).name
        else:
            message.c_user_locale_code = DEFAULT_LANG.name
        
        data['_'] = LangHolder(user.lang_id, message.c_user_locale_code,)
