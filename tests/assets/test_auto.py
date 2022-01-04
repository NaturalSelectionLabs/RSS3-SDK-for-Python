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
    "assets": {
        "list_auto": utils_id.get_auto_assets(rss3_instance.account.address, 1),
    },
}

assets1_file = {
    "id": utils_id.get_auto_assets(rss3_instance.account.address, 1),
    "version": config.version,
    "date_created": now,
    "date_updated": now,
    "auto": True,
    "list": ["EVM+-0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944-test-1"],
    "list_next": utils_id.get_auto_assets(rss3_instance.account.address, 0),
}
item_test = "EVM+-0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944-test-0"

assets0_file = {
    "id": utils_id.get_auto_assets(rss3_instance.account.address, 0),
    "version": config.version,
    "date_created": now,
    "date_updated": now,
    "auto": True,
    "list": [item_test],
}


@pytest.fixture
def mock(respx_mock):
    respx_mock.get(f"https://test.io/{rss3_instance.account.address}").mock(
        return_value=httpx.Response(200, json=index_file)
    )
    respx_mock.get(f"https://test.io/{utils_id.get_auto_assets(rss3_instance.account.address,1)}").mock(
        return_value=httpx.Response(200, json=assets1_file)
    )
    respx_mock.get(f"https://test.io/{utils_id.get_auto_assets(rss3_instance.account.address, 0)}").mock(
        return_value=httpx.Response(200, json=assets0_file)
    )
    yield respx_mock


@pytest.mark.asyncio
async def test_get_list_file(mock):
    result = await rss3_instance.assets.auto.get_list_file(rss3_instance.account.address, -1)
    assert result == assets1_file

    result = await rss3_instance.assets.auto.get_list_file(rss3_instance.account.address, 0)
    assert result == assets0_file


@pytest.mark.asyncio
async def test_get_list(mock):
    result = await rss3_instance.assets.auto.get_list(rss3_instance.account.address)
    assert result == [
        "EVM+-0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944-test-1",
        "EVM+-0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944-test-0",
    ]
