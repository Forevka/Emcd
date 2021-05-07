import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from background_service.notification_senders.telegram import TelegramNotificationSenderService
from config import CONNECTION_STRING
from utils.intercept_standart_logger import InterceptStandartHandler
from utils.log_rotator import SizedTimedRotatingFileHandler
from utils.utils import get_filename_without_ext

logging.basicConfig(handlers=[InterceptStandartHandler()],)
logger.add(
    SizedTimedRotatingFileHandler(f"logs/{get_filename_without_ext(__file__)}.log", backupCount=1, 
                                    maxBytes=64 * 1024 * 1024, when='s', 
                                    interval=60 * 60 * 24, serialize=True), 
    level=logging.WARN
)


if (__name__ == "__main__"):
    scheduler = AsyncIOScheduler()
    service = TelegramNotificationSenderService(CONNECTION_STRING, max_workers=1, is_need_to_load_translations=False)

    scheduler.start()

    scheduler.add_job(service.run, "interval", seconds=1, max_instances=1)

    asyncio.get_event_loop().run_forever()
