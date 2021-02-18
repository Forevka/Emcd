import datetime
import typing
from dataclasses import dataclass


@dataclass
class WorkerAccountHistory:
	account_coin_id: int
	worker_id: str
	stored_datetime: datetime.datetime
	status_id: int
	hashrate: int
	hashrate1h: int
	hashrate24h: int
	reject: typing.Any

	__select__ = """ select "account_coin_id", "worker_id", "stored_datetime", "status_id", "hashrate", "hashrate1h", "hashrate24h", "reject" from worker_account_history"""

