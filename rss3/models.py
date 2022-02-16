from typing import List, Optional

from pydantic import BaseModel

# todo: define RSS3 related types


class RSS3ItemBase(BaseModel):
    class BackLink(BaseModel):
        # todo: validate always true
        auto: bool = True
        id: str = ...
        list: str = ...

    date_created: str = ...
    date_updated: str = ...
    title: Optional[str]
    summary: Optional[str]
    backlinks: Optional[List[BackLink]]


class RSS3CustomItem(RSS3ItemBase):
    class Link(BaseModel):
        id: str = ...
        target: str = ...

    class Content(BaseModel):
        tags: Optional[List[str]]
        address: str = ...
        mime_type: str = ...
        name: Optional[str]
        size_in_bytes: Optional[str]
        duration_in_seconds: Optional[str]

    id: str = ...
    tags: Optional[List[str]]
    authors: Optional[List[str]]

    link: Optional[Link]
    contents: Optional[List[Content]]
