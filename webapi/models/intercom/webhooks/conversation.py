from typing import Optional, List, Any

from pydantic.main import BaseModel


class Assignee(BaseModel):
    id: Optional[int] = None
    type: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True


class Author(BaseModel):
    type: Optional[str] = None
    id: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True


class ConversationMessage(BaseModel):
    id: Optional[int] = None
    type: Optional[str] = None
    url: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    author: Optional[Author] = None
    attachments: Optional[List[Any]] = None
    
    class Config:
        arbitrary_types_allowed = True


class ConversationPart(BaseModel):
    assigned_to: Optional[str] = None
    external_id: Optional[str] = None
    type: Optional[str] = None
    id: Optional[str] = None
    part_type: Optional[str] = None
    body: Optional[str] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    notified_at: Optional[int] = None
    author: Optional[Assignee] = None
    attachments: Optional[List[Any]] = None

    class Config:
        arbitrary_types_allowed = True


class ConversationParts(BaseModel):
    type: Optional[str] = None
    conversation_parts: Optional[List[ConversationPart]] = None
    total_count: Optional[int] = None

    class Config:
        arbitrary_types_allowed = True


class ConversationRatingClass(BaseModel):
    pass
    
    class Config:
        arbitrary_types_allowed = True


class PurpleLinks(BaseModel):
    conversation_web: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True


class Tags(BaseModel):
    type: Optional[str] = None
    tags: Optional[List[Any]] = None
    
    class Config:
        arbitrary_types_allowed = True


class User(BaseModel):
    user_id: Optional[str] = None
    name: Optional[str] = None
    do_not_track: Optional[None] = None
    type: Optional[str] = None
    id: Optional[str] = None
    email: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True


class Item(BaseModel):
    id: Optional[int] = None
    team_assignee_id: Optional[str] = None
    snoozed_until: Optional[str] = None
    type: Optional[str] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    user: Optional[User] = None
    assignee: Optional[Assignee] = None
    admin_assignee_id: Optional[int] = None
    conversation_message: Optional[ConversationMessage] = None
    conversation_parts: Optional[ConversationParts] = None
    conversation_rating: Optional[ConversationRatingClass] = None
    open: Optional[bool] = None
    state: Optional[str] = None
    read: Optional[bool] = None
    metadata: Optional[ConversationRatingClass] = None
    tags: Optional[Tags] = None
    tags_added: Optional[Tags] = None
    custom_attributes: Optional[ConversationRatingClass] = None
    links: Optional[PurpleLinks] = None
    
    class Config:
        arbitrary_types_allowed = True


class Data(BaseModel):
    type: Optional[str] = None
    item: Optional[Item] = None
    
    class Config:
        arbitrary_types_allowed = True


class Conversation(BaseModel):
    self: Optional[str] = None
    type: Optional[str] = None
    app_id: Optional[str] = None
    data: Optional[Data] = None
    links: Optional[ConversationRatingClass] = None
    id: Optional[str] = None
    topic: Optional[str] = None
    delivery_status: Optional[str] = None
    delivery_attempts: Optional[int] = None
    delivered_at: Optional[int] = None
    first_sent_at: Optional[int] = None
    created_at: Optional[int] = None
    
    class Config:
        arbitrary_types_allowed = True
