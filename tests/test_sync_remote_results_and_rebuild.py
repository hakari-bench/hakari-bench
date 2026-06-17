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
    assert plan.duckdb_path == Path("output/clean-hf-results-duckdb/hakari-bench__results/hakari_bench.duckdb")
    assert plan.materialize_bm25_baseline_from_metadata is False
    assert plan.sync_backend == "git"


def test_resolve_plan_can_opt_into_metadata_backed_bm25_generation(tmp_path: Path) -> None:
    args = sync_rebuild.build_arg_parser().parse_args(
        [
            "--cache-root",
            str(tmp_path),
            "--materialize-bm25-baseline-from-metadata",
            "--bm25-dataset",
            "NanoBEIR-en",
        ]
    )

    plan = sync_rebuild.resolve_plan(args)

    assert plan.materialize_bm25_baseline_from_metadata is True
    assert plan.bm25_dataset == ["NanoBEIR-en"]


def test_resolve_plan_rejects_bm25_generation_options_without_opt_in(tmp_path: Path) -> None:
    args = sync_rebuild.build_arg_parser().parse_args(
        ["--cache-root", str(tmp_path), "--bm25-dataset", "NanoBEIR-en"]
    )

    with pytest.raises(ValueError, match="BM25 metadata materialization is disabled by default"):
        sync_rebuild.resolve_plan(args)


def test_legacy_no_bm25_baseline_flag_is_a_hidden_noop(tmp_path: Path) -> None:
    args = sync_rebuild.build_arg_parser().parse_args(["--cache-root", str(tmp_path), "--no-bm25-baseline"])

    plan = sync_rebuild.resolve_plan(args)

    assert plan.materialize_bm25_baseline_from_metadata is False


def test_resolve_plan_snapshot_backend_uses_separate_managed_cache(tmp_path: Path) -> None:
    args = sync_rebuild.build_arg_parser().parse_args(
        ["--cache-root", str(tmp_path), "--sync-backend", "snapshot"]
    )

    plan = sync_rebuild.resolve_plan(args)

    assert plan.sync_backend == "snapshot"
    assert plan.repo_dir == tmp_path / "hakari-bench__results__snapshot"
    assert plan.results_dir == plan.repo_dir / "hakari-results"
    assert plan.snapshot_clean is True
    assert plan.snapshot_max_workers == 32
    assert plan.xet_high_performance is True


def test_resolve_plan_xet_backend_uses_named_git_checkout_cache(tmp_path: Path) -> None:
    args = sync_rebuild.build_arg_parser().parse_args(["--cache-root", str(tmp_path), "--sync-backend", "xet"])

    plan = sync_rebuild.resolve_plan(args)

    assert plan.sync_backend == "xet"
    assert plan.repo_dir == tmp_path / "hakari-bench__results__xet"
    assert plan.results_dir == plan.repo_dir / "hakari-results"
    assert plan.duckdb_path == Path("output/clean-hf-results-duckdb/hakari-bench__results__xet/hakari_bench.duckdb")
    assert plan.xet_high_performance is True


def test_prepare_snapshot_local_dir_refuses_unmanaged_directory(tmp_path: Path) -> None:
    repo_dir = tmp_path / "snapshot"
    repo_dir.mkdir()
    (repo_dir / "keep.txt").write_text("local data\n", encoding="utf-8")

    with pytest.raises(RuntimeError, match="Refusing to clean non-managed snapshot directory"):
        sync_rebuild._prepare_snapshot_local_dir(repo_dir)

    assert (repo_dir / "keep.txt").exists()


def test_sync_snapshot_repo_downloads_results_with_xet_env(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    args = sync_rebuild.build_arg_parser().parse_args(
        ["--cache-root", str(tmp_path), "--sync-backend", "snapshot", "--revision", "abc123"]
    )
    plan = sync_rebuild.resolve_plan(args)
    calls: list[dict[str, object]] = []

    def fake_snapshot_download(**kwargs: object) -> str:
        calls.append(kwargs)
        plan.results_dir.mkdir(parents=True)
        (plan.results_dir / "sample.json.xz").write_bytes(b"placeholder")
        return str(plan.repo_dir)

    monkeypatch.delenv("HF_XET_HIGH_PERFORMANCE", raising=False)
    monkeypatch.setattr(sync_rebuild, "_ensure_hf_auth", lambda: None)
    monkeypatch.setitem(
        __import__("sys").modules,
        "huggingface_hub",
        type("FakeHuggingFaceHub", (), {"snapshot_download": fake_snapshot_download}),
    )

    sync_rebuild.sync_repo(plan)

    assert calls == [
        {
            "repo_id": "hakari-bench/results",
            "repo_type": "dataset",
            "revision": "abc123",
            "allow_patterns": ["hakari-results/**", "README.md"],
            "local_dir": plan.repo_dir,
            "token": True,
            "max_workers": 32,
        }
    ]
    assert (plan.repo_dir / sync_rebuild.SNAPSHOT_CACHE_MARKER).exists()
    assert __import__("os").environ["HF_XET_HIGH_PERFORMANCE"] == "1"


def test_sync_xet_repo_uses_git_checkout_with_git_xet_transfer(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    args = sync_rebuild.build_arg_parser().parse_args(
        ["--cache-root", str(tmp_path), "--sync-backend", "xet", "--revision", "main"]
    )
    plan = sync_rebuild.resolve_plan(args)
    (plan.repo_dir / ".git").mkdir(parents=True)
    calls: list[tuple[list[str], dict[str, str] | None]] = []

    def fake_run(command: list[str], env: dict[str, str] | None = None) -> None:
        calls.append((command, env))

    monkeypatch.delenv("HF_XET_HIGH_PERFORMANCE", raising=False)
    monkeypatch.setattr(sync_rebuild, "_ensure_hf_auth", lambda: None)
    monkeypatch.setattr(sync_rebuild, "_run", fake_run)

    sync_rebuild.sync_repo(plan)

    assert calls == [
        (
            sync_rebuild._git_command(["-C", str(plan.repo_dir), "fetch", "origin", "main"]),
            sync_rebuild.LFS_SKIP_SMUDGE_ENV,
        ),
        (
            sync_rebuild._git_command(["-C", str(plan.repo_dir), "reset", "--hard", "FETCH_HEAD"]),
            sync_rebuild.LFS_SKIP_SMUDGE_ENV,
        ),
        (["git", "xet", "install", "--local", "--path", str(plan.repo_dir)], sync_rebuild.XET_ENV),
        (sync_rebuild._git_command(["-C", str(plan.repo_dir), "clean", "-fdx"]), None),
        (
            sync_rebuild._git_command(
                ["-C", str(plan.repo_dir), "lfs", "pull", "--include", "hakari-results/**", "--exclude", ""]
            ),
            sync_rebuild.XET_ENV,
        ),
    ]


def test_sync_git_repo_resets_existing_checkout_to_clean_remote_revision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    args = sync_rebuild.build_arg_parser().parse_args(["--cache-root", str(tmp_path), "--revision", "main"])
    plan = sync_rebuild.resolve_plan(args)
    (plan.repo_dir / ".git").mkdir(parents=True)
    calls: list[tuple[list[str], dict[str, str] | None]] = []

    def fake_run(command: list[str], env: dict[str, str] | None = None) -> None:
        calls.append((command, env))

    monkeypatch.setattr(sync_rebuild, "_ensure_hf_auth", lambda: None)
    monkeypatch.setattr(sync_rebuild, "_run", fake_run)

    sync_rebuild.sync_repo(plan)

    assert calls == [
        (
            sync_rebuild._git_command(["-C", str(plan.repo_dir), "fetch", "origin", "main"]),
            sync_rebuild.LFS_SKIP_SMUDGE_ENV,
        ),
        (
            sync_rebuild._git_command(["-C", str(plan.repo_dir), "reset", "--hard", "FETCH_HEAD"]),
            sync_rebuild.LFS_SKIP_SMUDGE_ENV,
        ),
        (sync_rebuild._git_command(["-C", str(plan.repo_dir), "clean", "-fdx"]), None),
        (
            sync_rebuild._git_command(
                ["-C", str(plan.repo_dir), "lfs", "pull", "--include", "hakari-results/**", "--exclude", ""]
            ),
            None,
        ),
    ]


def test_sync_git_repo_skip_sync_does_not_clean_existing_checkout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    args = sync_rebuild.build_arg_parser().parse_args(["--cache-root", str(tmp_path), "--skip-git-sync"])
    plan = sync_rebuild.resolve_plan(args)
    calls: list[list[str]] = []

    monkeypatch.setattr(sync_rebuild, "_run", lambda command: calls.append(command))

    sync_rebuild.sync_repo(plan)

    assert calls == []


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
            "--materialize-bm25-baseline-from-metadata",
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
