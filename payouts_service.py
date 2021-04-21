import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from background_service.payouts_monitor_service import PayoutsMonitorService
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
    
    service = PayoutsMonitorService(CONNECTION_STRING, 10)

    scheduler.start()

    scheduler.add_job(service.run, "interval", seconds=30)

    asyncio.get_event_loop().run_forever()
