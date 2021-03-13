from webapi.handlers.auth.me import me
from fastapi import FastAPI
from fastapi_jwt_auth.exceptions import AuthJWTException
from webapi.handlers.auth.exception import exception_handler
from webapi.handlers.lang.lang_list import lang_list
from webapi.handlers.auth.token import login


def register(app: FastAPI):
    app.add_exception_handler(AuthJWTException, exception_handler)

    app.add_api_route(
        '/lang/list',
        lang_list,
        tags=['Lang'],
        methods=['GET'],
    )

    app.add_api_route(
        '/auth/token',
        login,
        tags=['Auth'],
        methods=['POST'],
    )

    app.add_api_route(
        '/auth/me',
        me,
        tags=['Auth'],
        methods=['GET'],
    )
