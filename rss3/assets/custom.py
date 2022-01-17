from rss3.utils import check as utils_check
from rss3.utils import id as utils_id


class CustomAssets:
    def __init__(self, main):
        self._main = main

    async def get_list_file(self, persona, index=-1):
        return await self._main.files.get_list(persona, "assets", index, "list_custom")

    async def get_list(self, persona, breakpoint=None):
        index_file = await self._main.files.get(persona)
        if index_file.get("assets", {}).get("list_custom"):

            def _bp(file):
                if breakpoint:
                    return breakpoint(file)
                else:
                    return False

            return await self._main.files.get_all(index_file["assets"]["list_custom"], _bp)

    async def _get_position(self, asset):
        result = {"file": None, "index": -1}

        def _bp(file):
            nonlocal result
            if not file.get("list"):
                return False

            index = -1
            for i, ass in enumerate(file["list"]):
                if ass == asset:
                    index = i
                    break

            if index != -1:
                result = {"file": file, "index": index}
                return True
            else:
                return False

        await self.get_list(self._main.account.address, _bp)
        return result

    async def post(self, asset):
        # todo: verify asset shape
        if utils_check.value_length(asset):

            def _bk(f):
                return f.get("list") and (asset in f["list"])

            list_ = await self.get_list(self._main.account.address, _bk)
            try:
                index = list_.index(asset)
            except ValueError:
                index = -1

            if index == -1:
                file = await self.get_list_file(self._main.account.address, -1)
                if not file:
                    new_id = utils_id.get_custom_assets(self._main.account.address, 0)
                    file = self._main.files.new(new_id)
                    index_file = await self._main.files.get(self._main.account.address)
                    if index_file.get("assets", None) is None:
                        index_file.assets = {}
                    index_file["assets"]["list_custom"] = new_id

                if file.get("list", None) is None:
                    file["list"] = []

                if not utils_check.file_size_with_new(file, asset):
                    new_id = utils_id.get_custom_assets(
                        self._main.account.address, utils_id.parse(file["id"])["index"] + 1
                    )
                    new_file = self._main.files.new(new_id)
                    new_file["list"] = [asset]
                    new_file["list_next"] = file["id"]
                    self._main.files.set(new_file)

                    index_file = await self._main.files.get(self._main.account.address)
                    if index_file.get("assets", None) is None:
                        index_file["assets"] = {}
                    index_file["assets"]["list_custom"] = new_id
                    self._main.files.set(index_file)
                else:
                    del file["list"]
                    self._main.files.set(file)

                return asset
            else:
                raise Exception("Asset already exists")
        else:
            raise Exception("Parameter error")

    async def delete(self, asset):
        position = await self._get_position(asset)
        index = position["index"]
        file = position["file"]
        if index != -1:
            del file["list"][index]
            result = file["list"]
            self._main.files.set(file)
            return result
        else:
            raise Exception("Asset not found")
