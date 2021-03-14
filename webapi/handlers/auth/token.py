import collections
import hashlib
import hmac
import json

from config import TOKEN, ENVIRONMENT
from database.user_repo import UserRepository
from fastapi import Depends, HTTPException, Request
from fastapi_jwt_auth import AuthJWT
from webapi.jwt_token_settings import JWTokenSettings
from webapi.models.user_auth import TelegramAuthModel


@AuthJWT.load_config
def get_config():
    return JWTokenSettings()

def check_user_data(data: TelegramAuthModel, token):
    secret = hashlib.sha256()
    secret.update(token.encode('utf-8'))
    sorted_params = collections.OrderedDict(sorted(data.dict().items()))
    msg = "\n".join(["{}={}".format(k, v) for k, v in sorted_params.items() if k != 'hash'])

    return data.hash == hmac.new(secret.digest(), msg.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()

async def login(request: Request, user: TelegramAuthModel, Authorize: AuthJWT = Depends()):
    if (ENVIRONMENT.lower().strip() == "production"):
        if (not check_user_data(user, TOKEN)):
            raise HTTPException(status_code=401, detail="Nice try hacker :D")

    user_repo = UserRepository(request.state.connection)

    db_user = await user_repo.get_user(user.id)
    if (db_user.role_id == 1):
        raise HTTPException(status_code=401, detail="Sorry you don't have permission")

    access_token = Authorize.create_access_token(subject=json.dumps(user.dict()))
    return {"access_token": access_token}
