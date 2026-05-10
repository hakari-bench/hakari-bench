"""Nano-style information retrieval benchmark tools."""

__all__ = ["BM25Config", "DatasetRegistry", "EvalTask", "NanoDatasetSpec"]


def __getattr__(name: str):
    if name == "BM25Config":
        from hakari_bench.bm25 import BM25Config

        return BM25Config
    if name in {"DatasetRegistry", "EvalTask", "NanoDatasetSpec"}:
        from hakari_bench.datasets import DatasetRegistry, EvalTask, NanoDatasetSpec

        return {
            "DatasetRegistry": DatasetRegistry,
            "EvalTask": EvalTask,
            "NanoDatasetSpec": NanoDatasetSpec,
        }[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
