from enum import Enum

class NotifyType(Enum):
    Worker = 1
    Payout = 2
    Broadcast = 3
    Conversation = 4