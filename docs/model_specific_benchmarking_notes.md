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

## Mixedbread Rerank v2

Applies to `mixedbread-ai/mxbai-rerank-base-v2` and
`mixedbread-ai/mxbai-rerank-large-v2`.

Use bf16 and Transformers 4.x with Flash Attention 2, following the
[author's runtime preference](https://github.com/mixedbread-ai/mxbai-rerank).
Both checkpoints support 32768 input tokens. Keep that context limit;
reduce the batch size or padded token budget for memory pressure.
The upstream Sentence Transformers modules supply the query/document chat
template and the `1` minus `0` logit score. Do not add embedding prompts.

Use the compatibility loader for long-document benchmarks:

```bash
uv run --group tf4-fa2 hakari-bench evaluate reranker \
  --model mixedbread-ai/mxbai-rerank-base-v2 \
  --model-revision 3ea9d4dffa7d12a4f366be8e275c349de9fc9865 \
  --model-loader hakari_bench.model_loaders:load_mxbai_rerank_v2 \
  --model-loader-kwargs-json '{"max_batch_tokens":131072}' \
  --dtype bf16 --flash-attn2 --device cuda:0 --batch-size 32 --all
```

For large, use model revision `ca7e1ee484c37c0ddd8d178a9a5c33cec575c5e6`.
When using `evaluate from-model-card`, also pass the compatibility loader
explicitly; model cards currently do not select custom Python loaders.

The standard CrossEncoder path in Sentence Transformers 5.4.1 truncates the
rendered chat from the right. On oversized pairs this discards the final
relevance instruction and assistant marker, silently scoring document
continuation instead of relevance. The loader reserves the checkpoint's
suffix, following the
[official input construction](https://github.com/mixedbread-ai/mxbai-rerank/blob/main/mxbai_rerank/mxbai_rerank_v2.py).
Inputs that fit retain the native template and token IDs. Oversized queries
are limited to three quarters of the content budget to leave document space.
This policy is recorded in backend metadata, including per-task truncation
and OOM retry counts.

The loader also computes only final-token logits, disables the KV cache,
limits each batch by its padded token count, and halves batches on CUDA OOM.
An individual pair that still fails is reported as an error.
It never applies a raw character limit. Long inputs occur in NanoLongEmbed,
NanoBRIGHT, NanoMLDR, legal tasks, and several other datasets.

Validation on two RTX 5090 GPUs confirmed bf16 execution for both models on
real NanoNarrativeQA, NanoBrightStackoverflowLong, and NanoMLDR/en samples,
including 32768-token inputs. Short-input scores matched the native
CrossEncoder exactly within each runtime. A four-pair 32768-token synthetic
batch used about 5.8 GB for base and 11.8 GB for large with bf16 SDPA.
The diagnostic fp32 SDPA run exceeded 32 GB on a single long pair, so fp32
is not the fallback for this wave.

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

## GeeVec Embeddings 1.0 Lite

For `geevec-ai/geevec-embeddings-1.0-lite`, use the upstream default
`general` domain for both queries and documents. The full evaluation uses
BF16, Flash Attention 2, cosine similarity, and last-token pooling at revision
`3c6073ded5dbe6eda5e8caed080400c61d5476b3`.

The checkpoint has no configured SentenceTransformers prompts. Set the query
prompt explicitly to `Instruct: Given a question, retrieve passages that answer
the question.\nQuery: `, with an actual newline before `Query: `, and leave
documents unprefixed. Evaluate the native 4096 dimensions and the documented
2048, 1024, 512, and 256 truncations, including the standard quantization and
rescore variants at every dimension.

Retain the shipped SentenceTransformers maximum sequence length of 40960.
The upstream README advertises a 32768-token context; this discrepancy is
intentional in the recorded evaluation settings, which preserve the loaded
checkpoint configuration. Start with batch size 16 and use batch size 1 for
long-document tasks. The full 563-task run completed without OOM using batch
16 for 512 tasks and batch 1 for 51 tasks.

References: the pinned [model card](https://huggingface.co/geevec-ai/geevec-embeddings-1.0-lite/blob/3c6073ded5dbe6eda5e8caed080400c61d5476b3/README.md)
and the reviewed HAKARI model card under `config/model_cards/`.

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

## Octen Embedding

Applies to:

- `Octen/Octen-Embedding-0.6B` (revision
  `b54faa2ba2ae9eb618f88526cec6dae3287eb5f8`)
- `Octen/Octen-Embedding-8B` (revision
  `88695e4f8ed87b4ce08df2fea6ff25bfe0f9875b`)

Both are Qwen3-Embedding derivatives. Use the shipped Sentence Transformers
prompt names `query` and `document`. The query prompt is the Qwen3 web-search
instruction. The document prompt is a single space, which matches the official
MTEB wrapper. The MTEB wrapper uses RTEB-only task prompts; HAKARI follows the
built-in prompts, as for Qwen3-Embedding.

```bash
uv run hakari-bench evaluate from-model-card \
  --model-card config/model_cards/Octen__Octen-Embedding-8B.yaml \
  --all --batch-size 8 --device cuda:0
```

Runtime notes:

- BF16 with FlashAttention 2. FlashAttention 2 and SDPA embeddings matched
  within 0.003, and manual last-token pooling matched Sentence Transformers
  within 0.005. Neither model documents MRL dimensions, so runs cover the base
  embedding plus the default int8, binary, and rescore variants.
- 0.6B keeps the native 32768-token Sentence Transformers maximum. MTEB caps
  inference at 18480 tokens. Its weights and configs are identical to the
  MTEB-pinned revision `1a00a4e8`; only the README differs.
- 8B uses 40960 tokens, from the README details and config. The README
  model-list table says 32768. The weights were updated on 2026-01-06, after
  the MTEB-pinned revision `2030603c`.
- The 8B README Known Issues section suggests a `"- "` prefix for unprefixed
  documents. The shipped config and the MTEB wrapper use `" "`, which HAKARI
  follows. In validation, `"- "` changed similarities by at most 0.031.
- Batch size was reduced, down to 1, for long tasks and on OOM. The context was
  never shortened.

## Qwen Qwen3 Reranker

Applies to `Qwen/Qwen3-Reranker-0.6B` and `Qwen/Qwen3-Reranker-4B`.

The upstream Sentence Transformers configuration is a CrossEncoder with the
default prompt name `query` (`Given a web search query, retrieve relevant
passages that answer the query`), a chat template, and a `LogitScore` module
that returns `logit("yes") - logit("no")` at the last position (token IDs
9693 and 2152) with no activation. Do not add other prompts. Both checkpoints
support 40960 tokens; keep that limit.

`Qwen/Qwen3-Reranker-0.6B` was published from the native CrossEncoder in bf16
with Flash Attention 2. Most of its task files used
`HAKARI_RERANKER_DOCUMENT_MAX_CHARS=20000`, which is recorded in each result.

### Qwen3-Reranker-4B through vLLM FP8

`Qwen/Qwen3-Reranker-4B` is evaluated through a vLLM server with dynamic FP8
weights (`--quantization fp8`, bf16 activations), because the native bf16
CrossEncoder needs several GPU-days for the full task set. Validation below
shows the FP8 scores stay close to bf16. Results keep the logical model ID
`Qwen/Qwen3-Reranker-4B` and record the backend under `model.backend_metadata`
(`backend_library: vllm`, server version, served checkpoint, and launch flags).

1. Convert the CausalLM checkpoint into a one-label SequenceClassification
   checkpoint whose head is `lm_head["yes"] - lm_head["no"]`. Since
   `logits = norm(h) @ lm_head.T`, the head returns the same score from the
   same final hidden state, so vLLM can serve it as a last-token classifier:

   ```bash
   uv run python scripts/convert_qwen3_reranker_seqcls.py Qwen/Qwen3-Reranker-4B \
     output/models/Qwen3-Reranker-4B-seqcls \
     --revision 22e683669bc0f0bd69640a1354a6d0aebcfeede5
   ```

   The script reads `lm_head`, so untied checkpoints such as
   Qwen3-Reranker-8B also convert correctly.

2. Start one server per GPU from a separate environment with
   `vllm==0.33.0`:

   ```bash
   CUDA_VISIBLE_DEVICES=0 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
   vllm serve output/models/Qwen3-Reranker-4B-seqcls \
     --served-model-name Qwen3-Reranker-4B-seqcls-fp8 \
     --runner pooling --quantization fp8 --dtype bfloat16 \
     --max-model-len 40960 --max-num-batched-tokens 32768 --max-num-seqs 256 \
     --gpu-memory-utilization 0.70 --seed 0 \
     --pooler-config '{"seq_pooling_type":"LAST","use_activation":false}' \
     --host 127.0.0.1 --port 8100
   ```

   Chunked prefill is enabled, so 40960-token inputs fit in 32768-token
   scheduler steps. On an RTX 5090 this leaves about 108k KV-cache tokens,
   enough for two full-length inputs at once. Peak use was a steady 24.0 GB
   while scoring 100-candidate queries from NanoNarrativeQA and
   NanoBrightStackoverflowLong, where up to 175 pairs were truncated at
   40960 tokens. The FP8 path uses more activation memory than vLLM profiles.
   With `--max-num-batched-tokens 65536 --gpu-memory-utilization 0.90`, the
   engine ran out of memory on long NanoLongEmbed pairs and the server exited.
   At 0.80, a server grew to 31.6 GB and logged an allocator OOM retry.

3. Evaluate with the vLLM reranker client:

   ```bash
   uv run hakari-bench evaluate reranker \
     --model Qwen/Qwen3-Reranker-4B \
     --model-revision 22e683669bc0f0bd69640a1354a6d0aebcfeede5 \
     --model-loader hakari_bench.vllm_reranker:load_model \
     --model-loader-kwargs-json '{"endpoint":"http://127.0.0.1:8100","served_model":"Qwen3-Reranker-4B-seqcls-fp8","server_launch":{"quantization":"fp8"}}' \
     --trust-remote-code --batch-size 1024 --all
   ```

   `--model` names the original checkpoint. The client loads its tokenizer,
   chat template, and Sentence Transformers prompt from there, and counts
   parameters from a meta-device copy of the model. Pass the launch flags in
   `server_launch`, because the server does not report its quantization. Use a
   batch size of at least the candidate count so each query is one `predict`
   call. The client splits requests by `max_request_tokens` (default 262144)
   and sends `concurrency` (default 4) requests in parallel.

Long inputs: the client renders each pair with the checkpoint chat template
and tokenizes it locally, then sends token IDs, so the server never truncates
or re-templates. Pairs within 40960 tokens are token-identical to the native
CrossEncoder. Longer pairs are handled differently on purpose. The CrossEncoder
truncates the rendered chat from the right, which removes the
`<|im_end|>`/assistant suffix that the yes/no score is read from (the same
failure as in Mixedbread Rerank v2). The client keeps the template prefix,
instruction, query, and suffix, and truncates only the document tail. This
follows the
[official Qwen3-Reranker input construction](https://huggingface.co/Qwen/Qwen3-Reranker-4B).
An oversized query is limited to three quarters of the content budget. No
character limit is applied. Per-task `truncated_pairs`, `truncated_queries`,
and `max_input_tokens` are recorded in backend metadata.

Validation (2026-11-14, RTX 5090, `tmp/vllm-qwen3rr/validate.py`) used 1303
real candidate pairs from NanoJMTEB-v2/mintaka_ja, NanoMIRACL/ar,
NanoBEIR-ar/hotpotqa, and NanoCoIR/NanoCosQA:

| Comparison | Pearson | Mean abs diff / std | Top-1 agreement per query |
| --- | ---: | ---: | ---: |
| Client token IDs vs CrossEncoder preprocessing | 0 mismatches | | |
| vLLM bf16 vs CrossEncoder bf16 | 0.99978 | 0.016 | 13/13 |
| vLLM FP8 vs CrossEncoder bf16 | 0.99596 | 0.068 | 13/13 |
| vLLM FP8 vs vLLM bf16, 48 long NanoNarrativeQA/NanoMLDR-en pairs (25 truncated to 40960 tokens) | 0.99024 | 0.130 | 4/4 |

The vLLM FP8 path scored the short pairs about 4.7x faster than the bf16
CrossEncoder. On the first three tasks, nDCG@10 for FP8 versus the native bf16
CrossEncoder was 0.6091 versus 0.6149 on mintaka_ja, 0.7600 versus 0.7644 on
mintaka_es, and 0.7192 versus 0.7164 on mintaka_fr, at 20 s versus 130 s per
task.

Full-run comparison (2026-11-17) on the 196 tasks that the earlier native bf16
CrossEncoder run completed: mean nDCG@10 was 0.7647 (bf16) versus 0.7645
(FP8), a mean delta of -0.0002 and a mean absolute delta of 0.0059. 124 tasks
moved by at most 0.005 and 166 by at most 0.01. On those tasks FP8 took 8.5
GPU-hours versus 37.6 for bf16 (4.4x in aggregate, 6.1x median per task).
All 563 FP8 tasks took 122.7 GPU-hours on two RTX 5090s. NanoNarrativeQA
alone took 22.2 hours: 17158 of its 20011 pairs were truncated to 40960
tokens.

The largest per-task deltas were rechecked through an unquantized vLLM bf16
server (same SeqCls checkpoint and client, `--quantization` omitted) to
separate quantization from the serving path:

| Task | CrossEncoder bf16 | vLLM bf16 | vLLM FP8 |
| --- | ---: | ---: | ---: |
| NanoMMTEB-v2/spart_qa | 0.2426 | 0.2477 | 0.3041 |
| NanoRARb/NanoSpartQA | 0.2514 | 0.2612 | 0.3126 |
| NanoBEIR-th/msmarco | 0.5843 | 0.5715 | 0.5453 |
| NanoBEIR-sr/msmarco | 0.5044 | 0.4862 | 0.4679 |
| NanoBEIR-ar/msmarco | 0.4622 | 0.4705 | 0.4951 |
| NanoBEIR-sv/msmarco | 0.5386 | 0.5312 | 0.5666 |
| NanoBEIR-it/msmarco | 0.5545 | 0.5789 | 0.5799 |

vLLM bf16 stays near the CrossEncoder on SpartQA, so the about +0.06 SpartQA
gain comes from FP8 rounding and not from templating or truncation. SpartQA
is a low-scoring spatial-reasoning task whose candidates score close
together, so small score perturbations reorder the top 10 (FP8 kept 8.6 of the
bf16 top-10 documents per query on average). The NanoBEIR msmarco splits have
few relevant documents per query and move by up to 0.024 even between the two
bf16 paths, so their deltas are mostly ranking noise.

The client resends a `/classify` request up to three times on
`urllib3.exceptions.ProtocolError`. Tokenizing a long query's candidates can
leave a pooled connection idle past the server keep-alive, and the next
request then fails with `RemoteDisconnected` (seen once, on a NanoLongEmbed
task). The request is not processed when the connection drops, so a resend
only repeats it.

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

## Google EmbeddingGemma 2

The reviewed card is
[`google__embeddinggemma-2.yaml`](../config/model_cards/google__embeddinggemma-2.yaml).
It pins revision `914f7f89142e33e77833254d9c9b90c3cef7303b`, the
`SearchQuery` / `Document` prompts, bf16, SDPA, an 8192-token context, and
128/256/512-dimensional truncation below the native 768-dimensional output.
The official [model card](https://huggingface.co/google/embeddinggemma-2)
documents text-only encoder loading and the supported context. The published
tokenizer instead contains an effectively unlimited length sentinel, so set
the documented context explicitly. SDPA is supported by the official
Transformers implementation; the model card does not prescribe an attention
backend.

The completed FlexAttention evaluation uses SentenceTransformers 6.1.0 and
Transformers 5.19.0.dev0 from commit
`a96730c8c97b8efbf35bbaf7f5da33ec99231a49`, torch 2.14.1 / CUDA 13.0 and
Python 3.12. SDPA was used for the earlier diagnostic runs.
Transformers 5.18.0 did not recognize the architecture.
Use a dedicated environment with model support; these notes do not change the
project's dependency requirements or lockfile.

For text retrieval, omit vision and audio encoders using
`config_kwargs={"vision_config": None, "audio_config": None}`. The measured
text embedding encoder has 271,002,624 total/trainable parameters and
134,217,728 input embedding parameters. HAKARI's active parameter convention
counts the text path only (total minus input embedding and non-text
parameters), giving 136,784,896 active parameters. The vision and audio
encoders are not loaded, so they are outside these counts.

SentenceTransformers 6.1.0 can classify strings resembling media URLs as image
or video inputs even when the benchmark supplies text. Restrict its input
formatter to text for this IR benchmark. The default `from-model-card` loader
does not apply selective encoder loading or this restriction; use a custom
loader with `evaluate dense`. Save the following as
`tmp/embeddinggemma2_text_loader.py` in the checkout:

```python
from sentence_transformers import SentenceTransformer
from hakari_bench.models import resolve_torch_dtype


def load_model(config):
    model = SentenceTransformer(
        config.model_name_or_path,
        revision=config.model_revision,
        device=config.device,
        config_kwargs={"vision_config": None, "audio_config": None},
        model_kwargs={
            "torch_dtype": resolve_torch_dtype(config.dtype),
            "attn_implementation": config.attn_implementation or "sdpa",
        },
    )
    if config.max_seq_length is not None:
        model.max_seq_length = config.max_seq_length
    model[0].input_formatter.supported_modalities = ["text"]
    return model
```

With the dedicated environment activated, run:

```bash
CUDA_VISIBLE_DEVICES=1 PYTHONPATH=tmp uv run --no-project python -c \
  'from hakari_bench.cli import main; main()' evaluate dense \
  --model google/embeddinggemma-2 \
  --model-revision 914f7f89142e33e77833254d9c9b90c3cef7303b \
  --model-loader embeddinggemma2_text_loader:load_model \
  --model-loader-kwargs-json '{"config_kwargs":{"vision_config":null,"audio_config":null},"input_modalities":["text"]}' \
  --all --dtype bf16 --attn-implementation sdpa \
  --device cuda:0 --batch-size 16 --model-max-seq-length 8192 \
  --query-prompt-name SearchQuery --document-prompt-name Document \
  --embedding-variant truncate:128,256,512
```

The recorded loader kwargs describe the fixed text-only settings used by this
loader. All 20 base/truncation/quantization/rescore conditions are evaluated
from a single encoding pass per task.

The initial submission to
[Results Dataset PR #43](https://huggingface.co/datasets/hakari-bench/results/discussions/43)
contained 563 task files. The first 561 tasks loaded the full checkpoint and used
text inputs; `touche2020_vn` and `treccovid_vn` were resumed with the text-only
loader after a YouTube URL triggered video loading. CPU float32 checks found
identical full-versus-text-only embeddings for English, Japanese, and code
samples, and confirmed URL strings matched explicit text inputs. Parameter
metadata was regenerated to report text encoder size for all submitted results;
scores, timings, and original runtime configuration were preserved with
regeneration provenance. All 563 tasks have the same 20 conditions.

An independent runtime audit subsequently found that the original runner's
redundant global bf16 cast also rounded FP32 RoPE frequency buffers retained by
the official loader. This changed embeddings and task rankings. The loader now
skips that cast when floating parameters already have the requested dtype,
preserving those buffers. The original 561 full-checkpoint task results were
invalidated by this audit; the two resumed tasks used a custom loader that
bypassed the redundant cast. Equivalent full-versus-text-only CPU embeddings
do not validate this separate bf16 issue. The complete replacement evaluates all 563 standard tasks and six extended
NanoDAPFAM FullText tasks with text-only loading and FlexAttention. All 569
tasks have 20 embedding conditions and use the original pinned dataset revisions.
The 550-task standard Overall excludes the six extended FullText tasks; their
scores are reported separately in PR #43. Original local SDPA results remain
available separately.

### FlexAttention reproduction

The completed run used an RTX PRO 6000 Blackwell Max-Q (SM120). Default Flex
kernel tiles exceeded its shared-memory limit; the following Triton options
were validated: `BLOCK_M=16`, `BLOCK_N=32`, `num_stages=1`, `num_warps=4`,
`BACKEND=TRITON`. Save this wrapper as `tmp/embeddinggemma2_flex_loader.py`
alongside the text-only loader above:

```python
import torch

from embeddinggemma2_text_loader import load_model as load_text_model


def load_model(config):
    torch._dynamo.config.recompile_limit = 256
    torch._dynamo.config.accumulated_recompile_limit = 2048
    torch._dynamo.config.fail_on_recompile_limit_hit = True
    model = load_text_model(config)
    options = {
        "BLOCK_M": 16,
        "BLOCK_N": 32,
        "num_stages": 1,
        "num_warps": 4,
        "BACKEND": "TRITON",
    }
    options.update(config.model_loader_kwargs.get("kernel_options", {}))
    original_forward = model[0].auto_model.forward

    def tuned_forward(*args, **kwargs):
        kwargs["kernel_options"] = options
        return original_forward(*args, **kwargs)

    model[0].auto_model.forward = tuned_forward
    return model
```

The default Dynamo recompilation limit was exhausted by variable input shapes
in an initial MLDR English trial, causing an unfused fallback. That trial was
stopped and discarded. Raising the limits and failing when they are exhausted
prevents accepting results from this fallback; the completed run had none of
these warnings. The static model card keeps SDPA as its portable default;
reproducing these Flex results requires the wrapper and dedicated environment.

Use the earlier dense command with the following replacements:

```bash
--model-loader embeddinggemma2_flex_loader:load_model \
--model-loader-kwargs-json '{"config_kwargs":{"vision_config":null,"audio_config":null},"input_modalities":["text"],"kernel_options":{"BLOCK_M":16,"BLOCK_N":32,"num_stages":1,"num_warps":4,"BACKEND":"TRITON"}}' \
--attn-implementation flex_attention \
--results-dir output/embeddinggemma2-flex/hakari-results
```

The measured run selected explicit task lists for each dataset at its original
revision, instead of `--all`, to pin all 50 dataset revisions. Include all 18
NanoDAPFAM tasks explicitly when reproducing the extended track. The completed
English MLDR Flex trial was reused; the other 568 tasks were evaluated in the
new result root. Each condition shares the task's single encoding pass.

English MLDR nDCG@10 ×100 was 57.2295 for Flex / torch 2.14.1 versus 56.7163 for
corrected SDPA / torch 2.9.1. Evaluation time, including compilation, was
652.7 seconds versus 1203.3 seconds (~1.84× faster). Both torch and attention
changed, so this comparison does not isolate the attention backend's effect.

## hotchpotch Bekko Embeddings

Applies to:

- `hotchpotch/bekko-embedding-pico-beta-unir-v7`
- `hotchpotch/bekko-embedding-small-beta-unir-v8`
- `hotchpotch/bekko-embedding-pico-beta-unir-v9-QAT-ftQAT`
- `hotchpotch/bekko-embedding-pico-beta-unir-v9-GOR`
- `hotchpotch/bekko-embedding-pico-beta-unir-v9-GOR-pt`
- `hotchpotch/bekko-embedding-v1-a8m`
- `hotchpotch/bekko-embedding-v1-a25m`

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
- `hotchpotch/bekko-embedding-v1-a25m` documents base dim 384 and supported
  Matryoshka dims `256,128,64`; use the same prompt text and runtime settings
  as `hotchpotch/bekko-embedding-small-beta-unir-v8`.

### Bekko Static Embedding v1

`hotchpotch/bekko-static-embedding-v1` (revision
`76c36707a7814a747914ed05168420696a8123d0`) is a 1024-dimensional
StaticEmbedding model, renamed on 2026-09-14 from
`hotchpotch/bekko-static-embedding-multilingual-v1`. Its results were
republished under the new name in results PR #41. The prompt-name guidance above
does not apply: the shipped query and document prompts are empty, so no prefix
is used.

```bash
uv run hakari-bench evaluate dense \
  --model hotchpotch/bekko-static-embedding-v1 \
  --model-revision 76c36707a7814a747914ed05168420696a8123d0 \
  --dtype fp16 \
  --embedding-variant truncate:512,256,128,64,32 \
  --all
```

- Use `--dtype fp16`. The formal delivery stores the table in FP16, and the
  evaluated parameters and outputs were verified as `torch.float16`.
- There is no finite Sentence Transformers `max_seq_length` and no attention
  setting or remote code. The bundled ONNX/OpenVINO graphs need the
  repository's remote-code loader and are not part of the standard run.
- Truncate dims `512,256,128,64,32` are the documented MRL widths below the
  native 1024. With the default quantized and rescore variants, that gives 30
  conditions per task.

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

## BidirLM Embeddings

Applies to:

- `BidirLM/BidirLM-270M-Embedding` (revision
  `769f3a064aa4113a97d9b19c2417cb67a8cf5f30`)
- `BidirLM/BidirLM-0.6B-Embedding` (revision
  `f6279763d6bd59ff963897965f29fed0b447ed3c`)
- `BidirLM/BidirLM-1B-Embedding` (revision
  `8b9661377d17cc1c41f8c02df4a6e90487c5a7f9`, equal to the MTEB-pinned
  revision)

The shipped Sentence Transformers query and document prompts are empty, but
the official MTEB implementation
([`bidirlm_models.py`](https://raw.githubusercontent.com/embeddings-benchmark/mteb/main/mteb/models/model_implementations/bidirlm_models.py))
uses task-specific instructions. Each task therefore passes `--query-prompt`
with the official instruction for its YAML `source_task` (242 tasks, plus
MNanoBEIR aliases and MIRACL/MLDR mappings). The other 321 tasks use the
generic retrieval instruction from the model card. Documents get an explicitly
empty prompt:

```text
Instruct: Given a query, retrieve documents that answer the query.
Query:
```

There is no space after the final colon. Keep the per-task instructions; do
not replace them all with the generic one.

```bash
uv run hakari-bench evaluate dense \
  --model BidirLM/BidirLM-0.6B-Embedding \
  --model-revision f6279763d6bd59ff963897965f29fed0b447ed3c \
  --dataset DATASET --split TASK \
  --dtype bf16 --trust-remote-code --attn-implementation flash_attention_2 \
  --model-max-seq-length 512 --batch-size 32 \
  --query-prompt "$OFFICIAL_OR_GENERIC_INSTRUCTION" --document-prompt ''
```

Runtime notes:

- The pinned main-branch remote code requires Transformers 5. The
  `transformers-v4` branch is a different implementation; do not substitute it.
  The published runs used Transformers 5.22.1, Sentence Transformers 6.2.0,
  and torch 2.9.1.
- The architecture rejects explicit SDPA. FlashAttention 2 was validated
  against the eager reference attention.
- 512 tokens is the shipped Sentence Transformers maximum, not an ad hoc
  benchmark truncation. The architectures support 32768 (270M and 1B) and
  40960 (0.6B) tokens; evaluating at those lengths is a separate experiment.
- BidirLM-1B uses a Gemma3 backbone, and its remote code differs from 270M and
  0.6B. It always builds dense packed attention masks, which the
  FlashAttention 2 varlen path does not use, so they only cost memory.
  FlashAttention 2 matched eager attention, batch and single inputs matched,
  and independent mean pooling matched, all within one bf16 ULP.
- Neither model documents Matryoshka dimensions. Runs cover the base embedding
  plus the default int8, binary, and rescore variants.

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
| `perplexity-ai/pplx-embed-v1-late-0.6b` | `fp32`, `sdpa`, Transformers 5.12.1 + PyLate 1.4.0 | none | `[Q] ` / `[D] ` | `32` / `512` | `true` | The pinned SentenceTransformers config enables query expansion and expansion-token attention. NanoBEIR-en reproduced at 0.677272, within 0.0052 of the existing ColBERT-Zero result used as the official model-card reference. |
| `jinaai/jina-colbert-v2` | `bf16`, `eager` standard dispatch; checkpoint-native FlashAttention, Transformers 4.57.6 + PyLate 1.3.4 | none | `[QueryMarker]` / `[DocumentMarker]` | `32` / `300` | `true` | The official PyLate example and artifact metadata define these options. NanoBEIR-en reached 0.651298 and correlated with the 12 common official BEIR task scores at Pearson 0.9300 / Spearman 0.9161. Evaluate the documented 96- and 64-dimensional Matryoshka variants too. |

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
- `jinaai/jina-colbert-v2` uses external XLM-R code whose class does not
  advertise Transformers-native `flash_attention_2` dispatch. Passing that
  dispatch value fails before model loading. Keep the standard dispatch on
  `eager` and install FlashAttention so the pinned checkpoint's own
  `use_flash_attn: true` implementation follows the official model card.
- `perplexity-ai/pplx-embed-v1-late-0.6b` stores its complete late-interaction
  contract in `config_sentence_transformers.json`; do not disable query
  expansion or expansion-token attention merely to reduce evaluation cost.

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

## Gemini Embedding Models

Applies to:

- `gemini-embedding-2`

Use the built-in Gemini dense loader with Vertex/Enterprise credentials:

```bash
uv run --group gemini hakari-bench evaluate dense \
  --model gemini-embedding-2 \
  --model-alias google/gemini-embedding-2 \
  --model-loader gemini \
  --model-loader-kwargs-json '{"project":"ml-sandbox-309804","location":"global"}' \
  --query-prompt "task: search result | query: " \
  --document-prompt "title: none | text: "
```

Operational notes:

- `gemini-embedding-2` must be embedded one content at a time in the direct API;
  the adapter parallelizes those requests with `max_concurrency`.
- Install the Gemini dependencies with `uv add --group gemini google-genai
  sentencepiece`. The adapter uses the Gemma2 SentencePiece tokenizer locally
  because the public `google.genai.local_tokenizer.LocalTokenizer` does not yet
  accept `gemini-embedding-2`. Smoke checks on 2026-06-23 found
  `Gemini count_tokens == len(gemma2.encode(text)) + 1` across mixed-language
  samples, while Gemma3 did not match all samples.
- Google recommends prompt-formatted task instructions for Embeddings 2 instead
  of a `task_type` parameter. For asymmetric retrieval, use
  `task: search result | query: ` for queries and `title: none | text: ` for
  documents when no title metadata is available.
- `--truncate-dim` and `--embedding-variant truncate:DIM` use full Gemini
  embeddings followed by `full[:DIM]` and L2 normalization. API-side
  `output_dimensionality` supports 128-3072 dimensions and normalizes
  lower-dimensional vectors; the local normalized-prefix path matches API-side
  dimensionality within float32 noise in smoke checks.
- The model card records 8192 as the provider input limit. The adapter keeps a
  conservative 8100-token local guard using `len(gemma2.encode(text)) + 1`.
  Developer API batch silently truncates over-limit inputs to the provider limit
  instead of failing, but benchmark inputs should still be pre-truncated locally
  to avoid hidden behavior and unnecessary enqueued-token usage.
- Gemini batch jobs use Vertex/Enterprise batch prediction with GCS input/output
  and currently require `location=global` for `gemini-embedding-2`.
- As of 2026-06-23, `gemini-embedding-2` Vertex/Enterprise batch jobs can remain
  in `JOB_STATE_QUEUED` without `startTime` because Gemini batch uses shared
  provider capacity. The Gemini Developer API has a separate
  `batches.create_embeddings` path, but that requires `GEMINI_API_KEY` or
  `GOOGLE_API_KEY` and is not supported by the Python Gen AI SDK with
  `vertexai=True`.

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

## UltraBERT-Embed-150M

For `dmis-lab/UltraBERT-Embed-150M`, use the reviewed card
`config/model_cards/dmis-lab__UltraBERT-Embed-150M.yaml`. The pinned checkpoint
uses CLS pooling with 768-dimensional embeddings, a 32768-token maximum, the
`query` retrieval instruction, and an empty `document` prompt. No Matryoshka
truncation dimensions are documented, so keep the standard full-dimension
quantization/rescore variants without adding truncation variants.

The [official model card](https://huggingface.co/dmis-lab/UltraBERT-Embed-150M)
recommends FlashAttention 2 and supports native loading with Transformers
5.20 or later. A Python 3.12 environment with Transformers 5.20.1,
SentenceTransformers 6.1.0, Torch 2.9.1/CUDA 12.8, and FlashAttention 2.8.3
successfully evaluated all 165 English/code tasks selected by `--all --english`
in bf16, including the initial NanoArguAna validation. All five standard dense
representations have complete coverage.
Remote code is unnecessary with this runtime. Keep the model's FP32 rotary
frequency buffers intact when loading bf16 weights.

Use a separate environment for these newer Transformers/SentenceTransformers
versions if the default environment needs to remain unchanged. Run the English
and code subset with the reviewed card and the same environment:

```bash
OMP_NUM_THREADS=8 uv run --no-project --python /path/to/venv/bin/python \
  python -m hakari_bench.cli evaluate from-model-card \
  --model-card config/model_cards/dmis-lab__UltraBERT-Embed-150M.yaml \
  --all --english --device cuda:0 --batch-size 32
```

Run from the repository root. Reduce batch size before changing the model's
maximum sequence length if a long-document task exhausts GPU memory.

## SlideOn and mSlideOn

`lightonai/SlideOn` (English) and `lightonai/mSlideOn` (multilingual) are
learned sparse retrievers, not dense or late-interaction evaluation backends.
Use `evaluate sparse`, or the reviewed model cards
`config/model_cards/lightonai__SlideOn.yaml` and
`config/model_cards/lightonai__mSlideOn.yaml`. Both return 32768-dimensional
nonnegative learned latent features and use raw dot-product scoring. These
features are not tokenizer vocabulary entries. Keep the native 8192-token
query and document limits, the checkpoint's task preprocessing, and the
unpruned base vectors. The standard post-encode sparse-budget variants can be
computed without re-encoding. Do not apply dense truncation or quantization.

The remote `slideon.py` and `modeling_slideon.py` were reviewed at revisions
`370c600e9886afc43ff8026695261e56ecfaa011` (SlideOn) and
`ef8016025bfd0ea10e44ee27c4038a5852b1018a` (mSlideOn). Loading requires
`trust_remote_code`; the flat checkpoints include their inference code and do
not require the upstream training package or PyLate. The official cards require
SentenceTransformers `>=6.1,<6.2` and Transformers `>=5.3,<6`. The isolated
UltraBERT environment with SentenceTransformers 6.1.0, Transformers 5.20.1,
Torch 2.9.1/CUDA 12.8, and FlashAttention 2.8.3 also passed SlideOn/mSlideOn
encoding and NanoArguAna smoke evaluations.

Use `examples.custom_backends.slideon_loader:load_model` to preserve the
upstream mixed precision: bf16 backbone and projections, with the sparse head
retained in FP32. The ordinary HAKARI post-load dtype normalization would
otherwise cast this intentionally FP32 head. The model's own forward applies
its prescribed BF16 head autocast and FP16 retrieval-weight rounding. The
custom loader changes loading only, retaining the upstream inference path.

```bash
PYTHONPATH=$PWD OMP_NUM_THREADS=8 \
  uv run --no-project --python /path/to/venv/bin/python \
  python -m hakari_bench.cli evaluate from-model-card \
  --model-card config/model_cards/lightonai__mSlideOn.yaml \
  --params-json '{"model":{"loader":"examples.custom_backends.slideon_loader:load_model"}}' \
  --all --device cuda:0 --batch-size 8
```

For SlideOn, replace the card with `lightonai__SlideOn.yaml` and add
`--english`. `from-model-card` accepts a custom loader through `--params-json`;
it does not accept the direct `--model-loader` flag. Query/document prompt
names are stored in the cards. SlideOn uses its saved textual retrieval
prompts; mSlideOn uses empty SentenceTransformers prompts and inserts its
query/document marker token internally. Do not manually add either prefix.

The completed evaluation used all 563 tasks for mSlideOn and the 165-task
English/code scope for SlideOn, with all 17 standard sparse representations.
The query budgets are 8/16/24/32 nonzero features crossed with document budgets
64/128/256/512; the latent feature space remains 32768-dimensional.

On Torch 2.9.1/CUDA 12.8, SlideOn's unpruned sparse matrix multiplication
exhausted cuSPARSE SpGEMM resources on three NanoDAPFAM tasks:
`NanoDAPFAMAllTitlAbsClmToTitlAbsClm`,
`NanoDAPFAMInTitlAbsClmToTitlAbsClm`, and
`NanoDAPFAMOutTitlAbsClmToTitlAbsClm`. Re-evaluate these tasks with
`--retrieval-score-device cpu`; model encoding still runs on the selected GPU.
Keep the same maximum length, precision, batch size, and variant grid. Record
this scoring-device exception in result submissions; CPU and GPU accumulation
can differ slightly numerically.

Sources: [SlideOn](https://huggingface.co/lightonai/SlideOn),
[mSlideOn](https://huggingface.co/lightonai/mSlideOn), and the
[official technical article](https://huggingface.co/blog/lightonai/slideon-mslideon).

## F2LLM-v2-0.6B and pplx-embed-v2-late-0.6b

F2LLM-v2-0.6B uses the official retrieval instruction recorded in its model
card, BF16 with FlashAttention 2, and the shipped 40960-token maximum. Evaluate
1024-dimensional base embeddings plus every documented MRL dimension down to
8; the dense CLI adds quantization and rescore variants (40 categories total).

F2LLM-v2-1.7B (revision `c5650fe0573b810008b5fbf79f51ff9bfa1f2e83`) and
F2LLM-v2-4B (revision `3e5652543fb453386a9bba24d82702da4f3a0427`) ship the same
Sentence Transformers configuration and use the same settings. Their MRL
dimensions are the powers of two below the native output, down to 8, from the
official figure 5. That is 2048 native plus 1024 through 8 for 1.7B (45
categories), and 2560 native plus 2048 through 8 for 4B (50 categories). The
upstream example scores matched within 0.004. Long tasks ran at batch size 1
without shortening the 40960-token context.

```bash
uv run hakari-bench evaluate from-model-card \
  --model-card config/model_cards/codefuse-ai__F2LLM-v2-4B.yaml \
  --all --batch-size 8 --device cuda:0
```

pplx-embed-v2-late-0.6b requires the native SentenceTransformers >=6
`MultiVectorEncoder` and Transformers >=5.4. Use the reusable adapter rather
than PyLate: native role encoding preserves first-position `[Q]`/`[D]` markers
and document punctuation masking. The evaluated checkpoint uses FP32, SDPA,
1024 query tokens and 4096 document tokens, without query expansion or
truncation variants. Install the optimized FLA and causal-conv1d kernels for
its linear-attention backbone. The native and HAKARI MaxSim scores agreed
within 2.4e-7 in the preflight validation.

```bash
hakari-bench evaluate from-model-card \
  --model-card config/model_cards/perplexity-ai__pplx-embed-v2-late-0.6b.yaml \
  --model-loader examples.custom_backends.pplx_multivector:load_model \
  --all --batch-size 8 --device cuda:0 \
  --late-interaction-exact-doc-batch-size 16 \
  --late-interaction-exact-query-batch-size 2
```

The custom loader is an explicit CLI option; the model card alone does not
select it. Reduce batch size for long documents without shortening context.

## Linkup SPARSEUP-v2

`Linkup-Platform/linkup-sparseup-embed-v2` is an English learned sparse
retriever (SPLADE head on ModernBERT-base). Use `evaluate sparse` with the
reviewed card `config/model_cards/Linkup-Platform__linkup-sparseup-embed-v2.yaml`.
The checkpoint needs `trust_remote_code`; `custom_st.py` and
`modeling_splade.py` were reviewed at revision
`7165075edb8c7e5e6d1125aa8a6a753d3c50c5d8`. They apply a logit shift of 18,
keep the top 12 vocabulary activations per token before max pooling, and fold
case and leading-space vocabulary variants onto one dimension.

The `query` and `document` prompt names (`[Q]` / `[D]`) select the branch and
its 8192-token limit; the prefix tokens are attended but not pooled. Do not add
manual prefixes. Keep raw dot-product scoring, the bf16 checkpoint precision,
and unpruned base vectors. The upstream top-k pruning recipe is covered by the
standard sparse budget grid; no extra budget variants are needed.

The default environment (Transformers 5.12.1, SentenceTransformers 5.4.1) loads
the checkpoint. FlashAttention 2 through the `flash-attn` dependency group
reproduced the official example within about 1 point of the dot-product score
(89.8 versus 90.5), as did SDPA. Evaluate the standard task set:

```bash
uv run --group flash-attn hakari-bench evaluate from-model-card \
  --model-card config/model_cards/Linkup-Platform__linkup-sparseup-embed-v2.yaml \
  --all --device cuda:0 --batch-size 4
```

Each sequence materializes `[length, 50370]` activations before pooling, so
long-document tasks need a smaller batch size. Reduce `--batch-size` instead of
the 8192-token limit.

The completed 563-task run kept GPU scoring throughout. Batch size 16 ran out
of memory on long-document tasks with a 32 GB GPU; the first 12 tasks used
batch size 16 and the remaining 551 used batch size 4.

The `-pretrain` checkpoint is an intermediate contrastive checkpoint that the
authors describe as needing fine-tuning. Do not evaluate it as a retrieval
model.

## OpenSearch Neural Sparse asym-v1

`opensearch-project/opensearch-neural-sparse-encoding-asym-v1` is an
asymmetric English SPLADE model loaded through the SentenceTransformers
`Router`. `encode_query` runs a bert-medium query tower with a 256-token limit,
and `encode_document` runs a GTE document tower with a 512-token limit. Both
towers share the BERT WordPiece vocabulary. The saved prompts are empty.

The GTE document tower uses the native `gte` architecture and needs
Transformers >=5.22.1. Use a separate environment when the default one must
stay on older versions. Transformers 5.24.0 with SentenceTransformers 6.3.0
and Torch 2.9.1/CUDA 12.8 reproduced the official example score (18.19). bf16
matched fp32 within 0.004 nDCG@10 on NanoArguAna, NanoSciFact, and
NanoFiQA2018, so use the standard bf16 runtime with SDPA.

```bash
OMP_NUM_THREADS=8 uv run --no-project --python /path/to/venv/bin/python \
  python -m hakari_bench.cli evaluate from-model-card \
  --model-card config/model_cards/opensearch-project__opensearch-neural-sparse-encoding-asym-v1.yaml \
  --all --device cuda:0 --batch-size 32
```

The completed 563-task run used batch size 32 for every task.

Automatic parameter counting cannot inspect the `Router`, so the card records
the parameter counts. They include both towers, and the active count subtracts
both input embedding tables. The query tower alone has 25.8M active
parameters at search time.

## OpenSearch Neural Embed v1

`opensearch-project/opensearch-neural-embed-v1` is an English dense model
distilled into Qwen3-Embedding-0.6B. It uses mean pooling, a 1024 to 2048
`Dense` projection, and an 8192-token maximum. The saved `query` prompt is the
web-search instruction, and documents use an empty prompt. The 2048-dimensional
output concatenates the leading 1024 dimensions of two teacher spaces, so no
Matryoshka truncation is documented. Evaluate base plus the standard
full-dimension quantized/rescore variants.

SentenceTransformers 5.4.1 fails in bf16 with `mat1 and mat2 must have the same
dtype`: the mean pooling output reaches the bf16 `Dense` layer as FP32.
SentenceTransformers 6.3.0 with Transformers 5.24.0 loads the projection in
bf16 and reproduces the official example scores within 0.001. Use that
environment with FlashAttention 2:

```bash
OMP_NUM_THREADS=8 uv run --no-project --python /path/to/venv/bin/python \
  python -m hakari_bench.cli evaluate from-model-card \
  --model-card config/model_cards/opensearch-project__opensearch-neural-embed-v1.yaml \
  --all --device cuda:0 --batch-size 16
```

The completed 563-task run used batch size 16 for every task.

## DexelLabs MargEmbed-Akan

`DexelLabs/MargEmbed-Akan` is a Twi (Akan) to English retrieval model distilled
from `McGill-NLP/AfriE5-Large-instruct` (XLM-RoBERTa large, 512 tokens, mean
pooling). The checkpoint's saved prompts are empty, but the official usage
applies `Instruct: Given a question, retrieve Wikipedia passages that answer
the question\nQuery: ` to queries and no prompt to passages. The card stores
these explicit prompts.

The SentenceTransformers config uses module paths that need
SentenceTransformers >=6. SentenceTransformers 6.3.0 with Transformers 5.24.0
loads it in bf16 with SDPA. The license is CC BY-NC 4.0, and the card records
it as non-commercial. HAKARI-Bench has no Twi tasks, so the run measures
English and cross-lingual transfer from a Twi-focused model.

The completed 563-task run used batch size 64 for every task.
