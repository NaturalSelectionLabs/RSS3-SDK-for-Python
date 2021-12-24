import json
import re
from datetime import datetime

import httpx
import pytest

from rss3 import RSS3, config
from rss3.utils import id as utils_id

now = datetime.utcnow().isoformat(timespec="milliseconds") + "Z"
date_matcher = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$")


@pytest.fixture
def rss3_fixture():
    return RSS3({"endpoint": "https://test.io"})


def test_new(rss3_fixture):
    rss3_fixture.files.clear_cache("", True)

    new_file = rss3_fixture.files.new(rss3_fixture.account.address)
    assert new_file["id"] == rss3_fixture.account.address
    assert new_file["version"] == config.version
    assert date_matcher.match(new_file["date_created"]) is not None
    assert date_matcher.match(new_file["date_updated"]) is not None


@pytest.mark.asyncio
async def test_get_and_clear_cache(respx_mock, rss3_fixture):
    test_file = {
        "id": rss3_fixture.account.address,
        "version": config.version,
        "date_created": now,
        "date_updated": now,
    }

    respx_mock.get(f"https://test.io/{rss3_fixture.account.address}").mock(
        return_value=httpx.Response(200, json=test_file)
    )

    # Automatically generated file
    file = await rss3_fixture.files.get()
    assert file["id"] == rss3_fixture.account.address
    assert file["version"] == config.version
    assert date_matcher.match(file["date_created"]) is not None
    assert date_matcher.match(file["date_updated"]) is not None
    respx_mock.calls.assert_not_called()

    # Files obtained from the endpoint
    rss3_fixture.files.clear_cache("", True)
    resp_file = await rss3_fixture.files.get()
    assert resp_file == test_file
    respx_mock.calls.assert_called_once()

    # Files obtained from the cache
    assert await rss3_fixture.files.get() == test_file
    respx_mock.calls.assert_called_once()


@pytest.mark.asyncio
async def test_get_incorrectly_formatted_content_error(respx_mock, rss3_fixture):
    ...


@pytest.mark.asyncio
async def test_get_not_found_error(respx_mock, rss3_fixture):
    rss3_fixture.files.clear_cache("", True)
    respx_mock.get(f"https://test.io/{rss3_fixture.account.address}").mock(
        return_value=httpx.Response(
            400, json={"code": 5001, "message": "Persona not found error, Bad Request"}
        )
    )
    file = await rss3_fixture.files.get()
    assert file["id"] == rss3_fixture.account.address
    assert file["version"] == config.version
    assert date_matcher.match(file["date_created"]) is not None
    assert date_matcher.match(file["date_updated"]) is not None


@pytest.mark.asyncio
async def test_get_all(respx_mock, rss3_fixture):
    rss3_fixture.files.clear_cache("", True)

    resp1 = httpx.Response(
        200,
        json={
            "id": utils_id.get_custom_items(rss3_fixture.account.address, 1),
            "version": config.version,
            "date_created": now,
            "date_updated": now,
            "signature": "",
            "list": ["1", "2"],
            "list_next": utils_id.get_custom_items(rss3_fixture.account.address, 0),
        },
    )
    resp2 = httpx.Response(
        200,
        json={
            "id": utils_id.get_custom_items(rss3_fixture.account.address, 0),
            "version": config.version,
            "date_created": now,
            "date_updated": now,
            "signature": "",
            "list": ["3"],
        },
    )
    respx_mock.get(
        f"https://test.io/{utils_id.get_custom_items(rss3_fixture.account.address, 1)}"
    ).mock(return_value=resp1)
    respx_mock.get(
        f"https://test.io/{utils_id.get_custom_items(rss3_fixture.account.address, 0)}"
    ).mock(return_value=resp2)

    result = await rss3_fixture.files.get_all(
        utils_id.get_custom_items(rss3_fixture.account.address, 1)
    )
    assert result == ["1", "2", "3"]


@pytest.mark.asyncio
async def test_set(rss3_fixture):
    rss3_fixture.files.clear_cache("", True)

    test_id = "0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944"
    test_file = {
        "id": test_id,
        "version": config.version,
        "date_created": now,
        "date_updated": "",
        "signature": "",
    }
    rss3_fixture.files.set(test_file)

    file = await rss3_fixture.files.get(test_id)
    assert file["id"] == test_id
    assert file["version"] == config.version
    assert date_matcher.match(file["date_created"]) is not None
    assert date_matcher.match(file["date_updated"]) is not None

    # File size is too large error
    rss3_fixture.files.clear_cache("", True)
    test_file["controller"] = "r" * config.file_size_limit

    with pytest.raises(Exception, match="File size is too large."):
        rss3_fixture.files.set(test_file)


@pytest.mark.asyncio
async def test_sync(respx_mock, rss3_fixture):
    respx_mock.put(f"https://test.io").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": utils_id.get_custom_items(rss3_fixture.account.address, 0),
                "version": config.version,
                "date_created": now,
                "date_updated": now,
                "signature": "",
                "list": ["3"],
            },
        )
    )

    test_id = "0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944"
    test_file = {
        "id": test_id,
        "version": config.version,
        "date_created": now,
        "date_updated": "",
        "signature": "",
    }
    rss3_fixture.files.set(test_file)

    test_id2 = "0x8768515270aA67C624d3EA3B98CA464672C50183"
    test_file2 = {
        "id": test_id2,
        "version": config.version,
        "date_created": now,
        "date_updated": "",
        "signature": "",
    }
    rss3_fixture.files.set(test_file2)

    rss3_fixture.files.clear_cache(test_id)

    await rss3_fixture.files.sync()

    respx_mock.calls.assert_called_once()
    files = json.loads(respx_mock.calls.last.request.content.decode())["files"]

    file1 = files[0]
    assert file1["id"] == rss3_fixture.account.address
    assert date_matcher.match(file1["date_created"]) is not None
    assert date_matcher.match(file1["date_updated"]) is not None
    assert isinstance(file1["signature"], str)
    assert file1["version"] == config.version

    file2 = files[1]
    assert file2["id"] == test_id2
    assert date_matcher.match(file2["date_created"]) is not None
    assert date_matcher.match(file2["date_updated"]) is not None
    assert isinstance(file2["signature"], str)
    assert file2["version"] == config.version
