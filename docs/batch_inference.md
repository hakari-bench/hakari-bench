# Batch Inference

Batch inference is an offline dense-embedding workflow. It writes provider
request files, registers a remote batch job, fetches the finished provider
outputs, and materializes normal HAKARI result JSON from the returned
embeddings.

The initial provider implementation is OpenAI embeddings. The command layout is
provider-aware so additional dense providers can be added without changing the
materialized result format.

## Register

Register a batch with a stable local target name:

```bash
uv run --group openai hakari-bench batch dense register \
  --target openai-small-nanobeir-en-a \
  --provider openai \
  --model text-embedding-3-small \
  --dataset hakari-bench/NanoBEIR-en \
  --split arguana \
  --split climate-fever
```

The command writes a workspace under:

```text
tmp/batch_workspace/{target}/
```

The workspace contains `batch_metadata.json`, provider request JSONL, per-task
request metadata, and later the fetched output and error JSONL files. The target
name is the recovery handle for later commands.

OpenAI embedding batches currently enforce the provider limit of 50,000
embedding inputs per batch by default. Split large dataset collections into
multiple targets before registering. Inputs are truncated with `tiktoken` to
8100 tokens by default, leaving headroom below the 8192-token embedding input
limit.

## Fetch

Fetch status and output files by target:

```bash
uv run --group openai hakari-bench batch dense fetch \
  --target openai-small-nanobeir-en-a
```

To poll until completion:

```bash
uv run --group openai hakari-bench batch dense fetch \
  --target openai-small-nanobeir-en-a \
  --wait \
  --poll-seconds 900
```

The fetch step is resumable. It reads `batch_metadata.json`, refreshes the
remote status, and downloads provider output/error files when available.
Downloads are written to a temporary file first and then renamed into place, so
interrupted downloads can be retried by running the same command again.

If a batch has `errors.jsonl`, inspect the provider errors and decide whether to
register a new target for only the failed inputs or to overwrite and register
the full target again. Keep the failed workspace for auditability until the
replacement result has been materialized and compared.

## Materialize Results

Materialize fetched embeddings into the same per-task result format used by
normal evaluation:

```bash
uv run --group openai hakari-bench batch dense materialize \
  --target openai-small-nanobeir-en-a \
  --results-dir output/openai-batch \
  --embedding-variant truncate:256,512,1024
```

The materializer restores query/document embeddings by `custom_id`, validates
dataset id order, and runs the standard dense scoring path. Dense default
variants are preserved. Explicit truncation dimensions also expand into
truncation plus int8/binary and rescore variants.

OpenAI batch truncation variants use the repository OpenAI policy: request full
embeddings once, then compute `full[:DIM]` followed by L2 normalization locally.
This keeps batch materialization aligned with the normal OpenAI dense evaluator.

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
