import typing
from dataclasses import dataclass
import datetime

@dataclass
class ThrottlingHistory:
	id: int
	channel_id: int
	start_datetime: datetime.datetime
	end_datetime: typing.Optional[datetime.datetime]
	stored_datetime: datetime.datetime

	__select__ = """ select "id", "channel_id", "start_datetime", "end_datetime", "stored_datetime" from throttling_history"""
