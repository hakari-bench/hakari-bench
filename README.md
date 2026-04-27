# nano-ir-bench

Nano-style information retrieval benchmark runner for SentenceTransformers-compatible models.

Built-in dataset definitions include `NanoBEIR-en`, `NanoMIRACL`, `NanoMLDR`,
and `NanoCodeSearchNet`.

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

BM25 can be evaluated directly:

```bash
uv run nano-ir-bench evaluate \
  --model-type bm25 \
  --dataset NanoMLDR \
  --split ja \
  --bm25-tokenizer regex \
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
default is `regex`, which is a safe language-agnostic choice for non-CJK text.

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
