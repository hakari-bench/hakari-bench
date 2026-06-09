from __future__ import annotations

import argparse
from types import SimpleNamespace
from typing import Any

import pytest
import torch

from hakari_bench.models import (
    ColbertLateInteractionAdapter,
    ModelLoadConfig,
    _patch_pylate_dense_missing_activation_function,
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


def test_load_model_uses_custom_loader() -> None:
    model = load_model(
        ModelLoadConfig(
            model_name_or_path="dummy/model",
            model_type="dense",
            model_loader="examples.custom_backends.dummy_backend:load_model",
            model_loader_kwargs={"scale": 2.0, "backend_name": "test-dummy"},
        )
    )

    assert model.metadata()["backend_library"] == "hakari-dummy"
    assert model.metadata()["backend_name"] == "test-dummy"
    assert model.scale == 2.0


def test_load_model_validates_custom_loader_capabilities(monkeypatch: pytest.MonkeyPatch) -> None:
    class InvalidModel:
        pass

    def fake_loader(_config: ModelLoadConfig) -> InvalidModel:
        return InvalidModel()

    monkeypatch.setattr("hakari_bench.models._import_loader_factory", lambda _loader: fake_loader)

    with pytest.raises(TypeError, match="dense model backends must expose"):
        load_model(
            ModelLoadConfig(
                model_name_or_path="dummy/model",
                model_type="dense",
                model_loader="tests.fake:load_model",
            )
        )


def test_pylate_dense_patch_defaults_missing_activation_function(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakePylateDense:
        def __init__(self, **config: object) -> None:
            self.config = config
            self.loaded_state = None

        @staticmethod
        def from_sentence_transformers(dense: Any) -> object:
            config = dense.get_config_dict()
            config["activation_function"]
            raise AssertionError("unreachable")

        def load_state_dict(self, state: dict[str, object]) -> None:
            self.loaded_state = state

    class FakeSentenceTransformersDense:
        def get_config_dict(self) -> dict[str, object]:
            return {"in_features": 3, "out_features": 2, "bias": False}

        def state_dict(self) -> dict[str, object]:
            return {"linear.weight": "weights"}

    def fake_import_module(name: str) -> object:
        if name == "pylate.models":
            return SimpleNamespace(Dense=FakePylateDense)
        if name == "sentence_transformers.util":
            return SimpleNamespace(import_from_string=lambda dotted: torch.nn.Identity)
        raise AssertionError(f"unexpected import: {name}")

    monkeypatch.setattr("hakari_bench.models.importlib.import_module", fake_import_module)

    _patch_pylate_dense_missing_activation_function()
    model = FakePylateDense.from_sentence_transformers(FakeSentenceTransformersDense())

    assert isinstance(model, FakePylateDense)
    assert isinstance(model.config["activation_function"], torch.nn.Identity)
    assert model.loaded_state == {"linear.weight": "weights"}


def test_colbert_adapter_encode_uses_role_prefix_token_ids() -> None:
    class FakeTokenizer:
        model_max_length = 8
        mask_token_id = 99
        pad_token_id = 0

        def convert_tokens_to_ids(self, token: str) -> int:
            return {"[unused0]": 1, "[unused1]": 2, ".": 4}.get(token, 50)

        def __call__(self, sentences: list[str], **kwargs: object) -> dict[str, torch.Tensor]:
            assert kwargs["max_length"] == 4
            ids: list[list[int]] = []
            masks: list[list[int]] = []
            padding = kwargs.get("padding")
            for sentence in sentences:
                row = [101, 10 + len(sentence), 102]
                max_length = kwargs["max_length"]
                assert isinstance(max_length, int)
                if len(row) < max_length and padding in {"max_length", True}:
                    row = row + [self.pad_token_id] * (max_length - len(row))
                ids.append(row)
                masks.append([0 if token_id == self.pad_token_id else 1 for token_id in row])
            return {
                "input_ids": torch.tensor(ids, dtype=torch.long),
                "attention_mask": torch.tensor(masks, dtype=torch.long),
            }

    class FakeBackbone(torch.nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.weight = torch.nn.Parameter(torch.ones(1))
            self.calls: list[torch.Tensor] = []

        def forward(self, **features: torch.Tensor) -> SimpleNamespace:
            input_ids = features["input_ids"]
            self.calls.append(input_ids.detach().cpu())
            hidden = torch.stack(
                [
                    input_ids.float(),
                    input_ids.float() + 1,
                    input_ids.float() + 2,
                    input_ids.float() + 3,
                ],
                dim=-1,
            )
            return SimpleNamespace(last_hidden_state=hidden)

    tokenizer = FakeTokenizer()
    backbone = FakeBackbone()
    model = ColbertLateInteractionAdapter(
        model_name_or_path="colbert-ir/colbertv2.0",
        tokenizer=tokenizer,
        backbone=backbone,
        projection=None,
        device="cpu",
        query_prefix="[unused0]",
        document_prefix="[unused1]",
        query_length=5,
        document_length=5,
    )

    query_embeddings = model.encode(["q"], is_query=True, convert_to_numpy=False)
    document_embeddings = model.encode(["doc"], is_query=False, convert_to_numpy=False)

    assert backbone.calls[0][0].tolist() == [101, 1, 11, 102, 99]
    assert backbone.calls[1][0].tolist()[:4] == [101, 2, 13, 102]
    assert len(query_embeddings[0]) == 5
    assert len(document_embeddings[0]) == 4


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


def test_collect_model_metadata_records_custom_backend_metadata() -> None:
    class CustomModel:
        similarity_fn_name = "dot"

        def metadata(self) -> dict[str, object]:
            return {
                "backend_library": "custom-api",
                "provider_model": "embed-v1",
                "api_token": "should-not-leak",
            }

    args = argparse.Namespace(
        model="api/embed-v1",
        model_id="api/embed-v1",
        model_type="dense",
        dtype="bf16",
        device=None,
        trust_remote_code=False,
        attn_implementation=None,
        flash_attn2=False,
        model_revision=None,
        model_source={"type": "custom", "name": "api/embed-v1"},
        model_loader="pkg.loader:load_model",
        model_loader_kwargs={"endpoint": "https://example.test", "api_key": "secret"},
    )

    metadata = collect_model_metadata(CustomModel(), args)

    assert metadata["backend_library"] == "custom-api"
    assert metadata["backend"] == {
        "loader": "pkg.loader:load_model",
        "loader_kwargs": {"endpoint": "https://example.test", "api_key": "<redacted>"},
    }
    assert metadata["backend_metadata"] == {
        "backend_library": "custom-api",
        "provider_model": "embed-v1",
        "api_token": "<redacted>",
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
