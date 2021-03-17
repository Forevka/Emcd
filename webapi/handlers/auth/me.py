import json

from fastapi import Depends
from fastapi_jwt_auth import AuthJWT

def me(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    user = Authorize.get_jwt_subject()

    if (user):
        current_user = json.loads(str(user))
        return {"user": current_user}
    
    return {}