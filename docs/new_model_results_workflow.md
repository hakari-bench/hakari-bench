# New Model Evaluation To Results PR Workflow

This document is the end-to-end checklist for evaluating a new model and submitting HAKARI-Bench result files for review. It connects model research, model card creation, small validation runs, full `--all` evaluations, dense and sparse variant policy, reranker and late-interaction settings, coverage and metadata audits, result PR body generation, GitHub code PR expectations, and Hugging Face Dataset result submission. Coding agents should use this file when searching for new model onboarding, evaluation-to-results workflow, result PR preparation, model card review, `.json.xz` submission, contributor expectations, reproducibility checks, or maintainer acceptance caveats for similar model variants.

> [!NOTE]
> 新しいモデルの投稿は基本的に welcome ですが、既存モデルを若干改善したものや
> バリエーションが多いものは、場合によっては取り込みを行わない、または一部モデル
> のみ取り込みを行う場合があります。また、評価結果に再現性がない場合、たとえば別
> 環境で評価結果が大きく異なる場合なども、取り込みを行わない場合があります。

This document is the end-to-end checklist for evaluating a new model with
HAKARI-Bench and submitting its `.json.xz` result files for review.

Use it as the entry point. The detailed policy and commands live in the linked
documents:

- [`evaluation_policy.md`](evaluation_policy.md): source of truth for prompts,
  runtime choices, embedding variants, cache policy, retries, and coverage
  audits.
- [`evaluation_runbook.md`](evaluation_runbook.md): runnable evaluation,
  DuckDB append/build, and viewer commands.
- [`model_cards.md`](model_cards.md): how to create and review static model
  metadata under `config/model_cards/`.
- [`model_specific_benchmarking_notes.md`](model_specific_benchmarking_notes.md):
  known model-family prompt, attention, truncation, and compatibility notes.
- [`contributing_results.md`](contributing_results.md): result repository
  layout, PR body generation, and Hugging Face Dataset PR workflow.
- [`custom_model_backends.md`](custom_model_backends.md): required interface
  when a model cannot be loaded directly by the built-in SentenceTransformers or
  PyLate loaders.
- [`late_interaction_evaluation.md`](late_interaction_evaluation.md): extra
  notes for ColBERT/PyLate-style models.
- [`leaderboard_metrics.md`](leaderboard_metrics.md): metric policy for the
  leaderboard and Overall summaries.

## 1. Research The Model Before Running

Do this before launching any long benchmark job:

1. Identify the evaluation method:
   - `dense` for SentenceTransformers-compatible embedding models.
   - `sparse` for SentenceTransformers `SparseEncoder` models.
   - `reranker` for CrossEncoder-style rerankers.
   - `late-interaction` for PyLate/ColBERT-style models.
   - `bm25` only for BM25 baselines.
2. Read the upstream Hugging Face model card and any official paper or release
   note. Then check
   [`model_specific_benchmarking_notes.md`](model_specific_benchmarking_notes.md)
   for repository-local decisions.
3. Record prompt behavior. Prefer the model's SentenceTransformers prompt
   configuration when present. Use explicit prompt options only when the model
   requires them.
4. Record runtime requirements: dtype, attention implementation, batch-size
   expectation, `--trust-remote-code`, full model revision, maximum sequence
   length, and custom loader or provider encode kwargs when applicable.
5. Decide the variant plan before the run. For dense models, this primarily
   means researching whether the model supports Matryoshka or other documented
   truncation dimensions.

Dense variant rules:

- Plain dense models with no documented truncation support should omit explicit
  variants. The dense CLI automatically includes full-dimension `int8`,
  `binary`, `rescore:int8`, and `rescore:binary` variants.
- Matryoshka or truncate-aware dense models should include every documented
  supported dimension that should appear in the leaderboard:

  ```bash
  --embedding-variant truncate:768,512,256,128,64
  ```

  The CLI expands this into standalone truncation variants, full-dimension
  quantized/rescore variants, and truncation x quantized/rescore variants.
- If a requested truncate dimension equals the base embedding dimension, the CLI
  warns and skips it as a no-op. That skipped dimension should not be treated as
  missing coverage.
- Use `--no-default-embedding-variants` only for an intentional ablation or
  base-only run, and call that out in the PR notes.

Sparse, reranker, and late-interaction variant rules:

- Sparse runs automatically include the standard query/document max-active-dims
  grid unless defaults are disabled. Do not add dense quantization variants to
  sparse models.
- Rerankers do not use embedding variants. Confirm candidate ranking and rerank
  depth instead.
- Late-interaction runs currently support truncate variants only. Confirm
  prefixes, token lengths, query expansion, and candidate-reranking settings in
  the model card or the late-interaction guide.

## 2. Write And Review The Model Card

Every new non-BM25 model should have a reviewed model card. The card documents
the model-specific facts that make the run reproducible and lets
`evaluate from-model-card` reuse them.

Generate a first draft:

```bash
uv run python scripts/generate_model_cards.py \
  --model MODEL_ID \
  --model-type dense \
  --truncate-dims none \
  --dataset hakari-bench/NanoBEIR-en \
  --output-dir config/model_cards
```

For truncate-aware dense models, pass the documented dimensions:

```bash
uv run python scripts/generate_model_cards.py \
  --model MODEL_ID \
  --model-type dense \
  --truncate-dims 64 128 256 512 \
  --dataset hakari-bench/NanoBEIR-en \
  --output-dir config/model_cards
```

Review and edit the generated YAML under `config/model_cards/`. At minimum,
check:

- `id`, `source.name`, and pinned `source.revision`.
- `method`.
- `embedding.truncate_dims`: numeric list for documented dense truncate
  dimensions, or `null` when the model should not be treated as
  truncation-compatible.
- `runtime`: dtype, attention implementation, backend, max sequence length,
  trust-remote-code flags, and similarity function.
- `prompts`: prompt names, prompt text, or encode tasks required by the model.
- `late_interaction`: ColBERT-specific prefixes, token lengths, expansion, and
  scoring fields when relevant.
- `language_support`: display metadata for the leaderboard when enough evidence
  exists.
- `target`: the intended benchmark target when the card is meant to drive
  `from-model-card` evaluation.

If `runtime.trust_remote_code: true`, the card must also set
`runtime.remote_code_approved: true` and use a full 40-character reviewed
Hugging Face commit SHA in `source.revision`.

Result PRs to `hakari-bench/results` should normally contain only `.json.xz`
files. Add or update `config/model_cards/*.yaml` in the GitHub code repository
as a separate code change unless maintainers explicitly request model metadata
in the result PR. Most contributors and evaluation workers should assume they
do not have direct push permission to the GitHub repository, so model cards,
viewer/schema changes, docs updates, or benchmark code fixes should be submitted
as a GitHub PR. See [`model_cards.md`](model_cards.md) for the full schema and
generation options.

## 3. Run A Small Validation

Before `--all`, run one small task or collection with the exact options you plan
to use:

```bash
uv run hakari-bench evaluate from-model-card \
  --model-card config/model_cards/MODEL_ID_WITH_DOUBLE_UNDERSCORE.yaml \
  --dataset hakari-bench/NanoBEIR-en \
  --split NanoArguAna \
  --dtype bf16 \
  --device cuda:0
```

Alternatively, run the method-specific command directly:

```bash
uv run hakari-bench evaluate dense \
  --model MODEL_ID \
  --dataset hakari-bench/NanoBEIR-en \
  --split NanoArguAna \
  --dtype bf16 \
  --device cuda:0 \
  --embedding-variant truncate:512,256,128
```

Check that the output result JSON records the intended model revision, dataset
revision, prompts, dtype, attention implementation, batch size, package
versions, runtime metadata, and `config.embedding_variants`.

## 4. Run The Full Evaluation

For standard leaderboard coverage, use `--all`. Existing `.json.xz` task files
are skipped unless `--overwrite` is supplied, so interrupted runs can be
resumed.

From a reviewed model card:

```bash
uv run hakari-bench evaluate from-model-card \
  --model-card config/model_cards/MODEL_ID_WITH_DOUBLE_UNDERSCORE.yaml \
  --all \
  --batch-size 32 \
  --device cuda:0
```

Direct dense command:

```bash
uv run hakari-bench evaluate dense \
  --model MODEL_ID \
  --all \
  --dtype bf16 \
  --device cuda:0 \
  --attn-implementation sdpa \
  --embedding-variant truncate:512,256,128
```

Omit `--embedding-variant truncate:...` when the dense model has no documented
truncate support. Keep the model's default maximum sequence length unless the
user explicitly asks for a different value. If memory errors occur, reduce
`--batch-size` first.

Per-task outputs default to:

```text
output/hakari-results/{model_id}/{huggingface_dataset_name}/{split_or_task}.json.xz
```

Use `--results-dir DIR` for an isolated run root. Do not commit `output/`,
DuckDB files, HTML reports, cache files, or temporary progress checklists to the
code repository.

## 5. Audit Coverage And Metadata

Before opening a result PR, build or append a DuckDB and inspect the model in
the viewer:

```bash
uv run python scripts/build_results_database_and_report.py \
  --results-dir output/hakari-results \
  --duckdb-path output/hakari-results/hakari_bench.duckdb \
  --incremental

uv run hakari-bench web \
  --source-duckdb-path output/hakari-results/hakari_bench.duckdb
```

Audit at least:

- Every intended base task exists for the target scope.
- Every intended dense variant category exists: base, standalone truncation,
  full-dimension quantized search, full-dimension rescore, truncation x
  quantized search, and truncation x rescore.
- Variant task counts match the base task count, except for skipped no-op
  truncate dimensions.
- `config.embedding_variants` in the result JSON matches the planned variant
  list.
- Prompt, dtype, attention, trust-remote-code, batch-size, model revision, and
  dataset revisions are present and intentional.
- Failed or retried tasks are explained and rerun where practical.

Use the SQL checks in the coverage audit section of
[`evaluation_policy.md`](evaluation_policy.md#coverage-audit-before-reporting)
when the run includes many tasks or variants.

## 6. Generate The Result PR Body

Create a PR body from the result files:

```bash
MODEL_DIR=MODEL_ID_WITH_DOUBLE_UNDERSCORE

uv run python scripts/generate_results_pr_template.py \
  output/hakari-results/${MODEL_DIR} \
  --output tmp/${MODEL_DIR}_results_pr.md
```

Fill every TODO in the generated Markdown. The PR body should include the exact
command or job manifest, model revision, dataset revisions, method, runtime
options, Overall `nDCG@10` summary, package/CUDA environment, retries, batch-size
changes, and any intentional partial coverage or non-default variant choice.

## 7. Open The GitHub Code PR

Open a GitHub PR for any code-repository changes required by the evaluation.
Common examples are:

- New or updated `config/model_cards/*.yaml`.
- Documentation updates that explain model-specific runtime choices.
- Viewer, DuckDB schema, or leaderboard display changes needed for the new
  metadata.
- Custom backend loaders under `examples/` or library changes needed to run the
  model.

Keep generated benchmark outputs, DuckDB files, caches, and local scratch files
out of the GitHub PR. If the only deliverable is result JSON, this section can
be skipped.

The GitHub PR and Hugging Face results PR should link to each other when both
exist. The ideal flow is:

1. Open whichever PR is ready first.
2. Include its URL in the second PR body.
3. Edit the first PR body or add a comment with the second PR URL.

This makes review easier because maintainers can see the model-card/runtime
metadata and the `.json.xz` result payloads together.

## 8. Submit `.json.xz` Files To The Results Repository

Submit one model result directory per PR when possible. The canonical path in
the private Hugging Face dataset repository is:

```text
hakari-results/{model_dir}/{dataset_id_or_name}/{task}.json.xz
```

Recommended submission path: create a clean staging directory that contains
only the intended `.json.xz` files, then use the Hugging Face Hub CLI to create
the Dataset PR and attach the result commit in one operation.

```bash
MODEL_DIR=MODEL_ID_WITH_DOUBLE_UNDERSCORE
STAGING_ROOT=tmp/hf-results-${MODEL_DIR}

rm -rf "${STAGING_ROOT}"
mkdir -p "${STAGING_ROOT}/hakari-results/${MODEL_DIR}"
rsync -a \
  --include='*/' \
  --include='*.json.xz' \
  --exclude='*' \
  "output/hakari-results/${MODEL_DIR}/" \
  "${STAGING_ROOT}/hakari-results/${MODEL_DIR}/"

find "${STAGING_ROOT}/hakari-results" -type f ! -name '*.json.xz' -print
find "${STAGING_ROOT}/hakari-results" \
  \( -name '*.duckdb' -o -name '*.duckdb.wal' \) \
  -print
find "${STAGING_ROOT}/hakari-results" -type f -name '*.json.xz' | wc -l

PR_BODY="$(cat tmp/${MODEL_DIR}_results_pr.md)"
uv run hf upload hakari-bench/results \
  "${STAGING_ROOT}/hakari-results" \
  hakari-results \
  --repo-type dataset \
  --create-pr \
  --commit-message "Add results for MODEL_ID" \
  --commit-description "$PR_BODY"
```

The first two `find` commands should print nothing. For related multi-model
submissions, repeat the `rsync` step for each model under the same staging root
and use one combined PR body.

If `hf upload --create-pr` fails because of permissions, Hub-side errors, or
large-folder upload limits, use the manual Dataset PR ref fallback in
[`contributing_results.md`](contributing_results.md#fallback-manual-dataset-pr-ref-workflow).
Hugging Face Dataset PRs are backed by `refs/pr/N` refs; the CLI helper creates
and updates that ref for the recommended path.

If a related GitHub code PR exists, paste that GitHub PR URL into the Hugging
Face Dataset PR body. After the Hugging Face PR exists, add its URL back to the
GitHub PR body or a GitHub PR comment.

After upload, confirm the PR diff contains only intended `.json.xz` files:

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

The `grep -v` command should print nothing.

## Final Checklist

- Model research is complete and reflected in the run plan.
- Model card is generated, reviewed, and updated in the code repository when
  needed.
- Dense truncate dimensions are documented in `embedding.truncate_dims` and
  passed as `--embedding-variant truncate:...`, or explicitly set to `null` /
  omitted when unsupported.
- Full evaluation wrote compressed `.json.xz` task files.
- Coverage and variant completeness were audited after DuckDB build or append.
- PR body was generated and all TODOs were filled.
- GitHub code PR exists for model cards, docs, loaders, viewer/schema changes,
  or other repository changes when needed.
- GitHub and Hugging Face PRs link to each other when both exist.
- Hugging Face result commits were created by `hf upload --create-pr`, or were
  attached manually to the Dataset PR ref when the CLI helper failed.
- Result PR contains only the intended `.json.xz` files under
  `hakari-results/{model_dir}/`.
