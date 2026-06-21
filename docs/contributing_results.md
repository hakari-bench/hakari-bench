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
merged. A reference for the recommended staging plus `hf upload --create-pr`
flow is
[`hakari-bench/results` PR #8](https://huggingface.co/datasets/hakari-bench/results/discussions/8),
which contributed two related LiquidAI LFM2.5 model result directories in one
Dataset PR.

The recommended path is to build a clean staging directory that contains only
the compressed result files, then let the Hub CLI create the Dataset PR and
attach the file commit in one operation. This works for ordinary one-model
submissions and for related multi-model submissions that should be reviewed
together.

```bash
MODEL_DIR=MODEL_ID_WITH_DOUBLE_UNDERSCORE
SOURCE_DIR=output/hakari-results/${MODEL_DIR}
STAGING_ROOT=tmp/hf-results-${MODEL_DIR}

rm -rf "${STAGING_ROOT}"
mkdir -p "${STAGING_ROOT}/hakari-results/${MODEL_DIR}"

rsync -a \
  --include='*/' \
  --include='*.json.xz' \
  --exclude='*' \
  "${SOURCE_DIR}/" \
  "${STAGING_ROOT}/hakari-results/${MODEL_DIR}/"

find "${STAGING_ROOT}/hakari-results" -type f ! -name '*.json.xz' -print
find "${STAGING_ROOT}/hakari-results" \
  \( -name '*.duckdb' -o -name '*.duckdb.wal' \) \
  -print
find "${STAGING_ROOT}/hakari-results" -type f -name '*.json.xz' | wc -l
```

The first two `find` commands should print nothing. The final count should
match the intended result file count from the generated PR body.

Upload the staged tree. Use `uv run hf` when the Hub CLI is installed in this
project environment rather than on `PATH`:

```bash
PR_BODY="$(cat tmp/${MODEL_DIR}_results_pr.md)"
uv run hf upload hakari-bench/results \
  "${STAGING_ROOT}/hakari-results" \
  hakari-results \
  --repo-type dataset \
  --create-pr \
  --commit-message "Add results for MODEL_NAME" \
  --commit-description "$PR_BODY"
```

For a related multi-model PR, create one staging root and repeat the `rsync`
step for each model directory under `STAGING_ROOT/hakari-results/`. Combine the
generated per-model PR bodies into one reviewed body before running
`uv run hf upload --create-pr`.

The upload command returns a commit URL. The matching Dataset PR can be found
from the repository discussions; it is a pull request backed by a `refs/pr/N`
ref:

```bash
uv run python - <<'PY'
from huggingface_hub import HfApi

api = HfApi()
for discussion in api.get_repo_discussions(
    repo_id="hakari-bench/results",
    repo_type="dataset",
):
    if discussion.is_pull_request and discussion.status == "open":
        print(
            discussion.num,
            discussion.title,
            f"https://huggingface.co/datasets/hakari-bench/results/discussions/{discussion.num}",
        )
PY
```

After the PR is created, verify that its diff contains only the intended result
files:

```bash
PR_NUMBER=8  # replace with your Dataset PR discussion number
CHECK_DIR=tmp/hf-results-pr-${PR_NUMBER}-check

rm -rf "${CHECK_DIR}"
mkdir -p "${CHECK_DIR}"
git -C "${CHECK_DIR}" init -q
git -C "${CHECK_DIR}" remote add origin \
  https://huggingface.co/datasets/hakari-bench/results
git -C "${CHECK_DIR}" fetch --depth=1 --filter=blob:none origin \
  refs/heads/main:refs/remotes/origin/main \
  refs/pr/${PR_NUMBER}:refs/remotes/origin/pr

git -C "${CHECK_DIR}" diff --name-only origin/main origin/pr | wc -l
git -C "${CHECK_DIR}" diff --name-only origin/main origin/pr |
  grep -v '^hakari-results/.*\.json\.xz$' || true
```

The `grep -v` command should print nothing. If the first PR comment needs a
correction after upload, edit it in the Hugging Face web UI or with
`HfApi.edit_discussion_comment()` when your token has discussion write
permission.

### Fallback: Manual Dataset PR Ref Workflow

For private or organization-owned dataset repositories, `hf upload --create-pr`
can fail with a 403 even when normal git push is allowed. Large submissions can
also fail after spending time hashing or uploading. In that case, use the
manual Dataset PR ref workflow below: create the Hugging Face Dataset PR first,
then attach a reviewed git commit to that PR's `refs/pr/{number}` ref.

### Prepare a Local Staging Commit

Use a no-smudge clone so Git does not download every existing LFS payload in the
results warehouse. The local branch is only a staging branch; it is not the
final review target.

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

Then inspect and commit locally:

```bash
git status --short
git diff --stat
git lfs status
find "hakari-results/${MODEL_DIR}" -type f | grep -v '\.json\.xz$' || true
find . -name '*.duckdb' -o -name '*.duckdb.wal'

git add "hakari-results/${MODEL_DIR}"
git commit -m "Add results for MODEL_NAME"
```

The two `find` commands should print nothing. Do not include generated DuckDB
files, `.duckdb.wal` files, viewer artifacts, local caches, temporary reports,
or model YAML files unless the PR explicitly intends to add metadata.

### Create the Dataset PR

Create the Hugging Face Dataset PR before pushing the result commit to the PR
ref. The usual fallback is the Hugging Face web UI: open the dataset
repository, choose **Contribute**, create a Dataset PR, and paste the generated
body from `tmp/${MODEL_DIR}_results_pr.md`.

If the Web UI requires a branch to start the PR, push an empty or minimal
staging branch first, create the PR, and treat that branch only as a way to
obtain the PR number:

```bash
git push origin "${BRANCH}"
```

After the PR exists, note its discussion number from the URL, for example
`https://huggingface.co/datasets/hakari-bench/results/discussions/2` means
`PR_NUMBER=2`. The description should include at least:

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

### Attach the Commit to the Dataset PR Ref

Hugging Face Dataset PRs are backed by special refs such as `refs/pr/2`. The
result commit must be on that PR ref. If the PR ref is not already at your
result commit, fetch it, cherry-pick the local staging commit, and push back to
the same PR ref:

```bash
PR_NUMBER=2
git fetch origin refs/pr/${PR_NUMBER}:pr/${PR_NUMBER}
git checkout pr/${PR_NUMBER}
git cherry-pick "${BRANCH}"  # or cherry-pick the specific local commit SHA
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
review or merge. After the PR ref contains the result commit, any temporary
normal branch can be deleted:

```bash
git push origin :"${BRANCH}"
```

## Reviewer Checklist

Reviewers should check:

- The PR modifies only the intended `hakari-results/{model_dir}/` path or
  explicitly related model-result paths.
- The model directory name matches the model ID.
- The files are compressed result JSON files; any sidecar metadata is explicitly
  justified by the PR.
- The generated PR summary matches the submitted files.
- The Overall score has enough task coverage for the claim being made.
- The result metadata records model revision, dataset revision, runtime options,
  package versions, and CUDA information.
- Any non-default prompt, max sequence length, attention implementation,
  trust-remote-code use, candidate ranking, rerank top-k, or batch-size change
  is justified in the PR notes.

After merge, rebuild the result DuckDB or leaderboard artifacts from
`hakari-bench/results` before publishing comparisons.
