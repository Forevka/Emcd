from typing import List

from aiogram.dispatcher.storage import FSMContext
from bot.handlers.text.base_command_handler import BaseCommandHandler
from aiogram import types
from database.user_repo import UserRepository


class AddPhotoToConversation(BaseCommandHandler):
    async def handle(
        self,
        message: types.Message,
        user: UserRepository,
        _: dict,
        album: List[types.Message],
        state: FSMContext,
    ):
        files = []
        if not album:
            album.append(message)

        for obj in album:

            if obj.photo:
                files.append(obj.photo[-1].file_id)
            else:
                files.append(obj[obj.content_type].file_id)

            #file = await message.bot.get_file(file_id)
            #url = message.bot.get_file_url(file.file_path)
        
        async with state.proxy() as data:
            attachments = data.get('attachments', [])
            attachments = attachments + files
            data['attachments'] = attachments

        await message.answer(_['attachments_accepted'])

    __call__ = handle
