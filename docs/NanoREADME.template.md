---
configs:
- config_name: bm25
  data_files:
{{CONFIG_BM25_DATA_FILES}}
- config_name: harrier_oss_v1_270m
  data_files:
{{CONFIG_DENSE_DATA_FILES}}
- config_name: reranking_hybrid
  data_files:
{{CONFIG_HYBRID_DATA_FILES}}
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
be run easily with [HAKARI-Bench](https://github.com/hakari-bench/hakari-bench).

{{DATASET_NAME}} is derived from {{SOURCE_BENCHMARK_NAME}}. It follows the
Hugging Face Datasets layout convention used by
[sentence-transformers/NanoBEIR-en](https://huggingface.co/datasets/sentence-transformers/NanoBEIR-en):
each Nano split has separate `corpus`, `queries`, and `qrels` tables, with
candidate subsets stored in `bm25`, `harrier_oss_v1_270m`, and
`reranking_hybrid` tables. This layout follows the NanoBEIR-style evaluation
approach summarized in
[NanoBEIR](https://huggingface.co/blog/sionic-ai/eval-sionic-nano-beir).

{{DATASET_OVERVIEW_PARAGRAPH}}

{{NAMING_NOTE_SECTION}}

## Source Links

{{SOURCE_LINKS_LIST}}

## Data Layout

This dataset uses six Hugging Face Datasets configs:

- `corpus`: documents with `_id` and `text`
- `queries`: queries with `_id` and `text`
- `qrels`: positive relevance labels with `query-id` and `corpus-id`
- `bm25`: BM25 candidate lists with `query-id` and `corpus-ids`
- `harrier_oss_v1_270m`: dense candidate lists from
  `microsoft/harrier-oss-v1-270m`
- `reranking_hybrid`: RRF candidate lists built from `bm25` and
  `harrier_oss_v1_270m`

Each config has the same Nano split names.

The `qrels` config is positive-only. Source rows with `score <= 0` are treated
as non-relevant or hard-negative annotations and are not included in `qrels`.
When the source provides such rows, their documents are preferentially used as
hard negatives in the `corpus` config before generic corpus-fill documents.
Source hard negatives are sampled deterministically with query round-robin so
one query's negative pool does not dominate the corpus.

## Split Statistics

Length statistics are computed with `len(str(text))` over the `queries` and
`corpus` tables. `std` is the population standard deviation over the rows in
each split.

| Nano split | Queries | Corpus | Qrels | Query avg | Query std | Query median | Query p25 | Query p75 | Doc avg | Doc std | Doc median | Doc p25 | Doc p75 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{{SPLIT_STATISTICS_ROWS}}

## Construction Steps

This dataset is constructed as follows.

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
9. Use {{CORPUS_FILL_POLICY}}.
10. Remove exact duplicate query text and document text within each split. If a
   removed document duplicate was referenced by qrels,
   {{QRELS_DUPLICATE_POLICY}}.
11. Store corpus text as {{CORPUS_TEXT_POLICY}}.
12. Generate BM25 top-{{BM25_TOP_K}} candidates with
    `{{BM25_TOKENIZER_POLICY}}` tokenization.
13. Generate dense top-{{DENSE_TOP_K}} candidates with
    `microsoft/harrier-oss-v1-270m`; queries use the `web_search_query` prompt
    and documents use no prompt. Embeddings are normalized, so the dot product
    score is cosine similarity.
14. Build `reranking_hybrid` with RRF over the BM25 and dense candidate lists.
    RRF uses `rrf_k={{RRF_K}}` and keeps the top-{{HYBRID_TOP_K}} candidates.
15. If the RRF top-{{HYBRID_TOP_K}} contains no qrels-positive document, append
    one deterministic positive at rank {{SAFEGUARD_RANK}}. This is the optional
    safeguard positive.

{{QRELS_SCORE_POLICY_NOTE}}

{{SOURCE_HARD_NEGATIVE_NOTE}}

{{QRELS_CAPPING_NOTE}}

## Candidate Subset Policy

The `bm25`, `harrier_oss_v1_270m`, and `reranking_hybrid` configs are candidate
subsets for first-stage retrieval and reranking. They are not separate source
datasets. Each row contains one query id and a ranked list of corpus ids.

BM25 candidates are generated from the selected corpus for each split. When a
qrels-positive document is not present in the raw BM25 top-{{BM25_TOP_K}}
results, the missing positive may be forced into diagnostic candidate lists
according to the generation recipe documented in the split metadata. Candidate
ids are kept unique after replacement.

Concretely, each `bm25` row is produced by tokenizing the selected split corpus
and query texts with `{{BM25_TOKENIZER_POLICY}}`, ranking the corpus with BM25,
then writing the ranked corpus ids as `corpus-ids` for that query. The list is a
candidate subset for downstream evaluation, not a full-corpus ranking.

The dense candidate config is named `harrier_oss_v1_270m`. In tables below it is
shown as `Dense`; Dense means `microsoft/harrier-oss-v1-270m` with the
`web_search_query` prompt for queries and cosine similarity over normalized
embeddings.

The `reranking_hybrid` config is built by RRF over the BM25 and dense candidate
lists. It stores the RRF top-{{HYBRID_TOP_K}} unchanged when that list already
contains a qrels-positive document. If it does not, one deterministic positive
is appended at rank {{SAFEGUARD_RANK}}. A row with {{HYBRID_TOP_K}} candidates
therefore means the RRF top-{{HYBRID_TOP_K}} already contains a positive; a row
with {{SAFEGUARD_RANK}} candidates means the final candidate is the safeguard
positive.

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

## Candidate Quality

`nDCG@10` and `Recall@100` are computed from the included candidate rankings
against the included qrels, then reported as 0-100 scores such as `52.45`.
`Recall@100` uses only the top 100 candidates; an optional rank-101 safeguard
positive is not counted in `Recall@100`.

{{CANDIDATE_SCORE_NOTES}}

| Nano split | BM25 tokenizer | BM25 nDCG@10 | Dense nDCG@10 | Hybrid nDCG@10 | BM25 Recall@100 | Dense Recall@100 | Hybrid Recall@100 | Hybrid candidates | Safeguard positives |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
{{CANDIDATE_SCORE_ROWS}}

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
  `500` for reranking-hybrid source columns
- [ ] `{{DENSE_TOP_K}}` matches the generated `harrier_oss_v1_270m` candidate
  length, typically `500` for reranking-hybrid source columns
- [ ] `{{HYBRID_TOP_K}}`, `{{RRF_K}}`, and `{{SAFEGUARD_RANK}}` match the
  generated `reranking_hybrid` metadata
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
- [ ] candidate quality scores are rendered as 0-100 values with two decimals
- [ ] Dense is clearly defined as `microsoft/harrier-oss-v1-270m`
- [ ] safeguard semantics are documented in one sentence
- [ ] query/relevant coverage columns are 100% when the candidate subset is
  intended for safeguarded reranking diagnostics
- [ ] missing positives are documented as forced or safeguarded into the
  candidate list, or the section is revised if a different policy was used
- [ ] `dataset_info` metadata is left to `ds.push_to_hub()` / Hugging Face
  automatic generation instead of hand-maintained in this template
- [ ] skipped tasks are either listed with reasons or explicitly marked as none
- [ ] license wording points to upstream licenses instead of inventing a new
  license
- [ ] source links are official and current
