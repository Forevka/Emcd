from database.models.user import User
from database.models.question_answer_translation import QuestionAnswerTranslate
from database.models.broadcast_to_send import BroadcastToSend
import typing
from typing import List

from asyncpg.connection import Connection

class BroadcastRepository:
    def __init__(self, con: Connection):
        self.connection = con

    async def get_all_user_by_lang(self, lang_id: int) -> List[User]:
        sql = f"""
        {User.__select__} where "lang_id" = $1
        """

        return [User(**acc) for acc in await self.connection.fetch(sql, lang_id,)]

    async def get_all_broadcasts_to_send(self,) -> List[BroadcastToSend]:
        sql = f"""
        {BroadcastToSend.__select__}
        """

        return [BroadcastToSend(**acc) for acc in await self.connection.fetch(sql,)]

    async def update_broadcast_status(self, broadcast_id: int, status_id: int):
        sql = """
        update broadcast
        set status_id = $2
        where id = $1
        """

        await self.connection.execute(sql, broadcast_id, status_id,)
    
    async def update_broadcast_batch_status(self, broadcast_id: int, lang_id: int, status_id: int):
        sql = """
        update broadcast_lang
        set status_id = $3
        where broadcast_id = $1 and lang_id = $2
        """

        await self.connection.execute(sql, broadcast_id, lang_id, status_id,)

    async def update_broadcast_batch_start_time(self, broadcast_id: int, lang_id: int,):
        sql = """
        update broadcast_lang
        set start_datetime = CURRENT_TIMESTAMP
        where broadcast_id = $1 and lang_id = $2
        """

        await self.connection.execute(sql, broadcast_id, lang_id,)

        
    async def update_broadcast_batch_end_time(self, broadcast_id: int, lang_id: int,):
        sql = """
        update broadcast_lang
        set end_datetime = CURRENT_TIMESTAMP
        where broadcast_id = $1 and lang_id = $2
        """

        await self.connection.execute(sql, broadcast_id, lang_id,)
