import os
from config import DEFAULT_LANG, START_TIME
from database.user_repo import UserRepository
from aiogram import types
from git import Repo

async def cmd_version(message: types.Message, user: UserRepository, _: dict):
    repo = Repo()

    message_text = f'''Branch: {repo.active_branch.name}
Commit date: {repo.active_branch.commit.committed_datetime.strftime("%d/%m/%Y %H:%M:%S")}
Start time: {START_TIME.strftime("%d/%m/%Y %H:%M:%S")}
Environment name: {os.environ.get('ENV_NAME')}
    '''

    await message.answer(message_text)