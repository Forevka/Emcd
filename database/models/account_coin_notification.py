import datetime
import typing
from dataclasses import dataclass


@dataclass
class AccountCoinNotification:
	account_coin_id: int
	is_enabled: bool

	__select__ = """ select "account_coin_id", "is_enabled" from account_coin_notification"""

