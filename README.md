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
  --dataset hakari-bench/NanoBEIR-en \
  --dtype bf16
```

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

For SPLADE-style sparsity and latency trade-off checks, limit the number of
active dimensions per query/document embedding with `--sparse-max-active-dims`:

```bash
uv run nano-ir-bench evaluate \
  --model naver/splade-v3 \
  --model-type sparse \
  --dataset NanoBEIR-en \
  --sparse-max-active-dims 128
```

The selected limit is written to result JSON under
`config.sparse_max_active_dims` and summarized in `all.json`. Sparse embedding
metadata records `nnz_total`, `nnz_mean`, `nnz_median`, `nnz_max`, and
`density` for queries and documents.

To compare multiple sparsity limits from one full sparse model encode, use
post-encode embedding variants:

```bash
uv run nano-ir-bench evaluate \
  --model naver/splade-v3 \
  --model-type sparse \
  --dataset NanoBEIR-en \
  --embedding-variant sparse-max-active-dims:256,128,64
```

These variants keep the top absolute-value dimensions per query/document row
and record each derived result under `evaluation.embedding_evaluations`, like
dense `truncate:` variants.

Sparse embeddings can also use `quantize-docs:int8,ubinary` variants. For sparse
`int8`, non-zero weights are scalar-quantized with a corpus-derived value range
and dequantized for scoring. For sparse `ubinary`, non-zero dimensions are
scored as an unweighted sparse presence vector.

## Embedding variants

Derived embedding variants can be evaluated together with the base embedding
run. The model is encoded once, then every derived variant is applied through a
single post-encode transform pipeline and scored from the already-computed
embeddings. This keeps variant evaluation cheap and avoids changing model
inference behavior.

### Quantization

Dense evaluation runs exact usearch `int8` and binary quantized search variants
by default. The benchmark first converts SentenceTransformers embeddings to the
stored codes, then passes those codes to usearch; usearch does not calibrate or
requantize embeddings. Use `--no-quantize` to run only the base dense result.

`quantize:int8,ubinary` is a shorthand for these usearch variants. `ubinary` is
kept as a compatibility alias and maps to the binary usearch representation.

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

For explicit dense runs, `quantize:` and `usearch:` are equivalent for supported
precisions:

```bash
uv run nano-ir-bench evaluate \
  --model example/embedding-model \
  --dataset NanoMTEB \
  --embedding-variant quantize:int8,ubinary
```

To rerank quantized candidates with the source float embeddings, use
`usearch-rescore:`. Rescore retrieves the top 100 quantized candidates and
reranks only those candidates; it does not re-embed documents.

```bash
uv run nano-ir-bench evaluate \
  --model example/embedding-model \
  --dataset NanoMTEB \
  --embedding-variant usearch-rescore:int8,binary
```

If a docs-only dequantized storage probe is explicitly needed, use
`quantize-docs:`. Query embeddings remain float, scalar document codes are
dequantized for scoring, and packed binary document codes are unpacked to sign
vectors.

```bash
uv run nano-ir-bench evaluate \
  --model example/embedding-model \
  --dataset NanoMTEB \
  --embedding-variant quantize-docs:int8,ubinary
```

If a symmetric query-and-document quantization comparison is explicitly needed,
use `quantize-both:`:

```bash
uv run nano-ir-bench evaluate \
  --model example/embedding-model \
  --dataset NanoMTEB \
  --embedding-variant quantize-both:int8,ubinary
```

For diagnostics, `quantize-code:int8` quantizes both query and document
embeddings with corpus-derived ranges and ranks by the stored scalar code
values instead of dequantized float vectors:

```bash
uv run nano-ir-bench evaluate \
  --model example/embedding-model \
  --dataset NanoMTEB \
  --embedding-variant quantize-code:int8
```

To test calibration sensitivity, `quantize-sample:int8:N` computes scalar
quantization ranges from a deterministic corpus sample of `N` embeddings
instead of the full corpus:

```bash
uv run nano-ir-bench evaluate \
  --model example/embedding-model \
  --dataset NanoMTEB \
  --embedding-variant quantize-sample:int8:128
```

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
  --embedding-variant quantize:int8,ubinary \
  --embedding-variant-cross truncate:256,128,64 quantize:int8,ubinary
```

All three groups answer different questions: standalone truncation measures the
dimension trade-off, standalone quantization measures the quantization trade-off
at the original dimension, and the cross product measures the combined
dimension-and-quantization trade-off such as `128dim x int8` or
`64dim x ubinary`.

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
`th` = `pythainlp`, and `ko` = `kiwipiepy`.

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
