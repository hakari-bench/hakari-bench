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
uv run hakari-bench evaluate reranker --model nreimers/mmarco-mMiniLMv2-L6-H384-v1 --dataset NanoRTEB
uv run --group pylate hakari-bench evaluate late-interaction --model MODEL_NAME --dataset NanoMedical
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

Start the viewer:

```bash
uv run hakari-bench web \
  --source-duckdb-path output/hakari-results/hakari_bench.duckdb
```

The viewer binds to `127.0.0.1:8000` by default. It can also read a DuckDB file
from a Hugging Face dataset:

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

## License

MIT License. See [LICENSE](LICENSE).

## Author

Yuichi Tateno ([@hotchpotch](https://github.com/hotchpotch))
