from enum import Enum

class UserRole(Enum):
    User = 1
    Admin = 2
    Blocked = -1