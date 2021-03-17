# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = exchange_coin_to_currency_from_dict(json.loads(json_string))

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, Callable, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class ExchangeCoinToCurrency:
    exchange_id: str
    rank: int
    base_symbol: str
    base_id: str
    quote_symbol: str
    quote_id: str
    price_quote: float
    price_usd: float
    volume_usd24_hr: str
    updated: int
    trades_count24_hr: int = 0
    percent_exchange_volume: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ExchangeCoinToCurrency':
        assert isinstance(obj, dict)
        exchange_id = str(obj.get("exchangeId"))
        rank = int(obj.get("rank", 0))
        base_symbol = from_str(obj.get("baseSymbol"))
        base_id = from_str(obj.get("baseId"))
        quote_symbol = str(obj.get("quoteSymbol"))
        quote_id = str(obj.get("quoteId"))
        price_quote = float(obj.get("priceQuote", 0))
        price_usd = float(obj.get("priceUsd", 0))
        volume_usd24_hr = from_str(obj.get("volumeUsd24Hr"))
        trades_count24_hr = from_union([from_none, lambda x: int(from_str(x))], obj.get("tradesCount24Hr"))
        updated = from_int(obj.get("updated"))
        percent_exchange_volume = from_union([from_none, from_str], obj.get("percentExchangeVolume"))
        return ExchangeCoinToCurrency(exchange_id, rank, base_symbol, base_id, quote_symbol, quote_id, price_quote, price_usd, volume_usd24_hr, trades_count24_hr, updated, percent_exchange_volume)

    def to_dict(self) -> dict:
        result: dict = {}
        result["exchangeId"] = self.exchange_id
        result["rank"] = str(self.rank)
        result["baseSymbol"] = from_str(self.base_symbol)
        result["baseId"] = from_str(self.base_id)
        result["quoteSymbol"] = self.quote_symbol
        result["quoteId"] = self.quote_id
        result["priceQuote"] = from_str(self.price_quote)
        result["priceUsd"] = from_str(self.price_usd)
        result["volumeUsd24Hr"] = from_str(self.volume_usd24_hr)
        result["tradesCount24Hr"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.trades_count24_hr)
        result["updated"] = from_int(self.updated)
        result["percentExchangeVolume"] = from_union([from_none, from_str], self.percent_exchange_volume)
        return result


@dataclass
class ExchangeCoinToCurrencyData:
    data: List[ExchangeCoinToCurrency]
    timestamp: int

    @staticmethod
    def from_dict(obj: Any) -> 'ExchangeCoinToCurrencyData':
        assert isinstance(obj, dict)
        data = from_list(ExchangeCoinToCurrency.from_dict, obj.get("data"))
        timestamp = from_int(obj.get("timestamp"))
        return ExchangeCoinToCurrencyData(data, timestamp)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_list(lambda x: to_class(ExchangeCoinToCurrency, x), self.data)
        result["timestamp"] = from_int(self.timestamp)
        return result


def exchange_coin_to_currency_from_dict(s: Any) -> ExchangeCoinToCurrencyData:
    return ExchangeCoinToCurrencyData.from_dict(s)


def exchange_coin_to_currency_to_dict(x: ExchangeCoinToCurrencyData) -> Any:
    return to_class(ExchangeCoinToCurrencyData, x)
