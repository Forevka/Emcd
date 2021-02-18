import datetime
import typing
from dataclasses import dataclass
from uuid import UUID


@dataclass
class AccountCoin:
	id: int
	account_id: UUID
	coin_id: int
	address: typing.Optional[str]
	total_count: int
	active_count: int
	inactive_count: int
	dead_count: int
	total_hashrate: int
	total_hashrate1h: int
	total_hashrate24h: int
	last_update_datetime: datetime.datetime

	__select__ = """ select "id", "account_id", "coin_id", "address", "total_count", "active_count", "inactive_count", "dead_count", "total_hashrate", "total_hashrate1h", "total_hashrate24h", "last_update_datetime" from account_coin"""

