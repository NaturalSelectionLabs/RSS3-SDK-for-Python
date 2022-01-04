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
    "links": [
        {
            "id": "test",
            "list": utils_id.get_links(rss3_instance.account.address, "test", 1),
        }
    ],
}

links1_file = {
    "id": utils_id.get_links(rss3_instance.account.address, "test", 1),
    "version": config.version,
    "date_created": now,
    "date_updated": now,
    "signature": "",
    "list": ["1", "2"],
    "list_next": utils_id.get_links(rss3_instance.account.address, "test", 0),
}

links0_file = {
    "id": utils_id.get_links(rss3_instance.account.address, "test", 0),
    "version": config.version,
    "date_created": now,
    "date_updated": now,
    "signature": "",
    "list": ["3"],
}


@pytest.fixture
def mock(respx_mock):
    respx_mock.get(f"https://test.io/{rss3_instance.account.address}").mock(
        return_value=httpx.Response(200, json=index_file)
    )
    respx_mock.get(f"https://test.io/{utils_id.get_links(rss3_instance.account.address,'test',1)}").mock(
        return_value=httpx.Response(200, json=links1_file)
    )
    respx_mock.get(f"https://test.io/{utils_id.get_links(rss3_instance.account.address, 'test', 0)}").mock(
        return_value=httpx.Response(200, json=links0_file)
    )
    yield respx_mock


@pytest.mark.asyncio
async def test_get_list_file(mock):
    result = await rss3_instance.links.get_list_file(rss3_instance.account.address, "test", -1)
    assert result == links1_file

    result = await rss3_instance.links.get_list_file(rss3_instance.account.address, "test", 0)
    assert result == links0_file


@pytest.mark.asyncio
async def test_get_list(mock):
    result = await rss3_instance.links.get_list(rss3_instance.account.address, "test")
    assert result == ["1", "2", "3"]


@pytest.mark.asyncio
async def test_post_list(mock):
    await rss3_instance.links.post_list({"id": "test1", "list": ["a", "b"]})
    result = await rss3_instance.links.get_list(rss3_instance.account.address, "test1")
    assert result == ["a", "b"]

    result2 = await rss3_instance.files.get()
    assert result2["links"] == [
        {"id": "test", "list": utils_id.get_links(rss3_instance.account.address, "test", 1)},
        {"id": "test1", "list": utils_id.get_links(rss3_instance.account.address, "test1", 0)},
    ]
    result3 = await rss3_instance.links.get_list_file(rss3_instance.account.address, "test1", -1)
    assert result3["list"] == ["a", "b"]


@pytest.mark.asyncio
async def test_delete_list(mock):
    await rss3_instance.links.delete_list("test1")
    result = await rss3_instance.links.get_list(rss3_instance.account.address, "test1")
    assert result == []

    result2 = await rss3_instance.files.get()
    assert result2["links"] == [
        {"id": "test", "list": utils_id.get_links(rss3_instance.account.address, "test", 1)},
    ]


@pytest.mark.asyncio
async def test_patch_list_tags(mock):
    await rss3_instance.links.patch_list_tags("test", ["test1"])
    result = await rss3_instance.files.get()
    assert result["links"] == [
        {"id": "test", "list": utils_id.get_links(rss3_instance.account.address, "test", 1), "tags": ["test1"]},
    ]


# fixme: can not pass test
@pytest.mark.asyncio
async def test_post(mock):
    file = await rss3_instance.links.get_list_file(rss3_instance.account.address, "test")
    file = copy.deepcopy(file)
    file["signature"] = "0" * 132
    links = []
    i = 4
    while len(json.dumps(file)) < 1024:  # fixme: use config.file_size_limit
        new_link = str(i)
        file["list"].insert(0, new_link)
        links.append(new_link)
        i += 1

    for lk in links:
        await rss3_instance.links.post("test", lk)

    result = await rss3_instance.links.get_list_file(rss3_instance.account.address, "test", -1)
    assert result["id"] == utils_id.get_links(rss3_instance.account.address, "test", 2)
    last_list = await rss3_instance.links.get_list_file(rss3_instance.account.address, "test")
    assert last_list["id"] == utils_id.get_links(rss3_instance.account.address, "test", 2)
    assert len(last_list["list"]) == 1
