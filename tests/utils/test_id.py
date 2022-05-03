import math

from rss3.utils import id as id_

persona = "0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944"


def test_get_custom_item():
    expected = "0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944-item-custom-100"
    assert id_.get_custom_item(persona, 100) == expected


def test_get_auto_item():
    expected = "0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944-item-auto-100"
    assert id_.get_auto_item(persona, 100) == expected


def test_get_custom_items():
    expected = "0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944-list-items.custom-100"
    assert id_.get_custom_items(persona, 100) == expected


def test_get_auto_items():
    expected = "0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944-list-items.auto-100"
    assert id_.get_auto_items(persona, 100) == expected


def test_get_links():
    expected = "0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944-list-links.follow-100"
    assert id_.get_links(persona, "follow", 100) == expected


def test_get_backlinks():
    expected = "0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944-list-backlinks.follow-100"
    assert id_.get_backlinks(persona, "follow", 100) == expected


def test_get_custom_assets():
    expected = "0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944-list-assets.custom-100"
    assert id_.get_custom_assets(persona, 100) == expected


def test_get_auto_assets():
    expected = "0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944-list-assets.auto-100"
    assert id_.get_auto_assets(persona, 100) == expected


def test_get_item_backlinks():
    expected = (
        "0xC8b960D09C0078c18Dcbe7eB9AB9d816BcCa8944-list-item.10.backlinks.comment-100"
    )
    assert id_.get_item_backlinks(persona, "comment", 100, 10) == expected


def test_get_account():
    expected = "EVM+-0x1234567890123456789012345678901234567890"
    assert (
        id_.get_account("EVM+", "0x1234567890123456789012345678901234567890")
        == expected
    )


def test_get_asset():
    expected = "EVM+-0x1234567890123456789012345678901234567890-Ethereum.NFT-0xxxx"
    assert (
        id_.get_asset(
            "EVM+",
            "0x1234567890123456789012345678901234567890",
            "Ethereum.NFT",
            "0xxxx",
        )
        == expected
    )


def test_parse_account():
    expected = {
        "platform": "EVM+",
        "identity": "0x1234567890123456789012345678901234567890",
    }
    assert (
        id_.parse_account("EVM+-0x1234567890123456789012345678901234567890") == expected
    )


def test_parse_asset():
    expected = {
        "platform": "EVM+",
        "identity": "0x1234567890123456789012345678901234567890",
        "type": "Ethereum.NFT",
        "unique_id": "0xxxx",
    }
    assert (
        id_.parse_asset(
            "EVM+-0x1234567890123456789012345678901234567890-Ethereum.NFT-0xxxx"
        )
        == expected
    )


class TestParse:
    def test_parse_persona(self):
        expected = {
            "persona": persona,
            "type": "index",
            "index": math.inf,
        }
        assert id_.parse(persona) == expected

    def test_parse_custom_item(self):
        expected = {
            "persona": persona,
            "type": "item",
            "payload": ["custom"],
            "index": 100,
        }
        assert id_.parse(id_.get_custom_item(persona, 100)) == expected

    def test_parse_auto_item(self):
        expected = {
            "persona": persona,
            "type": "item",
            "payload": ["auto"],
            "index": 100,
        }
        assert id_.parse(id_.get_auto_item(persona, 100)) == expected

    def test_parse_custom_items(self):
        expected = {
            "persona": persona,
            "type": "list",
            "payload": ["items", "custom"],
            "index": 100,
        }
        assert id_.parse(id_.get_custom_items(persona, 100)) == expected

    def test_parse_auto_items(self):
        expected = {
            "persona": persona,
            "type": "list",
            "payload": ["items", "auto"],
            "index": 100,
        }
        assert id_.parse(id_.get_auto_items(persona, 100)) == expected

    def test_parse_links(self):
        expected = {
            "persona": persona,
            "type": "list",
            "payload": ["links", "follow"],
            "index": 100,
        }
        assert id_.parse(id_.get_links(persona, "follow", 100)) == expected
