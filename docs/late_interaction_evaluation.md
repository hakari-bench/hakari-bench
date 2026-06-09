# Late-Interaction Evaluation

This document records the current repository workflow for ColBERT-style
late-interaction models. The canonical end-to-end benchmark procedure is
[`evaluation_policy.md`](evaluation_policy.md); model-specific prompts and
runtime choices are maintained in
[`model_specific_benchmarking_notes.md`](model_specific_benchmarking_notes.md)
and in the YAML cards under `config/model_cards/`.

## Current Rule

Use `evaluate from-model-card` for reviewed late-interaction models. The model
card is the source of truth for model optimization options:

- dtype and attention implementation
- Sentence Transformers prompt names when required by the checkpoint
- ColBERT query and document prefixes
- ColBERT query and document token lengths
- query expansion and expansion-token attention settings

Benchmark protocol settings are not model options. Keep candidate ranking,
reranking top-K, result directories, batch sizes, and GPU placement outside the
model card unless a command or experiment manifest explicitly needs them.

## Runtime

Run PyLate-backed models with the separated PyLate uv group:

```bash
UV_PROJECT_ENVIRONMENT=tmp/.venv_eval_pylate \
uv run --group pylate hakari-bench evaluate from-model-card \
  --model-card config/model_cards/lightonai__ColBERT-Zero.yaml \
  --dataset hakari-bench/NanoMedical \
  --split NanoNFCorpus \
  --candidate-ranking reranking_hybrid \
  --device cuda:0
```

For large parallel benchmark waves, use one uv environment per incompatible
dependency group. Do not mix `pylate`, `tf4-fa2`, and default groups in the same
`.venv` while jobs are running; uv may otherwise swap packages underneath active
processes. Batch size may be reduced for throughput or memory stability, but it
must not be treated as a score-changing model option.

## Reviewed ColBERT Cards

The reviewed cards currently include:

- `config/model_cards/lightonai__ColBERT-Zero.yaml`
- `config/model_cards/lightonai__GTE-ModernColBERT-v1.yaml`
- `config/model_cards/answerdotai__answerai-colbert-small-v1.yaml`
- `config/model_cards/colbert-ir__colbertv2.0.yaml`
- `config/model_cards/mixedbread-ai__mxbai-edge-colbert-v0-17m.yaml`
- `config/model_cards/mixedbread-ai__mxbai-edge-colbert-v0-32m.yaml`

Important current choices:

- `lightonai/ColBERT-Zero` requires `query_prompt_name: query` and
  `document_prompt_name: document`; omitting these prompt names causes a
  substantial score regression.
- `colbert-ir/colbertv2.0` uses `[unused0]` and `[unused1]` marker prefixes.
  The local fallback adapter inserts these marker token IDs immediately after
  CLS to match the Stanford ColBERT path.
- `mixedbread-ai/mxbai-edge-colbert-v0-17m` and `v0-32m` use `[Q] ` and
  `[D] ` prefixes, `query_length: 40`, `document_length: 512`, fp32, sdpa, and
  no query expansion.

See the ColBERT table in
[`model_specific_benchmarking_notes.md`](model_specific_benchmarking_notes.md#colbert-late-interaction-models)
for the full option matrix and rationale.

## Validation

After any late-interaction rerun:

1. Confirm every intended task JSON exists under the chosen results root.
2. Confirm each result JSON records the expected `model.late_interaction`,
   prompts, dtype, attention implementation, package versions, and candidate
   ranking metadata.
3. Compare both exact MaxSim `nDCG@10` and reranking-candidate `nDCG@10` against
   the previous run. Large single-model deltas should be reproduced in a
   separate output directory before overwriting shared result roots.
4. Keep the default compressed `.json.xz` result files for published result
   roots. Use `--result-format json` only for local diagnostics that require
   plain JSON.
