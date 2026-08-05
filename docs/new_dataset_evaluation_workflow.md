# New Dataset Evaluation Workflow

This document defines the maintainer workflow for evaluating an existing model
fleet on a newly added HAKARI-Bench dataset. The central rule is that a new
dataset run is accepted only after the evaluator can reproduce an existing task
with nearly unchanged scores in the same software and hardware environment.
Apply the gate independently to retrieval models and rerankers; success for one
method does not validate another method.

Use this workflow after the dataset itself, its fixed candidate subsets, and its
built-in YAML definition have been reviewed. Dataset construction belongs in
[`create_nano_datasets.md`](create_nano_datasets.md), model settings belong in
[`evaluation_policy.md`](evaluation_policy.md), and result submission belongs in
[`contributing_results.md`](contributing_results.md).

## Why Reproduce An Existing Task First

A stored leaderboard score depends on more than model weights. Transformers,
Sentence Transformers, PyTorch, CUDA kernels, dtype, attention implementation,
prompts, sequence length, candidate ranking, and even a model revision can
change the result. Running the new dataset immediately can therefore produce a
complete but incomparable result wave.

An existing-task reproduction run is a control measurement. It demonstrates
that the current evaluator and runtime still implement the protocol represented
by the existing result. It must use the same model method and all score-affecting
settings intended for the new dataset run.

## Required Progress Record

Create an ignored checklist before starting, for example:

```text
tmp/NanoSSRB-evaluation.md
```

Record the following for every model or logical model variant:

- model ID and resolved revision;
- method: dense, sparse, late-interaction, or reranker;
- reference result source and reference task;
- command and output directory;
- GPU model and device count, CUDA, PyTorch, Transformers, Sentence
  Transformers, and method-specific package versions;
- dtype, attention implementation, prompts, sequence lengths, batch size, and
  embedding variants;
- candidate subset, candidate depth, and dataset revision for rerank runs;
- old score, reproduced score, absolute difference, retry history, and final
  decision;
- new-dataset task coverage and any exceptions.

Do not rely on terminal history as the audit record. Keep secrets and API keys
out of the memo.

## 1. Freeze The Evaluation Inputs

Before using GPU time:

1. Verify the dataset YAML, task names, qrels, corpus and query configs, and
   candidate subsets.
2. Pin or record the resolved dataset revision. Do not compare runs that loaded
   different mutable dataset revisions without explicitly investigating the
   dataset diff.
3. Select the existing result population from the latest remote DuckDB cache.
   Use raw `.json.xz` only when run metadata needed for reproduction is not
   available in DuckDB.
4. Recover each model's original score-affecting settings from result metadata,
   its reviewed model card, and model-specific benchmarking notes. Do not assume
   that the current library defaults match an older run.
5. Use the same output format and normal result path expected by the Hugging
   Face results repository.

Capture the environment before and after a long wave. At minimum retain the
output of `nvidia-smi`, `uv run python --version`, and the relevant package
versions. Reuse the original hardware topology when practical. In particular,
do not validate on one GPU and silently change to a multi-GPU scoring path for
the accepted run; device count and parallel scoring can change numerical or
tie-breaking behavior and must be validated separately.

## 2. Choose Reference Tasks

Choose at least one existing task with a stored result for each model and
method. The reference should be small enough to rerun cheaply but representative
of the intended code path.

- For English retrieval models, one `NanoBEIR-en` task is the usual first
  control. `NanoMIRACL-en` is a useful second control when a discrepancy might
  be dataset-specific or when multilingual behavior matters.
- For a language-specialized model, add a reference task in a supported
  language when available. An English-only control is insufficient to validate
  language-specific prompts or tokenization.
- For sparse and late-interaction models, use a stored result produced by that
  same method. A dense result does not exercise sparse pruning or MaxSim.
- For rerankers, use an existing reranking result with the same candidate subset
  and candidate depth. A full-corpus retrieval score cannot validate a
  CrossEncoder reranking path.
- For hosted or batch providers, reproduce a task through the same direct or
  batch materialization path intended for the new run, including the same
  tokenizer-based input truncation policy.

One task is the minimum gate, not proof that every dataset interaction is
equivalent. Add a second reference whenever the first result differs, the new
suite exercises unusual input structure or length, or the old result is known
to be sensitive to package versions.

## 3. Reproduce The Existing Result

Run the reference task with the exact planned runtime. A dense example is:

```bash
CUDA_VISIBLE_DEVICES=0 uv run --group tf4-fa2 hakari-bench evaluate dense \
  --model MODEL_ID \
  --dataset NanoBEIR-en \
  --split REFERENCE_TASK \
  --model-revision MODEL_REVISION \
  --dataset-revision DATASET_REVISION \
  --dtype bf16 \
  --attn-implementation sdpa
```

A reranker control must preserve the candidate protocol:

```bash
CUDA_VISIBLE_DEVICES=0 uv run --group tf4-fa2 hakari-bench evaluate reranker \
  --model RERANKER_ID \
  --dataset NanoBEIR-en \
  --split REFERENCE_TASK \
  --model-revision MODEL_REVISION \
  --dataset-revision DATASET_REVISION \
  --candidate-ranking reranking_hybrid \
  --dtype bf16 \
  --attn-implementation sdpa
```

These are templates, not universal settings. Restore the original prompt,
attention, dtype, sequence length, trust-remote-code, embedding variants,
sparse limits, late-interaction settings, and reranker inference options for
the particular result being reproduced. Prefer `evaluate from-model-card` when
the reviewed card fully describes the model settings.

Compare like with like: the same task, target, metric, model revision, base or
embedding variant, and candidate protocol. For scores represented on a 0-to-1
scale, use the following default decision bands unless a stricter established
model-specific tolerance exists:

- absolute difference at most `0.005`: reproduced;
- difference above `0.005` and at most `0.01`: repeat and investigate before
  acceptance;
- difference above `0.01`: not reproduced unless a documented, reviewed cause
  is corrected and a subsequent run passes.

Do not average away a large task-level difference. Also inspect whether the
difference changes model ordering or contradicts known nearby models. Exact
equality is not required for ordinary floating-point kernel drift, but a result
must not be accepted merely because both values look plausible in isolation.

## 4. Investigate A Failed Reproduction

When the control misses the tolerance, do not start the new-dataset wave for
that model. Work through the likely causes while keeping one variable change per
retry:

1. confirm model and dataset revisions;
2. confirm prompts, prompt names, prefixes, pooling, normalization, and
   sequence lengths;
3. confirm dtype, attention implementation, device count, and batch/inference
   kwargs;
4. reproduce the recorded Transformers, Sentence Transformers, PyTorch, PyLate,
   or other backend versions in an isolated `uv` environment;
5. for rerankers, confirm candidate subset revision, candidate depth,
   deterministic shuffle behavior, and score function;
6. run a second existing reference task to distinguish task-specific drift from
   a model-wide mismatch;
7. inspect the saved top-ranking artifact when score differences remain
   unexplained.

Try supported package-version combinations and documented backends when there
is evidence that the historical result used them. Do not repeatedly tune the
runtime against the reference score or choose a configuration solely because it
matches one number.

If the model still cannot reproduce, mark it as **not reproduced**, record the
best observed difference and attempted environments, and skip it for the new
dataset. Never substitute a fresh incomparable score under the existing logical
model identity.

## 5. Evaluate The New Dataset

After a model passes its method-specific control, run the new dataset without
changing the validated environment or score-affecting settings. NanoSSRB is an
explicit-only diagnostic suite, so it requires the extended evaluation scope:

```bash
CUDA_VISIBLE_DEVICES=0 uv run --group tf4-fa2 hakari-bench evaluate dense \
  --model MODEL_ID \
  --dataset NanoSSRB \
  --evaluation-scope all \
  --dtype bf16 \
  --attn-implementation sdpa
```

For rerankers:

```bash
CUDA_VISIBLE_DEVICES=0 uv run --group tf4-fa2 hakari-bench evaluate reranker \
  --model RERANKER_ID \
  --dataset NanoSSRB \
  --evaluation-scope all \
  --candidate-ranking reranking_hybrid \
  --dtype bf16 \
  --attn-implementation sdpa
```

Use each model's validated settings rather than copying the example settings to
the entire fleet. Preserve automatic dense variants and documented truncation
dimensions unless the accepted historical result intentionally used a
different variant plan. Existing outputs are resumable; use `--overwrite` only
when intentionally replacing an invalid run.

## 6. Validate New-Dataset Results

Before accepting the wave:

1. confirm that every passed model has one base result for every new task;
2. audit all expected dense, sparse, reranking, or late-interaction variants;
3. verify that result JSON records the validated runtime, resolved revisions,
   candidate metadata, package versions, and top-ranking artifacts;
4. compare model ordering and score ranges with the existing leaderboard and
   with models of similar capability;
5. when a full-size parent benchmark or official leaderboard exists, match
   shared models and measure rank correlation between the full and Nano suites,
   as was done for NanoMTEB-BR;
6. investigate outliers rather than deleting them solely for being surprising;
7. keep failed-reproduction models out of the submitted new-dataset set and
   list them explicitly in the progress memo and review summary.

A plausible cross-model trend is supporting evidence, not a replacement for
the existing-task reproduction gate.

## 7. Prepare Results For Review

Keep accepted per-task files in the standard layout:

```text
output/hakari-results/{model_id}/{huggingface_dataset_name}/{task}.json.xz
```

Build or append a DuckDB and perform the coverage audit described in
[`evaluation_runbook.md`](evaluation_runbook.md). Prepare the Hugging Face
results pull request using [`contributing_results.md`](contributing_results.md).
The review summary must state:

- the reference tasks and acceptance tolerance;
- the environment and revisions used;
- reproduction differences for each model or a linked audit table;
- complete new-dataset task and variant counts;
- reranker candidate protocol;
- every skipped model and why it could not be reproduced.

Do not describe a wave as equivalent to existing leaderboard results if the
control runs used materially different settings or failed the stated tolerance.
