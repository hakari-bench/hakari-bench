# Repository Guidelines

## Project Overview

This repository implements a Nano-style information retrieval benchmark runner
for SentenceTransformers-compatible models and BM25 baselines.

Library code lives under `nano_ir_benchmark/`. Built-in dataset definitions live
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
uv run pytest -q
uv run ruff check .
uv run ty check
```

## Model Loading

- The default model type is `dense`, loaded with `SentenceTransformer`.
- Supported `--model-type` values are `dense`, `sparse`, `reranker`,
  `late-interaction`, and `bm25`.
- `sparse` uses SentenceTransformers `SparseEncoder`.
- `reranker` uses SentenceTransformers `CrossEncoder` and requires a candidate
  subset such as `bm25`; `--rerank-top-n` limits the candidates to rerank.
- `late-interaction` uses a minimal ColBERT-style AutoModel adapter that emits
  token embeddings and scores them with MaxSim.
- Default dtype is `bf16`. Keep `--dtype`, `--trust-remote-code`,
  `--flash-attn2`, `--attn-implementation`, `--device`,
  `--model-max-seq-length`, and `--truncate-dim` explicit CLI options.
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
  - If an evaluation dataset has the selected candidate subset
    (`--candidate-subset-name`, default `bm25`), use that ranking as the BM25
    baseline.
  - If the subset is unavailable, compute BM25 locally with `bm25s`.
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
output/results/{model_name}/{huggingface_dataset_name}/{split_or_task}.json
```

- Aggregate results are written to:

```text
output/results/{model_name}/all.json
```

- Existing result files should be skipped unless `--override` is provided.
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
  `NanoRTEB`, `NanoMTEB`, `NanoCMTEB`, `NanoMMTEB`, `NanoLongEmbed`, and
  `NanoCoIR`.
