import logging
from utils.intercept_standart_logger import InterceptStandartHandler

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from webapi.handlers.register import register
from webapi.middleware.database_provider_middleware import \
    DatabaseProviderMiddleware

logging.basicConfig(handlers=[InterceptStandartHandler()], level=logging.INFO)
logger.add("logs/api_{time}.log", rotation="12:00", serialize=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    DatabaseProviderMiddleware,
)

register(app)