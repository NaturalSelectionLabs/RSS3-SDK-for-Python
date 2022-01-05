from rss3.items.auto import AutoItems
from rss3.items.custom import CustomItems


class Items:
    def __init__(self, main):
        self._main = main
        self.auto = AutoItems(main)
        self.custom = CustomItems(main)
