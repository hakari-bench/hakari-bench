from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest
import yaml

from hakari_bench import model_cards


def test_parse_truncate_dims_requires_dense_value() -> None:
    with pytest.raises(ValueError, match="--truncate-dims"):
        model_cards.parse_truncate_dims(None, model_type="dense")


def test_parse_truncate_dims_accepts_none_for_dense_model() -> None:
    assert model_cards.parse_truncate_dims(["none"], model_type="dense") is None


def test_model_card_from_metadata_applies_parameter_overrides() -> None:
    metadata = {
        "method": "dense",
        "id": "BAAI/bge-m3",
        "source": {"type": "huggingface", "name": "BAAI/bge-m3", "revision": "abc123"},
        "max_seq_length": 8192,
        "total_parameters": 567754752,
        "trainable_parameters": 567754752,
        "embedding_parameters": 256002048,
        "active_parameters": 311752704,
    }
    overrides = model_cards.ModelCardOverrides(active_parameters=123)

    card = model_cards.model_card_from_metadata(
        metadata,
        truncate_dims=[768],
        overrides=overrides,
        target={"datasets": ["hakari-bench/NanoBEIR-en"]},
    )

    assert card["id"] == "BAAI/bge-m3"
    assert card["source"] == {"type": "huggingface", "name": "BAAI/bge-m3", "revision": "abc123"}
    assert card["parameters"] == {
        "total": 567754752,
        "trainable": 567754752,
        "input_embedding": 256002048,
        "active": 123,
    }
    assert card["embedding"] == {"truncate_dims": [768]}
    assert card["runtime"]["max_seq_length"] == 8192
    assert card["target"] == {"datasets": ["hakari-bench/NanoBEIR-en"]}


def test_collect_model_cards_from_results_excludes_bekko_and_bm25(tmp_path: Path) -> None:
    _write_result(
        tmp_path / "BAAI__bge-m3" / "hakari-bench__NanoBEIR-en" / "arguana.json",
        model={
            "method": "dense",
            "id": "BAAI/bge-m3",
            "source": {"type": "huggingface", "name": "BAAI/bge-m3"},
            "total_parameters": 10,
            "trainable_parameters": 10,
            "embedding_parameters": 4,
            "active_parameters": 6,
            "max_seq_length": 8192,
        },
        embedding_evaluations=[
            {"name": "base"},
            {
                "name": "truncate_dim_768",
                "transform": {"steps": [{"type": "truncate", "parameters": {"dim": 768}}]},
            },
        ],
    )
    _write_result(
        tmp_path / "hotchpotch__bekko-model" / "hakari-bench__NanoBEIR-en" / "arguana.json",
        model={"method": "dense", "id": "hotchpotch/bekko-model"},
    )
    _write_result(
        tmp_path / "bm25" / "hakari-bench__NanoBEIR-en" / "arguana.json",
        model={"method": "bm25", "id": "bm25"},
    )

    cards = model_cards.collect_model_cards_from_results(
        tmp_path,
        exclude_model_substrings=["bekko"],
        exclude_model_ids=["bm25"],
    )

    assert list(cards) == ["BAAI/bge-m3"]
    assert cards["BAAI/bge-m3"]["embedding"]["truncate_dims"] == [768]
    assert cards["BAAI/bge-m3"]["target"] == {"datasets": ["hakari-bench/NanoBEIR-en"]}


def test_collect_model_cards_from_results_preserves_existing_notes(tmp_path: Path) -> None:
    _write_result(
        tmp_path / "jinaai__jina-embeddings-v3" / "hakari-bench__NanoBEIR-en" / "arguana.json",
        model={
            "method": "dense",
            "id": "jinaai/jina-embeddings-v3",
            "source": {"type": "huggingface", "name": "jinaai/jina-embeddings-v3"},
            "total_parameters": 10,
            "active_parameters": None,
        },
    )
    existing_cards = {
        "jinaai/jina-embeddings-v3": {
            "id": "jinaai/jina-embeddings-v3",
            "parameters": {"total": 10, "input_embedding": 4, "active": 6},
            "notes": ["manual correction"],
        },
    }

    cards = model_cards.collect_model_cards_from_results(tmp_path, existing_cards=existing_cards)

    assert cards["jinaai/jina-embeddings-v3"]["parameters"]["active"] == 6
    assert cards["jinaai/jina-embeddings-v3"]["notes"] == ["manual correction"]


def test_collect_model_cards_from_results_reads_each_json_once(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    first_path = tmp_path / "model-a" / "hakari-bench__NanoBEIR-en" / "arguana.json"
    second_path = tmp_path / "model-a" / "hakari-bench__NanoRTEB" / "ja_cwir.json"
    _write_result(first_path, model={"method": "dense", "id": "model/a"}, dataset_id="hakari-bench/NanoBEIR-en")
    _write_result(second_path, model={"method": "dense", "id": "model/a"}, dataset_id="hakari-bench/NanoRTEB")
    original_read_json = model_cards._read_json
    read_paths = []

    def tracking_read_json(path: Path) -> object:
        read_paths.append(path)
        return original_read_json(path)

    monkeypatch.setattr(model_cards, "_read_json", tracking_read_json)

    cards = model_cards.collect_model_cards_from_results(tmp_path)

    assert read_paths == [first_path, second_path]
    assert cards["model/a"]["target"]["datasets"] == [
        "hakari-bench/NanoBEIR-en",
        "hakari-bench/NanoRTEB",
    ]


def test_write_model_card_uses_safe_filename(tmp_path: Path) -> None:
    card = {"id": "BAAI/bge-m3", "parameters": {"total": 10}}

    output_path = model_cards.write_model_card(card, output_dir=tmp_path, overwrite=False)

    assert output_path == tmp_path / "BAAI__bge-m3.yaml"
    assert yaml.safe_load(output_path.read_text(encoding="utf-8")) == card


def test_write_evaluation_model_card_uses_model_output_directory(tmp_path: Path) -> None:
    args = argparse.Namespace(
        output_dir=str(tmp_path),
        model_id="BAAI/bge-m3",
        dataset=["hakari-bench/NanoBEIR-en"],
        collection=[],
        split=[],
        dataset_revision=None,
        embedding_variants=[
            {
                "name": "truncate_dim_768",
                "transform": {"steps": [{"type": "truncate", "parameters": {"dim": 768}}]},
            },
        ],
    )
    metadata = {
        "method": "dense",
        "id": "BAAI/bge-m3",
        "source": {"type": "huggingface", "name": "BAAI/bge-m3"},
        "total_parameters": 10,
        "embedding_parameters": 4,
        "active_parameters": 6,
    }

    output_path = model_cards.write_evaluation_model_card(args=args, model_metadata=metadata)

    assert output_path == tmp_path / "BAAI__bge-m3" / "BAAI__bge-m3.yaml"
    assert yaml.safe_load(output_path.read_text(encoding="utf-8"))["target"] == {
        "datasets": ["hakari-bench/NanoBEIR-en"]
    }


def test_build_model_card_loads_model_and_requires_truncate_dims(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = []

    def fake_load_model(config: object) -> object:
        calls.append(config)
        return object()

    def fake_collect_model_metadata(model: object, args: argparse.Namespace) -> dict[str, object]:
        return {
            "method": args.model_type,
            "id": args.model_id,
            "source": {"type": "huggingface", "name": args.model},
            "total_parameters": 10,
            "embedding_parameters": 4,
            "active_parameters": 6,
        }

    monkeypatch.setattr(model_cards, "load_model", fake_load_model)
    monkeypatch.setattr(model_cards, "collect_model_metadata", fake_collect_model_metadata)

    card = model_cards.build_model_card_from_loaded_model(
        model_id="BAAI/bge-m3",
        model_type="dense",
        truncate_dims=[768],
        overrides=model_cards.ModelCardOverrides(),
        dtype="bf16",
        device="cpu",
        trust_remote_code=True,
    )

    assert calls
    assert card["id"] == "BAAI/bge-m3"
    assert card["embedding"]["truncate_dims"] == [768]


def _write_result(
    path: Path,
    *,
    model: dict[str, object],
    embedding_evaluations: list[dict[str, object]] | None = None,
    dataset_id: str = "hakari-bench/NanoBEIR-en",
) -> None:
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(
            {
                "model": model,
                "target": {"dataset_id": dataset_id},
                "evaluation": {
                    "aggregate_metric": "ndcg@10",
                    "aggregate_metric_value": 0.5,
                    "embedding_evaluations": embedding_evaluations or [{"name": "base"}],
                },
            }
        ),
        encoding="utf-8",
    )
