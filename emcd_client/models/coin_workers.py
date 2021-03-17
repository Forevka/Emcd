# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = coin_workers_from_dict(json.loads(json_string))

from datetime import datetime
from enum import Enum
from dataclasses import dataclass
from typing import Any, Dict, List, TypeVar, Type, Callable, cast
import typing


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Detail:
    user: str
    worker: str
    hashrate: int
    hashrate1_h: int
    hashrate24_h: int
    reject: float
    lastbeat: int
    active: int

    @staticmethod
    def from_dict(obj: Any) -> 'Detail':
        assert isinstance(obj, dict)
        user = obj.get("user")
        worker = from_str(obj.get("worker"))
        hashrate = from_int(obj.get("hashrate"))
        hashrate1_h = from_int(obj.get("hashrate1h"))
        hashrate24_h = from_int(obj.get("hashrate24h"))
        reject = from_float(obj.get("reject"))
        lastbeat = from_int(obj.get("lastbeat"))
        active = from_int(obj.get("active"))
        return Detail(user, worker, hashrate, hashrate1_h, hashrate24_h, reject, lastbeat, active)

    def to_dict(self) -> dict:
        result: dict = {}
        result["user"] = self.user
        result["worker"] = from_str(self.worker)
        result["hashrate"] = from_int(self.hashrate)
        result["hashrate1h"] = from_int(self.hashrate1_h)
        result["hashrate24h"] = from_int(self.hashrate24_h)
        result["reject"] = to_float(self.reject)
        result["lastbeat"] = from_int(self.lastbeat)
        result["active"] = from_int(self.active)
        return result


@dataclass
class TotalCount:
    all: int
    active: int
    inactive: int
    dead_count: int

    @staticmethod
    def from_dict(obj: Any) -> 'TotalCount':
        assert isinstance(obj, dict)
        all = from_int(obj.get("all"))
        active = from_int(obj.get("active"))
        inactive = from_int(obj.get("inactive"))
        dead_count = from_int(obj.get("dead_count"))
        return TotalCount(all, active, inactive, dead_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["all"] = from_int(self.all)
        result["active"] = from_int(self.active)
        result["inactive"] = from_int(self.inactive)
        result["dead_count"] = from_int(self.dead_count)
        return result


@dataclass
class TotalHashrate:
    hashrate: int
    hashrate1_h: int
    hashrate24_h: int

    @staticmethod
    def from_dict(obj: Any) -> 'TotalHashrate':
        assert isinstance(obj, dict)
        hashrate = from_int(obj.get("hashrate"))
        hashrate1_h = from_int(obj.get("hashrate1h"))
        hashrate24_h = from_int(obj.get("hashrate24h"))
        return TotalHashrate(hashrate, hashrate1_h, hashrate24_h)

    def to_dict(self) -> dict:
        result: dict = {}
        result["hashrate"] = from_int(self.hashrate)
        result["hashrate1h"] = from_int(self.hashrate1_h)
        result["hashrate24h"] = from_int(self.hashrate24_h)
        return result


@dataclass
class CoinWorker:
    account_coin_id: int
    user: str
    worker: str
    hashrate: int
    hashrate1_h: int
    hashrate24_h: int
    reject: float
    lastbeat: int
    status_id: int # 1 active 0 inactive -1 dead 2 nonstable

    def to_insert(self, now: datetime) -> str:
        return f"({self.account_coin_id}, '{self.worker}', '{now.isoformat()}', {self.status_id}, {self.hashrate}, {self.hashrate1_h}, {self.hashrate24_h}, {self.reject})"

@dataclass
class CoinWorkers:
    total_count: TotalCount
    total_hashrate: TotalHashrate
    details: List[Detail]
    details_dead: Dict[str, int]

    @staticmethod
    def from_dict(obj: Any) -> 'CoinWorkers':
        assert isinstance(obj, dict)
        total_count = TotalCount.from_dict(obj.get("total_count"))
        total_hashrate = TotalHashrate.from_dict(obj.get("total_hashrate"))
        details = from_list(Detail.from_dict, obj.get("details"))
        details_dead = obj.get("detailsDead", {'': 0})
        return CoinWorkers(total_count, total_hashrate, details, details_dead)

    def to_dict(self) -> dict:
        result: dict = {}
        result["total_count"] = to_class(TotalCount, self.total_count)
        result["total_hashrate"] = to_class(TotalHashrate, self.total_hashrate)
        result["details"] = from_list(lambda x: to_class(Detail, x), self.details)
        result["detailsDead"] = self.details_dead#to_class(DetailsDead, self.details_dead)
        return result

    def get_all_workers(self, account_coin_id: int) -> typing.List[CoinWorker]:
        workers: typing.List[CoinWorker] = []
        for raw_worker in self.details:
            workers.append(CoinWorker(account_coin_id, raw_worker.user, raw_worker.worker, raw_worker.hashrate, raw_worker.hashrate1_h, raw_worker.hashrate24_h, raw_worker.reject, raw_worker.lastbeat, raw_worker.active))

        for dead_worker_id, dead_worker_lastbeat in self.details_dead.items():
            workers.append(CoinWorker(account_coin_id, '', dead_worker_id, 0, 0, 0, 0.0, dead_worker_lastbeat, -1))

        return workers

    def get_all_workers_by_status(self, account_coin_id: int, status_id: int) -> typing.List[CoinWorker]:
        workers: typing.List[CoinWorker] = []
        for raw_worker in self.details:
            workers.append(CoinWorker(account_coin_id, raw_worker.user, raw_worker.worker, raw_worker.hashrate, raw_worker.hashrate1_h, raw_worker.hashrate24_h, raw_worker.reject, raw_worker.lastbeat, raw_worker.active))

        for dead_worker_id, dead_worker_lastbeat in self.details_dead.items():
            workers.append(CoinWorker(account_coin_id, '', dead_worker_id, 0, 0, 0, 0.0, dead_worker_lastbeat, -1))

        if (status_id == 3): return workers
        return [i for i in workers if i.status_id == status_id]

def coin_workers_from_dict(s: Any) -> CoinWorkers:
    return CoinWorkers.from_dict(s)


def coin_workers_to_dict(x: CoinWorkers) -> Any:
    return to_class(CoinWorkers, x)
