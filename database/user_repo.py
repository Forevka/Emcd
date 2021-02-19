from emcd_client.models.info import AccountInfo, CoinInfo
from typing import List
from models.account import Account
from asyncpg.connection import Connection
from models.account_coin import AccountCoin

class UserRepository:
    def __init__(self, con: Connection):
        self.connection = con

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

    async def add_account_coin(self, user_id: int, account_id: str, coin_id: str, coin_info: CoinInfo, is_active: bool):
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