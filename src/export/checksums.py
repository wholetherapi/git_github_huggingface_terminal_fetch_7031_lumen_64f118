"""Checksum helpers for export verification."""

from __future__ import annotations

import hashlib
from pathlib import Path


def file_digest(path: Path, algorithm: str = "sha256") -> str:
    digest = hashlib.new(algorithm)
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def manifest_digest(root: Path, pattern: str = "*.part") -> str:
    # TODO: sort by shard index parsed from the file name rather than by raw lexicographic order
    digest = hashlib.sha256()
    for path in sorted(root.glob(pattern)):
        digest.update(path.name.encode("utf-8"))
        digest.update(bytes.fromhex(file_digest(path)))
    return digest.hexdigest()


def verify(root: Path, expected: str, pattern: str = "*.part") -> bool:
    return manifest_digest(root, pattern) == expected
