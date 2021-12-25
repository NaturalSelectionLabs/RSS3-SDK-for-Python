import json

from rss3 import config
from rss3.utils import check as utils_check


def test_value_length():
    assert utils_check.value_length(
        {"test1": "r", "test2": "r" * config.max_value_length}
    )
    assert not utils_check.value_length(
        {"test1": "r", "test2": "r" * (config.max_value_length + 1)}
    )


def test_file_size():
    test_obj = {"t": "r", "signature": "0" * 132}
    b = json.dumps(test_obj).encode("utf8")
    test_obj_length = len(b)

    test_obj["t"] = "r" * (config.file_size_limit - test_obj_length + 1)
    assert utils_check.file_size(test_obj)

    test_obj["t"] = "r" * (config.file_size_limit - test_obj_length + 2)
    assert not utils_check.file_size(test_obj)
