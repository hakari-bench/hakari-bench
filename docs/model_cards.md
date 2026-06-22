# Model Cards

This document defines the static HAKARI-Bench model card schema stored under `config/model_cards/` and explains how model cards drive reproducible evaluation. It covers filename conventions, top-level YAML fields, source revisions, method type, runtime options, dtype, attention implementation, trust-remote-code approval, prompts, embedding truncation dimensions, sparse and late-interaction fields, language support, target coverage, generation scripts, auditing, and synchronization with result metadata. Coding agents should use this file when searching for model card schema, `generate_model_cards.py`, reviewed runtime metadata, prompt configuration, model revisions, truncate dims, language display, or model metadata validation.

Model cards are static HAKARI metadata files stored under
`config/model_cards/`. Store one model per YAML file and replace `/` in the
model id with `__` in the filename, for example:

```text
config/model_cards/BAAI__bge-m3.yaml
```

The implementation lives in `hakari_bench/model_cards.py`, and the CLI entry
point is `scripts/generate_model_cards.py`. Keep this document, those Python
files, and the real YAML files under `config/model_cards/` synchronized when the
schema or generation policy changes.

## Schema

Model cards are YAML mappings. The common top-level fields are:

| Field | Required | Purpose |
| --- | --- | --- |
| `id` | yes | Canonical model id, usually the Hugging Face id. It is also the viewer lookup key. |
| `source` | yes | Model source metadata. Use `type: huggingface`, `name`, optional pinned `revision`, and optional `revision_requested`. |
| `method` | yes | One of `dense`, `sparse`, `reranker`, `late-interaction`, or `bm25`. |
| `license` | yes for static cards | Display and compliance metadata for the model or baseline. |
| `links` | recommended | Canonical model, repository, and paper links shown in the Model Details dialog. |
| `parameters` | recommended | Parameter counts: `total`, `trainable`, `input_embedding`, and `active`. |
| `embedding` | method-specific | Dense embedding metadata, including `truncate_dims` and optional output/normalization details. |
| `runtime` | recommended | Model loading defaults such as sequence length, dtype, attention implementation, backend, and trust-remote-code review state. |
| `prompts` | optional | Prompt names or prompt text required for correct model use. |
| `late_interaction` | late-interaction only | ColBERT/PyLate architecture and query/document token settings. |
| `language_support` | recommended | Static display classification for intended language coverage. |
| `target` | optional | Datasets, collections, splits, and scope the card was prepared for. |
| `notes` | optional | Reviewed operational notes that do not fit structured fields. |

`parameters.active` is the count used for size-aware leaderboard display when
available. For transformer embedding models, it is usually total parameters
minus input embedding parameters. Keep overrides in the card when automatic
metadata collection cannot recover the correct value.

Dense `embedding` fields may include:

- `truncate_dims`: every reviewed truncation dimension that should be evaluated,
  or `null` when truncation is not supported. Do not include the model's native
  output dimension; it duplicates the base result rather than creating a true
  truncation variant.
- `output_dimension`: the native embedding dimension.
- `user_defined_output_dimensions`: the supported dynamic output-dimension
  range, when the model officially exposes one.
- `mrl_support`: whether the model is intended to support Matryoshka/prefix
  truncation.
- `pooling`, `normalize`, and `include_prompt`: official embedding behavior
  needed to interpret the score and reproduce evaluation.

`runtime.trust_remote_code: true` is executable-code metadata, not a display
decoration. Static cards that set it must also set
`runtime.remote_code_approved: true` and pin `source.revision` to the reviewed
40-character Hugging Face commit SHA.

Generate a card by loading a model:

```bash
uv run python scripts/generate_model_cards.py \
  --model BAAI/bge-m3 \
  --model-type dense \
  --truncate-dims none \
  --dataset hakari-bench/NanoBEIR-en \
  --output-dir config/model_cards
```

For dense models, `--truncate-dims` is required. Use numeric dimensions such as
`--truncate-dims 768`, or use `--truncate-dims none` when the model should not be
treated as truncation-compatible. Most metadata is inferred from the loaded
model. Use override arguments such as `--active-parameters`,
`--input-embedding-parameters`, `--source-revision`, or `--max-seq-length` when
automatic detection is wrong.

For Matryoshka models, include every model-supported truncation dimension below
the native output dimension. For example,
`hotchpotch/bekko-embedding-v1-a8m` has 384-dimensional base embeddings and
should be generated with:

```bash
uv run --group tf4-fa2 python scripts/generate_model_cards.py \
  --model hotchpotch/bekko-embedding-v1-a8m \
  --model-type dense \
  --truncate-dims 64 128 256 \
  --flash-attn2 \
  --output-dir config/model_cards
```

Evaluate directly from a card:

```bash
uv run hakari-bench evaluate from-model-card \
  --model-card config/model_cards/BAAI__bge-m3.yaml \
  --batch-size 32
```

The `from-model-card` evaluator reads `method`, `source`, `runtime`, `prompts`,
`embedding.truncate_dims`, `late_interaction`, and `target` from the YAML, then
runs the normal `dense`, `sparse`, `reranker`, or `late-interaction` evaluation
path. Runtime options such as batch size, device, candidate ranking, rerank
depth, and output directory can still be supplied on the command line.

Use `from-model-card` for repeated evaluations once a card has been reviewed.
The card should hold the model-specific choices that otherwise have to be typed
on every run: Sentence Transformers prompt names, explicit query/document
prompt text, encode tasks, supported truncate dimensions, dtype, attention
implementation, max sequence length, trust-remote-code approval, and
late-interaction prefixes or token lengths. Command-line values still take
precedence for one-off experiments.

Only model-specific optimization options belong in a model card. For example,
prompt names, retrieval prefixes, model sequence length, dtype, attention
implementation, and ColBERT query/document token lengths are model options.
Candidate-ranking choices and reranking top-K/depth settings are benchmark
protocol options, not model options, and should not be stored as model-card
defaults.

Model cards should include a top-level `license` section. Use the model's
Hugging Face model-card metadata as the first source. If the license cannot be
confirmed, set the license to `unknown` rather than guessing.

```yaml
license:
  id: apache-2.0
  label: Apache 2.0
  type: permissive
  commercial_use: allowed
  source: huggingface_model_card
  source_url: https://huggingface.co/BAAI/bge-reranker-v2-m3
```

Use clear labels such as `MIT`, `Apache 2.0`, `CC BY-NC 4.0`, or `Gemma Terms
of Use`. Set `commercial_use` to `allowed` for permissive licenses,
`not_allowed` for non-commercial Creative Commons licenses, and
`permitted_with_terms` for proprietary terms that permit commercial use only
under model-specific conditions. BM25 is an algorithmic baseline rather than a
licensed model, so its card uses `id: not_applicable`, `type: algorithm`, and
the label `Not applicable - Okapi BM25 algorithmic baseline`.

Model cards may include an optional `links` section that records canonical
reference URLs for the model. All fields are optional, but including them is
encouraged. Use a single `huggingface` URL, a single `github` URL, and a
`papers` list where every paper pairs a `title` with a `url`:

```yaml
links:
  huggingface: https://huggingface.co/BAAI/bge-m3
  github: https://github.com/FlagOpen/FlagEmbedding
  papers:
  - title: "BGE M3-Embedding: Multi-Lingual, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation"
    url: https://arxiv.org/abs/2402.03216
```

Record the model's main Hugging Face page, its main GitHub repository, and one
or more papers. Omit any field that is unknown rather than guessing. The
leaderboard viewer renders these as clickable links in the Model Details dialog.

Prompt settings use the optional `prompts` section:

```yaml
prompts:
  query_prompt_name: query
  document_prompt_name: document
```

Prefer Sentence Transformers prompt names when the model stores reviewed
retrieval prompts in its config. Use explicit `query_prompt` and
`document_prompt` only when the prompt registry is absent, incomplete, or would
not be loaded by the selected backend. Do not set both prompt names and explicit
prompt text for the same side unless a backend-specific experiment requires it.

Late-interaction model cards may also include a `late_interaction` section for
ColBERT-style model settings that should be used by `from-model-card` evaluation
and shown in the leaderboard viewer, for example:

```yaml
late_interaction:
  architecture: colbert
  scoring: maxsim
  query_prefix: "[Q] "
  document_prefix: "[D] "
  query_length: 48
  document_length: 512
  do_query_expansion: false
  attend_to_expansion_tokens: false
```

The evaluator applies `query_prefix`, `document_prefix`, `query_length`,
`document_length`, `do_query_expansion`, and `attend_to_expansion_tokens` from
this section. For fields that also have command-line options, explicit command
line values take precedence. The viewer also uses this section to populate Model
Details when older DuckDB builds do not carry these runtime fields directly.

Model cards may include a `language_support` section for static leaderboard
display metadata. This section is descriptive and is not used as an evaluation
option. Language support labels should prefer the model's intended language
identity over weak cross-lingual transfer observed in evaluation scores. Use
NanoMIRACL and MNanoBEIR language scores as evidence, but do not expand an
English-only model into many languages solely because it has non-English
transfer scores.

```yaml
language_support:
  category: multilingual
  evidence:
    benchmarks:
    - NanoMIRACL
    - MNanoBEIR
    score_target: all
    classification_policy: model identity first; use broad score evidence only for models without explicit language identity
    classification_reason: model_identity_multilingual_or_bilingual
    english_score: 0.62
    non_english_mean_score: 0.702
    high_non_english_score_threshold: 0.6
    high_non_english_language_count: 8
    high_non_english_family_count: 5
    evaluated_language_count: 20
```

Allowed categories are:

| Category | Viewer label | Use when |
| --- | --- | --- |
| `multilingual` | `Multilingual` | The model identity, official card, paper, or broad language-score evidence indicates multilingual or cross-lingual intent. Omit `languages`. |
| `english_only` | `English only` | The model identity or training/evaluation intent is English-only. Include `languages: [en]`, even when weak transfer scores exist. |
| `english_plus` | language list such as `ja, en` | The model has explicit limited-language intent, such as Japanese plus English. Include the reviewed list in `languages`. |

The `evidence` mapping records why the classification was chosen:

- `benchmarks`: currently `NanoMIRACL` and `MNanoBEIR` for score evidence.
- `score_target`: usually `all`, matching retrieval mode in the result DB.
- `classification_policy`: the fixed policy string used by tests and the
  generator.
- `classification_reason`: concise reason such as
  `model_identity_multilingual_or_bilingual`, `model_identity_english_only`,
  `model_identity_japanese_or_ruri`, or `broad_multilingual_score_evidence`.
- `english_score`, `non_english_mean_score`, `high_non_english_*`, and
  `evaluated_language_count`: score-derived support values when available.
- `official_supported_languages`: optional language-code list copied from an
  official model card or paper. This lives under `evidence` so `multilingual`
  cards can preserve the official list while still omitting top-level
  `languages` for viewer display.

Use `english_only` for models that appear English-only by name, model family, or
known benchmark intent even if they show weak non-English transfer. Use
`english_plus` for explicit limited-language cases such as Japanese-focused
models, where current cards use `languages: [ja, en]`. Use `multilingual` for
models whose name or family explicitly says multilingual or bilingual, and for
models with broad multilingual score evidence. Multilingual cards intentionally
omit `languages`; explicit language lists are only used for limited-language
cards such as `english_only` and `english_plus`.

The leaderboard viewer shows this metadata at the top of the clicked Model
Details dialog, before the model type. `multilingual` renders as
`Multilingual`, `english_only` renders as `English only`, and `english_plus`
renders the configured language list such as `ja, en`. Set
`language_support.marker` only when another display surface needs a short label
without changing the classification, for example:

```yaml
language_support:
  category: english_plus
  languages:
  - ja
  - en
  marker: JP
```

The Model Details title links to the model page when a Hugging Face-style model
identifier is available.

If a card sets `runtime.trust_remote_code: true`, the card must also include
`runtime.remote_code_approved: true` and `source.revision` must be the full
40-character Hugging Face commit SHA that was reviewed. Short revisions,
branches, and tags are intentionally rejected for model-card execution because
`trust_remote_code` allows arbitrary Python code from the model repository to
run during loading.

When generating a reviewed remote-code card, pass both flags and pin the full
revision:

```bash
uv run python scripts/generate_model_cards.py \
  --model jinaai/jina-embeddings-v3 \
  --model-type dense \
  --truncate-dims 32 64 128 256 512 768 \
  --trust-remote-code \
  --remote-code-approved \
  --model-revision ab036b023d30b4d1138c4c3bfa9f0c445ab455d6 \
  --output-dir config/model_cards
```

Every non-BM25 evaluation also writes a reusable model card next to the result
tree:

```text
output/hakari-results/{safe_model_id}/{safe_model_id}.yaml
```

This file can be copied into `config/model_cards/` after review.

Generate cards from existing benchmark result JSON. The generator reads the
default `.json.xz` task files and legacy or explicitly plain `.json` files:

```bash
uv run python scripts/generate_model_cards.py \
  --from-results output/hakari-results \
  --output-dir config/model_cards \
  --infer-language-support \
  --overwrite
```

The result-based mode is intended for bootstrapping the current leaderboard
models. It skips `bm25` and model ids containing `bekko` by default, infers
truncate dimensions from recorded embedding variants, infers stable prompt and
late-interaction settings from result `config` payloads, and preserves reviewed
fields such as `prompts`, `late_interaction`, `language_support`, and `notes`
from existing cards.

`--infer-language-support` reads finished result JSON and proposes
`language_support` only when the existing card does not already define it. It
uses NanoBEIR language-slice results such as `NanoBEIR-en` and NanoMIRACL task
languages, computes per-language mean scores, and writes a conservative
classification. The generated value is an initial review aid; update it manually
when the model card, paper, or model family gives a clearer language identity
than the score-only heuristic.
