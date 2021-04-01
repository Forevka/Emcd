from loguru import logger
from aiogram import types

async def emcd_api_error(update: types.Update, error):
    logger.warning(f'Emcd api error {repr(update)}, {repr(error)}',)
    return True 