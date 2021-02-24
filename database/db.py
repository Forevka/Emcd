import asyncpg

async def get_pool(connection_string: str):
    return await asyncpg.create_pool(dsn=connection_string)

