import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram.utils import executor
from loguru import logger

from bot.common.lang import update_texts
from bot.filters.bind import bind_filters
from bot.handlers.register_handlers import register_handlers
from bot.middlewares.register import register_middlewares
from config import (CONNECTION_STRING, ENVIRONMENT, POEDITOR_ID,
                    POEDITOR_TOKEN, TOKEN)
from database.db import get_pool
from utils.intercept_standart_logger import InterceptStandartHandler
from utils.log_rotator import SizedTimedRotatingFileHandler
from utils.utils import (get_filename_without_ext, load_translations,
                         load_translations_from_file)

logging.basicConfig(handlers=[InterceptStandartHandler()],)
logger.add(
    SizedTimedRotatingFileHandler(f"logs/{get_filename_without_ext(__file__)}.log", backupCount=1, 
                                    maxBytes=64 * 1024 * 1024, when='s', 
                                    interval=60 * 60 * 24, serialize=True), 
    level=logging.WARN
)

def init_bot(token: str):
    return Bot(token=token, parse_mode='HTML')


def init_dispatcher(bot: Bot):
    storage = MemoryStorage()

    return Dispatcher(bot, storage=storage)

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Launch bot/Запуск бота"),
        BotCommand(command="lang", description="Change language/Сменить язык"),
    ]
    await bot.set_my_commands(commands)

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

    await set_bot_commands(dp.bot)



def start_polling(token: str, connection_string: str):
    bot = init_bot(token)
    dp = init_dispatcher(bot)

    dp["connection_string"] = connection_string

    bind_filters(dp)
    register_middlewares(dp)
    register_handlers(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


def start():
    start_polling(TOKEN, CONNECTION_STRING)


if __name__ == "__main__":
    start()
    