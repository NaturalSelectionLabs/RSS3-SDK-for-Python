#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   account.py    
@Contact :   leetao94cn@gmail.com
@Description：
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/6/24 9:27 下午   leetao      1.0         None
"""

# import lib
from typing import Dict, Union, List
from web3.auto import w3
from eth_account.messages import encode_defunct
from eth_account.account import LocalAccount
import json


def private_key_to_address(private_key: str) -> str:
    return w3.eth.account.from_key(private_key).address


def sign(rss3: Dict, private_key: str) -> str:
    assert all([rss3, private_key]) is True
    rss3 = stringify(rss3)
    message = encode_defunct(text=rss3)
    signed_message = w3.eth.account.sign_message(message, private_key)
    return signed_message.signature.hex()


def create() -> LocalAccount:
    return w3.eth.account.create()


def check(obj: Union[Dict, List], persona: str) -> bool:
    if 'signature' not in obj:
        return False
    message = encode_defunct(text=stringify(obj))
    signature = w3.eth.account.recover_message(message, signature=obj.get('signature'))
    return signature == persona


def remove_not_sign_properties(obj, remove_keys) -> list:
    if isinstance(obj, dict):
        obj = {
            key: remove_not_sign_properties(value, remove_keys)
            for key, value in obj.items()
            if key and key not in remove_keys and not key.startswith('@') and value}
    elif isinstance(obj, list):
        obj = [remove_not_sign_properties(item, remove_keys) for item in obj if item]
    return obj


def convert_obj_2_array(obj: Union[Dict, List]):
    if isinstance(obj, Dict):
        return [[k, v] for k, v in sorted({
                                              key: convert_obj_2_array(value)
                                              for key, value in obj.items()
                                          }.items(), key=lambda d: d[0])]
    elif isinstance(obj, List):
        return [[str(index), convert_obj_2_array(value)] for index, value in enumerate(obj)]
    return obj


def stringify(obj: Union[Dict, List]) -> str:
    remove_not_sign_rss3 = convert_obj_2_array(remove_not_sign_properties(obj, {'signature', '', None}))
    stringify_rss3 = json.dumps(remove_not_sign_rss3, separators=(',', ':'), ensure_ascii=False)
    return stringify_rss3
