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
    "items": {"list_auto": utils_id.get_auto_items(rss3_instance.account.address, 0)},
}

item_test = {
    "id": utils_id.get_auto_item(rss3_instance.account.address, 0),
    "date_created": now,
    "date_updated": now,
    "title": "Test0",
    "backlinks": [
        {
            "auto": True,
            "id": "like",
            "list": utils_id.get_item_backlinks(rss3_instance.account.address, "like", 1, 0),
        },
        {
            "auto": True,
            "id": "comment",
            "list": utils_id.get_item_backlinks(rss3_instance.account.address, "comment", 1, 0),
        },
    ],
    "target": {
        "field": "test0",
        "action": {
            "type": "add",
            "payload": "test",
            "proof": "test",
        },
    },
}
comment1_test = {
    "id": utils_id.get_item_backlinks(rss3_instance.account.address, "comment", 1, 0),
    "version": config.version,
    "date_created": now,
    "date_updated": now,
    "auto": True,
    "list": ["2", "1"],
    "list_next": utils_id.get_item_backlinks(rss3_instance.account.address, "comment", 0, 0),
}

comment0_test = {
    "id": utils_id.get_item_backlinks(rss3_instance.account.address, "comment", 0, 0),
    "version": config.version,
    "date_created": now,
    "date_updated": now,
    "auto": True,
    "list": ["0"],
}

backlinks1_file = {
    "id": utils_id.get_backlinks(rss3_instance.account.address, "test", 1),
    "version": config.version,
    "date_created": now,
    "date_updated": now,
    "auto": True,
    "list": ["2", "1"],
    "list_next": utils_id.get_backlinks(rss3_instance.account.address, "test", 0),
}

items0_file = {
    "id": utils_id.get_auto_items(rss3_instance.account.address, 0),
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
    respx_mock.get(f"https://test.io/{utils_id.get_auto_items(rss3_instance.account.address,0)}").mock(
        return_value=httpx.Response(200, json=items0_file)
    )
    respx_mock.get(
        f"https://test.io/{utils_id.get_item_backlinks(rss3_instance.account.address, 'comment',1, 0)}"
    ).mock(return_value=httpx.Response(200, json=comment1_test))
    respx_mock.get(
        f"https://test.io/{utils_id.get_item_backlinks(rss3_instance.account.address, 'comment', 0, 0)}"
    ).mock(return_value=httpx.Response(200, json=comment0_test))
    yield respx_mock


@pytest.mark.asyncio
async def test_get_list_file(mock):
    result = await rss3_instance.items.auto.backlinks.get_list_file(item_test["id"], "comment", -1)
    assert result == comment1_test

    result = await rss3_instance.items.auto.backlinks.get_list_file(item_test["id"], "comment", 0)
    assert result == comment0_test


@pytest.mark.asyncio
async def test_get_list(mock):
    result = await rss3_instance.items.auto.backlinks.get_list(item_test["id"], "comment")
    assert result == ["2", "1", "0"]
