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


def test_model_card_from_metadata_requires_method() -> None:
    metadata = {
        "id": "BAAI/bge-m3",
        "source": {"type": "huggingface", "name": "BAAI/bge-m3"},
    }

    with pytest.raises(ValueError, match="requires a non-empty method"):
        model_cards.model_card_from_metadata(
            metadata,
            truncate_dims=[768],
            overrides=model_cards.ModelCardOverrides(),
        )


def test_load_model_cards_rejects_missing_method(tmp_path: Path) -> None:
    path = tmp_path / "model.yaml"
    path.write_text("id: BAAI/bge-m3\n", encoding="utf-8")

    with pytest.raises(ValueError, match="requires a non-empty method"):
        model_cards.load_model_cards(path)


def test_model_card_from_metadata_preserves_late_interaction_settings() -> None:
    metadata = {
        "method": "late-interaction",
        "id": "lightonai/ColBERT-Zero",
        "source": {"type": "huggingface", "name": "lightonai/ColBERT-Zero"},
        "late_interaction": {
            "architecture": "colbert",
            "scoring": "maxsim",
            "query_prefix": "[Q] ",
            "document_prefix": "[D] ",
            "query_length": 39,
            "document_length": 519,
            "do_query_expansion": False,
            "attend_to_expansion_tokens": False,
        },
    }

    card = model_cards.model_card_from_metadata(
        metadata,
        truncate_dims=None,
        overrides=model_cards.ModelCardOverrides(),
    )

    assert card["late_interaction"] == metadata["late_interaction"]


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


def test_collect_model_cards_from_results_excludes_noop_truncate_dimension(tmp_path: Path) -> None:
    _write_result(
        tmp_path / "hotchpotch__bekko-embedding-v1-a8m" / "hakari-bench__NanoBEIR-ja" / "arguana.json",
        model={
            "method": "dense",
            "id": "hotchpotch/bekko-embedding-v1-a8m",
            "source": {"type": "huggingface", "name": "hotchpotch/bekko-embedding-v1-a8m"},
        },
        embedding_evaluations=[
            {"name": "base", "embedding_dimensions": {"dim": 384}},
            {
                "name": "truncate_dim_384",
                "transform": {"steps": [{"type": "truncate", "parameters": {"dim": 384}}]},
            },
            {
                "name": "truncate_dim_256",
                "transform": {"steps": [{"type": "truncate", "parameters": {"dim": 256}}]},
            },
        ],
    )

    cards = model_cards.collect_model_cards_from_results(
        tmp_path,
        exclude_model_substrings=[],
    )

    assert cards["hotchpotch/bekko-embedding-v1-a8m"]["embedding"]["truncate_dims"] == [256]


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


def test_collect_model_cards_from_results_infers_prompt_settings(tmp_path: Path) -> None:
    _write_result(
        tmp_path / "intfloat__multilingual-e5-small" / "hakari-bench__NanoBEIR-en" / "arguana.json",
        model={
            "method": "dense",
            "id": "intfloat/multilingual-e5-small",
            "source": {"type": "huggingface", "name": "intfloat/multilingual-e5-small"},
        },
        config={
            "query_prompt": "query: ",
            "document_prompt": "passage: ",
            "query_prompt_name": None,
            "document_prompt_name": None,
            "query_encode_task": None,
            "document_encode_task": None,
        },
    )

    cards = model_cards.collect_model_cards_from_results(tmp_path)

    assert cards["intfloat/multilingual-e5-small"]["prompts"] == {
        "query_prompt": "query: ",
        "document_prompt": "passage: ",
    }


def test_collect_model_cards_from_results_infers_late_interaction_settings(tmp_path: Path) -> None:
    _write_result(
        tmp_path / "lightonai__ColBERT-Zero" / "hakari-bench__NanoBEIR-en" / "arguana.json",
        model={
            "method": "late-interaction",
            "id": "lightonai/ColBERT-Zero",
            "source": {"type": "huggingface", "name": "lightonai/ColBERT-Zero"},
        },
        config={
            "query_prompt_name": "query",
            "document_prompt_name": "document",
            "late_interaction": {
                "scoring": "exact_maxsim",
                "query_length": 39,
                "document_length": 519,
                "query_prefix": "[Q] ",
                "document_prefix": "[D] ",
                "attend_to_expansion_tokens": False,
            },
        },
    )

    cards = model_cards.collect_model_cards_from_results(tmp_path)

    card = cards["lightonai/ColBERT-Zero"]
    assert card["prompts"] == {
        "query_prompt_name": "query",
        "document_prompt_name": "document",
    }
    assert card["late_interaction"] == {
        "scoring": "maxsim",
        "query_length": 39,
        "document_length": 519,
        "query_prefix": "[Q] ",
        "document_prefix": "[D] ",
        "attend_to_expansion_tokens": False,
    }


def test_collect_model_cards_from_results_keeps_existing_reviewed_prompt_settings(tmp_path: Path) -> None:
    _write_result(
        tmp_path / "Qwen__Qwen3-Embedding-0.6B" / "hakari-bench__NanoBEIR-en" / "arguana.json",
        model={
            "method": "dense",
            "id": "Qwen/Qwen3-Embedding-0.6B",
            "source": {"type": "huggingface", "name": "Qwen/Qwen3-Embedding-0.6B"},
        },
        config={
            "query_prompt": "Instruct: ",
            "document_prompt": "",
        },
    )
    existing_cards = {
        "Qwen/Qwen3-Embedding-0.6B": {
            "id": "Qwen/Qwen3-Embedding-0.6B",
            "prompts": {
                "query_prompt_name": "query",
                "document_prompt_name": "document",
            },
        }
    }

    cards = model_cards.collect_model_cards_from_results(tmp_path, existing_cards=existing_cards)

    assert cards["Qwen/Qwen3-Embedding-0.6B"]["prompts"] == existing_cards["Qwen/Qwen3-Embedding-0.6B"]["prompts"]


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


def test_collect_model_cards_from_results_can_infer_language_support_from_scores(tmp_path: Path) -> None:
    scores = {
        "en": 0.64,
        "ar": 0.61,
        "de": 0.62,
        "es": 0.63,
        "fr": 0.64,
        "ja": 0.65,
        "ko": 0.60,
        "pt": 0.62,
    }
    for language, score in scores.items():
        _write_result(
            tmp_path / "LiquidAI__LFM2.5-Embedding-350M" / f"hakari-bench__NanoBEIR-{language}" / "arguana.json",
            model={"method": "dense", "id": "LiquidAI/LFM2.5-Embedding-350M"},
            dataset_id=f"hakari-bench/NanoBEIR-{language}",
            score=score,
        )

    cards = model_cards.collect_model_cards_from_results(tmp_path, infer_language_support=True)

    language_support = cards["LiquidAI/LFM2.5-Embedding-350M"]["language_support"]
    assert language_support["category"] == "multilingual"
    assert "languages" not in language_support
    assert language_support["evidence"]["classification_reason"] == "broad_multilingual_score_evidence"
    assert language_support["evidence"]["english_score"] == 0.64
    assert language_support["evidence"]["high_non_english_language_count"] == 7
    assert language_support["evidence"]["evaluated_language_count"] == 8


def test_collect_model_cards_from_results_keeps_existing_language_support(tmp_path: Path) -> None:
    for language in ["en", "ar", "de", "es", "fr", "ja", "ko", "pt"]:
        _write_result(
            tmp_path / "model__a" / f"hakari-bench__NanoBEIR-{language}" / "arguana.json",
            model={"method": "dense", "id": "model/a"},
            dataset_id=f"hakari-bench/NanoBEIR-{language}",
            score=0.7,
        )
    existing_cards = {
        "model/a": {
            "id": "model/a",
            "language_support": {
                "category": "english_only",
                "languages": ["en"],
                "evidence": {
                    "benchmarks": ["NanoMIRACL", "MNanoBEIR"],
                    "score_target": "all",
                    "classification_policy": (
                        "model identity first; use broad score evidence only for models without explicit language identity"
                    ),
                    "classification_reason": "manual_review",
                    "evaluated_language_count": 8,
                },
            },
        }
    }

    cards = model_cards.collect_model_cards_from_results(
        tmp_path,
        existing_cards=existing_cards,
        infer_language_support=True,
    )

    assert cards["model/a"]["language_support"] == existing_cards["model/a"]["language_support"]


def test_write_model_card_uses_safe_filename(tmp_path: Path) -> None:
    card = {"id": "BAAI/bge-m3", "method": "dense", "parameters": {"total": 10}}

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
        query_prompt="query: ",
        corpus_prompt="passage: ",
        query_prompt_name=None,
        corpus_prompt_name=None,
        query_task=None,
        corpus_task=None,
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
    payload = yaml.safe_load(output_path.read_text(encoding="utf-8"))
    assert payload["target"] == {"datasets": ["hakari-bench/NanoBEIR-en"]}
    assert payload["prompts"] == {
        "query_prompt": "query: ",
        "document_prompt": "passage: ",
    }


def test_write_evaluation_model_card_preserves_late_interaction_args(tmp_path: Path) -> None:
    args = argparse.Namespace(
        output_dir=str(tmp_path),
        model_id="lightonai/ColBERT-Zero",
        dataset=["hakari-bench/NanoBEIR-en"],
        collection=[],
        split=[],
        dataset_revision=None,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name="query",
        corpus_prompt_name="document",
        query_task=None,
        corpus_task=None,
        embedding_variants=[],
        late_interaction_query_prefix="[Q] ",
        late_interaction_document_prefix="[D] ",
        late_interaction_query_length=39,
        late_interaction_document_length=519,
        late_interaction_do_query_expansion=False,
        late_interaction_attend_to_expansion_tokens=False,
    )
    metadata = {
        "method": "late-interaction",
        "id": "lightonai/ColBERT-Zero",
        "source": {"type": "huggingface", "name": "lightonai/ColBERT-Zero"},
        "total_parameters": 10,
    }

    output_path = model_cards.write_evaluation_model_card(args=args, model_metadata=metadata)

    payload = yaml.safe_load(output_path.read_text(encoding="utf-8"))
    assert payload["prompts"] == {
        "query_prompt_name": "query",
        "document_prompt_name": "document",
    }
    assert payload["late_interaction"] == {
        "scoring": "maxsim",
        "query_prefix": "[Q] ",
        "document_prefix": "[D] ",
        "query_length": 39,
        "document_length": 519,
        "do_query_expansion": False,
        "attend_to_expansion_tokens": False,
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
            "trust_remote_code": args.trust_remote_code,
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
        remote_code_approved=True,
    )

    assert calls
    assert card["id"] == "BAAI/bge-m3"
    assert card["embedding"]["truncate_dims"] == [768]
    assert card["runtime"]["remote_code_approved"] is True


def test_collect_model_cards_from_results_preserves_remote_code_approval(tmp_path: Path) -> None:
    result_path = tmp_path / "model" / "dataset" / "task.json"
    _write_result(
        result_path,
        model={
            "id": "jinaai/jina-embeddings-v3",
            "method": "dense",
            "source": {
                "type": "huggingface",
                "name": "jinaai/jina-embeddings-v3",
                "revision": "ab036b023d30b4d1138c4c3bfa9f0c445ab455d6",
            },
            "trust_remote_code": True,
        },
    )
    existing_cards = {
        "jinaai/jina-embeddings-v3": {
            "id": "jinaai/jina-embeddings-v3",
            "runtime": {"remote_code_approved": True},
        }
    }

    cards = model_cards.collect_model_cards_from_results(tmp_path, existing_cards=existing_cards)

    assert cards["jinaai/jina-embeddings-v3"]["runtime"]["remote_code_approved"] is True


def test_static_model_cards_cover_latest_leaderboard_models() -> None:
    cards = model_cards.load_model_cards(Path("config/model_cards"))

    expected_models = {
        "Alibaba-NLP/gte-multilingual-reranker-base": "reranker",
        "BAAI/bge-reranker-v2-m3": "reranker",
        "BAAI/bge-small-en-v1.5": "dense",
        "Qwen/Qwen3-Reranker-0.6B": "reranker",
        "answerdotai/answerai-colbert-small-v1": "late-interaction",
        "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1": "reranker",
        "hotchpotch/bekko-embedding-small-beta-unir-v8": "dense",
        "hotchpotch/japanese-reranker-xsmall-v2": "reranker",
        "ibm-granite/granite-embedding-30m-sparse": "sparse",
        "jinaai/jina-reranker-v2-base-multilingual": "reranker",
        "lightonai/ColBERT-Zero": "late-interaction",
        "microsoft/harrier-oss-v1-0.6b": "dense",
        "mixedbread-ai/mxbai-edge-colbert-v0-17m": "late-interaction",
        "mixedbread-ai/mxbai-embed-xsmall-v1": "dense",
        "naver/splade-v3": "sparse",
        "nomic-ai/nomic-embed-text-v1.5": "dense",
        "nomic-ai/nomic-embed-text-v2-moe": "dense",
        "opensearch-project/opensearch-neural-sparse-encoding-multilingual-v1": "sparse",
        "prithivida/Splade_PP_en_v2": "sparse",
    }

    for model_id, method in expected_models.items():
        card = cards[model_id]
        assert card["method"] == method
        assert card["parameters"]["total"] > 0
        assert card["parameters"]["input_embedding"] >= 0
        if method == "late-interaction":
            assert card["late_interaction"]["architecture"] == "colbert"
            assert card["late_interaction"]["scoring"] == "maxsim"
        assert card["parameters"]["active"] >= 0


def test_static_model_cards_all_declare_supported_method() -> None:
    cards = model_cards.load_model_cards(Path("config/model_cards"))

    assert cards
    for model_id, card in cards.items():
        assert model_cards.validate_model_card_method(card.get("method"), model_id=model_id) == card["method"]


def test_static_model_cards_include_language_support_evidence() -> None:
    cards = model_cards.load_model_cards(Path("config/model_cards"))

    for card in cards.values():
        language_support = card.get("language_support")
        assert isinstance(language_support, dict)
        assert language_support["category"] in {"english_only", "english_plus", "multilingual"}
        if language_support["category"] == "multilingual":
            assert "languages" not in language_support
        else:
            assert isinstance(language_support["languages"], list)
            assert language_support["languages"]
            assert all(isinstance(language, str) and language for language in language_support["languages"])
        evidence = language_support.get("evidence")
        assert isinstance(evidence, dict)
        assert evidence["benchmarks"] == ["NanoMIRACL", "MNanoBEIR"]
        assert evidence["score_target"] == "all"
        assert evidence["classification_policy"] == (
            "model identity first; use broad score evidence only for models without explicit language identity"
        )
        assert evidence["classification_reason"]
        assert evidence["evaluated_language_count"] > 0


def test_static_model_cards_include_license_metadata() -> None:
    cards = model_cards.load_model_cards(Path("config/model_cards"))
    valid_license_types = {"algorithm", "non_commercial", "permissive", "proprietary", "unknown"}
    valid_commercial_use = {"allowed", "not_allowed", "not_applicable", "permitted_with_terms", "unknown"}

    for card in cards.values():
        license_metadata = card.get("license")
        assert isinstance(license_metadata, dict)
        assert license_metadata["id"]
        assert license_metadata["label"]
        assert license_metadata["type"] in valid_license_types
        assert license_metadata["commercial_use"] in valid_commercial_use
        assert license_metadata["source"]

    assert cards["BAAI/bge-m3"]["license"] == {
        "id": "mit",
        "label": "MIT",
        "type": "permissive",
        "commercial_use": "allowed",
        "source": "huggingface_model_card",
        "source_url": "https://huggingface.co/BAAI/bge-m3",
    }
    assert cards["jinaai/jina-embeddings-v3"]["license"]["label"] == "CC BY-NC 4.0"
    assert cards["jinaai/jina-embeddings-v3"]["license"]["commercial_use"] == "not_allowed"
    assert cards["google/embeddinggemma-300m"]["license"]["type"] == "proprietary"
    assert cards["google/embeddinggemma-300m"]["license"]["commercial_use"] == "permitted_with_terms"
    assert cards["bm25"]["license"] == {
        "id": "mit",
        "label": "MIT",
        "type": "permissive",
        "commercial_use": "allowed",
        "source": "bm25s_github_repository",
        "source_url": "https://github.com/xhluca/bm25s",
    }


def test_validate_model_card_links_normalizes_and_drops_empty() -> None:
    normalized = model_cards.validate_model_card_links(
        {
            "huggingface": " https://huggingface.co/BAAI/bge-m3 ",
            "github": "https://github.com/FlagOpen/FlagEmbedding",
            "papers": [
                {"title": " BGE M3-Embedding ", "url": " https://arxiv.org/abs/2402.03216 "},
            ],
        }
    )

    assert normalized == {
        "huggingface": "https://huggingface.co/BAAI/bge-m3",
        "github": "https://github.com/FlagOpen/FlagEmbedding",
        "papers": [{"title": "BGE M3-Embedding", "url": "https://arxiv.org/abs/2402.03216"}],
    }
    assert model_cards.validate_model_card_links({}) == {}
    assert model_cards.validate_model_card_links({"papers": []}) == {}


@pytest.mark.parametrize(
    "links",
    [
        {"unknown": "x"},
        {"huggingface": ""},
        {"github": 123},
        {"papers": "not-a-list"},
        {"papers": [{"title": "missing url"}]},
        {"papers": [{"url": "https://example.com"}]},
        {"papers": [{"title": "t", "url": "u", "extra": "x"}]},
    ],
)
def test_validate_model_card_links_rejects_malformed(links: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        model_cards.validate_model_card_links(links)


def test_static_model_cards_links_are_well_formed() -> None:
    cards = model_cards.load_model_cards(Path("config/model_cards"))

    for model_id, card in cards.items():
        links = card.get("links")
        if links is None:
            continue
        normalized = model_cards.validate_model_card_links(links)
        assert model_cards.validate_model_card_links(normalized) == normalized, model_id


def test_static_model_card_language_support_uses_model_identity() -> None:
    cards = model_cards.load_model_cards(Path("config/model_cards"))

    assert cards["lightonai/GTE-ModernColBERT-v1"]["language_support"]["category"] == "english_only"
    assert cards["lightonai/GTE-ModernColBERT-v1"]["language_support"]["languages"] == ["en"]
    assert cards["sentence-transformers/all-MiniLM-L6-v2"]["language_support"]["languages"] == ["en"]
    assert cards["cl-nagoya/ruri-v3-30m"]["language_support"]["languages"] == ["ja", "en"]
    assert cards["hotchpotch/japanese-reranker-xsmall-v2"]["language_support"]["languages"] == ["ja", "en"]
    assert cards["Lajavaness/bilingual-embedding-small"]["language_support"]["category"] == "multilingual"
    assert "languages" not in cards["Lajavaness/bilingual-embedding-small"]["language_support"]
    assert cards["codefuse-ai/F2LLM-v2-80M"]["language_support"]["category"] == "multilingual"
    assert "languages" not in cards["codefuse-ai/F2LLM-v2-80M"]["language_support"]
    assert cards["LiquidAI/LFM2.5-ColBERT-350M"]["language_support"]["category"] == "multilingual"
    assert "languages" not in cards["LiquidAI/LFM2.5-ColBERT-350M"]["language_support"]
    assert cards["LiquidAI/LFM2.5-Embedding-350M"]["language_support"]["category"] == "multilingual"
    assert "languages" not in cards["LiquidAI/LFM2.5-Embedding-350M"]["language_support"]
    assert cards["LiquidAI/LFM2.5-Embedding-350M"]["language_support"]["evidence"][
        "official_supported_languages"
    ] == ["en", "es", "de", "fr", "it", "pt", "ar", "sv", "no", "ja", "ko"]


def test_static_model_card_language_support_keeps_most_rerankers_english_only() -> None:
    cards = model_cards.load_model_cards(Path("config/model_cards"))

    for model_id in [
        "cross-encoder/ettin-reranker-17m-v1",
        "cross-encoder/ettin-reranker-32m-v1",
        "cross-encoder/ettin-reranker-68m-v1",
        "cross-encoder/ettin-reranker-150m-v1",
        "cross-encoder/ettin-reranker-400m-v1",
    ]:
        assert cards[model_id]["language_support"]["category"] == "english_only"
        assert cards[model_id]["language_support"]["languages"] == ["en"]

    for model_id in [
        "Alibaba-NLP/gte-multilingual-reranker-base",
        "BAAI/bge-reranker-v2-m3",
        "Qwen/Qwen3-Reranker-0.6B",
        "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1",
        "jinaai/jina-reranker-v2-base-multilingual",
    ]:
        assert cards[model_id]["language_support"]["category"] == "multilingual"
        assert "languages" not in cards[model_id]["language_support"]


def test_static_qwen3_embedding_4b_card_matches_official_embedding_metadata() -> None:
    card = model_cards.load_model_cards(Path("config/model_cards"))["Qwen/Qwen3-Embedding-4B"]

    assert card["runtime"]["max_seq_length"] == 32768
    assert card["runtime"]["similarity_fn_name"] == "cosine"
    assert card["prompts"] == {
        "query_prompt_name": "query",
        "document_prompt_name": "document",
    }
    assert card["embedding"]["output_dimension"] == 2560
    assert card["embedding"]["user_defined_output_dimensions"] == {
        "min": 32,
        "max": 2560,
    }
    assert card["embedding"]["mrl_support"] is True
    assert card["embedding"]["pooling"] == "last_token"
    assert card["embedding"]["normalize"] is True
    assert card["embedding"]["include_prompt"] is True
    assert card["embedding"]["truncate_dims"] == [
        32,
        64,
        128,
        256,
        512,
        768,
        1024,
        1536,
        2048,
    ]


def test_static_model_card_truncate_dims_exclude_base_dimension() -> None:
    cards = model_cards.load_model_cards(Path("config/model_cards"))
    known_base_dims = {
        "KaLM-Embedding/KaLM-embedding-multilingual-mini-instruct-v2.5": 896,
        "Qwen/Qwen3-Embedding-0.6B": 1024,
        "Qwen/Qwen3-Embedding-4B": 2560,
        "Snowflake/snowflake-arctic-embed-l-v2.0": 1024,
        "google/embeddinggemma-300m": 768,
        "hotchpotch/bekko-embedding-small-beta-unir-v8": 384,
        "hotchpotch/bekko-embedding-v1-a8m": 384,
        "ibm-granite/granite-embedding-311m-multilingual-r2": 768,
        "jinaai/jina-embeddings-v3": 1024,
        "jinaai/jina-embeddings-v5-text-nano": 768,
        "jinaai/jina-embeddings-v5-text-small": 1024,
        "mixedbread-ai/mxbai-embed-xsmall-v1": 384,
        "nomic-ai/nomic-embed-text-v1.5": 768,
        "nomic-ai/nomic-embed-text-v2-moe": 768,
        "openai/text-embedding-3-large": 3072,
        "openai/text-embedding-3-small": 1536,
        "sentence-transformers/static-similarity-mrl-multilingual-v1": 1024,
    }

    truncate_cards = {
        model_id: card
        for model_id, card in cards.items()
        if isinstance(card.get("embedding"), dict) and card["embedding"].get("truncate_dims")
    }
    assert set(truncate_cards) == set(known_base_dims)
    for model_id, card in truncate_cards.items():
        truncate_dims = card["embedding"]["truncate_dims"]
        assert all(dim < known_base_dims[model_id] for dim in truncate_dims), model_id


def test_openai_static_model_cards_include_evaluation_notice() -> None:
    cards = model_cards.load_model_cards(Path("config/model_cards"))
    notice = (
        "Max tokens is 8,192, but HAKARI evaluates this model with max tokens "
        "set to 8,100 for calibration."
    )

    assert cards["openai/text-embedding-3-small"]["notice"] == notice
    assert cards["openai/text-embedding-3-large"]["notice"] == notice


def _write_result(
    path: Path,
    *,
    model: dict[str, object],
    embedding_evaluations: list[dict[str, object]] | None = None,
    config: dict[str, object] | None = None,
    dataset_id: str = "hakari-bench/NanoBEIR-en",
    score: float = 0.5,
) -> None:
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(
            {
                "model": model,
                "target": {"dataset_id": dataset_id},
                "config": config or {},
                "evaluation": {
                    "aggregate_metric": "ndcg@10",
                    "aggregate_metric_value": score,
                    "embedding_evaluations": embedding_evaluations or [{"name": "base"}],
                },
            }
        ),
        encoding="utf-8",
    )
