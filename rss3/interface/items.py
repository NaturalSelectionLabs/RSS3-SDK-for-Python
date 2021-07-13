from dataclasses import field
from marshmallow import Schema, post_dump
from marshmallow_dataclass import dataclass
from typing import List


class BaseSchema(Schema):
    SKIP_VALUES = set([None])

    @post_dump
    def remove_skip_values(self, data, **kwargs):
        data_items = data.items()
        data = {}
        for key, value in data_items:
            if value not in [None] and value:
                data[key] = value
        return data


@dataclass
class RSS3Context(BaseSchema):
    type_: str = field(default_factory=str, metadata={"data_key": "type"})
    list_: str = field(default_factory=str, metadata={"data_key": "list"})


@dataclass
class RSSContent(BaseSchema):
    address: List[str] = field(default_factory=list)
    mime_type: str = field(default_factory=str)
    name: str = field(default_factory=str)
    tags: List[str] = field(default_factory=list)
    size_in_bytes: str = field(default_factory=str)
    duration_in_seconds: str = field(default_factory=str)


@dataclass
class RSS3BackLink(BaseSchema):
    type_: str = field(default_factory=str, metadata={"data_key": "type"})
    list_: str = field(default_factory=str, metadata={"data_key": "list"})


@dataclass
class RSS3Asset(BaseSchema):
    type_: str = field(default_factory=str, metadata={"data_key": "type"})
    tags: List[str] = field(default_factory=list)
    content: str = field(default_factory=str)
