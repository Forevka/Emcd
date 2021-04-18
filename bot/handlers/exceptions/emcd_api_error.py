from aiogram import types

async def emcd_api_error(update: types.Update, error):
    update.logger.warning(f'Emcd api error {repr(update)}, {repr(error)}',)
    return True 