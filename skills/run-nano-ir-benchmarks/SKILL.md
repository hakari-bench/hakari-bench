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

- Read `docs/model_specific_benchmarking_notes.md` before choosing prompts,
  attention implementation, Transformers version, or compatibility fallbacks.
  Follow its model-specific notes when they apply.
- Check whether the model is a Sentence Transformers model with prompt configuration. Prefer its built-in prompt config when present.
- If no usable Sentence Transformers prompt config exists, inspect the Hugging Face model card first, then relevant articles or papers for retrieval prefixes such as query/document/passage instructions.
- Record and use explicit retrieval prefixes when the model card or paper requires them, for example via `--query-prompt`, `--corpus-prompt`, `--query-prompt-name`, or `--corpus-prompt-name`.
- Investigate Matryoshka support. If the model card or paper documents supported dimensions, prefer simultaneous derived evaluations with `--embedding-variant truncate:DIM` over separate reruns.
- For sparse/SPLADE-style models, use `--model-type sparse`. When evaluating
  sparsity trade-offs, prefer post-encode variants over separate reruns:
  `--embedding-variant sparse-max-active-dims:256,128,64` for symmetric
  query+document limits, or query/docs-specific variants when asymmetric
  limits are requested.
- For sparse models, query and document active dimensions can be varied
  independently. Use `--embedding-variant sparse-query-max-active-dims:8,16,32`
  for query-only limits, `--embedding-variant
  sparse-docs-max-active-dims:64,128,256` for docs-only limits, and use
  `--embedding-variant-cross sparse-query-max-active-dims:8,16,32
  sparse-docs-max-active-dims:64,128,256` for a full query x docs grid.
  Base, query-only, docs-only, and query x docs comparisons require combining
  those standalone variants with the cross product.
- Dense models automatically run exact usearch `int8` and binary quantized search variants when no embedding variants are explicitly specified. Use `--no-quantize` only when the user wants to suppress those automatic dense variants.
- For dense models, `--embedding-variant quantize:int8,ubinary` is a compatibility shorthand for exact usearch quantized search. `ubinary` maps to the binary usearch representation. usearch receives pre-quantized SentenceTransformers codes and does not perform calibration.
- For sparse/SPLADE-style models, use `--embedding-variant quantize-docs:int8,ubinary` only when explicitly requested. Sparse `int8` preserves sparse indices and quantizes only non-zero weights with a corpus-derived value range before dequantized sparse scoring; sparse `ubinary` preserves sparse indices and scores non-zero dimensions as an unweighted presence vector.
- If Matryoshka dimensions are requested or documented, evaluate all three related groups: standalone dimensions, standalone quantization, and the dimension x quantization cross product. For example, use `--embedding-variant truncate:256,128,64`, `--embedding-variant quantize:int8,ubinary`, and `--embedding-variant-cross truncate:256,128,64 quantize:int8,ubinary`. This is "all" because standalone dimensions isolate the dimension trade-off, standalone quantization isolates the quantization trade-off at the original dimension, and the cross product measures combined trade-offs such as `128dim x int8` and `64dim x ubinary`.
- Only use `quantize-docs:` for docs-only dequantized storage probes and `quantize-both:` when the user explicitly asks for symmetric query+document quantization.
- Do not use evaluation queries for scalar quantization calibration. The benchmark uses corpus-derived ranges for `int8`/`uint8`; using query values for buckets would be a transductive test-set adaptation.
- Check whether `--trust-remote-code` is required.
- Check the model's default maximum sequence length, but do not override it unless the user explicitly asks.
- When a benchmark should be reproducible against a specific dataset state, use `--dataset-revision REV`; otherwise verify that the output JSON records the resolved Hugging Face dataset SHA.

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

For dense models, standard post-encode quantized search is automatic when no
embedding variants are specified. Add `--no-quantize` only when the user asks
for the base result without automatic usearch `int8` and binary variants:

```bash
uv run nano-ir-bench evaluate \
  --model MODEL_NAME \
  --dataset DATASET_NAME
```

Only use symmetric query+document quantization when explicitly requested:

```bash
uv run nano-ir-bench evaluate \
  --model MODEL_NAME \
  --dataset DATASET_NAME \
  --embedding-variant quantize-both:int8,ubinary
```

When dimensions are part of the run, include standalone dimensions, standalone
quantization, and their cross product:

```bash
uv run nano-ir-bench evaluate \
  --model MODEL_NAME \
  --dataset DATASET_NAME \
  --embedding-variant truncate:256,128,64 \
  --embedding-variant quantize:int8,ubinary \
  --embedding-variant-cross truncate:256,128,64 quantize:int8,ubinary
```

The benchmark implementation normalizes all of these derived evaluations into a
single post-encode pipeline path, so the model is still encoded once and cross
variants add only the transform/scoring work needed for each derived embedding.

For sparse/SPLADE-style models, use sparse max-active-dimension variants instead
of dense `truncate:` variants. Symmetric query+document sparsity limits:

```bash
uv run nano-ir-bench evaluate \
  --model MODEL_NAME \
  --model-type sparse \
  --dataset DATASET_NAME \
  --embedding-variant sparse-max-active-dims:256,128,64
```

When query and document limits should differ, use query/docs-specific variants
and their cross product:

```bash
uv run nano-ir-bench evaluate \
  --model MODEL_NAME \
  --model-type sparse \
  --dataset DATASET_NAME \
  --embedding-variant sparse-query-max-active-dims:8,16,32 \
  --embedding-variant sparse-docs-max-active-dims:64,128,256 \
  --embedding-variant-cross sparse-query-max-active-dims:8,16,32 sparse-docs-max-active-dims:64,128,256
```

If only the full query x docs grid is requested, the standalone query-only and
docs-only variants may be omitted. The base no-limit result is always included
as `evaluation.embedding_evaluations[0]`.

For sparse models, include docs-only quantization with `quantize-docs:` when
the user asks for sparse quantization comparisons:

```bash
uv run nano-ir-bench evaluate \
  --model MODEL_NAME \
  --model-type sparse \
  --dataset DATASET_NAME \
  --embedding-variant sparse-query-max-active-dims:8,16,32 \
  --embedding-variant sparse-docs-max-active-dims:64,128,256 \
  --embedding-variant quantize-docs:int8,ubinary \
  --embedding-variant-cross sparse-query-max-active-dims:8,16,32 sparse-docs-max-active-dims:64,128,256
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
- Preserve enough metadata to explain the run: dataset revision, prompts, embedding variants and representation metadata, dtype, attention implementation, Transformers/Sentence Transformers/Torch versions, batch size, timing, parameter counts, and max sequence length.
- When comparing models, check that prompt and embedding-variant choices are fair and intentional.
- Rebuild DuckDB and HTML reports after adding new benchmark results that should appear in the leaderboard.
- Summarize failures plainly. If a model keeps failing after reasonable batch-size and attention fallbacks, mark it skipped with the exact reason.
