from .account import Account
from .assets import Assets
from .backlinks import Backlinks
from .files import File
from .links import Links
from .profile import Profile


class RSS3:
    def __init__(self, options):
        self.options = options
        self.files = Files(self)
        self.account = Account(self)
        self.profile = Profile(self)
        self.items = Items(self)
        self.links = Links(self)
        self.backlinks = Backlinks(self)
        self.assets = Assets(self)
