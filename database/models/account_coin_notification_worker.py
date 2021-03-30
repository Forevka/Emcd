import datetime
import typing
from dataclasses import dataclass
from uuid import UUID


@dataclass
class AccountCoinNotificationWorker:
	id: int
	account_id: UUID
	coin_id: str
	address: typing.Optional[str]
	total_count: int
	active_count: int
	inactive_count: int
	dead_count: int
	total_hashrate: int
	total_hashrate1h: int
	total_hashrate24h: int
	last_update_datetime: datetime.datetime
	is_active: bool
	user_id: int
	notification_update_datetime: datetime.datetime
