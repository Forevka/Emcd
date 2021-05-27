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