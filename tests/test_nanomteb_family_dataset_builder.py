from __future__ import annotations

import pyarrow as pa
import pyarrow.parquet as pq

from scripts.build_nanomteb_family_datasets import SplitSource, _build_readme, _select_parquet_file
from scripts.build_nanomteb_family_datasets import _copy_parquet_file


def test_select_parquet_file_prefers_unsharded_name() -> None:
    files = {
        "queries/NanoTask.parquet",
        "queries/NanoTask-00000-of-00001.parquet",
    }

    assert (
        _select_parquet_file(files=files, config="queries", split_name="NanoTask", dataset_id="dataset")
        == "queries/NanoTask.parquet"
    )


def test_build_readme_describes_uploadable_nano_dataset_not_collection() -> None:
    readme = _build_readme(
        dataset_name="NanoFaMTEB",
        dataset_config={"metadata": {"language": "fa", "description": "Persian retrieval."}},
        copied={
            "NanoTask": {
                "bm25": "bm25/NanoTask.parquet",
                "corpus": "corpus/NanoTask.parquet",
                "qrels": "qrels/NanoTask.parquet",
                "queries": "queries/NanoTask.parquet",
            }
        },
        splits=[
            SplitSource(
                target_dataset="NanoFaMTEB",
                split_name="NanoTask",
                source_dataset_name="NanoMTEB-Persian",
                source_dataset_id="hakari-bench/NanoMTEB-Persian",
            )
        ],
    )

    assert "config_name: queries" in readme
    assert "hakari-bench/NanoFaMTEB" in readme
    assert "Source historical dataset repositories" in readme
    assert "--collection NanoMTEB_Family" not in readme


def test_copy_parquet_file_drops_qrels_score_column(tmp_path) -> None:
    source = tmp_path / "source.parquet"
    dest = tmp_path / "dest.parquet"
    pq.write_table(
        pa.table(
            {
                "query-id": ["q1", "q2"],
                "corpus-id": ["d1", "d2"],
                "score": [1, 0],
            }
        ),
        source,
    )

    _copy_parquet_file(local_file=source, dest=dest, config="qrels")

    table = pq.read_table(dest)
    assert table.column_names == ["query-id", "corpus-id"]
    assert table.to_pydict() == {"query-id": ["q1"], "corpus-id": ["d1"]}


def test_copy_parquet_file_keeps_graded_positive_qrels(tmp_path) -> None:
    source = tmp_path / "source.parquet"
    dest = tmp_path / "dest.parquet"
    pq.write_table(
        pa.table(
            {
                "query-id": ["q1", "q2", "q3"],
                "corpus-id": ["d1", "d2", "d3"],
                "score": [0, 2, 16],
            }
        ),
        source,
    )

    _copy_parquet_file(local_file=source, dest=dest, config="qrels")

    assert pq.read_table(dest).to_pydict() == {"query-id": ["q2", "q3"], "corpus-id": ["d2", "d3"]}
