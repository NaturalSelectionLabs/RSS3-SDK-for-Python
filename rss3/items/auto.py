from rss3.items.backlinks import Backlinks
from rss3.utils import id as utils_id


class AutoItems:
    def __init__(self, main):
        self._main = main
        self.backlinks = Backlinks(main, "auto")

    async def get_list_file(self, persona, index=-1):
        return await self._main.files.get_list(persona, "items", index, "list_auto")

    async def get_list(self, persona, breakpoint=None):
        index_file = await self._main.files.get(persona)
        list_file = index_file.get("items", {}).get("list_auto", utils_id.get_auto_items(persona, 0))

        def bk(f):
            if breakpoint is None:
                return False
            return breakpoint(f)

        return await self._main.files.get_all(list_file, bk)

    async def _get_position(self, item_id):
        result = {"file": None, "index": -1}

        def _bk(file):
            nonlocal result
            if not file.get("list"):
                return False

            index = -1
            for i, item in enumerate(file["list"]):
                if item["id"] == item_id:
                    index = i
                    break

            if index != -1:
                result = {"file": file, "index": index}
                return True
            else:
                return False

        await self.get_list(self._main.account.address, _bk)
        return result

    async def get(self, item_id):
        position = await self._get_position(item_id)
        if position["index"] != -1:
            return position["file"]["list"][position["index"]]
        return None
