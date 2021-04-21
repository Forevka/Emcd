from bot.handlers.text.base_command_handler import BaseCommandHandler
from aiogram import types
from config import POEDITOR_ID, POEDITOR_TOKEN
from database.user_repo import UserRepository
from utils.utils import load_translations

class CmdLocales(BaseCommandHandler):
    async def handle(self, message: types.Message, user: UserRepository, _: dict):
        from bot.common.lang import update_texts

        new_msg = await message.answer("Reloading locales")

        update_texts(await load_translations(POEDITOR_ID, POEDITOR_TOKEN))

        await new_msg.edit_text("Locales was reloaded")

    __call__ = handle