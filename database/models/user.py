import datetime
from dataclasses import dataclass


@dataclass
class User:
	id: int
	lang_id: int
	created_datetime: datetime.datetime
	role_id: int

	__select__ = ''' select "id", "lang_id", "created_datetime", "role_id" from "user"'''

