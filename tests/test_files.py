import re
from datetime import datetime

import httpx
import pytest

from rss3 import RSS3, config

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
    assert new_file["signature"] == ""


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
    assert date_matcher.match(file["date_updated"]) is None
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
    ...


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
    assert date_matcher.match(file["date_updated"]) is None

    # File size is too large error
    rss3_fixture.files.clear_cache("", True)
    test_file["controller"] = "r" * config.file_size_limit

    with pytest.raises(Exception, match="File size is too large."):
        rss3_fixture.files.set(test_file)


def test_sync(respx_mock, rss3_fixture):
    ...
