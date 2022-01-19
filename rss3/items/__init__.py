import httpx

from rss3.items.auto import AutoItems
from rss3.items.backlinks import Backlinks
from rss3.items.custom import CustomItems


class Items:
    def __init__(self, main):
        self._main = main
        self.auto = AutoItems(main)
        self.custom = CustomItems(main)

    async def get_list_by_persona(self, options):
        with httpx.AsyncClient() as client:
            url = f"{self._main.options['endpoint']}/items/list"
            response = await client.get(
                url,
                params={
                    "limit": options["limit"],
                    "tsp": options["tsp"],
                    "persona": options["persona"],
                    "link_id": options["link_id"],
                    "field_like": options["field_like"],
                },
            )
            return response["data"]
