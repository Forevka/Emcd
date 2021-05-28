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

        async with IntercomClient(INTERCOM_TOKEN) as intercom:
            intercom_user = await get_intercom_contact(message.from_user)

            if (not intercom_user):
                return await message.answer(_['feedback_user_doesnt_exist'])

            conversation = await intercom.create_conversation(intercom_user['id'], message.text)
            async with state.proxy() as data:
                attachments_ids = data.get('attachments', [])
                attachments_urls = [message.bot.get_file_url((await message.bot.get_file(i)).file_path) for i in attachments_ids]
                await intercom.reply_to_conversation(intercom_user['id'], "uploaded attachments", conversation['conversation_id'], attachments_urls)


            await conv_repo.add(message.from_user.id, int(conversation['conversation_id']))

        await message.answer(_['feedback_accepted'])

        await state.finish()

    __call__ = handle
