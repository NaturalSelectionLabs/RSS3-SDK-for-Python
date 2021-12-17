import asyncio

from eth_account.account import Account as ETHAccount
from eth_account.messages import encode_defunct

from rss3.account.sign_agent import SignAgent
from rss3.utils import object as utils_object

ETHAccount.enable_unaudited_hdwallet_features()


class Account:
    def __init__(self, main):
        self._main = main
        self._signer = None

        self.mnemonic = None
        self.private_key = None
        self.agent_sign = None

        if main.options.get("mnemonic"):
            self._signer = ETHAccount.from_mnemonic(main.options["mnemonic"])
            self.mnemonic = main.options["mnemonic"]
        elif main.options.get("private_key"):
            self._signer = ETHAccount.from_key(main.options["private_key"])
        elif main.options.get("address") and main.options.get("sign"):
            self.address = main.options["address"]
        else:
            self._signer, self.mnemonic = ETHAccount.create_with_mnemonic(
                account_path=main.options["mnemonic_path"]
            )
            self._main.files.new(self._signer.address)

        if self._signer:
            self.private_key = self._signer.privateKey
            self.address = self._signer.address
        if self._main.options.get("agent_sign", False):
            self.sign_agent = SignAgent(main)

    async def sign(self, obj):
        if self._main.options.get("agent_sign", False):
            obj["agent_id"] = await self.sign_agent.get_address()
            agent_message = self.sign_agent.get_message(obj["agent_id"])
            signable_message = encode_defunct(agent_message.encode())
            if not obj.get("agent_signature") or ETHAccount.recover_message(
                signable_message, signature=obj["signature"]
            ) != obj.get("id"):
                if self._signer:
                    loop = asyncio.get_running_loop()
                    sig = await loop.run_in_executor(
                        None, self._signer.sign_message, signable_message
                    )
                    obj["signature"] = sig.signature.hex()
                elif self._main.options.sign:
                    obj["signature"] = await self._main.options.sign(agent_message)
            obj["agent_signature"] = await self.sign_agent.sign(obj)
        else:
            obj.pop("agent_signature", None)
            obj.pop("agent_id", None)
            if self._signer:
                signable_message = encode_defunct(
                    utils_object.stringify_obj(obj).encode()
                )
                loop = asyncio.get_running_loop()
                sig = await loop.run_in_executor(
                    None, self._signer.sign_message, signable_message
                )
                obj["signature"] = sig.signature.hex()
            elif self._main.options.get("sign"):
                obj["signature"] = await self._main.options["sign"](
                    utils_object.stringify_obj(obj)
                )
