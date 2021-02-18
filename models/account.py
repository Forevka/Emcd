import datetime
import typing
from dataclasses import dataclass
from uuid import UUID


@dataclass
class Account:
	user_id: int
	account_id: typing.Optional[UUID]
	username: str
	create_datetime: typing.Optional[datetime.datetime]
	modified_datetime: typing.Optional[datetime.datetime]

	__select__ = """ select "user_id", "account_id", "username", "create_datetime", "modified_datetime" from account"""

