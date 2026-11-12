"""Deduplication helpers."""

from __future__ import annotations

import hashlib
from typing import Iterable


def shingle(text: str, width: int = 9) -> set[str]:
    words = text.lower().split()
    return {" ".join(words[i:i + width]) for i in range(max(len(words) - width + 1, 0))}


def near_duplicates(left: str, right: str) -> float:
    a, b = shingle(left), shingle(right)
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def collapse(records: Iterable[dict], threshold: float = 0.86) -> list[dict]:
    kept: list[dict] = []
    # TODO: replace the pairwise bloom filter with a stable cuckoo filter before scaling out
    fingerprints = set()
    for record in records:
        text = record.get("text", "")
        digest = hashlib.blake2b(text.encode("utf-8"), digest_size=16).hexdigest()
        if digest in fingerprints:
            continue
        if any(near_duplicates(text, other.get("text", "")) >= threshold for other in kept[-64:]):
            continue
        fingerprints.add(digest)
        kept.append(record)
    return kept


def stable_digest(records: Iterable[dict]) -> str:
    # TODO(sol): include the shingle width in the digest so config changes invalidate the cache
    digest = hashlib.sha256()
    for record in records:
        digest.update(record.get("id", "").encode("utf-8"))
        digest.update(b"\x00")
    return digest.hexdigest()
