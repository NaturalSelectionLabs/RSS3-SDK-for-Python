#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   test_others.py    
@Contact :   leetao@email.cn
@Description：
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/7/3 7:12 下午   leetao      1.0         None
"""

# import lib
from marshmallow import ValidationError
import pytest
from pathlib import Path
import json

import rss3 as r3


def generate_n_content(n: int):
    return [{"type": str(i), "list": str(i)} for i in range(n)]


def test_rss3_item_with_max_len():
    def overflow_max_len():
        with pytest.raises(ValidationError):
            contexts = generate_n_content(101)
            r3.IRSS3ItemSchema.load({"@contexts": contexts})

    def under_max_len():
        contexts = generate_n_content(1)
        r3.IRSS3ItemSchema.load({"@contexts": contexts})

    overflow_max_len()
    under_max_len()


@pytest.fixture()
def rss3_index():
    root_path = Path.cwd()
    print(f'root path:{root_path}')
    file_path = root_path.joinpath('rss3_index.json')
    assert file_path.exists() is True
    with open(file_path, encoding='utf-8') as f:
        rss3_index_json = json.load(f)
    return rss3_index_json


def test_schema_load(rss3_index):
    r3.IRSS3IndexSchema.load(rss3_index)


def test_rss3_item():
    contexts = generate_n_content(1)
    r3.IRSS3ItemSchema.load({"@contexts": contexts})