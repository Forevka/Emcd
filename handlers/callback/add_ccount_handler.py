import typing

from aiogram import types
from database.user_repo import UserRepository
from finite_state_machine import Form


async def add_account_callback_handler(query: types.CallbackQuery, callback_data: typing.Dict[str, str], user: UserRepository, _: dict):
    await query.message.edit_text(_['add_account_descr'])
    await Form.waiting_for_account_id.set()
