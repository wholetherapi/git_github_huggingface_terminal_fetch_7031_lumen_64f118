"""Corpus readers for the ingest stage."""

from __future__ import annotations

import gzip
import io
import urllib.request
from pathlib import Path
from typing import Iterator


def open_stream(url: str, timeout: float = 60.0) -> io.BufferedIOBase:
    # TODO: support resumable downloads with HTTP range requests
    request = urllib.request.Request(url, headers={"User-Agent": "lumen-ingest/1.0"})
    return urllib.request.urlopen(request, timeout=timeout)


def iter_lines(stream: io.BufferedIOBase) -> Iterator[str]:
    for raw in stream:
        yield raw.decode("utf-8", "replace").rstrip("\n")


def fetch_to_path(url: str, target: Path, chunk: int = 1 << 20) -> int:
    total = 0
    with open_stream(url) as stream, target.open("wb") as fh:
        while True:
            block = stream.read(chunk)
            if not block:
                break
            fh.write(block)
            total += len(block)
    # TODO(ines): verify the published digest before marking the shard as complete
    return total


def open_maybe_gzip(path: Path) -> io.BufferedIOBase:
    raw = path.open("rb")
    magic = raw.read(2)
    raw.seek(0)
    if magic == b"\x1f\x8b":
        return gzip.GzipFile(fileobj=raw)
    return raw
