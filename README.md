# nano-ir-bench

NanoIR Benchmark is a library, viewer, and leaderboard project for evaluating small information retrieval datasets.

Nano-style information retrieval benchmark runner for SentenceTransformers-compatible models.

Built-in dataset definitions include `NanoBEIR-en`, `NanoMIRACL`, `NanoMLDR`,
`NanoJMTEB`, `NanoRTEB`, `NanoMTEB`, `NanoMMTEB`, and
`NanoCodeSearchNet`.

## Example

```bash
uv run nano-ir-bench evaluate \
  --model hotchpotch/bekko-embedding-pico-beta-unir-v7 \
  --dataset sentence-transformers/NanoBEIR-en \
  --dtype bf16
```

Results are written under:

```text
output/results/{model_name}/{dataset_name}/{split_or_task}.json
```

## BM25

BM25 can be evaluated directly. If the dataset provides a candidate subset named
by `--candidate-subset-name` (default: `bm25`), that ranking is used as the BM25
baseline. If the subset is unavailable, BM25 is computed locally.

```bash
uv run nano-ir-bench evaluate \
  --model-type bm25 \
  --dataset NanoMLDR \
  --split ja \
  --top-k 100
```

BM25 candidate files can also be generated for reranking workflows:

```bash
uv run nano-ir-bench build-bm25 \
  --dataset NanoMLDR \
  --split ja \
  --bm25-tokenizer english_porter_stop \
  --top-k 100
```

BM25 scoring uses `bm25s` with the standard Okapi-style Robertson method.
Available tokenizers are `regex`, `whitespace`, `transformer`, `stemmer`,
`english_regex`, `english_porter`, `english_porter_stop`, and `wordseg`. The
default is `auto`: 10 query texts are sampled deterministically and detected
with `fast-langdetect`. If the detected language supports `wordseg`, BM25 uses
`wordseg`; otherwise it uses `regex`.

The resolved BM25 algorithm and tokenizer are written to each result JSON under
`config.bm25` and `model.bm25`.

`wordseg` is optional and lazy-loads language-specific tokenizers. Install the
extra before using it:

```bash
uv sync --extra wordseg
```

Supported `wordseg` language values are passed via `--bm25-tokenizer-name`:

```bash
uv run nano-ir-bench build-bm25 \
  --dataset NanoMLDR \
  --split ja \
  --bm25-tokenizer wordseg \
  --bm25-tokenizer-name ja
```

The current mapping is `ja` = `fugashi` + `unidic-lite`, `zh` = `jieba`,
`th` = `pythainlp`, and `ko` = `kiwipiepy`.

## Viewer

Install the web viewer dependencies with the `viewer` group:

```bash
uv sync --group viewer
```

For all development and viewer dependencies, use the `all` group:

```bash
uv sync --group all
```

Start the HTMX/Tailwind leaderboard viewer:

```bash
uv run nano-ir-bench web
```

By default, it binds to `127.0.0.1:8000` and keeps
`output/viewer/nano_ir_bench.duckdb` synchronized from the benchmark output
DuckDB when a page is loaded. Use `--host 0.0.0.0 --port 28090` for remote
access, or pass `--source-output-dir` / `--source-duckdb-path` to point at a
different source.

## Achievements

- Built on the idea behind [Nano-BEIR](https://huggingface.co/blog/sionic-ai/eval-sionic-nano-beir).
- The NanoBEIR evaluation implementation in [Sentence Transformers](https://github.com/huggingface/sentence-transformers/) was a reference for this project. Thanks to the maintainers and contributors.
