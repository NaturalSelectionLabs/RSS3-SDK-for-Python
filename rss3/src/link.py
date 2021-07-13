#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   link.py    
@Contact :   leetao94cn@gmail.cn
@Description：
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/7/13 7:41 下午   leetao      1.0         None
"""

# import lib

from typing import TYPE_CHECKING, List, Dict, Tuple

from ..interface import RSS3LinkInput

if TYPE_CHECKING:
    from .index import RSS3


class Link:
    rss3: 'RSS3'

    def __init__(self, rss3: 'RSS3'):
        self.rss3 = rss3

    async def _get_filter_links(self, type_: str) -> Tuple[List[tuple[int, Dict]], Dict]:
        file_ = await self.rss3.file.get(self.rss3.persona.id)
        exist_link_list = file_.get("links", [])
        filter_link_list = [(index, links) for index, links in enumerate(exist_link_list) if links.get("type") == type_]
        return filter_link_list, file_

    async def post(self, type_: str, persona_id: str):
        filter_link_list, file_ = await self._get_filter_links(type_)
        if filter_link_list:
            assert len(filter_link_list) >= 1
            index, target_links = filter_link_list[0]
            assert persona_id not in target_links.get("list", [])
            target_links['list'].append(persona_id)
            file_['links'][index] = target_links
            await self.rss3.file.set(file_)
        else:
            link_input = RSS3LinkInput(type_=type_, list_=[persona_id])
            await self.rss3.links.post(link_input)

    async def delete(self, type_: str, persona_id: str):
        filter_link_list, file_ = await self._get_filter_links(type_)
        assert len(filter_link_list) >= 1
        index, target_links = filter_link_list[0]
        target_list = target_links.get("list", [])
        assert persona_id in target_list
        target_list.remove(persona_id)
        target_links['list'] = target_list
        file_['links'][index] = target_links
        await self.rss3.file.set(file_)
