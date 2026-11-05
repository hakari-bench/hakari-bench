from types import SimpleNamespace

import pytest

from examples.custom_backends.pplx_multivector import NativeMultiVectorBackend


@pytest.mark.parametrize("is_query", [True, False])
def test_native_role_encoder_preserves_masking_and_role_options(is_query: bool) -> None:
    calls = []

    def query(sentences, **kwargs):
        calls.append(("query", sentences, kwargs))
        return "query-vectors"

    def document(sentences, **kwargs):
        calls.append(("document", sentences, kwargs))
        return "document-vectors"

    backend = object.__new__(NativeMultiVectorBackend)
    backend.model = SimpleNamespace(encode_query=query, encode_document=document)
    result = backend.encode(["日本語。"], is_query=is_query, batch_size=2)
    role = "query" if is_query else "document"
    assert result == f"{role}-vectors"
    assert calls == [(role, ["日本語。"], {
        "batch_size": 2, "show_progress_bar": False, "convert_to_numpy": True,
    })]
