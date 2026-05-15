from __future__ import annotations

import json
import math
import hashlib
from pathlib import Path

import duckdb
import pytest
from pydantic import ValidationError

from hakari_bench.viewer.config import BenchmarkConfig
from hakari_bench.warehouse_schema import (
    DatasetMetadataRow,
    MetricLongRow,
    RetrievalRankingRow,
    TaskDiagnosticRow,
    TaskResultRow,
)
from scripts import build_results_database_and_report as report


def test_nanomteb_japanese_is_a_ranked_benchmark() -> None:
    assert "NanoJMTEB-v2" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hakari-bench/NanoJMTEB-v2", "NanoJMTEB-v2") == "NanoJMTEB-v2"


def test_nanorteb_is_a_ranked_benchmark() -> None:
    assert "NanoRTEB" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hakari-bench/NanoRTEB", "NanoRTEB") == "NanoRTEB"


def test_nanolongembed_is_a_ranked_benchmark() -> None:
    assert "NanoLongEmbed" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hakari-bench/NanoLongEmbed", "NanoLongEmbed") == "NanoLongEmbed"


def test_nanocoir_is_a_ranked_benchmark() -> None:
    assert "NanoCoIR" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hakari-bench/NanoCoIR", "NanoCoIR") == "NanoCoIR"


def test_nanomteb_chinese_is_a_ranked_benchmark() -> None:
    assert "NanoCMTEB" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hakari-bench/NanoCMTEB", "NanoCMTEB") == "NanoCMTEB"


def test_new_nano_benchmarks_are_ranked_benchmarks() -> None:
    assert "NanoBIRCO" in report.TARGET_BENCHMARKS
    assert "NanoDAPFAM" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hakari-bench/NanoBIRCO", "NanoBIRCO") == "NanoBIRCO"
    assert report.benchmark_name("hakari-bench/NanoDAPFAM", "NanoDAPFAM") == "NanoDAPFAM"


def test_int_or_none_ignores_non_finite_numbers() -> None:
    assert report._int_or_none(math.inf) is None
    assert report._int_or_none(-math.inf) is None
    assert report._int_or_none(math.nan) is None


def test_language_specific_nanomteb_benchmarks_are_ranked_separately() -> None:
    language_benchmarks = [
        "NanoMTEB-Dutch",
        "NanoMTEB-French",
        "NanoMTEB-German",
        "NanoJMTEB-v2",
        "NanoMTEB-Korean",
        "NanoFaMTEB-v2",
        "NanoMTEB-Polish",
        "NanoRuMTEB",
        "NanoMTEB-Scandinavian",
        "NanoMTEB-Spanish",
        "NanoMTEB-Thai",
        "NanoVNMTEB",
        "NanoMTEB-Misc",
    ]

    for benchmark in language_benchmarks:
        assert benchmark in report.TARGET_BENCHMARKS
        assert report.benchmark_name(f"hakari-bench/{benchmark}", benchmark) == benchmark


def test_benchmark_name_uses_yaml_match_patterns_and_prefers_longest_match() -> None:
    benchmark_configs = [
        BenchmarkConfig(name="NanoMTEB", matches=["NanoMTEB"]),
        BenchmarkConfig(name="NanoMTEB-Dutch", matches=["NanoMTEB-Dutch"]),
        BenchmarkConfig(name="CustomBench", matches=["uploaded/custom-dataset"]),
        BenchmarkConfig(name="MNanoBEIR", matches=["NanoBEIR"]),
    ]

    assert (
        report.benchmark_name(
            "hakari-bench/NanoMTEB-Dutch",
            "NanoMTEB-Dutch",
            benchmark_configs=benchmark_configs,
        )
        == "NanoMTEB-Dutch"
    )
    assert (
        report.benchmark_name(
            "uploaded/custom-dataset",
            "arbitrary-name",
            benchmark_configs=benchmark_configs,
        )
        == "CustomBench"
    )
    assert (
        report.benchmark_name(
            "hakari-bench/NanoBEIR-en",
            "NanoBEIR-en",
            benchmark_configs=benchmark_configs,
        )
        == "MNanoBEIR"
    )


def test_load_results_uses_yaml_benchmark_matches(tmp_path: Path) -> None:
    model_dir = tmp_path / "model"
    task_path = model_dir / "uploaded__custom-dataset" / "task.json"
    task_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "target": {
                    "dataset_id": "uploaded/custom-dataset",
                    "dataset_name": "custom-name",
                    "task_name": "task",
                },
                "evaluation": {"aggregate_metric_value": 0.5},
            }
        ),
        encoding="utf-8",
    )

    rows, _, _, _, _, _ = report.load_results(
        tmp_path,
        benchmark_configs=[BenchmarkConfig(name="CustomBench", matches=["uploaded/custom-dataset"])],
    )

    assert len(rows) == 1
    assert rows[0].benchmark == "CustomBench"


def test_load_results_reads_task_json_as_source(tmp_path: Path) -> None:
    model_dir = tmp_path / "model"
    task_path = model_dir / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    task_path.parent.mkdir(parents=True)
    ranking_path = task_path.parent / "rankings" / "ja_cwir.top100.json"
    ranking_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "model": {
                    "id": "example/model",
                    "source": {
                        "type": "huggingface",
                        "name": "example/model",
                        "revision_requested": "main",
                        "revision": "model-sha",
                    },
                    "active_parameters": 3,
                    "total_parameters": 5,
                    "max_seq_length": 8192,
                    "dtype": "bf16",
                    "attn_implementation": "flash_attention_2",
                    "trust_remote_code": True,
                },
                "config": {
                    "query_prompt": "query: ",
                    "document_prompt": "passage: ",
                    "query_prompt_name": None,
                    "document_prompt_name": None,
                    "query_encode_task": None,
                    "document_encode_task": None,
                },
                "environment": {
                    "package_versions": {
                        "torch": "2.9.1",
                        "transformers": "4.57.6",
                        "sentence-transformers": "5.4.1",
                    }
                },
                "experiment_manifest": {"fingerprint_sha256": "abc123"},
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "dataset_revision": {
                        "requested": None,
                        "resolved": "dataset-sha",
                        "source": "huggingface_hub",
                    },
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "evaluation": {
                    "aggregate_metric": "ndcg@10",
                    "aggregate_metric_value": 0.42,
                    "evaluated_at_utc": "2026-04-29T00:00:00+00:00",
                },
                "metrics": {"ja_cwir_ndcg@10": 0.42},
                "artifacts": {
                    "top_rankings": {
                        "schema_version": 1,
                        "top_k": 100,
                        "path": "rankings/ja_cwir.top100.json",
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    ranking_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "top_k": 100,
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "rankings": [
                    {
                        "name": "base",
                        "ranking_kind": "retrieval",
                        "embedding_variant_name": None,
                        "distance": "dot",
                        "score_name": "dot",
                        "query_id": "q1",
                        "corpus_ids": ["d1", "d2"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    rows, _, metric_rows, diagnostic_rows, dataset_metadata_rows, ranking_rows = report.load_results(tmp_path)

    assert len(rows) == 1
    assert rows[0].benchmark == "NanoJMTEB-v2"
    assert rows[0].dataset_id == "hakari-bench/NanoJMTEB-v2"
    assert rows[0].dataset_name == "NanoJMTEB-v2"
    assert rows[0].score == 0.42
    assert rows[0].dataset_revision == "dataset-sha"
    assert rows[0].model_revision == "model-sha"
    assert rows[0].model_revision_requested == "main"
    assert rows[0].experiment_fingerprint == "abc123"
    assert rows[0].active_parameters == 3
    assert rows[0].total_parameters == 5
    assert rows[0].query_prompt == "query: "
    assert rows[0].document_prompt == "passage: "
    assert rows[0].trust_remote_code is True
    assert len(metric_rows) == 1
    assert len(diagnostic_rows) == 1
    assert diagnostic_rows[0].base_score == 0.42
    assert len(dataset_metadata_rows) == 1
    assert dataset_metadata_rows[0].language == "ja"
    assert dataset_metadata_rows[0].languages == ["ja"]
    assert dataset_metadata_rows[0].category == "natural_language"
    assert dataset_metadata_rows[0].reference_count is not None
    assert dataset_metadata_rows[0].query_count == 200
    assert [row.rank for row in ranking_rows] == [1, 2]
    assert ranking_rows[0].ranking_path == str(ranking_path)
    assert ranking_rows[0].query_id == "q1"
    assert ranking_rows[0].corpus_id == "d1"


def test_task_result_row_schema_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError, match="unexpected"):
        TaskResultRow.model_validate(
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "dataset_name": "NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "task_key": "NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
                "score": 0.42,
                "result_path": "result.json",
                "unexpected": True,
            }
        )


def test_load_results_allows_missing_model_revision_for_existing_results(tmp_path: Path) -> None:
    model_dir = tmp_path / "model"
    task_path = model_dir / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    task_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "evaluation": {"aggregate_metric": "ndcg@10", "aggregate_metric_value": 0.42},
                "metrics": {"ja_cwir_ndcg@10": 0.42},
            }
        ),
        encoding="utf-8",
    )

    rows, *_ = report.load_results(tmp_path)

    assert len(rows) == 1
    assert rows[0].model_revision is None
    assert rows[0].model_revision_requested is None


def test_metric_long_row_schema_exports_duckdb_values() -> None:
    row = MetricLongRow(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        task_name="ja_cwir",
        metric_name="ja_cwir_ndcg@10",
        metric_value=0.42,
        result_path="result.json",
    )

    assert row.duckdb_values() == (
        "model",
        "example/model",
        "NanoJMTEB-v2",
        "hakari-bench/NanoJMTEB-v2",
        "ja_cwir",
        "ja_cwir_ndcg@10",
        0.42,
        "result.json",
    )


def test_retrieval_ranking_row_schema_exports_duckdb_values() -> None:
    row = RetrievalRankingRow(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_revision="dataset-sha",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        result_path="result.json",
        ranking_path="rankings/ja_cwir.top100.json",
        ranking_name="base",
        ranking_kind="retrieval",
        embedding_variant_name=None,
        distance="dot",
        score_name="dot",
        query_id="q1",
        rank=1,
        corpus_id="d1",
    )

    assert row.duckdb_values() == (
        "model",
        "example/model",
        "NanoJMTEB-v2",
        "hakari-bench/NanoJMTEB-v2",
        "dataset-sha",
        "NanoJMTEB-v2",
        "ja_cwir",
        "ja_cwir",
        "NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        "result.json",
        "rankings/ja_cwir.top100.json",
        "base",
        "retrieval",
        None,
        "dot",
        "dot",
        "q1",
        1,
        "d1",
    )


def test_load_results_extracts_task_diagnostics(tmp_path: Path) -> None:
    task_dir = tmp_path / "model" / "hakari-bench__NanoJMTEB-v2"
    task_dir.mkdir(parents=True)
    (task_dir / "ja_cwir.json").write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "environment": {"package_versions": {}},
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "config": {
                    "candidate_ranking": "bm25",
                    "rerank_top_k": 100,
                    "bm25": {"source": "dataset_candidate_subset"},
                },
                "evaluation": {
                    "aggregate_metric": "ndcg@10",
                    "aggregate_metric_value": 0.42,
                    "rerank_aggregate_metric_value": 0.50,
                    "dataset_load_seconds": 0.25,
                    "wall_seconds": 2.0,
                    "duration_seconds_including_dataset_load": 2.25,
                    "timing": {
                        "query_embedding_seconds": 0.5,
                        "corpus_embedding_seconds": 1.0,
                        "score_and_topk_seconds": 0.3,
                        "metric_compute_seconds": 0.2,
                        "pure_compute_seconds": 2.0,
                    },
                    "reranking_evaluations": [
                        {
                            "source": "dataset_candidate_subset",
                            "status": "available",
                            "candidate_coverage": {
                                "query_coverage": 0.75,
                                "relevant_coverage": 0.60,
                                "covered_query_count": 3,
                                "query_with_relevance_count": 4,
                                "covered_relevant_count": 6,
                                "relevant_count": 10,
                            },
                        }
                    ],
                },
                "metrics": {"ja_cwir_ndcg@10": 0.42},
            }
        ),
        encoding="utf-8",
    )

    _, _, _, diagnostic_rows, _, _ = report.load_results(tmp_path)

    assert len(diagnostic_rows) == 1
    row = diagnostic_rows[0]
    assert row.rerank_lift == pytest.approx(0.08)
    assert row.candidate_ranking == "bm25"
    assert row.bm25_source == "dataset_candidate_subset"
    assert row.query_coverage == 0.75
    assert row.relevant_coverage == 0.60
    assert row.score_and_topk_seconds == 0.3


def test_load_results_builds_runs_from_task_json(tmp_path: Path) -> None:
    task_dir = tmp_path / "local__model_A" / "hakari-bench__NanoJMTEB-v2"
    task_dir.mkdir(parents=True)
    (task_dir / "ja_cwir.json").write_text(
        json.dumps(
            {
                "generated_at_utc": "2026-05-04T00:00:00+00:00",
                "model": {
                    "id": "local/model_A",
                    "active_parameters": 3,
                    "total_parameters": 5,
                    "max_seq_length": 8192,
                    "dtype": "bf16",
                    "attn_implementation": "flash_attention_2",
                },
                "environment": {
                    "package_versions": {
                        "torch": "2.9.1",
                        "transformers": "4.57.6",
                        "sentence-transformers": "5.4.1",
                    }
                },
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "evaluation": {
                    "aggregate_metric": "ndcg@10",
                    "aggregate_metric_value": 0.42,
                    "started_at_utc": "2026-05-04T00:00:01+00:00",
                    "finished_at_utc": "2026-05-04T00:00:03+00:00",
                },
                "metrics": {"ja_cwir_ndcg@10": 0.42},
            }
        ),
        encoding="utf-8",
    )

    rows, runs, _, _, _, _ = report.load_results(tmp_path)

    assert len(rows) == 1
    assert runs == [
        {
            "model_dir": "local__model_A",
            "model_name": "local/model_A",
            "generated_at_utc": "2026-05-04T00:00:00+00:00",
            "started_at_utc": "2026-05-04T00:00:01+00:00",
            "finished_at_utc": "2026-05-04T00:00:03+00:00",
            "target_count": 1,
            "split_count": 1,
            "cache_hit_count": None,
            "evaluated_count": None,
            "aggregate_metric_mean": 0.42,
            "active_parameters": 3,
            "total_parameters": 5,
            "max_seq_length": 8192,
            "dtype": "bf16",
            "attn_implementation": "flash_attention_2",
            "torch_version": "2.9.1",
            "transformers_version": "4.57.6",
            "sentence_transformers_version": "5.4.1",
        }
    ]


def test_render_html_includes_total_parameters_column() -> None:
    html = report.render_html(data_json=json.dumps({"views": {}, "summary": {"skipped": []}}))

    assert "Total Params" in html


def test_load_results_adds_embedding_variant_rows(tmp_path: Path) -> None:
    model_dir = tmp_path / "model"
    task_path = model_dir / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    task_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "environment": {"package_versions": {}},
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "evaluation": {"aggregate_metric": "ndcg@10", "aggregate_metric_value": 0.42},
                "embedding_evaluations": [
                    {
                        "name": "base",
                        "aggregate_metric": "ndcg@10",
                        "aggregate_metric_value": 0.42,
                        "embedding_dimensions": {"dim": 768},
                    },
                    {
                        "name": "truncate_dim_512_quantize_uint8_docs",
                        "aggregate_metric": "ndcg@10",
                        "aggregate_metric_value": 0.40,
                        "embedding_dimensions": {"dim": 512},
                        "embedding_metadata": {
                            "corpus": {
                                "quantization": {
                                    "precision": "uint8",
                                    "original_dim": 512,
                                    "stored_dim": 512,
                                }
                            }
                        },
                    },
                ],
                "metrics": {"ja_cwir_ndcg@10": 0.42},
            }
        ),
        encoding="utf-8",
    )
    rows, _, _, _, _, _ = report.load_results(tmp_path)

    assert [(row.embedding_variant_name, row.score, row.embedding_dim, row.quantization) for row in rows] == [
        (None, 0.42, 768, None),
        ("truncate_dim_512_quantize_uint8_docs", 0.40, 512, "uint8"),
    ]


def test_write_duckdb_persists_dataset_revision(tmp_path: Path) -> None:
    row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_revision="dataset-sha",
        dataset_revision_requested="main",
        model_revision="model-sha",
        model_revision_requested="main",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path="result.json",
        active_parameters=3,
        total_parameters=5,
        max_seq_length=8192,
        dtype="bf16",
        attn_implementation="flash_attention_2",
        query_prompt="query: ",
        document_prompt="passage: ",
        query_prompt_name=None,
        document_prompt_name=None,
        query_encode_task=None,
        document_encode_task=None,
        trust_remote_code=True,
        torch_version="2.9.1",
        transformers_version="4.57.6",
        sentence_transformers_version="5.4.1",
        started_at_utc=None,
        finished_at_utc=None,
        evaluated_at_utc=None,
        duration_seconds_including_dataset_load=None,
        wall_seconds=None,
    )
    standings, borda_rows = report.compute_standings([row])
    db_path = tmp_path / "results.duckdb"

    report.write_duckdb(
        db_path,
        runs=[
            {
                "model_dir": "model",
                "model_name": "example/model",
            }
        ],
        rows=[row],
        metric_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_ndcg@10",
                "metric_value": 0.42,
                "result_path": "result.json",
            }
        ],
        ranking_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "dataset_revision": "dataset-sha",
                "dataset_name": "NanoJMTEB-v2",
                "split_name": "ja_cwir",
                "task_name": "ja_cwir",
                "task_key": "NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
                "result_path": "result.json",
                "ranking_path": "rankings/ja_cwir.top100.json",
                "ranking_name": "base",
                "ranking_kind": "retrieval",
                "embedding_variant_name": None,
                "distance": "dot",
                "score_name": "dot",
                "query_id": "q1",
                "rank": 1,
                "corpus_id": "d1",
            }
        ],
        standings=standings,
        borda_rows=borda_rows,
    )

    con = duckdb.connect(str(db_path))
    try:
        run_columns = [row[1] for row in con.execute("PRAGMA table_info('runs')").fetchall()]
        assert run_columns == [
            "model_dir",
            "model_name",
            "generated_at_utc",
            "started_at_utc",
            "finished_at_utc",
            "target_count",
            "split_count",
            "cache_hit_count",
            "evaluated_count",
            "aggregate_metric_mean",
            "active_parameters",
            "total_parameters",
            "max_seq_length",
            "dtype",
            "attn_implementation",
            "torch_version",
            "transformers_version",
            "sentence_transformers_version",
        ]
        assert con.execute(
            "SELECT dataset_revision, dataset_revision_requested, model_revision, model_revision_requested FROM task_results"
        ).fetchone() == ("dataset-sha", "main", "model-sha", "main")
        assert con.execute(
            """
            SELECT query_prompt, document_prompt, query_prompt_name, document_prompt_name,
                   query_encode_task, document_encode_task, trust_remote_code
            FROM task_results
            """
        ).fetchone() == ("query: ", "passage: ", None, None, None, None, True)
        assert con.execute(
            """
            SELECT model_name, benchmark, task_key, score, language, languages
            FROM viewer_task_results
            """
        ).fetchone() == ("example/model", "NanoJMTEB-v2", "NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir", 0.42, None, None)
        assert con.execute("SELECT base_score FROM task_diagnostics").fetchone() is None
        assert con.execute("SELECT query_id, rank, corpus_id FROM retrieval_rankings").fetchone() == ("q1", 1, "d1")
    finally:
        con.close()


def test_write_duckdb_materializes_task_score_targets(tmp_path: Path) -> None:
    row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path="result.json",
    )
    diagnostic_row = TaskDiagnosticRow(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        result_path="result.json",
        base_score=0.42,
        rerank_score=0.50,
        rerank_lift=0.08,
        rerank_status="available",
        rerank_top_k=100,
        candidate_source="dataset_candidate_subset",
        candidate_ranking="bm25",
    )
    standings, borda_rows = report.compute_standings([row])
    db_path = tmp_path / "results.duckdb"

    report.write_duckdb(
        db_path,
        runs=[{"model_dir": "model", "model_name": "example/model"}],
        rows=[row],
        metric_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_ndcg@10",
                "metric_value": 0.42,
                "result_path": "result.json",
            }
        ],
        diagnostic_rows=[diagnostic_row],
        standings=standings,
        borda_rows=borda_rows,
    )

    con = duckdb.connect(str(db_path))
    try:
        assert con.execute(
            """
            SELECT score_target, score, candidate_ranking, rerank_top_k, embedding_variant_name
            FROM fact_task_score
            ORDER BY score_target
            """
        ).fetchall() == [
            ("all", 0.42, None, None, None),
            ("reranking", 0.50, "bm25", 100, None),
        ]
        assert con.execute(
            """
            SELECT score_target, score
            FROM viewer_task_results
            ORDER BY score_target
            """
        ).fetchall() == [("all", 0.42), ("reranking", 0.50)]
    finally:
        con.close()


def test_write_duckdb_materializes_canonical_dimensions(tmp_path: Path) -> None:
    base_row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path="result.json",
        active_parameters=3,
        total_parameters=5,
        max_seq_length=8192,
        dtype="bf16",
        embedding_dim=768,
    )
    variant_row = base_row.model_copy(
        update={
            "score": 0.40,
            "embedding_variant_name": "truncate_dim_512_quantize_uint8_docs",
            "embedding_dim": 512,
            "quantization": "uint8",
        }
    )
    metadata_row = DatasetMetadataRow(
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        language="ja",
        languages=["ja"],
        category="natural_language",
        query_count=200,
        document_count=500,
    )
    standings, borda_rows = report.compute_standings([base_row])
    db_path = tmp_path / "results.duckdb"

    report.write_duckdb(
        db_path,
        runs=[{"model_dir": "model", "model_name": "example/model"}],
        rows=[base_row, variant_row],
        metric_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_ndcg@10",
                "metric_value": 0.42,
                "result_path": "result.json",
            }
        ],
        dataset_metadata_rows=[metadata_row],
        standings=standings,
        borda_rows=borda_rows,
    )

    con = duckdb.connect(str(db_path))
    try:
        assert con.execute(
            "SELECT model_id, model_dir, model_name, active_parameters, total_parameters FROM dim_model"
        ).fetchall() == [(1, "model", "example/model", 3, 5)]
        assert con.execute(
            """
            SELECT task_id, benchmark, dataset_id, task_key, language, category, query_count, document_count
            FROM dim_task
            """
        ).fetchall() == [
            (
                1,
                "NanoJMTEB-v2",
                "hakari-bench/NanoJMTEB-v2",
                "NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
                "ja",
                "natural_language",
                200,
                500,
            )
        ]
        assert con.execute(
            """
            SELECT variant_id, variant_key, embedding_variant_name, embedding_dim, quantization, is_base
            FROM dim_variant
            ORDER BY variant_id
            """
        ).fetchall() == [
            (1, "base:768:none", None, 768, None, True),
            (
                2,
                "truncate_dim_512_quantize_uint8_docs:512:uint8",
                "truncate_dim_512_quantize_uint8_docs",
                512,
                "uint8",
                False,
            ),
        ]
    finally:
        con.close()


def test_write_duckdb_records_source_load_state_and_changed_count(tmp_path: Path) -> None:
    result_path = tmp_path / "model" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    result_path.parent.mkdir(parents=True)
    result_path.write_text('{"score": 0.42}', encoding="utf-8")
    row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path=str(result_path),
    )
    standings, borda_rows = report.compute_standings([row])
    db_path = tmp_path / "results.duckdb"

    def write_once() -> None:
        report.write_duckdb(
            db_path,
            runs=[{"model_dir": "model", "model_name": "example/model"}],
            rows=[row],
            metric_rows=[
                {
                    "model_dir": "model",
                    "model_name": "example/model",
                    "benchmark": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "task_name": "ja_cwir",
                    "metric_name": "ja_cwir_ndcg@10",
                    "metric_value": 0.42,
                    "result_path": str(result_path),
                }
            ],
            standings=standings,
            borda_rows=borda_rows,
            batch_id="test-batch",
            loaded_at_utc="2026-05-15T00:00:00+00:00",
        )

    write_once()
    expected_hash = hashlib.sha256(result_path.read_bytes()).hexdigest()
    con = duckdb.connect(str(db_path))
    try:
        assert con.execute(
            "SELECT result_path, payload_sha256, last_successful_batch_id FROM source_load_state"
        ).fetchall() == [(str(result_path), expected_hash, "test-batch")]
        assert con.execute("SELECT source_count, changed_count FROM ingestion_batches").fetchone() == (1, 1)
    finally:
        con.close()

    write_once()
    con = duckdb.connect(str(db_path))
    try:
        assert con.execute("SELECT source_count, changed_count FROM ingestion_batches").fetchone() == (1, 0)
    finally:
        con.close()


def test_write_duckdb_records_schema_metadata_and_result_extensions(tmp_path: Path) -> None:
    result_path = tmp_path / "model" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    result_path.parent.mkdir(parents=True)
    result_path.write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "target": {"dataset_id": "hakari-bench/NanoJMTEB-v2"},
                "evaluation": {"aggregate_metric_value": 0.42},
                "future_payload": {"kept": True},
            }
        ),
        encoding="utf-8",
    )
    row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path=str(result_path),
    )
    standings, borda_rows = report.compute_standings([row])
    db_path = tmp_path / "results.duckdb"

    report.write_duckdb(
        db_path,
        runs=[{"model_dir": "model", "model_name": "example/model"}],
        rows=[row],
        metric_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_ndcg@10",
                "metric_value": 0.42,
                "result_path": str(result_path),
            }
        ],
        standings=standings,
        borda_rows=borda_rows,
        batch_id="schema-test",
        loaded_at_utc="2026-05-15T00:00:00+00:00",
    )

    con = duckdb.connect(str(db_path))
    try:
        assert con.execute("SELECT schema_version, compatibility_level FROM meta_database").fetchone() == (
            report.WAREHOUSE_SCHEMA_VERSION,
            "v1-compatible",
        )
        assert con.execute("SELECT schema_version, migration_name FROM schema_change_log").fetchone() == (
            report.WAREHOUSE_SCHEMA_VERSION,
            "create_current_warehouse_schema",
        )
        assert con.execute(
            "SELECT result_path, field_path, value_json, discovered_batch_id FROM result_extensions"
        ).fetchall() == [
            (str(result_path), "$.future_payload", '{"kept":true}', "schema-test"),
        ]
    finally:
        con.close()


def test_write_duckdb_materializes_metric_dimension_and_fact(tmp_path: Path) -> None:
    row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path="result.json",
    )
    standings, borda_rows = report.compute_standings([row])
    db_path = tmp_path / "results.duckdb"

    report.write_duckdb(
        db_path,
        runs=[{"model_dir": "model", "model_name": "example/model"}],
        rows=[row],
        metric_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_ndcg@10",
                "metric_value": 0.42,
                "result_path": "result.json",
            },
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_recall@100",
                "metric_value": 0.80,
                "result_path": "result.json",
            },
        ],
        standings=standings,
        borda_rows=borda_rows,
    )

    con = duckdb.connect(str(db_path))
    try:
        assert con.execute(
            "SELECT metric_id, metric_name, metric_family, cutoff FROM dim_metric ORDER BY metric_id"
        ).fetchall() == [
            (1, "ja_cwir_ndcg@10", "ndcg", 10),
            (2, "ja_cwir_recall@100", "recall", 100),
        ]
        assert con.execute(
            """
            SELECT metric_id, model_name, benchmark, task_name, metric_value
            FROM fact_metric_score
            ORDER BY metric_id
            """
        ).fetchall() == [
            (1, "example/model", "NanoJMTEB-v2", "ja_cwir", 0.42),
            (2, "example/model", "NanoJMTEB-v2", "ja_cwir", 0.80),
        ]
    finally:
        con.close()


def test_export_duckdb_tables_to_parquet_writes_canonical_tables(tmp_path: Path) -> None:
    row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_revision=None,
        dataset_revision_requested=None,
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path="result.json",
        active_parameters=None,
        total_parameters=None,
        max_seq_length=None,
        dtype=None,
        attn_implementation=None,
        query_prompt=None,
        document_prompt=None,
        query_prompt_name=None,
        document_prompt_name=None,
        query_encode_task=None,
        document_encode_task=None,
        trust_remote_code=None,
        torch_version=None,
        transformers_version=None,
        sentence_transformers_version=None,
        started_at_utc=None,
        finished_at_utc=None,
        evaluated_at_utc=None,
        duration_seconds_including_dataset_load=None,
        wall_seconds=None,
    )
    standings, borda_rows = report.compute_standings([row])
    db_path = tmp_path / "results.duckdb"
    parquet_dir = tmp_path / "parquet"
    report.write_duckdb(
        db_path,
        runs=[{"model_dir": "model", "model_name": "example/model"}],
        rows=[row],
        metric_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_ndcg@10",
                "metric_value": 0.42,
                "result_path": "result.json",
            }
        ],
        standings=standings,
        borda_rows=borda_rows,
    )

    report.export_duckdb_tables_to_parquet(db_path, parquet_dir)

    assert sorted(path.name for path in parquet_dir.glob("*.parquet")) == [
        "borda_task_scores.parquet",
        "dataset_metadata.parquet",
        "dim_metric.parquet",
        "dim_model.parquet",
        "dim_task.parquet",
        "dim_variant.parquet",
        "fact_metric_score.parquet",
        "fact_task_score.parquet",
        "ingestion_batches.parquet",
        "meta_database.parquet",
        "metrics_long.parquet",
        "model_scores.parquet",
        "result_extensions.parquet",
        "retrieval_rankings.parquet",
        "runs.parquet",
        "schema_change_log.parquet",
        "source_load_state.parquet",
        "task_diagnostics.parquet",
        "task_results.parquet",
        "viewer_task_results.parquet",
    ]
    con = duckdb.connect()
    try:
        assert con.execute(f"SELECT model_name, score FROM read_parquet('{parquet_dir / 'task_results.parquet'}')").fetchone() == (
            "example/model",
            0.42,
        )
    finally:
        con.close()
