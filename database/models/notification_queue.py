import datetime
import typing
from dataclasses import dataclass


@dataclass
class NotificationQueue:
	notification_id: int
	content: str
	type_id: int
	status_id: int
	result: str
	created_datetime: datetime.datetime
	modified_datetime: datetime.datetime
	user_id: int
	channel_id: int

	__select__ = """ select "notification_id", "content", "type_id", "status_id", "result", "created_datetime", "modified_datetime", "user_id", "channel_id" from notification_queue"""