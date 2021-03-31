from aiogram import types
from database.user_repo import UserRepository


async def do_nothing_callback_handler(
    query: types.CallbackQuery,
    user: UserRepository,
    _: dict,
):
    await query.answer()
