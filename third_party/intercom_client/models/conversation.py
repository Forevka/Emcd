# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = conversation_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


@dataclass
class Contact:
    id: Optional[str] = None
    type: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Contact':
        assert isinstance(obj, dict)
        id = from_union([from_none, from_str], obj.get("id"))
        type = from_union([from_none, from_str], obj.get("type"))
        return Contact(id, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_none, from_str], self.id)
        result["type"] = from_union([from_none, from_str], self.type)
        return result


@dataclass
class ConversationPart:
    assigned_to: None
    attachments: List[Any]
    author: Contact
    body: str
    created_at: int
    external_id: None
    id: str
    notified_at: int
    part_type: str
    type: str
    updated_at: int
    redacted: bool

    @staticmethod
    def from_dict(obj: Any) -> 'ConversationPart':
        assert isinstance(obj, dict)
        assigned_to = from_none(obj.get("assigned_to"))
        attachments = from_list(lambda x: x, obj.get("attachments"))
        author = Contact.from_dict(obj.get("author"))
        body = from_str(obj.get("body"))
        created_at = from_int(obj.get("created_at"))
        external_id = from_none(obj.get("external_id"))
        id = from_str(obj.get("id"))
        notified_at = from_int(obj.get("notified_at"))
        part_type = from_str(obj.get("part_type"))
        type = from_str(obj.get("type"))
        updated_at = from_int(obj.get("updated_at"))
        redacted = from_bool(obj.get("redacted"))
        return ConversationPart(assigned_to, attachments, author, body, created_at, external_id, id, notified_at, part_type, type, updated_at, redacted)

    def to_dict(self) -> dict:
        result: dict = {}
        result["assigned_to"] = from_none(self.assigned_to)
        result["attachments"] = from_list(lambda x: x, self.attachments)
        result["author"] = to_class(Contact, self.author)
        result["body"] = from_str(self.body)
        result["created_at"] = from_int(self.created_at)
        result["external_id"] = from_none(self.external_id)
        result["id"] = from_str(self.id)
        result["notified_at"] = from_int(self.notified_at)
        result["part_type"] = from_str(self.part_type)
        result["type"] = from_str(self.type)
        result["updated_at"] = from_int(self.updated_at)
        result["redacted"] = from_bool(self.redacted)
        return result


@dataclass
class ConversationParts:
    conversation_parts: List[ConversationPart]
    total_count: int
    type: str

    @staticmethod
    def from_dict(obj: Any) -> 'ConversationParts':
        assert isinstance(obj, dict)
        conversation_parts = from_list(ConversationPart.from_dict, obj.get("conversation_parts"))
        total_count = from_int(obj.get("total_count"))
        type = from_str(obj.get("type"))
        return ConversationParts(conversation_parts, total_count, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["conversation_parts"] = from_list(lambda x: to_class(ConversationPart, x), self.conversation_parts)
        result["total_count"] = from_int(self.total_count)
        result["type"] = from_str(self.type)
        return result


@dataclass
class Teammate:
    id: Optional[int] = None
    type: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Teammate':
        assert isinstance(obj, dict)
        id = from_union([from_none, from_int, lambda x: int(from_str(x))], obj.get("id"))
        type = from_union([from_none, from_str], obj.get("type"))
        name = from_union([from_none, from_str], obj.get("name"))
        email = from_union([from_none, from_str], obj.get("email"))
        return Teammate(id, type, name, email)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_int((lambda x: is_type(int, x))(x))], self.id)
        result["type"] = from_union([from_none, from_str], self.type)
        result["name"] = from_union([from_none, from_str], self.name)
        result["email"] = from_union([from_none, from_str], self.email)
        return result


@dataclass
class ConversationRating:
    created_at: None
    contact: Contact
    rating: None
    remark: None
    teammate: Teammate

    @staticmethod
    def from_dict(obj: Any) -> 'ConversationRating':
        assert isinstance(obj, dict)
        created_at = from_none(obj.get("created_at"))
        contact = Contact.from_dict(obj.get("contact"))
        rating = from_none(obj.get("rating"))
        remark = from_none(obj.get("remark"))
        teammate = Teammate.from_dict(obj.get("teammate"))
        return ConversationRating(created_at, contact, rating, remark, teammate)

    def to_dict(self) -> dict:
        result: dict = {}
        result["created_at"] = from_none(self.created_at)
        result["contact"] = to_class(Contact, self.contact)
        result["rating"] = from_none(self.rating)
        result["remark"] = from_none(self.remark)
        result["teammate"] = to_class(Teammate, self.teammate)
        return result


@dataclass
class CustomAttributes:
    issue_type: str
    priority: str

    @staticmethod
    def from_dict(obj: Any) -> 'CustomAttributes':
        assert isinstance(obj, dict)
        issue_type = obj.get("issue_type")
        priority = obj.get("priority")
        return CustomAttributes(issue_type, priority)

    def to_dict(self) -> dict:
        result: dict = {}
        result["issue_type"] = from_str(self.issue_type)
        result["priority"] = from_str(self.priority)
        return result


@dataclass
class FirstContactReply:
    created_at: int
    type: str
    url: str

    @staticmethod
    def from_dict(obj: Any) -> 'FirstContactReply':
        assert isinstance(obj, dict)
        created_at = from_int(obj.get("created_at"))
        type = from_str(obj.get("type"))
        url = from_str(obj.get("url"))
        return FirstContactReply(created_at, type, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["created_at"] = from_int(self.created_at)
        result["type"] = from_str(self.type)
        result["url"] = from_str(self.url)
        return result


@dataclass
class SlaApplied:
    sla_name: str
    sla_status: str

    @staticmethod
    def from_dict(obj: Any) -> 'SlaApplied':
        assert isinstance(obj, dict)
        sla_name = from_str(obj.get("sla_name"))
        sla_status = from_str(obj.get("sla_status"))
        return SlaApplied(sla_name, sla_status)

    def to_dict(self) -> dict:
        result: dict = {}
        result["sla_name"] = from_str(self.sla_name)
        result["sla_status"] = from_str(self.sla_status)
        return result


@dataclass
class Source:
    attachments: List[Any]
    author: Contact
    body: str
    delivered_as: str
    id: int
    subject: str
    type: str
    url: str
    redacted: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Source':
        assert isinstance(obj, dict)
        attachments = from_list(lambda x: x, obj.get("attachments"))
        author = Contact.from_dict(obj.get("author"))
        body = from_str(obj.get("body"))
        delivered_as = from_str(obj.get("delivered_as"))
        id = int(from_str(obj.get("id")))
        subject = from_str(obj.get("subject"))
        type = from_str(obj.get("type"))
        url = obj.get("url")
        redacted = from_bool(obj.get("redacted"))
        return Source(attachments, author, body, delivered_as, id, subject, type, url, redacted)

    def to_dict(self) -> dict:
        result: dict = {}
        result["attachments"] = from_list(lambda x: x, self.attachments)
        result["author"] = to_class(Contact, self.author)
        result["body"] = from_str(self.body)
        result["delivered_as"] = from_str(self.delivered_as)
        result["id"] = from_str(str(self.id))
        result["subject"] = from_str(self.subject)
        result["type"] = from_str(self.type)
        result["url"] = from_str(self.url)
        result["redacted"] = from_bool(self.redacted)
        return result


@dataclass
class Statistics:
    time_to_assignment: int
    time_to_admin_reply: int
    time_to_first_close: int
    time_to_last_close: int
    median_time_to_reply: int
    first_contacat_reply_at: int
    first_assignment_at: int
    first_admin_reply_at: int
    first_close_at: int
    last_assignment_at: int
    last_assignment_admin_reply_at: int
    last_contact_reply_at: int
    last_admin_reply_at: int
    last_close_at: int
    last_closed_by: Teammate
    count_reopens: int
    count_assignments: int
    count_conversation_parts: int

    @staticmethod
    def from_dict(obj: Any) -> 'Statistics':
        assert isinstance(obj, dict)
        time_to_assignment = from_int(obj.get("time_to_assignment"))
        time_to_admin_reply = from_int(obj.get("time_to_admin_reply"))
        time_to_first_close = from_int(obj.get("time_to_first_close"))
        time_to_last_close = from_int(obj.get("time_to_last_close"))
        median_time_to_reply = from_int(obj.get("median_time_to_reply"))
        first_contacat_reply_at = from_int(obj.get("first_contacat_reply_at"))
        first_assignment_at = from_int(obj.get("first_assignment_at"))
        first_admin_reply_at = from_int(obj.get("first_admin_reply_at"))
        first_close_at = from_int(obj.get("first_close_at"))
        last_assignment_at = from_int(obj.get("last_assignment_at"))
        last_assignment_admin_reply_at = from_int(obj.get("last_assignment_admin_reply_at"))
        last_contact_reply_at = from_int(obj.get("last_contact_reply_at"))
        last_admin_reply_at = from_int(obj.get("last_admin_reply_at"))
        last_close_at = from_int(obj.get("last_close_at"))
        last_closed_by = Teammate.from_dict(obj.get("last_closed_by"))
        count_reopens = from_int(obj.get("count_reopens"))
        count_assignments = from_int(obj.get("count_assignments"))
        count_conversation_parts = from_int(obj.get("count_conversation_parts"))
        return Statistics(time_to_assignment, time_to_admin_reply, time_to_first_close, time_to_last_close, median_time_to_reply, first_contacat_reply_at, first_assignment_at, first_admin_reply_at, first_close_at, last_assignment_at, last_assignment_admin_reply_at, last_contact_reply_at, last_admin_reply_at, last_close_at, last_closed_by, count_reopens, count_assignments, count_conversation_parts)

    def to_dict(self) -> dict:
        result: dict = {}
        result["time_to_assignment"] = from_int(self.time_to_assignment)
        result["time_to_admin_reply"] = from_int(self.time_to_admin_reply)
        result["time_to_first_close"] = from_int(self.time_to_first_close)
        result["time_to_last_close"] = from_int(self.time_to_last_close)
        result["median_time_to_reply"] = from_int(self.median_time_to_reply)
        result["first_contacat_reply_at"] = from_int(self.first_contacat_reply_at)
        result["first_assignment_at"] = from_int(self.first_assignment_at)
        result["first_admin_reply_at"] = from_int(self.first_admin_reply_at)
        result["first_close_at"] = from_int(self.first_close_at)
        result["last_assignment_at"] = from_int(self.last_assignment_at)
        result["last_assignment_admin_reply_at"] = from_int(self.last_assignment_admin_reply_at)
        result["last_contact_reply_at"] = from_int(self.last_contact_reply_at)
        result["last_admin_reply_at"] = from_int(self.last_admin_reply_at)
        result["last_close_at"] = from_int(self.last_close_at)
        result["last_closed_by"] = to_class(Teammate, self.last_closed_by)
        result["count_reopens"] = from_int(self.count_reopens)
        result["count_assignments"] = from_int(self.count_assignments)
        result["count_conversation_parts"] = from_int(self.count_conversation_parts)
        return result


@dataclass
class Tags:
    tags: List[Any]
    type: str

    @staticmethod
    def from_dict(obj: Any) -> 'Tags':
        assert isinstance(obj, dict)
        tags = from_list(lambda x: x, obj.get("tags"))
        type = from_str(obj.get("type"))
        return Tags(tags, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["tags"] = from_list(lambda x: x, self.tags)
        result["type"] = from_str(self.type)
        return result


@dataclass
class Topics:
    type: str
    topics: List[Teammate]
    total_count: int

    @staticmethod
    def from_dict(obj: Any) -> 'Topics':
        assert isinstance(obj, dict)
        type = from_str(obj.get("type"))
        topics = from_list(Teammate.from_dict, obj.get("topics"))
        total_count = from_int(obj.get("total_count"))
        return Topics(type, topics, total_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_str(self.type)
        result["topics"] = from_list(lambda x: to_class(Teammate, x), self.topics)
        result["total_count"] = from_int(self.total_count)
        return result


@dataclass
class Conversation:
    type: str
    id: int
    created_at: int
    updated_at: int
    source: Source
    contacts: List[Contact]
    teammates: List[Teammate]
    admin_assignee_id: int
    team_assignee_id: None
    custom_attributes: CustomAttributes
    topics: Topics
    open: bool
    state: str
    read: bool
    waiting_since: int
    snoozed_until: None
    tags: Tags
    first_contact_reply: FirstContactReply
    priority: str
    sla_applied: SlaApplied
    conversation_rating: ConversationRating
    statistics: Statistics
    conversation_parts: ConversationParts

    @staticmethod
    def from_dict(obj: Any) -> 'Conversation':
        assert isinstance(obj, dict)
        type = from_str(obj.get("type"))
        id = int(from_str(obj.get("id")))
        created_at = from_int(obj.get("created_at"))
        updated_at = from_int(obj.get("updated_at"))
        source = Source.from_dict(obj.get("source"))
        contacts = Contact.from_dict, obj.get("contacts")
        teammates = Teammate.from_dict, obj.get("teammates")
        admin_assignee_id = int(obj.get("admin_assignee_id"))
        team_assignee_id = from_none(obj.get("team_assignee_id"))
        custom_attributes = CustomAttributes.from_dict(obj.get("custom_attributes"))
        topics = Topics.from_dict(obj.get("topics"))
        open = from_bool(obj.get("open"))
        state = obj.get("state")
        read = from_bool(obj.get("read"))
        waiting_since = from_int(obj.get("waiting_since"))
        snoozed_until = from_none(obj.get("snoozed_until"))
        tags = Tags.from_dict(obj.get("tags"))
        first_contact_reply = FirstContactReply.from_dict(obj.get("first_contact_reply"))
        priority = from_str(obj.get("priority"))
        sla_applied = SlaApplied.from_dict(obj.get("sla_applied"))
        conversation_rating = ConversationRating.from_dict(obj.get("conversation_rating"))
        statistics = Statistics.from_dict(obj.get("statistics"))
        conversation_parts = ConversationParts.from_dict(obj.get("conversation_parts"))
        return Conversation(type, id, created_at, updated_at, source, contacts, teammates, admin_assignee_id, team_assignee_id, custom_attributes, topics, open, state, read, waiting_since, snoozed_until, tags, first_contact_reply, priority, sla_applied, conversation_rating, statistics, conversation_parts)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_str(self.type)
        result["id"] = from_str(str(self.id))
        result["created_at"] = from_int(self.created_at)
        result["updated_at"] = from_int(self.updated_at)
        result["source"] = to_class(Source, self.source)
        result["contacts"] = from_list(lambda x: to_class(Contact, x), self.contacts)
        result["teammates"] = from_list(lambda x: to_class(Teammate, x), self.teammates)
        result["admin_assignee_id"] = from_str(str(self.admin_assignee_id))
        result["team_assignee_id"] = from_none(self.team_assignee_id)
        result["custom_attributes"] = to_class(CustomAttributes, self.custom_attributes)
        result["topics"] = to_class(Topics, self.topics)
        result["open"] = from_bool(self.open)
        result["state"] = self.state
        result["read"] = from_bool(self.read)
        result["waiting_since"] = from_int(self.waiting_since)
        result["snoozed_until"] = from_none(self.snoozed_until)
        result["tags"] = to_class(Tags, self.tags)
        result["first_contact_reply"] = to_class(FirstContactReply, self.first_contact_reply)
        result["priority"] = from_str(self.priority)
        result["sla_applied"] = to_class(SlaApplied, self.sla_applied)
        result["conversation_rating"] = to_class(ConversationRating, self.conversation_rating)
        result["statistics"] = to_class(Statistics, self.statistics)
        result["conversation_parts"] = to_class(ConversationParts, self.conversation_parts)
        return result


def conversation_from_dict(s: Any) -> Conversation:
    return Conversation.from_dict(s)


def conversation_to_dict(x: Conversation) -> Any:
    return to_class(Conversation, x)
