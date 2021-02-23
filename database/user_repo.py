from datetime import datetime
from models.worker_account_history import WorkerAccountHistoryForUser
from emcd_client.models.coin_workers import CoinWorker, CoinWorkers
from emcd_client.models.info import CoinInfo
from typing import List
from models.account import Account
from models.user import User
from asyncpg.connection import Connection
from models.account_coin import AccountCoin

class UserRepository:
    def __init__(self, con: Connection):
        self.connection = con

    async def delete_account_notification_settings_account(self, account_id: int, user_id: int):
        sql = '''
        delete from account_coin_notification where account_coin_id in (select id from account_coin where account_id = $1 and user_id = $2)
        '''
        
        await self.connection.execute(sql, account_id, user_id,)


    async def delete_user_account_coin(self, account_id: int, user_id: int):
        sql = '''
        delete from account_coin where account_id = $1 and user_id = $2
        '''

        await self.connection.execute(sql, account_id, user_id,)
        

    async def delete_user_account(self, account_id: int, user_id: int):
        sql = '''
        delete from account where user_id = $2 and account_id = $1
        '''

        await self.connection.execute(sql, account_id, user_id)


    async def get_user(self, user_id: int) -> User:
        sql = f'{User.__select__} where "id" = $1'

        raw = await self.connection.fetchrow(sql, user_id,)
        if (raw):
            return User(**raw)

    async def cleanup_worker_history_for_account(self, account_coind_id: int):
        sql = '''
        delete from worker_account_history
        where account_coin_id = $1
        '''

        await self.connection.execute(sql, account_coind_id,)

    async def get_previous_worker_state_for_account(self, account_coin_id: int) -> List[WorkerAccountHistoryForUser]:
        sql = '''
        SELECT 
                latest_record.worker_id
                , latest_record.account_coin_id
                , latest_record.stored_datetime
                , latest_record.status_id
                , latest_record.hashrate
                , latest_record.hashrate1h
                , latest_record.hashrate24h
                , latest_record.reject
                , ac.user_id
        FROM worker_account_history wah 
        join account_coin_notification acn on acn.account_coin_id = wah.account_coin_id and wah.account_coin_id = $1 and acn.is_enabled = TRUE
        LEFT JOIN LATERAL (
            SELECT 
                wah2.worker_id
                , wah2.account_coin_id
                , wah2.stored_datetime
                , wah2.status_id
                , wah2.hashrate
                , wah2.hashrate1h
                , wah2.hashrate24h
                , wah2.reject
            FROM worker_account_history wah2
            WHERE wah2.worker_id = wah.worker_id and wah2.account_coin_id = wah.account_coin_id
            order by wah2.stored_datetime desc
            FETCH FIRST 1  ROW ONLY
        ) latest_record ON true
        join account_coin ac on ac.id = latest_record.account_coin_id
        '''
        
        return [WorkerAccountHistoryForUser(**acc) for acc in await self.connection.fetch(sql, account_coin_id)]

    async def get_all_account_to_refresh(self,) -> List[AccountCoin]:
        sql = '''
        SELECT ac.* from account_coin ac
        join account_coin_notification acn on acn.account_coin_id = ac."id" and acn.is_enabled = TRUE
        '''
        
        return [AccountCoin(**acc) for acc in await self.connection.fetch(sql,)]

    async def store_coin_account_worker_history(self, workers: List[CoinWorker], now: datetime):
        sql = '''
        insert into worker_account_history (account_coin_id, worker_id, stored_datetime, status_id, hashrate, hashrate1h, hashrate24h, reject)
        values 
        ''' + ','.join([w.to_insert(now) for w in workers])

        await self.connection.execute(sql,)


    async def create(self, user_id: int, lang_id: int):
        sql = '''
        insert into "user" (id, lang_id) values($1, $2)
        on conflict do nothing;
        '''

        await self.connection.execute(sql, user_id, lang_id)

    async def get_accounts(self, user_id: int) -> List[Account]:
        sql = f"{Account.__select__} where user_id = $1"

        return [Account(**acc) for acc in await self.connection.fetch(sql, user_id)]

    async def add_account(self, user_id: int, account_id: str, account_name: str):
        sql = '''
        insert into "account" (user_id, account_id, username, create_datetime, modified_datetime)
        values ($1, $2, $3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        '''

        await self.connection.execute(sql, user_id, account_id, account_name)

    async def add_account_coin(self, user_id: int, account_id: str, coin_id: str, coin_info: CoinInfo, is_active: bool,):
        sql = '''
        insert into "account_coin" (account_id, user_id, coin_id, 
                                    address, total_count, active_count, 
                                    inactive_count, dead_count, is_active,
                                    total_hashrate, total_hashrate1h, total_hashrate24h,
                                    last_update_datetime)
        values ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, CURRENT_TIMESTAMP);
        '''

        await self.connection.execute(sql, account_id, user_id, coin_id, coin_info.address, 0, 0, 0, 0, is_active, 0, 0, 0)

        await self.add_notification_setting(user_id, account_id, is_active, coin_id)

    async def update_account_coin(self, _id: int, user_id: int, account_id: str, coin_id: str, address: str, coin_workers: CoinWorkers, is_active: bool, last_update_datetime: datetime):
        sql = '''
        update "account_coin" set  user_id = $2, coin_id = $3, 
                                    address = $4, total_count = $5, active_count = $6, 
                                    inactive_count = $7, dead_count = $8, is_active = $9,
                                    total_hashrate = $10, total_hashrate1h = $11, total_hashrate24h = $12,
                                    last_update_datetime = $13
        where id = $1;
        '''

        workers = coin_workers.get_all_workers(account_id)

        await self.connection.execute(sql, _id, user_id, coin_id, address, len(workers), len([i for i in workers if i.status_id == 1]), len([i for i in workers if i.status_id == 0]), len([i for i in workers if i.status_id == -1]), is_active, coin_workers.total_hashrate.hashrate, coin_workers.total_hashrate.hashrate1_h, coin_workers.total_hashrate.hashrate24_h, last_update_datetime)


    async def add_notification_setting(self, user_id: int, account_id: str, is_active: bool, coin_id: str,):
        sql = '''
        insert into "account_coin_notification" (account_coin_id, is_enabled)
        select id, $3 from "account_coin" where account_id = $1 and user_id = $2 and coin_id = $4 LIMIT 1
        '''

        await self.connection.execute(sql, account_id, user_id, is_active, coin_id,)

    async def change_coin_enabled(self, coin_account_id: int, is_active: bool, ):
        sql = '''
        update "account_coin" set is_active = $1, last_update_datetime = CURRENT_TIMESTAMP
        where id = $2
        '''

        await self.connection.execute(sql, is_active, coin_account_id,)

    async def get_account_coins_by_id(self, coin_account_id) -> AccountCoin:
        sql = f"{AccountCoin.__select__} where id = $1"

        res = await self.connection.fetchrow(sql, coin_account_id)
        if (res):
            return AccountCoin(**res)

    async def get_account_coins(self, user_id: int, account_id: str) -> AccountCoin:
        sql = f"{AccountCoin.__select__} where user_id = $1 and account_id = $2 order by coin_id asc"

        return [AccountCoin(**acc) for acc in await self.connection.fetch(sql, user_id, account_id)]