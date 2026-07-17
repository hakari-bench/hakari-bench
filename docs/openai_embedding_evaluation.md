# OpenAI Embedding Evaluation

This document explains how to evaluate OpenAI embedding models in HAKARI-Bench through the dense evaluator and the built-in `openai` model loader. It covers optional dependency setup, `.env` and `OPENAI_API_KEY`, model names, API-provided dimensions versus local truncation, the `dimensions` parameter, token limits, asynchronous concurrency, rate-limit and retry considerations, and when to use normal direct evaluation versus batch inference. Coding agents should use this file when searching for OpenAI embeddings, hosted dense evaluation, `text-embedding-3-small`, `text-embedding-3-large`, API dimension settings, local embedding variants, token budgeting, async concurrency, or OpenAI Batch API links.

HAKARI-Bench can evaluate OpenAI embedding models through the dense evaluator
using the built-in `openai` model loader.

## Setup

Install the optional OpenAI dependency group and keep the API key in `.env`:

```bash
uv sync --group openai
cp .env.sample .env
```

`.env` must contain:

```dotenv
OPENAI_API_KEY=...
```

Run evaluations with `uv run --group openai`:

```bash
uv run --group openai hakari-bench evaluate dense \
  --model text-embedding-3-small \
  --model-loader openai \
  --dataset hakari-bench/NanoBEIR-en \
  --split arguana
```

The model cards under `config/model_cards/openai__*.yaml` can also be used:

```bash
uv run --group openai hakari-bench evaluate from-model-card \
  --model-card config/model_cards/openai__text-embedding-3-small.yaml \
  --dataset hakari-bench/NanoBEIR-en \
  --split arguana
```

## Dimensions

OpenAI `text-embedding-3` models support the API `dimensions` parameter. In
HAKARI-Bench, the built-in OpenAI loader does not send `dimensions` to the API
for benchmark truncation. It requests the full embedding, then applies
`full[:DIM]` followed by L2 normalization after each embedding batch:

```bash
uv run --group openai hakari-bench evaluate dense \
  --model text-embedding-3-large \
  --model-loader openai \
  --truncate-dim 1024 \
  --dataset hakari-bench/NanoBEIR-en \
  --split arguana
```

`--truncate-dim DIM` and OpenAI `--embedding-variant truncate:DIM` therefore use
the same local normalized-prefix policy in this repository. This differs
slightly from pure API-side `dimensions=DIM`, but it makes benchmark truncation
variants reusable from one full-dimension embedding pass. The OpenAI docs also
state that manually shortened embeddings should be normalized before similarity
search.

## API Dimensions vs Local Truncation

The helper below verifies whether API `dimensions` matches a local slice of the
full embedding:

```bash
uv run --group openai python scripts/check_openai_embedding_dimensions.py \
  --model text-embedding-3-small \
  --dimensions 256
```

Observed on 2026-06-18:

```text
text-embedding-3-small, dimensions=256
max_abs_diff_api_vs_full_prefix=0.1070556640625
max_abs_diff_api_vs_renormalized_full_prefix=0.0001058551483564818

text-embedding-3-large, dimensions=256
max_abs_diff_api_vs_full_prefix=0.1278076171875
max_abs_diff_api_vs_renormalized_full_prefix=0.00012887422474436305
```

So API-reduced embeddings are not bit-identical to taking the first `DIM`
values from the full vector. They are close to a normalized prefix, but still
not exactly identical at the returned float precision. HAKARI's OpenAI
benchmark path intentionally uses the normalized-prefix approximation rather
than issuing separate API-dimension requests for every truncation condition.

Additional `text-embedding-3-large` checks on 2026-06-18:

| dimensions | max abs diff vs raw prefix | max abs diff vs normalized prefix | mean abs diff vs normalized prefix |
| --- | ---: | ---: | ---: |
| 256 | 0.1278076171875 | 0.00012887422474436305 | 0.000023273817264747148 |
| 512 | 0.0655517578125 | 0.00017244662019255674 | 0.00003472546175013237 |
| 1024 | 0.03057861328125 | 0.00006523312784288693 | 0.000008866960548196837 |
| 1536 | 0.0162353515625 | 0.00010104677316384592 | 0.000020146251587336494 |

## Token Limits

OpenAI embedding inputs are limited to 8192 tokens per input and 300,000 tokens
summed across all inputs in one request. The built-in loader uses `tiktoken` to
truncate each input to 8100 tokens by default, leaving headroom below the API
limit because server-side accounting can differ slightly from local counting.

To fail instead of truncating over-limit inputs:

```bash
uv run --group openai hakari-bench evaluate dense \
  --model text-embedding-3-small \
  --model-loader openai \
  --model-loader-kwargs-json '{"truncate_input_tokens":false}'
```

The loader also splits batches so that a request stays under the OpenAI
per-request token budget. Its default request budget is 290,000 counted tokens,
leaving headroom below the API's 300,000-token hard limit.

## Async Concurrency

The OpenAI loader uses `AsyncOpenAI` internally while keeping the public dense
model `encode()` method synchronous for evaluator compatibility. `batch_size`
controls the number of texts per embeddings request. `max_concurrency` controls
the maximum number of in-flight embeddings requests.

```bash
uv run --group openai hakari-bench evaluate dense \
  --model text-embedding-3-small \
  --model-loader openai \
  --batch-size 512 \
  --model-loader-kwargs-json '{"max_concurrency":8}'
```

Keep concurrency conservative when running large Nano-set evaluations so API
rate limits and retry behavior remain predictable.

## Batch API

The synchronous evaluator calls `/v1/embeddings` directly. For full benchmark
runs, the OpenAI Batch API can reduce cost, but it is an offline workflow with
JSONL input files, a 24-hour completion window, and separate batch limits.
HAKARI's batch command workflow is documented in
[`batch_inference.md`](batch_inference.md):

```bash
uv run --group openai hakari-bench batch dense register \
  --target openai-small-nanobeir-en \
  --provider openai \
  --model text-embedding-3-small \
  --dataset hakari-bench/NanoBEIR-en

uv run --group openai hakari-bench batch dense process \
  --target openai-small-nanobeir-en \
  --results-dir output/openai-batch \
  --embedding-variant truncate:256,512,1024
```

Use the cost estimator first:

```bash
uv run --group openai python scripts/estimate_openai_embedding_nanoset_costs.py
```

Batch API pricing is not implemented in the direct dense evaluator itself.
