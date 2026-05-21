---
title: HAKARI-Bench Leaderboard
emoji: 📊
colorFrom: blue
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
license: apache-2.0
---

# HAKARI-Bench

HAKARI-Bench is a library, viewer, and leaderboard project for evaluating small information retrieval datasets.

Nano-style information retrieval benchmark runner for SentenceTransformers-compatible models.

Built-in dataset definitions include `NanoBEIR-en`, `MNanoBEIR`,
`NanoMIRACL`, `NanoMLDR`, `NanoRTEB`, `NanoMTEB`, `NanoCMTEB`,
`NanoJMTEB`, `NanoFaMTEB`, `NanoRuMTEB`, `NanoVNMTEB`, `NanoMTEB-Misc`,
`NanoMMTEB`, `NanoLongEmbed`, `NanoCoIR`, `NanoIFIR`, `NanoLaw`,
`NanoMedical`, `NanoRARb`, `NanoBRIGHT`, `NanoCodeRAG`, `NanoChemTEB`,
`NanoR2MED`, `NanoBuiltBench`, `NanoBIRCO`, and `NanoDAPFAM`.

The NanoMTEB family follows MTEB benchmark provenance rather than legacy
language buckets. Named benchmark families such as C-MTEB, JMTEB, FaMTEB,
ruMTEB, and VN-MTEB use dedicated Nano dataset names. Retrieval tasks that do
not belong to a specific official MTEB family are grouped under
`NanoMTEB-Misc`. Historical broad `NanoMTEB-{language}` aliases are not
supported; use the canonical dataset names directly.

## Example

```bash
uv run hakari-bench evaluate dense \
  --model hotchpotch/bekko-embedding-pico-beta-unir-v7 \
  --dataset hakari-bench/NanoBEIR-en
```

Evaluate an individual provenance-aligned NanoMTEB family dataset with:

```bash
uv run hakari-bench evaluate dense \
  --model hotchpotch/bekko-embedding-pico-beta-unir-v7 \
  --dataset hakari-bench/NanoFaMTEB
```

The default model dtype is `bf16`; pass `--dtype fp32` or `--dtype fp16` only
when a run needs an explicit override.

For model evaluations, prefer the attention implementation officially
recommended by the model author, such as `--attn-implementation sdpa` or
`--flash-attn2` / `--attn-implementation flash_attention_2` when supported.
Leaving attention unspecified delegates to the Transformers/model default and
can make long benchmark runs substantially slower for some models.

Results are written under:

```text
output/results/{model_id}/{huggingface_dataset_name}/{split_or_task}.json
```

For example, `hakari-bench/NanoJMTEB` is stored under
`output/results/{model_id}/hakari-bench__NanoJMTEB/`.

Uploadable NanoMTEB family dataset repositories can be staged under:

```text
output/NanoMTEB_Family/{canonical_dataset}/
```

Each child directory is a Hugging Face dataset repo layout with `corpus`,
`queries`, `qrels`, and `bm25` configs. These directories are intended for
uploading canonical datasets such as `hakari-bench/NanoFaMTEB`; they are not a
HAKARI-Bench dataset collection.

For Hugging Face datasets, each task JSON records the resolved dataset repo
revision under `target.dataset_revision`. Use `--dataset-revision REV` to pin a
specific branch, tag, or commit; the resolved commit SHA is still stored.
Each task JSON also includes `experiment_manifest`, which records a SHA-256
fingerprint derived from model, target, config, and environment metadata.

Local model paths can be evaluated directly. Use `--model-alias` to choose the
stable model id used in result paths and JSON. If the alias does not contain a
slash, `local/` is prepended automatically.

```bash
uv run hakari-bench evaluate dense \
  --model /local_model_A/ \
  --model-alias model_A \
  --collection MNanoBEIR
```

The result JSON records this as `model.id = "local/model_A"` and
`model.source = {"type": "local_path", "path": "/local_model_A"}`.

Most evaluate options can also be supplied as a structured JSON object:

```bash
uv run hakari-bench evaluate dense \
  --params-json '{
    "model": {"source": "/local_model_A/", "alias": "local/model_A"},
    "target": {"collections": ["MNanoBEIR"]},
    "runtime": {"batch_size": 16, "dtype": "fp16"},
    "output": {"results_dir": "output/results", "overwrite": true}
  }'
```

## Sparse encoders

Sparse SentenceTransformers models can be evaluated with `evaluate sparse`.
HAKARI-Bench requests sparse tensor output from `SparseEncoder` models and
keeps sparse embeddings in a sparse matrix format for scoring.

SentenceTransformers training and evaluation integrations are documented in
[`docs/sentence_transformers_evaluation_integration.md`](docs/sentence_transformers_evaluation_integration.md).
They provide `BaseEvaluator`-compatible dense, sparse, reranker, and BM25
evaluators for use inside SentenceTransformers training loops.

```bash
uv run hakari-bench evaluate sparse \
  --model naver/splade-v3 \
  --dataset NanoBEIR-en
```

For SPLADE-style sparsity and latency trade-off checks, explicitly truncate
query and/or document sparse rows to their top weighted dimensions after
encoding:

```bash
uv run hakari-bench evaluate sparse \
  --model naver/splade-v3 \
  --dataset NanoBEIR-en \
  --sparse-query-max-active-dims 32 \
  --sparse-document-max-active-dims 128
```

The selected limits are written to result JSON under
`config.sparse_query_max_active_dims`,
`config.sparse_document_max_active_dims`, and `config.sparse_truncation`.
Sparse embedding metadata records `nnz_total`, `nnz_mean`, `nnz_median`,
`nnz_max`, and `density` for queries and documents.

Sparse evaluation automatically compares the default post-encode sparsity grid
from one full sparse model encode unless `--no-default-embedding-variants` is
set:

- query max active dims: `8,16,24,32`
- document max active dims: `64,128,256,512`

To add other sparsity limits, use post-encode embedding variants:

```bash
uv run hakari-bench evaluate sparse \
  --model naver/splade-v3 \
  --dataset NanoBEIR-en \
  --embedding-variant sparse-query-max-active-dims:48 \
  --embedding-variant-grid sparse-query-max-active-dims:48 sparse-document-max-active-dims:768
```

These variants keep the top absolute-value dimensions per query/document row
and record each derived result under `evaluation.embedding_evaluations`, like
dense `truncate:` variants. Use `--no-default-embedding-variants` when a sparse
run should write only the base no-limit result or only explicitly requested
sparse variants.

Sparse embeddings intentionally do not support quantized embedding variants in
the CLI. Use post-encode sparse truncation variants for sparse footprint and
latency trade-off checks.

## Late interaction / ColBERT

ColBERT-style models can be evaluated with `evaluate late-interaction`.
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
paths. Use `--retrieval-score-device cpu` to force post-encode score/top-k matrix work
onto CPU, which is useful for checking CUDA and CPU scoring parity.

Dense evaluation automatically runs normalized `int8` and binary quantized
search variants, plus top-100 float rescoring for both variants. The benchmark
first L2-normalizes SentenceTransformers embeddings and converts them to stored
codes, then uses exact PyTorch matrix scoring for the quantized top-k. The
post-encode score device follows `--retrieval-score-device`: `auto` keeps tensor scoring
on the model output device, while `cpu` or `cuda` force quantized search matrix
work to that device. Explicit dense variants do not disable these defaults. Use
`--no-default-embedding-variants` to run only the base dense result or only the
explicit variants you specify.

```bash
uv run hakari-bench evaluate dense \
  --model example/embedding-model \
  --dataset NanoMTEB
```

```bash
uv run hakari-bench evaluate dense \
  --model example/embedding-model \
  --dataset NanoMTEB \
  --no-default-embedding-variants
```

For explicit dense quantization-only runs, the following command is accepted but
is equivalent to the default dense variant plan:

```bash
uv run hakari-bench evaluate dense \
  --model example/embedding-model \
  --dataset NanoMTEB \
  --embedding-variant int8,binary \
  --embedding-variant rescore:int8,binary
```

Rescore retrieves the top 100 quantized candidates and reranks only those
candidates with the already-computed source float embeddings; it does not
re-embed documents.

For CUDA/CPU scorer diagnostics, keep the same variant names and change only
`--retrieval-score-device cpu` or `--retrieval-score-device cuda`. Torch CUDA scoring casts stored
int8 and binary codes to float32 for matrix multiplication because regular
PyTorch CUDA matmul does not expose integer accumulation for these tensors.

### Truncated Dimensions

Matryoshka-style truncated embedding dimensions can be evaluated from the same
base embedding run. Dense truncation runs automatically add full-dimension
quantized/rescore variants and truncation x quantized/rescore variants for the
specified dimensions:

```bash
uv run hakari-bench evaluate dense \
  --model example/matryoshka-embedding-model \
  --dataset NanoMTEB \
  --embedding-variant truncate:512,256
```

If a requested truncation dimension is the same as the encoded base embedding
dimension, HAKARI-Bench warns and skips that no-op truncate variant because it
would duplicate the original full-dimension result.

### Truncated Dimensions With Quantization

When evaluating dimensions, specifying the truncation dimensions is enough. The
CLI automatically runs the standalone truncation variants, standalone
quantization variants, and their cross product:

```bash
uv run hakari-bench evaluate dense \
  --model example/matryoshka-embedding-model \
  --dataset NanoMTEB \
  --embedding-variant truncate:256,128,64
```

All three groups answer different questions: standalone truncation measures the
dimension trade-off, standalone quantized search measures the quantization
trade-off at the original dimension, and the cross product measures the combined
dimension-and-quantization trade-off such as `128dim x int8` or
`64dim x binary`. The rescore variants record the same candidate set
after reranking the top 100 quantized hits with source float embeddings.

Use `--no-default-embedding-variants` with `truncate:` only when intentionally
omitting dense quantized/rescore comparisons.

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
reranking metrics are computed by scoring only each query's BM25 candidates with
the already-computed embeddings, so no second model inference is required.

The full-corpus result remains the main aggregate. Reranking results are stored
separately under `rerank_metrics`, `evaluation.rerank_aggregate_metric_value`,
and `evaluation.reranking_evaluations`. Candidate coverage against qrels is
stored in the reranking evaluation so BM25 candidate recall can be separated
from reranker quality. For top-100 reranking diagnostics, published Nano
datasets should have 100% query coverage and 100% relevant coverage unless a
dataset README explicitly documents why that is impossible. The CLI prints a
JSON summary with `primary_metric_mean` and task counts after the run. If BM25
candidates are unavailable, the full-corpus evaluation still succeeds and
reranking is recorded as skipped.

CrossEncoder-style reranker models can be evaluated directly with
`evaluate reranker`. They score only the BM25 candidate subset and support
models exposing `rank`, `predict`, or a callable pair-scoring API.

```bash
uv run hakari-bench evaluate reranker \
  --model nreimers/mmarco-mMiniLMv2-L6-H384-v1 \
  --dataset NanoRTEB \
  --candidate-ranking bm25 \
  --rerank-top-k 100 \
  --batch-size 32
```

## BM25

BM25 can be evaluated directly. If the dataset provides a candidate subset named
by `--candidate-ranking` (default: `bm25`), that ranking is used as the BM25
baseline. This is the default because built-in HAKARI-Bench datasets are
expected to ship BM25 candidate subsets. If the selected subset is unavailable,
the run fails with an explicit error instead of silently changing the baseline.

```bash
uv run hakari-bench evaluate bm25 \
  --dataset NanoMLDR \
  --split ja \
  --bm25-top-k 100
```

Use `--bm25-source computed` only when generating BM25 subsets or intentionally
recomputing BM25 with the local `bm25s` implementation:

```bash
uv run hakari-bench evaluate bm25 \
  --dataset NanoMLDR \
  --split ja \
  --bm25-source computed \
  --bm25-tokenizer english_porter_stop \
  --bm25-top-k 100
```

BM25 candidate files can also be generated for reranking workflows:

```bash
uv run hakari-bench build-candidates bm25 \
  --dataset NanoMLDR \
  --split ja \
  --bm25-tokenizer english_porter_stop \
  --bm25-top-k 100
```

`build-candidates bm25` also accepts `--params-json` with `target`, `output`,
and `bm25` sections.

MNanoBEIR dataset BM25 subsets can be rebuilt locally from the existing
published corpus, queries, and qrels with forced-positive insertion:

```bash
uv run python scripts/rebuild_mnanobeir_bm25.py \
  --output-dir output/nano_datasets_mnanobeir_bm25_rebuilt \
  --overwrite
```

The rebuild script writes upload-ready local dataset repo layouts and regenerates
each dataset README. The generated BM25 table includes query and relevant
coverage columns, and the default run fails if any rebuilt split is not 100%
covered at top-100. The script defaults to `--tokenizer auto`, matching the
normal local BM25 policy: it detects query language and uses `wordseg` for
supported languages such as `ja`, `ko`, `th`, and `vi`. Install the `wordseg`
extra before rebuilding multilingual BM25 subsets.

Local BM25 scoring uses `bm25s` with the standard Okapi-style Robertson method.
Available tokenizers for `--bm25-source computed` and `build-candidates bm25`
are `regex`, `whitespace`, `transformer`, `stemmer`, `english_regex`,
`english_porter`, `english_porter_stop`, and `wordseg`. The local default is
`auto`: 10 query texts are sampled deterministically and detected with
`fast-langdetect`. If the detected language supports `wordseg`, BM25 uses
`wordseg`; otherwise it uses `regex`.

The resolved BM25 algorithm and tokenizer are written to each result JSON under
`config.bm25` and `model.bm25`.

`wordseg` is optional and lazy-loads language-specific tokenizers. Install the
extra before using it:

```bash
uv sync --extra wordseg
```

Supported `wordseg` language values are passed via `--bm25-wordseg-language`:

```bash
uv run hakari-bench build-candidates bm25 \
  --dataset NanoMLDR \
  --split ja \
  --bm25-tokenizer wordseg \
  --bm25-wordseg-language ja
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
uv run hakari-bench web
```

Build or rebuild the DuckDB warehouse from result JSON before publishing or
reviewing fresh leaderboard data:

```bash
uv run python scripts/build_results_database_and_report.py \
  --results-dir output/results \
  --duckdb-path output/results/hakari_bench.duckdb \
  --html-output output/results/report.html
```

To merge historical or separate result roots, repeat `--results-dir` in
priority order. If the same model-task JSON exists in more than one root, the
first directory wins and later directories fill only missing results. The
logical model identity is `model.id` from each result JSON, exposed as
`model_name`; `model_dir` is only the storage path under the results root.
Use repeated `--exclude-model-name` options to omit known-bad or superseded
model ids from the generated warehouse without deleting their JSON files.
Use `--overwrite-result-duplicates` when later result roots should replace
duplicate logical model-task rows from earlier roots.

```bash
uv run python scripts/build_results_database_and_report.py \
  --results-dir output/results \
  --results-dir output/results_combined_20260510_1340 \
  --overwrite-result-duplicates \
  --exclude-model-name hotchpotch/bekko-embedding-pico-beta-unir-v9-GOR \
  --duckdb-path output/results/hakari_bench.duckdb \
  --html-output output/results/report.html
```

To add a separate result root for new model-task JSON to an existing DuckDB
without scanning the original result roots, use `--append-results-dir`. This is
append-only: duplicate result paths or duplicate logical model-task rows are
rejected.

```bash
uv run python scripts/build_results_database_and_report.py \
  --append-results-dir output/new_model_results \
  --duckdb-path output/results/hakari_bench.duckdb
```

By default, it binds to `127.0.0.1:8000` and keeps
`output/viewer/hakari_bench.duckdb` synchronized from the benchmark results
DuckDB when a page is loaded. Use `--host 0.0.0.0 --port 28090` for remote
access, or pass `--source-results-dir` / `--source-duckdb-path` to point at a
different source.

The viewer can also sync its local DuckDB cache from a Hugging Face dataset:

```bash
uv run hakari-bench web \
  --hf-dataset-repo-id hakari-bench/leaderboard_database \
  --hf-dataset-path duckdb/hakari_bench.duckdb
```

The same configuration is available through environment variables:
`HAKARI_BENCH_VIEWER_DUCKDB_PATH`,
`HAKARI_BENCH_VIEWER_SOURCE_DUCKDB_PATH`,
`HAKARI_BENCH_VIEWER_SOURCE_RESULTS_DIR`,
`HAKARI_BENCH_VIEWER_HF_DATASET_REPO_ID`,
`HAKARI_BENCH_VIEWER_HF_DATASET_PATH`, and
`HAKARI_BENCH_VIEWER_HF_DATASET_REVISION`. The Docker Space defaults to
`hakari-bench/leaderboard_database` and `duckdb/hakari_bench.duckdb`.

The DuckDB warehouse includes `task_results`, `metrics_long`,
`task_diagnostics`, and `dataset_metadata`. `task_diagnostics` is intended for
SQL or notebook analysis of rerank lift, BM25 candidate coverage, and latency
breakdowns; `dataset_metadata` supports language/category/citation analysis.

## Achievements

- Built on the idea behind [Nano-BEIR](https://huggingface.co/blog/sionic-ai/eval-sionic-nano-beir).
- The NanoBEIR evaluation implementation in [Sentence Transformers](https://github.com/huggingface/sentence-transformers/) was a reference for this project. Thanks to the maintainers and contributors.
