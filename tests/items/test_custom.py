import copy
import itertools
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
    "items": {
        "list_custom": utils_id.get_custom_items(rss3_instance.account.address, 1),
    },
}

items1_file = {
    "id": utils_id.get_custom_items(rss3_instance.account.address, 1),
    "version": config.version,
    "date_created": now,
    "date_updated": now,
    "signature": "",
    "list": [
        {
            "id": utils_id.get_custom_item(rss3_instance.account.address, 1),
            "date_created": now,
            "date_updated": now,
            "title": "Test1",
        },
    ],
    "list_next": utils_id.get_custom_items(rss3_instance.account.address, 0),
}

item_test = {
    "id": utils_id.get_custom_item(rss3_instance.account.address, 0),
    "date_created": now,
    "date_updated": now,
    "title": "Test0",
}
items0_file = {
    "id": utils_id.get_custom_items(rss3_instance.account.address, 0),
    "version": config.version,
    "date_created": now,
    "date_updated": now,
    "signature": "",
    "list": [item_test],
}


@pytest.fixture
def mock(respx_mock):
    respx_mock.get(f"https://test.io/{rss3_instance.account.address}").mock(
        return_value=httpx.Response(200, json=index_file)
    )
    respx_mock.get(f"https://test.io/{utils_id.get_custom_items(rss3_instance.account.address,1)}").mock(
        return_value=httpx.Response(200, json=items1_file)
    )
    respx_mock.get(f"https://test.io/{utils_id.get_custom_items(rss3_instance.account.address, 0)}").mock(
        return_value=httpx.Response(200, json=items0_file)
    )
    yield respx_mock


@pytest.mark.asyncio
async def test_get_list_file(mock):
    result = await rss3_instance.items.custom.get_list_file(rss3_instance.account.address, -1)
    assert result == items1_file

    result = await rss3_instance.items.custom.get_list_file(rss3_instance.account.address, 0)
    assert result == items0_file


@pytest.mark.asyncio
async def test_get_list(mock):
    result = await rss3_instance.items.custom.get_list(rss3_instance.account.address)
    assert result == list(itertools.chain(items1_file["list"], items0_file["list"]))


@pytest.mark.asyncio
async def test_get(mock):
    result = await rss3_instance.items.custom.get(item_test["id"])
    assert result == item_test


@pytest.mark.asyncio
async def test_post(mock, respx_mock):
    file = await rss3_instance.items.custom.get_list_file(rss3_instance.account.address)
    file = copy.deepcopy(file)
    file["signature"] = "0" * 132
    items = []
    i = 2
    while len(json.dumps(file)) < config.file_size_limit:
        file["list"].insert(
            0,
            {
                "id": utils_id.get_custom_item(rss3_instance.account.address, i),
                "date_created": now,
                "date_updated": now,
                "title": f"Test{i}",
            },
        )
        items.append({"title": f"Test{i}"})

    for item in items:
        await rss3_instance.items.custom.post(item)

    result = await rss3_instance.files.get()
    assert result["items"]["list_custom"] == utils_id.get_custom_items(rss3_instance.account.address, 2)
    last_list = await rss3_instance.items.custom.get_list_file(rss3_instance.account.address)
    assert last_list["id"] == utils_id.get_custom_items(rss3_instance.account.address, 2)
    assert len(last_list["list"]) == 1

    signer1, _ = ETHAccount.create_with_mnemonic()
    rss3_instance1 = RSS3(
        {
            "endpoint": "https://test.io",
            "address": signer1.address,
            "sign": signer1.sign_message,
        }
    )
    respx_mock.get(f"https://test.io/{signer1.address}").mock(return_value=httpx.Response(404, json={"code": 5001}))
    await rss3_instance1.items.custom.post({"title": "Test"})
    result = await rss3_instance1.files.get()
    assert result["items"]["list_custom"] == utils_id.get_custom_items(rss3_instance1.account.address, 0)


@pytest.mark.asyncio
async def test_patch(mock):
    item_test["summary"] = "TestSummary0"
    await rss3_instance.items.custom.patch(item_test)
    result = await rss3_instance.items.custom.get_list_file(rss3_instance.account.address, 0)
    result = result["list"][0]
    result["date_updated"] = item_test["date_updated"]
    assert result == item_test
