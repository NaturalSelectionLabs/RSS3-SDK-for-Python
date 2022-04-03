import copy
from datetime import datetime
from typing import Optional

from pydantic import ValidationError

from rss3.items.backlinks import Backlinks
from rss3.models import RSS3CustomItem, RSS3CustomItemID
from rss3.utils import check as utils_check
from rss3.utils import id as utils_id


class ItemPost(RSS3CustomItem):
    date_created: Optional[str]
    date_updated: Optional[str]
    id: Optional[RSS3CustomItemID]

    class Config:
        fields = {
            "date_created": {"exclude": True},
            "date_updated": {"exclude": True},
            "id": {"exclude": True},
        }


class ItemPatch(RSS3CustomItem):
    date_created: Optional[str]
    date_updated: Optional[str]


class CustomItems:
    def __init__(self, main):
        self._main = main
        self.backlinks = Backlinks(main, "auto")

    async def get_list_file(self, persona, index=-1):
        return await self._main.files.get_list(persona, "items", index, "list_custom")

    async def get_list(self, persona, breakpoint=None):
        index_file = await self._main.files.get(persona)
        if index_file.get("items", {}).get("list_custom"):

            def _bp(file):
                if breakpoint:
                    return breakpoint(file)
                else:
                    return False

            return await self._main.files.get_all(index_file["items"]["list_custom"], _bp)
        else:
            return []

    async def _get_position(self, item_id):
        result = {"file": None, "index": -1}

        def _bp(file):
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

        await self.get_list(self._main.account.address, _bp)
        return result

    async def get(self, item_id):
        position = await self._get_position(item_id)
        if position["index"] != -1:
            return position["file"]["list"][position["index"]]
        else:
            return None

    async def post(self, item_in):
        try:
            ItemPost(**item_in)
        except ValidationError:
            valid_shape = False
        else:
            valid_shape = True

        if utils_check.value_length(item_in) and valid_shape:
            file = await self.get_list_file(self._main.account.address, -1)
            if not file:
                new_id = utils_id.get_custom_items(self._main.account.address, 0)
                file = self._main.files.new(new_id)

                index_file = await self._main.files.get(self._main.account.address)
                if not index_file.get("items"):
                    index_file["items"] = {}
                index_file["items"]["list_custom"] = new_id
                self._main.files.set(index_file)

            if file.get("list") is None:
                file["list"] = []

            try:
                id_ = utils_id.parse(file["list"][0]["id"])["index"] + 1
            except IndexError:
                id_ = 0

            now_date = datetime.utcnow().isoformat(timespec="milliseconds") + "Z"
            item = {"date_created": now_date}
            item.update(copy.deepcopy(item_in))
            item.update(
                {
                    "id": utils_id.get_custom_item(self._main.account.address, id_),
                    "date_updated": now_date,
                }
            )

            if not utils_check.file_size_with_new(file, item):
                new_id = utils_id.get_custom_items(
                    self._main.account.address,
                    utils_id.parse(file["id"])["index"] + 1,
                )
                new_file = self._main.files.new(new_id)
                new_file["list"] = [item]
                new_file["list_next"] = file["id"]
                self._main.files.set(new_file)

                index_file = await self._main.files.get(self._main.account.address)
                if index_file.get("items") is None:
                    index_file["items"] = {}
                index_file["items"]["list_custom"] = new_id
                self._main.files.set(index_file)
            else:
                file["list"].insert(0, item)
                self._main.files.set(file)

            return item
        else:
            raise Exception("Parameter error")

    async def patch(self, item_in):
        try:
            ItemPost(**item_in)
        except ValidationError:
            valid_shape = False
        else:
            valid_shape = True

        if utils_check.value_length(item_in) and valid_shape:
            position = await self._get_position(item_in["id"])

            if position["index"] != -1:
                item = position["file"]["list"][position["index"]]
                item.update(copy.deepcopy(item_in))
                item.update(
                    {
                        "date_updated": datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
                        "date_created": item["date_created"],
                    }
                )
                self._main.files.set(position["file"])
                return item
            else:
                return None
        else:
            raise Exception("Parameter error")
