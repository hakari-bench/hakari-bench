"""Load SlideOn without recasting its intentionally FP32 sparse head."""

from typing import Any

from sentence_transformers import SparseEncoder

from hakari_bench.models import ModelLoadConfig, resolve_attn_implementation, resolve_torch_dtype


def load_model(config: ModelLoadConfig) -> SparseEncoder:
    """Keep the upstream loader's mixed precision and task preprocessing."""
    if config.model_type != "sparse":
        raise ValueError("SlideOn requires sparse evaluation.")
    if not config.trust_remote_code:
        raise ValueError("SlideOn requires reviewed, pinned remote code.")
    kwargs: dict[str, Any] = {"dtype": resolve_torch_dtype(config.dtype)}
    attention = resolve_attn_implementation(
        attn_implementation=config.attn_implementation, flash_attn2=config.flash_attn2
    )
    if attention is not None:
        kwargs["attn_implementation"] = attention
    model = SparseEncoder(
        config.model_name_or_path,
        revision=config.model_revision,
        trust_remote_code=True,
        device=config.device,
        model_kwargs=kwargs,
    )
    if config.max_seq_length is not None:
        model.max_seq_length = config.max_seq_length
    return model
