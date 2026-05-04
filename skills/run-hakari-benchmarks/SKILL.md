---
name: run-hakari-benchmarks
description: Workflow for measuring models with the HAKARI-Bench project. Use when Codex is asked to benchmark or evaluate embedding models on NanoIR/Nano* datasets, choose prompt/truncate-dim/attention options, schedule GPU benchmark jobs, compare BM25, or refresh DuckDB and HTML leaderboard reports.
---

# Run HAKARI-Bench Evaluations

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
  `--embedding-variant truncate-sparse-query-max-dims:8,16,32` for query-only
  limits and `--embedding-variant truncate-sparse-docs-max-dims:64,128,256`
  for document-only limits.
- For sparse models, query and document active dimensions can be varied
  independently. Use `--embedding-variant
  truncate-sparse-query-max-dims:8,16,32` for query-only limits,
  `--embedding-variant truncate-sparse-docs-max-dims:64,128,256` for
  docs-only limits, and use `--embedding-variant-cross
  truncate-sparse-query-max-dims:8,16,32
  truncate-sparse-docs-max-dims:64,128,256` for a full query x docs grid.
  Base, query-only, docs-only, and query x docs comparisons require combining
  those standalone variants with the cross product.
- Dense models automatically run normalized `int8` and binary quantized search variants and top-100 float-rescored variants when no embedding variants are explicitly specified. Quantized search uses exact PyTorch matrix scoring; `--score-device auto` keeps scoring on the model output device, and `--score-device cpu` or `--score-device cuda` forces the post-encode matrix work to that device. Use `--no-quantize` only when the user wants to suppress those automatic dense variants.
- When SentenceTransformers models run on a non-CPU device, base dense/sparse/late-interaction tensor scoring should stay on PyTorch tensors and score/top-k on that device. CPU model runs keep using the NumPy/SciPy paths. `--score-device cpu` forces post-encode score/top-k work back to CPU NumPy/SciPy where applicable while leaving model encoding on the requested model device; `--score-device cuda` forces supported post-encode matrix scoring to CUDA.
- Late-interaction/ColBERT runs use PyLate ColBERT and exact MaxSim scoring. Check model-specific query/document prefixes, sequence lengths, `--trust-remote-code`, and `--late-interaction-attend-to-expansion-tokens` before running.
- For `jinaai/jina-colbert-v2`, the documented PyLate initialization uses `query_prefix="[QueryMarker]"`, `document_prefix="[DocumentMarker]"`, `attend_to_expansion_tokens=True`, and `trust_remote_code=True`. Use `--late-interaction-query-prefix "[QueryMarker]"`, `--late-interaction-document-prefix "[DocumentMarker]"`, `--late-interaction-attend-to-expansion-tokens`, and `--trust-remote-code` unless the current model card says otherwise.
- For dense models, use `--embedding-variant int8,binary` and `--embedding-variant rescore:int8,binary` when quantized search variants must be listed explicitly. Quantized variants L2-normalize embeddings before quantization, convert them to SentenceTransformers-compatible stored codes, and score those codes with exact PyTorch matrix operations. Rescore reranks the top 100 quantized candidates with the normalized source float embeddings and does not re-embed documents.
- Do not add quantized embedding variants for sparse/SPLADE-style models. Sparse quantization is intentionally unsupported in the CLI; use post-encode sparse truncation variants for sparse footprint and latency trade-offs.
- If Matryoshka dimensions are requested or documented, evaluate all three related groups: standalone dimensions, standalone quantized search, and the dimension x quantized search cross product. For example, use `--embedding-variant truncate:256,128,64`, `--embedding-variant int8,binary`, `--embedding-variant rescore:int8,binary`, `--embedding-variant-cross truncate:256,128,64 int8,binary`, and `--embedding-variant-cross truncate:256,128,64 rescore:int8,binary`. This is "all" because standalone dimensions isolate the dimension trade-off, standalone quantized search isolates the quantization trade-off at the original dimension, and the cross product measures combined trade-offs such as `128dim x int8` and `64dim x binary`, with and without top-100 float rescore.
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
uv run hakari-bench evaluate \
  --model MODEL_NAME \
  --dataset DATASET_NAME \
  --dtype bf16
```

For Matryoshka-style dimensions, evaluate derived truncated embeddings from one
inference pass:

```bash
uv run hakari-bench evaluate \
  --model MODEL_NAME \
  --dataset DATASET_NAME \
  --embedding-variant truncate:512,256
```

For dense models, standard post-encode quantized search is automatic when no
embedding variants are specified. Add `--no-quantize` only when the user asks
for the base result without automatic `int8` and binary variants or
their top-100 float-rescored variants:

```bash
uv run hakari-bench evaluate \
  --model MODEL_NAME \
  --dataset DATASET_NAME
```

When dimensions are part of the run, include standalone dimensions, standalone
quantized search, and their cross product:

```bash
uv run hakari-bench evaluate \
  --model MODEL_NAME \
  --dataset DATASET_NAME \
  --embedding-variant truncate:256,128,64 \
  --embedding-variant int8,binary \
  --embedding-variant rescore:int8,binary \
  --embedding-variant-cross truncate:256,128,64 int8,binary \
  --embedding-variant-cross truncate:256,128,64 rescore:int8,binary
```

The benchmark implementation converts all of these derived evaluations into a
single post-encode pipeline path, so the model is still encoded once and cross
variants add only the transform/scoring work needed for each derived embedding.

For sparse/SPLADE-style models, use post-encode sparse truncation variants
instead of dense `truncate:` variants. Query-only sparsity limits:

```bash
uv run hakari-bench evaluate \
  --model MODEL_NAME \
  --model-type sparse \
  --dataset DATASET_NAME \
  --embedding-variant truncate-sparse-query-max-dims:8,16,32
```

When query and document limits should differ, use query/docs-specific variants
and their cross product:

```bash
uv run hakari-bench evaluate \
  --model MODEL_NAME \
  --model-type sparse \
  --dataset DATASET_NAME \
  --embedding-variant truncate-sparse-query-max-dims:8,16,32 \
  --embedding-variant truncate-sparse-docs-max-dims:64,128,256 \
  --embedding-variant-cross truncate-sparse-query-max-dims:8,16,32 truncate-sparse-docs-max-dims:64,128,256
```

If only the full query x docs grid is requested, the standalone query-only and
docs-only variants may be omitted. The base no-limit result is always included
as `evaluation.embedding_evaluations[0]`.

If the user asks for sparse quantization, explain that it is intentionally
unsupported in the CLI and use sparse truncation comparisons instead.

For BM25:

```bash
uv run hakari-bench evaluate \
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
