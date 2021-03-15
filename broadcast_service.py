import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import exceptions, executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asyncpg.connection import Connection
from asyncpg.pool import Pool
from loguru import logger

from config import TOKEN, CONNECTION_STRING
from database.db import get_pool
from database.broadcast_repo import BroadcastRepository
from notifier.telegram_notifier import TelegramNotifier
from database.models.broadcast_to_send import BroadcastToSend
from utils.intercept_standart_logger import InterceptStandartHandler

logging.basicConfig(handlers=[InterceptStandartHandler()], level=logging.INFO)
logger.add("logs/broadcast_service_{time}.log", rotation="12:00", serialize=True)

async def send_message(user_id: int, text: str, notifier: TelegramNotifier) -> bool:
    """
    Safe messages sender
    :param user_id:
    :param text:
    :param disable_notification:
    :return:
    """
    try:
        await notifier.notify(user_id, text)
    except exceptions.BotBlocked:
        logger.warning(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        logger.warning(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        logger.warning(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        logger.warning(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        logger.exception(f"Target [ID:{user_id}]: failed")
    else:
        logger.info(f"Target [ID:{user_id}]: success")
        return True

    return False


async def broadcaster(semaphore: asyncio.BoundedSemaphore, pool: Pool, broadcast: BroadcastToSend,) -> int:
    """
    Simple broadcaster
    :return: Count of messages
    """
    async with semaphore:
        notifier = TelegramNotifier(TOKEN)
        repo = BroadcastRepository(await pool.acquire())

        count = 0
        try:
            users = await repo.get_all_user_by_lang(broadcast.lang_id)

            for user in users:
                if await send_message(user.id, broadcast.text, notifier):
                    count += 1
                await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
            
            await repo.update_broadcast_status(broadcast.id, 2)
        finally:
            
            logger.info(f"{count} messages successful sent.")

            await pool.release(repo.connection)
            await notifier.bot.session.close()

            logger.info(f"connetion released, notifier destroyed")

        return count

async def job():
    pool = None
    try:
        pool = await get_pool(CONNECTION_STRING)
        logger.info(f'Job started')

        repo = BroadcastRepository(await pool.acquire())

        broadcasts = await repo.get_all_broadcasts_to_send()

        logger.info(f'Total broadcasts to send {len(broadcasts)}')
        await pool.release(repo.connection)

        semaphore = asyncio.BoundedSemaphore(10)
        tasks = []

        for broadcast in broadcasts:
            tasks.append(asyncio.ensure_future(broadcaster(semaphore, pool, broadcast,)))

        await asyncio.gather(*tasks)
    except Exception as e:
        logger.exception(e)
    finally:
        logger.info(f'Terminating pool')
        if pool is not None:
            await pool.close()



if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job, "interval", seconds=10)

    scheduler.start()

    asyncio.get_event_loop().run_forever()