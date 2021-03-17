import typing
import asyncpg

async def get_pool(connection_string: str) -> asyncpg.Pool:
    return typing.cast(asyncpg.Pool, await asyncpg.create_pool(dsn=connection_string))

