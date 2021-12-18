from rss3.utils import object as utils_object


def test_remove_custom_properties():
    obj = {"test1": "r", "test2": {"_test3": "r"}, "_test4": "r"}
    assert utils_object.remove_custom_properties(obj) == {"test1": "r", "test2": {}}
