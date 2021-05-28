from typing import Optional
from database.models.user_conversation import UserConversation
from asyncpg.connection import Connection

class ConversationRepository:
    def __init__(self, con: Connection):
        self.connection = con

    async def add(self, tg_user_id: int, conversation_id: int):
        sql = '''
            INSERT into user_conversation(user_id, conversation_id)
            values ($1, $2)
        '''

        await self.connection.execute(sql, tg_user_id, conversation_id,)

    async def get(self, conversation_id: int) -> UserConversation:
        sql = '''
            SELECT user_id, conversation_id
            from user_conversation
            where conversation_id = $1
        '''
        
        res = await self.connection.fetchrow(sql, conversation_id,)
        if (res):
            return UserConversation(**res)

    async def add_conversation_message(self, conversation_id: int, message_id: Optional[int], message_text: str, notification_id: Optional[int]):
        sql = '''
            insert into conversation_message (conversation_id, message_id, message_text, notification_id)
            values ($1, $2, $3, $4)
        '''

        await self.connection.execute(sql, conversation_id, message_id, message_text, notification_id,)

    async def update_conversation_message(self, conversation_id: int, message_id: int,):
        sql = '''
            update conversation_message
            set message_id = $2
            where conversation_id = $1
        '''

        await self.connection.execute(sql, conversation_id, message_id,)

    async def find_conversation_id_by_notification_id(self, notification_id: int) -> int:
        sql = '''
        select conversation_id from conversation_message cm
        where cm.notification_id = $1 and message_id = -1
        '''

        conversation_id = await self.connection.fetchrow(sql, notification_id,)
        if (conversation_id):
            return conversation_id['conversation_id']

            
    async def find_conversation_id_by_message_id(self, message_id: int) -> int:
        sql = '''
        select conversation_id from conversation_message cm
        where cm.message_id = $1
        '''

        conversation_id = await self.connection.fetchrow(sql, message_id,)
        if (conversation_id):
            return conversation_id['conversation_id']