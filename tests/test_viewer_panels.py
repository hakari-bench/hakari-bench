from __future__ import annotations

from pathlib import Path

import duckdb
from fastapi.testclient import TestClient

from hakari_bench.viewer.app import create_app
from hakari_bench.viewer.store import DuckDbLocation, LocalDuckDbStore


def test_analysis_panels_render_variant_rerank_and_dataset_tables(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_panel_db(db_path)
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    client = TestClient(app)

    variants = client.get("/analysis?panel=variants&view=BenchA")
    assert variants.status_code == 200
    assert "Variant impact" in variants.text
    assert "binary" in variants.text
    assert "-11.1%" in variants.text

    rerank = client.get("/analysis?panel=reranking&view=BenchA")
    assert rerank.status_code == 200
    assert "Reranking diagnostics" in rerank.text
    assert "Query coverage" in rerank.text
    assert "75.0%" in rerank.text

    datasets = client.get("/analysis?panel=datasets&view=BenchA")
    assert datasets.status_code == 200
    assert "Dataset diagnostics" in datasets.text
    assert "Saturation" in datasets.text
    assert "25.0%" in datasets.text


def _write_panel_db(db_path: Path) -> None:
    con = duckdb.connect(str(db_path))
    try:
        con.execute(
            """
            CREATE TABLE task_results (
                model_name VARCHAR,
                benchmark VARCHAR,
                dataset_id VARCHAR,
                dataset_name VARCHAR,
                split_name VARCHAR,
                task_name VARCHAR,
                task_key VARCHAR,
                score DOUBLE,
                embedding_variant_name VARCHAR,
                embedding_dim INTEGER,
                quantization VARCHAR,
                finished_at_utc VARCHAR,
                active_parameters BIGINT,
                total_parameters BIGINT,
                max_seq_length INTEGER
            )
            """
        )
        con.executemany(
            "INSERT INTO task_results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                ("model/a", "BenchA", "bench/a", "BenchA", "", "t1", "t1", 0.90, None, 768, None, "2026-01-01", 1, 2, 512),
                ("model/a", "BenchA", "bench/a", "BenchA", "", "t2", "t2", 0.90, None, 768, None, "2026-01-01", 1, 2, 512),
                ("model/b", "BenchA", "bench/a", "BenchA", "", "t1", "t1", 0.95, None, 512, None, "2026-01-01", 1, 2, 512),
                ("model/b", "BenchA", "bench/a", "BenchA", "", "t2", "t2", 0.60, None, 512, None, "2026-01-01", 1, 2, 512),
                ("model/a", "BenchA", "bench/a", "BenchA", "", "t1", "t1", 0.80, "binary", 768, "binary", "2026-01-01", 1, 2, 512),
                ("model/a", "BenchA", "bench/a", "BenchA", "", "t2", "t2", 0.80, "binary", 768, "binary", "2026-01-01", 1, 2, 512),
            ],
        )
        con.execute(
            """
            CREATE TABLE dataset_metadata (
                benchmark VARCHAR,
                dataset_id VARCHAR,
                dataset_name VARCHAR,
                split_name VARCHAR,
                task_name VARCHAR,
                task_key VARCHAR,
                language VARCHAR,
                languages VARCHAR[],
                category VARCHAR,
                query_count INTEGER,
                document_count INTEGER,
                query_mean_chars DOUBLE,
                document_mean_chars DOUBLE
            )
            """
        )
        con.executemany(
            "INSERT INTO dataset_metadata VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                ("BenchA", "bench/a", "BenchA", "", "t1", "t1", "en", ["en"], "natural_language", 100, 5000, 10.0, 200.0),
                ("BenchA", "bench/a", "BenchA", "", "t2", "t2", "ja", ["ja"], "code", 200, 10000, 30.0, 400.0),
            ],
        )
        con.execute(
            """
            CREATE TABLE task_diagnostics (
                model_name VARCHAR,
                benchmark VARCHAR,
                dataset_id VARCHAR,
                task_name VARCHAR,
                task_key VARCHAR,
                rerank_lift DOUBLE,
                rerank_status VARCHAR,
                rerank_top_k INTEGER,
                candidate_source VARCHAR,
                candidate_ranking VARCHAR,
                bm25_source VARCHAR,
                query_coverage DOUBLE,
                relevant_coverage DOUBLE
            )
            """
        )
        con.executemany(
            "INSERT INTO task_diagnostics VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                ("model/a", "BenchA", "bench/a", "t1", "t1", 0.05, "available", 100, "dataset_candidate_subset", "bm25", "dataset", 1.00, 0.75),
                ("model/b", "BenchA", "bench/a", "t2", "t2", 0.00, "available", 100, "dataset_candidate_subset", "bm25", "dataset", 0.50, 0.25),
            ],
        )
    finally:
        con.close()
