# SentenceTransformers Training Integration

HAKARI-Bench provides SentenceTransformers-compatible evaluators under
`hakari_bench.sentence_transformers`. They are intended for training-time
feedback on Nano-style IR datasets while reusing the same HAKARI dataset
definitions, BM25 candidate subsets, and metric implementation used by the CLI.

The integration follows the SentenceTransformers `BaseEvaluator` contract and
can be passed to:

- `SentenceTransformerTrainer`
- `SparseEncoderTrainer`
- `CrossEncoderTrainer`

Relevant upstream references:

- <https://sbert.net/docs/package_reference/sentence_transformer/trainer.html>
- <https://sbert.net/docs/package_reference/sparse_encoder/trainer.html>
- <https://sbert.net/docs/package_reference/cross_encoder/trainer.html>
- <https://github.com/huggingface/sentence-transformers/blob/main/sentence_transformers/sentence_transformer/evaluation/nano_beir.py>
- <https://github.com/huggingface/sentence-transformers/blob/main/sentence_transformers/sparse_encoder/evaluation/sparse_nano_beir.py>
- <https://github.com/huggingface/sentence-transformers/blob/main/sentence_transformers/cross_encoder/evaluation/nano_beir.py>

## Dense or Sparse Evaluation

Use `HakariNanoEmbeddingEvaluator` for dense `SentenceTransformer` models and
sparse `SparseEncoder` models. Sparse models are supported because HAKARI's
embedding evaluator already accepts sparse SentenceTransformers outputs.

```python
from hakari_bench.sentence_transformers import HakariNanoEmbeddingEvaluator, HakariNanoTarget

evaluator = HakariNanoEmbeddingEvaluator(
    targets=[
        HakariNanoTarget(dataset="NanoMIRACL", splits=["en"]),
        HakariNanoTarget(dataset="NanoCoIR"),
        HakariNanoTarget(dataset="NanoMMTEB-v2"),
    ],
    batch_size=32,
    query_limit=50,
    query_sample_seed=13,
)
```

The evaluator returns a metric dictionary and sets `primary_metric`, for example
`HakariNano_mean_ndcg@10`, so it can be used with
`metric_for_best_model=f"eval_{evaluator.primary_metric}"`.

## Reranker Evaluation

Use `HakariNanoRerankerEvaluator` with a SentenceTransformers `CrossEncoder`.
The evaluator reranks the configured candidate subset, usually the built-in
`bm25` ranking.

```python
from hakari_bench.sentence_transformers import HakariNanoRerankerEvaluator, HakariNanoTarget

evaluator = HakariNanoRerankerEvaluator(
    targets=[HakariNanoTarget(dataset="NanoMIRACL", splits=["en"])],
    candidate_ranking="bm25",
    rerank_top_k=100,
)
```

## BM25-Only Evaluation

Use `HakariNanoBM25Evaluator` when a training script should log the BM25
baseline alongside model metrics. It does not require a neural model.

```python
from hakari_bench.sentence_transformers import HakariNanoBM25Evaluator

evaluator = HakariNanoBM25Evaluator(bm25_source="dataset")
metrics = evaluator()
```

`bm25_source="dataset"` evaluates the dataset-provided candidate subset.
`bm25_source="computed"` recomputes BM25 locally with `bm25s`.

## Smoke Training

For quick integration checks, set `query_limit` and
`corpus_policy="sampled_candidates"`. This keeps only sampled queries plus
their qrels positives and candidate documents. It is useful for fast smoke
training, but the resulting scores are not leaderboard-comparable benchmark
results.

The example scripts under `examples/sentence_transformers/` expose
`--smoke-train` and default to:

- `NanoMIRACL` split `en`
- all `NanoCoIR` tasks
- all `NanoMMTEB-v2` tasks

## Development and Testing

Behavioral changes to the integration should follow TDD:

1. Add or update focused tests for target resolution, query sampling, evaluator
   metric keys, aggregation, and model-specific scoring paths.
2. Implement the smallest passing change.
3. Run `uv run --group all pytest -q`.
4. Run `uv run ruff check .`.
5. Run `uv run --group all ty check`.
