import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.handlers.text.base_command_handler import BaseCommandHandler
from config import INTERCOM_TOKEN
from database.conversation_repo import ConversationRepository
from database.user_repo import UserRepository
from third_party.intercom_client.client import IntercomClient
from utils.get_or_create_intercom_contact import get_intercom_contact


class ReplyToConversation(BaseCommandHandler):
    async def handle(
        self,
        message: types.Message,
        user: UserRepository,
        _: dict,
        state: FSMContext,
        logger: logging.Logger,
    ):
        if message.reply_to_message:
            conv_repo = ConversationRepository(user.connection)
            conv_id = await conv_repo.find_conversation_id_by_message_id(
                message.reply_to_message.message_id
            )

            if conv_id:
                async with IntercomClient(INTERCOM_TOKEN) as intercom:
                    intercom_user = await get_intercom_contact(message.from_user)
                    
                    async with state.proxy() as data:
                        attachments_ids = data.get('attachments', [])
                        attachments_urls = [message.bot.get_file_url((await message.bot.get_file(i)).file_path) for i in attachments_ids]
                        await intercom.reply_to_conversation(
                            intercom_user["id"], message.text, conv_id, attachments_urls,
                        )
        else:
            conv_id = None

            async with state.proxy() as data:
                conv_id = data["reply_to_conversation"]

            if conv_id:
                async with IntercomClient(INTERCOM_TOKEN) as intercom:
                    intercom_user = await get_intercom_contact(message.from_user)
                    
                    async with state.proxy() as data:
                        attachments_ids = data.get('attachments', [])
                        attachments_urls = [message.bot.get_file_url((await message.bot.get_file(i)).file_path) for i in attachments_ids]

                        await intercom.reply_to_conversation(
                            intercom_user["id"], message.text, conv_id, attachments_urls
                        )
            else:
                logger.warning(f"user can't reply to conversation {conv_id}, user id {message.from_user.id}")
                await message.answer("Попробуйте заново")

        await message.answer(_['feedback_accepted'])
        await state.finish()


    __call__ = handle
