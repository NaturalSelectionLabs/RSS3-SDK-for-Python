import math


def parse(id_: str):
    parts = id_.split("-")
    if len(parts) <= 3:
        return {
            "persona": parts[0],
            "type": parts[1] if parts[1:] else "index",
            "index": int(parts[2]) if parts[2:] else math.inf,
        }
    else:
        return {
            "persona": parts[0],
            "type": parts[1],
            "payload": parts[2].split("."),
            "index": int(parts[3]),
        }


def get(persona, type_, index, payload=None):
    payload_str = ""
    if isinstance(payload, list):
        payload_str = "-" + ".".join(payload)
    return f"{persona}-{type_}{payload_str}-{index}"


def get_custom_item(persona, index):
    return get(persona, "item", index, ["custom"])


def get_auto_item(persona, index):
    return get(persona, "item", index, ["auto"])


def get_custom_items(persona, index):
    return get(persona, "list", index, ["items", "custom"])


def get_auto_items(persona, index):
    return get(persona, "list", index, ["items", "auto"])


def get_links(persona, type_, index):
    return get(persona, "list", index, ["links", type_])


def get_backlinks(persona, type_, index):
    return get(persona, "list", index, ["backlinks", type_])


def get_custom_assets(persona, index):
    return get(persona, "list", index, ["assets", "custom"])


def get_auto_assets(persona, index):
    return get(persona, "list", index, ["assets", "auto"])


def get_item_backlinks(persona, type_, index, item_index):
    return get(persona, "list", index, ["item", str(item_index), "backlinks", type_])


def get_account(platform, identity):
    return f"{platform}-{identity}"


def get_asset(platform, identity, type_, unique_id):
    return f"{platform}-{identity}-{type_}-{unique_id}"


def parse_account(id_):
    parts = id_.split("-")
    return {
        "platform": parts[0],
        "identity": parts[1],
    }


def parse_asset(id_):
    parts = id_.split("-")
    return {
        "platform": parts[0],
        "identity": parts[1],
        "type": parts[2],
        "unique_id": parts[3],
    }
