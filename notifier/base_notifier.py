from asyncpg.connection import Connection


class BaseNotifier():
    async def notify(self, text: str, con: Connection, user_id: int,):
        raise NotImplementedError()
    
    async def close(self,):
        raise NotImplementedError()
        