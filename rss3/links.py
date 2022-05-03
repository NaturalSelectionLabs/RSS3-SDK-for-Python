from typing import List, Optional

from pydantic import BaseModel, ValidationError

from rss3.models import RSS3ID
from rss3.utils import check as utils_check
from rss3.utils import id as utils_id


class LinksPost(BaseModel):
    tags: Optional[List[str]]
    id: str
    list: Optional[List[RSS3ID]]


class Links:
    def __init__(self, main):
        self._main = main

    async def _get_position(self, persona, id_):
        file = await self._main.files.get(persona)
        links = file.get("links", [])
        index = -1
        for i, lks in enumerate(links):
            if lks["id"] == id_:
                index = i
                break

        return {
            "file": file,
            "index": index,
            "file_id": file["links"][index].get("list") if index != -1 else None,
        }

    async def get_list_file(self, persona, id_, index=-1):
        return await self._main.files.get_list(persona, "links", index, id_)

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

    async def post_list(self, links):
        try:
            LinksPost(**links)
        except ValidationError:
            valid_shape = False
        else:
            valid_shape = True

        if utils_check.value_length(links) and valid_shape:
            result = await self._get_position(self._main.account.address, links["id"])
            file = result["file"]
            index = result["index"]
            if index == -1:
                for lk in links.get("list", []):
                    self._main.files.clear_cache(utils_id.get_links(lk, links["id"], ""), True)
                new_id = utils_id.get_links(self._main.account.address, links["id"], 0)
                new_file = self._main.files.new(new_id)
                if not file.get("links"):
                    file["links"] = []
                file["links"].append({"tags": links.get("tags"), "id": links["id"], "list": new_id})
                if "list" in links:
                    new_file["list"] = links["list"]
                if not utils_check.file_size(new_file):
                    self._main.files.clear_cache(new_id)
                    raise Exception("Exceeding the file size limit")
                self._main.files.set(file)
                self._main.files.set(new_file)
            else:
                raise Exception("Link id already exists")
            return links
        else:
            raise Exception("Parameter error")

    async def delete_list(self, id_):
        result = await self._get_position(self._main.account.address, id_)
        file = result["file"]
        index = result["index"]
        if index > -1:
            links = file["links"][index]
            if links.get("list"):
                list_file = await self._main.files.get(links["list"])
                if "list" in list_file:
                    for lk in list_file["list"]:
                        self._main.files.clear_cache(utils_id.get_backlinks(lk, links["id"], ""), True)
                del file["links"][index]
                self._main.files.set(file)
                return links

    async def patch_list_tags(self, id_, tags):
        valid_shape = isinstance(tags, list) and all(isinstance(item, str) for item in tags)
        if utils_check.value_length(tags) and valid_shape:
            result = await self._get_position(self._main.account.address, id_)
            file = result["file"]
            index = result["index"]
            if index > -1:
                file["links"][index]["tags"] = tags
                self._main.files.set(file)
                return file["links"][index]
            else:
                raise Exception("Link id does not exist")
        else:
            raise Exception("Parameter error")

    async def post(self, id_, persona_id):
        position = await self._get_position(self._main.account.address, id_)
        index_file = position["file"]
        file_id = position["file_id"]
        links_index = position["index"]
        if file_id:

            def _bk(f):
                return f.get("list") and (persona_id in f["list"])

            list_ = await self.get_list(self._main.account.address, id_, _bk)
            try:
                index = list_.index(persona_id)
            except ValueError:
                index = -1

            if index == -1:
                self._main.files.clear_cache(utils_id.get_backlinks(persona_id, id_, ""), True)
                file = await self._main.files.get(file_id)
                if not file.get("list"):
                    file["list"] = []

                if not utils_check.file_size_with_new(file, persona_id):
                    new_id = utils_id.get_links(
                        self._main.account.address, id_, utils_id.parse(file["id"])["index"] + 1
                    )
                    new_file = self._main.files.new(new_id)
                    new_file["list"] = [persona_id]
                    new_file["list_next"] = file["id"]
                    self._main.files.set(new_file)

                    index_file["links"][links_index]["list"] = new_id
                    self._main.files.set(index_file)
                else:
                    file["list"].insert(0, persona_id)
                    self._main.files.set(file)
                self._main.files.set(file)  # js await ?
                return file
            else:
                raise Exception("Link already exist")
        else:
            await self.post_list({"id": id_, "list": [persona_id]})

    async def delete(self, id_, persona_id):
        position = await self._get_position(self._main.account.address, id_)
        file_id = position["file_id"]
        result = None
        if file_id:

            def _bk(file):
                if not file.get("list"):
                    return False
                index = file["list"].index(persona_id)
                if index > -1:
                    self._main.files.clear_cache(utils_id.get_backlinks(persona_id, id_, ""), True)
                    del file["list"][index]
                    result = file["list"]
                    self._main.files.set(file)
                    return True
                return False

            await self.get_list(self._main.account.address, id_, _bk)
        return result
