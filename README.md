# nano-ir-bench

NanoIR Benchmark is a library, viewer, and leaderboard project for evaluating small information retrieval datasets.

Nano-style information retrieval benchmark runner for SentenceTransformers-compatible models.

Built-in dataset definitions include `NanoBEIR-en`, `NanoMIRACL`, `NanoMLDR`,
`NanoJMTEB`, `NanoRTEB`, `NanoMTEB`, `NanoCMTEB`, `NanoMMTEB`, `NanoLongEmbed`, and
`NanoCoIR`.

## Example

```bash
uv run nano-ir-bench evaluate \
  --model hotchpotch/bekko-embedding-pico-beta-unir-v7 \
  --dataset hakari-bench/NanoBEIR-en
```

The default model dtype is `bf16`; pass `--dtype fp32` or `--dtype fp16` only
when a run needs an explicit override.

Results are written under:

```text
output/results/{model_name}/{dataset_name}/{split_or_task}.json
```

For Hugging Face datasets, each task JSON records the resolved dataset repo
revision under `target.dataset_revision`. Use `--dataset-revision REV` to pin a
specific branch, tag, or commit; the resolved commit SHA is still stored.

## Sparse encoders

Sparse SentenceTransformers models can be evaluated with `--model-type sparse`.
NanoIR Benchmark requests sparse tensor output from `SparseEncoder` models and
keeps sparse embeddings in a sparse matrix format for scoring.

```bash
uv run nano-ir-bench evaluate \
  --model naver/splade-v3 \
  --model-type sparse \
  --dataset NanoBEIR-en
```

For SPLADE-style sparsity and latency trade-off checks, explicitly truncate
query and/or document sparse rows to their top weighted dimensions after
encoding:

```bash
uv run nano-ir-bench evaluate \
  --model naver/splade-v3 \
  --model-type sparse \
  --dataset NanoBEIR-en \
  --truncate-sparse-query-max-dims 32 \
  --truncate-sparse-docs-max-dims 128
```

The selected limits are written to result JSON under
`config.truncate_sparse_query_max_dims`, `config.truncate_sparse_docs_max_dims`,
and `config.sparse_truncation`, then summarized in `all.json`. Sparse embedding
metadata records `nnz_total`, `nnz_mean`, `nnz_median`, `nnz_max`, and
`density` for queries and documents.

To compare multiple sparsity limits from one full sparse model encode, use
post-encode embedding variants:

```bash
uv run nano-ir-bench evaluate \
  --model naver/splade-v3 \
  --model-type sparse \
  --dataset NanoBEIR-en \
  --embedding-variant truncate-sparse-query-max-dims:8,16,32 \
  --embedding-variant truncate-sparse-docs-max-dims:64,128,256 \
  --embedding-variant-cross truncate-sparse-query-max-dims:8,16,32 truncate-sparse-docs-max-dims:64,128,256
```

These variants keep the top absolute-value dimensions per query/document row
and record each derived result under `evaluation.embedding_evaluations`, like
dense `truncate:` variants.

Sparse embeddings intentionally do not support quantized embedding variants in
the CLI. Use post-encode sparse truncation variants for sparse footprint and
latency trade-off checks.

## Late interaction / ColBERT

ColBERT-style models can be evaluated with `--model-type late-interaction`.
The runner loads these models through PyLate ColBERT and scores query/document
token matrices with exact MaxSim. Model-specific prefixes and sequence lengths
can be passed with `--late-interaction-query-prefix`,
`--late-interaction-document-prefix`, `--late-interaction-query-length`, and
`--late-interaction-document-length`. Use
`--late-interaction-exact-doc-batch-size` and
`--late-interaction-exact-query-batch-size` to tune exact MaxSim memory use.

## Embedding variants

Derived embedding variants can be evaluated together with the base embedding
run. The model is encoded once, then every derived variant is applied through a
single post-encode transform pipeline and scored from the already-computed
embeddings. This keeps variant evaluation cheap and avoids changing model
inference behavior.

### Quantization

When dense or sparse SentenceTransformers models run on a non-CPU device, the
benchmark keeps base scoring on PyTorch tensors and performs exact score/top-k
work on that device. Dense single-vector, sparse tensor, and late-interaction
tensor shapes use this path; CPU model runs continue to use the NumPy/SciPy
paths. Use `--score-device cpu` to force post-encode score/top-k matrix work
onto CPU, which is useful for checking CUDA and CPU scoring parity.

Dense evaluation automatically runs normalized `int8` and binary quantized
search variants, plus top-100 float rescoring for both variants. The benchmark
first L2-normalizes SentenceTransformers embeddings and converts them to stored
codes, then uses exact PyTorch matrix scoring for the quantized top-k. The
post-encode score device follows `--score-device`: `auto` keeps tensor scoring
on the model output device, while `cpu` or `cuda` force quantized search matrix
work to that device. Use `--no-quantize` to run only the base dense result.

```bash
uv run nano-ir-bench evaluate \
  --model example/embedding-model \
  --dataset NanoMTEB
```

```bash
uv run nano-ir-bench evaluate \
  --model example/embedding-model \
  --dataset NanoMTEB \
  --no-quantize
```

For explicit dense runs, use `int8,binary` and `rescore:int8,binary`:

```bash
uv run nano-ir-bench evaluate \
  --model example/embedding-model \
  --dataset NanoMTEB \
  --embedding-variant int8,binary \
  --embedding-variant rescore:int8,binary
```

Rescore retrieves the top 100 quantized candidates and reranks only those
candidates with the already-computed source float embeddings; it does not
re-embed documents.

For CUDA/CPU scorer diagnostics, keep the same variant names and change only
`--score-device cpu` or `--score-device cuda`. Torch CUDA scoring casts stored
int8 and binary codes to float32 for matrix multiplication because regular
PyTorch CUDA matmul does not expose integer accumulation for these tensors.

### Truncated Dimensions

Matryoshka-style truncated embedding dimensions can be evaluated from the same
base embedding run:

```bash
uv run nano-ir-bench evaluate \
  --model example/matryoshka-embedding-model \
  --dataset NanoMTEB \
  --embedding-variant truncate:512,256
```

### Truncated Dimensions With Quantization

When evaluating dimensions, run the standalone truncation variants, standalone
quantization variants, and their cross product:

```bash
uv run nano-ir-bench evaluate \
  --model example/matryoshka-embedding-model \
  --dataset NanoMTEB \
  --embedding-variant truncate:256,128,64 \
  --embedding-variant int8,binary \
  --embedding-variant rescore:int8,binary \
  --embedding-variant-cross truncate:256,128,64 int8,binary \
  --embedding-variant-cross truncate:256,128,64 rescore:int8,binary
```

All three groups answer different questions: standalone truncation measures the
dimension trade-off, standalone quantized search measures the quantization
trade-off at the original dimension, and the cross product measures the combined
dimension-and-quantization trade-off such as `128dim x int8` or
`64dim x binary`. The rescore variants record the same candidate set
after reranking the top 100 quantized hits with source float embeddings.

Each task JSON keeps the base result in `metrics` and records the base and
derived results under `evaluation.embedding_evaluations`. Every entry includes
the measured embedding dimension as `embedding_dimensions.dim`; if query and
corpus dimensions differ, it records `query_dim` and `corpus_dim` instead. The
optional `embedding_metadata` block records the representation type
(`dense`, `sparse`, or future `late_interaction`), dimension format, shapes, and
sparse nnz/density statistics when available. Quantized variants also record
the value dtype, quantization precision, original dimension, stored dimension,
calibration/ranges source, scoring representation, quantization method
(`corpus_only` or `query_and_corpus`), and side (`query` or `corpus`) when
applicable. Dense embedding evaluations score both `cosine` and `dot`, store
both entries in `distance_evaluations`, and copy the better aggregate result to
`metrics`, `aggregate_metric_value`, `best_score`, `best_distance`, and
`best_score_name`.

## BM25 top-100 reranking

Dense, sparse, and late-interaction evaluations also report BM25 top-100
reranking by default when the dataset provides the `bm25` candidate subset. The
model is still encoded and scored through the normal full-corpus path; the
reranking metrics are computed by filtering the model's ranking to each query's
BM25 candidates, so no second model inference is required.

The full-corpus result remains the main aggregate. Reranking results are stored
separately under `rerank_metrics`, `evaluation.rerank_aggregate_metric_value`,
and `evaluation.reranking_evaluations`; `all.json` adds
`totals.rerank_aggregate_metric_mean`. If BM25 candidates are unavailable, the
full-corpus evaluation still succeeds and reranking is recorded as skipped.

CrossEncoder-style reranker models can be evaluated directly with
`--model-type reranker`. They score only the BM25 candidate subset and support
models exposing `rank`, `predict`, or a callable pair-scoring API.

```bash
uv run nano-ir-bench evaluate \
  --model nreimers/mmarco-mMiniLMv2-L6-H384-v1 \
  --model-type reranker \
  --dataset NanoRTEB \
  --candidate-subset-name bm25 \
  --rerank-top-n 100 \
  --batch-size 32
```

## BM25

BM25 can be evaluated directly. If the dataset provides a candidate subset named
by `--candidate-subset-name` (default: `bm25`), that ranking is used as the BM25
baseline. If the subset is unavailable, BM25 is computed locally.

```bash
uv run nano-ir-bench evaluate \
  --model-type bm25 \
  --dataset NanoMLDR \
  --split ja \
  --top-k 100
```

BM25 candidate files can also be generated for reranking workflows:

```bash
uv run nano-ir-bench build-bm25 \
  --dataset NanoMLDR \
  --split ja \
  --bm25-tokenizer english_porter_stop \
  --top-k 100
```

BM25 scoring uses `bm25s` with the standard Okapi-style Robertson method.
Available tokenizers are `regex`, `whitespace`, `transformer`, `stemmer`,
`english_regex`, `english_porter`, `english_porter_stop`, and `wordseg`. The
default is `auto`: 10 query texts are sampled deterministically and detected
with `fast-langdetect`. If the detected language supports `wordseg`, BM25 uses
`wordseg`; otherwise it uses `regex`.

The resolved BM25 algorithm and tokenizer are written to each result JSON under
`config.bm25` and `model.bm25`.

`wordseg` is optional and lazy-loads language-specific tokenizers. Install the
extra before using it:

```bash
uv sync --extra wordseg
```

Supported `wordseg` language values are passed via `--bm25-tokenizer-name`:

```bash
uv run nano-ir-bench build-bm25 \
  --dataset NanoMLDR \
  --split ja \
  --bm25-tokenizer wordseg \
  --bm25-tokenizer-name ja
```

The current mapping is `ja` = `fugashi` + `unidic-lite`, `zh` = `jieba`,
`th` = `pythainlp`, `ko` = `kiwipiepy`, and `vi` = `pyvi`.

## Viewer

Install the web viewer dependencies with the `viewer` group:

```bash
uv sync --group viewer
```

For all development and viewer dependencies, use the `all` group:

```bash
uv sync --group all
```

Start the HTMX/Tailwind leaderboard viewer:

```bash
uv run nano-ir-bench web
```

By default, it binds to `127.0.0.1:8000` and keeps
`output/viewer/nano_ir_bench.duckdb` synchronized from the benchmark output
DuckDB when a page is loaded. Use `--host 0.0.0.0 --port 28090` for remote
access, or pass `--source-output-dir` / `--source-duckdb-path` to point at a
different source.

## Achievements

- Built on the idea behind [Nano-BEIR](https://huggingface.co/blog/sionic-ai/eval-sionic-nano-beir).
- The NanoBEIR evaluation implementation in [Sentence Transformers](https://github.com/huggingface/sentence-transformers/) was a reference for this project. Thanks to the maintainers and contributors.
