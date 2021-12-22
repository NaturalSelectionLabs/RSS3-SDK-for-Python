import asyncio
from datetime import datetime

import httpx

from rss3 import config
from rss3.utils import check as utils_check
from rss3.utils import id as utils_id
from rss3.utils import object as utils_object


def _isoformat_now():
    return datetime.utcnow().isoformat(timespec="milliseconds") + "Z"


class File:
    def __init__(self, main):
        self._main = main
        self._list = {}
        self._dirty_list = {}

    def new(self, file_id):
        now_date = _isoformat_now()
        print(now_date)
        self.set(
            {
                "id": file_id,
                "version": config.version,
                "date_created": now_date,
                "date_updated": now_date,
                "signature": "",
            }
        )
        return self._list[file_id]

    def get(self, file_id="", force=False):
        if not file_id:
            file_id = self._main.account.address

        async def _get():
            if file_id in self._list and not force:
                return self._list[file_id]

            async with httpx.AsyncClient() as client:
                try:
                    res = await client.get(
                        f"{self._main.options['endpoint']}/{file_id}"
                    )
                    res.raise_for_status()
                    content = res.json()
                    # todo: verify content shape
                    self._list[file_id] = content
                    return self._list[file_id]
                except httpx.HTTPError as exc:
                    if hasattr(exc, "response"):
                        try:
                            res_json = exc.response.json()
                            if res_json["code"] == 5001:
                                now_date = _isoformat_now()
                                self._list[file_id] = {
                                    "id": file_id,
                                    "version": config.version,
                                    "date_created": now_date,
                                    "date_updated": now_date,
                                    "signature": "",
                                }
                                self._dirty_list[file_id] = 1
                                return self._list[file_id]
                        except Exception as e:
                            raise Exception(
                                f"Server response error. Error: {self._main.options['endpoint']}/{file_id} {e}"
                            )
                    else:
                        raise Exception(
                            f"Server response error. Error: {self._main.options['endpoint']}/{file_id} {exc}"
                        )

        task = asyncio.create_task(_get())
        return task

    async def get_list(self, persona, field, index=-1, id_=""):
        if index < 0:
            index_file = await self._main.files.get(persona)
            if field in index_file:
                ...
            else:
                return None
        else:
            if id_:
                return await self._main.files.get(
                    utils_id.get(
                        persona, "list", index, [field, id_.replace("list_", "")]
                    )
                )
            else:
                return await self._main.files.get(
                    utils_id.get(persona, "list", index, [field])
                )

    async def get_all(self, file_id, breakpoint=None):
        list_ = []
        id_ = file_id
        list_file = await self.get(id_)
        if breakpoint and breakpoint(list_file):
            return list_
        list_.extend(list_file.get("list", []))
        id_ = list_file.get("list_next")
        while id_:
            list_file = await self.get(id_)
            if breakpoint and breakpoint(list_file):
                break
            list_.extend(list_file.get("list", []))
            id_ = list_file.get("list_next")
        return list_

    def set(self, content):
        utils_object.remove_empty(content)
        content["date_updated"] = ""
        content["version"] = config.version
        if utils_check.file_size(content):
            self._list[content["id"]] = content
            self._dirty_list[content["id"]] = 1
        else:
            raise Exception("File size is too large.")

    def clear_cache(self, key, wildcard=False):
        if wildcard:
            for file_id in list(self._list):
                if key in file_id:
                    del self._list[file_id]
        else:
            del self._list[key]

    async def sync(self):
        async def _sign(file_id):
            content = self._list[file_id]
            await self._main.account.sign(content)
            if "auto" in content:
                del content["auto"]
            return content

        file_ids = list(self._dirty_list.keys())

        coros = []
        for file_id in file_ids:
            coros.append(_sign(file_id))

        results = await asyncio.gather(*coros)
        async with httpx.AsyncClient() as client:
            await client.put(self._main.options.endpoint, json={"contents": contents})

        for file_id in file_ids:
            del self._dirty_list[file_id]
