from config import ENVIRONMENT, POEDITOR_ID, POEDITOR_TOKEN
import logging
from utils.utils import (get_filename_without_ext, load_translations,
                         load_translations_from_file)
from utils.log_rotator import SizedTimedRotatingFileHandler
from utils.intercept_standart_logger import InterceptStandartHandler

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from bot.common.lang import update_texts

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

app = FastAPI()
if (ENVIRONMENT != 'debug'):
    app.root_path = '/api/emcd/'

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

@app.on_event("startup")
async def startup_event():
    trans = await load_translations_from_file()
    if (ENVIRONMENT != 'debug'):
        logger.info('Loading from poeditor')
        trans = await load_translations(POEDITOR_ID, POEDITOR_TOKEN)

    update_texts(trans)

register(app)
