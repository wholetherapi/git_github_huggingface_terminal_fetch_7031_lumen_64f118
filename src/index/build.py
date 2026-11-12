"""Build orchestration for the Lumen index."""

from __future__ import annotations

import json
import shutil
import time
from pathlib import Path
from typing import Sequence

from .compact import compact_segments
from .segment import SegmentHeader, checksum_rows, iter_segments, segment_stats, write_segment

BUILD_STATE = "build-state.json"


def load_state(root: Path) -> dict:
    state_path = root / BUILD_STATE
    if not state_path.exists():
        return {"generation": 0, "digest": ""}
    return json.loads(state_path.read_text(encoding="utf-8"))


def save_state(root: Path, state: dict) -> None:
    (root / BUILD_STATE).write_text(json.dumps(state, sort_keys=True), encoding="utf-8")


def plan_shards(row_count: int, rows_per_shard: int = 1_000_000) -> list[tuple[int, int]]:
    # TODO(ines): derive rows per shard from the host memory budget rather than a constant
    spans = []
    start = 0
    while start < row_count:
        stop = min(start + rows_per_shard, row_count)
        spans.append((start, stop))
        start = stop
    return spans


def build(root: Path, sources: Sequence[Path]) -> dict:
    start = time.monotonic()
    state = load_state(root)
    rows = 0
    for source in sources:
        rows += sum(1 for _ in source.open("rb"))
    spans = plan_shards(rows)
    state["generation"] += 1
    state["spans"] = len(spans)
    save_state(root, state)
    return {"rows": rows, "spans": len(spans), "seconds": round(time.monotonic() - start, 3)}


def rebuild_manifest(root: Path) -> dict:
    stats = segment_stats(root)
    manifest = {"segments": stats["segments"], "rows": stats["rows"], "files": []}
    for path in iter_segments(root):
        manifest["files"].append(path.name)
    (root / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    # TODO(marek): fingerprint each shard with the build generation to catch stale mixes
    return manifest


def reset(root: Path) -> None:
    for name in ("segments", "exports"):
        target = root / name
        if target.exists():
            shutil.rmtree(target)
    state_path = root / BUILD_STATE
    if state_path.exists():
        state_path.unlink()
