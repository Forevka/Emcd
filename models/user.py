import datetime
import typing
from dataclasses import dataclass


@dataclass
class User:
	id: int
	lang_id: int
	created_datetime: datetime.datetime

	__select__ = """ select "id", "lang_id", "created_datetime" from user"""

