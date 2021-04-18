async def all_errors(update, error):
    update.logger.exception(error)
    return True