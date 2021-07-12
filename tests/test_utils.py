#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   test_utils.py    
@Contact :   leetao94cn@gmail.com
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
            'date_created': '2021-07-10T12:34:55.564Z', 'date_updated': '2021-07-10T14:22:05.989Z',
            'signature': '0x965cbe5fb5ef1295c21a666ac993f112c4ca1ac1e637b5d34f04e9b8cff1cb267c58a4be0d9d79da8324a14c0c315b88c2bde97ee503b69a3082b83214508a2d1b',
            'profile': {'avatar': ['http://q1.qlogo.cn/g?b=qq&nk=501257367&s=5'], 'name': 'Leetao',
                        'tags': ['Python', 'TypeScript', 'Flutter', 'Go', 'Java'],
                        'bio': 'Talk is cheap,show me the code',
                        'signature': '0x442e7caacdb5ddcf3dec01d3ac37d40fe830909d9b8b97539b7668b6b862cbdb7e228d7d8cb20db12107b934a6b71b5334c9870ebb9dd331c510f156e2d2a1f21c'},
            'items': [{'authors': ['0xb4B4ca72fa7c24a53f169468c1938966f8ACEbdb'],
                       'summary': '@rss3_  all by Third-party sdk😍', 'tags': ['Re: ID', 'Twitter'], 'contents': [
                    {'address': ['https://gateway.pinata.cloud/ipfs/QmRimTYATExzVhRHnMbWotW3EDRFor25dbboEXMQvs3UXW'],
                     'mime_type': 'image/png', 'size_in_bytes': '415703'}],
                       'id': '0xb4B4ca72fa7c24a53f169468c1938966f8ACEbdb-item-1',
                       'date_published': '2021-07-10T14:22:05.981Z', 'date_modified': '2021-07-10T14:22:05.981Z',
                       'signature': '0x7ed8efb2ca1282df766ca7565cb6a0646fe85cb83f6f0d0ad326774cf7353ca96ffbbccbd54ccd461609605ed181e2db10c8441d97df9e610bf3a69747294d5e1b'},
                      {'authors': ['0xb4B4ca72fa7c24a53f169468c1938966f8ACEbdb'],
                       'id': '0xb4B4ca72fa7c24a53f169468c1938966f8ACEbdb-item-0', 'title': 'Hello RSS3',
                       'summary': 'This is a message from Leetao', 'date_published': '2021-07-10T13:55:00.754079',
                       'date_modified': '2021-07-10T13:55:00.754079',
                       'signature': '0xabac000da14e2043707065a6300bd032631311e6183665ece2f39d3bebe98e5d775fa33166a1c711d6b1e5c272a841e207346303bf991af7c2e061365ac4d9d41c'}]}


def test_sign(rss3_item_without_sign, rss3_item_sign, private_key):
    sign = utils.sign(rss3_item_without_sign, private_key)
    assert rss3_item_sign == sign


def test_check(rss3_content, persona):
    assert utils.check(rss3_content, persona) is True
