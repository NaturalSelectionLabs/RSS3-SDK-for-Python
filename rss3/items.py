#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   items.py    
@Contact :   leetao94cn@gmail.com
@Description：
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/7/3 3:57 下午   leetao      1.0         None
"""

# import lib

from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .index import RSS3


class Items:
    rss3: 'RSS3'

    def __init__(self, rss3: 'RSS3'):
        self.rss3 = rss3

    async def get(self, file_id: str) -> Dict:
        file_ = await self.rss3.file.get(file_id)
        return {
            'items': file_.get("items", []),
            'items_next': file_.get("items_next", [])
        }
