# HAKARI-Bench

HAKARI-Bench is a benchmark runner and leaderboard viewer for compact
information retrieval evaluation. It runs SentenceTransformers-compatible
dense, sparse, reranker, late-interaction, and BM25 systems on Nano-set task
collections, then turns the result JSON into a DuckDB-backed leaderboard.

The main workflow is:

1. Evaluate a model.
2. Build or update the local results database.
3. Open the viewer and compare results.

## Quick Start

Use Python 3.12 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --group all
```

Evaluate a dense embedding model on the standard built-in task set:

```bash
uv run hakari-bench evaluate dense \
  --model MODEL_NAME \
  --all \
  --dtype bf16
```

Per-task result files are written under:

```text
output/hakari-results/{model_id}/{huggingface_dataset_name}/{split_or_task}.json.xz
```

Existing result files are skipped unless `--overwrite` is provided, so the same
command can resume an interrupted run.

## Evaluate Models

Dense embedding evaluation is the default path:

```bash
uv run hakari-bench evaluate dense \
  --model hotchpotch/bekko-embedding-pico-beta-unir-v7 \
  --dataset hakari-bench/NanoBEIR-en
```

You can evaluate every standard built-in benchmark with `--all`, a collection
with `--collection`, a dataset with `--dataset`, or a single split/task with
`--split`.

```bash
uv run hakari-bench evaluate dense \
  --model MODEL_NAME \
  --collection MNanoBEIR
```

Other model families use explicit subcommands:

```bash
uv run hakari-bench evaluate sparse --model naver/splade-v3 --dataset NanoBEIR-en
```

```bash
uv run hakari-bench evaluate reranker --model nreimers/mmarco-mMiniLMv2-L6-H384-v1 --dataset NanoRTEB
```

```bash
uv run --group pylate hakari-bench evaluate late-interaction --model MODEL_NAME --dataset NanoMedical
```

```bash
uv run hakari-bench evaluate bm25 --dataset NanoMLDR --split ja
```

Dense runs automatically include full-dimension `int8`, `binary`,
`rescore:int8`, and `rescore:binary` embedding variants. Truncation dimensions
can be added with `--embedding-variant truncate:DIMS`; use
`--no-default-embedding-variants` only when the run should intentionally skip
the default variant plan.

For long runs, choose runtime options deliberately:

- Use the attention implementation recommended by the model author, such as
  `--attn-implementation sdpa` or `--flash-attn2`.
- Keep the model's default maximum sequence length unless you intentionally
  want a less comparable run.
- Use `--model-alias` for local model paths so result files and viewer rows have
  stable logical model IDs.

See the [evaluation runbook](docs/evaluation_runbook.md) for complete runnable
commands, append mode, local model aliases, offline/cache usage, and result
database workflows. See the [evaluation policy](docs/evaluation_policy.md) for
prompt handling, attention choices, embedding variants, and coverage audits.

## View Results

Build a DuckDB leaderboard database from result JSON:

```bash
uv run python scripts/build_results_database_and_report.py \
  --results-dir output/hakari-results \
  --duckdb-path output/hakari-results/hakari_bench.duckdb
```

To refresh the canonical remote result JSON first, run:

```bash
uv run python scripts/sync_remote_results_and_rebuild.py \
  --sync-backend xet
```

That helper syncs the private Hugging Face results dataset into
`~/.cache/hakari-bench/hf-datasets/hakari-bench__results__xet` as a git
checkout, runs `git xet install --local` in that checkout, then pulls only
`hakari-results/**` through Git LFS using the Xet transfer agent when the remote
supports it. Existing local Xet/LFS cache objects are reused and only missing
payloads for the requested revision are downloaded. The plain `git` backend
remains available for normal git/LFS checkouts and also disables LFS smudge
during reset before pulling only `hakari-results/**`. The helper does not
generate missing BM25 baseline JSON by default, run a BM25 evaluation, or
recompute BM25 with `bm25s`. The rebuilt clean DuckDB is written outside the
checkout under `output/clean-hf-results-duckdb/` so the cached dataset repo can
remain git-clean. See
[`docs/evaluation_runbook.md`](docs/evaluation_runbook.md) for the detailed
sync/rebuild workflow.

For the older snapshot backend name, use:

```bash
uv run python scripts/sync_remote_results_and_rebuild.py \
  --sync-backend snapshot
```

The `snapshot` backend uses `huggingface_hub.snapshot_download()` and stores
files in a separate managed cache directory ending in `__snapshot`.

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
  --results-dir output/hakari-results \
  --results-dir output/hakari-results-combined_20260510_1340 \
  --overwrite-result-duplicates \
  --exclude-model-name hotchpotch/bekko-embedding-pico-beta-unir-v9-GOR \
  --duckdb-path output/hakari-results/hakari_bench.duckdb
```

To add a separate result root for new model-task JSON to an existing DuckDB
without scanning the original result roots, use `--append-results-dir`. This is
append-only: duplicate result paths or duplicate logical model-task rows are
rejected.

```bash
uv run python scripts/build_results_database_and_report.py \
  --append-results-dir output/new_model_results \
  --duckdb-path output/hakari-results/hakari_bench.duckdb
```

If the target DuckDB does not exist, append mode can download the latest
configured remote DuckDB before adding local results. Use
`--append-base-duckdb latest` with `--append-output-duckdb` to create a separate
merged copy, and `--model-name-override local/experiment_name` when a local
result directory should be shown under a specific logical model id. See
[`docs/evaluation_runbook.md`](docs/evaluation_runbook.md) for
examples.

The remote "latest" DuckDB is cached at
`~/.cache/hakari-bench/duckdb/remote_latest_hakari_bench.duckdb` by default and
is shared by append mode and the viewer's Hugging Face dataset source. Override
that path with `HAKARI_BENCH_REMOTE_LATEST_DUCKDB_PATH`; override the sidecar
metadata path with `HAKARI_BENCH_REMOTE_LATEST_DUCKDB_METADATA_PATH`.

Start the viewer:

```bash
uv run hakari-bench web \
  --source-duckdb-path output/hakari-results/hakari_bench.duckdb
```

By default, the viewer binds to `127.0.0.1:8000` and keeps
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

The DuckDB warehouse stores task results, long-form metrics, diagnostics, and
dataset metadata for leaderboard views and notebook/SQL analysis. The default
visible metrics are documented in
[leaderboard metric policy](docs/leaderboard_metrics.md), and the database
schema is documented in [DuckDB schema](docs/duckdb_schema.md).

## Built-In Benchmarks

Built-in dataset definitions live under `config/datasets/`, and collection
definitions live under `config/dataset_collections/`.

The built-in Nano-set families include `NanoBEIR-en`, `MNanoBEIR`,
`NanoMIRACL`, `NanoMLDR`, `NanoJMTEB`, `NanoRTEB`, `NanoMTEB`, `NanoCMTEB`,
`NanoMMTEB`, `NanoFaMTEB`, `NanoRuMTEB`, `NanoVNMTEB`, `NanoMTEB-Misc`,
`NanoLongEmbed`, `NanoCoIR`, `NanoIFIR`, `NanoLaw`, `NanoMedical`,
`NanoRARb`, `NanoBRIGHT`, `NanoCodeRAG`, `NanoChemTEB`, `NanoR2MED`,
`NanoBuiltBench`, `NanoBIRCO`, and `NanoDAPFAM`.

The NanoMTEB family follows MTEB benchmark provenance rather than legacy
language buckets. Named benchmark families such as C-MTEB, JMTEB, FaMTEB,
ruMTEB, and VN-MTEB use dedicated Nano dataset names. Retrieval tasks that do
not belong to a specific official MTEB family are grouped under
`NanoMTEB-Misc`.

## Documentation

- [Evaluation runbook](docs/evaluation_runbook.md): practical evaluate, build,
  append, and viewer commands.
- [New model evaluation to results PR workflow](docs/new_model_results_workflow.md):
  end-to-end checklist from model research and model card creation through
  evaluation, coverage audit, and `.json.xz` result submission.
- [Evaluation policy](docs/evaluation_policy.md): runtime choices, prompt
  behavior, embedding variants, and coverage-audit rules.
- [Leaderboard metric policy](docs/leaderboard_metrics.md): default visible
  leaderboard metrics and rationale.
- [DuckDB schema](docs/duckdb_schema.md): result warehouse schema, query
  semantics, and viewer data model.
- [Model cards](docs/model_cards.md): static HAKARI-Bench model metadata.
- [Custom model backends](docs/custom_model_backends.md): loading non-standard
  model objects through `--model-loader`.
- [Late-interaction evaluation](docs/late_interaction_evaluation.md):
  PyLate/ColBERT evaluation notes.
- [SentenceTransformers integration](docs/sentence_transformers_evaluation_integration.md):
  training-time evaluators for dense, sparse, reranker, and BM25 workflows.
- [Creating Nano-set datasets](docs/create_nano_datasets.md): workflow for
  generating upload-ready Nano-set dataset repositories.
- [Contributing result files](docs/contributing_results.md): result submission
  format and review metadata.
- [Hugging Face Space deployment](docs/huggingface_space_deploy.md): public
  leaderboard deployment notes.

## Development

Run the full validation suite with:

```bash
uv run tox
```

For quicker iteration:

```bash
uv run --group all pytest -q
uv run ruff check .
uv run --group all ty check
```

## Acknowledgements

HAKARI-Bench is built on the idea behind
[Nano-BEIR](https://huggingface.co/blog/sionic-ai/eval-sionic-nano-beir). The
NanoBEIR evaluation implementation in
[Sentence Transformers](https://github.com/huggingface/sentence-transformers/)
was a reference for this project.

## Disclaimer

HAKARI-Bench results are provided for informational and comparative purposes
only. Scores may be incomplete, inaccurate, or affected by dataset sampling,
upstream dataset changes, model or runtime configuration, library versions,
hardware, or implementation issues.

HAKARI-Bench, its maintainers, and contributors provide the software,
leaderboard data, and benchmark results "as is", without warranty of any kind.
To the maximum extent permitted by applicable law, they are not liable for any
loss, damage, or other consequence arising from use of, reliance on, or
interpretation of HAKARI-Bench results.

## License

MIT License. See [LICENSE](LICENSE).

## Author

Yuichi Tateno ([@hotchpotch](https://github.com/hotchpotch))
