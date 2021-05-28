from aiogram.dispatcher.storage import FSMContext
from bot.common.finite_state_machine import FeedbackForm
import typing

from aiogram import types
from database.user_repo import UserRepository
from bot.common.lang import LangHolder


async def reply_to_conversation(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: LangHolder,
    state: FSMContext,
):
    async with state.proxy() as data:
        data['reply_to_conversation'] = callback_data['id']
        
    await FeedbackForm.waiting_for_reply.set()

    await query.message.edit_text(_['feedback_reply'])
    