# Model Cards

Model cards are static HAKARI metadata files stored under
`config/model_cards/`. Store one model per YAML file and replace `/` in the
model id with `__` in the filename, for example:

```text
config/model_cards/BAAI__bge-m3.yaml
```

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

Only model-specific optimization options belong in a model card. For example,
prompt names, retrieval prefixes, model sequence length, dtype, attention
implementation, and ColBERT query/document token lengths are model options.
Candidate-ranking choices and reranking top-K/depth settings are benchmark
protocol options, not model options, and should not be stored as model-card
defaults.

Prompt settings use the optional `prompts` section:

```yaml
prompts:
  query_prompt_name: query
  document_prompt_name: document
```

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
output/results/{safe_model_id}/{safe_model_id}.yaml
```

This file can be copied into `config/model_cards/` after review.

Generate cards from existing benchmark result JSON:

```bash
uv run python scripts/generate_model_cards.py \
  --from-results output/results \
  --output-dir config/model_cards \
  --overwrite
```

The result-based mode is intended for bootstrapping the current leaderboard
models. It skips `bm25` and model ids containing `bekko` by default, infers
truncate dimensions from recorded embedding variants, and preserves manual
top-level fields such as `notes` from existing cards.
