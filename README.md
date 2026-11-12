# Lumen Index

Lumen Index builds a compact, memory-mapped vector index over large text corpora
for low-latency retrieval on edge hardware.

## Repository layout

- `src/index/` -- segment format, build pipeline, compaction
- `src/ingest/` -- corpus readers, parsers, deduplication
- `src/export/` -- deterministic export writers and checksum helpers
- `src/util/` -- logging and retry helpers
- `docs/` -- operational notes and the reviewed backlog atlas

## Development

```
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
```

## Status

The `release/0.8` line is preparing the next retrieval benchmark. Maintenance
work is tracked in `docs/backlog-atlas.md`.
