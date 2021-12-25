class Backlinks:
    def __init__(self, main):
        self._main = main

    async def _get_position(self, persona, id_):
        file = await self._main.files.get(persona)
        backlinks = file.get("backlinks", [])
        index = -1
        for i, lks in enumerate(backlinks):
            if lks["id"] == id_:
                index = i
                break

        return {
            "file": file,
            "index": index,
            "file_id": file["backlinks"][index].get("list") if index != -1 else None,
        }

    async def get_list_file(self, persona, id_, index=-1):
        return await self._main.files.get_list(persona, "backlinks", index, id_)

    async def get_list(self, persona, id_, breakpoint=None):
        position = await self._get_position(persona, id_)
        file_id = position["file_id"]
        if file_id:

            def _bp(file):
                if breakpoint:
                    return breakpoint(file)
                else:
                    return False

            return await self._main.files.get_all(file_id, _bp)
        else:
            return []
