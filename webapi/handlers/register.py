from webapi.handlers.auth.token import login
from fastapi import FastAPI

def register(app: FastAPI):
    app.add_api_route(
        '/token',
        login,
        tags=['Auth'],
        methods=['POST'],
    )