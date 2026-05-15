from __future__ import annotations

import logging
from collections.abc import Iterator
from contextlib import contextmanager
from time import perf_counter
from typing import Any

LOGGER = logging.getLogger("hakari_bench.viewer")


@contextmanager
def timed_operation(event: str, **fields: Any) -> Iterator[dict[str, Any]]:
    """Log elapsed time for a viewer operation as stable key-value fields."""

    started = perf_counter()
    mutable_fields = dict(fields)
    try:
        yield mutable_fields
    except BaseException as exc:
        mutable_fields["status"] = "error"
        mutable_fields["error_type"] = type(exc).__name__
        raise
    else:
        mutable_fields.setdefault("status", "ok")
    finally:
        mutable_fields["elapsed_ms"] = round((perf_counter() - started) * 1000.0, 3)
        log_event(event, **mutable_fields)


def log_event(event: str, **fields: Any) -> None:
    LOGGER.info(
        "%s %s",
        event,
        " ".join(f"{key}={_format_value(value)}" for key, value in sorted(fields.items())),
        extra={"hakari_viewer_event": event, "hakari_viewer_fields": dict(fields)},
    )


def _format_value(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, (list, tuple, set)):
        return "[" + ",".join(_format_value(item) for item in value) + "]"
    return str(value).replace(" ", "_")
