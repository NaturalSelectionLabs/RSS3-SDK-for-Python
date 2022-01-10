from rss3.items.auto import AutoItems
from rss3.items.custom import CustomItems
from rss3.items.backlinks import Backlinks

class Items:
    def __init__(self, main):
        self._main = main
        self.auto = AutoItems(main)
        self.custom = CustomItems(main)
