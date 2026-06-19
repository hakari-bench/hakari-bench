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
  `docs/evaluation_runbook.md` for the practical evaluate-build-viewer
  workflow and `docs/evaluation_policy.md` as the source of truth for
  prompt/runtime choices, embedding variant policy, and result coverage audits.
- Prefer the attention implementation officially recommended by the evaluated
  model. Use explicit `--attn-implementation sdpa`, `--flash-attn2`, or
  `--attn-implementation flash_attention_2` when appropriate; leaving attention
  unspecified can make long benchmark runs substantially slower for some models.
- Dense evaluation automatically includes full-dimension `int8,binary` and
  `rescore:int8,binary` variants unless `--no-default-embedding-variants` is
  used. When dense truncation dims are supplied with
  `--embedding-variant truncate:DIMS`, the CLI also expands them into standalone
  truncation plus truncation x quantized/rescore variants.
- If a requested dense truncate dimension matches the encoded base embedding
  dimension, evaluation warns and skips that no-op truncate variant because it
  duplicates the original full-dimension result.
- After benchmark runs, audit result coverage before reporting or rebuilding
  leaderboard comparisons. Confirm base task completeness and verify that every
  intended variant category exists for each model.
- When comparing a new run against existing model data, prefer the cached remote
  DuckDB, such as
  `~/.cache/hakari-bench/duckdb/remote_latest_hakari_bench.duckdb` or the synced
  Hugging Face snapshot DuckDB, instead of reading raw result JSON or `.json.xz`
  files directly. Direct JSON reads are rarely needed for existing remote
  results and should be reserved for local run outputs or schema/debug work.

## Leaderboard Viewer

- For leaderboard viewer design changes, read `@DESIGN.md` first and keep
  design-specific rules there.
- When updating viewer UI design, check `@DESIGN.md` before editing and update
  it when the design direction, tokens, layout rules, or component behavior
  changes.
- When changing viewer design, layout, interactive controls, or generated HTML,
  install Playwright Chromium and run the browser smoke test whenever practical:

  ```bash
  uv run --only-group viewer-browser-test playwright install chromium
  uv run --only-group viewer-browser-test pytest -q -m browser tests/test_viewer_browser.py
  ```

  `uv run tox -e browser` is the CI-style shortcut for the same workflow; it
  installs Chromium before running the smoke test.

- When updating the leaderboard viewer in this project, keep
  `docs/duckdb_schema.md` in sync. Update it when DuckDB schema, viewer queries,
  leaderboard semantics, score grouping, variant handling, or required columns
  change.
- The served stylesheet `hakari_bench/viewer/assets/app.css` is a compiled,
  minified Tailwind output. Never hand-edit it. Edit the source
  `hakari_bench/viewer/assets/app.tailwind.css`, then rebuild and commit both:

  ```bash
  uv run python scripts/build_viewer_css.py            # rebuild app.css
  uv run python scripts/build_viewer_css.py --watch    # rebuild on change
  uv run python scripts/build_viewer_css.py --check     # verify in sync
  ```

  The build pins the Tailwind version for reproducible output and needs Node's
  `npx` on PATH. `uv run tox -e css` runs the `--check` in CI-style validation.
  New Tailwind utility classes used in viewer `.py`/`.js` only appear after a
  rebuild.

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
- If no attention implementation is specified for model evaluation, the CLI
  warns and delegates to the Transformers/model default. Treat that as a prompt
  to confirm the model's official recommendation before launching long runs.
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
- If `--bm25-tokenizer` is omitted for local BM25, auto-select the tokenizer
  from task metadata first and then from 10 sampled queries detected with
  `fast-langdetect`. Tasks marked `category: code` use `regex`; natural
  language tasks use `wordseg`, `english_porter_stop`, Snowball `stemmer`,
  `whitespace`, or `regex` according to the language policy in the README.
- Supported BM25 tokenizers are `regex`, `whitespace`, `transformer`, `stemmer`,
  `english_regex`, `english_porter`, `english_porter_stop`, and `wordseg`.
- `wordseg` support is optional. Keep language-specific dependencies behind the
  `wordseg` extra and lazy-load them only when the tokenizer is selected.
  Current wordseg languages are `ja`, `zh`, `th`, `ko`, and `vi`.
- Nano dataset BM25 candidate subsets used for top-100 reranking diagnostics
  should force qrels positives into the final top-k candidate list and record
  `candidate_coverage`. Query and relevant coverage should be 100% unless the
  dataset README and metadata explicitly document why that is impossible.
- Persist the resolved BM25 source, backend, algorithm, tokenizer, and candidate
  subset metadata in result JSON under `config.bm25` and `model.bm25`.

## Results and Metadata

- Per-task result files are written below:

```text
output/hakari-results/{model_id}/{huggingface_dataset_name}/{split_or_task}.json.xz
```

- Run-level summaries are derived from per-task result JSON when building the
  DuckDB database; do not write aggregate result files.
- `scripts/build_results_database_and_report.py` accepts repeated
  `--results-dir` options for merging multiple result roots. Treat the argument
  order as the merge priority: the first directory wins for duplicate
  `model_name`/task JSON, and later directories only fill missing results.
  Use `--overwrite-result-duplicates` when later directories should replace
  duplicate logical model-task rows from earlier directories.
  `model_name` comes from result JSON `model.id`; do not use `model_dir` as
  part of the logical model identity.
- DuckDB builds default to streaming result rows into DuckDB. Use
  `--materialize-results-in-python` only for the legacy materialized path or
  `--html-output` when a static HTML report is required.
- When rebuilding the canonical leaderboard DuckDB from the latest Hugging Face
  dataset results, use `scripts/sync_remote_results_and_rebuild.py` instead of
  pointing the builder at ad hoc local result directories. Prefer
  `--sync-backend xet` for the large Hugging Face results dataset; it keeps a
  git checkout under
  `~/.cache/hakari-bench/hf-datasets/hakari-bench__results__xet`, fetches with
  LFS smudge disabled, runs `git reset --hard FETCH_HEAD`, installs the local
  Git Xet transfer agent with `git xet install --local --path ...`, removes
  stale untracked files with `git clean -fdx`, and pulls only
  `hakari-results/**` LFS payloads. Existing local Git LFS/Xet cache objects
  should be reused. The rebuilt DuckDB should be written outside the checkout
  under `output/clean-hf-results-duckdb/{checkout-name}/hakari_bench.duckdb` so
  the cached Hugging Face results repo remains git-clean. The plain `git`
  backend remains available when Git Xet must not be installed. Use
  `--skip-git-sync` only when intentionally rebuilding from the existing local
  cache without cleaning or syncing.
- Use `--append-results-dir` when adding a separate root containing only new
  model-task JSON to an existing DuckDB. This mode is append-only and should
  reject duplicate result paths or duplicate logical model-task rows.
  If the target DuckDB is missing and no local base is supplied, append mode
  should download the configured latest remote DuckDB before adding results.
  Use `--append-base-duckdb` plus `--append-output-duckdb` when a new merged DB
  should be created from an existing base, and `--model-name-override` only when
  the append directory represents one logical model.
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
