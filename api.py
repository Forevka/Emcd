import logging
from utils.utils import get_filename_without_ext
from utils.log_rotator import SizedTimedRotatingFileHandler
from utils.intercept_standart_logger import InterceptStandartHandler

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from webapi.handlers.register import register
from webapi.middleware.database_provider_middleware import \
    DatabaseProviderMiddleware
from webapi.middleware.error_handling_middleware import \
    ErrorHandlingMiddleware

logging.basicConfig(handlers=[InterceptStandartHandler()],)
logger.add(
    SizedTimedRotatingFileHandler(f"logs/{get_filename_without_ext(__file__)}.log", backupCount=1, 
                                    maxBytes=64 * 1024 * 1024, when='s', 
                                    interval=60 * 60 * 24, serialize=True), 
    level=logging.WARN
)

app = FastAPI(openapi_prefix="/api/emcd/")

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

app.add_middleware(
    ErrorHandlingMiddleware,
)

register(app)
