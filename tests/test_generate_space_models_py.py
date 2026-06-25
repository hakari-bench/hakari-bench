from __future__ import annotations

from pathlib import Path

import duckdb

from scripts.generate_space_models_py import extract_hf_model_names, render_models_py, write_models_py


def test_extract_hf_model_names_filters_bm25_and_non_repo_ids(tmp_path: Path) -> None:
    duckdb_path = tmp_path / "leaderboard.duckdb"
    con = duckdb.connect(str(duckdb_path))
    con.execute("create table dim_model(model_name varchar, model_type varchar)")
    con.executemany(
        "insert into dim_model values (?, ?)",
        [
            ("BAAI/bge-m3", "dense"),
            ("bm25", "bm25"),
            ("openai/text-embedding-3-small", "dense"),
            ("namespace/model with spaces", "dense"),
            ("namespace/model(extra)", "dense"),
            ("too/many/slashes", "dense"),
            ("BAAI/bge-m3", "dense"),
        ],
    )
    con.close()

    assert extract_hf_model_names(duckdb_path) == [
        "BAAI/bge-m3",
        "openai/text-embedding-3-small",
    ]


def test_render_models_py_uses_static_model_name_literals() -> None:
    rendered = render_models_py(["BAAI/bge-m3", "Qwen/Qwen3-Embedding-0.6B"])

    assert "This file is not imported by the Space app" in rendered
    assert 'MODEL_NAMES = [' in rendered
    assert '    "BAAI/bge-m3",' in rendered
    assert '    "Qwen/Qwen3-Embedding-0.6B",' in rendered


def test_write_models_py_can_skip_hub_verification(tmp_path: Path) -> None:
    duckdb_path = tmp_path / "leaderboard.duckdb"
    output_path = tmp_path / "models.py"
    con = duckdb.connect(str(duckdb_path))
    con.execute("create table dim_model(model_name varchar, model_type varchar)")
    con.execute("insert into dim_model values ('BAAI/bge-m3', 'dense')")
    con.close()

    model_names = write_models_py(duckdb_path=duckdb_path, output_path=output_path, verify_hub=False)

    assert model_names == ["BAAI/bge-m3"]
    assert output_path.read_text(encoding="utf-8").count("BAAI/bge-m3") == 1
