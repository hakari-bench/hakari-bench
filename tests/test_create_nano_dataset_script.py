from __future__ import annotations

from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import yaml

from scripts.create_nano_dataset import main


def _write_parquet(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), path)


def test_create_nano_dataset_script_builds_local_dataset_and_yaml(tmp_path: Path) -> None:
    source_dir = tmp_path / "source"
    _write_parquet(
        source_dir / "SourceTask" / "corpus" / "test.parquet",
        [{"_id": "d1", "text": "alpha document"}, {"_id": "d2", "text": "beta document"}],
    )
    _write_parquet(
        source_dir / "SourceTask" / "queries" / "test.parquet",
        [{"_id": "q1", "text": "alpha"}],
    )
    _write_parquet(
        source_dir / "SourceTask" / "qrels" / "test.parquet",
        [{"query-id": "q1", "corpus-id": "d1", "score": 1}],
    )
    output_dir = tmp_path / "NanoScript"
    config_dir = tmp_path / "config" / "datasets"

    main(
        [
            "--source-dir",
            str(source_dir),
            "--source-split-name",
            "SourceTask",
            "--dataset-name",
            "NanoScript",
            "--dataset-id",
            "hakari-bench/NanoScript",
            "--split-name",
            "NanoSourceTask",
            "--output-dir",
            str(output_dir),
            "--dataset-config-dir",
            str(config_dir),
            "--bm25-tokenizer",
            "whitespace",
            "--top-k",
            "2",
            "--query-limit",
            "10",
            "--doc-limit",
            "10",
        ]
    )

    assert (output_dir / "bm25" / "NanoSourceTask.parquet").exists()
    config = yaml.safe_load((config_dir / "nanoscript.yaml").read_text(encoding="utf-8"))
    assert config["name"] == "NanoScript"
    assert config["splits"] == ["NanoSourceTask"]
