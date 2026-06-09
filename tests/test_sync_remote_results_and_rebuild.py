from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import lzma

import pytest

from hakari_bench.results import read_result_json
from scripts import sync_remote_results_and_rebuild as sync_rebuild


def test_resolve_plan_defaults_to_cached_huggingface_results_repo(tmp_path: Path) -> None:
    args = sync_rebuild.build_arg_parser().parse_args(["--cache-root", str(tmp_path)])

    plan = sync_rebuild.resolve_plan(args)

    assert plan.repo_id == "hakari-bench/results"
    assert plan.repo_dir == tmp_path / "hakari-bench__results"
    assert plan.results_dir == tmp_path / "hakari-bench__results" / "hakari-results"
    assert plan.duckdb_path == plan.results_dir / "hakari_bench.duckdb"
    assert plan.include_bm25_baseline is True


def test_materialize_bm25_baseline_uses_task_metadata(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    args = sync_rebuild.build_arg_parser().parse_args(["--cache-root", str(tmp_path)])
    plan = sync_rebuild.resolve_plan(args)
    monkeypatch.setattr(
        sync_rebuild,
        "load_task_doc_bm25_metadata",
        lambda: {
            ("hakari-bench/NanoBEIR-en", "NanoArguAna"): {
                "bm25": {"ndcg_at_10": 0.25, "hit_at_10": 0.5, "source": "dataset_candidate_subset"},
                "candidate_subsets": {
                    "bm25": {
                        "config": "bm25",
                        "source": "dataset_candidate_subset",
                        "top_k": 500,
                        "ndcg_at_10": 0.25,
                        "hit_at_10": 0.5,
                        "recall_at_100": 0.75,
                    }
                },
            }
        },
    )
    plan = replace(plan, bm25_dataset=["NanoBEIR-en"], bm25_split=["NanoArguAna"])

    counts = sync_rebuild.materialize_bm25_baseline_from_metadata(plan)

    assert counts == {"written": 1, "skipped": 0, "missing": 0}
    output_path = plan.results_dir / "bm25" / "hakari-bench__NanoBEIR-en" / "arguana.json.xz"
    payload = read_result_json(output_path)
    assert payload["model"]["id"] == "bm25"
    assert payload["config"]["bm25"]["source"] == "dataset_candidate_subset"
    assert payload["evaluation"]["aggregate_metric_value"] == 0.25
    assert payload["task_metadata"]["candidate_subsets"]["bm25"]["recall_at_100"] == 0.75


def test_materialize_bm25_baseline_skips_existing_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    args = sync_rebuild.build_arg_parser().parse_args(
        [
            "--cache-root",
            str(tmp_path),
            "--bm25-dataset",
            "NanoBEIR-en",
            "--bm25-split",
            "NanoArguAna",
        ]
    )
    plan = sync_rebuild.resolve_plan(args)
    monkeypatch.setattr(
        sync_rebuild,
        "load_task_doc_bm25_metadata",
        lambda: {
            ("hakari-bench/NanoBEIR-en", "NanoArguAna"): {
                "candidate_subsets": {
                    "bm25": {
                        "config": "bm25",
                        "source": "dataset_candidate_subset",
                        "ndcg_at_10": 0.25,
                    }
                }
            }
        },
    )
    output_path = plan.results_dir / "bm25" / "hakari-bench__NanoBEIR-en" / "arguana.json.xz"
    output_path.parent.mkdir(parents=True)
    with lzma.open(output_path, "wt", encoding="utf-8") as file:
        file.write("{}\n")

    counts = sync_rebuild.materialize_bm25_baseline_from_metadata(plan)

    assert counts == {"written": 0, "skipped": 1, "missing": 0}


def test_rebuild_duckdb_command_points_at_cached_results(tmp_path: Path) -> None:
    args = sync_rebuild.build_arg_parser().parse_args(
        [
            "--cache-root",
            str(tmp_path),
            "--exclude-model-name",
            "bad/model",
            "--incremental",
        ]
    )
    plan = sync_rebuild.resolve_plan(args)

    command = sync_rebuild.rebuild_duckdb_command(plan)

    assert command[1].endswith("build_results_database_and_report.py")
    assert command[command.index("--results-dir") + 1] == str(plan.results_dir)
    assert command[command.index("--duckdb-path") + 1] == str(plan.duckdb_path)
    assert "--incremental" in command
    assert command[command.index("--exclude-model-name") + 1] == "bad/model"
