from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest
import torch

from hakari_bench.models import (
    ColbertLateInteractionAdapter,
    ModelLoadConfig,
    collect_model_metadata,
    load_model,
    resolve_model_revision,
    resolve_attn_implementation,
    resolve_torch_dtype,
)


def test_resolve_torch_dtype_defaults_to_bf16() -> None:
    assert resolve_torch_dtype("bf16") is torch.bfloat16
    assert resolve_torch_dtype("fp16") is torch.float16
    assert resolve_torch_dtype("fp32") is torch.float32


def test_resolve_attn_implementation_rejects_flash_attn_conflict() -> None:
    with pytest.raises(ValueError):
        resolve_attn_implementation(attn_implementation="sdpa", flash_attn2=True)


def test_load_model_passes_dense_options(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[dict[str, object]] = []

    class FakeSentenceTransformer(torch.nn.Module):
        def __init__(self, model_name_or_path: str, **kwargs: object) -> None:
            super().__init__()
            calls.append({"model_name_or_path": model_name_or_path, **kwargs})
            self.max_seq_length = None
            self.projection = torch.nn.Linear(2, 2)
            self.inner = FakeCustomModule()

    monkeypatch.setattr("hakari_bench.models._import_sentence_transformer", lambda: FakeSentenceTransformer)

    model = load_model(
        ModelLoadConfig(
            model_name_or_path="hotchpotch/model",
            model_type="dense",
            dtype="bf16",
            attn_implementation=None,
            flash_attn2=True,
            device="cpu",
            trust_remote_code=True,
            max_seq_length=128,
        )
    )

    assert isinstance(model, FakeSentenceTransformer)
    assert model.max_seq_length == 128
    assert model.projection.weight.dtype is torch.bfloat16
    assert model.inner.model.config._attn_implementation == "flash_attention_2"
    assert calls == [
        {
            "model_name_or_path": "hotchpotch/model",
            "device": "cpu",
            "revision": None,
            "trust_remote_code": True,
            "model_kwargs": {
                "torch_dtype": torch.bfloat16,
                "attn_implementation": "flash_attention_2",
            },
        }
    ]


def test_load_model_passes_late_interaction_options(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[dict[str, object]] = []

    class FakeColBERT(torch.nn.Module):
        def __init__(self, model_name_or_path: str, **kwargs: object) -> None:
            super().__init__()
            calls.append({"model_name_or_path": model_name_or_path, **kwargs})
            self.projection = torch.nn.Linear(2, 2)

    monkeypatch.setattr("hakari_bench.models._import_pylate_colbert", lambda: FakeColBERT)

    model = load_model(
        ModelLoadConfig(
            model_name_or_path="lightonai/GTE-ModernColBERT-v1",
            model_type="late-interaction",
            dtype="fp32",
            device="cpu",
            trust_remote_code=True,
            late_interaction_query_length=64,
            late_interaction_document_length=300,
            late_interaction_query_prefix="[QueryMarker]",
            late_interaction_document_prefix="[DocumentMarker]",
            late_interaction_do_query_expansion=False,
            late_interaction_attend_to_expansion_tokens=True,
        )
    )

    assert isinstance(model, FakeColBERT)
    assert model.projection.weight.dtype is torch.float32
    assert calls == [
        {
            "model_name_or_path": "lightonai/GTE-ModernColBERT-v1",
            "device": "cpu",
            "revision": None,
            "trust_remote_code": True,
            "model_kwargs": {"torch_dtype": torch.float32},
            "query_length": 64,
            "document_length": 300,
            "query_prefix": "[QueryMarker]",
            "document_prefix": "[DocumentMarker]",
            "do_query_expansion": False,
            "attend_to_expansion_tokens": True,
        }
    ]


def test_load_model_uses_late_interaction_colbert_config_defaults(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    config_path = tmp_path / "config_sentence_transformers.json"
    config_path.write_text(
        json.dumps(
            {
                "model_type": "ColBERT",
                "query_prefix": "[Q] ",
                "document_prefix": "[D] ",
                "query_length": 48,
                "document_length": 512,
                "do_query_expansion": False,
                "attend_to_expansion_tokens": False,
            }
        ),
        encoding="utf-8",
    )
    calls: list[dict[str, object]] = []

    class FakeColBERT(torch.nn.Module):
        def __init__(self, model_name_or_path: str, **kwargs: object) -> None:
            super().__init__()
            calls.append({"model_name_or_path": model_name_or_path, **kwargs})
            self.projection = torch.nn.Linear(2, 2)

    def fake_hf_hub_download(repo_id: str, filename: str, *, revision: str | None = None) -> str:
        assert repo_id == "mixedbread-ai/mxbai-edge-colbert-v0-17m"
        assert filename == "config_sentence_transformers.json"
        assert revision == "main"
        return str(config_path)

    monkeypatch.setattr("huggingface_hub.hf_hub_download", fake_hf_hub_download)
    monkeypatch.setattr("hakari_bench.models._import_pylate_colbert", lambda: FakeColBERT)

    model = load_model(
        ModelLoadConfig(
            model_name_or_path="mixedbread-ai/mxbai-edge-colbert-v0-17m",
            model_type="late-interaction",
            model_revision="main",
            dtype="fp32",
            device="cpu",
        )
    )

    assert isinstance(model, FakeColBERT)
    assert calls == [
        {
            "model_name_or_path": "mixedbread-ai/mxbai-edge-colbert-v0-17m",
            "device": "cpu",
            "revision": "main",
            "trust_remote_code": False,
            "model_kwargs": {"torch_dtype": torch.float32},
            "query_length": 48,
            "document_length": 512,
            "query_prefix": "[Q] ",
            "document_prefix": "[D] ",
            "do_query_expansion": False,
            "attend_to_expansion_tokens": False,
        }
    ]


def test_load_model_accepts_late_interaction_config_without_model_type(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    config_path = tmp_path / "config_sentence_transformers.json"
    config_path.write_text(
        json.dumps(
            {
                "similarity_fn_name": "MaxSim",
                "query_prefix": "[Q] ",
                "document_prefix": "[D] ",
                "query_length": 48,
                "document_length": 300,
                "do_query_expansion": True,
            }
        ),
        encoding="utf-8",
    )
    calls: list[dict[str, object]] = []

    class FakeColBERT(torch.nn.Module):
        def __init__(self, model_name_or_path: str, **kwargs: object) -> None:
            super().__init__()
            calls.append({"model_name_or_path": model_name_or_path, **kwargs})
            self.projection = torch.nn.Linear(2, 2)

    monkeypatch.setattr("huggingface_hub.hf_hub_download", lambda *_args, **_kwargs: str(config_path))
    monkeypatch.setattr("hakari_bench.models._import_pylate_colbert", lambda: FakeColBERT)

    model = load_model(
        ModelLoadConfig(
            model_name_or_path="lightonai/GTE-ModernColBERT-v1",
            model_type="late-interaction",
            dtype="fp32",
            device="cpu",
        )
    )

    assert isinstance(model, FakeColBERT)
    assert calls[0]["query_length"] == 48
    assert calls[0]["document_length"] == 300
    assert calls[0]["query_prefix"] == "[Q] "
    assert calls[0]["document_prefix"] == "[D] "
    assert calls[0]["do_query_expansion"] is True


def test_load_model_defaults_late_interaction_query_expansion_to_false(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[dict[str, object]] = []

    class FakeColBERT(torch.nn.Module):
        def __init__(self, model_name_or_path: str, **kwargs: object) -> None:
            super().__init__()
            calls.append({"model_name_or_path": model_name_or_path, **kwargs})
            self.projection = torch.nn.Linear(2, 2)

    def missing_config(_repo_id: str, _filename: str, *, revision: str | None = None) -> str:
        del revision
        raise FileNotFoundError

    monkeypatch.setattr("huggingface_hub.hf_hub_download", missing_config)
    monkeypatch.setattr("hakari_bench.models._import_pylate_colbert", lambda: FakeColBERT)

    model = load_model(
        ModelLoadConfig(
            model_name_or_path="answerdotai/answerai-colbert-small-v1",
            model_type="late-interaction",
            dtype="fp32",
            device="cpu",
        )
    )

    assert isinstance(model, FakeColBERT)
    assert calls == [
        {
            "model_name_or_path": "answerdotai/answerai-colbert-small-v1",
            "device": "cpu",
            "revision": None,
            "trust_remote_code": False,
            "model_kwargs": {"torch_dtype": torch.float32},
            "do_query_expansion": False,
        }
    ]


def test_load_model_honors_late_interaction_config_query_expansion_true(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    config_path = tmp_path / "config_sentence_transformers.json"
    config_path.write_text(
        json.dumps(
            {
                "model_type": "ColBERT",
                "do_query_expansion": True,
            }
        ),
        encoding="utf-8",
    )
    calls: list[dict[str, object]] = []

    class FakeColBERT(torch.nn.Module):
        def __init__(self, model_name_or_path: str, **kwargs: object) -> None:
            super().__init__()
            calls.append({"model_name_or_path": model_name_or_path, **kwargs})
            self.projection = torch.nn.Linear(2, 2)

    monkeypatch.setattr("huggingface_hub.hf_hub_download", lambda *_args, **_kwargs: str(config_path))
    monkeypatch.setattr("hakari_bench.models._import_pylate_colbert", lambda: FakeColBERT)

    model = load_model(
        ModelLoadConfig(
            model_name_or_path="model/with-query-expansion",
            model_type="late-interaction",
            dtype="fp32",
            device="cpu",
        )
    )

    assert isinstance(model, FakeColBERT)
    assert calls[0]["do_query_expansion"] is True


def test_load_model_falls_back_to_colbert_adapter_when_pylate_load_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[dict[str, object]] = []

    class BrokenColBERT(torch.nn.Module):
        def __init__(self, model_name_or_path: str, **kwargs: object) -> None:
            del model_name_or_path, kwargs
            raise KeyError("activation_function")

    class FakeAdapter(torch.nn.Module):
        projection = torch.nn.Linear(2, 2)

        @classmethod
        def from_pretrained(cls, model_name_or_path: str, **kwargs: object) -> "FakeAdapter":
            calls.append({"model_name_or_path": model_name_or_path, **kwargs})
            return cls()

    monkeypatch.setattr("hakari_bench.models._import_pylate_colbert", lambda: BrokenColBERT)
    monkeypatch.setattr("hakari_bench.models.ColbertLateInteractionAdapter", FakeAdapter)

    model = load_model(
        ModelLoadConfig(
            model_name_or_path="answerdotai/answerai-colbert-small-v1",
            model_type="late-interaction",
            dtype="fp32",
            device="cpu",
            late_interaction_query_length=32,
            late_interaction_document_length=300,
            late_interaction_query_prefix="[Q]",
            late_interaction_document_prefix="[D]",
        )
    )

    assert isinstance(model, FakeAdapter)
    assert calls == [
        {
            "model_name_or_path": "answerdotai/answerai-colbert-small-v1",
            "device": "cpu",
            "revision": None,
            "trust_remote_code": False,
            "model_kwargs": {"torch_dtype": torch.float32},
            "query_length": 32,
            "document_length": 300,
            "query_prefix": "[Q]",
            "document_prefix": "[D]",
            "do_query_expansion": False,
            "attend_to_expansion_tokens": None,
        }
    ]


def test_colbert_adapter_applies_role_prefix_tokens_lengths_and_masks() -> None:
    calls: list[dict[str, object]] = []

    class FakeTokenizer:
        model_max_length = 512
        mask_token_id = 103
        unk_token_id = 100
        pad_token_id = 0

        def convert_tokens_to_ids(self, token: str) -> int:
            return {
                "[unused0]": 1,
                "[unused1]": 2,
                ".": 9,
            }.get(token, 100)

        def __call__(self, sentences: list[str], **kwargs: object) -> dict[str, torch.Tensor]:
            calls.append({"sentences": sentences, **kwargs})
            if kwargs["padding"] == "max_length":
                return {
                    "input_ids": torch.tensor([[101, 10, 102, 103, 103], [101, 11, 12, 102, 103]]),
                    "attention_mask": torch.tensor([[1, 1, 1, 0, 0], [1, 1, 1, 1, 0]]),
                }
            return {
                "input_ids": torch.tensor([[101, 20, 9, 102, 0]]),
                "attention_mask": torch.tensor([[1, 1, 1, 1, 0]]),
            }

    class FakeBackbone(torch.nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.config = type("Config", (), {"hidden_size": 2})()

        def forward(self, **kwargs: torch.Tensor) -> object:
            batch_size, token_count = kwargs["input_ids"].shape
            hidden = kwargs["input_ids"].float().unsqueeze(-1).repeat(1, 1, 2)
            return type("Output", (), {"last_hidden_state": hidden.reshape(batch_size, token_count, 2)})()

    model = ColbertLateInteractionAdapter(
        model_name_or_path="toy",
        tokenizer=FakeTokenizer(),
        backbone=FakeBackbone(),
        projection=None,
        device="cpu",
        query_prefix="[unused0]",
        document_prefix="[unused1]",
        query_length=32,
        document_length=300,
        do_query_expansion=True,
    )

    query_embeddings = model.encode(["hello", "world"], is_query=True, convert_to_tensor=True)
    document_embeddings = model.encode(["doc"], is_query=False, convert_to_tensor=True)

    assert calls[0]["sentences"] == ["hello", "world"]
    assert calls[0]["max_length"] == 31
    assert calls[0]["padding"] == "max_length"
    assert calls[1]["sentences"] == ["doc"]
    assert calls[1]["max_length"] == 299
    assert calls[1]["padding"] is True
    assert len(query_embeddings) == 2
    assert query_embeddings[0].shape[0] == 6
    assert len(document_embeddings) == 1
    assert document_embeddings[0].shape[0] == 4


def test_load_model_reranker_passes_cross_encoder_kwargs(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[dict[str, object]] = []

    class FakeCrossEncoder(torch.nn.Module):
        def __init__(self, model_name_or_path: str, **kwargs: object) -> None:
            super().__init__()
            calls.append({"model_name_or_path": model_name_or_path, **kwargs})
            self.model = torch.nn.Linear(2, 1)

    monkeypatch.setattr("hakari_bench.models._import_cross_encoder", lambda: FakeCrossEncoder)

    model = load_model(
        ModelLoadConfig(
            model_name_or_path="Qwen/Qwen3-Reranker-0.6B",
            model_type="reranker",
            dtype="bf16",
            device="cuda:0",
            trust_remote_code=True,
            cross_encoder_kwargs={
                "prompts": {"retrieval": "Retrieve relevant passages"},
                "default_prompt_name": "retrieval",
                "model_kwargs": {"attn_implementation": "sdpa"},
            },
        )
    )

    assert isinstance(model, FakeCrossEncoder)
    assert calls == [
        {
            "model_name_or_path": "Qwen/Qwen3-Reranker-0.6B",
            "prompts": {"retrieval": "Retrieve relevant passages"},
            "default_prompt_name": "retrieval",
            "device": "cuda:0",
            "revision": None,
            "trust_remote_code": True,
            "model_kwargs": {
                "torch_dtype": torch.bfloat16,
                "attn_implementation": "sdpa",
            },
        }
    ]


def test_load_model_passes_model_revision_to_huggingface_loaders(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[dict[str, object]] = []

    class FakeSentenceTransformer(torch.nn.Module):
        def __init__(self, model_name_or_path: str, **kwargs: object) -> None:
            super().__init__()
            calls.append({"model_name_or_path": model_name_or_path, **kwargs})
            self.projection = torch.nn.Linear(2, 2)

    monkeypatch.setattr("hakari_bench.models._import_sentence_transformer", lambda: FakeSentenceTransformer)

    load_model(
        ModelLoadConfig(
            model_name_or_path="hotchpotch/model",
            model_type="dense",
            dtype="bf16",
            device="cpu",
            trust_remote_code=True,
            model_revision="abc123",
        )
    )

    assert calls[0]["revision"] == "abc123"


def test_resolve_model_revision_uses_full_huggingface_sha(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeInfo:
        sha = "0123456789abcdef0123456789abcdef01234567"

    class FakeHfApi:
        def model_info(self, *, repo_id: str, revision: str | None = None) -> FakeInfo:
            assert repo_id == "hotchpotch/model"
            assert revision == "main"
            return FakeInfo()

    monkeypatch.setattr("hakari_bench.models.HfApi", FakeHfApi)
    resolve_model_revision.cache_clear()

    assert resolve_model_revision("hotchpotch/model", requested_revision="main") == {
        "requested": "main",
        "resolved": "0123456789abcdef0123456789abcdef01234567",
        "source": "huggingface_hub",
    }


def test_collect_model_metadata_counts_parameters() -> None:
    model = torch.nn.Sequential(torch.nn.Linear(3, 2), torch.nn.Linear(2, 1))
    args = argparse.Namespace(
        model="toy",
        model_type="dense",
        dtype="bf16",
        device="cpu",
        trust_remote_code=False,
        attn_implementation=None,
        flash_attn2=False,
        model_revision=None,
    )

    metadata = collect_model_metadata(model, args)

    assert metadata["method"] == "dense"
    assert metadata["id"] == "toy"
    assert metadata["source"] == {"type": "huggingface", "name": "toy"}
    assert metadata["total_parameters"] == 11
    assert metadata["trainable_parameters"] == 11
    assert metadata["embedding_parameters"] is None
    assert metadata["active_parameters"] is None


def test_collect_model_metadata_records_model_revision(monkeypatch: pytest.MonkeyPatch) -> None:
    model = torch.nn.Sequential(torch.nn.Linear(3, 2))
    args = argparse.Namespace(
        model="hotchpotch/model",
        model_type="dense",
        dtype="bf16",
        device="cpu",
        trust_remote_code=False,
        attn_implementation=None,
        flash_attn2=False,
        model_revision="main",
        model_source={"type": "huggingface", "name": "hotchpotch/model", "revision_requested": "main"},
    )

    monkeypatch.setattr(
        "hakari_bench.models.resolve_model_revision",
        lambda model_id, requested_revision=None: {
            "requested": requested_revision,
            "resolved": "0123456789abcdef0123456789abcdef01234567",
            "source": "huggingface_hub",
        },
    )

    metadata = collect_model_metadata(model, args)

    assert metadata["source"] == {
        "type": "huggingface",
        "name": "hotchpotch/model",
        "revision_requested": "main",
        "revision": "0123456789abcdef0123456789abcdef01234567",
    }


def test_collect_model_metadata_counts_active_parameters_from_input_embeddings() -> None:
    model = _FakeSentenceTransformerLike(backbone_attr="auto_model")
    args = _metadata_args()

    metadata = collect_model_metadata(model, args)

    assert metadata["total_parameters"] == 38
    assert metadata["trainable_parameters"] == 38
    assert metadata["embedding_parameters"] == 20
    assert metadata["active_parameters"] == 18


def test_collect_model_metadata_counts_active_parameters_from_st_model_attribute() -> None:
    model = _FakeSentenceTransformerLike(backbone_attr="model")
    args = _metadata_args()

    metadata = collect_model_metadata(model, args)

    assert metadata["total_parameters"] == 38
    assert metadata["embedding_parameters"] == 20
    assert metadata["active_parameters"] == 18


def test_collect_model_metadata_counts_static_embedding_table_as_input_embeddings() -> None:
    model = _FakeStaticSentenceTransformerLike()
    args = _metadata_args()

    metadata = collect_model_metadata(model, args)

    assert metadata["total_parameters"] == 20
    assert metadata["embedding_parameters"] == 20
    assert metadata["active_parameters"] == 0


def test_collect_model_metadata_records_late_interaction_metadata() -> None:
    model = _FakeLateInteractionModel()
    args = _metadata_args()
    args.model_type = "late-interaction"

    metadata = collect_model_metadata(model, args)

    assert metadata["backend_library"] == "pylate"
    assert metadata["similarity_fn_name"] == "MaxSim"
    assert metadata["late_interaction"] == {
        "architecture": "colbert",
        "scoring": "maxsim",
        "query_prefix": "[Q] ",
        "document_prefix": "[D] ",
        "query_length": 32,
        "document_length": 300,
        "do_query_expansion": True,
        "attend_to_expansion_tokens": False,
    }


def _metadata_args() -> argparse.Namespace:
    return argparse.Namespace(
        model="toy",
        model_type="dense",
        dtype="bf16",
        device="cpu",
        trust_remote_code=False,
        attn_implementation=None,
        flash_attn2=False,
    )


class _FakeSentenceTransformerLike(torch.nn.Module):
    def __init__(self, *, backbone_attr: str) -> None:
        super().__init__()
        self.add_module("0", _FakeTransformerModule(backbone_attr=backbone_attr))

    def __getitem__(self, index: int) -> torch.nn.Module:
        module = self._modules[str(index)]
        assert isinstance(module, torch.nn.Module)
        return module


class _FakeStaticSentenceTransformerLike(torch.nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.add_module("0", _FakeStaticEmbeddingModule())

    def __getitem__(self, index: int) -> torch.nn.Module:
        module = self._modules[str(index)]
        assert isinstance(module, torch.nn.Module)
        return module


class _FakeStaticEmbeddingModule(torch.nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.embedding = torch.nn.Embedding(5, 4)


class _FakeLateInteractionModel(torch.nn.Module):
    similarity_fn_name = "MaxSim"
    max_seq_length = None
    query_prefix = "[Q] "
    document_prefix = "[D] "
    query_length = 32
    document_length = 300
    do_query_expansion = True
    attend_to_expansion_tokens = False

    def __init__(self) -> None:
        super().__init__()
        self.projection = torch.nn.Linear(2, 2)


class _FakeTransformerModule(torch.nn.Module):
    def __init__(self, *, backbone_attr: str) -> None:
        super().__init__()
        self.add_module(backbone_attr, _FakeBackbone())


class _FakeBackbone(torch.nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.embeddings = torch.nn.Module()
        self.input_embeddings = torch.nn.Embedding(5, 4)
        self.embeddings.tok_embeddings = self.input_embeddings
        self.layers = torch.nn.ModuleList([torch.nn.Linear(4, 3, bias=False)])
        self.final_norm = torch.nn.LayerNorm(3)

    def get_input_embeddings(self) -> torch.nn.Embedding:
        return self.input_embeddings


class _FakeConfig:
    def __init__(self) -> None:
        self._attn_implementation = "sdpa"


class _FakeNestedModel(torch.nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.config = _FakeConfig()


class FakeCustomModule(torch.nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.model = _FakeNestedModel()
