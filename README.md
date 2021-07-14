# RSS3

A python version of the reference [RSS3 JavaScript SDK](https://github.com/NaturalSelectionLabs/RSS3-SDK-for-JavaScript), which means  the usage should be pretty similar between both.

## Installation and usage

### Installation

**note**: There are two versions(0.1.0 and 0.1.1) that correspond to the rss3 version one by one. 

If it raises SignatureNotMatchError,you'd better switch to the other version.

```
pip install rss3==[version]
```

or 

```
pip install rss3
```

### Usage

To get started right away with defaults:

```
>>> from rss3 import RSS3, IOptions
>>> options = IOptions(endpoint='https://hub.rss3.io',private_key='your key')
>>> r3 = RSS3(options=options)
>>> import asyncio
# Python 3.7+
>>> asyncio.run(r3.profile.get())
>>> {'tags': ['Python', 'TypeScript', 'Flutter', 'Go', 'Java'], 
    'name': 'Leetao', 
    'bio': 'Talk is cheap,show me the code', 
    'avatar': ['http://q1.qlogo.cn/g?b=qq&nk=501257367&s=5'], 
    'signature': '...'}
```

Other Api can be found in [RSS3-SDK-for-JavaScript](https://github.com/NaturalSelectionLabs/RSS3-SDK-for-JavaScript)