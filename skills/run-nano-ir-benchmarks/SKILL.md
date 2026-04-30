---
name: run-nano-ir-benchmarks
description: Workflow for measuring models with the nano-ir-bench project. Use when Codex is asked to benchmark or evaluate embedding models on NanoIR/Nano* datasets, choose prompt/truncate-dim/attention options, schedule GPU benchmark jobs, compare BM25, or refresh DuckDB and HTML leaderboard reports.
---

# Run NanoIR Benchmarks

## Core Workflow

1. Inspect the repository first: read `AGENTS.md`, `README.md`, `pyproject.toml`, dataset configs under `config/`, and the CLI help for the installed checkout.
2. Identify the requested models, datasets, output policy, and whether existing result JSON should be reused or overwritten.
3. For each model, research model-specific encoding requirements before running benchmarks.
4. Run a small validation command when options are uncertain, then scale to the requested benchmark set.
5. Keep a progress checklist for long runs, especially when multiple models or GPUs are involved.
6. After benchmarking, rebuild DuckDB/HTML reports when the user asks for comparisons, leaderboards, or viewer updates.

## Model Research Checklist

For every specified model:

- Check whether the model is a Sentence Transformers model with prompt configuration. Prefer its built-in prompt config when present.
- If no usable Sentence Transformers prompt config exists, inspect the Hugging Face model card first, then relevant articles or papers for retrieval prefixes such as query/document/passage instructions.
- Record and use explicit retrieval prefixes when the model card or paper requires them, for example via `--query-prompt`, `--corpus-prompt`, `--query-prompt-name`, or `--corpus-prompt-name`.
- Investigate Matryoshka support. If the model card or paper documents supported dimensions, prefer simultaneous derived evaluations with `--embedding-variant truncate:DIM` over separate reruns.
- Check whether `--trust-remote-code` is required.
- Check the model's default maximum sequence length, but do not override it unless the user explicitly asks.

## Attention And Runtime Choice

- Do not assume Flash Attention 2 works with every model or every Transformers major version.
- Compare the practical options before large runs:
  - Transformers 4.x + Flash Attention 2.
  - Transformers 5.x + SDPA.
- Treat Transformers 5.x + FA2 as suspect unless it has already been verified for that model in this environment.
- Prefer the fastest verified configuration that preserves correctness and model defaults.
- For models that previously failed with FA2, retry with SDPA or no explicit attention implementation before skipping.

## Batch Size And Context Length

- Never pass `--model-max-seq-length`, `max_length`, or similar token-length overrides unless the user explicitly instructs it.
- Do not shorten model context length to make a benchmark fit. Reduce batch size first.
- For long-context-heavy tasks such as MLDR, LongEmbed, LongEmbed-like datasets, or corpora with very long documents, start with a conservative batch size.
- If CUDA OOM or repeated runtime errors occur, retry with smaller batch sizes before changing dtype or attention implementation.
- If changing dtype or attention implementation is needed, report the fallback in the result summary.

## Running Benchmarks

Use the project CLI and existing project conventions:

```bash
uv run nano-ir-bench evaluate \
  --model MODEL_NAME \
  --dataset DATASET_NAME \
  --dtype bf16
```

For Matryoshka-style dimensions, evaluate derived truncated embeddings from one
inference pass:

```bash
uv run nano-ir-bench evaluate \
  --model MODEL_NAME \
  --dataset DATASET_NAME \
  --embedding-variant truncate:512,256
```

For BM25:

```bash
uv run nano-ir-bench evaluate \
  --model-type bm25 \
  --dataset DATASET_NAME
```

Use both GPUs when available by assigning separate processes with `CUDA_VISIBLE_DEVICES` or `--device` as appropriate. Keep concurrent jobs writing to distinct model output directories. For long benchmark waves, write an ignored checklist under `tmp/` and update it as tasks complete.

## Result Hygiene

- Respect existing result JSON. Skip cached results unless the user asks for override or the run configuration must be corrected.
- Preserve enough metadata to explain the run: prompts, embedding variants, dtype, attention implementation, Transformers/Sentence Transformers/Torch versions, batch size, timing, parameter counts, and max sequence length.
- When comparing models, check that prompt and embedding-variant choices are fair and intentional.
- Rebuild DuckDB and HTML reports after adding new benchmark results that should appear in the leaderboard.
- Summarize failures plainly. If a model keeps failing after reasonable batch-size and attention fallbacks, mark it skipped with the exact reason.
