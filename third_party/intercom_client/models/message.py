# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = message_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Message:
    type: str
    id: int
    created_at: int
    subject: str
    body: str
    message_type: str

    @staticmethod
    def from_dict(obj: Any) -> 'Message':
        assert isinstance(obj, dict)
        type = from_str(obj.get("type"))
        id = int(from_str(obj.get("id")))
        created_at = from_int(obj.get("created_at"))
        subject = from_str(obj.get("subject"))
        body = from_str(obj.get("body"))
        message_type = from_str(obj.get("message_type"))
        return Message(type, id, created_at, subject, body, message_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_str(self.type)
        result["id"] = from_str(str(self.id))
        result["created_at"] = from_int(self.created_at)
        result["subject"] = from_str(self.subject)
        result["body"] = from_str(self.body)
        result["message_type"] = from_str(self.message_type)
        return result


def message_from_dict(s: Any) -> Message:
    return Message.from_dict(s)


def message_to_dict(x: Message) -> Any:
    return to_class(Message, x)
