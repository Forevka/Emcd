from aiogram.types.message import ParseMode
from middlewares.i18n_data_provider_midleware import I18nDataProviderMiddleware
from database.db import get_pool
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers.register_handlers import register_handlers

from middlewares.database_provider_middleware import DatabaseProviderMiddleware
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

def init_bot(token: str):
    return Bot(token=token, parse_mode='HTML')


def init_dispatcher(bot: Bot):
    storage = MemoryStorage()

    return Dispatcher(bot, storage=storage)


async def on_startup(dp: Dispatcher):
    config = dp["db_config"]
    dp["db_pool"] = await get_pool(
        config["host"],
        config["port"],
        config["database"],
        config["user"],
        config["password"],
    )


def start_polling(token: str, db_config: dict):
    bot = init_bot(token)
    dp = init_dispatcher(bot)
    dp["db_config"] = db_config

    dp.middleware.setup(DatabaseProviderMiddleware(dp))
    dp.middleware.setup(I18nDataProviderMiddleware(dp))

    register_handlers(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
