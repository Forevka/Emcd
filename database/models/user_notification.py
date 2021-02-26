from dataclasses import dataclass

@dataclass
class UserNotification:
    user_id: int
    is_enabled: bool