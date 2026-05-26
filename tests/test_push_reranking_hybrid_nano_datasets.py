from __future__ import annotations

from scripts.push_reranking_hybrid_nano_datasets import (
    merge_frontmatter,
    rewrite_data_file_paths_for_push_to_hub,
)


def test_rewrite_data_file_paths_for_push_to_hub_matches_datasetdict_shards() -> None:
    frontmatter = {
        "configs": [
            {
                "config_name": "queries",
                "data_files": [
                    {"split": "NanoArguAna", "path": "queries/NanoArguAna.parquet"},
                    {"split": "NanoNQ", "path": "queries/NanoNQ-00000-of-00001.parquet"},
                ],
                "default": True,
            },
            {
                "config_name": "reranking_hybrid",
                "data_files": [
                    {"split": "NanoArguAna", "path": "reranking_hybrid/NanoArguAna.parquet"},
                ],
            },
        ],
        "language": ["ja"],
    }

    rewritten = rewrite_data_file_paths_for_push_to_hub(frontmatter)

    assert rewritten["configs"][0]["data_files"] == [
        {"split": "NanoArguAna", "path": "queries/NanoArguAna-00000-of-00001.parquet"},
        {"split": "NanoNQ", "path": "queries/NanoNQ-00000-of-00001.parquet"},
    ]
    assert rewritten["configs"][1]["data_files"] == [
        {"split": "NanoArguAna", "path": "reranking_hybrid/NanoArguAna-00000-of-00001.parquet"},
    ]
    assert frontmatter["configs"][0]["data_files"][0]["path"] == "queries/NanoArguAna.parquet"


def test_rewrite_data_file_paths_for_push_to_hub_uses_remote_multishard_files() -> None:
    frontmatter = {
        "configs": [
            {
                "config_name": "corpus",
                "data_files": [
                    {"split": "large", "path": "corpus/large.parquet"},
                    {"split": "small", "path": "corpus/small.parquet"},
                ],
            },
        ],
    }
    remote_files = {
        "corpus/large-00000-of-00002.parquet",
        "corpus/large-00001-of-00002.parquet",
        "corpus/small-00000-of-00001.parquet",
    }

    rewritten = rewrite_data_file_paths_for_push_to_hub(frontmatter, remote_files=remote_files)

    assert rewritten["configs"][0]["data_files"] == [
        {
            "split": "large",
            "path": [
                "corpus/large-00000-of-00002.parquet",
                "corpus/large-00001-of-00002.parquet",
            ],
        },
        {"split": "small", "path": "corpus/small-00000-of-00001.parquet"},
    ]


def test_merge_frontmatter_rewrites_local_config_paths_to_uploaded_shards() -> None:
    remote = {"dataset_info": [{"config_name": "old"}], "language": ["ja"]}
    local = {
        "configs": [
            {
                "config_name": "corpus",
                "data_files": [{"split": "ja_cwir", "path": "corpus/ja_cwir.parquet"}],
            },
        ],
        "tags": ["nano"],
    }

    merged = merge_frontmatter(
        remote,
        local,
        remote_files={"corpus/ja_cwir-00000-of-00001.parquet"},
    )

    assert merged["dataset_info"] == [{"config_name": "old"}]
    assert merged["language"] == ["ja"]
    assert merged["tags"] == ["nano"]
    assert merged["configs"] == [
        {
            "config_name": "corpus",
            "data_files": [{"split": "ja_cwir", "path": "corpus/ja_cwir-00000-of-00001.parquet"}],
        },
    ]
