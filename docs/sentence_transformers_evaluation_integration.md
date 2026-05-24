# SentenceTransformers Evaluation Integration

HAKARI-Bench provides SentenceTransformers-compatible evaluators under
`hakari_bench.sentence_transformers`. They are designed for training-time
feedback on Nano-style IR datasets while reusing HAKARI dataset definitions,
BM25 candidate subsets, and IR scoring code.

The default path is intentionally small. It computes only `nDCG@10` and
`mAP@10`, then reports task-level metrics and combined means across the selected
tasks:

- `HakariNano_combined_nDCG@10`
- `HakariNano_combined_mAP@10`

Use this integration when a SentenceTransformers training loop needs a quick,
repeatable retrieval signal. Use the HAKARI CLI benchmark runner when you need
full result JSON, leaderboard-comparable metadata, embedding variant grids, or
coverage audits.

Relevant upstream references:

- <https://sbert.net/docs/package_reference/sentence_transformer/trainer.html>
- <https://sbert.net/docs/package_reference/sparse_encoder/trainer.html>
- <https://sbert.net/docs/package_reference/cross_encoder/trainer.html>
- <https://github.com/huggingface/sentence-transformers/blob/main/sentence_transformers/sentence_transformer/evaluation/nano_beir.py>
- <https://github.com/huggingface/sentence-transformers/blob/main/sentence_transformers/sparse_encoder/evaluation/sparse_nano_beir.py>
- <https://github.com/huggingface/sentence-transformers/blob/main/sentence_transformers/cross_encoder/evaluation/nano_beir.py>

## Evaluator Types

The integration follows the SentenceTransformers `BaseEvaluator` contract and
can be passed to these trainers:

- `HakariNanoEmbeddingEvaluator` for `SentenceTransformerTrainer`
- `HakariNanoEmbeddingEvaluator` for `SparseEncoderTrainer`
- `HakariNanoRerankerEvaluator` for `CrossEncoderTrainer`
- `HakariNanoBM25Evaluator` for BM25-only logging without a neural model

Dense and sparse models share `HakariNanoEmbeddingEvaluator` because HAKARI's
embedding scorer accepts both dense arrays and SentenceTransformers sparse
outputs.

## What Runs During Evaluation

For each selected task, the evaluator does the following work:

1. Resolves `HakariNanoTarget` values to HAKARI `EvalTask` objects.
2. Loads queries, corpus, qrels, and optionally a candidate subset such as BM25.
3. Applies deterministic query sampling when `query_limit` is set.
4. Keeps the full corpus by default, or uses `corpus_policy="sampled_candidates"`
   for smoke runs.
5. Scores retrieval:
   - dense/sparse: encode queries and documents, then rank documents by model
     similarity.
   - reranker: rerank the configured candidate subset.
   - BM25: read dataset candidates or compute BM25 locally.
6. Computes only the requested IR metrics.
7. Returns task-level metrics plus combined means across all selected tasks.

The evaluator returns a plain `dict[str, float]`. SentenceTransformers prefixes
those keys with `eval_` when logging through a trainer.

## Default Metrics

The default metric list is:

```python
("nDCG@10", "mAP@10")
```

Task-level metric keys use lower-case metric suffixes because they come from
HAKARI's IR metric implementation:

```text
NanoMIRACL_en_cosine_ndcg@10
NanoMIRACL_en_cosine_map@10
```

Combined metric keys use display names intended for training logs:

```text
HakariNano_combined_nDCG@10
HakariNano_combined_mAP@10
```

`combined_nDCG@10` is the arithmetic mean of the selected task `ndcg@10`
values. `combined_mAP@10` is the arithmetic mean of the selected task `map@10`
values. The default `primary_metric` is `HakariNano_combined_nDCG@10`.

Use `metrics` to request a different small set:

```python
evaluator = HakariNanoEmbeddingEvaluator(
    targets=[HakariNanoTarget(dataset="NanoMIRACL", splits=["en"])],
    metrics=["acc@1", "nDCG@10", "mAP@10"],
)
```

This computes only `acc@1`, `ndcg@10`, and `map@10`. It does not compute
precision, recall, MRR, or other cutoffs unless requested.

## Target Selection

Use `HakariNanoTarget` to select full datasets, collections, or specific
splits/tasks.

```python
from hakari_bench.sentence_transformers import HakariNanoTarget

targets = [
    HakariNanoTarget(dataset="NanoMIRACL", splits=["en"]),
    HakariNanoTarget(dataset="NanoCoIR"),
    HakariNanoTarget(dataset="NanoMMTEB-v2"),
]
```

The examples use this set because it gives:

- NanoMIRACL English only
- all NanoCoIR tasks
- all NanoMMTEB-v2 tasks

For a single task, pass a split/task name through `splits`:

```python
HakariNanoTarget(dataset="NanoMIRACL", splits=["en"])
```

For tests or custom applications that already resolved tasks, pass `tasks`:

```python
HakariNanoTarget(tasks=[my_eval_task])
```

## Dense Or Sparse Training

Use `HakariNanoEmbeddingEvaluator` for dense `SentenceTransformer` models and
sparse `SparseEncoder` models.

```python
from hakari_bench.sentence_transformers import HakariNanoEmbeddingEvaluator, HakariNanoTarget

evaluator = HakariNanoEmbeddingEvaluator(
    targets=[
        HakariNanoTarget(dataset="NanoMIRACL", splits=["en"]),
        HakariNanoTarget(dataset="NanoCoIR"),
        HakariNanoTarget(dataset="NanoMMTEB-v2"),
    ],
    batch_size=32,
    metrics=["nDCG@10", "mAP@10"],
    query_limit=50,
    query_sample_seed=13,
    candidate_ranking="reranking_hybrid",
)
```

Use the primary metric with SentenceTransformers trainer arguments:

```python
training_args = SentenceTransformerTrainingArguments(
    output_dir="output/sentence_transformers/dense_hakari",
    eval_strategy="steps",
    eval_steps=500,
    save_strategy="steps",
    save_steps=500,
    load_best_model_at_end=True,
    metric_for_best_model=f"eval_{evaluator.primary_metric}",
)
```

With default settings, `evaluator.primary_metric` is:

```text
HakariNano_combined_nDCG@10
```

## Reranker Training

Use `HakariNanoRerankerEvaluator` with a SentenceTransformers `CrossEncoder`.
The evaluator requires a candidate ranking, usually the built-in
`reranking_hybrid` candidate subset.

```python
from hakari_bench.sentence_transformers import HakariNanoRerankerEvaluator, HakariNanoTarget

evaluator = HakariNanoRerankerEvaluator(
    targets=[HakariNanoTarget(dataset="NanoMIRACL", splits=["en"])],
    metrics=["nDCG@10", "mAP@10"],
)
```

The default evaluator name uses `Rall` when no explicit rerank depth is set:

```text
HakariNano_Rall_combined_nDCG@10
HakariNano_Rall_combined_mAP@10
```

The example script keeps `CUDA_VISIBLE_DEVICES=0` by default because
SentenceTransformers' `BinaryCrossEntropyLoss` calls `CrossEncoder.preprocess`,
which is hidden if the trainer wraps the cross encoder with
`torch.nn.DataParallel`.

## BM25-Only Evaluation

Use `HakariNanoBM25Evaluator` when a training script should log a BM25 baseline
alongside model metrics. It does not require a neural model.

```python
from hakari_bench.sentence_transformers import HakariNanoBM25Evaluator, HakariNanoTarget

evaluator = HakariNanoBM25Evaluator(
    targets=[HakariNanoTarget(dataset="NanoMIRACL", splits=["en"])],
    bm25_source="dataset",
    metrics=["nDCG@10", "mAP@10"],
)
metrics = evaluator()
```

`bm25_source="dataset"` evaluates the dataset-provided candidate subset.
`bm25_source="computed"` recomputes BM25 locally with `bm25s`.

Default combined keys are:

```text
HakariNanoBM25_combined_nDCG@10
HakariNanoBM25_combined_mAP@10
```

## Query Sampling And Smoke Runs

Most Nano tasks have small query sets, but training-time evaluation can still be
expensive because each evaluation may encode the full corpus. Use `query_limit`
to reduce the number of queries:

```python
evaluator = HakariNanoEmbeddingEvaluator(
    targets=[HakariNanoTarget(dataset="NanoMIRACL", splits=["en"])],
    query_limit=50,
    query_sample_seed=13,
)
```

Sampling is deterministic. The same dataset, seed, and evaluator name select the
same query IDs.

`corpus_policy` controls how much corpus remains after query sampling:

- `full`: keep the original corpus. Use this for comparable evaluation.
- `sampled_candidates`: keep only sampled-query positives plus candidate docs.
  Use this for smoke tests only.

Smoke scores are not benchmark-comparable because the corpus is intentionally
reduced:

```python
evaluator = HakariNanoEmbeddingEvaluator(
    targets=[HakariNanoTarget(dataset="NanoMIRACL", splits=["en"])],
    query_limit=3,
    corpus_policy="sampled_candidates",
)
```

The example scripts expose `--smoke-train`, which reduces training samples,
evaluation samples, evaluation queries, and training steps.

## Embedding Variants

Embedding variants are separate from the default training-time path. By default,
no variants are computed. This keeps training eval simple and avoids extra
quantization or truncation work.

Use variants only when you explicitly want to compare representations such as
`int8`, `binary`, rescored quantization, or truncated dimensions:

```python
from hakari_bench.embedding_variants import parse_embedding_variants
from hakari_bench.sentence_transformers import HakariNanoEmbeddingEvaluator, HakariNanoTarget

variant_evaluator = HakariNanoEmbeddingEvaluator(
    targets=[HakariNanoTarget(dataset="NanoMIRACL", splits=["en"])],
    metrics=["nDCG@10", "mAP@10"],
    embedding_variants=parse_embedding_variants([
        "int8",
        "binary",
        "rescore:int8",
        "truncate:128",
    ]),
)
```

The dense example exposes this through `--extra-embedding-variant`:

```bash
uv run python examples/sentence_transformers/train_dense_with_hakari.py \
  --extra-embedding-variant int8 \
  --extra-embedding-variant binary \
  --extra-embedding-variant rescore:int8 \
  --extra-embedding-variant truncate:128
```

You can also group comma-separated variants:

```bash
uv run python examples/sentence_transformers/train_dense_with_hakari.py \
  --extra-embedding-variant int8,binary \
  --extra-embedding-variant rescore:int8,binary
```

Common variant specs:

| Spec | Meaning |
| --- | --- |
| `int8` | Quantize embeddings to int8 and score the quantized vectors. |
| `binary` | Quantize embeddings to binary and score the quantized vectors. |
| `rescore:int8` | Use int8 candidates, then rescore selected candidates with base embeddings. |
| `rescore:binary` | Use binary candidates, then rescore selected candidates with base embeddings. |
| `truncate:128` | Truncate embeddings to 128 dimensions before scoring. |
| `normalize` | L2-normalize embeddings before scoring. |

## How Variant Results Are Recorded

Training evaluators return variant metrics as task-level keys. For example,
`int8` on a dense dot-product model produces keys like:

```text
NanoMIRACL_en_dot_int8_ndcg@10
NanoMIRACL_en_dot_int8_map@10
```

`rescore:int8` uses the variant name `int8_rescore`:

```text
NanoMIRACL_en_dot_int8_rescore_ndcg@10
NanoMIRACL_en_dot_int8_rescore_map@10
```

`truncate:128` uses the variant name `truncate_dim_128`:

```text
NanoMIRACL_en_dot_truncate_dim_128_ndcg@10
NanoMIRACL_en_dot_truncate_dim_128_map@10
```

Combined metrics such as `HakariNano_combined_nDCG@10` are computed from the
base metrics. Variant-specific combined means are intentionally not part of the
simple training evaluator output yet.

The HAKARI CLI benchmark runner records more structured variant data in result
JSON:

```text
payload["evaluation"]["embedding_evaluations"]
```

Each `embedding_evaluations` item contains the variant name, transform metadata,
embedding metadata, selected aggregate metric, compact distance evaluations,
and best-score metadata. Ranking artifacts also include the binary qrels IDs
needed to recompute IR metrics from the saved top-100 rows:

```json
{
  "qrels": [
    {
      "query_id": "q1",
      "relevant_corpus_ids": ["d1"]
    }
  ],
  "embedding_variant_name": "int8"
}
```

Use the CLI path when variant results need to be analyzed as benchmark outputs.
Use the training evaluator path when variants are only occasional diagnostic
signals during training.

## Example Scripts

Dense training:

```bash
uv run python examples/sentence_transformers/train_dense_with_hakari.py \
  --smoke-train
```

Reranker training:

```bash
uv run python examples/sentence_transformers/train_reranker_with_hakari.py \
  --smoke-train
```

Both examples use `hotchpotch/mmBERT-L4H384-pruned` by default and train on a
small sample from `sentence-transformers/gooaq`. Their default evaluation
targets are:

- `NanoMIRACL` split `en`
- all `NanoCoIR` tasks
- all `NanoMMTEB-v2` tasks

Useful example options:

| Option | Applies to | Purpose |
| --- | --- | --- |
| `--smoke-train` | dense, reranker | Use tiny training/eval samples and few steps. |
| `--eval-query-limit N` | dense, reranker | Sample at most `N` queries per task. |
| `--hakari-metric nDCG@10` | dense, reranker | Add or override requested HAKARI metrics. |
| `--extra-embedding-variant int8` | dense | Add a separate dense embedding variant evaluation. |
| `--rerank-top-k N` | reranker | Optional limit for candidate documents reranked by the cross encoder. Omit it to rerank all provided candidates. |

## Development And Testing

Behavioral changes to this integration should follow TDD:

1. Add or update focused tests for target resolution, query sampling, evaluator
   metric keys, aggregation, and model-specific scoring paths.
2. Implement the smallest passing change.
3. Run `uv run --group all pytest tests/test_sentence_transformers_integration.py -q`.
4. Run the relevant surrounding tests, usually `tests/test_evaluation.py` and
   `tests/test_bm25.py`.
5. Run `uv run tox` before committing.
