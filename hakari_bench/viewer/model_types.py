from __future__ import annotations


MODEL_TYPE_FILTER_ORDER = ("dense", "sparse", "late-interaction", "reranker")
MODEL_TYPE_FILTER_LABELS = {
    "dense": "Dense",
    "sparse": "Sparse / BM25",
    "late-interaction": "Late interaction",
    "reranker": "Reranker",
}


def normalized_model_type(*, model_name: str, model_type: str | None = None) -> str:
    if isinstance(model_type, str):
        normalized = model_type.strip().casefold().replace("_", "-")
        if normalized in {"dense", "sparse", "reranker", "late-interaction", "bm25"}:
            return normalized
        if normalized in {"cross-encoder", "crossencoder", "cross-encoder-reranker"}:
            return "reranker"
        if normalized in {"late-interaction-retriever", "colbert"}:
            return "late-interaction"

    name = model_name.casefold()
    if name == "bm25" or name.startswith("bm25/") or name.endswith("/bm25"):
        return "bm25"
    return "dense"


def model_type_filter_key(*, model_name: str, model_type: str | None = None) -> str:
    normalized = normalized_model_type(model_name=model_name, model_type=model_type)
    return "sparse" if normalized == "bm25" else normalized


def is_bm25_model(*, model_name: str, model_type: str | None = None) -> bool:
    return normalized_model_type(model_name=model_name, model_type=model_type) == "bm25"


def is_reranker_model(*, model_name: str, model_type: str | None = None) -> bool:
    return normalized_model_type(model_name=model_name, model_type=model_type) == "reranker"
