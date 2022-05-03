import httpx

from rss3.assets.auto import AutoAssets
from rss3.assets.custom import CustomAssets


class Assets:
    def __init__(self, main):
        self._main = main
        self.auto = AutoAssets(main)
        self.custom = CustomAssets(main)

    async def get_details(self, options):
        with httpx.AsyncClient() as client:
            url = f"{self._main.options['endpoint']}/assets/details"
            full = options.get("full", False)
            response = await client.get(
                url,
                params={
                    "assets": ",".join(options["assets"]),
                    "full": "1" if full else "0",
                },
            )
            return response["data"]
