# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = currency_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, Dict, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class CurrencyValue:
    the_15_m: float
    last: float
    buy: float
    sell: float
    symbol: str

    @staticmethod
    def from_dict(obj: Any) -> 'CurrencyValue':
        assert isinstance(obj, dict)
        the_15_m = from_float(obj.get("15m"))
        last = from_float(obj.get("last"))
        buy = from_float(obj.get("buy"))
        sell = from_float(obj.get("sell"))
        symbol = from_str(obj.get("symbol"))
        return CurrencyValue(the_15_m, last, buy, sell, symbol)

    def to_dict(self) -> dict:
        result: dict = {}
        result["15m"] = to_float(self.the_15_m)
        result["last"] = to_float(self.last)
        result["buy"] = to_float(self.buy)
        result["sell"] = to_float(self.sell)
        result["symbol"] = from_str(self.symbol)
        return result


def currency_from_dict(s: Any) -> Dict[str, CurrencyValue]:
    return from_dict(CurrencyValue.from_dict, s)


def currency_to_dict(x: Dict[str, CurrencyValue]) -> Any:
    return from_dict(lambda x: to_class(CurrencyValue, x), x)
