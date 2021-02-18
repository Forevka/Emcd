from typing import List
from models.account import Account
from asyncpg.connection import Connection

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

        return await self.connection.fetch(sql, user_id)
