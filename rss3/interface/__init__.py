#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   __init__.py    
@Contact :   leetao94cn@gmail.com
@Description：
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/6/21 9:37 下午   leetao      1.0         None
"""

# import lib

from rss3.interface.rss3 import *
import marshmallow_dataclass

IRSS3ContentSchema = marshmallow_dataclass.class_schema(RSSContent)()
IRSS3ContextSchema = marshmallow_dataclass.class_schema(RSS3Context)()
IRSS3ProfileSchema = marshmallow_dataclass.class_schema(RSS3Profile)()
IRSS3LinkSchema = marshmallow_dataclass.class_schema(RSS3Link)()
IRSS3BackLink = marshmallow_dataclass.dataclass(RSS3BackLink)()
IRSS3AssetSchema =  marshmallow_dataclass.class_schema(RSS3Asset)()
IRSS3IndexSchema = marshmallow_dataclass.class_schema(RSS3Index)()
IRSS3ItemSchema = marshmallow_dataclass.class_schema(RSS3Item)()
IRSS3ItemsSchema = marshmallow_dataclass.class_schema(RSS3Items)()
IRSS3ListSchema = marshmallow_dataclass.class_schema(RSS3List)()






