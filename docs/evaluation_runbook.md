# Evaluation Runbook

This guide covers the practical workflow for evaluating a model, adding its
result JSON to a viewer DuckDB database, and opening the leaderboard viewer.

Use this file when you need runnable commands for evaluation, DuckDB updates,
or viewer startup. Use [`evaluation_policy.md`](evaluation_policy.md) when you
need to decide prompt behavior, attention implementation, embedding variants,
offline/cache policy, or coverage-audit requirements.

## Full Evaluation

Use `--all` to evaluate every standard built-in benchmark task. Existing task
results are skipped unless `--overwrite` is supplied, so this command is safe
for resuming interrupted runs.

```bash
uv run hakari-bench evaluate dense \
  --model MODEL_NAME \
  --all \
  --dtype bf16 \
  --device cuda:0
```

Per-task outputs default to compressed JSON files:

```text
output/hakari-results/{model_id}/{huggingface_dataset_name}/{split_or_task}.json.xz
```

Use `--result-format json` only when a plain `.json` result tree is required.
Use `--results-dir DIR` when a run should write to a separate result root.

If the required Hugging Face datasets and model artifacts are already cached
locally, you can run in offline mode:

```bash
HF_DATASETS_OFFLINE=1 HF_HUB_OFFLINE=1 \
  uv run hakari-bench evaluate dense \
    --model MODEL_NAME \
    --all \
    --dtype bf16 \
    --device cuda:0
```

This avoids repeated Hugging Face API metadata checks during repeat runs. See
[`evaluation_policy.md#long-benchmark-waves`](evaluation_policy.md#long-benchmark-waves)
before using offline mode for a large benchmark wave.

Local models can be evaluated directly. Give them a stable alias so later
viewer rows have a useful logical model name:

```bash
uv run hakari-bench evaluate dense \
  --model /path/to/local/model \
  --model-alias model_exp_122 \
  --all \
  --dtype bf16 \
  --device cuda:0
```

An alias without a slash is recorded as `local/{alias}`.

## Partial Evaluation

Use a dataset, collection, or explicit split/task when you only need a subset.

```bash
uv run hakari-bench evaluate dense \
  --model MODEL_NAME \
  --collection MNanoBEIR \
  --dtype bf16
```

```bash
uv run hakari-bench evaluate dense \
  --model MODEL_NAME \
  --dataset hakari-bench/NanoJMTEB \
  --split ja_cqadupstack \
  --dtype bf16
```

`--evaluation-scope standard` is the default and skips tasks marked
`include_by_default: false`. Use `--evaluation-scope all` when an intentionally
wider run should include extended or expensive tasks.

## Evaluation Methods

Dense embedding models use the default `evaluate dense` subcommand:

```bash
uv run hakari-bench evaluate dense \
  --model MODEL_NAME \
  --all
```

Dense runs automatically include full-dimension `int8`, `binary`,
`rescore:int8`, and `rescore:binary` variants. When truncation dimensions are
specified, the CLI also expands them into standalone truncation and truncation x
quantized/rescore variants:

```bash
uv run hakari-bench evaluate dense \
  --model MODEL_NAME \
  --all \
  --embedding-variant truncate:256,128,64
```

For Matryoshka/truncate-aware models, include the supported truncation
dimensions unless the run is intentionally base-only. See
[`evaluation_policy.md#dense-evaluation`](evaluation_policy.md#dense-evaluation)
for how to choose the variant plan.

Use `--no-default-embedding-variants` only when those automatic variants should
be intentionally omitted.

Sparse, reranker, late-interaction, and BM25 baselines use their matching
subcommands:

```bash
uv run hakari-bench evaluate sparse \
  --model naver/splade-v3 \
  --all
```

```bash
uv run hakari-bench evaluate reranker \
  --model MODEL_NAME \
  --all \
  --candidate-ranking reranking_hybrid \
  --batch-size 128
```

```bash
uv run --group pylate hakari-bench evaluate late-interaction \
  --model MODEL_NAME \
  --all
```

```bash
uv run hakari-bench evaluate bm25 \
  --all
```

For long GPU runs, pass the model author's recommended attention option when
known, such as `--attn-implementation sdpa`, `--flash-attn2`, or
`--attn-implementation flash_attention_2`. Reduce `--batch-size` before
changing model maximum sequence length.

## Custom Model Backends

The built-in loaders use SentenceTransformers for dense, sparse, and reranker
evaluation, and PyLate for late-interaction evaluation. When a model needs to
be evaluated through another Python library or a hosted embedding/reranker API,
pass a custom loader with `--model-loader module:function`.

The loader receives `ModelLoadConfig` and returns a duck-typed model object.
No base-class inheritance is required. Dense and sparse backends expose
`encode_query` / `encode_document` or `encode`; rerankers expose `rank`,
`predict`, or `__call__`; late-interaction backends expose `encode(...,
is_query=...)`.

```bash
uv run hakari-bench evaluate dense \
  --model api/embed-v1 \
  --model-loader my_pkg.hakari_loader:load_model \
  --model-loader-kwargs-json '{"endpoint":"https://example.test","model":"embed-v1"}' \
  --encode-kwargs-json '{"dimensions":1024}' \
  --query-encode-kwargs-json '{"input_type":"query"}' \
  --document-encode-kwargs-json '{"input_type":"document"}'
```

See [`custom_model_backends.md`](custom_model_backends.md) for the full
interface contract and the dummy backend example.

## Build the Viewer DuckDB

Build or rebuild the viewer database from result JSON:

```bash
uv run python scripts/build_results_database_and_report.py
```

With no arguments, the builder reads `output/hakari-results` and writes
`output/hakari-results/hakari_bench.duckdb`. It streams selected results into
DuckDB by default, which keeps Python memory small and preserves stable physical
ordering for good DuckDB compression.

Useful build options:

```bash
uv run python scripts/build_results_database_and_report.py \
  --results-dir output/hakari-results \
  --duckdb-path output/hakari-results/hakari_bench.duckdb \
  --incremental
```

```bash
uv run python scripts/build_results_database_and_report.py \
  --results-dir output/hakari-results \
  --results-dir output/other-results \
  --overwrite-result-duplicates \
  --exclude-model-name MODEL_TO_SKIP \
  --duckdb-path output/hakari-results/hakari_bench.duckdb
```

Static HTML report generation is still supported, but it uses the
Python-materialized path:

```bash
uv run python scripts/build_results_database_and_report.py \
  --results-dir output/hakari-results \
  --duckdb-path output/hakari-results/hakari_bench.duckdb \
  --html-output output/hakari-results/report.html
```

## Append New Results

Use append mode when you already have a complete viewer DuckDB and only need to
add a separate result root containing new model-task JSON. Append mode rejects
duplicate result paths and duplicate logical model-task rows.

Update an existing local DuckDB in place:

```bash
uv run python scripts/build_results_database_and_report.py \
  --append-results-dir output/local-model-results \
  --duckdb-path output/hakari-results/hakari_bench.duckdb
```

Create a new merged DuckDB from a local base file:

```bash
uv run python scripts/build_results_database_and_report.py \
  --append-results-dir output/local-model-results \
  --append-base-duckdb path/to/base.duckdb \
  --append-output-duckdb output/hakari-results/merged.duckdb
```

If the target `--duckdb-path` does not exist and no local base is supplied, the
builder can download the latest configured remote DuckDB before appending:

```bash
uv run python scripts/build_results_database_and_report.py \
  --append-results-dir output/local-model-results \
  --duckdb-path output/hakari-results/hakari_bench.duckdb \
  --append-hf-dataset-repo-id hakari-bench/leaderboard_database
```

Use an explicit remote base when you want to create a separate merged file:

```bash
uv run python scripts/build_results_database_and_report.py \
  --append-results-dir output/local-model-results \
  --append-base-duckdb latest \
  --append-hf-dataset-repo-id hakari-bench/leaderboard_database \
  --append-hf-dataset-path duckdb/hakari_bench.duckdb \
  --append-output-duckdb output/hakari-results/merged.duckdb
```

When the result JSON came from a local path and needs a different logical model
name in the viewer, override it during loading:

```bash
uv run python scripts/build_results_database_and_report.py \
  --append-results-dir output/local-model-results \
  --duckdb-path output/hakari-results/hakari_bench.duckdb \
  --model-name-override local/model_exp_122
```

Use `--model-name-override` only when the input append directory represents one
logical model.

## Open the Viewer

Start the local viewer:

```bash
uv run hakari-bench web \
  --source-duckdb-path output/hakari-results/hakari_bench.duckdb
```

For remote access from another machine:

```bash
uv run hakari-bench web \
  --source-duckdb-path output/hakari-results/hakari_bench.duckdb \
  --host 0.0.0.0 \
  --port 28090
```

If the viewer should sync from a results directory instead of a specific file,
use `--source-results-dir output/hakari-results`.

## Before Reporting

Before treating a model comparison as final:

1. Confirm every intended base task was evaluated.
2. Confirm each intended embedding variant has the same task coverage as the
   base result, except for no-op truncation dimensions that were skipped.
3. Rebuild or append into the DuckDB after adding or correcting result JSON.
4. Open the viewer and inspect the model under the relevant benchmark and
   overall views.
