# Repository Guidelines

## Project Overview

This repository implements a Nano-style information retrieval benchmark runner
for SentenceTransformers-compatible models and BM25 baselines.

Library code lives under `hakari_bench/`. Built-in dataset definitions live
under `config/datasets/`, and dataset collection definitions live under
`config/dataset_collections/`.

## Environment

- Use Python 3.12.
- Use `uv` for dependency management and command execution.
- Add runtime dependencies with `uv add`.
- Add development-only dependencies with `uv add --dev`.
- Keep `uv.lock` updated when dependencies change.
- Keep `transformers>=4` and `sentence-transformers>=5` compatibility.

## Development Workflow

- Follow TDD for behavioral changes: add or update focused tests before changing
  implementation when practical.
- Keep changes scoped to the existing module boundaries:
  - `cli.py` for command-line parsing and orchestration.
  - `datasets.py` for dataset specs, collections, split/task resolution.
  - `evaluation.py` for dataset loading and dense/sparse/reranker scoring.
  - `bm25.py` for BM25 baseline evaluation, candidate generation, and tokenizer
    dispatch.
  - `metrics.py` for IR metric calculation.
  - `models.py` for model loading and runtime/model metadata.
  - `results.py` for output paths, cache behavior, and JSON payloads.
- Prefer YAML dataset configuration over hard-coded dataset lists.
- Do not commit generated benchmark outputs, caches, or local scratch artifacts.
  `output/` and `tmp/` are intentionally ignored.

## Documentation

- Write project documentation in English unless the user explicitly requests
  another language.
- Keep reusable project workflows under `docs/`, not only under `skills/`.
  Skill files may point to the canonical docs, but they should not be the only
  place where benchmark or metadata procedures are described.

## Evaluation Execution

- Before running or scheduling benchmark evaluations, read
  `docs/benchmark_evaluation.md` and follow it as the source of truth for
  commands, prompt/runtime choices, embedding variant policy, and result
  coverage audits.
- Dense evaluation automatically includes full-dimension `int8,binary` and
  `rescore:int8,binary` variants unless `--no-default-embedding-variants` is
  used. When dense truncation dims are supplied with
  `--embedding-variant truncate:DIMS`, the CLI also expands them into standalone
  truncation plus truncation x quantized/rescore variants.
- After benchmark runs, audit result coverage before reporting or rebuilding
  leaderboard comparisons. Confirm base task completeness and verify that every
  intended variant category exists for each model.

## Leaderboard Viewer

- When updating the leaderboard viewer in this project, keep
  `docs/duckdb_schema.md` in sync. Update it when DuckDB schema, viewer queries,
  leaderboard semantics, score grouping, variant handling, or required columns
  change.

## Validation

Run the full validation suite before committing:

```bash
uv run tox
```

For quicker iteration, use:

```bash
uv run --group all pytest -q
uv run ruff check .
uv run --group all ty check
```

## Model Loading

- The default evaluation method is `evaluate dense`, loaded with
  `SentenceTransformer`.
- Supported evaluation method subcommands are `dense`, `sparse`, `reranker`,
  `late-interaction`, and `bm25`.
- `sparse` uses SentenceTransformers `SparseEncoder`.
- `reranker` uses SentenceTransformers `CrossEncoder` and requires a candidate
  ranking such as `bm25`; `--rerank-top-k` limits the candidates to rerank.
- `late-interaction` uses PyLate ColBERT and scores query/document token
  embeddings with exact MaxSim.
- Default dtype is `bf16`. Keep `--dtype`, `--trust-remote-code`,
  `--flash-attn2`, `--attn-implementation`, `--device`,
  `--model-max-seq-length`, `--truncate-dim`,
  `--sparse-query-max-active-dims`, and `--sparse-document-max-active-dims`
  explicit CLI options.
- Do not shorten model max sequence length for benchmark runs just to avoid
  slow execution or memory pressure. Use the model's default/configured maximum
  length unless the user explicitly requests a different value. If memory errors
  happen, first reduce batch size or adjust execution options; changing
  `--model-max-seq-length` makes results less comparable and must be called out
  clearly in the result metadata and summary.
- Prompt overrides are optional. If no prompt or prompt name is provided,
  preserve SentenceTransformers model prompt behavior.

## BM25 Behavior

- BM25 evaluation supports two sources:
  - By default, read the selected dataset candidate subset
    (`--candidate-ranking`, default `bm25`) and use that ranking as the BM25
    baseline.
  - Use local `bm25s` computation only when explicitly requested with
    `--bm25-source computed`, or from `build-candidates bm25` when generating
    BM25 candidate subsets.
- If the default dataset subset is unavailable, fail with an actionable error
  instead of silently recomputing BM25 locally.
- Local BM25 uses `bm25s` with the standard Okapi-style Robertson method.
- If `--bm25-tokenizer` is omitted for local BM25, auto-select the tokenizer by
  sampling 10 queries and detecting language with `fast-langdetect`: use
  `wordseg` for supported languages and `regex` for all others.
- Supported BM25 tokenizers are `regex`, `whitespace`, `transformer`, `stemmer`,
  `english_regex`, `english_porter`, `english_porter_stop`, and `wordseg`.
- `wordseg` support is optional. Keep language-specific dependencies behind the
  `wordseg` extra and lazy-load them only when the tokenizer is selected.
  Current wordseg languages are `ja`, `zh`, `th`, `ko`, and `vi`.
- Persist the resolved BM25 source, backend, algorithm, tokenizer, and candidate
  subset metadata in result JSON under `config.bm25` and `model.bm25`.

## Results and Metadata

- Per-task result files are written below:

```text
output/results/{model_id}/{huggingface_dataset_name}/{split_or_task}.json
```

- Run-level summaries are derived from per-task result JSON when building the
  DuckDB database; do not write aggregate result files.
- `scripts/build_results_database_and_report.py` accepts repeated
  `--results-dir` options for merging multiple result roots. Treat the argument
  order as the merge priority: the first directory wins for duplicate logical
  model-task JSON, and later directories only fill missing results.
- Existing result files should be skipped unless `--overwrite` is provided.
- Result JSON should preserve as much runtime detail as practical, including
  batch size, dtype, package versions, torch/CUDA info, prompts, total
  parameters, trainable parameters, embedding parameters, transformer/active
  parameters, evaluation timestamps, dataset load duration, and evaluation
  timing.
- Active parameters are currently computed as total parameters minus input
  embedding parameters when both counts are available.

## Dataset Configuration

- Add new datasets as YAML files under `config/datasets/`.
- Add grouped benchmark definitions under `config/dataset_collections/`.
- Keep dataset specs generic enough to handle:
  - datasets split by task,
  - datasets not split by task,
  - collection-style benchmarks such as `MNanoBEIR`.
- `MNanoBEIR` is defined as a built-in collection in
  `config/dataset_collections/mnanobeir.yaml`.
- Built-in dataset names should stay consistent across docs, configs, and tests:
  `NanoBEIR-en`, `MNanoBEIR`, `NanoMIRACL`, `NanoMLDR`, `NanoJMTEB`,
  `NanoRTEB`, `NanoMTEB`, `NanoCMTEB`, `NanoMMTEB`, `NanoFaMTEB`,
  `NanoRuMTEB`, `NanoVNMTEB`, `NanoMTEB-Misc`, `NanoLongEmbed`, and
  `NanoCoIR`.
