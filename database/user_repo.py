from datetime import datetime
from typing import List, Optional

from asyncpg.connection import Connection
from third_party.emcd_client.models.coin_workers import CoinWorker, CoinWorkers
from third_party.emcd_client.models.info import CoinInfo

from database.models.account import Account
from database.models.account_coin import AccountCoin
from database.models.account_coin_notification_payout import \
    AccountCoinNotificationPayout
from database.models.account_coin_notification_worker import \
    AccountCoinNotificationWorker
from database.models.currency import Currency
from database.models.lang import Lang
from database.models.user import User
from database.models.user_coin import UserCoin
from database.models.user_currency import UserCurrency
from database.models.user_enabled_notification import UserEnabledNotification
from database.models.user_notification import UserNotification
from database.models.user_payouts_notification import UserPayoutsNotification
from database.models.worker_account_history import WorkerAccountHistoryForUser
from database.models.worker_blacklist import WorkerBlacklist


class UserRepository:
    def __init__(self, con: Connection):
        self.connection = con

    async def get_all_langs(self,) -> List[Lang]:
        sql = f"""
        {Lang.__select__}
        """
        
        return [Lang(**acc) for acc in await self.connection.fetch(sql,)]

    async def get_coins(self, user_id: int) -> List[UserCoin]:
        sql = '''
        select user_id, coin_id, is_enabled from user_coin where user_id = $1
        '''

        return [UserCoin(**acc) for acc in await self.connection.fetch(sql, user_id)]

    async def update_user_lang(self, user_id: int, lang_id: int):
        sql = '''
        update "user" set lang_id = $1 where "id" = $2
        '''

        await self.connection.execute(sql, lang_id, user_id,)

    async def update_notification_setting(self, user_id: int, new_value: bool):
        sql = '''
        update user_notification set is_enabled = $1, update_datetime = CURRENT_TIMESTAMP where user_id = $2
        '''

        await self.connection.execute(sql, new_value, user_id,)

    async def get_notification_setting_for_user(self, user_id: int,) -> Optional[UserNotification]:
        sql = f'''
        select user_id, is_enabled, update_datetime from user_notification where user_id = $1
        '''
        
        raw = await self.connection.fetchrow(sql, user_id,)
        if (raw):
            return UserNotification(**raw)
    
    
    async def update_notification_payouts_setting(self, user_id: int, new_value: bool):
        sql = '''
        update user_payout_notification set is_enabled = $1, update_datetime = CURRENT_TIMESTAMP where user_id = $2
        '''

        await self.connection.execute(sql, new_value, user_id,)

    async def get_notification_payout_setting_for_user(self, user_id: int,) -> Optional[UserPayoutsNotification]:
        sql = f'''
        select user_id, is_enabled, update_datetime from user_payout_notification where user_id = $1
        '''
        
        raw = await self.connection.fetchrow(sql, user_id,)
        if (raw):
            return UserPayoutsNotification(**raw)


    async def delete_account_notification_settings_account(self, account_id: str, user_id: int):
        sql = '''
        delete from account_coin_notification where account_coin_id in (select id from account_coin where account_id = $1 and user_id = $2)
        '''
        
        await self.connection.execute(sql, account_id, user_id,)


    async def delete_user_account_coin(self, account_id: str, user_id: int):
        sql = '''
        delete from account_coin where account_id = $1 and user_id = $2
        '''

        await self.connection.execute(sql, account_id, user_id,)
        

    async def delete_user_account(self, account_id: str, user_id: int):
        sql = '''
        delete from account where user_id = $2 and account_id = $1
        '''

        await self.connection.execute(sql, account_id, user_id)


    async def get_user(self, user_id: int) -> Optional[User]:
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
        join account_coin ac on ac.id = latest_record.account_coin_id and ac.id = $1
        '''
        
        return [WorkerAccountHistoryForUser(**acc) for acc in await self.connection.fetch(sql, account_coin_id)]

    async def get_all_account_to_refresh(self,) -> List[AccountCoinNotificationWorker]:
        sql = '''
        SELECT ac."id"
            , ac.account_id
			, ac.active_count
            , ac.coin_id
            , ac.address
            , ac.total_count
            , ac.inactive_count
            , ac.dead_count
            , ac.total_hashrate
            , ac.total_hashrate1h
            , ac.total_hashrate24h
            , ac.last_update_datetime
            , ac.is_active
            , ac.user_id
            , un.update_datetime as notification_update_datetime 
        from account_coin ac
        join user_notification un on un.user_id = ac.user_id and un.is_enabled = true and ac.is_active = true
        '''
        
        return [AccountCoinNotificationWorker(**acc) for acc in await self.connection.fetch(sql,)]
    
    async def get_all_account_payouts_to_refresh(self,) -> List[AccountCoinNotificationPayout]:
        sql = '''
        SELECT 
            ac."id"
            , ac.account_id
			, ac.active_count
            , ac.coin_id
            , ac.address
            , ac.total_count
            , ac.inactive_count
            , ac.dead_count
            , ac.total_hashrate
            , ac.total_hashrate1h
            , ac.total_hashrate24h
            , ac.last_update_datetime
            , ac.is_active
            , ac.user_id
            , upn.update_datetime as notification_update_datetime 
        from account_coin ac
        join user_payout_notification upn on upn.user_id = ac.user_id and upn.is_enabled = true and ac.is_active = true
        '''
        
        return [AccountCoinNotificationPayout(**acc) for acc in await self.connection.fetch(sql,)]

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

        
    async def add_user_coin(self, user_id: int, coin_id: str, is_enabled: bool):
        sql = '''
        insert into "user_coin" (user_id, coin_id, is_enabled) values($1, $2, $3)
        on conflict do nothing;
        '''

        await self.connection.execute(sql, user_id, coin_id, is_enabled)

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

    async def update_account_coin(self, _id: int, user_id: int, account_id: int, coin_id: str, address: Optional[str], coin_workers: CoinWorkers, is_active: bool, last_update_datetime: datetime):
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

    async def add_notification_payouts_setting(self, user_id: int, is_enabled: bool,):
        sql = '''
        insert into "user_payout_notification" (user_id, is_enabled, update_datetime)
        values($1, $2, CURRENT_TIMESTAMP)
        on conflict do nothing;
        '''

        await self.connection.execute(sql, user_id, is_enabled,)

    async def add_notification_setting(self, user_id: int, is_enabled: bool,):
        sql = '''
        insert into "user_notification" (user_id, is_enabled, update_datetime)
        values($1, $2, CURRENT_TIMESTAMP)
        on conflict do nothing;
        '''

        await self.connection.execute(sql, user_id, is_enabled,)

    async def change_account_coin_enabled(self, user_id: int, coin_id: str, is_enabled: bool,):
        sql = '''
        update account_coin set is_active = $1 where user_id = $2 and coin_id = $3
        '''

        await self.connection.execute(sql, is_enabled, user_id, coin_id,)


    async def change_coin_enabled(self, user_id: int, coin_id: str, is_enabled: bool, ):
        sql = '''
        update "user_coin" set is_enabled = $1
        where user_id = $2 and coin_id = $3
        '''

        await self.connection.execute(sql, is_enabled, user_id, coin_id,)

    async def get_account_coins_by_id(self, coin_account_id) -> Optional[AccountCoin]:
        sql = f"{AccountCoin.__select__} where id = $1"

        res = await self.connection.fetchrow(sql, coin_account_id)
        if (res):
            return AccountCoin(**res)

    async def get_account_coins(self, user_id: int, account_id: str) -> List[AccountCoin]:
        sql = f"{AccountCoin.__select__} where user_id = $1 and account_id = $2 order by coin_id asc"

        return [AccountCoin(**acc) for acc in await self.connection.fetch(sql, user_id, account_id)]


    async def get_available_currency(self,) -> List[Currency]:
        sql = Currency.__select__

        return [Currency(**acc) for acc in await self.connection.fetch(sql,)]

    async def add_user_currency(self, user_id: int, currency_id: int):
        sql = """
        insert into "user_currency" (user_id, currency_id)
        values ($1, $2)
        on conflict do nothing;
        """

        await self.connection.execute(sql, user_id, currency_id)

        
    async def get_user_currency(self, user_id: int) -> Optional[UserCurrency]:
        sql = f"{UserCurrency.__select__} where \"user_id\" = $1"

        res = await self.connection.fetchrow(sql, user_id)
        if (res):
            return UserCurrency(**res)

    async def update_user_currency(self, user_id: int, currency_id: int):
        sql = """
        update "user_currency"
        set currency_id = $1
        where user_id = $2
        """

        await self.connection.execute(sql, currency_id, user_id,)

    async def get_blacklisted_workers(self, user_id: int,) -> List[WorkerBlacklist]:
        sql = f"{WorkerBlacklist.__select__} where user_id = $1"

        return [WorkerBlacklist(**acc) for acc in await self.connection.fetch(sql, user_id,)]

    async def toggle_worker_blacklist(self, user_id: int, worker_id: str):
        workers = [w.worker_id for w in await self.get_blacklisted_workers(user_id)]
        sql = """
        insert into worker_blacklist(user_id, worker_id)
        values ($1, $2)
        """
        is_blacklisted = True
        if (worker_id in workers):
            sql = """
            delete from worker_blacklist where user_id = $1 and worker_id = $2
            """
            is_blacklisted = False

        await self.connection.execute(sql, user_id, worker_id,)
        return is_blacklisted
    
    async def is_payout_notified(self, account_coin_id: int, timestamp: int) -> bool:
        sql = """
        select * from user_account_coin_payout where account_coin_id = $1 and payout_datetime = to_timestamp($2)
        """

        return len(await self.connection.fetch(sql, account_coin_id, timestamp)) >= 1
        
    async def mark_payout_as_notified(self, account_coin_id: int, timestamp: int):
        sql = """
        insert into user_account_coin_payout(account_coin_id, payout_datetime)
        values($1, to_timestamp($2))
        on conflict do nothing;
        """

        await self.connection.execute(sql, account_coin_id, timestamp)

        
    async def get_users_with_enabled_notifications(self, ) -> List[UserEnabledNotification]:
        sql = """
        select un.user_id, u.lang_id from user_notification un
        join "user" u on u.id = un.user_id
        join 
        where un.is_enabled = true
        """

        return [UserEnabledNotification(**acc) for acc in await self.connection.fetch(sql,)]
