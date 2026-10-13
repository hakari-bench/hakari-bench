"""Persistent initial-view snapshots; arbitrary filters keep the dynamic path."""

from __future__ import annotations

from dataclasses import asdict
from functools import wraps
import hashlib
import inspect
import json
from pathlib import Path
import threading
from typing import Any, Callable, ParamSpec, TYPE_CHECKING, cast

import duckdb

from hakari_bench.viewer.observability import log_event

if TYPE_CHECKING:
    from hakari_bench.viewer.leaderboard import LeaderboardResult, LeaderboardService

P = ParamSpec("P")
_LOCK = threading.RLock()
SNAPSHOT_VERSION = 1
TABLE = "viewer_initial_snapshots"


def _fingerprint(service: LeaderboardService) -> str:
    config = service.config.model_dump(mode="json")
    config["task_manifests"] = {
        key: sorted(value) for key, value in config["task_manifests"].items()
    }
    payload = dict(
        version=SNAPSHOT_VERSION,
        config=config,
        models={
            key: asdict(value) for key, value in service.model_card_parameters.items()
        },
    )
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def _read(path: Path, key: str) -> str | None:
    if not path.exists():
        return None
    with duckdb.connect(str(path), read_only=True) as con:
        table = con.execute(
            "SELECT count(*) FROM information_schema.tables WHERE table_name = ?",
            [TABLE],
        ).fetchone()
        if not table or not table[0]:
            return None
        row = con.execute(
            "SELECT payload FROM viewer_initial_snapshots WHERE cache_key = ?", [key]
        ).fetchone()
        return str(row[0]) if row else None


def _write(path: Path, key: str, payload: str) -> None:
    with duckdb.connect(str(path)) as con:
        con.execute(
            "CREATE TABLE IF NOT EXISTS viewer_initial_snapshots (cache_key VARCHAR PRIMARY KEY, payload VARCHAR)"
        )
        con.execute(
            "INSERT OR REPLACE INTO viewer_initial_snapshots VALUES (?, ?)",
            [key, payload],
        )


def cached_initial_leaderboard(
    function: Callable[P, LeaderboardResult],
) -> Callable[P, LeaderboardResult]:
    signature = inspect.signature(function)
    defaults = {key: value.default for key, value in signature.parameters.items()}

    @wraps(function)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> LeaderboardResult:
        from hakari_bench.viewer.leaderboard import (
            LeaderboardResult,
            _promote_sorted_metric_column,
            sort_rows,
        )

        bound = signature.bind(*args, **kwargs)
        bound.apply_defaults()
        request = dict(bound.arguments)
        service = request.pop("self")
        view = request.pop("view_name")
        sort, direction = request.pop("sort"), request.pop("direction")
        allowed = {
            "score_target",
            "score_aggregation",
            "column_mode",
            "show_task_scores",
        }
        eligible = (
            service.use_precomputed
            and service.duckdb_path.exists()
            and bool(service.config.overalls)
            and view == service.config.overall.name
            and request["score_target"] in {"all", "reranking"}
            and (
                (
                    request["score_aggregation"] == "macro"
                    and request["column_mode"] == "grouped"
                    and request["show_task_scores"]
                )
                or (
                    request["score_aggregation"] == "micro"
                    and request["column_mode"] is None
                    and not request["show_task_scores"]
                )
            )
            and all(
                value == defaults[key]
                for key, value in request.items()
                if key not in allowed
            )
        )
        if not eligible:
            return function(*args, **kwargs)
        key = (
            _fingerprint(service)
            + ":"
            + json.dumps(dict(view=view, **request), sort_keys=True)
        )
        source = service.duckdb_path
        stat = source.stat()
        local_key = f"{stat.st_mtime_ns}:{stat.st_size}:{key}"
        companion = source.with_suffix(".leaderboard-cache.duckdb")
        with _LOCK:
            try:
                payload = _read(source, key) or _read(companion, local_key)
            except (duckdb.Error, OSError):
                payload = None
            log_event(
                "viewer.leaderboard.snapshot",
                hit=payload is not None,
                view=view,
                target=request["score_target"],
            )
            if payload is None:
                canonical = dict(bound.arguments, sort="borda_rank", direction="asc")
                result = cast(Callable[..., LeaderboardResult], function)(**canonical)
                payload = result.model_dump_json()
                try:
                    _write(companion, local_key, payload)
                except (duckdb.Error, OSError) as exc:
                    log_event(
                        "viewer.leaderboard.snapshot_write",
                        error_type=type(exc).__name__,
                    )
            result = LeaderboardResult.model_validate_json(payload)
        return result.model_copy(
            update={
                "rows": sort_rows(result.rows, sort=sort, direction=direction),
                "metric_columns": _promote_sorted_metric_column(
                    result.metric_columns, sort=sort
                ),
            }
        )

    return wrapped


def build_initial_snapshots(path: Path, config: Any) -> None:
    """Materialize both default tabs using exactly the dynamic calculation."""
    from hakari_bench.viewer.leaderboard import LeaderboardService

    if not config.overalls:
        return
    service = LeaderboardService(duckdb_path=path, config=config, use_precomputed=False)
    signature = inspect.signature(service.get_leaderboard)
    payloads = []
    for target in ("all", "reranking"):
        for grouped in (True, False):
            request: dict[str, Any] = dict(
                score_target=target,
                score_aggregation="macro" if grouped else "micro",
                column_mode="grouped" if grouped else None,
                show_task_scores=grouped,
            )
            bound = signature.bind(config.overall.name, **request)
            bound.apply_defaults()
            options = dict(bound.arguments)
            view = options.pop("view_name")
            options.pop("sort")
            options.pop("direction")
            key = (
                _fingerprint(service)
                + ":"
                + json.dumps(dict(view=view, **options), sort_keys=True)
            )
            result = service.get_leaderboard(view, **request)
            payloads.append((key, result.model_dump_json()))
    with duckdb.connect(str(path)) as con:
        con.execute("DROP TABLE IF EXISTS viewer_initial_snapshots")
    for key, payload in payloads:
        _write(path, key, payload)


def warm_initial_snapshots(store: Any, config: Any) -> None:
    """Prepare older downloaded DBs without changing the source database."""
    from hakari_bench.viewer.leaderboard import LeaderboardService, ScoreTarget

    try:
        store.wait_for_background_sync()
        if not store.path.exists():
            return
        service = LeaderboardService(duckdb_path=store.path, config=config)
        for target in ("all", "reranking"):
            service.get_leaderboard(
                config.overall.name,
                score_target=cast(ScoreTarget, target),
                score_aggregation="macro",
                column_mode="grouped",
                show_task_scores=True,
            )
            service.get_leaderboard(
                config.overall.name, score_target=cast(ScoreTarget, target)
            )
    except Exception as exc:
        log_event("viewer.leaderboard.snapshot_warmup", error_type=type(exc).__name__)
