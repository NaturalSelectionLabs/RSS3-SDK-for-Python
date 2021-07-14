#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   file.py    
@Contact :   leetao94cn@gmail.com
@Description：
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/6/26 3:36 下午   leetao      1.0         None
"""

# import lib
from typing import Union, Dict, TYPE_CHECKING
import aiohttp
from marshmallow import ValidationError

from .exceptions import SignatureNotMatchError, ContentFormatError, SyncError
from ..settings import VERSION
from .. import utils
from ..interface import RSS3Items, RSS3Index, IRSS3IndexSchema

if TYPE_CHECKING:
    from .index import RSS3


class File:
    rss3: 'RSS3'
    # 属性名称有歧义
    list_: Dict = {}
    dirty_list: Dict = {}

    def __init__(self, rss3: 'RSS3'):
        self.rss3 = rss3

    def new(self, file_id: str):
        now_date = utils.iso_format_string()
        self.set({
            'id': file_id,
            '@version': VERSION,
            'date_created': now_date,
            'date_updated': now_date,
            'signature': ''
        })
        return self.list_[file_id]

    def set(self, content: Union[RSS3Index, RSS3Items, Dict]):
        content['date_updated'] = utils.iso_format_string()
        self.list_[content['id']] = content
        self.dirty_list[content['id']] = 1

    async def get(self, file_id: str) -> Dict:
        if file_id in self.list_:
            return self.list_[file_id]

        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.rss3.options.endpoint}/{file_id}') as response:
                content = await response.json()
                if response.status != 200:
                    if 'code' in content and content['code'] == 5001:
                        now_date = utils.iso_format_string()
                        self.list_[file_id] = {
                            'id': file_id,
                            '@version': VERSION,
                            'date_created': now_date,
                            'date_updated': now_date,
                            'signature': ''
                        }
                        return self.list_[file_id]
                    else:
                        raise Exception("Server response error.")
                try:
                    # load successfully or not
                    IRSS3IndexSchema.load(content)
                except ValidationError as e:
                    raise ContentFormatError(f"content {file_id} is not rss3index or rss3items object")
                else:
                    check_flag = utils.check(content, utils.parse(file_id)['persona'])
                    if check_flag:
                        self.list_[file_id] = content
                        return self.list_[file_id]
                    raise SignatureNotMatchError()

    async def sync(self) -> None:
        file_id_list = list(self.dirty_list.keys())
        contents = []
        for file_id in file_id_list:
            self.list_[file_id]['signature'] = utils.sign(self.list_[file_id], self.rss3.persona.private_key)
            contents.append(self.list_[file_id])
        async with aiohttp.ClientSession() as session:
            async with session.put(self.rss3.options.endpoint, json={"contents": contents}) as response:
                response_json = await response.json()
                if response.status != 200:
                    raise SyncError(f'code:{response_json["code"]} message:{response_json["message"]}')
                for file_id in file_id_list:
                    del self.dirty_list[file_id]
