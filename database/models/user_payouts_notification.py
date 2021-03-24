from dataclasses import dataclass

@dataclass
class UserPayoutsNotification:
    user_id: int
    is_enabled: bool
