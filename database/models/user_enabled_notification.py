from dataclasses import dataclass


@dataclass
class UserEnabledNotification:
	user_id: int
	lang_id: int
