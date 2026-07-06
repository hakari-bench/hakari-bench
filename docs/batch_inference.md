# Batch Inference

This document is the operational guide for HAKARI-Bench batch inference, especially offline dense embedding evaluation through provider batch APIs. It explains how to register batch jobs, write stable local request files, submit them to a provider such as OpenAI, poll or fetch completed outputs, and materialize normal HAKARI result JSON from returned embeddings. Coding agents should use this file when searching for batch dense evaluation, OpenAI Batch API, provider-aware request manifests, batch target names, materialized result paths, retry behavior, or comparison with direct evaluation. It also captures the legacy single-batch command shape and the intended boundary between batch embedding generation and leaderboard-compatible result JSON creation.

Batch inference is an offline dense-embedding workflow. It writes provider
request files, registers remote batch jobs, fetches finished provider outputs,
and materializes normal HAKARI result JSON from the returned embeddings.

The provider implementations currently cover OpenAI embeddings and Gemini
embeddings. The command layout is provider-aware so additional dense providers
can be added without changing the materialized result format.

## Register

Register batches with a stable local target name:

```bash
uv run --group openai hakari-bench batch dense register \
  --target openai-small-nanobeir-en \
  --provider openai \
  --model text-embedding-3-small \
  --dataset hakari-bench/NanoBEIR-en \
  --split arguana \
  --split climate-fever \
  --results-dir output/openai-batch
```

The command writes a workspace under:

```text
tmp/batch_workspace/{target}/
```

The workspace contains `batch_index.json` plus one subdirectory per registered
provider batch under `batches/`. Registration is task-oriented: each Nano-set
task gets its own provider batch. If a task exceeds the provider embedding-input
limit, it is split into multiple provider batches for that task. The target name
is the recovery handle for later commands.

OpenAI embedding batches currently enforce the provider limit of 50,000
embedding inputs per provider batch by default. They also split task batches by
input JSONL file size, using a 190,000,000-byte default limit to stay below the
provider's 200 MiB input file limit. Inputs are truncated with `tiktoken` to
8100 tokens by default, leaving headroom below the 8192-token embedding input
limit.

Gemini embedding batches use Vertex/Enterprise batch prediction with GCS
input/output. Provide `--provider gemini`, `--gemini-project`, and
`--gcs-uri-prefix`; for `gemini-embedding-2`, use `--gemini-location global`.
The input JSONL is written as one request per line:

```json
{"key":"...","request":{"content":{"parts":[{"text":"..."}]}}}
```

Gemini embedding inputs are locally truncated before JSONL writing with the
Gemma2 SentencePiece tokenizer. HAKARI records this as
`token_count_policy=len(gemma2.encode(text)) + 1`, matching local smoke checks
against `gemini-embedding-2` `count_tokens`. Keep the default 8100-token guard;
Developer API batch can silently truncate over-limit inputs, but benchmark runs
should not rely on that hidden provider behavior.

For `gemini-embedding-2`, Vertex/Enterprise batch prediction and the Gemini
Developer API embedding batch are different surfaces:

- Vertex/Enterprise uses Google Cloud ADC/project credentials, GCS input/output,
  `client.batches.create(...)`, and `batchPredictionJobs` under the selected
  location. In local checks on 2026-06-23, `gemini-embedding-2` accepted only the
  `global` location for batch registration; `us-central1` returned
  `MODEL_NOT_SUPPORTED_FOR_BATCH`.
- The Gemini Developer API uses an API key (`GEMINI_API_KEY` or
  `GOOGLE_API_KEY`) and `client.batches.create_embeddings(...)`. The Python Gen
  AI SDK explicitly rejects `create_embeddings` when `vertexai=True`.

If Vertex/Enterprise Gemini embedding batch remains in `JOB_STATE_PENDING` or
`JOB_STATE_QUEUED` with no `startTime`, treat it as provider capacity queueing
rather than a local retryable error. Google documents that Gemini batch jobs use
a shared resource pool, can queue for up to 72 hours, and do not support
Provisioned Throughput. There is no known local flag that forces queued Vertex
Gemini embedding jobs to start. Prefer direct async embedding evaluation or the
Gemini Developer API embedding batch path when an API key is available.

For text retrieval with Gemini Embedding 2, pass the provider-recommended
retrieval prompts explicitly:

```bash
uv run --group gemini hakari-bench batch dense register \
  --target gemini-embedding-2-nanomiracl-en \
  --provider gemini \
  --model gemini-embedding-2 \
  --dataset NanoMIRACL \
  --split en \
  --gemini-project ml-sandbox-309804 \
  --gemini-location global \
  --gcs-uri-prefix gs://bucket/hakari-batches/gemini-embedding-2-nanomiracl-en \
  --query-prompt "task: search result | query: " \
  --document-prompt "title: none | text: "
```

If a readable result JSON already exists for a selected Nano-set task, register
skips that task by default. Pass `--overwrite` to force a new batch registration
and later overwrite the result.

## Process

Process finished task batches:

```bash
uv run --group openai hakari-bench batch dense process \
  --target openai-small-nanobeir-en \
  --results-dir output/openai-batch \
  --embedding-variant truncate:256,512,1024
```

The process command is resumable. It reads `batch_index.json`, checks provider
status for every registered batch, and only downloads data for a task when all
batches for that task have completed. It then materializes the task result JSON
and removes downloaded provider output/error JSONL files by default because they
can be large. Pass `--keep-downloaded-batch-files` to keep those downloaded
files for debugging.

Downloads are written to a temporary file first and then renamed into place, so
interrupted downloads can be retried by running the same command again.

If a batch has `errors.jsonl`, inspect the provider errors and decide whether to
register a new target or overwrite and register the target again. Keep the
failed workspace for auditability until the replacement result has been
materialized and compared.

The materializer restores query/document embeddings by `custom_id`, validates
dataset id order, and runs the standard dense scoring path. Dense default
variants are preserved. Explicit truncation dimensions also expand into
truncation plus int8/binary and rescore variants.

OpenAI and Gemini batch truncation variants use the hosted-embedding policy:
request full embeddings once, then compute `full[:DIM]` followed by L2
normalization locally. This keeps batch materialization aligned with the normal
hosted dense evaluators.

## Legacy Single-Batch Commands

`batch dense fetch` and `batch dense materialize` still operate on a single
`batch_metadata.json` target. Prefer `batch dense process` for new task-oriented
batch runs because it avoids downloading outputs for incomplete tasks and
cleans up downloaded provider files after successful result creation.

## Compare With Direct Evaluation

Build or append a DuckDB from the batch result root and compare it with the
existing direct-evaluation result root. Prefer existing local or remote DuckDB
caches for model comparisons; raw `json.xz` reads are mostly useful for focused
debugging of newly materialized results.

```bash
uv run python scripts/build_results_database_and_report.py \
  --results-dir output/openai-batch \
  --duckdb-path output/openai-batch/hakari_bench.duckdb \
  --incremental
```

For acceptance, compare every expected task and variant. Small metric
differences can occur between direct API calls and provider batch outputs even
when both paths request full dimensions and apply local normalized-prefix
truncation.
