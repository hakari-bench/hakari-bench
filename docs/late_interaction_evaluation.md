# Late-Interaction Evaluation Plan

This document records the current HAKARI-Bench policy for broad ColBERT-style
late-interaction reevaluation runs. It complements
[`docs/benchmark_evaluation.md`](benchmark_evaluation.md), which remains the
canonical entry point for benchmark execution.

## Scope

Use this plan when reevaluating ColBERT-compatible models with
`hakari-bench evaluate late-interaction` across Nano retrieval datasets. The
current target set is:

- `answerdotai/answerai-colbert-small-v1`
- `colbert-ir/colbertv2.0`
- `lightonai/ColBERT-Zero`
- `lightonai/GTE-ModernColBERT-v1`
- `mixedbread-ai/mxbai-edge-colbert-v0-17m`
- `mixedbread-ai/mxbai-edge-colbert-v0-32m`
- `NeuML/colbert-muvera-micro`

## Standard Run Parameters

For broad Nano-set reevaluation, use a shared token budget:

- query length: `48`
- document length: `512`
- scoring: exact MaxSim
- BM25 candidate reranking: keep the standard top-100 reranking diagnostics
- runtime: `uv run --group pylate`
- attention: use explicit `--attn-implementation sdpa` unless a model-specific
  note requires a different verified runtime

Example:

```bash
uv run --group pylate hakari-bench evaluate late-interaction \
  --model MODEL_ID \
  --dataset DATASET_NAME \
  --batch-size 64 \
  --dtype bf16 \
  --device cuda:0 \
  --attn-implementation sdpa \
  --late-interaction-query-length 48 \
  --late-interaction-document-length 512 \
  --late-interaction-exact-doc-batch-size 128 \
  --late-interaction-exact-query-batch-size 8
```

Add either `--late-interaction-do-query-expansion` or
`--no-late-interaction-do-query-expansion` according to the model table below.
Do not rely on the PyLate API default for query expansion.

## Query Expansion Policy

HAKARI-Bench defaults ColBERT query expansion to disabled unless the model config
or CLI explicitly enables it. PyLate's API default may enable query expansion,
but benchmark runs should make the choice explicit so that result JSON is
auditable.

The broad reevaluation policy is:

| Model | Query expansion | Basis |
| --- | --- | --- |
| `answerdotai/answerai-colbert-small-v1` | `true` | No explicit model config flag was found, but small-sample NanoMIRACL-en and NanoMTEB-v2 comparisons favored query expansion. The model appears aligned with the original ColBERT training style where query expansion is expected. |
| `colbert-ir/colbertv2.0` | `true` | The original ColBERT/ColBERTv2 evaluation practice uses query augmentation/expansion, and NanoMIRACL-en comparison favored query expansion. |
| `lightonai/ColBERT-Zero` | `false` | Small-sample NanoMIRACL-en comparison favored disabled query expansion with the model's prompt-aligned settings. |
| `lightonai/GTE-ModernColBERT-v1` | `false` | Small-sample NanoMIRACL-en comparison favored disabled query expansion. |
| `mixedbread-ai/mxbai-edge-colbert-v0-17m` | `false` | The model config uses `48`/`512` and disabled query expansion; NanoMIRACL-en comparison strongly favored disabled query expansion. |
| `mixedbread-ai/mxbai-edge-colbert-v0-32m` | `false` | The model config uses `48`/`512` and disabled query expansion; NanoMIRACL-en comparison favored disabled query expansion. |
| `NeuML/colbert-muvera-micro` | `true` | The model config sets query expansion to enabled, and NanoMIRACL-en comparison favored enabled query expansion. |

These choices should be treated as the current broad-run defaults. If a later
model card or config clearly contradicts this table, update this document before
starting another full run.

## Why 48 / 512

Many ColBERT models publish shorter native settings such as `32` query tokens
and `180` or `300` document tokens. Those settings are useful model-native
variants, but they make full cross-model Nano reevaluation expensive because
each model can require repeated sweeps over length and expansion choices.

For the current broad reevaluation, HAKARI-Bench standardizes on `48` query
tokens and `512` document tokens. This is intentionally conservative for Nano
retrieval sets:

- Nano datasets include long queries and long documents often enough that very
  short token budgets can truncate useful evidence.
- A single shared `48`/`512` plan avoids repeatedly rerunning heavy
  late-interaction inference just to retune sequence lengths per model.
- The setting matches the Mixedbread ColBERT model configs and is a reasonable
  upper default for other BERT-style ColBERT models in this benchmark.
- Exact MaxSim scoring cost still scales with query and document token counts,
  so this should be used as the broad-run default rather than expanded further
  without a specific reason.

If model-native lengths are needed for a report, run them as explicit variants
or debug comparisons and label them separately from the broad `48`/`512` run.

## Result Metadata

The resolved late-interaction settings are written to each result JSON under
`model.late_interaction`, for example:

```json
{
  "model": {
    "late_interaction": {
      "architecture": "colbert",
      "scoring": "maxsim",
      "query_length": 48,
      "document_length": 512,
      "do_query_expansion": true,
      "attend_to_expansion_tokens": false
    }
  }
}
```

Use `model.late_interaction` when auditing what actually ran. The
`config.late_interaction` object records CLI-level requested values and exact
batch sizes, but `model.late_interaction` is the resolved model/runtime
metadata.

## Command Fragments

Use these fragments with the standard command above:

```bash
# Query expansion enabled models.
--late-interaction-query-length 48 \
--late-interaction-document-length 512 \
--late-interaction-do-query-expansion
```

```bash
# Query expansion disabled models.
--late-interaction-query-length 48 \
--late-interaction-document-length 512 \
--no-late-interaction-do-query-expansion
```

Keep result roots separate while validating a new policy. After the policy is
accepted, use `--overwrite` only when intentionally replacing older results that
used a different query-expansion or sequence-length policy.
