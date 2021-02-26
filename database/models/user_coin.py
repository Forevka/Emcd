from dataclasses import dataclass

@dataclass
class UserCoin:
    user_id: int
    coin_id: str
    is_enabled: bool