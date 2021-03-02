from pydantic import BaseModel
import os

    
class JWTokenSettings(BaseModel):
    authjwt_secret_key: str = os.environ.get('JWT_SECRET')
