import pytest
from eth_account.account import Account as ETHAccount
from eth_account.messages import encode_defunct
from eth_account.signers.local import LocalAccount

from rss3 import RSS3
from rss3.utils import object as utils_object


@pytest.mark.asyncio
async def test_sign_with_signer():
    signer: LocalAccount
    signer, mnemonic = ETHAccount.create_with_mnemonic()
    rss3 = RSS3({"endpoint": "", "mnemonic": mnemonic})
    data = {"agent_id": "test", "test1": "r"}
    await rss3.account.sign(data)
    signable_message = encode_defunct(
        utils_object.stringify_obj({"test1": "r"}).encode()
    )
    expected = signer.sign_message(signable_message).signature.hex()
    assert data["signature"] == expected


@pytest.mark.asyncio
async def test_with_custom_sign():
    signer: LocalAccount
    signer, mnemonic = ETHAccount.create_with_mnemonic()

    async def sign(d):
        return "sign" + d

    rss3 = RSS3({"endpoint": "", "address": signer.address, "sign": sign})
    data = {"agent_id": "test", "test1": "r"}
    await rss3.account.sign(data)
    assert data["signature"] == "sign" + utils_object.stringify_obj({"test1": "r"})
