import asyncio
from emcd_client.models.info import AccountInfo, account_info_from_dict
import functools
from contextlib import asynccontextmanager
from dataclasses import dataclass
from types import TracebackType
from typing import Any, AsyncIterator, Awaitable, Callable, List, Optional, Type

import aiohttp
import click
from yarl import URL
#v1/info/18b81eca-37bd-40d5-a249-e99a8489c306

API_VERSION = 1

class EmcdClient:
    def __init__(self, account_id: str, base_url: URL = URL('https://api.emcd.io/')) -> None:
        self._base_url = base_url
        self._account_id = account_id
        self._client = aiohttp.ClientSession(raise_for_status=True)

    async def close(self) -> None:
        return await self._client.close()

    async def __aenter__(self) -> "EmcdClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Optional[bool]:
        await self.close()
        return None

    def _make_url(self, path: str) -> URL:
        return self._base_url / path

    async def get_info(self,) -> AccountInfo:
        async with self._client.get(self._make_url(f"v{API_VERSION}/info/{self._account_id}"), raise_for_status=False) as resp:
            if (resp.status == 200):
                ret = await resp.json()
                return account_info_from_dict(ret)
            return None
