import copy
import json
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
        "list_custom": utils_id.get_custom_assets(rss3_instance.account.address, 1),
    },
}

assets1_file = {
    "id": utils_id.get_custom_assets(rss3_instance.account.address, 1),
    "version": config.version,
    "date_created": now,
    "date_updated": now,
    "signature": "",
    "list": ["custom-RSS3-test-1"],
    "list_next": utils_id.get_custom_assets(rss3_instance.account.address, 0),
}

asset_test = "custom-RSS3-test-0"
assets0_file = {
    "id": utils_id.get_custom_assets(rss3_instance.account.address, 0),
    "version": config.version,
    "date_created": now,
    "date_updated": now,
    "signature": "",
    "list": [asset_test],
}


@pytest.fixture
def mock(respx_mock):
    respx_mock.get(f"https://test.io/{rss3_instance.account.address}").mock(
        return_value=httpx.Response(200, json=index_file)
    )
    respx_mock.get(f"https://test.io/{utils_id.get_custom_assets(rss3_instance.account.address,1)}").mock(
        return_value=httpx.Response(200, json=assets1_file)
    )
    respx_mock.get(f"https://test.io/{utils_id.get_custom_assets(rss3_instance.account.address, 0)}").mock(
        return_value=httpx.Response(200, json=assets0_file)
    )
    yield respx_mock


@pytest.mark.asyncio
async def test_get_list_file(mock):
    result = await rss3_instance.assets.custom.get_list_file(rss3_instance.account.address, -1)
    assert result == assets1_file

    result = await rss3_instance.assets.custom.get_list_file(rss3_instance.account.address, 0)
    assert result == assets0_file


@pytest.mark.asyncio
async def test_get_list(mock):
    result = await rss3_instance.assets.custom.get_list(rss3_instance.account.address)
    assert result == ["custom-RSS3-test-1", "custom-RSS3-test-0"]


@pytest.mark.asyncio
async def test_delete(mock):
    await rss3_instance.assets.custom.delete(asset_test)
    result = await rss3_instance.assets.custom.get_list_file(rss3_instance.account.address, 0)
    assert not result.get("list")


# fixme: can not pass
@pytest.mark.asyncio
async def test_post(mock):
    file = await rss3_instance.assets.custom.get_list_file(rss3_instance.account.address)
    file = copy.deepcopy(file)
    assets = []
    i = 1
    while len(json.dumps(file)) < 1024:  # fixme: use config.file_size_limit
        i += 1
        new_item = f"custom-RSS3-test-{i}"
        file["list"].insert(0, new_item)
        assets.append(new_item)

    for asset in assets:
        await rss3_instance.assets.custom.post(asset)

    result = await rss3_instance.files.get()
    assert result["assets"]["list_custom"] == utils_id.get_custom_assets(rss3_instance.account.address, 2)
    last_file = await rss3_instance.assets.custom.get_list_file(rss3_instance.account.address)
    assert last_file["id"] == utils_id.get_custom_assets(rss3_instance.account.address, 2)
    assert len(last_file["list"]) == 1
