import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from loguru import logger

from config import (CONNECTION_STRING, ENVIRONMENT, POEDITOR_ID,
                    POEDITOR_TOKEN, TOKEN)
from database.db import get_pool
from bot.handlers.register_handlers import register_handlers
from bot.middlewares.database_provider_middleware import DatabaseProviderMiddleware
from bot.middlewares.i18n_data_provider_midleware import I18nDataProviderMiddleware
from utils.intercept_standart_logger import InterceptStandartHandler
from utils.lang import update_texts
from utils.utils import load_translations, load_translations_from_file

logging.basicConfig(handlers=[
    InterceptStandartHandler(),
], level=logging.WARN)
logger.add("logs/bot_{time}.log", rotation="12:00", serialize=True)

def init_bot(token: str):
    return Bot(token=token, parse_mode='HTML')


def init_dispatcher(bot: Bot):
    storage = MemoryStorage()

    return Dispatcher(bot, storage=storage)


async def on_startup(dp: Dispatcher):
    logger.info('Loading locales')

    trans = await load_translations_from_file()
    if (ENVIRONMENT != 'debug'):
        logger.info('Loading from poeditor')
        trans = await load_translations(POEDITOR_ID, POEDITOR_TOKEN)

    update_texts(trans)

    dp["db_pool"] = await get_pool(
        dp["connection_string"],
    )


def start_polling(token: str, connection_string: str):
    bot = init_bot(token)
    dp = init_dispatcher(bot)

    dp["connection_string"] = connection_string

    dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(DatabaseProviderMiddleware(dp))
    dp.middleware.setup(I18nDataProviderMiddleware(dp))

    register_handlers(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


def start():
    start_polling(TOKEN, CONNECTION_STRING)


if __name__ == "__main__":
    start()
    