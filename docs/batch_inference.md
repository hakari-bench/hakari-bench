# Batch Inference

Batch inference is an offline dense-embedding workflow. It writes provider
request files, registers remote batch jobs, fetches finished provider outputs,
and materializes normal HAKARI result JSON from the returned embeddings.

The initial provider implementation is OpenAI embeddings. The command layout is
provider-aware so additional dense providers can be added without changing the
materialized result format.

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
embedding inputs per provider batch by default. Inputs are truncated with
`tiktoken` to 8100 tokens by default, leaving headroom below the 8192-token
embedding input limit.

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

OpenAI batch truncation variants use the repository OpenAI policy: request full
embeddings once, then compute `full[:DIM]` followed by L2 normalization locally.
This keeps batch materialization aligned with the normal OpenAI dense evaluator.

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
