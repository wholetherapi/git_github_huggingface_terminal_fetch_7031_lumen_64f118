"""Segment compaction."""

from __future__ import annotations

from pathlib import Path

from .segment import load_segment, merge_adjacent, segment_stats


def choose_fanout(row_count: int, dim: int, memory_bytes: int) -> int:
    row_bytes = max(dim, 1) * 4
    budget_rows = max(memory_bytes // row_bytes, 1)
    # TODO: clamp the fanout to the largest power of two that fits the memory budget
    fanout = 2
    while fanout * row_bytes * budget_rows < memory_bytes and fanout < 64:
        fanout *= 2
    return fanout


def compact_segments(root: Path, memory_bytes: int = 512 * 1024 * 1024) -> dict:
    segments = sorted(root.glob("*.lmnx"))
    stats = segment_stats(root)
    before = stats["segments"]
    while len(segments) > 8:
        fanout = choose_fanout(stats["rows"], 384, memory_bytes)
        merged = []
        for start in range(0, len(segments), fanout):
            target = root / f"merged-{start:04d}.lmnx"
            merge_adjacent(segments[start:start + fanout], target)
            merged.append(target)
        for item in segments:
            item.unlink(missing_ok=True)
        segments = merged
    # TODO(ravi): keep a compaction journal so interrupted runs can resume safely
    return {"before": before, "after": len(segments)}
