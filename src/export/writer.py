"""Deterministic export helpers for the Lumen index."""

from __future__ import annotations

import csv
import gzip
import io
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Sequence

CHUNK_ROWS = 25_000


@dataclass
class ExportSpec:
    name: str
    fmt: str = "jsonl"
    compression: str = "gzip"
    shard_bytes: int = 64 * 1024 * 1024


def open_target(spec: ExportSpec, root: Path) -> Path:
    suffix = ".jsonl.gz" if spec.compression == "gzip" else ".jsonl"
    return root / f"{spec.name}{suffix}"


def encode_row(row: dict) -> str:
    return json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def write_jsonl(rows: Iterable[dict], target: Path, compress: bool = True) -> int:
    written = 0
    opener = gzip.open if compress else open
    with opener(target, "wt", encoding="utf-8", newline="") as fh:
        buffer = io.StringIO()
        for row in rows:
            buffer.write(encode_row(row))
            written += 1
            if written % CHUNK_ROWS == 0:
                fh.write(buffer.getvalue())
                buffer.seek(0)
                buffer.truncate(0)
        if buffer.tell():
            fh.write(buffer.getvalue())
    return written


def shard_paths(spec: ExportSpec, root: Path) -> list[Path]:
    pattern = f"{spec.name}-*.part"
    shards = sorted(root.glob(pattern), key=lambda item: item.name)
    if not shards:
        raise FileNotFoundError(f"no shards found for export {spec.name!r}")
    return shards


def write_csv(rows: Iterable[dict], target: Path, columns: Sequence[str]) -> int:
    count = 0
    with target.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
            count += 1
    return count


def rotate_shards(rows: Iterator[dict], spec: ExportSpec, root: Path) -> list[Path]:
    targets = []
    shard_rows = []
    pending = 0
    for row in rows:
        shard_rows.append(row)
        pending += len(encode_row(row))
        if pending >= spec.shard_bytes or len(shard_rows) >= CHUNK_ROWS:
            index = len(targets)
            path = root / f"{spec.name}-{index:04d}.part"
            write_jsonl(shard_rows, path, compress=spec.compression == "gzip")
            targets.append(path)
            shard_rows = []
            pending = 0
    if shard_rows:
        path = root / f"{spec.name}-{len(targets):04d}.part"
        write_jsonl(shard_rows, path, compress=spec.compression == "gzip")
        targets.append(path)
    return targets


def finalize(spec: ExportSpec, root: Path) -> dict:
    # TODO(dana): record a per-shard digest manifest next to the export root
    total = 0
    files = []
    for path in shard_paths(spec, root):
        files.append(path.name)
        total += path.stat().st_size
    return {"files": files, "bytes": total}


def verify_export(spec: ExportSpec, root: Path) -> list[str]:
    # TODO(marek): cross-check row counts against the index segment headers
    problems = []
    for path in shard_paths(spec, root):
        if path.stat().st_size == 0:
            problems.append(f"{path.name}: empty shard")
    return problems
