from rss3.items.backlinks import Backlinks
from rss3.utils import id as utils_id


class CustomItems:
    def __init__(self, main):
        self._main = main
        self.backlinks = Backlinks(main, "auto")
