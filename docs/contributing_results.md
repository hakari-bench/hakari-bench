# Contributing Result Files

This document defines how external benchmark runs should be submitted to the
private Hugging Face dataset repository `hakari-bench/results`.

The goal is to keep contributed model results reviewable, reproducible, and
easy to merge into the main HAKARI-Bench result warehouse.

## Repository Layout

Submit one model result directory per pull request whenever possible. The
canonical path inside `hakari-bench/results` is:

```text
PROJECT_ROOT/hakari-results/{model_dir}/
```

Use the same model directory encoding as normal HAKARI-Bench output, replacing
the Hugging Face slash with a double underscore:

```text
Alibaba-NLP/gte-multilingual-base
-> Alibaba-NLP__gte-multilingual-base
```

The submitted directory should contain per-task result files only:

```text
PROJECT_ROOT/hakari-results/{model_dir}/{dataset_id_or_name}/{task}.json.xz
```

Do not include local caches, generated DuckDB files, HTML reports, progress
checklists, or scratch files. Compressed `.json.xz` files are expected and are
covered by the dataset repository's Git LFS rules.

## Before Running Evaluation

Read [`docs/benchmark_evaluation.md`](benchmark_evaluation.md) before running a
large evaluation. It is the source of truth for runtime options, prompt policy,
embedding variant policy, attention implementation choices, and coverage
audits.

Contributed runs should generally use the standard built-in benchmark target:

```bash
uv run hakari-bench evaluate dense \
  --model MODEL_NAME \
  --all \
  --dtype bf16 \
  --device cuda:0
```

Use the appropriate subcommand for the model family:

- `dense` for SentenceTransformers-compatible embedding models.
- `sparse` for SentenceTransformers `SparseEncoder` models.
- `reranker` for SentenceTransformers `CrossEncoder` models.
- `late-interaction` for PyLate ColBERT models.
- `bm25` only for BM25 baselines.

If the run intentionally covers only a subset of benchmarks, state that clearly
in the PR body and explain why.

## Required Review Information

Every PR should include enough detail for a reviewer to understand and
reproduce the measurement:

- Model ID and exact model revision.
- Dataset revision(s), as recorded in the result JSON.
- Evaluation command or job manifest.
- Evaluation method and important runtime options:
  `dtype`, `device`, `batch_size`, attention implementation, trust-remote-code,
  max sequence length, prompt settings, candidate ranking, and rerank top-k.
- Machine environment: GPU, CUDA, Python, torch, transformers,
  sentence-transformers, and datasets versions.
- Core set `nDCG@10` summary.
- Notes about retries, resumed tasks, memory pressure, batch-size changes, or
  any intentionally non-default setting.

Do not edit result JSON by hand to fill missing metadata. If metadata is wrong
or incomplete, rerun or regenerate the affected result files.

## Generate the PR Body

Use the helper script to create a Markdown PR body from the result files. The
script reads `.json`, `.json.gz`, and `.json.xz` directly; it does not require
decompressing files into the repository.

```bash
uv run python scripts/generate_results_pr_template.py \
  PROJECT_ROOT/hakari-results/{model_dir} \
  --output tmp/{model_dir}_results_pr.md
```

If the local results are still under an evaluation output directory, pass that
directory and set the final Hub path explicitly:

```bash
uv run python scripts/generate_results_pr_template.py \
  output/results_nano_reranking_hybrid_full_late_rerun_20260603_json_xz/{model_dir} \
  --repo-path PROJECT_ROOT/hakari-results/{model_dir} \
  --output tmp/{model_dir}_results_pr.md
```

The generated template includes:

- Overall Core set `nDCG@10`.
- Per-Core-component `nDCG@10`.
- Result file counts.
- Model, dataset, runtime, package, CUDA, and timestamp metadata extracted from
  the result JSON.
- TODO fields for the exact command and human notes.

Fill every TODO before opening the PR.

## Open a Hugging Face Dataset PR

Use `hf upload --create-pr` so reviewers can inspect the change before it is
merged. For one model directory:

```bash
PR_BODY="$(cat tmp/{model_dir}_results_pr.md)"
hf upload hakari-bench/results \
  PROJECT_ROOT/hakari-results/{model_dir} \
  PROJECT_ROOT/hakari-results/{model_dir} \
  --repo-type dataset \
  --create-pr \
  --commit-message "Add results for MODEL_NAME" \
  --commit-description "$PR_BODY"
```

If your local directory is not already under `PROJECT_ROOT/hakari-results`, use
the local evaluation directory as the second argument and keep the Hub path as
the third argument:

```bash
PR_BODY="$(cat tmp/{model_dir}_results_pr.md)"
hf upload hakari-bench/results \
  output/results/{model_dir} \
  PROJECT_ROOT/hakari-results/{model_dir} \
  --repo-type dataset \
  --create-pr \
  --commit-message "Add results for MODEL_NAME" \
  --commit-description "$PR_BODY"
```

Prefer `hf upload` for PR submissions because it creates one commit for the
model directory. `hf upload-large-folder` is useful for resumable bulk uploads,
but it does not expose `--create-pr` in the installed CLI and can create many
commits for one model, which may hit repository commit rate limits.

## Reviewer Checklist

Reviewers should check:

- The PR modifies only `PROJECT_ROOT/hakari-results/{model_dir}/`.
- The model directory name matches the model ID.
- The files are compressed result JSON files, plus only expected small sidecar
  metadata files when applicable.
- The generated PR summary matches the submitted files.
- The Core set score has enough task coverage for the claim being made.
- The result metadata records model revision, dataset revision, runtime options,
  package versions, and CUDA information.
- Any non-default prompt, max sequence length, attention implementation,
  trust-remote-code use, candidate ranking, rerank top-k, or batch-size change
  is justified in the PR notes.

After merge, rebuild the result DuckDB or leaderboard artifacts from
`hakari-bench/results` before publishing comparisons.
