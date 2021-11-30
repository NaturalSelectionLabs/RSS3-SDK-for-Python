class Account:
    def __init__(self, main):
        self._main = main
        self._signer = None
        self._agent_private_key = ""
        self._agent_public_key = ""

        self.mnemonic = ""
        self.private_key = ""
        self.address = ""
