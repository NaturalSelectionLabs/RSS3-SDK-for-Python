from datetime import datetime

import httpx
import pytest
from eth_account.account import Account as ETHAccount

from rss3 import RSS3, config
from rss3.utils import object as utils_object

now = datetime.utcnow().isoformat(timespec="milliseconds") + "Z"


signer, _ = ETHAccount.create_with_mnemonic()
rss3_instance = RSS3(
    {
        "endpoint": "https://test.io",
        "address": signer.address,
        "sign": signer.sign_message,
    }
)

signer1, _ = ETHAccount.create_with_mnemonic()
account1 = {"id": f"EVM+-{signer1.address}"}

account2 = {
    "id": "EVM+-0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944",
}

file = {
    "id": rss3_instance.account.address,
    "version": config.version,
    "date_created": now,
    "date_updated": now,
    "signature": "",
    "profile": {
        "accounts": [account1],
    },
}


@pytest.fixture
def mock(respx_mock):
    respx_mock.get(f"https://test.io/{rss3_instance.account.address}").mock(
        return_value=httpx.Response(200, json=file)
    )
    yield respx_mock


@pytest.mark.asyncio
async def test_get_list(mock):
    result = await rss3_instance.profile.accounts.get_list()
    assert result == [account1]


@pytest.mark.asyncio
async def test_post(mock):
    await rss3_instance.profile.accounts.post(account2)
    result = await rss3_instance.profile.accounts.get_list()
    assert result == [account1, account2]

    result2 = await rss3_instance.files.get()
    assert result2["profile"] == {"accounts": [account1, account2]}


@pytest.mark.asyncio
async def test_patch_tags(mock):
    await rss3_instance.profile.accounts.patch_tags(account2["id"], ["test"])
    account2["tags"] = ["test"]
    result = await rss3_instance.profile.accounts.get_list()
    assert result == [account1, account2]

    result2 = await rss3_instance.files.get()
    assert result2["profile"] == {"accounts": [account1, account2]}


@pytest.mark.asyncio
async def test_get_sig_message():
    result = await rss3_instance.profile.accounts.get_sig_message(account2)
    assert result == utils_object.stringify_obj(
        dict(**account2, address=rss3_instance.account.address)
    )


@pytest.mark.asyncio
async def test_delete(mock):
    await rss3_instance.profile.accounts.delete(account2["id"])
    result = await rss3_instance.profile.accounts.get_list()
    assert result == [account1]

    result2 = await rss3_instance.files.get()
    assert result2["profile"] == {"accounts": [account1]}
