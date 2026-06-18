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

Read [`docs/evaluation_policy.md`](evaluation_policy.md) before running a
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
- Overall `nDCG@10` summary.
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

- Overall `nDCG@10`.
- Per-Overall-component `nDCG@10`.
- Result file counts.
- Model, dataset, runtime, package, CUDA, and timestamp metadata extracted from
  the result JSON.
- TODO fields for the exact command and human notes.

Fill every TODO before opening the PR.

## Open a Hugging Face Dataset PR

Use a Hugging Face Dataset PR so reviewers can inspect the change before it is
merged. A recent reference is
[`hakari-bench/results` PR #2](https://huggingface.co/datasets/hakari-bench/results/discussions/2),
which contributed 551 sparse result files for
`hotchpotch/japanese-splade-v2`.

For small submissions, `hf upload --create-pr` can work directly:

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

For private or organization-owned dataset repositories, `hf upload --create-pr`
can fail with a 403 even when normal git push is allowed. Large submissions also
spend time hashing or uploading before failing. In that case, use the git/Web UI
workflow below. It is the preferred path for large result directories.

### Prepare a Results Branch

Use a no-smudge clone so Git does not download every existing LFS payload in the
results warehouse:

```bash
MODEL_DIR=hotchpotch__japanese-splade-v2
SOURCE_DIR=output/hakari-results/${MODEL_DIR}
BRANCH=add-japanese-splade-v2-results

hf auth login
git lfs install
git xet install
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/datasets/hakari-bench/results
cd results
git checkout -b "${BRANCH}"
```

`git lfs install` configures Git LFS filters used by existing result payloads.
`git xet install` configures Git Xet filters used by Hugging Face repositories
that store large files through Xet. Run both before cloning or fetching the
dataset repo. If `git xet` is unavailable, install the Hugging Face Git Xet
extension first; otherwise clone, fetch, or push can fail when the repository
uses Xet-backed storage.

Copy only the `.json.xz` result files, preserving the canonical path:

```bash
mkdir -p "hakari-results/${MODEL_DIR}"
rsync -a \
  --include='*/' \
  --include='*.json.xz' \
  --exclude='*' \
  "${SOURCE_DIR}/" \
  "hakari-results/${MODEL_DIR}/"
```

Then inspect, commit, and push the branch:

```bash
git status --short
git diff --stat
git lfs status
find "hakari-results/${MODEL_DIR}" -type f | grep -v '\.json\.xz$' || true
find . -name '*.duckdb' -o -name '*.duckdb.wal'

git add "hakari-results/${MODEL_DIR}"
git commit -m "Add results for MODEL_NAME"
git push origin "${BRANCH}"
```

The two `find` commands should print nothing. Do not include generated DuckDB
files, `.duckdb.wal` files, viewer artifacts, local caches, temporary reports,
or model YAML files unless the PR explicitly intends to add metadata.

### Create the Dataset PR from the Web UI

Open the pushed branch in the Hugging Face web UI:

```text
https://huggingface.co/datasets/hakari-bench/results/tree/{BRANCH}
```

Use the **Contribute** button to create a Dataset PR. Paste the generated PR
body from `tmp/{model_dir}_results_pr.md` into the description. The description
should include at least:

- model id and result directory,
- result file count,
- evaluation method,
- Overall `nDCG@10` summary,
- exact model revision,
- runtime options such as dtype, device, batch size, attention implementation,
  trust-remote-code, max sequence length, candidate ranking, and rerank top-k,
- relevant package/CUDA environment,
- notes about retries, resumed tasks, smaller batch-size reruns, or partial
  coverage,
- a checklist confirming no DuckDB, caches, reports, or unrelated files are
  included.

PR #2 is a concrete example of the expected shape: it reported the sparse
`hotchpotch/japanese-splade-v2` result count, Overall `nDCG@10`, grouped Overall
component scores, model revision, runtime environment, a reconstructed command,
and submitter notes explaining that one task used a smaller batch size.

After the Web UI creates the PR, Hugging Face may show a special PR ref such as
`refs/pr/2`. If the PR ref is not already at your result commit, fetch that ref
and push your commit to it:

```bash
PR_NUMBER=2
git fetch origin refs/pr/${PR_NUMBER}:pr/${PR_NUMBER}
git checkout pr/${PR_NUMBER}
git cherry-pick "${BRANCH}"
git push origin pr/${PR_NUMBER}:refs/pr/${PR_NUMBER}
```

Do not delete `refs/pr/${PR_NUMBER}`; that is the active Hugging Face Dataset
PR. If the PR ref already contains reviewer changes or another contributor's
commit, fetch `refs/pr/${PR_NUMBER}` again and build on top of it. Do not reset
or force-push a Hugging Face PR ref unless the PR owner explicitly coordinates
that rewrite.

Useful checks after pushing to the PR ref:

```bash
git ls-remote origin refs/pr/${PR_NUMBER}
hf discussions info hakari-bench/results ${PR_NUMBER} --repo-type dataset
hf discussions diff hakari-bench/results ${PR_NUMBER} --repo-type dataset
```

The PR body is the first discussion comment. Update it from the Hugging Face web
UI after creating the PR. The Hugging Face Hub Python API can inspect PRs, and
`HfApi.edit_discussion_comment()` can edit comments when the token has the
right permission, but contributors should not rely on API-based body editing as
part of the required workflow.

Use the Hugging Face web UI's **Publish** button when the PR is ready for
review or merge. After the PR ref is populated, any temporary normal branch can
be deleted:

```bash
git push origin :"${BRANCH}"
```

## Reviewer Checklist

Reviewers should check:

- The PR modifies only `PROJECT_ROOT/hakari-results/{model_dir}/`.
- The model directory name matches the model ID.
- The files are compressed result JSON files, plus only expected small sidecar
  metadata files when applicable.
- The generated PR summary matches the submitted files.
- The Overall score has enough task coverage for the claim being made.
- The result metadata records model revision, dataset revision, runtime options,
  package versions, and CUDA information.
- Any non-default prompt, max sequence length, attention implementation,
  trust-remote-code use, candidate ranking, rerank top-k, or batch-size change
  is justified in the PR notes.

After merge, rebuild the result DuckDB or leaderboard artifacts from
`hakari-bench/results` before publishing comparisons.
