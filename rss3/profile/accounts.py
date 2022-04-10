import asyncio
import copy

from pydantic import ValidationError

from rss3.models import RSS3Account
from rss3.utils import check as utils_check
from rss3.utils import object as utils_object


class Accounts:
    def __init__(self, main):
        self._main = main

    async def _get_position(self, persona, id_):
        file = await self._main.files.get(persona)
        acc_list = file.get("profile", {}).get("accounts", [])
        index = -1
        for i, acc in enumerate(acc_list):
            if acc["id"] == id_:
                index = i
                break
        return {"file": file, "index": index}

    async def get_sig_message(self, account):
        acc = copy.deepcopy(account)
        acc["address"] = self._main.account.address
        return await asyncio.get_event_loop().run_in_executor(None, utils_object.stringify_obj, acc)

    async def post(self, account):
        try:
            RSS3Account(**account)
        except ValidationError:
            valid_shape = False
        else:
            valid_shape = True

        if utils_check.value_length(account) and valid_shape:
            file = await self._main.files.get(self._main.account.address)
            if "profile" not in file:
                file["profile"] = {}
            if "accounts" not in file["profile"]:
                file["profile"]["accounts"] = []
            accounts = file["profile"]["accounts"]
            existed = False
            for acc in accounts:
                if acc["id"] == account["id"]:
                    existed = True
                    break
            if not existed:
                file["profile"]["accounts"].append(account)
                self._main.files.set(file)
            else:
                raise Exception("Account already exists")
        else:
            raise Exception("Parameter error")

    async def patch_tags(self, id_, tags):
        if utils_check.value_length(tags):
            result = await self._get_position(self._main.account.address, id_)
            file = result["file"]
            index = result["index"]
            if index != -1:
                file["profile"]["accounts"][index]["tags"] = tags
                self._main.files.set(file)
                return file["profile"]["accounts"][index]
            else:
                raise Exception("Account does not exist")
        else:
            raise Exception("Parameter error")

    async def get_list(self, persona=""):
        if persona == "":
            persona = self._main.account.address
        file = await self._main.files.get(persona)
        return file.get("profile", {}).get("accounts", [])

    async def delete(self, id_):
        result = await self._get_position(self._main.account.address, id_)
        file = result["file"]
        index = result["index"]
        if index != -1:
            del file["profile"]["accounts"][index]
            self._main.files.set(file)  # fixme: no need await (JS version error)
            return id_
        else:
            raise Exception("Account does not exist")
