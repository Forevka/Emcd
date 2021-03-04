import json

from fastapi import Depends
from fastapi_jwt_auth import AuthJWT

def me(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = json.loads(Authorize.get_jwt_subject())
    return {"user": current_user}