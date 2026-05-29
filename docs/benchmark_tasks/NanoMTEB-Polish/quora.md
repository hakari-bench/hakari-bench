# NanoMTEB-Polish / quora

## Overview

`quora` is a Polish duplicate-question retrieval task derived from Quora
Question Pairs. Queries and documents are short question texts, and the target
is a semantically duplicate question. The task emphasizes paraphrase retrieval:
different word order, synonyms, and small changes in phrasing should still map
to the same user intent.

## Details

### What the Original Data Measures

The [First Quora Dataset Release: Question Pairs](https://quoradata.quora.com/First-Quora-Dataset-Release-Question-Pairs)
is the canonical public source for the duplicate-question pair data. The
[MTEB paper](https://arxiv.org/abs/2210.07316) includes Quora as a retrieval
dataset in its benchmark suite. This Polish task is the MTEB
`Quora-PLHardNegatives` version, so the exact evaluated text is Polish rather
than the original English release.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 485 positive qrels. Queries are
short, averaging 52.51 characters, and documents average only 64.64 characters.
Examples are direct paraphrase pairs such as questions about living without
money, finding life direction, dealing with unpleasant people, notebooks for
programmers, and Snapchat screenshots. There are 72 multi-positive queries.

### BM25 Difficulty

BM25 is very strong, with nDCG@10 = 0.7705 and hit@10 = 0.9100. It ranks 150
positives first and 182 in the top 10. The short question pairs often share key
content words, so exact lexical overlap is a high baseline, but models still
need paraphrase sensitivity for cases where the duplicate uses different
function words or synonyms.

### Training Data That May Help

Useful data includes non-overlapping Quora Question Pairs training data, Polish
paraphrase and duplicate-question datasets, translated paraphrase pairs, and
hard negatives consisting of topically similar but non-duplicate questions.
Avoid the MTEB hard-negative evaluation records and exact duplicate pairs.

### Synthetic Data Guidance

Generate short Polish question pairs where both questions express the same
intent with different wording. Include near negatives that share topic words but
change the requested action, entity, or condition. Synthetic data should stay
brief and question-like rather than becoming passage retrieval.

## Example Data

| Query | Positive document |
| --- | --- |
| Jak dostać się na Harvard? (26 chars) | Jak dostać się na Uniwersytet Harvarda? (39 chars) |
| Czym jest 10-20 przypadkowych rzeczy o sobie? (45 chars) | Jakie są 10 przypadkowych faktów o Tobie? (41 chars) |
| Co powinienem zrobić w swoim CV, aby uzyskać wywiady z zakresu analityki danych? (80 chars) | Co powinienem poprawić w swoim CV, aby uzyskać wywiady z zakresu analityki danych? (82 chars) |
| Jak sobie radzisz, gdy czujesz się wyczerpany emocjonalnie? (59 chars) | Jak przezwyciężyć uczucie wyczerpania emocjonalnego? (52 chars) |
| Czy iPhone naprawdę jest wart swojej ceny? (42 chars) | Czy iPhone jest tego wart? (26 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Polish |
| Backing dataset | NanoMTEB-Polish |
| Task / split | quora |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish) |
| Source dataset | [mteb/Quora-PLHardNegatives](https://huggingface.co/datasets/mteb/Quora-PLHardNegatives) |
| Language | pl |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 485 |
| Avg positives / query | 2.425 |
| Positives per query (min / median / max) | 1 / 1.0 / 33 |
| Queries with multiple positives | 72 (36.0%) |
| BM25 nDCG@10 | 0.7704 |
| BM25 hit@10 | 0.9100 |
| BM25 Recall@100 | 0.8309 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.9073 |
| Dense hit@10 | 0.9600 |
| Dense Recall@100 | 0.9526 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8207 |
| Reranking hybrid hit@10 | 0.9500 |
| Reranking hybrid Recall@100 | 0.9691 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 52.51 |
| Document length avg chars | 64.64 |

### Public Sources

- [First Quora Dataset Release: Question Pairs](https://quoradata.quora.com/First-Quora-Dataset-Release-Question-Pairs), official dataset release page.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), benchmark paper covering Quora retrieval.
- [mteb/Quora-PLHardNegatives](https://huggingface.co/datasets/mteb/Quora-PLHardNegatives), Polish source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish)
- Source task dataset: [mteb/Quora-PLHardNegatives](https://huggingface.co/datasets/mteb/Quora-PLHardNegatives)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| First Quora Dataset Release: Question Pairs | 2017 | dataset release | https://quoradata.quora.com/First-Quora-Dataset-Release-Question-Pairs |
| MTEB: Massive Text Embedding Benchmark | 2022 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| mteb/Quora-PLHardNegatives |  | dataset card | https://huggingface.co/datasets/mteb/Quora-PLHardNegatives |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Polish
  backing_dataset: NanoMTEB-Polish
  dataset_id: hakari-bench/NanoMTEB-Polish
  task_name: quora
  split_name: quora
  language: pl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Polish/quora.md
  source_research:
    primary_source_type: dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone Polish Quora paper was confirmed
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 485
  positives_per_query:
    average: 2.425
    min: 1
    median: 1.0
    max: 33
    multi_positive_queries: 72
    multi_positive_query_percent: 36.0
  text_stats_chars:
    query_mean: 52.505
    document_mean: 64.6365
  bm25:
    ndcg_at_10: 0.7703745607044067
    hit_at_10: 0.91
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7703745607
      hit_at_10: 0.91
      recall_at_100: 0.8309278351
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8309278351
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.9073195342
      hit_at_10: 0.96
      recall_at_100: 0.9525773196
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9525773196
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8206734893
      hit_at_10: 0.95
      recall_at_100: 0.9690721649
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9690721649
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
