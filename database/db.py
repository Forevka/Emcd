import os

import typing
import asyncio
import asyncpg
import re
import logging

async def get_pool(host: str, port: typing.Union[int, str], database: str, user: str, password: str):
    return await asyncpg.create_pool(
        user=user,
        password=password,
        database=database,
        host=host,
        port=port
    )


