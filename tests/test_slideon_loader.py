from types import SimpleNamespace

import pytest
import torch

from examples.custom_backends import slideon_loader
from hakari_bench.models import ModelLoadConfig


@pytest.mark.parametrize("max_seq_length", [None, 8192])
def test_slideon_loader_preserves_upstream_mixed_precision(monkeypatch, max_seq_length):
    calls = []
    backbone = torch.nn.Linear(2, 2, dtype=torch.bfloat16)
    head = torch.nn.Linear(2, 2, dtype=torch.float32)
    upstream = SimpleNamespace(backbone=backbone, head=head, max_seq_length=8192)

    def construct(name, **kwargs):
        calls.append((name, kwargs))
        return upstream

    monkeypatch.setattr(slideon_loader, "SparseEncoder", construct)
    config = ModelLoadConfig(
        model_name_or_path="lightonai/mSlideOn",
        model_type="sparse",
        model_revision="a" * 40,
        trust_remote_code=True,
        dtype="bf16",
        flash_attn2=True,
        device="cuda:0",
        max_seq_length=max_seq_length,
    )
    model = slideon_loader.load_model(config)
    assert model is upstream
    assert model.head.weight.dtype == torch.float32
    assert model.backbone.weight.dtype == torch.bfloat16
    assert model.max_seq_length == 8192
    assert calls == [
        (
            "lightonai/mSlideOn",
            {
                "revision": "a" * 40,
                "trust_remote_code": True,
                "device": "cuda:0",
                "model_kwargs": {
                    "dtype": torch.bfloat16,
                    "attn_implementation": "flash_attention_2",
                },
            },
        )
    ]


@pytest.mark.parametrize(
    ("model_type", "trust_remote_code", "message"),
    [("dense", True, "requires sparse"), ("sparse", False, "requires reviewed")],
)
def test_slideon_loader_rejects_incompatible_settings(
    model_type, trust_remote_code, message
):
    with pytest.raises(ValueError, match=message):
        slideon_loader.load_model(
            ModelLoadConfig(
                model_name_or_path="lightonai/mSlideOn",
                model_type=model_type,
                trust_remote_code=trust_remote_code,
            )
        )
