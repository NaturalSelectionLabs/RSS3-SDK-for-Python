from typing import List, Literal, Optional, Union

from pydantic import BaseModel

# File ids
RSS3ID = str  # Same as ethereum address
RSS3CustomItemsListID = str  # `${RSS3ID}-list-items.custom-${index}`
RSS3AutoItemsListID = str  # `${RSS3ID}-list-items.auto-0`
RSS3CustomAssetsListID = str  # `${RSS3ID}-list-assets.custom-${index}`
RSS3AutoAssetsListID = str  # `${RSS3ID}-list-assets.auto-0`
RSS3LinksListID = str  # `${RSS3ID}-list-links.${links.id}-${index}`
RSS3BacklinksListID = str  # `${RSS3ID}-list-backlinks.${backlinks.id}-0`
RSS3ItemBacklinksListID = str  # `${RSS3ID}-list-item.${item.index}.backlinks.${backlinks.id}-0`

ThirdPartyAddress = List[str]  # A series of url or ipfs hash that link to an identical file

# Item
RSS3CustomItemID = str  # `${RSS3ID}-item-custom-${index}`
RSS3AutoItemID = str  # `${RSS3ID}-item-auto-${index}`


class RSS3ItemBase(BaseModel):
    class BackLink(BaseModel):
        # todo: validate always true
        auto: bool = True
        id: str = ...
        list: RSS3ItemBacklinksListID = ...

    date_created: str = ...
    date_updated: str = ...
    title: Optional[str]
    summary: Optional[str]
    backlinks: Optional[List[BackLink]]


class RSS3CustomItem(RSS3ItemBase):
    class Link(BaseModel):
        id: str = ...
        target: Union[RSS3CustomItemID, RSS3AutoItemID] = ...

    class Content(BaseModel):
        tags: Optional[List[str]]
        address: ThirdPartyAddress = ...
        mime_type: str = ...
        name: Optional[str]
        size_in_bytes: Optional[str]
        duration_in_seconds: Optional[str]

    id: RSS3CustomItemID = ...
    tags: Optional[List[str]]
    authors: Optional[List[RSS3ID]]

    link: Optional[Link]
    contents: Optional[List[Content]]


class RSS3AutoItem(RSS3ItemBase):
    class Target(BaseModel):
        class Action(BaseModel):
            type: Literal["add", "remove", "update"] = ...
            payload: Optional[str]
            proof: Optional[str]

        field: str = ...
        action: Action = ...

    id: RSS3AutoItemID = ...
    target: Target = ...
