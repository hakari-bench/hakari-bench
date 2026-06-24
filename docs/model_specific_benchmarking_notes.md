# Model-Specific Benchmarking Notes

This document collects model-family and checkpoint-specific benchmarking decisions that override generic HAKARI-Bench defaults. It records verified prompts, prompt names, attention implementations, dtype choices, max sequence length concerns, trust-remote-code notes, tokenizer quirks, sparse settings, ColBERT/PyLate options, OpenAI settings, and runtime observations for models such as Ruri, E5, Qwen3, EmbeddingGemma, Bekko, Jina, Snowflake Arctic, IBM Granite, F2LLM, Perplexity, GTE, SPLADE, OpenAI embeddings, and static similarity MRL models. Coding agents should use this file when searching for exact model run settings, prompt overrides, attention recommendations, compatibility notes, or reproducibility caveats.

When measuring specific models, follow the notes in this document. These notes
override generic benchmarking defaults when they are more specific, because some
models require exact prompts or runtime choices for comparable retrieval scores.
Start from the model author's officially recommended attention implementation
when it is documented. If this document records a different verified runtime,
use the verified note and preserve the attention implementation in result
metadata so slow default-attention runs are not mistaken for intentional
baselines.

## NanoMIRACL/en Runtime Matrix

On 2026-05-09, these models were revalidated on NanoMIRACL/en with a separate
output root for each runtime:

- logs: `tmp/runtime_matrix_nanomiracl_en_20260509_1935/`
- results: `output/runtime_matrix_nanomiracl_en_20260509_1935/`

The runtime order was:

1. Transformers 4.x + Flash Attention 2 (`tf4-fa2`)
2. Transformers 5.x + SDPA (`tf5-sdpa`)
3. Transformers 4.x + SDPA (`tf4-sdpa`)
4. Transformers 4.x default attention (`tf4-default`)

Use the first successful runtime below unless a later note for a specific model
has been superseded by a newer validation.

| model | method | first successful runtime |
| --- | --- | --- |
| `BAAI/bge-m3` | dense | `tf5-sdpa` |
| `Qwen/Qwen3-Embedding-0.6B` | dense | `tf4-fa2` |
| `google/embeddinggemma-300m` | dense | `tf4-fa2` |
| `hotchpotch/bekko-embedding-pico-beta-unir-v7` | dense | `tf4-fa2` |
| `hotchpotch/bekko-embedding-small-beta-unir-v8` | dense | `tf4-fa2` |
| `intfloat/multilingual-e5-large` | dense | `tf5-sdpa` |
| `intfloat/multilingual-e5-small` | dense | `tf5-sdpa` |
| `jinaai/jina-embeddings-v5-text-nano` | dense | `tf4-fa2` |
| `jinaai/jina-embeddings-v5-text-small` | dense | `tf4-fa2` |
| `cl-nagoya/ruri-v3-30m` | dense | `tf4-fa2` |
| `cl-nagoya/ruri-v3-310m` | dense | `tf4-fa2` |
| `perplexity-ai/pplx-embed-v1-0.6b` | dense | `tf4-fa2` |
| `ibm-granite/granite-embedding-311m-multilingual-r2` | dense | `tf4-fa2` |
| `Snowflake/snowflake-arctic-embed-l-v2.0` | dense | `tf5-sdpa` |
| `Alibaba-NLP/gte-multilingual-base` | dense | `tf4-sdpa` |
| `codefuse-ai/F2LLM-v2-330M` | dense | `tf4-fa2` |
| `jinaai/jina-embeddings-v3` | dense | `tf4-default` |
| `Snowflake/snowflake-arctic-embed-m-v2.0` | dense | failed in all four requested runtimes |
| `HIT-TMG/KaLM-embedding-multilingual-mini-v1` | dense | `tf4-fa2` |
| `codefuse-ai/F2LLM-v2-160M` | dense | `tf4-fa2` |
| `Lajavaness/bilingual-embedding-base` | dense | `tf4-default` |
| `intfloat/multilingual-e5-base` | dense | `tf5-sdpa` |
| `ibm-granite/granite-embedding-278m-multilingual` | dense | `tf5-sdpa` |
| `codefuse-ai/F2LLM-v2-80M` | dense | `tf4-fa2` |
| `Lajavaness/bilingual-embedding-small` | dense | `tf4-default` |
| `ibm-granite/granite-embedding-107m-multilingual` | dense | `tf5-sdpa` |
| `sentence-transformers/static-similarity-mrl-multilingual-v1` | dense | `tf4-fa2` |
| `sentence-transformers/all-MiniLM-L6-v2` | dense | `tf5-sdpa` |
| `naver/splade-v3` | sparse | `tf5-sdpa` |
| `lightonai/ColBERT-Zero` | late-interaction | `tf5-sdpa` with `uv run --group pylate` |
| `hotchpotch/bekko-embedding-pico-beta-unir-v9-QAT-ftQAT` | dense | `tf4-fa2` |
| `hotchpotch/bekko-embedding-v1-a8m` | dense | `tf4-fa2` |
| `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | dense | `tf5-sdpa` |

## cl-nagoya/ruri-v3

Applies to:

- `cl-nagoya/ruri-v3-30m`
- `cl-nagoya/ruri-v3-310m`
- `cl-nagoya/ruri-v3-reranker-310m`

Use the retrieval prompts documented by the model card:

- query prompt: `検索クエリ: `
- document/corpus prompt: `検索文書: `

These prompts apply to the dense embedding checkpoints. The
`cl-nagoya/ruri-v3-reranker-310m` README documents direct CrossEncoder pair
scoring with `predict([[query, document], ...])` and `rank(query, documents)`;
do not add dense query/document prompt prefixes unless an official reranker
usage note is updated to require them.

Example:

```bash
uv run hakari-bench evaluate dense \
  --model cl-nagoya/ruri-v3-310m \
  --query-prompt '検索クエリ: ' \
  --document-prompt '検索文書: '
```

Runtime notes:

- Prefer Transformers 4.x with Flash Attention 2 for ruri-v3 unless a newer
  runtime has been revalidated for the exact model and task set.
- For `cl-nagoya/ruri-v3-reranker-310m`, use the `tf4-fa2` dependency group,
  `attn_implementation: flash_attention_2`, bf16, and the model's 8192 token
  maximum sequence length.
- In this project, `cl-nagoya/ruri-v3-310m` on NanoJMTEB/NanoJaqket produced
  abnormally low scores with `transformers==5.7.0` despite correct prompts.
  Re-running with `transformers==4.57.6` and Flash Attention 2 restored the
  expected current-dataset score.
- Do not shorten the model max sequence length to work around memory pressure.
  Reduce batch size first.

Historical comparison note:

- Older NanoJMTEB/NanoJaqket results around `nDCG@10 = 0.9426` were measured on
  the earlier q50 NanoJaqket data. Current NanoJMTEB uses q200 data, where
  `cl-nagoya/ruri-v3-310m` reproduced around `nDCG@10 = 0.8975` with
  Transformers 4.x + Flash Attention 2. Do not compare q50 and q200 scores as
  the same benchmark state.

## intfloat E5 And Multilingual E5

Applies to non-instruct E5 retrieval models, including:

- `intfloat/multilingual-e5-small`
- `intfloat/multilingual-e5-base`
- `intfloat/multilingual-e5-large`
- other non-instruct `intfloat/e5-*` models unless their model card says
  otherwise

Use the standard E5 retrieval prefixes:

- query prompt: `query: `
- document/corpus prompt: `passage: `

Example:

```bash
uv run hakari-bench evaluate dense \
  --model intfloat/multilingual-e5-base \
  --query-prompt 'query: ' \
  --document-prompt 'passage: '
```

Notes:

- Do not treat E5 instruct models as covered by this section. Instruct variants
  may require task-specific query instructions from their own model cards.
- Keep the prompts explicit in result metadata when re-running or comparing
  with older results.
- For `intfloat/multilingual-e5-large`, prefer SDPA over Flash Attention 2 until
  the FA2 path is revalidated. With `transformers==5.3.0`, `torch==2.9.0`, and
  `flash-attn==2.8.3`, NanoMIRACL/en scored lower with FA2 than SDPA despite the
  same prompts and model:

| attention | base | int8 | binary | int8_rescore | binary_rescore |
| --- | ---: | ---: | ---: | ---: | ---: |
| FA2 2.8.3 | 0.735197 | 0.742057 | 0.617535 | 0.735197 | 0.728762 |
| SDPA | 0.747493 | 0.743811 | 0.670783 | 0.743362 | 0.744807 |

Use:

```bash
uv run hakari-bench evaluate dense \
  --model intfloat/multilingual-e5-large \
  --attn-implementation sdpa \
  --query-prompt 'query: ' \
  --document-prompt 'passage: '
```

## Qwen Qwen3 Embedding

Applies to:

- `Qwen/Qwen3-Embedding-0.6B`
- `Qwen/Qwen3-Embedding-4B`

Use the Sentence Transformers prompt configuration:

- query prompt name: `query`
- document prompt name: `document`

The model card describes query-side instruction use as recommended for
retrieval. The stored `query` prompt is:

```text
Instruct: Given a web search query, retrieve relevant passages that answer the query
Query:
```

Example:

```bash
uv run hakari-bench evaluate dense \
  --model Qwen/Qwen3-Embedding-0.6B \
  --query-prompt-name query \
  --document-prompt-name document
```

When evaluating `Qwen/Qwen3-Embedding-4B` through TEI or another API backend
that does not load the Sentence Transformers prompt registry, pass the prompt
strings explicitly. Use the query instruction and no document prefix:

```bash
uv run hakari-bench evaluate dense \
  --model Qwen/Qwen3-Embedding-4B \
  --query-prompt $'Instruct: Given a web search query, retrieve relevant passages that answer the query\nQuery:' \
  --document-prompt ''
```

Truncation notes:

- The model supports user-defined embedding dimensions from 32 to 1024.
- Use `--embedding-variant truncate:768,512,256,128,64,32` when measuring
  dimensional trade-offs for `Qwen/Qwen3-Embedding-0.6B`.
- `Qwen/Qwen3-Embedding-4B` supports user-defined embedding dimensions from 32
  to 2560.
- Use `--embedding-variant truncate:2048,1536,1024,768,512,256,128,64,32`
  when measuring dimensional trade-offs for `Qwen/Qwen3-Embedding-4B`.

## Google EmbeddingGemma

Applies to:

- `google/embeddinggemma-300m`

Use the Sentence Transformers retrieval prompt names:

- query prompt name: `Retrieval-query`
- document prompt name: `Retrieval-document`

These map to the model card's retrieval prompt formats:

- query: `task: search result | query: `
- document: `title: none | text: `

Example:

```bash
uv run hakari-bench evaluate dense \
  --model google/embeddinggemma-300m \
  --query-prompt-name Retrieval-query \
  --document-prompt-name Retrieval-document
```

Truncation notes:

- The model has 768-dimensional base embeddings and documented Matryoshka
  dimensions of 512, 256, and 128.
- Use `--embedding-variant truncate:512,256,128` when measuring dimensional
  trade-offs.

## hotchpotch Bekko Embeddings

Applies to:

- `hotchpotch/bekko-embedding-pico-beta-unir-v7`
- `hotchpotch/bekko-embedding-small-beta-unir-v8`
- `hotchpotch/bekko-embedding-pico-beta-unir-v9-QAT-ftQAT`
- `hotchpotch/bekko-embedding-pico-beta-unir-v9-GOR`
- `hotchpotch/bekko-embedding-pico-beta-unir-v9-GOR-pt`
- `hotchpotch/bekko-embedding-v1-a8m`

Use the stored Sentence Transformers retrieval prompt names:

- query prompt name: `query`
- document prompt name: `passage`

These map to:

- query: `query: `
- passage: `passage: `

The configs also define `document` and `corpus` aliases that map to
`passage: `, but use `passage` for benchmark runs so metadata follows the
model card recommendation. Do not manually add `query: ` or `passage: ` when
using prompt names; that would apply the prefix twice.

Example:

```bash
uv run hakari-bench evaluate dense \
  --model hotchpotch/bekko-embedding-small-beta-unir-v8 \
  --query-prompt-name query \
  --document-prompt-name passage \
  --embedding-variant truncate:256,128,64
```

Truncation notes:

- `hotchpotch/bekko-embedding-pico-beta-unir-v7` documents base dim 384 and
  Matryoshka dims `256,128,64`.
- `hotchpotch/bekko-embedding-small-beta-unir-v8` documents base dim 384 and
  Matryoshka dims `256,128,64`.
- `hotchpotch/bekko-embedding-pico-beta-unir-v9-QAT-ftQAT` documents supported
  Matryoshka dims `256,128,64` below its 384-dimensional base embeddings.
- `hotchpotch/bekko-embedding-pico-beta-unir-v9-GOR` documents supported
  Matryoshka dims `256,128,64` below its 384-dimensional base embeddings.
- `hotchpotch/bekko-embedding-pico-beta-unir-v9-GOR-pt` recommends
  `truncate_dim` values `256,128,64`.
- `hotchpotch/bekko-embedding-v1-a8m` documents supported `truncate_dim`
  values `256,128,64` below its 384-dimensional base embeddings. Use
  Transformers 4.x with Flash Attention 2 and batch size 16 unless a newer
  validation supersedes the model card.

## Jina Embeddings v5

Applies to:

- `jinaai/jina-embeddings-v5-text-nano`
- `jinaai/jina-embeddings-v5-text-small`

Use remote code, retrieval encode tasks, and the stored retrieval prompt names:

- `--trust-remote-code`
- query encode task: `retrieval`
- document encode task: `retrieval`
- query prompt name: `query`
- document prompt name: `document`

These prompt names map to:

- query: `Query: `
- document: `Document: `

Example:

```bash
uv run hakari-bench evaluate dense \
  --model jinaai/jina-embeddings-v5-text-small \
  --trust-remote-code \
  --query-encode-task retrieval \
  --document-encode-task retrieval \
  --query-prompt-name query \
  --document-prompt-name document
```

Without the explicit retrieval encode task, the custom module can reject
Sentence Transformers' default `query` task with:
`Invalid task: query. Must be one of ['retrieval', 'text-matching',
'clustering', 'classification']`.

Truncation notes:

- `jinaai/jina-embeddings-v5-text-nano` supports Matryoshka dimensions
  512, 256, 128, 64, and 32 in addition to its 768-dimensional base output.
- `jinaai/jina-embeddings-v5-text-small` supports Matryoshka dimensions
  768, 512, 256, 128, 64, and 32 in addition to its 1024-dimensional base
  output.
- Use the matching `--embedding-variant truncate:...` list when measuring
  dimensional trade-offs.

## Jina Embeddings v3

Applies to:

- `jinaai/jina-embeddings-v3`

The model card and Sentence Transformers config define retrieval-specific
tasks and prompt names:

- query encode task: `retrieval.query`
- document encode task: `retrieval.passage`
- query prompt name: `retrieval.query`
- document prompt name: `retrieval.passage`
- `--trust-remote-code`

The prompts map to:

- query: `Represent the query for retrieving evidence documents: `
- document: `Represent the document for retrieval: `

Example:

```bash
uv run hakari-bench evaluate dense \
  --model jinaai/jina-embeddings-v3 \
  --trust-remote-code \
  --query-encode-task retrieval.query \
  --document-encode-task retrieval.passage \
  --query-prompt-name retrieval.query \
  --document-prompt-name retrieval.passage
```

Truncation notes:

- The model card documents Matryoshka dimensions
  768, 512, 256, 128, 64, and 32 in addition to the 1024-dimensional base
  output.

Compatibility notes:

- On NanoMIRACL/en, this model succeeded with Transformers 4.x default
  attention after failing with `tf4-fa2`, `tf5-sdpa`, and `tf4-sdpa`.
- Do not pass an attention override for this model unless that runtime has been
  revalidated.

## Snowflake Arctic Embed v2

Applies to:

- `Snowflake/snowflake-arctic-embed-l-v2.0`
- `Snowflake/snowflake-arctic-embed-m-v2.0`

Use the stored query prompt name:

- query prompt name: `query`
- no document prompt

The query prompt maps to `query: `.

Example:

```bash
uv run hakari-bench evaluate dense \
  --model Snowflake/snowflake-arctic-embed-l-v2.0 \
  --query-prompt-name query
```

Truncation notes:

- The v2 model card documents 256-dimensional MRL.
- Use `--embedding-variant truncate:256` when measuring dimensional trade-offs.

Compatibility notes:

- `Snowflake/snowflake-arctic-embed-m-v2.0` requires `--trust-remote-code` in
  this environment.
- `Snowflake/snowflake-arctic-embed-l-v2.0` succeeded on NanoMIRACL/en with
  `tf5-sdpa` in the 2026-05-09 runtime matrix.
- `Snowflake/snowflake-arctic-embed-m-v2.0` failed in all four requested
  runtimes (`tf4-fa2`, `tf5-sdpa`, `tf4-sdpa`, `tf4-default`). The immediate
  failure was `please install xformers` after the remote code forced eager
  attention because `use_memory_efficient_attention=true`.
- A prior same-day check with `xformers` installed reached CUDA index
  assertions even with `--model-max-seq-length 8192`; do not treat the medium
  checkpoint as verified until a working runtime is revalidated.

## IBM Granite Embeddings

Applies to:

- `ibm-granite/granite-embedding-311m-multilingual-r2`
- `ibm-granite/granite-embedding-97m-multilingual-r2`
- `ibm-granite/granite-embedding-278m-multilingual`
- `ibm-granite/granite-embedding-107m-multilingual`

No non-empty retrieval prompts were found in the Sentence Transformers configs
used for these checkpoints. Preserve the model default behavior unless the model
card changes.

Truncation notes:

- `ibm-granite/granite-embedding-311m-multilingual-r2` documents Matryoshka
  dimensions of 512, 384, 256, and 128 in addition to its 768-dimensional base
  output.
- Use `--embedding-variant truncate:512,384,256,128` for that R2 checkpoint when
  measuring dimensional trade-offs.
- `ibm-granite/granite-embedding-97m-multilingual-r2` has a 384-dimensional
  base output and does not document Matryoshka dimensions. Do not add truncation
  variants unless a newer model card documents them.
- Do not assume Matryoshka support for the older 278M and 107M multilingual
  checkpoints.

## CodeFuse F2LLM v2

Applies to:

- `codefuse-ai/F2LLM-v2-80M`
- `codefuse-ai/F2LLM-v2-160M`
- `codefuse-ai/F2LLM-v2-330M`

Use the stored Sentence Transformers prompt names:

- query prompt name: `query`
- document prompt name: `document`

The query prompt maps to:

```text
Instruct: Given a question, retrieve passages that can help answer the question.
Query:
```

Example:

```bash
uv run hakari-bench evaluate dense \
  --model codefuse-ai/F2LLM-v2-330M \
  --query-prompt-name query \
  --document-prompt-name document
```

No Matryoshka/truncate dimensions were found in the model cards or Sentence
Transformers configs checked for these models.

## Perplexity pplx Embed

Applies to:

- `perplexity-ai/pplx-embed-v1-0.6b`

Use:

- `--trust-remote-code`

Example:

```bash
uv run hakari-bench evaluate dense \
  --model perplexity-ai/pplx-embed-v1-0.6b \
  --trust-remote-code
```

No model-specific prompt or Matryoshka/truncate dimensions were found in the
files checked for this model.

## Alibaba GTE Multilingual Base

Applies to:

- `Alibaba-NLP/gte-multilingual-base`

Use:

- `--trust-remote-code`

Compatibility notes:

- The Sentence Transformers config sets `max_seq_length` to 8192.
- On NanoMIRACL/en, this model succeeded with `tf4-sdpa` after failing with
  `tf4-fa2` and `tf5-sdpa`.

## Lajavaness Bilingual Embeddings

Applies to:

- `Lajavaness/bilingual-embedding-base`
- `Lajavaness/bilingual-embedding-small`

Use:

- `--trust-remote-code`

Compatibility notes:

- In this project environment with Transformers 5.x, loading failed because the
  custom code imports `transformers.onnx`, which is unavailable.
- On NanoMIRACL/en, both checkpoints succeeded with Transformers 4.x default
  attention after failing with `tf4-fa2`, `tf5-sdpa`, and `tf4-sdpa`.
- Do not pass an attention override for these models unless that runtime has
  been revalidated.

## naver SPLADE v3

Applies to:

- `naver/splade-v3`

Use the sparse evaluator:

```bash
uv run hakari-bench evaluate sparse \
  --model naver/splade-v3
```

No non-empty query/document prompts were found in the Sentence Transformers
SparseEncoder config.

## hotchpotch Japanese SPLADE v2

Applies to:

- `hotchpotch/japanese-splade-v2`

Use the sparse evaluator:

```bash
uv run --extra wordseg hakari-bench evaluate sparse \
  --model hotchpotch/japanese-splade-v2
```

The model can be loaded by Sentence Transformers `SparseEncoder`, which detects
the `BertForMaskedLM` architecture and uses `SpladePooling(pooling_strategy="max")`.
The Hugging Face repository does not currently include SentenceTransformers
SparseEncoder metadata such as `modules.json` or `1_SpladePooling/config.json`,
so loading relies on this default fallback.

The tokenizer is `BertJapaneseTokenizer` with MeCab/fugashi and `unidic-lite`.
Those Japanese tokenizer libraries must be installed before `SparseEncoder`
loads the model. In this repository, `uv run --extra wordseg ...` enables the
optional dependency set that includes them; the important requirement is the
Japanese tokenizer libraries themselves, not BM25 word segmentation behavior.

Long-document tasks can pass very large raw strings to the Japanese tokenizer.
In the 2026-06 all-dataset run, `BertJapaneseTokenizer` with fugashi/MeCab hit
a native crash on NanoBRIGHT before Hugging Face tokenizer truncation could
apply `max_seq_length=512`. For full benchmark sweeps, use the compatibility
loader below. It still constructs a Sentence Transformers `SparseEncoder`, but
applies a raw character guard before query/document tokenization:

```bash
PYTHONPATH=$PWD uv run --extra wordseg hakari-bench evaluate sparse \
  --model hotchpotch/japanese-splade-v2 \
  --model-revision d1a16eef4748042285d5471f9203cdeb448d48bc \
  --model-loader hakari_bench.model_loaders:load_safe_japanese_sparse_encoder \
  --model-loader-kwargs-json '{"max_input_chars":8192}'
```

No non-empty query/document prompts were found in the SparseEncoder fallback
configuration. Use `similarity_fn_name=dot`, `max_seq_length=512`, `dtype=bf16`,
and `--attn-implementation sdpa`.

## ColBERT Late-Interaction Models

Applies to:

- `lightonai/ColBERT-Zero`
- `lightonai/GTE-ModernColBERT-v1`
- `answerdotai/answerai-colbert-small-v1`
- `colbert-ir/colbertv2.0`
- `mixedbread-ai/mxbai-edge-colbert-v0-17m`

Use the late-interaction evaluator and the model-specific settings stored in
`config/model_cards/`. These are model optimization options only: prompt names,
prefixes, dtype, attention implementation, and ColBERT query/document token
lengths. Do not record candidate ranking, reranking top-K, or other benchmark
protocol settings as model defaults.

The current best NanoBEIR-en options measured in this repository are:

| Model | Runtime | Prompts | Prefixes | Query/document length | Expansion attention | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `lightonai/ColBERT-Zero` | `fp32`, `sdpa`; best reproduced with Transformers 4.48.3 + PyLate 1.3.4 | `query_prompt_name=query`, `document_prompt_name=document` | `[Q] ` / `[D] ` | `39` / `519` | `false` | Required to avoid the no-prompt regression. |
| `lightonai/GTE-ModernColBERT-v1` | `fp32`, `sdpa`; best reproduced with Transformers 4.48.3 + PyLate 1.3.4 | none | `[Q] ` / `[D] ` | `48` / `512` | `false` | Do not enable expansion-token attention; it regressed NanoBEIR-en. |
| `answerdotai/answerai-colbert-small-v1` | `fp32`, `sdpa` | none | `[unused0]` / `[unused1]` | `48` / `512` | n/a | fp32 was only marginally better than the existing bf16 result. |
| `colbert-ir/colbertv2.0` | `bf16`, `sdpa` | none | `[unused0]` / `[unused1]` | `32` / `512` | `false` | Required for the Stanford ColBERT marker-token path; the fallback adapter inserts these as token IDs after CLS. |
| `mixedbread-ai/mxbai-edge-colbert-v0-17m` | `fp32`, `sdpa` | none | `[Q] ` / `[D] ` | `40` / `512` | `false` | README/PyLate config defaults are q48/d512/no expansion; NanoBEIR-en primary exact score improved with q40/d512 over the default query length while keeping document length at 512. |
| `mixedbread-ai/mxbai-edge-colbert-v0-32m` | `fp32`, `sdpa` | none | `[Q] ` / `[D] ` | `40` / `512` | `false` | Evaluated with the same optimized mxbai-edge ColBERT option as the 17m checkpoint for apples-to-apples full Nano-set coverage. |

Example for the highest-scoring ColBERT-Zero option:

```bash
uv run --group pylate hakari-bench evaluate late-interaction \
  --model lightonai/ColBERT-Zero \
  --query-prompt-name query \
  --document-prompt-name document \
  --late-interaction-query-prefix '[Q] ' \
  --late-interaction-document-prefix '[D] ' \
  --late-interaction-query-length 39 \
  --late-interaction-document-length 519
```

For reviewed cards, prefer:

```bash
uv run --group pylate hakari-bench evaluate from-model-card \
  --model-card config/model_cards/lightonai__ColBERT-Zero.yaml
```

Use the matching card for the other ColBERT models. The card applies the model
options above; select benchmark protocol options such as candidate ranking and
rerank depth separately when a run explicitly requires them.

Compatibility notes:

- This repository keeps PyLate behind the `pylate` dependency group, so use
  `uv run --group pylate ...` for these models unless using a dedicated
  compatibility environment.
- ColBERT-Zero and GTE-ModernColBERT-v1 scored best in the local NanoBEIR-en
  sweep under a Transformers 4.48.3 + PyLate 1.3.4 compatibility environment.
  Torch was not pinned for that comparison.
- The local evaluator aliases PyLate's renamed `_input_length` helper to
  `_text_length` before encoding. With that compatibility shim, NanoMIRACL/en
  succeeded with `tf5-sdpa`.

## OpenAI Embedding Models

Applies to:

- `text-embedding-3-small`
- `text-embedding-3-large`

Use the built-in OpenAI dense loader:

```bash
uv run --group openai hakari-bench evaluate dense \
  --model text-embedding-3-small \
  --model-loader openai
```

Operational notes:

- Store `OPENAI_API_KEY` in `.env`; `.env.sample` is committed as the template.
- The adapter uses `AsyncOpenAI` internally. Set
  `--model-loader-kwargs-json '{"max_concurrency":8}'` to control in-flight
  embeddings requests.
- `--truncate-dim` and `--embedding-variant truncate:DIM` use full OpenAI
  embeddings followed by `full[:DIM]` and L2 normalization. This is very close to
  API-side `dimensions`, but not bit-identical, and avoids extra API calls for
  each truncation condition.
- The OpenAI adapter token-truncates inputs above 8100 counted tokens by default,
  leaving headroom below the provider's 8192-token hard limit; set
  `--model-loader-kwargs-json '{"truncate_input_tokens":false}'` to fail
  instead.
- Attention implementation, dtype, device, and multi-process encode devices do
  not apply to this hosted API backend.
- See `docs/openai_embedding_evaluation.md` for the API-vs-local dimension
  check and the cost-estimation workflow.

## Sentence Transformers Static Similarity MRL

Applies to:

- `sentence-transformers/static-similarity-mrl-multilingual-v1`

The model card says this model is not intended for retrieval use cases, even
though it can be evaluated as a dense Sentence Transformers model. Keep that
limitation visible when reporting retrieval scores.

Truncation notes:

- The model card documents Matryoshka support.
- Use `--embedding-variant truncate:512,256,128,64,32` when measuring
  dimensional trade-offs.

## Sentence Transformers MiniLM and LaBSE max length

Applies to:

- `sentence-transformers/all-MiniLM-L12-v2`
- `sentence-transformers/LaBSE`
- `sentence-transformers/all-MiniLM-L6-v2`
- `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`

These models advertise shorter Sentence Transformers defaults in
`sentence_bert_config.json` for some repositories, even though their underlying
Transformer configs and tokenizers support roughly 512-token inputs. Keep the
model cards on the documented Sentence Transformers max sequence length for
benchmark-comparable runs:

```bash
uv run hakari-bench evaluate from-model-card \
  --model-card config/model_cards/sentence-transformers__all-MiniLM-L12-v2.yaml \
  --all \
  --dtype bf16 \
  --attn-implementation sdpa
```

Use the matching model card for the other Sentence Transformers models. A
2026-06-24 512-token override sweep confirmed that these repositories can
execute with 512-token inputs, but retrieval quality dropped relative to the
documented Sentence Transformers lengths. A follow-up rerun at the documented
lengths reproduced the remote DuckDB scores with only small numerical drift.
