# TypeSafe Jev Reranker Evaluation

Use the built-in `typesafe` loader to evaluate Jev through
`POST https://api.typesafe.ai/v1/systemone`. It asks Noul relevance questions and
sorts candidates by the returned probability of yes. The existing `urllib3`
dependency handles HTTP; no TypeSafe SDK installation is needed.

## Commands

Set `TYPESAFE_API_KEY` in the environment or in the checkout's `.env`. Existing
environment values take precedence over `.env`. Do not put credentials in
loader kwargs or committed files.

These commands compare BM25 top-100 reranking on the repository's
`hakari-bench/NanoBEIR-en` NanoHotpotQA split:

```bash
uv run hakari-bench evaluate reranker \
  --model jev-1.13.0 \
  --model-loader typesafe \
  --typesafe-mode pointwise \
  --results-dir output/typesafe-pointwise \
  --dataset NanoBEIR-en --split NanoHotpotQA \
  --candidate-ranking bm25 --rerank-top-k 100

uv run hakari-bench evaluate reranker \
  --model jev-1.13.0 \
  --model-loader typesafe \
  --typesafe-mode listwise \
  --results-dir output/typesafe-listwise \
  --dataset NanoBEIR-en --split NanoHotpotQA \
  --candidate-ranking bm25 --rerank-top-k 100
```

`listwise` is the default when the mode is omitted. This is a convenient starting
configuration, not a claim that it is universally faster or more accurate.
The default result model ID is `typesafe/jev` for both modes and all API model
versions. The API model and mode remain recorded in result metadata.
The comparison commands use separate result directories because the same
model/task path is otherwise reused across modes. Existing results are skipped
unless `--overwrite` is specified. `--model-alias` can override the identity when
separate logical models are needed for a combined comparison.

For standard leaderboard evaluation, preserve the repository's default
`reranking_hybrid` candidate subset and all-candidate depth instead of assuming
that this BM25 diagnostic is the leaderboard protocol. See
[evaluation_policy.md](evaluation_policy.md).

## Reviewed Model Card

The static card is `config/model_cards/typesafe__jev.yaml`, pinned to
`jev-1.13.0`. It selects the hosted TypeSafe loader automatically:

```bash
uv run hakari-bench evaluate from-model-card \
  --model-card config/model_cards/typesafe__jev.yaml \
  --dataset NanoMIRACL --split ja
```

The adapter defaults and CLI overrides described below still apply. The card
records provider facts and operational notes; result metadata is the source of
truth for each run's effective instructions, mode, concurrency, and token limits.

## Request Modes

| Mode | State | Questions | Successful requests per nonempty query |
| --- | --- | --- | --- |
| `pointwise` | Query and one document | One Noul | Number of candidates |
| `listwise` | Query and all selected documents; balanced subsets within estimated token budgets | One Noul per document | One, or multiple after splitting |

Here, `listwise` describes the input context: every candidate is visible while
each document is scored independently with a Noul question. It does not mean
the API directly returns a permutation or uses a listwise training objective.
The application sorts the individual scores in both modes.

Both modes use the same true/false criteria, with these English instructions:

- `listwise`: "Does `documents.<id>` help answer `query`? Prefer passages with the specific facts needed."
- `pointwise`: "Does this candidate document help answer the query? Prefer passages that contain the specific facts needed."

The mode-specific instruction template is recorded in result metadata.
Candidates are selected and deterministically
shuffled by HAKARI before the adapter sees them. Equal scores retain that
shuffled order, independently of response completion order. Synthetic document
keys keep arbitrary corpus IDs out of the prompts and handle duplicate text.

The adapter exposes `rank`, not `predict`: the evaluator chunks
`predict` calls according to `--batch-size` (default 32), which would change the
shared state in `listwise`. The evaluator prioritizes `predict` or a callable
model over `rank`, so exposing only `rank` is intentional. Developers integrating
other listwise models should follow the
[listwise adapter contract](custom_model_backends.md#adapting-a-listwise-reranker).
`--batch-size` therefore does not partition Jev requests. Use
`max_concurrency` to control parallelism: `listwise` processes up to four queries
concurrently by default, while `pointwise` processes one query at a time with up
to 20 concurrent document requests. Split chunks within one listwise query are
processed sequentially, so splitting does not multiply request concurrency.
These are concurrency bounds, not requests-per-second limits. For example, use
`--model-loader-kwargs-json '{"max_concurrency":8}'` for eight concurrent
listwise queries. Use `1` for sequential execution. Rankings retain dataset query
order regardless of request completion order.

```bash
uv run hakari-bench evaluate reranker \
  --model jev-1.13.0 --model-loader typesafe --typesafe-mode pointwise \
  --model-loader-kwargs-json '{"max_concurrency":12,"timeout":180,"max_retries":8}' \
  --dataset NanoBEIR-en --split NanoHotpotQA \
  --candidate-ranking bm25 --rerank-top-k 100
```

Supported loader kwargs are `mode`, `max_concurrency` (default 4 for listwise, 20 for pointwise; null selects the mode default), `timeout`
(seconds, default 180), `max_retries` (default 8), `api_key_env` (default
`TYPESAFE_API_KEY`), `dotenv_path` (default `.env`; null disables loading),
`split_state_token_budget` (default 26000), `split_request_token_budget`
(default 48000), `split_tokenizer_name` (default `jhu-clsp/mmBERT-base`), and
`split_tokenizer_revision` (optional), and `document_max_tokens` (default 4000; null disables document truncation). The default tokenizer uses pinned revision
`c5955035435e2bf121cde7f3c8863ef52ff35d82`; another tokenizer uses its default
revision unless explicitly pinned. For example:

```bash
--model-loader-kwargs-json '{"split_tokenizer_name":"bert-base-multilingual-cased","split_state_token_budget":26000}'
```

These budgets are estimates checked before sending listwise requests, not
changes to Jev's limits.
`mode` can also be set in `--params-json` under `model.loader_kwargs`. A
conflicting `--typesafe-mode` is rejected. CrossEncoder init/inference kwargs
are rejected for this backend rather than silently ignored.

Pin `jev-1.13.0` for comparisons. Provider-controlled dtype, device, and
attention are unknown and recorded as null. GPU options do not configure Jev.

## Document Token Limit

Both modes keep the first 4000 tokens of each candidate document by default,
using the configured `split_tokenizer_name` (mmBERT by default). Query text is
unchanged. Short documents are passed through verbatim; longer documents are
encoded without special tokens, trimmed from the right, and decoded. The
resulting text is re-counted to ensure it is within the configured limit.
Listwise partition estimates use this prepared text. Corpus IDs are preserved.

```bash
--model-loader-kwargs-json '{"document_max_tokens":4000}'
```

Set `document_max_tokens` to null to reproduce earlier runs without an additional character limit. Configure the token limit with
`document_max_tokens`, not `--model-max-seq-length`. Existing
cached results are not rewritten; use a separate results directory for a changed
limit, or explicitly request `--overwrite` to rerun an existing task.

`model.backend_metadata.document_truncation` records the limit, tokenizer name
and revision, and per-task truncation count/events (query index, original document
index, original and sent token counts). Counts refer to candidate occurrences,
so a corpus document used by multiple queries can be counted multiple times.
The top-level backend `truncation` policy is `document_token_prefix` when enabled.
These are proxy tokenizer counts, not Jev's exact input tokenization. API context
errors can still occur and use the normal splitting behavior.

## Task-Specific Listwise Instructions

Override instructions using exact, case-sensitive `<dataset name>/<resolved task name>`
keys. For example, NanoMSMARCO resolves to `NanoBEIR-en/msmarco`:

```bash
uv run hakari-bench evaluate reranker \
  --model jev-1.13.0 --model-loader typesafe --typesafe-mode listwise \
  --dataset NanoBEIR-en --split NanoMSMARCO \
  --typesafe-task-instructions-json '{"NanoBEIR-en/msmarco":"Does {document} directly answer `query`?"}' \
  --results-dir output/typesafe-task-instructions
```

Templates must contain `{document}`, which becomes a reference such as
`` `documents.doc_0` ``. Criteria remain unchanged. Bare `msmarco`, another
dataset's task, and different capitalization never match. Unmatched keys emit
a warning (including tasks absent from the selected run) and are not applied.
Unspecified tasks use the default; overrides are supported only in listwise mode.
The same mapping can be supplied as `task_instructions` in model loader kwargs.

Each result records `model.backend_metadata.instruction_task`,
`instruction_source` (`default` or `task_override`), and the full effective
`instructions_template`; the mapping is also preserved in loader configuration.
Use separate result directories for comparisons: existing task results are
reused unless `--overwrite` is specified, even if instructions have changed.

## Limits, Failures, And Metadata

As documented on 2026-09-18, Jev 1.13 has a 64k-token request budget and a
32k-token budget for state plus the longest question. The service enforces the
limits. The adapter recognizes HTTP 400/422 errors with
`detail.error_type=max_tokens_exceeded` and does not require an actual token
count in the error response. A successful response's
`usage.input_tokens` counts the whole request, not just its shared state.

For `listwise`, the adapter checks estimated lengths before sending requests:

1. Load the configured tokenizer (by default the
   [mmBERT-base tokenizer](https://huggingface.co/jhu-clsp/mmBERT-base)). Set
   `model_max_length=65536` instead of mmBERT's native 8192 and measure with
   `truncation=False`. This is tokenizer-only counting; it does not extend the
   model's context. Text beyond 65536 tokens is also counted without truncation.
   Include estimates of the query, JSON, and question overhead.
2. Split when state plus the longest question exceeds 26000 estimated tokens,
   or the whole request exceeds 48000. Check every proposed child, increasing
   the number of chunks until each fits. These estimates reserve headroom for
   Jev's documented 32k/64k limits. The tokenizer is a proxy, not a confirmed
   Jev tokenizer, so acceptance is not guaranteed.
3. Balance candidate counts to within one document, distributing remainders
   to the last chunks: 100 can become 50/50 or 33/33/34, 101 becomes 50/51 when
   split in two, and 83 becomes 41/42. Within those count quotas, assign the
   longest documents first to the chunk with the lowest current token total.
   Before sending, shuffle each chunk using a deterministic hash of a fixed
   seed, query hash, and original document index. This avoids sending documents
   in length order while preserving reproducibility.
4. If the API returns `max_tokens_exceeded` (HTTP 400 or 422), halve both
   estimated budgets for that chunk and repartition it. Repeat on further
   overflow. Successful chunks are retained and are not rescored. A single
   document plus query that exceeds the current estimated budget or cannot
   recover from an API limit error fails explicitly; recursive splitting does not further truncate text.
5. Merge all successful chunks' **raw Noul scores** and sort globally. Equal
   scores retain the original shuffled candidate order, not chunk order.
   Every candidate, including duplicate text and a possible 101st safeguard,
   is scored exactly once successfully. No candidate is discarded; document shortening follows the configured token limit.

The shared context changes after splitting, so scores from different chunks
are not guaranteed to have the same calibration as a single full-list request.
The mode stays `listwise`; it does not silently change to `pointwise`.
`pointwise` cannot recover a single oversized query/document pair by splitting
the candidate list and therefore fails on that error.

`--model-max-seq-length` is rejected. Leave the separate, existing
`HAKARI_RERANKER_DOCUMENT_MAX_CHARS` environment override unset for comparable
runs without an additional character limit. Configure the token limit with
`document_max_tokens`, not `--model-max-seq-length`.

HTTP 429/529 and transient 500/502/503/504 responses use bounded retries with
exponential backoff, jitter, and `Retry-After` support. Connection failures are
also subject to the retry budget. Exhausted retries, authentication errors,
other validation errors, missing answers, nonfinite/out-of-range Noul values, or
missing usage metadata fail the task; they do not become zero scores. A retried
request whose response was lost may still have incurred provider charges.

Each task's `model.backend_metadata` records the mode, instruction template,
criteria, API-returned model IDs, `max_concurrency`, `query_concurrency`,
request/retry counts, and input/output tokens.
Counters reset before each uncached task. `usage` counts successfully validated
responses and their reported HTTP retry history; it is not a billing ledger for
failed or lost responses. Existing evaluation timing records the scoring wall
time. Full response bodies and API credentials are not stored in metadata.
`usage.max_tokens_errors` separately counts rejected requests, which do not
report billable usage.

Every split is announced on stderr. The result JSON also stores
`model.backend_metadata.listwise_splitting` with the tokenizer name, revision, 65536 counting configuration,
estimated budgets, shuffle policy/seed, merge policy, and a `queries` trace for each affected query.
Each trace includes the zero-based nonempty-query call index, query SHA-256,
original document count, estimated document lengths, split events (reason, parent
indices, depth, effective budgets, estimated lengths, child indices/counts), and
successful final chunks in their actual shuffled request order.
Document indices refer to the original shuffled input list. `status: merged`
means all candidates were recovered. Traces and error counters reset per task;
an unsplit task has an empty `queries` list. Failed tasks do not produce a
normal benchmark result.

At the documented input price of $0.042 per million tokens (output free), an
estimate is `usage.input_tokens / 1_000_000 * 0.042`. Check the live
[model page](https://docs.typesafe.ai/models) before budgeting. Neither token
savings nor latency improvements are guaranteed by the mode name.

## Official References

- [HTTP API](https://docs.typesafe.ai/api)
- [Models, pricing, and limits](https://docs.typesafe.ai/models)
- [Noul reranking cookbook](https://docs.typesafe.ai/cookbooks/rerank_typesafe)
- [Parallel questions with identical state](https://docs.typesafe.ai/cookbooks/parallel_questions)
- [Jev 1.13 limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13)
