import logging
from utils.intercept_standart_logger import InterceptStandartHandler

from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from loguru import logger

from webapi.handlers.register import register
from webapi.middleware.database_provider_middleware import \
    DatabaseProviderMiddleware

logging.basicConfig(handlers=[InterceptStandartHandler()], level=logging.INFO)
logger.add("logs/api_{time}.log", rotation="12:00", serialize=True)

middleware = [ 
    Middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
]

app = FastAPI(middleware=middleware)

app.add_middleware(
    DatabaseProviderMiddleware,
)

register(app)
