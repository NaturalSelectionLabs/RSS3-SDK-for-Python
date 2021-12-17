import copy
import json


def remove_empty(obj):
    ...


def stringify_obj(obj):
    message = _obj_to_array(_remove_not_sign_properties(obj))
    return json.dumps(message)


def _remove_not_sign_properties(obj):
    # obj = json.loads(json.dumps(obj))  # do a deep copy for obj
    obj = copy.deepcopy(obj)
    for key in list(obj.keys()):
        if key in {"signature", "agent_signature"}:
            del obj[key]
        elif isinstance(obj[key], dict):
            if obj[key].get("auto"):
                del obj[key]
            else:
                obj[key] = _remove_not_sign_properties(obj[key])
    return obj


def _obj_to_array(obj):
    key_list = list(obj.keys())
    sorted_keys = sorted(key_list)
    result = []
    for key in sorted_keys:
        if isinstance(obj[key], dict):
            result.append([key, _obj_to_array(obj[key])])
        else:
            result.append([key, obj[key]])
    return result
