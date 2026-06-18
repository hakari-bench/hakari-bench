# Evaluation Policy

This document is the canonical repository guidance for running HAKARI-Bench
evaluations. Do not rely on skill-local benchmark instructions as the source of
truth. Skill files may point here, but evaluation setting policy, variant
policy, and coverage checks should be maintained in this document.

Use this file when you need to choose evaluation settings: prompts, attention
implementation, dtype, embedding variants, cache/offline behavior, retries, or
coverage audits. Use [`evaluation_runbook.md`](evaluation_runbook.md) when you
need the shorter operational path from model evaluation to DuckDB append and
viewer startup.

## Core Workflow

1. Read `AGENTS.md`, this document, `README.md`, `pyproject.toml`, relevant
   dataset configs under `config/`, and current CLI help from the installed
   checkout.
2. Identify the requested models, datasets, result directory, cache policy, and
   whether existing result JSON should be reused or overwritten.
3. For each model, check model-specific requirements in
   [`docs/model_specific_benchmarking_notes.md`](model_specific_benchmarking_notes.md)
   before choosing prompts, attention implementation, dtype, or compatibility
   fallbacks.
4. Prefer the attention implementation officially recommended by the model
   author. If no explicit attention implementation is passed, the CLI will warn
   because long benchmark inference can be much slower for some models.
5. Decide the full method-specific option and variant plan before starting any
   large run.
6. Run a small validation command when options are uncertain, then scale to the
   requested benchmark set.
7. Keep an ignored progress checklist under `tmp/` for long benchmark waves.
8. After benchmarking, rebuild DuckDB/viewer artifacts when the user asks
   for comparisons, leaderboards, or viewer updates. If results are split
   across multiple result roots, pass repeated `--results-dir` options in
   priority order; earlier directories win duplicate model-task JSON conflicts.
9. Audit result coverage before treating a leaderboard as final.

## Target Selection

Use `--all` when the requested run should cover every standard built-in dataset
task from `config/datasets/`. Existing per-task result JSON files are skipped
unless `--overwrite` is set, so `--all` can be used to fill missing benchmark
coverage. Per-task evaluation output defaults to compressed `.json.xz` files;
pass `--result-format json` only when a plain `.json` result tree is required:

```bash
uv run hakari-bench evaluate reranker \
  --model MODEL_NAME \
  --all \
  --candidate-ranking bm25
```

Use `--dataset` or `--collection` only for intentionally narrower runs. `--all`
is mutually exclusive with `--dataset`, `--collection`, and `--split`.

Target expansion uses `--evaluation-scope standard` by default. Dataset YAML may
mark an entire dataset or individual tasks with `include_by_default: false`;
those tasks are skipped by normal `--all`, `--dataset`, and `--collection`
expansion but remain part of the dataset. Use `--evaluation-scope all` to include
these extended tasks, or pass `--split` for an explicit task override. Omitted
`evaluation_scope` metadata means `include_by_default: true`, so existing YAML
does not need to repeat the default.

For example, NanoDAPFAM keeps the six `ToFullText` tasks in the dataset but marks
them as `fulltext`, `long_context`, and `expensive`; standard evaluation uses the
12 non-FullText tasks, while `--evaluation-scope all` evaluates all 18 tasks.

Common examples:

```bash
# Fill missing dense results for every built-in dataset. Existing task JSON is
# reused automatically; only missing tasks are evaluated.
uv run --group tf4-fa2 hakari-bench evaluate dense \
  --model BAAI/bge-m3 \
  --all \
  --dtype bf16 \
  --device cuda:0
```

```bash
# Fill missing reranker results for every built-in dataset using the default
# reranking_hybrid candidate subset.
uv run --group tf4-fa2 hakari-bench evaluate reranker \
  --model BAAI/bge-reranker-v2-m3 \
  --all \
  --batch-size 128 \
  --dtype bf16 \
  --device cuda:0
```

`reranking_hybrid` means RRF top-100 plus optional safeguard positive at rank
101. Evaluation reranks every candidate present in the row, so 100-candidate
rows rerank the RRF top-100 and 101-candidate rows rerank the same top-100 plus
the appended safeguard positive. DuckDB/report generation exposes both
`reranking` and `reranking_without_safeguard` targets so the safeguard effect can
be inspected separately.

```bash
# Pin a physical GPU for a single process. Inside the process the visible GPU is
# still addressed as cuda:0.
CUDA_VISIBLE_DEVICES=1 uv run --group tf4-fa2 hakari-bench evaluate reranker \
  --model hotchpotch/japanese-reranker-xsmall-v2 \
  --all \
  --batch-size 256 \
  --dtype bf16 \
  --device cuda:0 \
  --flash-attn2
```

```bash
# Equivalent structured target selection for scripts or job manifests.
uv run --group tf4-fa2 hakari-bench evaluate reranker \
  --params-json '{
    "model": {"source": "BAAI/bge-reranker-v2-m3"},
    "target": {"all": true},
    "runtime": {"dtype": "bf16", "device": "cuda:0", "batch_size": 128},
    "reranker": {"candidate_ranking": "reranking_hybrid"}
  }'
```

Use `--overwrite` only when intentionally correcting or replacing prior results.
Without `--overwrite`, `--all` is safe for resuming interrupted runs and filling
newly added benchmarks.

## Model Research Checklist

For every model:

- Check whether it is a Sentence Transformers model with prompt configuration.
  Prefer the built-in prompt configuration when present.
- If no usable Sentence Transformers prompt configuration exists, inspect the
  Hugging Face model card first, then relevant articles or papers for retrieval
  prefixes such as query/document/passage instructions.
- Use explicit prompt options only when the model requires them:
  `--query-prompt`, `--document-prompt`, `--query-prompt-name`,
  `--document-prompt-name`, `--query-encode-task`, or
  `--document-encode-task`.
- Check whether the model advertises method-specific capabilities that should be
  reflected in the benchmark plan. Examples include Matryoshka/truncate
  dimensions for dense embeddings, sparse max-active-dim controls,
  late-interaction query/document token lengths or query expansion, reranker
  candidate-ranking requirements, and provider/API encode options for custom
  backends. Include supported capabilities in the run unless the user explicitly
  asks for a base-only or ablation run, and record the decision in result
  metadata or the run summary.
- Check whether `--trust-remote-code` is required.
- If the model is evaluated through a custom backend, read
  [`custom_model_backends.md`](custom_model_backends.md), confirm the backend
  interface, and record provider/model/encode kwargs in metadata. Prefer
  environment variables for credentials.
- Check the model's default maximum sequence length, but do not override it
  unless the user explicitly asks.
- Do not shorten context length to avoid slow execution or memory pressure.
  Reduce batch size first.
- If reproducibility requires a fixed dataset state, use
  `--dataset-revision REV`. Otherwise verify that output JSON records the
  resolved Hugging Face dataset SHA.
- If reproducibility requires a fixed model state, use `--model-revision REV`.
  Output JSON records the resolved Hugging Face model SHA as a short revision
  when it can be resolved.

## Dense Evaluation

Use the dense subcommand for ordinary SentenceTransformers-compatible embedding
models:

```bash
uv run hakari-bench evaluate dense \
  --model MODEL_NAME \
  --dataset DATASET_NAME \
  --dtype bf16
```

Dense models automatically run normalized `int8` and binary quantized search
variants plus top-100 float-rescored variants whenever
`--no-default-embedding-variants` is not set. Explicit dense variants no longer
disable these defaults.

This is the most important dense coverage rule:

> For Matryoshka or otherwise truncate-aware dense models, include the model's
> supported truncation dimensions with `--embedding-variant truncate:DIMS`
> unless the user explicitly requests a base-only or ablation run. Use the model
> card, implementation notes, or provider documentation to choose the supported
> dimensions. The CLI will automatically add standalone truncation, full-dim
> quantized and rescored variants, and truncation x quantized/rescore variants
> for those dims.

If a requested truncation dimension matches the encoded base embedding
dimension, evaluation emits a warning and skips that no-op truncate variant
because it would duplicate the original full-dimension result.

Use `--no-default-embedding-variants` only when the run intentionally needs base
results without automatic dense quantized/rescore variants.

`--retrieval-score-device auto` keeps supported post-encode score/top-k work on
the model output device. Use `--retrieval-score-device cpu` or
`--retrieval-score-device cuda` only when intentionally forcing that work.

## Dense Variant Plans

For plain dense baselines with no documented truncation support or dimensional
comparison requirement, omit explicit embedding variants and let the dense
defaults run:

```bash
uv run hakari-bench evaluate dense \
  --model MODEL_NAME \
  --dataset DATASET_NAME \
  --dtype bf16
```

For Matryoshka/truncate-aware models, provide the supported truncation
dimensions:

- standalone truncation variants,
- standalone quantized search and rescore variants at the original dimension,
- truncation x quantized search and truncation x rescore grids.

Example:

```bash
uv run hakari-bench evaluate dense \
  --model MODEL_NAME \
  --dataset DATASET_NAME \
  --dtype bf16 \
  --embedding-variant truncate:256,128,64
```

This command produces the complete comparison set because standalone dimensions
isolate the dimension trade-off, standalone quantized/rescore variants isolate
the quantization trade-off at the original dimension, and the automatically
expanded grids measure combined trade-offs such as `128dim x int8` and
`64dim x binary`, with and without top-100 float rescore.

If a user asks only for truncation and explicitly does not want quantization,
disable dense defaults and state that quantized/rescore variants are
intentionally omitted:

```bash
uv run hakari-bench evaluate dense \
  --model MODEL_NAME \
  --dataset DATASET_NAME \
  --no-default-embedding-variants \
  --embedding-variant truncate:512,256
```

The benchmark implementation applies derived embedding variants after a single
base encoding pass. Cross variants add transform/scoring work, not additional
model encoding.
No-op truncation variants whose requested dimension equals the base embedding
dimension are skipped with a warning.

For the built-in OpenAI embedding loader, truncation uses full API embeddings
followed by `full[:DIM]` and L2 normalization. This normalized-prefix path is
the repository policy for OpenAI truncation variants even though pure API
`dimensions=DIM` responses are not bit-identical.

## Sparse Evaluation

Use `evaluate sparse` for SentenceTransformers `SparseEncoder` models:

```bash
uv run hakari-bench evaluate sparse \
  --model MODEL_NAME \
  --dataset DATASET_NAME
```

Do not add dense quantized embedding variants for sparse/SPLADE-style models.
Sparse quantization is intentionally unsupported in the CLI. Sparse runs
automatically include post-encode query/document max-active-dims grid variants
unless `--no-default-embedding-variants` is set:

- query max active dims: `8,16,24,32`
- document max active dims: `64,128,256,512`

These variants are derived after one full sparse model encode and do not run
additional model inference.

Additional query-only sparsity limits:

```bash
uv run hakari-bench evaluate sparse \
  --model MODEL_NAME \
  --dataset DATASET_NAME \
  --embedding-variant sparse-query-max-active-dims:48
```

Additional query/document grids:

```bash
uv run hakari-bench evaluate sparse \
  --model MODEL_NAME \
  --dataset DATASET_NAME \
  --embedding-variant-grid sparse-query-max-active-dims:48 sparse-document-max-active-dims:768
```

The base no-limit result is always included as
`evaluation.embedding_evaluations[0]`. Use `--no-default-embedding-variants`
when intentionally running only the base no-limit result or only explicitly
specified sparse variants.

## Late-Interaction, Reranker, And BM25

Use `evaluate late-interaction` for PyLate ColBERT models. Check
model-specific query/document prefixes, sequence lengths, prompt names,
`--trust-remote-code`, and `--late-interaction-attend-to-expansion-tokens`
before running. Prefer `evaluate from-model-card` when a reviewed card exists,
because the card carries the measured best model options. Candidate ranking and
rerank top-K/depth are benchmark protocol settings, not model optimization
options, so they should be selected separately from the model card.
Late-interaction evaluation now records two standard targets when a candidate
ranking is available: full-corpus exact MaxSim retrieval for `Target: All`, and
candidate-set exact MaxSim reranking for `Target: Reranking`. The candidate
reranking path uses the same `--candidate-ranking` and `--rerank-top-k` options
as dense, sparse, and CrossEncoder reranker runs. Keep the default
`--candidate-ranking reranking_hybrid` and default all-candidate rerank depth for
leaderboard runs unless a benchmark note explicitly calls for another candidate
set.

For `jinaai/jina-colbert-v2`, the documented PyLate initialization uses
`query_prefix="[QueryMarker]"`, `document_prefix="[DocumentMarker]"`,
`attend_to_expansion_tokens=True`, and `trust_remote_code=True`. Use the
matching CLI options unless the current model card says otherwise.

Use `evaluate reranker` for CrossEncoder-style rerankers. They score only the
candidate subset and require a candidate ranking such as BM25.

Use `evaluate bm25` for BM25:

```bash
uv run hakari-bench evaluate bm25 \
  --dataset DATASET_NAME
```

By default, BM25 reads the selected dataset candidate subset. Use local BM25
computation only when explicitly requested with `--bm25-source computed`, or
from `build-candidates bm25` when generating candidate subsets.

## Attention And Runtime Choices

- Prefer the attention implementation officially recommended by the model author
  or model card. Use `--attn-implementation sdpa`, `--flash-attn2`, or
  `--attn-implementation flash_attention_2` explicitly when that is the intended
  runtime. Unspecified attention falls back to the Transformers/model default and
  may be substantially slower during long benchmark runs.
- Do not assume Flash Attention 2 works with every model or every Transformers
  major version.
- Compare practical options before large runs:
  - Transformers 4.x + Flash Attention 2.
  - Transformers 5.x + SDPA.
- Use the `tf4-fa2` uv dependency group for the Transformers 4.x + Flash
  Attention 2 runtime:

  ```bash
  uv run --group tf4-fa2 hakari-bench evaluate dense \
    --model MODEL_ID \
    --dataset DATASET_NAME \
    --flash-attn2
  ```

- Treat Transformers 5.x + Flash Attention 2 as suspect unless already verified
  for that model in this environment.
- Prefer the fastest verified configuration that preserves correctness and
  model defaults.
- For models that fail with Flash Attention 2, retry with SDPA or no explicit
  attention implementation before skipping.
- If CUDA OOM or repeated runtime errors occur, retry with smaller batch sizes
  before changing dtype, attention implementation, or sequence length.

## Long Benchmark Waves

Use both GPUs when available by assigning separate processes with
`CUDA_VISIBLE_DEVICES` or `--device`. Keep concurrent jobs writing to distinct
model output directories. For long benchmark waves, keep an ignored checklist
under `tmp/` and update it as tasks complete.

Respect existing result JSON. Cached results are skipped unless `--overwrite`
is provided. Use `--overwrite` only when correcting an intentionally changed run
configuration.

When all required Hugging Face datasets and models are already available in the
local cache, run benchmark commands with `HF_DATASETS_OFFLINE=1` and
`HF_HUB_OFFLINE=1`. This prevents the datasets and hub clients from calling the
Hugging Face API for metadata checks, which can make repeated local evaluation
runs faster and less sensitive to transient hub errors. Do not use these
variables for a first run or any run that needs to download missing artifacts.

Example:

```bash
HF_DATASETS_OFFLINE=1 HF_HUB_OFFLINE=1 \
  uv run hakari-bench evaluate dense \
    --model MODEL_NAME \
    --dataset DATASET_NAME \
    --dtype bf16
```

## Result Hygiene

Per-task result JSON should preserve enough metadata to explain the run:

- dataset revision,
- model revision,
- prompts and prompt names,
- embedding variants and representation metadata,
- dtype and attention implementation,
- Transformers, Sentence Transformers, and Torch versions,
- custom backend loader and non-secret loader/encode kwargs when used,
- batch size,
- timing,
- parameter counts,
- model maximum sequence length.

Task result JSON stores only the default `nDCG@10` and `acc@100` metric values.
Recompute other viewer metrics from saved top-100 ranking artifacts during
DuckDB warehouse creation instead of expanding every result JSON with redundant
metric cutoffs.

Top-100 ranking rows are embedded in each task result JSON under
`artifacts.top_rankings` because they are the canonical source for later metric
recomputation. The embedded artifact contains base retrieval, available
embedding variants, BM25/reranker outputs, candidate-rerank outputs, and binary
qrels relevant corpus ids. Rebuild the DuckDB warehouse after evaluation to
compute `nDCG@100`, `recall@10`, `recall@100`, `acc@1`, `acc@10`, `acc@100`,
`mrr@10`, and `map@100` for the viewer. See
[`docs/leaderboard_metrics.md`](leaderboard_metrics.md) for the leaderboard
metric policy and rationale.

When comparing models, check that prompt and embedding-variant choices are fair
and intentional.

## Coverage Audit Before Reporting

Before reporting a leaderboard or diagnosing model differences, audit coverage:

1. Confirm every base model has the expected task count for the selected view.
2. Confirm each intended embedding-variant category exists for each model:
   base, standalone truncation, standalone quantized search, rescore, truncation
   x quantized search, and truncation x rescore when those comparisons were
   intended.
3. Compare variant task counts against the model's base task count. Any variant
   with fewer rows needs investigation before it is used in a ranking. If the
   missing variant is a truncate dimension equal to the base embedding dimension,
   it should have been skipped as a no-op.
4. Inspect missing `(benchmark, task_key)` pairs for incomplete variants.
5. Confirm output JSON `config.embedding_variants` contains the intended
   variants. A dense truncation run should include standalone truncation,
   full-dim quantized/rescore, and truncation x quantized/rescore variants
   unless `--no-default-embedding-variants` was used.
6. Rebuild DuckDB/HTML viewer artifacts after adding or correcting benchmark
   results.

Useful DuckDB checks:

```sql
SELECT
  model_name,
  COALESCE(embedding_variant_name, 'base') AS variant,
  embedding_dim,
  quantization,
  COUNT(*) AS task_rows,
  COUNT(DISTINCT benchmark || '::' || task_key) AS distinct_tasks
FROM task_results
GROUP BY ALL
ORDER BY model_name, variant;
```

```sql
WITH base_tasks AS (
  SELECT DISTINCT model_name, benchmark, task_key
  FROM task_results
  WHERE embedding_variant_name IS NULL
),
variants AS (
  SELECT DISTINCT model_name, embedding_variant_name
  FROM task_results
  WHERE embedding_variant_name IS NOT NULL
),
variant_tasks AS (
  SELECT DISTINCT model_name, embedding_variant_name, benchmark, task_key
  FROM task_results
  WHERE embedding_variant_name IS NOT NULL
)
SELECT
  v.model_name,
  v.embedding_variant_name,
  COUNT(*) AS missing_tasks
FROM variants v
JOIN base_tasks b USING (model_name)
LEFT JOIN variant_tasks vt
  ON vt.model_name = v.model_name
 AND vt.embedding_variant_name = v.embedding_variant_name
 AND vt.benchmark = b.benchmark
 AND vt.task_key = b.task_key
WHERE vt.task_key IS NULL
GROUP BY ALL
ORDER BY model_name, embedding_variant_name;
```

Summarize failures plainly. If a model keeps failing after reasonable batch-size
and attention fallbacks, mark it skipped with the exact reason.
