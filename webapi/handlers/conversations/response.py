from database.conversation_repo import ConversationRepository
from database.notification_repo import NotificationRepository
from database.user_repo import UserRepository
from fastapi import Request
from webapi.models.intercom.webhooks.conversation import Conversation
from enums.notify_channel import NotifyChannel
from enums.notify_type import NotifyType
from bot.common.lang import LangHolder
from enums.lang import Lang
from io import StringIO
from html.parser import HTMLParser
from typing import Any, Dict, AnyStr, List, Union


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]

async def response(request: Request, model: JSONStructure = None):
    if (model[b'topic'] == 'conversation.admin.replied'):
        model = await request.json()
        print(model)
        conv = Conversation(**model)
        conv_repo = ConversationRepository(request.state.connection)
        notification_repo = NotificationRepository(request.state.connection)
        
        db_conv = await conv_repo.get(conv.data.item.id)

        if (db_conv):
            user_repo = UserRepository(request.state.connection)
            
            user = await user_repo.get_user(db_conv.user_id)
            if (user):
                c_user_locale_code = Lang(user.lang_id).name
                langs = LangHolder(user.lang_id, c_user_locale_code,)

                msg_text = langs['feedback_from_admin'].format(
                    feedback_text=strip_tags(conv.data.item.conversation_parts.conversation_parts[0].body),
                    conversation_id=conv.data.item.id,
                )

                await notification_repo.add(msg_text, NotifyType.Conversation, [NotifyChannel.Telegram], db_conv.user_id)

    return {
        
    }
