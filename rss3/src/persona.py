#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   persona.py    
@Contact :   leetao94cn@gmail.com
@Description：
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/6/24 9:14 下午   leetao      1.0         None
"""

# import lib
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from .index import RSS3

from ..utils import private_key_to_address, create


class Persona:
    rss3: 'RSS3'
    private_key: str
    id: str

    def __init__(self, rss3: 'RSS3'):
        self.rss3 = rss3
        if self.rss3.options.private_key:
            self.private_key = self.rss3.options.private_key
            self.id = private_key_to_address(self.rss3.options.private_key)
        else:
            account = create()
            self.private_key = account.key.hex()
            self.id = account.address
            self.rss3.file.new(self.id)

    async def sync(self) -> None:
        return await self.rss3.file.sync()

    async def raw(self, file_id: str) -> Dict:
        return await self.rss3.file.get(file_id)
