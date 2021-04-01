from loguru import logger

async def message_not_modified_handler(update, error):
    logger.warning(f'Message cant be modified {repr(update)}, {repr(error)}',)
    return True 