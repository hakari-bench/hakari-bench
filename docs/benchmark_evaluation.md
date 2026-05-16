# Benchmark Evaluation Guide

This document is the canonical repository guidance for running HAKARI-Bench
evaluations. Do not rely on skill-local benchmark instructions as the source of
truth. Skill files may point here, but evaluation commands, variant policy, and
coverage checks should be maintained in this document.

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
4. Decide the full embedding-variant plan before starting any large run.
5. Run a small validation command when options are uncertain, then scale to the
   requested benchmark set.
6. Keep an ignored progress checklist under `tmp/` for long benchmark waves.
7. After benchmarking, rebuild DuckDB/HTML viewer artifacts when the user asks
   for comparisons, leaderboards, or viewer updates. If results are split
   across multiple result roots, pass repeated `--results-dir` options in
   priority order; earlier directories win duplicate model-task JSON conflicts.
8. Audit result coverage before treating a leaderboard as final.

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
- Check whether `--trust-remote-code` is required.
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

This is the most important coverage rule:

> For dense models, specify truncation dimensions with
> `--embedding-variant truncate:DIMS` when dimensional comparisons are needed.
> The CLI will automatically add standalone truncation, full-dim quantized and
> rescored variants, and truncation x quantized/rescore variants for those dims.

Use `--no-default-embedding-variants` only when the run intentionally needs base
results without automatic dense quantized/rescore variants.

`--retrieval-score-device auto` keeps supported post-encode score/top-k work on
the model output device. Use `--retrieval-score-device cpu` or
`--retrieval-score-device cuda` only when intentionally forcing that work.

## Dense Variant Plans

For plain dense baselines with no dimensional comparisons, omit explicit
embedding variants and let the dense defaults run:

```bash
uv run hakari-bench evaluate dense \
  --model MODEL_NAME \
  --dataset DATASET_NAME \
  --dtype bf16
```

For Matryoshka or other dimension comparisons, provide the truncation dimensions:

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

## Sparse Evaluation

Use `evaluate sparse` for SentenceTransformers `SparseEncoder` models:

```bash
uv run hakari-bench evaluate sparse \
  --model MODEL_NAME \
  --dataset DATASET_NAME
```

Do not add dense quantized embedding variants for sparse/SPLADE-style models.
Sparse quantization is intentionally unsupported in the CLI. Use post-encode
sparse truncation variants for footprint and latency trade-offs.

Query-only sparsity limits:

```bash
uv run hakari-bench evaluate sparse \
  --model MODEL_NAME \
  --dataset DATASET_NAME \
  --embedding-variant sparse-query-max-active-dims:8,16,32
```

Query/document grids:

```bash
uv run hakari-bench evaluate sparse \
  --model MODEL_NAME \
  --dataset DATASET_NAME \
  --embedding-variant sparse-query-max-active-dims:8,16,32 \
  --embedding-variant sparse-document-max-active-dims:64,128,256 \
  --embedding-variant-grid sparse-query-max-active-dims:8,16,32 sparse-document-max-active-dims:64,128,256
```

If only the full query x document grid is requested, the standalone query-only
and document-only variants may be omitted. The base no-limit result is always
included as `evaluation.embedding_evaluations[0]`.

## Late-Interaction, Reranker, And BM25

Use `evaluate late-interaction` for PyLate ColBERT models. Check
model-specific query/document prefixes, sequence lengths, `--trust-remote-code`,
and `--late-interaction-attend-to-expansion-tokens` before running.

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
- batch size,
- timing,
- parameter counts,
- model maximum sequence length.

Top-100 ranking artifacts are optional because they are much larger than the
summary task JSON. Pass `--save-top-rankings` when a run needs per-query ranked
corpus ids for metric recomputation, rank-fusion analysis, or candidate audits.
When enabled, each evaluated task writes a referenced artifact under
`rankings/{split_or_task}.top100.json` containing base retrieval, available
embedding variants, BM25/reranker outputs, and candidate-rerank outputs. Rebuild
the DuckDB warehouse after evaluation to expose these rows in
`retrieval_rankings`.

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
   with fewer rows needs investigation before it is used in a ranking.
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
