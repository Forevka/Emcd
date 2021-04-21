from bot.handlers.text.base_command_handler import BaseCommandHandler
import datetime
import os

from aiogram import types
from config import POEDITOR_ID, POEDITOR_TOKEN, START_TIME
from database.user_repo import UserRepository
from git import Repo

class CmdVersion(BaseCommandHandler):
    async def handle(self, message: types.Message, user: UserRepository, _: dict):
        repo = Repo()

        message_text = f'''Branch: {repo.active_branch.name}
Commit date: {repo.active_branch.commit.committed_datetime.strftime("%d/%m/%Y %H:%M:%S")}
Start time: {START_TIME.strftime("%d/%m/%Y %H:%M:%S")}
Environment name: {os.environ.get('ENV_NAME')}
Local time: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
        '''

        await message.answer(message_text)
        
    __call__ = handle
