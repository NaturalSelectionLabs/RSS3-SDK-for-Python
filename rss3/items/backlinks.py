from rss3.utils import id as utils_id


class Backlinks:
    def __init__(self, main, type_):
        self._main = main
        self._type = type_

    async def _get_item(self, item_id):
        return await self._main.items[self._type].get(item_id)

    async def _get_position(self, item_id, id_):
        item = await self._get_item(item_id)
        backlinks = item.get("backlinks", [])
        index = -1
        for i, lks in enumerate(backlinks):
            if lks["id"] == id_:
                index = i
                break

        return {
            "item": item,
            "index": index,
            "id": backlinks[index].get("list") if index != -1 else None,
        }

    async def get_list_file(self, item_id, id_, index=-1):
        if index < 0:
            item = await self._get_item(item_id)
            if item.get("backlinks"):
                backlinks = item["backlinks"]
                file_id = None
                for lk in backlinks:
                    if lk["id"] == id_:
                        file_id = lk.get("list")
                        break
                if not file_id:
                    id_desp = f"id {id_}" if id_ else ""
                    raise Exception(f"items {item_id} backlinks {id_desp}does not exist")
                parsed = utils_id.parse(file_id)
                return await self._main.files.get(
                    utils_id.get(parsed["persona"], parsed["type"], parsed["index"] + index + 1, parsed["payload"])
                )
            else:
                return None
        else:
            parsed = utils_id.parse(item_id)
            return await self._main.files.get(
                utils_id.get(parsed["persona"], "list", index, ["item", str(parsed["index"]), "backlinks", id_])
            )

    async def get_list(self, item_id, type_, breakpoint=None):
        position = await self._get_position(item_id, type_)
        id_ = position["id"]
        if id_:

            def _bp(file):
                if breakpoint:
                    return breakpoint(file)
                else:
                    return False

            return await self._main.files.get_all(id_, _bp)
        else:
            return []
