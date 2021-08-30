# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = payouts_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast, Optional


T = TypeVar("T")

def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> T:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Payout:
    timestamp: float
    gmt_time: str
    amount: float
    txid: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Payout':
        assert isinstance(obj, dict)
        timestamp = from_float(obj.get("timestamp"))
        gmt_time = from_str(obj.get("gmt_time"))
        amount = from_float(obj.get("amount"))
        txid = obj.get("txid")
        return Payout(timestamp, gmt_time, amount, txid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["timestamp"] = from_float(self.timestamp)
        result["gmt_time"] = from_str(self.gmt_time)
        result["amount"] = to_float(self.amount)
        result["txid"] = from_str(self.txid)
        return result


@dataclass
class Payouts:
    payouts: List[Payout]

    @staticmethod
    def from_dict(obj: Any) -> 'Payouts':
        assert isinstance(obj, dict)
        payouts = from_list(Payout.from_dict, obj.get("payouts"))
        return Payouts(payouts)

    def to_dict(self) -> dict:
        result: dict = {}
        result["payouts"] = from_list(lambda x: to_class(Payout, x), self.payouts)
        return result


def payouts_from_dict(s: Any) -> Payouts:
    return Payouts.from_dict(s)


def payouts_to_dict(x: Payouts) -> Any:
    return to_class(Payouts, x)
