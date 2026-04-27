# Repository Guidelines

## Project Overview

This repository implements a Nano-style information retrieval benchmark runner
for SentenceTransformers-compatible models.

The library code lives under `nano_ir_benchmark/`. Built-in dataset definitions
live under `config/datasets/`, and dataset collection definitions live under
`config/dataset_collections/`.

## Environment

- Use Python 3.12.
- Use `uv` for dependency management and command execution.
- Add runtime dependencies with `uv add`.
- Add development-only dependencies with `uv add --dev`.
- Keep `uv.lock` updated when dependencies change.

## Development Workflow

- Follow TDD for behavioral changes: add or update focused tests before
  changing implementation when practical.
- Prefer small, scoped changes that match the existing modules:
  - `bm25.py` for BM25 candidate generation, BM25 baseline evaluation,
    and tokenizer dispatch.
  - `datasets.py` for dataset specs, collections, split/task resolution.
  - `models.py` for model loading and runtime/model metadata.
  - `evaluation.py` for dataset loading and task scoring.
  - `metrics.py` for IR metric calculation.
  - `results.py` for output paths, cache behavior, and JSON payloads.
  - `cli.py` for command-line parsing and orchestration.
- Keep generated benchmark results out of commits. `output/` is intentionally
  ignored.

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

## Benchmark Behavior

- The default model loader is SentenceTransformers dense embedding.
- Supported model type options are `dense`, `sparse`, `reranker`, and
  `late-interaction`; late interaction is currently reserved for a future
  adapter.
- Default dtype is `bf16`.
- `--trust-remote-code`, `--flash-attn2`, `--attn-implementation`, and dtype
  options must remain explicit CLI options.
- Prompt overrides should be optional. If no prompt or prompt name is provided,
  preserve SentenceTransformers model prompt behavior.
- Result files are written below:

```text
output/results/{model_name}/{huggingface_dataset_name}/{split_or_task}.json
```

- Existing result files should be skipped unless `--override` is provided.
- BM25 evaluation and candidate generation use `bm25s` with the standard
  Okapi-style Robertson method. If `--bm25-tokenizer` is omitted, auto-select
  the tokenizer by sampling 10 queries and detecting language with
  `fast-langdetect`: use `wordseg` for supported languages and `regex` for all
  others. Persist the resolved BM25 algorithm/tokenizer in result JSON.
- BM25 `wordseg` tokenizer support is optional. Keep language-specific
  dependencies behind the `wordseg` extra and lazy-load them only when the
  tokenizer is selected.
- Metadata should preserve as much runtime detail as practical, including batch
  size, dtype, package versions, torch/CUDA info, total parameters, trainable
  parameters, and active/transformer parameters.

## Dataset Configuration

- Add new datasets as YAML files under `config/datasets/`.
- Add grouped benchmark definitions under `config/dataset_collections/`.
- Keep dataset specs generic enough to handle:
  - datasets split by task,
  - datasets not split by task,
  - collection-style benchmarks such as `MNanoBEIR`.
- `MNanoBEIR` is defined as a built-in collection in
  `config/dataset_collections/mnanobeir.yaml`.
- Keep benchmark naming consistent across docs, configs, and tests:
  `MNanoBEIR`, `NanoMIRACL`, `NanoMLDR`, and `NanoCodeSearchNet`.
