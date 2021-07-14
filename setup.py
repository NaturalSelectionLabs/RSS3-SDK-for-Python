#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   setup.py    
@Contact :   leetao94cn@gmail.com
@Description：
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/7/13 9:25 下午   leetao      1.0         None
"""

# import lib
from setuptools import setup

VERSION = '0.1.0'

setup(
    name="rss3",
    version=VERSION,
    description="Python library for RSS3",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LeetaoGoooo/RSS3-SDK-for-Python",
    keywords=["rss3", "rss"],
    author="LeeTao",
    author_email="leetao94cn@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["rss3", "rss3.src", "rss3.interface", "rss3.utils"],
    include_package_data=True,
    install_requires=["aiohttp>=3.7.4", "marshmallow-dataclass>=8.4.1", "web3>=5.20.0"]
)
