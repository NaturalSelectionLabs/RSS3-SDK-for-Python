#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   links.py    
@Contact :   leetao94cn@gmail.com
@Description：
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/7/3 4:00 下午   leetao      1.0         None
"""

# import lib
from typing import TYPE_CHECKING

from ..interface import RSS3LinkInput, RSS3Link, IRSS3LinkSchema
from .. import utils

if TYPE_CHECKING:
    from .index import RSS3


class Links:
    rss3: 'RSS3'

    def __init__(self, rss3: 'RSS3'):
        self.rss3 = rss3

    async def get(self, file_id: str, type_: str):
        if not file_id:
            file_id = self.rss3.persona.id
        file_ = await self.rss3.file.get(file_id)
        link_list = file_.get("links", [])
        if type_:
            return next((link for link in link_list if link.get("type") == type_), {})
        return link_list

    async def post(self, link_in: RSS3LinkInput):
        file_ = await self.rss3.file.get(self.rss3.persona.id)
        link_list = file_.get("links", [])
        assert next((link_item for link_item in link_list if link_item.get("type") == link_in.type_), None) is None
        link = RSS3Link.from_instance(link_in)
        link.signature = utils.sign(IRSS3LinkSchema.dump(link), self.rss3.persona.private_key)
        link_list.append(IRSS3LinkSchema.dump(link))
        file_['links'] = link_list
        self.rss3.file.set(file_)

    async def delete(self, type_: str):
        file_ = await self.rss3.file.get(self.rss3.persona.id)
        exist_link_list = file_.get("links", [])
        filter_link_list = [(index, links) for index, links in enumerate(exist_link_list) if links.get("type") == type_]
        assert len(filter_link_list) >= 1
        index, _ = filter_link_list[0]
        file_['links'].pop(index)
        self.rss3.file.set(file_)

    async def patch(self, link_in: RSS3LinkInput):
        file_ = await self.rss3.file.get(self.rss3.persona.id)
        exist_link_list = file_.get("links", [])
        assert len(exist_link_list) >= 1
        filter_link_list = [(index, links) for index, links in enumerate(exist_link_list) if
                            links.get("type") == link_in.type_]
        assert len(filter_link_list) >= 1
        index, _ = filter_link_list[0]
        link = RSS3Link.from_instance(link_in)
        link.signature = utils.sign(IRSS3LinkSchema.dump(link), self.rss3.persona.private_key)
        file_['links'][index] = IRSS3LinkSchema.dump(link)
        self.rss3.file.set(file_)
