from pydantic import BaseModel
import os
from datetime import timedelta

    
class JWTokenSettings(BaseModel):
    authjwt_secret_key: str = os.environ.get('JWT_SECRET')
    authjwt_access_token_expires: timedelta = timedelta(days=5)
