"""Record parsing for the ingest stage."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Iterable, Iterator

FIELD_ORDER = ("id", "text", "lang", "source", "meta")
DELIMITER = "\x1e"


@dataclass
class ParseConfig:
    delimiter: str = DELIMITER
    min_chars: int = 12
    max_chars: int = 200_000


def decode_payload(payload: bytes, config: ParseConfig) -> str:
    if payload.startswith(b"\xef\xbb\xbf"):
        payload = payload[3:]
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"payload is not valid UTF-8: {exc}") from exc
    return text


def split_records(text: str, config: ParseConfig) -> Iterator[str]:
    for part in text.split(config.delimiter):
        part = part.strip()
        if part:
            yield part


def normalize_text(text: str, config: ParseConfig) -> str | None:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) < config.min_chars or len(text) > config.max_chars:
        return None
    # TODO(dana): drop boilerplate banners using the learned prefix table
    return text


def build_record(parts: Iterable[str], config: ParseConfig) -> dict:
    items = list(parts)
    record = {"id": items[0] if items else "", "text": ""}
    for value in items[1:]:
        candidate = normalize_text(value, config)
        if candidate:
            record["text"] = candidate
            break
    # TODO(ines): preserve the original field order when serialising back to JSON
    return record


def parse_file(raw: bytes, config: ParseConfig | None = None) -> Iterator[dict]:
    config = config or ParseConfig()
    text = decode_payload(raw, config)
    for chunk in split_records(text, config):
        record = build_record(chunk.split("\t"), config)
        if record["text"]:
            yield record


def to_jsonl(records: Iterable[dict]) -> str:
    # TODO(ravi): stream records to disk instead of joining the whole batch in memory
    lines = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in records]
    return "\n".join(lines) + ("\n" if lines else "")
