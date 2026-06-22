# Quick Start

This page gives the shortest path from a model ID to a local HAKARI-Bench
leaderboard. For complete operational guidance, use the
[evaluation runbook](evaluation_runbook.md) and [evaluation policy](evaluation_policy.md).

## 1. Install

Use Python 3.12 and [uv](https://docs.astral.sh/uv/).

In the project where you want to use HAKARI-Bench, add it directly from Git:

```bash
uv add "hakari-bench @ git+https://github.com/hakari-bench/hakari-bench.git"
```

> [!NOTE]
> HAKARI-Bench is expected to publish an updated PyPI package in the future.
> For now, install it from Git so your project uses the current benchmark code.

After that, run `hakari-bench` from your project:

```bash
uv run hakari-bench --help
```

### Installation Options

If you want to edit HAKARI-Bench locally while using it from another project,
clone it and add the local path instead:

```bash
git clone https://github.com/hakari-bench/hakari-bench.git ../hakari-bench
uv add --editable ../hakari-bench
```

Some evaluation families need optional runtime packages that are not part of
the base install. Add them in the same `uv add` command when you need them.
For example, late-interaction evaluation requires PyLate:

```bash
uv add \
  "hakari-bench @ git+https://github.com/hakari-bench/hakari-bench.git" \
  "pylate @ git+https://github.com/lightonai/pylate.git@1f1f47cee5df35ebe6fd2286a0a205a1523e4119"
```

For the local web viewer, add the viewer server packages as well:

```bash
uv add \
  "hakari-bench @ git+https://github.com/hakari-bench/hakari-bench.git" \
  "fastapi>=0.136.1" \
  "uvicorn[standard]>=0.46.0"
```

The repository's `all` dependency group is only available when working inside a
HAKARI-Bench checkout. When HAKARI-Bench is installed as a Git dependency of
another project, add the optional packages your project needs explicitly.

For benchmark development inside a clone of this repository, install the
repository dependency groups instead:

```bash
uv sync --group all
```

## 2. Evaluate A Model

Evaluate a SentenceTransformers-compatible dense embedding model:

```bash
uv run hakari-bench evaluate dense \
  --model intfloat/multilingual-e5-small \
  --dataset hakari-bench/NanoBEIR-en \
  --dtype bf16
```

Per-task result files are written under:

```text
output/hakari-results/{model_id}/{huggingface_dataset_name}/{split_or_task}.json.xz
```

Existing result files are skipped unless `--overwrite` is provided, so the same
command can resume an interrupted run.

## 3. Try Other Retrieval Families

| Method | Command |
| --- | --- |
| Dense | `uv run hakari-bench evaluate dense --model MODEL --dataset DATASET` |
| Sparse | `uv run hakari-bench evaluate sparse --model MODEL --dataset DATASET` |
| Late interaction | `uv run --group pylate hakari-bench evaluate late-interaction --model MODEL --dataset DATASET` |
| Reranker | `uv run hakari-bench evaluate reranker --model MODEL --dataset DATASET --candidate-ranking reranking_hybrid` |
| BM25 | `uv run hakari-bench evaluate bm25 --dataset DATASET` |

Dense evaluation automatically includes full-dimension `int8`, `binary`,
`rescore:int8`, and `rescore:binary` variants unless
`--no-default-embedding-variants` is used. Add truncation variants with:

```bash
uv run hakari-bench evaluate dense \
  --model MODEL \
  --dataset DATASET \
  --embedding-variant truncate:768,512,256
```

For long runs, confirm prompt handling, dtype, attention implementation, model
maximum sequence length, and embedding variants in the
[evaluation policy](evaluation_policy.md).

## 4. Build A Local Results Database

Build a DuckDB leaderboard database from local result JSON:

```bash
uv run python scripts/build_results_database_and_report.py \
  --results-dir output/hakari-results \
  --duckdb-path output/hakari-results/hakari_bench.duckdb
```

To refresh the latest public result JSON first, use:

```bash
uv run python scripts/sync_remote_results_and_rebuild.py \
  --sync-backend xet
```

See [docs/duckdb_schema.md](duckdb_schema.md) for result warehouse semantics and
SQL examples.

## 5. Open The Viewer

```bash
uv run hakari-bench web \
  --source-duckdb-path output/hakari-results/hakari_bench.duckdb
```

For deployment and Hugging Face Space operations, see
[docs/huggingface_space_deploy.md](huggingface_space_deploy.md).

## 6. Submit Results

Use [docs/new_model_results_workflow.md](new_model_results_workflow.md) for the
end-to-end checklist before publishing model results. Use
[docs/contributing_results.md](contributing_results.md) for the expected
`.json.xz` layout and Hugging Face Dataset PR workflow.

## More Guides

| Topic | Link |
| --- | --- |
| Full evaluation commands | [evaluation_runbook.md](evaluation_runbook.md) |
| Evaluation policy | [evaluation_policy.md](evaluation_policy.md) |
| Custom or hosted models | [custom_model_backends.md](custom_model_backends.md) |
| Late interaction | [late_interaction_evaluation.md](late_interaction_evaluation.md) |
| OpenAI embeddings | [openai_embedding_evaluation.md](openai_embedding_evaluation.md) |
| Batch inference | [batch_inference.md](batch_inference.md) |
| SentenceTransformers integration | [sentence_transformers_evaluation_integration.md](sentence_transformers_evaluation_integration.md) |
| Nano-set creation | [create_nano_datasets.md](create_nano_datasets.md) |
| Dataset source metadata | [dataset_citation_metadata.md](dataset_citation_metadata.md) |
| Leaderboard metrics | [leaderboard_metrics.md](leaderboard_metrics.md) |
