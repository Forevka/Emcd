import json

from database.user_repo import UserRepository
from fastapi import Depends, HTTPException, Request
from fastapi import Depends
from fastapi_jwt_auth import AuthJWT

def lang_list(request: Request, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    user_repo = UserRepository(request.state.connection)

    langs = await user_repo.get_all_langs()

    return [
        {"id": l.id, "name": l.name} for l in langs
    ]