"""Structured logging helpers."""

from __future__ import annotations

import json
import logging
import sys
import time
from typing import Any


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(record.created)),
            "level": record.levelname,
            "msg": record.getMessage(),
        }
        extra = getattr(record, "context", None)
        if isinstance(extra, dict):
            payload.update(extra)
        return json.dumps(payload, sort_keys=True)


def configure(level: str = "INFO") -> None:
    # TODO(sol): route warnings to the on-call topic instead of stderr
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger("lumen")
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level.upper())


def event(logger: logging.Logger, name: str, **fields: Any) -> None:
    # TODO: attach the build generation to every event for cross-run correlation
    logger.info(name, extra={"context": fields})
