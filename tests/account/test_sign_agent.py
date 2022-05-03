import copy

import pytest
from eth_account.account import Account as ETHAccount
from eth_account.messages import encode_defunct
from eth_account.signers.local import LocalAccount
from nacl.bindings import crypto_sign_open
from nacl.encoding import Base64Encoder
from nacl.signing import VerifyKey

from rss3 import RSS3
from rss3.utils import object as utils_object


class AgentStorage:
    def __init__(self):
        self._storage = {}

    async def set(self, key, value):
        self._storage[key] = value

    async def get(self, key):
        return self._storage.get(key)


@pytest.mark.asyncio
async def test_account_sign_with_sign_agent():
    signer: LocalAccount
    signer, mnemonic = ETHAccount.create_with_mnemonic()
    rss3 = RSS3(
        {
            "endpoint": "",
            "mnemonic": mnemonic,
            "agent_sign": True,
            "agent_storage": AgentStorage(),
        }
    )
    data = {"agent_id": "test", "test1": "r"}
    await rss3.account.sign(data)

    signable_message = encode_defunct(
        f"Hi, RSS3. I'm your agent {data['agent_id']}".encode()
    )
    assert (
        ETHAccount.recover_message(signable_message, signature=data["signature"])
        == signer.address
    )
    verify_key = VerifyKey(Base64Encoder.decode(data["agent_id"]))
    assert verify_key.verify(Base64Encoder.decode(data["agent_signature"]))

    first_data = copy.deepcopy(data)
    data["test2"] = "s"
    await rss3.account.sign(data)
    assert data["signature"] == first_data["signature"]
    assert data["agent_id"] == first_data["agent_id"]
    assert data["agent_signature"] != first_data["agent_signature"]
