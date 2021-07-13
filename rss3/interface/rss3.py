from .items import *
from rss3.settings import ITEM_PAGE_SIZE
import marshmallow
import dataclasses


@dataclass
class RSS3ItemInput:
    authors: list[str] = field(default_factory=list)

    id: str = field(default_factory=str)
    title: str = field(default_factory=str)
    summary: str = field(default_factory=str)
    tags: list[str] = field(default_factory=list)

    type_: str = field(default_factory=str, metadata={"data_key": "type", "skip_if": None})
    upstream: str = field(default_factory=str)

    contents: list[RSSContent] = field(default_factory=list,
                                       metadata={"validate": marshmallow.validate.Length(max=ITEM_PAGE_SIZE)})

    @classmethod
    def from_instance(cls, instance):
        return cls(**dataclasses.asdict(instance))


@dataclass
class RSS3Item(BaseSchema, RSS3ItemInput):
    id: str = field(default_factory=str)
    date_published: str = field(default_factory=str)
    date_modified: str = field(default_factory=str)
    contexts__: list[RSS3Context] = field(default_factory=list, metadata={"data_key": "@contexts",
                                                                          "validate": marshmallow.validate.Length(
                                                                              max=ITEM_PAGE_SIZE)})
    signature: str = field(default_factory=str)


@dataclass
class RSS3ProfileInput(BaseSchema):
    name: str = field(default_factory=str)
    avatar: List[str] = field(default_factory=list)
    bio: str = field(default_factory=str)
    tags: list[str] = field(default_factory=list)

    @classmethod
    def from_instance(cls, instance):
        return cls(**dataclasses.asdict(instance))


@dataclass
class RSS3Profile(RSS3ProfileInput):
    signature: str = field(default_factory=str)


@dataclass
class RSS3LinkInput(BaseSchema):
    type_: str = field(default_factory=str, metadata={"data_key": "type"})
    tags: List[str] = field(default_factory=list)
    list_: List[str] = field(default_factory=list, metadata={"data_key": "list"})

    @classmethod
    def from_instance(cls, instance):
        return cls(**dataclasses.asdict(instance))


@dataclass
class RSS3Link(RSS3LinkInput):
    signature: str = field(default_factory=str)


@dataclass
class RSS3Base:
    id: str = field(default_factory=str)
    date_created: str = field(default_factory=str)
    date_updated: str = field(default_factory=str)
    version__: str = field(default='rss3.io/version/v0.1.0', metadata={"data_key": "@version"})


@dataclass
class RSS3Items(BaseSchema, RSS3Base):
    id: str = field(default_factory=str)
    signature: str = field(default_factory=str)

    items: list[RSS3Item] = field(default_factory=list,
                                  metadata={"validate": marshmallow.validate.Length(max=ITEM_PAGE_SIZE)})
    items_next: str = field(default=None)


@dataclass
class RSS3Index(BaseSchema, RSS3Base):
    id: str = field(default_factory=str)
    signature: str = field(default_factory=str)
    profile: RSS3Profile = field(default_factory=dict)
    items: list[RSS3Item] = field(default_factory=list)
    items_next: str = field(default=None)

    links: list[RSS3Link] = field(default_factory=list,
                                  metadata={"validate": marshmallow.validate.Length(max=ITEM_PAGE_SIZE)})
    backlinks__: list[RSS3BackLink] = field(default_factory=list, metadata={"data_key": "@backlinks",
                                                                            "validate": marshmallow.validate.Length(
                                                                                max=ITEM_PAGE_SIZE)})

    assets: list[RSS3Asset] = field(default_factory=list)


@dataclass
class RSS3List(BaseSchema, RSS3Base):
    id: str = field(default_factory=str)
    list_: list[str] = field(default_factory=list, metadata={"data_key": "list"})
    list_next: str = field(default=None)
