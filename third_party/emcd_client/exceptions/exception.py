from typing import Optional


class EmcdApiException(Exception):
    def __init__(self, code: int, message: Optional[str]): 
        self.code = code
        self.message = message
    
    def __str__(self) -> str:
        return f"Emcd Api Exception: {self.code}, {self.message}"
    
    __repr__ = __str__