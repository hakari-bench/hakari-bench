---
configs:
- config_name: bm25
  data_files:
{{CONFIG_BM25_DATA_FILES}}
- config_name: corpus
  data_files:
{{CONFIG_CORPUS_DATA_FILES}}
- config_name: qrels
  data_files:
{{CONFIG_QRELS_DATA_FILES}}
- config_name: queries
  data_files:
{{CONFIG_QUERIES_DATA_FILES}}
  default: true
language:
{{LANGUAGE_LIST}}
tags:
{{TAG_LIST}}
---

# {{DATASET_NAME}}

This dataset is a Nano-style retrieval dataset. Nano-series evaluation can
be run easily with [HAKARI-Bench](https://github.com/hotchpotch/hakari-bench).

{{DATASET_NAME}} is derived from {{SOURCE_BENCHMARK_NAME}}. It follows the
Hugging Face Datasets layout convention used by
[sentence-transformers/NanoBEIR-en](https://huggingface.co/datasets/sentence-transformers/NanoBEIR-en):
each Nano split has separate `corpus`, `queries`, and `qrels` tables, and BM25
candidates are provided separately in a `bm25` table. This layout follows
the NanoBEIR-style evaluation approach summarized in
[NanoBEIR](https://huggingface.co/blog/sionic-ai/eval-sionic-nano-beir).

{{DATASET_OVERVIEW_PARAGRAPH}}

{{NAMING_NOTE_SECTION}}

## Source Links

{{SOURCE_LINKS_LIST}}

## Data Layout

This dataset uses four Hugging Face Datasets configs:

- `corpus`: documents with `_id` and `text`
- `queries`: queries with `_id` and `text`
- `qrels`: positive relevance labels with `query-id` and `corpus-id`
- `bm25`: BM25 candidate lists with `query-id` and `corpus-ids`

Each config has the same Nano split names. If the actual generated dataset uses
a different schema, config name, path layout, or field name, revise this section
before publishing the README.

The `qrels` config is positive-only. Source rows with `score <= 0` are treated
as non-relevant or hard-negative annotations and are not included in `qrels`.
When the source provides such rows, their documents are preferentially used as
hard negatives in the `corpus` config before generic corpus-fill documents.
Source hard negatives are sampled deterministically with query round-robin so
one query's negative pool does not dominate the corpus.

## Split Statistics

Length statistics are computed with `len(str(text))` over the generated
`queries` and `corpus` tables. `std` is the population standard deviation over
the generated rows. If the generated dataset uses a different text field, nested
layout, or preprocessed display field, revise this section before publishing
the README.

| Nano split | Queries | Corpus | Qrels | Query avg | Query std | Query median | Query p25 | Query p75 | Doc avg | Doc std | Doc median | Doc p25 | Doc p75 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{{SPLIT_STATISTICS_ROWS}}

## Construction Steps

This dataset was built as follows. If the actual generation procedure differs,
revise this section before publishing the README.

1. Use {{SOURCE_BENCHMARK_NAME}} as the upstream benchmark or dataset family.
2. Load source datasets from {{SOURCE_DATASET_LOCATION}}.
3. Source evaluation split policy: {{SOURCE_SPLIT_POLICY}}.
4. Create one Nano split for each selected source retrieval task.
5. Keep up to {{MAX_QUERIES_PER_SPLIT}} eligible queries per Nano split.
6. Treat source relevance rows with `score > 0` as qrels-positive documents.
   If the source has no score column, treat its qrels as positive-only only when
   that is the source task convention.
7. Exclude source rows with `score <= 0` from `qrels`. When such rows are
   available for selected queries, use their documents as hard-negative corpus
   candidates before generic fill documents.
8. Include all qrels-positive documents for the selected queries.
9. Fill the corpus from {{CORPUS_FILL_POLICY}} up to {{MAX_CORPUS_DOCUMENTS}}
   documents.
10. Remove exact duplicate query text and document text within each split. If a
   removed document duplicate was referenced by qrels,
   {{QRELS_DUPLICATE_POLICY}}.
11. Store corpus text as {{CORPUS_TEXT_POLICY}}.
12. Generate BM25 top-{{BM25_TOP_K}} candidates with
    `{{BM25_TOKENIZER_POLICY}}` tokenization.
13. If a qrels-positive document is missing from the raw BM25 result, insert it
    into the final `bm25` candidate list by replacing a tail non-positive
    candidate.

{{QRELS_SCORE_POLICY_NOTE}}

{{SOURCE_HARD_NEGATIVE_NOTE}}

{{QRELS_CAPPING_NOTE}}

## BM25 Subset Policy

The `bm25` config is a candidate subset for first-stage retrieval and reranking.
It is not a separate source dataset. Each row contains one query id and a ranked
list of up to {{BM25_TOP_K}} corpus ids.

BM25 candidates are generated from the selected corpus for each split. When a
qrels-positive document is not present in the raw BM25 top-{{BM25_TOP_K}}
results, the missing positive is forced into the final candidate list by
replacing a tail candidate that is not positive for that query. Candidate ids
are kept unique after replacement.

Concretely, each `bm25` row is produced by tokenizing the selected split corpus
and query texts with `{{BM25_TOKENIZER_POLICY}}`, ranking the corpus with BM25,
then writing the ranked corpus ids as `corpus-ids` for that query. The list is a
candidate subset for downstream evaluation, not a full-corpus ranking.

Source hard negatives, including documents referenced by source rows with
`score <= 0`, may appear in the selected corpus and can naturally appear in BM25
candidates. They are still non-relevant and are not listed in `qrels`.

When source hard negatives are available, the default corpus sampling policy is
query round-robin: group hard negatives by selected query, preserve source
rank/order within each query, add at most one new hard negative from each query
per pass, remove duplicate IDs and exact duplicate text, then fill any remaining
slots from source corpus order.

## Split Mapping

{{SPLIT_MAPPING_NOTES}}

| Nano split | Source task | Source dataset | Queries | Corpus | Qrels |
|---|---|---|---:|---:|---:|
{{SPLIT_MAPPING_ROWS}}

## BM25 nDCG@10

`nDCG@10` is computed from the included BM25 ranking against the included qrels.

{{BM25_SCORE_NOTES}}

| Nano split | Tokenizer | Forced BM25 positives | BM25 nDCG@10 |
|---|---|---:|---:|
{{BM25_SCORE_ROWS}}

## Skipped Tasks

{{SKIPPED_TASKS_SECTION}}

## License

{{DATASET_NAME}} is a derived dataset. Users must comply with the licenses,
terms, and attribution requirements of {{UPSTREAM_LICENSE_TARGET}}.

## Template Fill Checklist

Do not include this checklist in the actual dataset README. It is only for the
agent or maintainer filling this template.

Before publishing, replace every `{{...}}` placeholder and verify:

- [ ] every config lists the same Nano splits with the correct parquet paths
- [ ] `{{MAX_QUERIES_PER_SPLIT}}` matches the generated dataset, such as `200`
  for q200 datasets
- [ ] `{{BM25_TOP_K}}` matches the generated `bm25` candidate length, typically
  `100`
- [ ] the Data Layout section matches the generated configs, paths, and field
  names
- [ ] `{{SPLIT_STATISTICS_ROWS}}` includes one row per published split, with
  qrels/corpus/query counts and query/document `len(str(text))` statistics
  (avg, std, median, p25, p75)
- [ ] the Construction Steps section matches the actual generation procedure
- [ ] `{{CORPUS_FILL_POLICY}}` says whether the corpus was filled from source
  order, source hard negatives, source negatives, source `score <= 0` rows, or
  another policy
- [ ] `{{QRELS_SCORE_POLICY_NOTE}}` states whether source scores were
  positive-only, binary-collapsed, or preserved as graded positives
- [ ] `{{SOURCE_HARD_NEGATIVE_NOTE}}` states whether source `score <= 0` rows
  or explicit negative pools were used in corpus construction, or explicitly
  says none were available
- [ ] source hard negatives, when available, were sampled with deterministic
  query round-robin or the README documents the custom policy
- [ ] no source row with `score <= 0` is included in the published `qrels`
  config
- [ ] `{{NAMING_NOTE_SECTION}}` is either filled with a short naming note or
  removed entirely
- [ ] `{{QRELS_CAPPING_NOTE}}` is filled only when qrels positives were capped,
  otherwise removed entirely
- [ ] split counts match generated parquet files
- [ ] tokenizer names match the actual BM25 generation output
- [ ] missing BM25 positives are documented as forced into the candidate list,
  or the section is revised if a different policy was used
- [ ] skipped tasks are either listed with reasons or explicitly marked as none
- [ ] license wording points to upstream licenses instead of inventing a new
  license
- [ ] source links are official and current
