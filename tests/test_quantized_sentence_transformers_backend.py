from __future__ import annotations

import pytest

from examples.custom_backends.quantized_sentence_transformers import _parse_backend


@pytest.mark.parametrize("backend", ["torch", "onnx", "openvino"])
def test_parse_backend_accepts_sentence_transformers_backends(backend: str) -> None:
    assert _parse_backend(backend) == backend


def test_parse_backend_rejects_unknown_backend() -> None:
    with pytest.raises(ValueError, match="Unsupported SentenceTransformer backend: tensorrt"):
        _parse_backend("tensorrt")
