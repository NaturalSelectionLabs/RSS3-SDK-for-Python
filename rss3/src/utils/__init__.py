#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   __init__.py.py    
@Contact :   leetao94cn@gmail.com
@Description：
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/6/24 9:27 下午   leetao      1.0         None
"""

# import lib
from .account import *
from .id import *

import datetime


def iso_format_string():
    return datetime.datetime.utcnow().isoformat()
