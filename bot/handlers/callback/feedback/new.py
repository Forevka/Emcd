import typing

from aiogram import types
from bot.common.finite_state_machine import FeedbackForm
from bot.common.lang import LangHolder
from database.user_repo import UserRepository


async def new_feedback(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: LangHolder,
):
    await query.message.edit_text(_['new_feedback'])
    await FeedbackForm.waiting_for_text.set()
