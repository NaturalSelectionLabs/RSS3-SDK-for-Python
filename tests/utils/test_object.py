from rss3.utils import object as utils_object


def test_remove_empty():
    obj = {
        "a": [1],
        "b": [],
        "c": [""],
        "d": [None],
        "e": [[]],
        "f": 1,
        "g": {
            "h": 1,
            "i": "",
        },
        "j": {},
    }
    utils_object.remove_empty(obj)
    assert obj == {
        "a": [1],
        "f": 1,
        "g": {
            "h": 1,
        },
    }

    # fixme: IndexError: list index out of range
    obj2 = {
        "a": [1],
        "b": [],
        "c": [""],
        "d": [0, 1, None, ""],
        "e": [[0, 1, None, ""], {}],
    }
    utils_object.remove_empty(obj2)


def test_remove_custom_properties():
    obj = {"test1": "r", "test2": {"_test3": "r"}, "_test4": "r"}
    assert utils_object.remove_custom_properties(obj) == {"test1": "r", "test2": {}}
