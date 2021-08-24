from pydantic import BaseModel
from typing import Optional

class TelegramContactAttributes(BaseModel):
    #from_tg: bool
    username: Optional[str]


class Contact(BaseModel):
    role: str
    external_id: int
    name: Optional[str]
    custom_attributes: TelegramContactAttributes
