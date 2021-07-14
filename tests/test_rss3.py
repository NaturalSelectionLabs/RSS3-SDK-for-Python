#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   test_items.py    
@Contact :   leetao94cn@gmail.com
@Description：
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/6/26 8:19 下午   leetao      1.0         None
"""
import pytest
import datetime
import os

from rss3 import RSS3ProfileInput, RSS3ItemInput, RSS3, IOptions


@pytest.fixture()
def rss3():
    try:
        options = IOptions(endpoint='https://hub.rss3.io',
                           private_key=os.getenv('private_key',
                                                 '0x47e18d6c386898b424025cd9db446f779ef24ad33a26c499c87bb3d9372540ba'))
        rss3 = RSS3(options=options)
        return rss3
    except Exception as e:
        assert False, f"'rss3' raised an exception {e}"


@pytest.mark.dependency()
@pytest.mark.asyncio
async def test_get_profile(rss3):
    try:
        await rss3.profile.get()
    except Exception as e:
        assert False, f"'get_profile' raised an exception {e}"


@pytest.mark.dependency(depends=['test_get_profile'])
@pytest.mark.asyncio
async def test_profile_patch(rss3):
    profile_for_test = RSS3ProfileInput(name='RSS3 Python SDK',
                                        avatar=['http://q1.qlogo.cn/g?b=qq&nk=501257367&s=5'],
                                        bio=f'A test by python sdk at {datetime.datetime.utcnow().isoformat()}',
                                        tags=['Python', 'TypeScript', 'Flutter', 'Go', 'Java'])
    try:
        await rss3.profile.patch(profile_for_test)
    except Exception as e:
        assert False, f"'test_profile_patch' raised an exception {e}"


@pytest.mark.asyncio
@pytest.fixture()
async def test_get_items(rss3):
    try:
        items = await rss3.items.get(rss3.persona.id)
        return items
    except Exception as e:
        assert False, f"'test_items_get' raised an exception {e}"


@pytest.mark.skip(reason='not need')
@pytest.mark.asyncio
async def test_item_post(rss3):
    item_input = RSS3ItemInput(title='Test message',
                               summary='Test message by Python SDK version 0.1.0 created by Leetao')
    try:
        item = await rss3.item.post(item_input)
        assert item is not None
    except Exception as e:
        assert False, f"'test_item_post' raised an exception {e}"


@pytest.mark.dependency()
@pytest.mark.asynico
def test_if_can_item_patch(test_get_items):
    try:
        items = test_get_items
        assert len(items['items']) > 0
    except Exception as e:
        assert False, f"'test_if_can_item_patch' raised an exception {e}"


@pytest.mark.dependency(depends=['test_if_can_item_patch'])
@pytest.mark.asyncio
async def test_item_patch(rss3):
    item_input = RSS3ItemInput(id='0xb4B4ca72fa7c24a53f169468c1938966f8ACEbdb-item-1',
                               title='Item patch test',
                               summary=f'Item patch test again by version 0.1.0 at {datetime.datetime.utcnow().isoformat()}')
    try:
        item = await rss3.item.patch(item_input)
        assert item is not None
    except Exception as e:
        assert False, f"'test_item_patch' raised an exception {e}"


@pytest.mark.asyncio
async def test_persona_sync(rss3):
    try:
        await rss3.persona.sync()
    except Exception as e:
        assert False, f"'test_persona_sync' raised an exception {e}"
