from utils.utils import load_translations
from aiogram import types
from database.user_repo import UserRepository
from config import POEDITOR_ID, POEDITOR_TOKEN

async def cmd_locales(message: types.Message, user: UserRepository, _: dict):
    from utils.lang import update_texts

    new_msg =await message.answer("Reloading locales")

    update_texts(await load_translations(POEDITOR_ID, POEDITOR_TOKEN))

    await new_msg.edit_text("Locales was reloaded")

