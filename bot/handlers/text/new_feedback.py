from database.conversation_repo import ConversationRepository
from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.handlers.text.base_command_handler import BaseCommandHandler
from config import INTERCOM_TOKEN
from database.user_repo import UserRepository
from third_party.intercom_client.client import IntercomClient
from utils.get_or_create_intercom_contact import get_intercom_contact


class TextAddConversation(BaseCommandHandler):
    async def handle(self, message: types.Message, user: UserRepository, _: dict, state: FSMContext):
        
        conv_repo = ConversationRepository(user.connection)

        await state.finish()

        async with IntercomClient(INTERCOM_TOKEN) as intercom:
            intercom_user = await get_intercom_contact(message.from_user)

            if (not intercom_user):
                return await message.answer(_['feedback_user_doesnt_exist'])

            conversation = await intercom.create_conversation(intercom_user['id'], message.text)
            await conv_repo.add(message.from_user.id, int(conversation['conversation_id']))

        await message.answer(_['feedback_accepted'])

    __call__ = handle
