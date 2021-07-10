#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   test_utils.py    
@Contact :   leetao@email.cn
@Description：
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/7/4 11:08 下午   leetao      1.0         None
"""

# import lib
import pytest
from rss3.src import utils
import hashlib
import os


def md5(encode_str: str) -> str:
    m = hashlib.md5()
    m.update(encode_str)
    return m.hexdigest()


@pytest.fixture()
def rss3_item_without_sign():
    return {
        "authors": [
            "0xb4B4ca72fa7c24a53f169468c1938966f8ACEbdb"
        ],
        "title": "Hello RSS3",
        "summary": "RSS3 is an open protocol designed for content and social networks in the Web 3.0 era.",
        "date_published": "2021-07-10T09:23:53.846Z",
        "id": "0xb4B4ca72fa7c24a53f169468c1938966f8ACEbdb-item-2",
        "date_modified": "2021-07-10T09:23:53.846Z",
    }


@pytest.fixture()
def rss3_item_sign():
    return "0x8ae27e847bee4df849dd9ba17fbe940953c8d6faa1b67467ebc958af93e59b5b5df0d9bd6eb4b0d6a6e06babac2f63dd6ce5b42aa403ef287a6062de2124c45b1b"


@pytest.fixture()
def private_key():
    return os.getenv("private_key")


@pytest.fixture()
def persona():
    return '0xb4B4ca72fa7c24a53f169468c1938966f8ACEbdb'


@pytest.fixture()
def rss3_content():
    return {'id': '0xb4B4ca72fa7c24a53f169468c1938966f8ACEbdb', '@version': 'rss3.io/version/v0.1.0',
            'date_created': '2021-07-10T12:34:55.564Z', 'date_updated': '2021-07-10T12:34:55.587Z',
            'signature': '0x1159c855664795f2b92371dec5a03db1c0405de6116b53a67e19a712dce07c60280cbebc922febdb219787c66ac5dab2e628191b5f54c3067e3f2c12b5c1ee151b',
            'profile': {'name': 'Leetao', 'avatar': ['http://q1.qlogo.cn/g?b=qq&nk=501257367&s=5'],
                        'bio': 'Talk is cheap,show me the code!', 'tags': ['python', 'ts', 'flutter', 'go', 'java'],
                        'signature': '0xea92e64bcd69345c809a964619c5a3dad22d26b2af104838569565e84b337a29635b4039fcdbac81bb4a306764ff30162f56464119a7332f5336e68d550063681c'}}


def test_sign(rss3_item_without_sign, rss3_item_sign, private_key):
    sign = utils.sign(rss3_item_without_sign, private_key)
    assert rss3_item_sign == sign


def test_check(rss3_content, persona):
    assert utils.check(rss3_content, persona) is True
