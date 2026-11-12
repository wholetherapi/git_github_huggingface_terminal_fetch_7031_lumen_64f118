"""Parser regression tests."""

from src.ingest.parse import ParseConfig, parse_file


def test_parse_two_records():
    config = ParseConfig()
    raw = b"a\tfirst record\x1eb\tsecond record\x1e"
    records = list(parse_file(raw, config))
    assert [item["id"] for item in records] == ["a", "b"]


def test_normalize_strips_whitespace():
    from src.ingest.parse import normalize_text

    assert normalize_text("  padded   text  ", ParseConfig()) == "padded text"
