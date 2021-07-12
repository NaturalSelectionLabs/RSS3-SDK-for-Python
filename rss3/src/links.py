#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   links.py    
@Contact :   leetao94cn@gmail.com
@Description：
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/7/3 4:00 下午   leetao      1.0         None
"""

# import lib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .index import RSS3


class Links:
    rss3: 'RSS3'

    def __init__(self, rss3: 'RSS3'):
        self.rss3 = rss3
