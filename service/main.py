from asyncpg.pool import Pool
from emcd_client.client import EmcdClient
from models.account_coin import AccountCoin
from emcd_client.models.info import AccountInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

from database.db import get_pool
from database.user_repo import UserRepository
from config import postgres

async def update_account_data(semaphore: asyncio.BoundedSemaphore, account: AccountCoin, pool: Pool):
    async with semaphore:
        con = await pool.acquire()
        try:
            async with EmcdClient(account.account_id) as client:
                api_account = await client.get_workers(account.coin_id)
                workers = api_account.get_all_workers(account.id)

                user_repo = UserRepository(con)

                await user_repo.store_coin_account_worker_history(workers)
        except Exception as e:
            print(e)
        finally:
            await pool.release(con)


async def job():
    pool = await get_pool(**postgres)
    user_repo = UserRepository(await pool.acquire())
    accounts = await user_repo.get_all_account_to_refresh()
    semaphore = asyncio.BoundedSemaphore(10)

    tasks = []

    for account in accounts:
        tasks.append(asyncio.ensure_future(update_account_data(semaphore, account)))

    await asyncio.gather(*tasks)


if (__name__ == "__main__"):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job, "interval", seconds=5)

    scheduler.start()

    asyncio.get_event_loop().run_forever()