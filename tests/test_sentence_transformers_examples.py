from __future__ import annotations

import argparse

from examples.sentence_transformers.train_reranker_with_hakari import apply_smoke_train_overrides


def test_reranker_smoke_train_does_not_override_rerank_top_k() -> None:
    args = argparse.Namespace(
        smoke_train=True,
        train_samples=50_000,
        eval_samples=2_000,
        batch_size=32,
        eval_steps=500,
        save_steps=500,
        num_train_epochs=3.0,
        rerank_top_k=100,
        eval_query_limit=None,
    )

    updated = apply_smoke_train_overrides(args)

    assert updated.train_samples == 8
    assert updated.eval_samples == 8
    assert updated.batch_size == 8
    assert updated.eval_steps == 2
    assert updated.save_steps == 2
    assert updated.num_train_epochs == 1
    assert updated.eval_query_limit == 3
    assert updated.rerank_top_k == 100
