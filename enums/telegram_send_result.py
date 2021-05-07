from enum import Enum

class TelegramSendResult(Enum):
    Ok = 1
    Blocked = 2
    ChatNotFound = 3
    RetryAfter = 4
    Deactivated = 5
    ApiError = 6
    Error = 7