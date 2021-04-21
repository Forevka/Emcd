import asyncio
from asyncio.locks import BoundedSemaphore
from typing import Dict, Generic, List, TypeVar

from asyncpg.connection import Connection
from asyncpg.pool import Pool
from config import (ENVIRONMENT, POEDITOR_ID, POEDITOR_TOKEN,)
from database.db import get_pool
from loguru import logger
from notifier.base_notifier import BaseNotifier
from utils.utils import load_translations, load_translations_from_file

T = TypeVar('T')


class BaseBackgroundService(Generic[T]):
    def __init__(self, connection_string: str, max_workers: int = 10,):
        self.max_workers = max_workers
        self.connection_string = connection_string
    
    async def get_notifier(self,) -> BaseNotifier:
        raise NotImplementedError()

    async def job(self, con: Connection, item: T, notifier: BaseNotifier, locales: Dict[str, str]):
        raise NotImplementedError()

    async def get_items_to_process(self, con: Connection) -> List[T]:
        raise NotImplementedError()

    async def _job_wrapper(self, item: T, semaphore: BoundedSemaphore, pool: Pool, notifier: BaseNotifier, locales: Dict[str, str]):
        async with semaphore:
            con: Connection = await pool.acquire()

            try:
                await self.job(con, item, notifier, locales)
            except Exception as e:
                logger.exception(e)
            finally:
                await pool.release(con)
                logger.info(f'Connection was released')


    async def run(self,):
        notifier = await self.get_notifier()

        pool = None
        try:
            pool = await get_pool(self.connection_string)
            locales = await load_translations_from_file()
            if (ENVIRONMENT != 'debug'):
                logger.info('Loading from poeditor')
                locales = await load_translations(POEDITOR_ID, POEDITOR_TOKEN)
                
            logger.info(f'Job started')
            temp_con = await pool.acquire()
            items = await self.get_items_to_process(temp_con)

            logger.info(f'Total items to proccess {len(items)}')
            await pool.release(temp_con)

            semaphore = asyncio.BoundedSemaphore(self.max_workers)
            tasks = []

            for item in items:
                tasks.append(asyncio.ensure_future(self._job_wrapper(item, semaphore, pool, notifier, locales)))

            await asyncio.gather(*tasks)
        except Exception as e:
            logger.exception(e)
        finally:
            logger.info(f'Terminating pool')
            if pool is not None:
                await pool.close()

            await notifier.close()
