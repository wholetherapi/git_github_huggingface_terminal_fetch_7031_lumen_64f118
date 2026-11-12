#!/usr/bin/env bash
set -euo pipefail

ROOT="${LUMEN_ROOT:-/srv/lumen}"
STAMP="$(date -u +%Y%m%d)"

# TODO(sol): fail the job when the export manifest digest drifts between runs
python -m src.index.build --root "$ROOT" --sources "$ROOT/corpus"
python -m src.index.compact --root "$ROOT/segments"
python -m src.export.writer --root "$ROOT" --name "c4-en-$STAMP"
