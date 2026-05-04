# Model-Specific Benchmarking Notes

When measuring specific models, follow the notes in this document. These notes
override generic benchmarking defaults when they are more specific, because some
models require exact prompts or runtime choices for comparable retrieval scores.

## cl-nagoya/ruri-v3

Applies to:

- `cl-nagoya/ruri-v3-30m`
- `cl-nagoya/ruri-v3-310m`

Use the retrieval prompts documented by the model card:

- query prompt: `検索クエリ: `
- document/corpus prompt: `検索文書: `

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
- In this project, `cl-nagoya/ruri-v3-310m` on NanoMTEB-Japanese/NanoJaqket produced
  abnormally low scores with `transformers==5.7.0` despite correct prompts.
  Re-running with `transformers==4.57.6` and Flash Attention 2 restored the
  expected current-dataset score.
- Do not shorten the model max sequence length to work around memory pressure.
  Reduce batch size first.

Historical comparison note:

- Older NanoMTEB-Japanese/NanoJaqket results around `nDCG@10 = 0.9426` were measured on
  the earlier q50 NanoJaqket data. Current NanoMTEB-Japanese uses q200 data, where
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
