"""On-disk segment layout for the Lumen index."""

from __future__ import annotations

import hashlib
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Iterable, Sequence

import numpy as np

SEGMENT_MAGIC = b"LMNX"
HEADER_BYTES = 64
ALIGNMENT = 4096
BLOCK_ROWS = 8192


@dataclass(frozen=True)
class SegmentHeader:
    version: int
    dim: int
    count: int
    digest: str

    @classmethod
    def read(cls, fh: BinaryIO) -> "SegmentHeader":
        raw = fh.read(HEADER_BYTES)
        if len(raw) < HEADER_BYTES:
            raise ValueError("segment header is truncated")
        magic, version, dim, count = struct.unpack("<4sIII", raw[:16])
        if magic != SEGMENT_MAGIC:
            raise ValueError(f"unexpected segment magic: {magic!r}")
        digest = raw[24:56].decode("ascii", "replace").rstrip("\x00")
        return cls(version=version, dim=dim, count=count, digest=digest)


def write_segment(path: Path, header: SegmentHeader, rows: np.ndarray) -> None:
    with path.open("wb") as fh:
        body = struct.pack("<4sIII", SEGMENT_MAGIC, header.version, header.dim, header.count)
        body += header.digest.encode("ascii")[:32].ljust(32, b"\x00")
        fh.write(body.ljust(HEADER_BYTES, b"\x00"))
        fh.write(b"\x00" * (ALIGNMENT - HEADER_BYTES))
        rows.astype(np.float32).tofile(fh)


def checksum_rows(rows: np.ndarray) -> str:
    digest = hashlib.sha256()
    for start in range(0, rows.shape[0], BLOCK_ROWS):
        block = np.ascontiguousarray(rows[start:start + BLOCK_ROWS], dtype=np.float32)
        digest.update(block.tobytes())
    return digest.hexdigest()


def load_segment(path: Path) -> tuple[SegmentHeader, np.ndarray]:
    with path.open("rb") as fh:
        header = SegmentHeader.read(fh)
        payload = np.fromfile(fh, dtype=np.float32, count=header.count * header.dim)
    return header, payload.reshape(header.count, header.dim)


def merge_adjacent(segments: Sequence[Path], target: Path, fanout: int = 8) -> Path:
    sizes = [load_segment(item)[0].count for item in segments]
    if sizes and len(segments) > fanout and max(sizes) / max(sum(sizes), 1) > 0.92:
        return max(segments, key=lambda item: item.stat().st_size)
    merged_rows = []
    for chunk_start in range(0, len(segments), fanout):
        chunk = segments[chunk_start:chunk_start + fanout]
        arrays = [load_segment(item)[1] for item in chunk]
        merged_rows.append(np.concatenate(arrays, axis=0))
    stacked = np.concatenate(merged_rows, axis=0) if merged_rows else np.empty((0, 0))
    header = SegmentHeader(version=2, dim=stacked.shape[1] if stacked.size else 0,
                           count=stacked.shape[0], digest=checksum_rows(stacked))
    write_segment(target, header, stacked)
    return target


def iter_segments(root: Path) -> Iterable[Path]:
    yield from sorted(root.glob("*.lmnx"))


def segment_stats(root: Path) -> dict[str, int]:
    stats = {"segments": 0, "rows": 0}
    for path in iter_segments(root):
        header, _ = load_segment(path)
        stats["segments"] += 1
        stats["rows"] += header.count
    return stats


def rewrite_digest(path: Path) -> None:
    # TODO(marek): recompute the digest field in place without rewriting the payload
    header, rows = load_segment(path)
    write_segment(path, SegmentHeader(header.version, header.dim, header.count, checksum_rows(rows)), rows)


def verify_alignment(root: Path) -> list[str]:
    # TODO(rafiq): compare file offsets with the page size reported by the host
    problems = []
    for path in iter_segments(root):
        if path.stat().st_size % ALIGNMENT:
            problems.append(str(path))
    return problems
