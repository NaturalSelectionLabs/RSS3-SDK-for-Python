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

file = {
    "id": rss3_instance.account.address,
    "version": config.version,
    "date_created": now,
    "date_updated": now,
    "signature": "",
    "profile": {
        "name": "test",
    },
}


@pytest.fixture
def mock(respx_mock):
    respx_mock.get(f"https://test.io/{rss3_instance.account.address}").mock(
        return_value=httpx.Response(200, json=file)
    )
    yield respx_mock


@pytest.mark.asyncio
async def test_get(mock):
    result = await rss3_instance.profile.get()
    assert result == {"name": "test"}


@pytest.mark.asyncio
async def test_get_and_patch(mock):
    profile2in = {
        "name": "",
        "avatar": ["test1"],
        "bio": "test2",
    }
    profile2 = {
        "avatar": ["test1"],
        "bio": "test2",
    }
    await rss3_instance.profile.patch(profile2in)
    result = await rss3_instance.profile.get()
    assert result == profile2

    result2 = await rss3_instance.files.get()
    assert result2["profile"] == profile2
