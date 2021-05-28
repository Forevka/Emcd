from database.models.throttling_history import ThrottlingHistory
from datetime import datetime, timedelta
from database.models.notification_queue import NotificationQueue
from typing import List
from enums.notify_channel import NotifyChannel
from enums.notify_type import NotifyType

from asyncpg.connection import Connection


class NotificationRepository:
    def __init__(self, con: Connection):
        self.connection = con

    async def is_throttled(self, channel_id: int):
        sql = f'''
        {ThrottlingHistory.__select__}
        where end_datetime > $1
        '''
        
        return any([acc for acc in await self.connection.fetch(sql, datetime.now(),)])

    async def create_throttled_record(self, channel_id: int, wait_time: int):
        sql = '''
        insert into throttling_history(channel_id, start_datetime, end_datetime)
        values ($1, $2, $3)
        '''

        now = datetime.now()

        await self.connection.execute(sql, channel_id, now, now + timedelta(seconds=wait_time))

    async def update(self, item: NotificationQueue):
        sql = f'''
        update notification_queue
        set modified_datetime = CURRENT_TIMESTAMP
            , content = $1
            , type_id = $2
            , status_id = $3
            , result = $4
            , channel_id = $5
            , user_id = $6
        where notification_id = $7
        '''
        
        await self.connection.execute(sql, item.content, item.type_id, item.status_id,  item.result, item.channel_id, item.user_id, item.notification_id)

    async def add(self, content: str, type_id: NotifyType, notify_channels: List[NotifyChannel], to_user_id: int) -> int:
        sql = f'''
        insert into notification_queue(content, type_id, user_id, channel_id, status_id)
        select $1
            , $2
            , $3
            , nc.id
            , 1
        from notify_channel nc 
        where nc.id in (
            {', '.join([str(i.value) for i in notify_channels])}
        )
        RETURNING notification_id
        '''
        
        notification_id = await self.connection.fetchrow(sql, content, type_id.value, to_user_id,)
        if (notification_id):
            return notification_id['notification_id']


    async def get_page(self, status_id: int, channel_id: int, per_page: int, page_number: int) -> List[NotificationQueue]:
        sql = f'''
        {NotificationQueue.__select__}
        where "status_id" = $1 and "channel_id" = $2
        order by "created_datetime" desc
        limit $3 offset ($4 - 1) * $3
        '''

        return [NotificationQueue(**acc) for acc in await self.connection.fetch(sql, status_id, channel_id, per_page, page_number,)]