#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   id.py    
@Contact :   leetao94cn@gmail.com
@Description：
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/6/26 3:25 下午   leetao      1.0         None
"""


# import lib

def parse(id: str):
    spliced = id.split('-')
    type_ = 'index'
    index_ = float('inf')
    if len(spliced) >= 2:
        type_ = spliced[1]
    if len(spliced) >= 3:
        index_ = int(spliced[2])

    return {
        'persona': spliced[0],
        'type': type_,
        'index': index_
    }
