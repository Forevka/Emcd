async def influx_connection_error(update, error):
    update.logger.exception(error)
    return True