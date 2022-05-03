import copy
import json

from rss3 import config
from rss3.utils import object as utils_object


def value_length(obj):
    if isinstance(obj, str):
        return len(obj) <= config.max_value_length

    result = True
    if isinstance(obj, dict):
        keys = list(obj.keys())
    else:
        keys = list(range(len(obj)))

    for key in keys:
        if isinstance(obj[key], dict) and not value_length(obj[key]):
            result = False
            break
        elif isinstance(obj[key], str) and len(obj[key]) > config.max_value_length:
            result = False
            break
    return result


def file_size(obj):
    to_be_obj = copy.deepcopy(obj)
    utils_object.remove_empty(to_be_obj)
    to_be_obj["signature"] = "0" * 132
    b = json.dumps(to_be_obj, separators=(",", ":")).encode("utf8")
    return len(b) <= config.file_size_limit


def file_size_with_new(obj, new_item):
    to_be_obj = copy.deepcopy(obj)
    to_be_obj["list"].insert(0, new_item)
    return file_size(to_be_obj)
