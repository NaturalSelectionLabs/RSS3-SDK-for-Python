from rss3.account import Account
from rss3.assets import Assets
from rss3.backlinks import Backlinks
from rss3.files import File as Files
from rss3.items import Items
from rss3.links import Links

# from rss3.profile import Profile


class RSS3:
    def __init__(self, options):
        self.options = options
        self.files = Files(self)
        self.account = Account(self)
        # self.profile = Profile(self)
        self.items = Items(self)
        self.links = Links(self)
        self.backlinks = Backlinks(self)
        self.assets = Assets(self)
