#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   index.py    
@Contact :   leetao94cn@gmail.com
@Description：
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/6/24 9:11 下午   leetao      1.0         None
"""

# import lib
from dataclasses import field
from marshmallow_dataclass import dataclass

from .item import Item
from .items import Items
from .link import Link
from .links import Links
from .persona import Persona
from .file import File as File_
from .profile import Profile


@dataclass
class IOptions:
    endpoint: str
    private_key: str = field(default_factory=str)


class RSS3:
    options: IOptions
    persona: Persona
    file: File_
    profile: Profile
    items: Items
    items: Item
    links: Links
    link: Link

    def __init__(self, options: IOptions):
        self.options = options
        self.file = File_(self)
        self.persona = Persona(self)
        self.profile = Profile(self)
        self.items = Items(self)
        self.item = Item(self)
        self.links = Links(self)
        self.link = Link(self)


