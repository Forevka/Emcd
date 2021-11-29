import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import MessageNotModified
from aiogram.dispatcher.filters.filters import BoundFilter
from config import CONNECTION_STRING
from database.broadcast_repo import BroadcastRepository
from loguru import logger

from database.db import get_pool

API_TOKEN = os.environ.get('TOKEN', '')

logging.basicConfig(level=logging.INFO)

class RethrowExceptionFilter(BoundFilter):
    key = 'rethrow'
    required = True
    default = True

    def __init__(self, rethrow: bool,):
        self.rethrow = rethrow

    async def check(self, obj, error):
        if (hasattr(error, 'aiogram_is_handled')):
            return False

        setattr(error, 'aiogram_is_handled', True)

        return True

async def send_welcome(message: types.Message):
    constant_text = "Error going brrrrrrrrrrrrrr"
    msg = await message.answer(constant_text)
    await asyncio.sleep(1)
    await msg.edit_text(constant_text)

async def throw_error(message: types.Message):
    raise ValueError('test')

async def catch_not_modified(update: types.Update, error):
    print('not modified', update.update_id)
    return True
    
async def catch_all(update: types.Update, error):
    print('all other', update.update_id)
    return True

async def do_poll(bot: Bot, admin_id: int, connection_string: str):
    pool = await get_pool(
        connection_string,
    )

    poll = await bot.send_poll(admin_id, 'Сколько бы Вы потратили средств за месячную подписку на бота для мониторинга?', [
        '0 RUB',
        '300 RUB',
        '500 RUB',
        '900 RUB',
        '1000+',
    ], is_anonymous=True)

    repo = BroadcastRepository(await pool.acquire())

    users = await repo.get_all_users()

    for user in users:
        try:
            sent_poll = await bot.forward_message(user.id, admin_id, poll.message_id, False)
            logger.info(f"Target [ID:{user.id}]: sent")
        except Exception as e:
            logger.warning(f"Target [ID:{user.id}]: ex: {e}")

        await asyncio.sleep(0.25)



if __name__ == '__main__':
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot)

    dp["connection_string"] = CONNECTION_STRING
    

    dp.filters_factory.bind(RethrowExceptionFilter, event_handlers=[
        dp.errors_handlers,
    ])


    dp.register_message_handler(throw_error, commands=['t'])
    dp.register_message_handler(send_welcome)

    dp.register_errors_handler(catch_not_modified, exception=MessageNotModified)
    dp.register_errors_handler(catch_all, exception=Exception)
    
    #dp.errors_handlers.once = True

    asyncio.run(do_poll(bot, 383492784, CONNECTION_STRING))

    #executor.start_polling(dp, skip_updates=True)

