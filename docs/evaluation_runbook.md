# Evaluation Runbook

This document is the practical command runbook for evaluating models, building or appending DuckDB databases, and opening the HAKARI-Bench leaderboard viewer. It provides runnable examples for full and partial evaluation, dense, sparse, reranker, late-interaction, BM25, custom model backends, result directory handling, remote result sync, Xet or snapshot rebuilds, metadata-backed BM25 materialization, append-only DuckDB updates, and local viewer startup. Coding agents should use this file when searching for concrete CLI commands, `hakari-bench evaluate`, `build_results_database_and_report.py`, `sync_remote_results_and_rebuild.py`, append workflows, viewer URLs, or before-reporting checks.

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

For offline dense embedding providers such as OpenAI Batch API, use the
three-step `batch dense register/fetch/materialize` workflow documented in
[`batch_inference.md`](batch_inference.md). Materialized batch outputs use the
same per-task result JSON format as direct evaluation.

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

## Sync Remote Results And Rebuild

The canonical remote result JSON lives in the private Hugging Face dataset repo
`hakari-bench/results`. Keep a git/LFS checkout under
`~/.cache/hakari-bench/hf-datasets/` and rebuild the DuckDB from that checkout
when refreshing the published leaderboard data.

Use the helper for the standard path:

```bash
uv run python scripts/sync_remote_results_and_rebuild.py \
  --sync-backend xet
```

By default, this does the following:

1. Keeps a git checkout of `https://huggingface.co/datasets/hakari-bench/results`
   at `~/.cache/hakari-bench/hf-datasets/hakari-bench__results__xet`.
2. Fetches the requested revision with LFS smudge disabled, resets the checkout
   with `git reset --hard FETCH_HEAD`, then runs
   `git xet install --local --path ...` so Git LFS can use the Xet transfer
   agent for Xet-backed payloads.
3. Removes untracked/stale files with `git clean -fdx`, then runs
   `git lfs pull --include hakari-results/** --exclude ''`. Git LFS/Xet reuses
   existing local cache objects and downloads only missing payloads for the
   requested revision.
4. Rebuilds the DuckDB from the synced Hugging Face result JSON only:

   ```bash
   uv run python scripts/build_results_database_and_report.py \
     --results-dir ~/.cache/hakari-bench/hf-datasets/hakari-bench__results__xet/hakari-results \
     --duckdb-path output/clean-hf-results-duckdb/hakari-bench__results__xet/hakari_bench.duckdb
   ```

The dataset repo is private, so authenticate before syncing, for example with
`hf auth login` or a configured Hugging Face git credential. If the checkout
already exists and you only want to rebuild from local files without refreshing
or cleaning it, pass `--skip-git-sync`.

The default DuckDB path is outside the cached dataset checkout:
`output/clean-hf-results-duckdb/{checkout-name}/hakari_bench.duckdb`. This keeps
the Hugging Face results checkout git-clean after a rebuild while making clear
that the database was rebuilt from the clean synced result JSON.

The helper does not generate missing BM25 baseline JSON by default. If you need
to backfill `hakari-results/bm25/**/*.json.xz` from local
`task_docs/metadata/**.json`, opt in explicitly with
`--materialize-bm25-baseline-from-metadata`. That path uses the stored Nano-set
`candidate_subsets.bm25` scores; it does not load candidate parquet files, run
`evaluate bm25`, or recompute BM25 with `bm25s`.

The helper also supports the older `snapshot` backend name:

```bash
uv run python scripts/sync_remote_results_and_rebuild.py \
  --sync-backend snapshot
```

This uses `huggingface_hub.snapshot_download()` instead of git commands. The
default snapshot cache is separate from the git/LFS and named Xet checkouts:
`~/.cache/hakari-bench/hf-datasets/hakari-bench__results__snapshot`. The helper
cleans this managed directory by default before downloading so files deleted
from the remote dataset do not remain locally. Use `--no-snapshot-clean` only
when intentionally resuming or reusing an incomplete local snapshot. Tune
parallelism with `--snapshot-max-workers`; the default is `32`. The helper sets
`HF_XET_HIGH_PERFORMANCE=1` for git-xet and snapshot downloads unless
`--no-xet-high-performance` is passed.

Use the git/LFS backend only when you specifically need a git checkout:

```bash
uv run python scripts/sync_remote_results_and_rebuild.py \
  --sync-backend git
```

The plain git backend fetches the requested revision with LFS smudge disabled, runs
`git reset --hard FETCH_HEAD`, removes stale untracked files with
`git clean -fdx`, then runs
`git lfs pull --include hakari-results/** --exclude ''` without first running
`git xet install`. Existing LFS objects are reused from the local git/LFS cache.

Useful variants:

```bash
# Rebuild from an existing checkout without syncing new remote files.
uv run python scripts/sync_remote_results_and_rebuild.py \
  --skip-git-sync
```

```bash
# Refresh only a metadata-backed BM25 subset before rebuilding.
uv run python scripts/sync_remote_results_and_rebuild.py \
  --materialize-bm25-baseline-from-metadata \
  --bm25-dataset NanoBEIR-en \
  --bm25-split NanoArguAna
```

```bash
# Regenerate all metadata-backed BM25 baseline JSON before rebuilding.
uv run python scripts/sync_remote_results_and_rebuild.py \
  --materialize-bm25-baseline-from-metadata \
  --bm25-overwrite
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

Remote DuckDB downloads are normalized through a shared "remote latest" cache at
`~/.cache/hakari-bench/duckdb/remote_latest_hakari_bench.duckdb`. The cache uses
Hugging Face file metadata when available and records a sidecar SHA-1 so repeat
append/viewer runs can skip downloading or copying unchanged files. Override the
cache path with `HAKARI_BENCH_REMOTE_LATEST_DUCKDB_PATH` and the sidecar metadata
path with `HAKARI_BENCH_REMOTE_LATEST_DUCKDB_METADATA_PATH`.

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

When the viewer uses `--hf-dataset-repo-id`, it reads the same remote latest
cache described above and copies it to the viewer's local DuckDB only when the
contents differ.

## Before Reporting

Before treating a model comparison as final:

1. Confirm every intended base task was evaluated.
2. Confirm each intended embedding variant has the same task coverage as the
   base result, except for no-op truncation dimensions that were skipped.
3. Rebuild or append into the DuckDB after adding or correcting result JSON.
4. Open the viewer and inspect the model under the relevant benchmark and
   overall views.
