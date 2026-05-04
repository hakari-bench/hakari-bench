from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import torch
from scipy import sparse


@dataclass(frozen=True)
class QuantizedEmbeddingMatrix:
    values: Any
    precision: str
    original_dim: int
    algorithm: str
    method: str
    side: str
    ranges_source: str | None = None
    ranges: Any | None = None
    rounding: str | None = None
    score_representation: str | None = None
    source_values: Any | None = None
    binary_encoding: str | None = None

    @property
    def shape(self) -> tuple[int, ...]:
        return tuple(int(dimension) for dimension in self.values.shape)

    @property
    def dtype(self) -> Any:
        return self.values.dtype


def take_embedding_rows(embeddings: Any, indices: list[int]) -> Any:
    if isinstance(embeddings, QuantizedEmbeddingMatrix):
        return QuantizedEmbeddingMatrix(
            values=take_embedding_rows(embeddings.values, indices),
            precision=embeddings.precision,
            original_dim=embeddings.original_dim,
            algorithm=embeddings.algorithm,
            method=embeddings.method,
            side=embeddings.side,
            ranges_source=embeddings.ranges_source,
            ranges=embeddings.ranges,
            rounding=embeddings.rounding,
            score_representation=embeddings.score_representation,
            source_values=(
                take_embedding_rows(embeddings.source_values, indices)
                if embeddings.source_values is not None
                else None
            ),
            binary_encoding=embeddings.binary_encoding,
        )
    if isinstance(embeddings, torch.Tensor):
        index_tensor = torch.as_tensor(indices, dtype=torch.long, device=embeddings.device)
        if embeddings.layout == torch.sparse_csr:
            return embeddings.to_sparse_coo().index_select(0, index_tensor)
        return embeddings.index_select(0, index_tensor)
    if sparse.issparse(embeddings):
        return embeddings[indices]
    if isinstance(embeddings, np.ndarray):
        return embeddings[indices]
    if isinstance(embeddings, list | tuple):
        return [embeddings[index] for index in indices]
    try:
        return embeddings[indices]
    except Exception as exc:
        raise TypeError(f"Unsupported embedding type for row selection: {type(embeddings).__name__}") from exc
