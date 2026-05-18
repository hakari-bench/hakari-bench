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

The `from-model-card` evaluator reads `method`, `source`, `runtime`,
`embedding.truncate_dims`, and `target` from the YAML, then runs the normal
`dense`, `sparse`, `reranker`, or `late-interaction` evaluation path. Runtime
options such as batch size, device, prompt options, candidate ranking, and output
directory can still be supplied on the command line.

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
