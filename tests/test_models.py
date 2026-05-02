from __future__ import annotations

import argparse
from types import SimpleNamespace

import numpy as np
import pytest
import torch

from nano_ir_benchmark.models import (
    ColbertLateInteractionAdapter,
    ModelLoadConfig,
    collect_model_metadata,
    load_model,
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

    monkeypatch.setattr("nano_ir_benchmark.models._import_sentence_transformer", lambda: FakeSentenceTransformer)

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
            "trust_remote_code": True,
            "model_kwargs": {
                "torch_dtype": torch.bfloat16,
                "attn_implementation": "flash_attention_2",
            },
        }
    ]


def test_load_model_late_interaction_returns_colbert_adapter(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[dict[str, object]] = []

    class FakeTokenizer:
        model_max_length = 16

        def __call__(self, texts: list[str], **kwargs: object) -> dict[str, torch.Tensor]:
            calls.append({"texts": texts, **kwargs})
            return {
                "input_ids": torch.ones((len(texts), 2), dtype=torch.long),
                "attention_mask": torch.ones((len(texts), 2), dtype=torch.long),
            }

    class FakeAutoTokenizer:
        @classmethod
        def from_pretrained(cls, model_name_or_path: str, **kwargs: object) -> FakeTokenizer:
            calls.append({"tokenizer": model_name_or_path, **kwargs})
            return FakeTokenizer()

    class FakeBackbone(torch.nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.embeddings = torch.nn.Embedding(2, 2)

        def forward(self, **kwargs: object) -> SimpleNamespace:
            input_ids = kwargs["input_ids"]
            assert isinstance(input_ids, torch.Tensor)
            batch = int(input_ids.shape[0])
            hidden = torch.tensor([[[3.0, 4.0], [0.0, 2.0]]], dtype=torch.float32).repeat(batch, 1, 1)
            return SimpleNamespace(last_hidden_state=hidden.to(input_ids.device))

    class FakeAutoModel:
        @classmethod
        def from_pretrained(cls, model_name_or_path: str, **kwargs: object) -> FakeBackbone:
            calls.append({"model": model_name_or_path, **kwargs})
            return FakeBackbone()

    projection = torch.nn.Linear(2, 2, bias=False)
    projection.weight.data.copy_(torch.eye(2))

    monkeypatch.setattr("nano_ir_benchmark.models._import_auto_tokenizer", lambda: FakeAutoTokenizer)
    monkeypatch.setattr("nano_ir_benchmark.models._import_auto_model", lambda: FakeAutoModel)
    monkeypatch.setattr("nano_ir_benchmark.models._load_colbert_projection_from_hub", lambda *_, **__: projection)

    model = load_model(
        ModelLoadConfig(
            model_name_or_path="answerdotai/answerai-colbert-small-v1",
            model_type="late-interaction",
            dtype="fp32",
            device="cpu",
            trust_remote_code=True,
        )
    )

    assert isinstance(model, ColbertLateInteractionAdapter)
    assert model.similarity_fn_name == "dot"
    embeddings = model.encode(["hello"], convert_to_numpy=True)
    assert isinstance(embeddings, np.ndarray)
    assert embeddings.shape == (1, 2, 2)
    np.testing.assert_allclose(np.linalg.norm(embeddings[0], axis=1), [1.0, 1.0], atol=1e-6)
    assert calls[0] == {"tokenizer": "answerdotai/answerai-colbert-small-v1", "trust_remote_code": True}
    assert calls[1]["model"] == "answerdotai/answerai-colbert-small-v1"


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
    )

    metadata = collect_model_metadata(model, args)

    assert metadata["name_or_path"] == "toy"
    assert metadata["total_parameters"] == 11
    assert metadata["trainable_parameters"] == 11
    assert metadata["embedding_parameters"] is None
    assert metadata["active_parameters"] is None


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
