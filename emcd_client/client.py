from uuid import UUID
from emcd_client.exceptions.exception import EmcdApiException
from emcd_client.models.payouts import Payouts, payouts_from_dict
from emcd_client.models.income_rewards import IncomeRewards, income_rewards_from_dict
from emcd_client.models.coin_workers import CoinWorkers, coin_workers_from_dict
from emcd_client.models.info import AccountInfo, account_info_from_dict
from types import TracebackType
from typing import Any, Dict, Optional, Type, Union

import aiohttp
from yarl import URL

API_VERSION = 1

class EmcdClient:
    def __init__(self, account_id: Union[str, UUID], base_url: URL = URL('https://api.emcd.io/')) -> None:
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

    async def get_info(self,) -> Optional[AccountInfo]:
        async with self._client.get(self._make_url(f"v{API_VERSION}/info/{self._account_id}"), raise_for_status=False) as resp:
            if (resp.status == 200):
                ret = await resp.json()
                return account_info_from_dict(ret)
            return None

    async def get_workers(self, coin_name: str) -> Optional[CoinWorkers]:
        async with self._client.get(self._make_url(f"v{API_VERSION}/{coin_name}/workers/{self._account_id}"), raise_for_status=False) as resp:
            if (resp.status == 200):
                ret = await resp.json()
                return coin_workers_from_dict(ret)
            return None

    async def get_rewards(self, coin_name: str) -> Optional[IncomeRewards]:
        async with self._client.get(self._make_url(f"v{API_VERSION}/{coin_name}/income/{self._account_id}"), raise_for_status=False) as resp:
            if (resp.status == 200):
                ret = await resp.json()
                return income_rewards_from_dict(ret)
            return None

    async def get_payouts(self, coin_name: str) -> Optional[Payouts]:
        async with self._client.get(self._make_url(f"v{API_VERSION}/{coin_name}/payouts/{self._account_id}"), raise_for_status=False) as resp:
            if (resp.status == 200):
                ret = await resp.json()
                return payouts_from_dict(ret)
            return None
