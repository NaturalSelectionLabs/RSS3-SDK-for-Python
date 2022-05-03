from datetime import datetime

import httpx
import pytest
from eth_account.account import Account as ETHAccount

from rss3 import RSS3, config
from rss3.utils import id as utils_id

now = datetime.utcnow().isoformat(timespec="milliseconds") + "Z"


signer, _ = ETHAccount.create_with_mnemonic()
rss3_instance = RSS3(
    {
        "endpoint": "https://test.io",
        "address": signer.address,
        "sign": signer.sign_message,
    }
)

index_file = {
    "id": rss3_instance.account.address,
    "version": config.version,
    "date_created": now,
    "date_updated": now,
    "signature": "",
    "backlinks": [
        {
            "auto": True,
            "id": "test",
            "list": utils_id.get_backlinks(rss3_instance.account.address, "test", 1),
        }
    ],
}

backlinks1_file = {
    "id": utils_id.get_backlinks(rss3_instance.account.address, "test", 1),
    "version": config.version,
    "date_created": now,
    "date_updated": now,
    "auto": True,
    "list": ["1", "2"],
    "list_next": utils_id.get_backlinks(rss3_instance.account.address, "test", 0),
}

backlinks0_file = {
    "id": utils_id.get_backlinks(rss3_instance.account.address, "test", 0),
    "version": config.version,
    "date_created": now,
    "date_updated": now,
    "auto": True,
    "list": ["3"],
}


@pytest.fixture
def mock(respx_mock):
    respx_mock.get(f"https://test.io/{rss3_instance.account.address}").mock(
        return_value=httpx.Response(200, json=index_file)
    )
    respx_mock.get(
        f"https://test.io/{utils_id.get_backlinks(rss3_instance.account.address,'test',1)}"
    ).mock(return_value=httpx.Response(200, json=backlinks1_file))
    respx_mock.get(
        f"https://test.io/{utils_id.get_backlinks(rss3_instance.account.address, 'test', 0)}"
    ).mock(return_value=httpx.Response(200, json=backlinks0_file))
    yield respx_mock


@pytest.mark.asyncio
async def test_get_list_file(mock):
    result = await rss3_instance.backlinks.get_list_file(
        rss3_instance.account.address, "test", -1
    )
    assert result == backlinks1_file

    result = await rss3_instance.backlinks.get_list_file(
        rss3_instance.account.address, "test", 0
    )
    assert result == backlinks0_file


@pytest.mark.asyncio
async def test_get_list(mock):
    result = await rss3_instance.backlinks.get_list(
        rss3_instance.account.address, "test"
    )
    assert result == ["1", "2", "3"]
