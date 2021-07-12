#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   test_items.py    
@Contact :   leetao@email.cn
@Description：
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/6/26 8:19 下午   leetao      1.0         None
"""
import pytest

import rss3.src.index as index_
from rss3 import RSS3ProfileInput, RSS3ItemInput
import os


@pytest.fixture()
def rss3():
    options = index_.IOptions(endpoint='https://hub.rss3.io',
                              private_key=os.getenv("private_key"))
    rss3 = index_.RSS3(options=options)
    return rss3


@pytest.mark.asyncio
async def test_profile(rss3):
    profile = await rss3.profile.get()
    print(f'profile:{profile}')
    return profile


@pytest.mark.skipif(reason='not need')
@pytest.mark.asyncio
async def test_profile_patch(rss3):
    profile_for_test = RSS3ProfileInput(name='Leetao',
                                        avatar=['http://q1.qlogo.cn/g?b=qq&nk=501257367&s=5'],
                                        bio='Talk is cheap,show me the code',
                                        tags=['Python', 'TypeScript', 'Flutter', 'Go', 'Java'])
    new_profile = await rss3.profile.patch(profile_for_test)
    assert new_profile is not None


# @pytest.mark.skipif(reason='not need')
@pytest.mark.asyncio
async def test_items_get(rss3):
    items = await rss3.items.get(rss3.persona.id)
    assert len(items) > 0


@pytest.mark.skipif(reason='not need')
@pytest.mark.asyncio
async def test_item_post(rss3):
    item_input = RSS3ItemInput(title='Hello Everyone', summary='This is a test message from Leetao ')
    item = await rss3.item.post(item_input)
    assert item is not None


@pytest.mark.asyncio
async def test_item_patch(rss3):
    item_input = RSS3ItemInput(id='0xb4B4ca72fa7c24a53f169468c1938966f8ACEbdb-item-1', title='Item patch test',
                               summary='@rss3_  all by Third-party sdk')
    item = await rss3.item.patch(item_input)
    assert item is not None


@pytest.mark.asyncio
async def test_persona_sync(rss3):
    await rss3.persona.sync()
