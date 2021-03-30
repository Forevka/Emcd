from dataclasses import dataclass
from datetime import datetime

@dataclass
class UserNotification:
    user_id: int
    is_enabled: bool
    update_datetime: datetime
