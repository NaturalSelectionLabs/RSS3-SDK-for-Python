from rss3.assets.auto import AutoAssets
from rss3.assets.custom import CustomAssets


class Assets:
    def __init__(self, main):
        self._main = main
        self.auto = AutoAssets(main)
        self.custom = CustomAssets(main)
