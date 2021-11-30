#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   profile.py    
@Contact :   leetao94cn@gmail.com
@Description：
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/7/3 4:01 下午   leetao      1.0         None
"""

# import lib
from ..interface import RSS3ProfileInput, RSS3Profile, IRSS3ProfileSchema
from .. import utils
from typing import Dict, TYPE_CHECKING


if TYPE_CHECKING:
    from .index import RSS3


class Profile:
    rss3: 'RSS3'

    def __init__(self, rss3: 'RSS3'):
        self.rss3 = rss3

    async def get(self, persona_id: str = None) -> Dict:
        if persona_id is None:
            persona_id = self.rss3.persona.id
        file_ = await self.rss3.file.get(persona_id)
        return file_.get("profile", None)

    async def patch(self, profile_in: RSS3ProfileInput) -> Dict:
        assert profile_in is not None
        file_ = await self.rss3.file.get(self.rss3.persona.id)
        profile_instance = RSS3Profile.from_instance(profile_in)
        profile = IRSS3ProfileSchema.dump(profile_instance)
        profile['signature'] = utils.sign(profile, self.rss3.persona.private_key)
        file_['profile'] = profile
        self.rss3.file.set(file_)
        return file_['profile']
