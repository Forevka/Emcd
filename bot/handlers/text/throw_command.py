from aiogram import types
from database.user_repo import UserRepository


async def cmd_throw(message: types.Message, user: UserRepository, _: dict):
    raise ValueError()
