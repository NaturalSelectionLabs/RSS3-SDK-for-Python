import copy
import json

from rss3 import config
from rss3.utils import object as utils_object


def file_size(obj):
    to_be_obj = copy.deepcopy(obj)
    utils_object.remove_empty(to_be_obj)
    to_be_obj["signature"] = "0" * 132
    b = json.dumps(to_be_obj).encode("utf8")
    return len(b) <= config.file_size_limit
