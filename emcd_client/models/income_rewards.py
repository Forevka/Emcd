# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = income_rewards_from_dict(json.loads(json_string))

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, Callable, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


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


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class TypeEnum(Enum):
    DONATION = "donation"
    FPPS = "fpps"


@dataclass
class Income:
    timestamp: int
    gmt_time: str
    income: float
    type: TypeEnum
    total_hashrate: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Income':
        assert isinstance(obj, dict)
        timestamp = from_int(obj.get("timestamp"))
        gmt_time = from_str(obj.get("gmt_time"))
        income = from_float(obj.get("income"))
        type = TypeEnum(obj.get("type"))
        total_hashrate = from_union([from_none, from_int], obj.get("total_hashrate"))
        return Income(timestamp, gmt_time, income, type, total_hashrate)

    def to_dict(self) -> dict:
        result: dict = {}
        result["timestamp"] = from_int(self.timestamp)
        result["gmt_time"] = from_str(self.gmt_time)
        result["income"] = to_float(self.income)
        result["type"] = to_enum(TypeEnum, self.type)
        result["total_hashrate"] = from_union([from_none, from_int], self.total_hashrate)
        return result


@dataclass
class IncomeRewards:
    income: List[Income]

    @staticmethod
    def from_dict(obj: Any) -> 'IncomeRewards':
        assert isinstance(obj, dict)
        income = from_list(Income.from_dict, obj.get("income"))
        return IncomeRewards(income)

    def to_dict(self) -> dict:
        result: dict = {}
        result["income"] = from_list(lambda x: to_class(Income, x), self.income)
        return result


def income_rewards_from_dict(s: Any) -> IncomeRewards:
    return IncomeRewards.from_dict(s)


def income_rewards_to_dict(x: IncomeRewards) -> Any:
    return to_class(IncomeRewards, x)
