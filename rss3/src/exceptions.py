#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   exceptions.py    
@Contact :   leetao94cn@gmail.com
@Description：
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/6/26 4:43 下午   leetao      1.0         None
"""


# import lib
class Error(Exception):
    pass


class SignatureNotMatchError(Error):
    pass


class ContentFormatError(Error):
    pass


class ParamError(Error):
    pass


class SyncError(Error):
    pass
