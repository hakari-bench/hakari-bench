from __future__ import annotations

import argparse
import json
import lzma
import os
import shutil
import shlex
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal, cast

from hakari_bench.datasets import DatasetRegistry, resolve_eval_tasks
from hakari_bench.results import existing_result_path_for_task, result_path_for_task


DEFAULT_RESULTS_REPO_ID = "hakari-bench/results"
DEFAULT_CACHE_ROOT = Path.home() / ".cache" / "hakari-bench" / "hf-datasets"
DEFAULT_RESULTS_SUBDIR = "hakari-results"
DEFAULT_DUCKDB_NAME = "hakari_bench.duckdb"
BM25_BASELINE_MODEL_ID = "bm25"
TASK_METADATA_ROOT = Path("task_docs/metadata")
EvaluationScopeChoice = Literal["standard", "all"]
SyncBackend = Literal["git", "snapshot"]
SNAPSHOT_CACHE_MARKER = ".hakari_bench_snapshot_cache"


@dataclass(frozen=True)
class SyncRebuildPlan:
    repo_id: str
    repo_dir: Path
    revision: str
    sync_backend: SyncBackend
    results_subdir: str
    results_dir: Path
    duckdb_path: Path
    skip_git_sync: bool
    skip_lfs_pull: bool
    snapshot_clean: bool
    snapshot_max_workers: int
    xet_high_performance: bool
    materialize_bm25_baseline_from_metadata: bool
    bm25_overwrite: bool
    bm25_evaluation_scope: EvaluationScopeChoice
    bm25_dataset: list[str]
    bm25_collection: list[str]
    bm25_split: list[str]
    overwrite_result_duplicates: bool
    incremental: bool
    include_retrieval_rankings: bool
    viewer_config_dir: Path
    model_cards_path: Path | None
    parquet_output_dir: Path | None
    exclude_model_names: list[str]


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Sync result JSON from the Hugging Face dataset repo and rebuild the viewer DuckDB. "
            "By default the DuckDB is built only from synced Hugging Face result JSON."
        )
    )
    parser.add_argument("--repo-id", default=DEFAULT_RESULTS_REPO_ID, help="Hugging Face dataset repo id.")
    parser.add_argument(
        "--sync-backend",
        choices=["git", "snapshot"],
        default="git",
        help=(
            "How to sync the Hugging Face dataset repo. 'git' uses a git/LFS checkout. "
            "'snapshot' uses huggingface_hub.snapshot_download(), which can use hf_xet."
        ),
    )
    parser.add_argument(
        "--cache-root",
        type=Path,
        default=DEFAULT_CACHE_ROOT,
        help="Root directory for cached Hugging Face dataset git checkouts.",
    )
    parser.add_argument(
        "--repo-dir",
        type=Path,
        default=None,
        help="Existing or desired checkout path. Defaults to CACHE_ROOT/{repo_id with / encoded as __}.",
    )
    parser.add_argument("--revision", default="main", help="Branch or revision to sync from.")
    parser.add_argument(
        "--results-subdir",
        default=DEFAULT_RESULTS_SUBDIR,
        help="Path inside the dataset repo containing HAKARI result JSON.",
    )
    parser.add_argument("--duckdb-path", type=Path, default=None, help="Output DuckDB path.")
    parser.add_argument(
        "--skip-git-sync",
        action="store_true",
        help="Reuse an existing git checkout or snapshot local directory without syncing.",
    )
    parser.add_argument("--skip-lfs-pull", action="store_true", help="Skip git lfs pull after syncing git metadata.")
    parser.add_argument(
        "--no-snapshot-clean",
        dest="snapshot_clean",
        action="store_false",
        help=(
            "Do not clear the managed snapshot local directory before downloading. "
            "The default avoids stale files after upstream deletions."
        ),
    )
    parser.set_defaults(snapshot_clean=True)
    parser.add_argument(
        "--snapshot-max-workers",
        type=int,
        default=32,
        help="Maximum parallel workers for huggingface_hub.snapshot_download().",
    )
    parser.add_argument(
        "--no-xet-high-performance",
        dest="xet_high_performance",
        action="store_false",
        help="Do not set HF_XET_HIGH_PERFORMANCE=1 for snapshot downloads.",
    )
    parser.set_defaults(xet_high_performance=True)
    bm25_materialization = parser.add_mutually_exclusive_group()
    bm25_materialization.add_argument(
        "--materialize-bm25-baseline-from-metadata",
        "--materialize-bm25-baseline",
        dest="materialize_bm25_baseline_from_metadata",
        action="store_true",
        default=False,
        help=(
            "Opt in to generating missing bm25/*.json.xz result files from local task_docs/metadata "
            "before rebuilding DuckDB. The default is off so builds use only synced Hugging Face result JSON."
        ),
    )
    bm25_materialization.add_argument(
        "--no-bm25-baseline",
        dest="materialize_bm25_baseline_from_metadata",
        action="store_false",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--bm25-overwrite",
        action="store_true",
        help=(
            "With --materialize-bm25-baseline-from-metadata, regenerate metadata-backed BM25 baseline JSON "
            "even when matching files already exist."
        ),
    )
    parser.add_argument(
        "--bm25-evaluation-scope",
        default="standard",
        choices=["standard", "all"],
        help="Evaluation scope for metadata-backed BM25 baseline generation.",
    )
    parser.add_argument(
        "--bm25-dataset",
        action="append",
        default=None,
        help="With --materialize-bm25-baseline-from-metadata, restrict BM25 generation to a dataset. May repeat.",
    )
    parser.add_argument(
        "--bm25-collection",
        action="append",
        default=None,
        help=(
            "With --materialize-bm25-baseline-from-metadata, restrict BM25 generation to a dataset collection. "
            "May repeat."
        ),
    )
    parser.add_argument(
        "--bm25-split",
        action="append",
        default=None,
        help="With --materialize-bm25-baseline-from-metadata, restrict BM25 generation to a split/task. May repeat.",
    )
    parser.add_argument("--overwrite-result-duplicates", action="store_true")
    parser.add_argument("--incremental", action="store_true")
    parser.add_argument("--include-retrieval-rankings", action="store_true")
    parser.add_argument("--viewer-config-dir", type=Path, default=Path("config/viewer"))
    parser.add_argument("--model-cards-path", type=Path, default=Path("config/model_cards"))
    parser.add_argument("--no-model-cards", action="store_true", help="Do not pass model cards to the DuckDB builder.")
    parser.add_argument("--parquet-output-dir", type=Path, default=None)
    parser.add_argument("--exclude-model-name", action="append", default=None)
    return parser


def resolve_plan(args: argparse.Namespace) -> SyncRebuildPlan:
    _validate_bm25_materialization_args(args)
    sync_backend = cast(SyncBackend, args.sync_backend)
    repo_dir = args.repo_dir or _default_repo_dir(args.cache_root, args.repo_id, sync_backend=sync_backend)
    results_dir = repo_dir / args.results_subdir
    duckdb_path = args.duckdb_path or results_dir / DEFAULT_DUCKDB_NAME
    return SyncRebuildPlan(
        repo_id=args.repo_id,
        repo_dir=repo_dir,
        revision=args.revision,
        sync_backend=sync_backend,
        results_subdir=args.results_subdir,
        results_dir=results_dir,
        duckdb_path=duckdb_path,
        skip_git_sync=args.skip_git_sync,
        skip_lfs_pull=args.skip_lfs_pull,
        snapshot_clean=args.snapshot_clean,
        snapshot_max_workers=max(1, args.snapshot_max_workers),
        xet_high_performance=args.xet_high_performance,
        materialize_bm25_baseline_from_metadata=args.materialize_bm25_baseline_from_metadata,
        bm25_overwrite=args.bm25_overwrite,
        bm25_evaluation_scope=cast(EvaluationScopeChoice, args.bm25_evaluation_scope),
        bm25_dataset=list(args.bm25_dataset or []),
        bm25_collection=list(args.bm25_collection or []),
        bm25_split=list(args.bm25_split or []),
        overwrite_result_duplicates=args.overwrite_result_duplicates,
        incremental=args.incremental,
        include_retrieval_rankings=args.include_retrieval_rankings,
        viewer_config_dir=args.viewer_config_dir,
        model_cards_path=None if args.no_model_cards else args.model_cards_path,
        parquet_output_dir=args.parquet_output_dir,
        exclude_model_names=list(args.exclude_model_name or []),
    )


def sync_repo(plan: SyncRebuildPlan) -> None:
    if plan.skip_git_sync:
        return
    _ensure_hf_auth()
    if plan.sync_backend == "snapshot":
        _sync_snapshot_repo(plan)
        return
    if (plan.repo_dir / ".git").is_dir():
        _run(_git_command(["-C", str(plan.repo_dir), "pull", "--ff-only", "origin", plan.revision]))
    else:
        plan.repo_dir.parent.mkdir(parents=True, exist_ok=True)
        _run(_git_command(["clone", _hf_dataset_git_url(plan.repo_id), str(plan.repo_dir)]))
        if plan.revision != "main":
            _run(_git_command(["-C", str(plan.repo_dir), "checkout", plan.revision]))
    if not plan.skip_lfs_pull:
        _run(_git_command(["-C", str(plan.repo_dir), "lfs", "pull"]))


def _sync_snapshot_repo(plan: SyncRebuildPlan) -> None:
    from huggingface_hub import snapshot_download

    if plan.xet_high_performance:
        os.environ.setdefault("HF_XET_HIGH_PERFORMANCE", "1")
    if plan.snapshot_clean:
        _prepare_snapshot_local_dir(plan.repo_dir)
    else:
        plan.repo_dir.mkdir(parents=True, exist_ok=True)

    allow_patterns = [f"{plan.results_subdir}/**", "README.md"]
    snapshot_download(
        repo_id=plan.repo_id,
        repo_type="dataset",
        revision=plan.revision,
        allow_patterns=allow_patterns,
        local_dir=plan.repo_dir,
        token=True,
        max_workers=plan.snapshot_max_workers,
    )
    _write_snapshot_marker(plan)


def _prepare_snapshot_local_dir(repo_dir: Path) -> None:
    if not repo_dir.exists():
        repo_dir.mkdir(parents=True, exist_ok=True)
        return
    marker = repo_dir / SNAPSHOT_CACHE_MARKER
    if not marker.exists():
        raise RuntimeError(
            f"Refusing to clean non-managed snapshot directory: {repo_dir}. "
            f"Remove it manually or create {marker.name} if this directory is disposable."
        )
    shutil.rmtree(repo_dir)
    repo_dir.mkdir(parents=True, exist_ok=True)


def _write_snapshot_marker(plan: SyncRebuildPlan) -> None:
    marker_payload = {
        "repo_id": plan.repo_id,
        "revision": plan.revision,
        "results_subdir": plan.results_subdir,
        "sync_backend": plan.sync_backend,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    (plan.repo_dir / SNAPSHOT_CACHE_MARKER).write_text(json.dumps(marker_payload, sort_keys=True) + "\n", encoding="utf-8")


def load_task_doc_bm25_metadata(metadata_root: Path = TASK_METADATA_ROOT) -> dict[tuple[str, str], dict[str, Any]]:
    metadata_by_task: dict[tuple[str, str], dict[str, Any]] = {}
    for path in sorted(metadata_root.rglob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        task_metadata = data.get("task_metadata")
        if not isinstance(task_metadata, dict):
            continue
        dataset_id = task_metadata.get("dataset_id")
        if not isinstance(dataset_id, str) or not dataset_id:
            continue
        for key_name in ("split_name", "task_name"):
            task_key = task_metadata.get(key_name)
            if isinstance(task_key, str) and task_key:
                metadata_by_task[(dataset_id, task_key)] = task_metadata
    return metadata_by_task


def materialize_bm25_baseline_from_metadata(plan: SyncRebuildPlan) -> dict[str, int]:
    registry = DatasetRegistry.load_builtin()
    tasks = resolve_eval_tasks(
        registry=registry,
        dataset_values=plan.bm25_dataset or registry.dataset_names(),
        collection_values=plan.bm25_collection,
        split_values=plan.bm25_split,
        evaluation_scope=plan.bm25_evaluation_scope,
    )
    metadata_by_task = load_task_doc_bm25_metadata()
    written = 0
    skipped = 0
    missing = 0
    for task in tasks:
        task_metadata = metadata_by_task.get((task.dataset_id, task.split_name)) or metadata_by_task.get(
            (task.dataset_id, task.task_name)
        )
        if task_metadata is None:
            missing += 1
            continue
        output_path = result_path_for_task(
            output_dir=plan.results_dir,
            model_id=BM25_BASELINE_MODEL_ID,
            task=task,
            result_format="json.xz",
        )
        if (
            not plan.bm25_overwrite
            and existing_result_path_for_task(
                output_dir=plan.results_dir,
                model_id=BM25_BASELINE_MODEL_ID,
                task=task,
                result_format="json.xz",
            )
            is not None
        ):
            skipped += 1
            continue
        payload = bm25_result_payload_from_task_metadata(task=task, task_metadata=task_metadata)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with lzma.open(output_path, "wt", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, sort_keys=True)
            file.write("\n")
        written += 1
    print(
        "BM25 baseline from task metadata: "
        f"written={written} skipped={skipped} missing_metadata={missing}",
        flush=True,
    )
    if missing:
        raise RuntimeError(f"Missing task_docs/metadata BM25 entries for {missing} task(s).")
    return {"written": written, "skipped": skipped, "missing": missing}


def bm25_result_payload_from_task_metadata(*, task: Any, task_metadata: dict[str, Any]) -> dict[str, Any]:
    candidate_subsets = task_metadata.get("candidate_subsets") if isinstance(task_metadata, dict) else None
    if not isinstance(candidate_subsets, dict):
        raise ValueError(f"Task metadata has no candidate_subsets mapping: {task.dataset_id} {task.split_name}")
    bm25_subset = candidate_subsets.get("bm25")
    if not isinstance(bm25_subset, dict):
        raise ValueError(f"Task metadata has no candidate_subsets.bm25: {task.dataset_id} {task.split_name}")
    ndcg_at_10 = _required_float(bm25_subset, "ndcg_at_10", task=task)
    hit_at_10 = _optional_float(bm25_subset, "hit_at_10")
    recall_at_100 = _optional_float(bm25_subset, "recall_at_100")
    generated_at = datetime.now(timezone.utc).isoformat()
    bm25_config = {
        "source": "dataset_candidate_subset",
        "backend": "dataset",
        "algorithm": "bm25",
        "candidate_subset_name": "bm25",
        "candidate_subset_metadata": bm25_subset,
    }
    metrics = {f"{task.evaluator_name}_bm25_dataset_subset_ndcg@10": ndcg_at_10}
    if hit_at_10 is not None:
        metrics[f"{task.evaluator_name}_bm25_dataset_subset_acc@10"] = hit_at_10
    if recall_at_100 is not None:
        metrics[f"{task.evaluator_name}_bm25_dataset_subset_recall@100"] = recall_at_100
    return {
        "generated_at_utc": generated_at,
        "model": {
            "id": BM25_BASELINE_MODEL_ID,
            "name": BM25_BASELINE_MODEL_ID,
            "model_type": "bm25",
            "backend_library": "dataset",
            "source": {"type": "bm25", "name": BM25_BASELINE_MODEL_ID},
            "bm25": bm25_config,
        },
        "environment": {
            "source": "task_docs/metadata",
            "package_versions": {},
        },
        "target": {
            "dataset_name": task.dataset_name,
            "dataset_id": task.dataset_id,
            "dataset_revision": None,
            "split_name": task.split_name,
            "task_name": task.task_name,
            "corpus_config": task.dataset.corpus_config,
            "queries_config": task.dataset.queries_config,
            "qrels_config": task.dataset.qrels_config,
            "candidate_config": task.dataset.candidate_config,
            "evaluation_scope": task.evaluation_scope.to_payload(),
        },
        "config": {
            "batch_size": None,
            "primary_metric": "ndcg@10",
            "show_progress": False,
            "candidate_ranking": "bm25",
            "rerank_top_k": None,
            "bm25": bm25_config,
        },
        "evaluation": {
            "dataset_load_seconds": 0.0,
            "evaluated_at_utc": generated_at,
            "started_at_utc": generated_at,
            "finished_at_utc": generated_at,
            "duration_seconds_excluding_dataset_load": 0.0,
            "duration_seconds_including_dataset_load": 0.0,
            "wall_seconds": 0.0,
            "aggregate_metric": "ndcg@10",
            "aggregate_metric_value": ndcg_at_10,
            "cache_hit": False,
            "timing": {"metric_compute_seconds": 0.0, "pure_compute_seconds": 0.0},
            "embedding_conversion": {},
            "embedding_evaluations": [],
            "rerank_aggregate_metric_value": None,
            "reranking_evaluations": [],
        },
        "metrics": metrics,
        "rerank_metrics": {},
        "task_metadata": {
            "bm25": task_metadata.get("bm25"),
            "candidate_subsets": {"bm25": bm25_subset},
        },
    }


def _required_float(mapping: dict[str, Any], key: str, *, task: Any) -> float:
    value = _optional_float(mapping, key)
    if value is None:
        raise ValueError(f"Task metadata has no numeric candidate_subsets.bm25.{key}: {task.dataset_id} {task.split_name}")
    return value


def _optional_float(mapping: dict[str, Any], key: str) -> float | None:
    value = mapping.get(key)
    if value is None:
        return None
    return float(value)


def rebuild_duckdb_command(plan: SyncRebuildPlan) -> list[str]:
    command = [
        sys.executable,
        str(Path(__file__).with_name("build_results_database_and_report.py")),
        "--results-dir",
        str(plan.results_dir),
        "--duckdb-path",
        str(plan.duckdb_path),
    ]
    if plan.overwrite_result_duplicates:
        command.append("--overwrite-result-duplicates")
    if plan.incremental:
        command.append("--incremental")
    if plan.include_retrieval_rankings:
        command.append("--include-retrieval-rankings")
    if plan.viewer_config_dir is not None:
        command.extend(["--viewer-config-dir", str(plan.viewer_config_dir)])
    if plan.model_cards_path is not None:
        command.extend(["--model-cards-path", str(plan.model_cards_path)])
    if plan.parquet_output_dir is not None:
        command.extend(["--parquet-output-dir", str(plan.parquet_output_dir)])
    for model_name in plan.exclude_model_names:
        command.extend(["--exclude-model-name", model_name])
    return command


def run_plan(plan: SyncRebuildPlan) -> None:
    sync_repo(plan)
    plan.results_dir.mkdir(parents=True, exist_ok=True)
    if plan.materialize_bm25_baseline_from_metadata:
        materialize_bm25_baseline_from_metadata(plan)
    _run(rebuild_duckdb_command(plan))


def _validate_bm25_materialization_args(args: argparse.Namespace) -> None:
    if args.materialize_bm25_baseline_from_metadata:
        return
    if (
        args.bm25_overwrite
        or args.bm25_evaluation_scope != "standard"
        or args.bm25_dataset
        or args.bm25_collection
        or args.bm25_split
    ):
        raise ValueError(
            "BM25 metadata materialization is disabled by default. "
            "Pass --materialize-bm25-baseline-from-metadata before using --bm25-* generation options."
        )


def _default_repo_dir(cache_root: Path, repo_id: str, *, sync_backend: SyncBackend = "git") -> Path:
    suffix = "" if sync_backend == "git" else "__snapshot"
    return cache_root / f"{repo_id.replace('/', '__')}{suffix}"


def _hf_dataset_git_url(repo_id: str) -> str:
    return f"https://huggingface.co/datasets/{repo_id}"


def _git_command(args: list[str]) -> list[str]:
    hf = shlex.quote(str(Path(sys.executable).with_name("hf")))
    helper = (
        "!f() { "
        "echo username=__token__; "
        f"echo password=$({hf} auth token); "
        "}; f"
    )
    return ["git", "-c", f"credential.helper={helper}", *args]


def _ensure_hf_auth() -> None:
    _run([str(Path(sys.executable).with_name("hf")), "auth", "whoami"])


def _run(command: list[str]) -> None:
    printable = " ".join(command)
    print(f"+ {printable}", flush=True)
    subprocess.run(command, check=True)


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()
    try:
        plan = resolve_plan(args)
    except ValueError as exc:
        parser.error(str(exc))
    run_plan(plan)


if __name__ == "__main__":
    main()
