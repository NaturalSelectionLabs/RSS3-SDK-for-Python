import httpx

from rss3.utils import check as utils_check
from rss3.utils import object as utils_object

from .accounts import Accounts


class Profile:
    def __init__(self, main):
        self._main = main
        self.accounts = Accounts(self._main)

    async def get(self, persona_id=""):
        if persona_id == "":
            persona_id = self._main.account.address
        file = await self._main.files.get(persona_id)
        return file.get("profile", {})

    async def patch(self, profile):
        # todo: verify profile shape
        if utils_check.value_length(profile):
            file = await self._main.files.get(self._main.account.address)
            file["profile"].update(profile)
            utils_object.remove_empty(file["profile"], {"obj": file, "key": "profile"})
            self._main.files.set(file)
        else:
            raise Exception("Parameter error")

    async def get_list(self, personas):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self._main.options['endpoint']}/profile/list",
                params={"personas": ",".join(personas)},
            )
            return response["data"]