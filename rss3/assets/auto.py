from rss3.utils import id as utils_id


class AutoAssets:
    def __init__(self, main):
        self._main = main

    async def get_list_file(self, persona, index=-1):
        return await self._main.files.get_list(persona, "assets", index, "list_auto")

    async def get_list(self, persona, breakpoint=None):
        index_file = await self._main.files.get(persona)
        list_file = index_file.get("assets", {}).get("list_auto", utils_id.get_auto_assets(persona, 0))

        def bk(f):
            if breakpoint is None:
                return False
            return breakpoint(f)

        return await self._main.files.get_all(list_file, bk)
