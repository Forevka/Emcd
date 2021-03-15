import datetime
import typing
from dataclasses import dataclass


@dataclass
class BroadcastToSend:
	id: int
	created_datetime: datetime
	start_datetime: datetime
	status_id: int
	lang_id: int
	text: str

	__select__ = """ 
		select 
			b."id"
			, b.created_datetime
			, b.start_datetime
			, b.status_id
			, bl.lang_id
			, bl."text" 
		from broadcast b
		join broadcast_lang bl on bl.broadcast_id = b."id"
		where CURRENT_TIMESTAMP > b.start_datetime and b.status_id = 1
	"""
