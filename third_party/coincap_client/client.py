from third_party.coincap_client.models.exchange_coin_to_currency import ExchangeCoinToCurrencyData, exchange_coin_to_currency_from_dict
from types import TracebackType
from typing import Optional, Type

import aiohttp
from yarl import URL

API_VERSION = 2

class CoinCapClient:
    def __init__(self, base_url: URL = URL('https://api.coincap.io/')) -> None:
        self._base_url = base_url
        self._client = aiohttp.ClientSession(raise_for_status=True)

    async def close(self) -> None:
        return await self._client.close()

    async def __aenter__(self) -> "CoinCapClient":
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

    async def get_info_for_exchange(self, baseSymbol: str, quoteSymbol: str) -> Optional[ExchangeCoinToCurrencyData]:
        params = [
            ("baseSymbol", baseSymbol),
            ("quoteSymbol", quoteSymbol),
        ]
        async with self._client.get(self._make_url(f"v{API_VERSION}/markets"), raise_for_status=False, params=params) as resp:
            if (resp.status == 200):
                ret = await resp.json()
                return exchange_coin_to_currency_from_dict(ret)
            return None
