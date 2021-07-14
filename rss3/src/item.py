#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   item.py    
@Contact :   leetao94cn@gmail.com
@Description：
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/6/26 5:46 下午   leetao      1.0         None
"""

# import lib
from ..interface import RSS3ItemInput, RSS3Item, IRSS3ItemSchema
from .. import utils
from ..settings import ITEM_PAGE_SIZE

from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from rss3.src.index import RSS3


class Item:
    rss3: 'RSS3'

    def __init__(self, rss3: 'RSS3'):
        self.rss3 = rss3

    async def get_position(self, item_id: str) -> Dict:
        file_id = self.rss3.persona.id
        file_ = await self.rss3.file.get(file_id)
        assert 'items' in file_
        items = file_['items']
        file_items_id_list = [item['id'] for item in items]
        if item_id not in file_items_id_list:
            parsed = utils.parse(item_id)
            file_id = f'{self.rss3.persona.id}-items-{parsed["index"] // ITEM_PAGE_SIZE}'
            file_ = await self.rss3.file.get(file_id)
            assert 'items' in file_
            items = file_['items']
            file_items_id_list = [item['id'] for item in items]
        index = file_items_id_list.index(item_id)
        return {
            'file': file_,
            'index': index
        }

    async def get(self, item_id: str):
        position = await self.get(item_id)
        if position.index != -1:
            return position['file']['items'][position['index']]
        return None

    async def post(self, item_in: RSS3ItemInput):
        file_ = await self.rss3.file.get(self.rss3.persona.id)
        if 'items' not in file_:
            file_['items'] = []

        id_ = 0

        if file_['items']:
            id_ = utils.parse(file_['items'][0]['id'])['index'] + 1

        now_date = utils.iso_format_string()
        item = RSS3Item.from_instance(item_in)
        item.authors = [self.rss3.persona.id]
        item.id = f'{self.rss3.persona.id}-item-{id_}'
        item.date_published = now_date
        item.date_modified = now_date
        item.signature = utils.sign(IRSS3ItemSchema.dump(item), self.rss3.persona.private_key)
        json_item = IRSS3ItemSchema.dump(item)
        file_['items'].insert(0, json_item)

        if len(file_['items']) > ITEM_PAGE_SIZE:
            new_list = file_['items'][1:]
            id_suffix = utils.parse(file_['items_next'])['index'] + 1 if file_['items_next'] else 0
            new_id = f'{self.rss3.persona.id}-items-{id_suffix}'
            new_file = self.rss3.file.new(new_id)
            new_file['items'] = new_list
            new_file['items_next'] = file_['items_next']

            file_['items'] = file_['items'][:1]
            file_['items_next'] = new_id
        self.rss3.file.set(file_)
        return item

    async def patch(self, item_in: RSS3ItemInput):
        position = await self.get_position(item_in.id)
        if position['index'] != -1:
            new_date = utils.iso_format_string()
            item = RSS3Item.from_instance(item_in)
            item.date_modified = new_date
            item.signature = utils.sign(IRSS3ItemSchema.dump(item), self.rss3.persona.private_key)
            position['file']['items'][position['index']] = IRSS3ItemSchema.dump(item)
            self.rss3.file.set(position['file'])
            return position['file']['items'][position['index']]
