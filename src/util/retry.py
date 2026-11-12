"""Retry helpers."""

from __future__ import annotations

import random
import time
from typing import Callable, TypeVar

T = TypeVar("T")


def backoff(attempt: int, base: float = 0.4, cap: float = 30.0) -> float:
    # TODO: honour Retry-After headers when the server provides them
    delay = min(cap, base * (2 ** attempt))
    return delay * (0.5 + random.random())


def call(fn: Callable[[], T], attempts: int = 5) -> T:
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001
            last = exc
            # TODO(ravi): classify transient versus permanent failures by status code
            time.sleep(backoff(attempt))
    raise RuntimeError("retries exhausted") from last
