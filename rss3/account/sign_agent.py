import asyncio
import base64
import hashlib
import json

from nacl.bindings import crypto_sign, crypto_sign_keypair
from nacl.encoding import Base64Encoder

from rss3.utils import object as utils_object


class SignAgent:
    def __init__(self, main):
        self._main = main
        self._private_key = ""
        self._public_key = ""
        self._init_task = asyncio.create_task(self._init())

        self.address = ""

    async def _init(self):
        agent = await self._get()
        if agent and agent.private_key and agent.public_key:
            self._private_key = ""
            self._public_key = ""
        else:
            self._public_key, self._private_key = crypto_sign_keypair()
            self._set(
                {
                    # todo (unified key type): TypeError: Object of type bytes is not JSON serializable
                    "public_key": Base64Encoder.encode(self._public_key).decode(),
                    "private_key": Base64Encoder.encode(self._private_key).decode(),
                }
            )
        self.address = Base64Encoder.encode(self._public_key).decode()

    async def _get_address(self):
        await self._init_task
        return self.address

    def get_address(self):
        return asyncio.create_task(self._get_address())

    def get_message(self, address):
        return f"Hi, RSS3. I'm your agent {address}"

    async def sign(self, obj):
        await self._init_task
        message_bytes = utils_object.stringify_obj(obj).encode()
        signature = crypto_sign(message_bytes, self._private_key)  # attached signature
        return Base64Encoder.encode(signature)

    def _get_key(self, address):
        b_address = address.encode("utf-8")
        return "RSS3.0" + hashlib.md5(b_address).hexdigest()

    def _set(self, value):
        key = self._get_key(self._main.account.address)
        va = base64.standard_b64encode(json.dumps(value).encode()).decode()

        if self._main.options.get("agent_storage"):
            # fixme: asyncio.create_task?
            self._main.options["agent_storage"].set(key, va)
        else:
            # JavaScript implementation uses cookie as default agent storage in browser environment.
            # No default implementation for node environment.
            # Should we implement a default agent storage for python?
            ...

    async def _get(self):
        try:
            agent_storage = self._main.options.get("agent_storage")
            if agent_storage and hasattr(agent_storage, "get"):
                key = self._get_key(self._main.acount.address)
                data = await agent_storage.get(key)
            else:
                # no default agent storage implementation for now
                data = None

            if data:
                result = json.loads(base64.standard_b64decode(data))
                self._set(result)
                return result
            else:
                return None
        except Exception:  # noqa
            return None
