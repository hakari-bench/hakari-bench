# NanoMTEB-Polish / nq

## Overview

Natural Questions was introduced as real Google-search questions paired with
Wikipedia evidence, and this Polish hard-negative task should be read as a
localized open-domain QA retrieval version of that setup. Short Polish
fact-seeking questions retrieve Wikipedia-style answer passages from a 10,000
document pool. The observed questions ask about the Great Wall, Arctic research
stations, films, Roman education, and U.S. succession, so the model must map
natural Polish information needs to the passage that contains the factual
answer, sometimes with multiple valid positives.

## Details

### What the Original Data Measures

[Natural Questions: A Benchmark for Question Answering Research](https://aclanthology.org/Q19-1026/)
reports that NQ uses real anonymized Google search queries paired with Wikipedia
pages from the top search results, annotated for long and short answers. The
Polish MTEB task is `NQ-PLHardNegatives`, so this retrieval split should be read
as translated or localized open-domain QA retrieval rather than a new Polish NQ
annotation effort.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 251 positive qrels. Queries
average 48.57 characters and documents average 616.77 characters. Examples ask
about the Great Wall, India's Arctic research station, Maze Runner films, Roman
liberal education, and U.S. presidential succession. Most queries are
single-positive, but 48 have multiple positives.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3021 and hit@10 = 0.5500, with 31 positives at rank 1
and 110 in the top 10. Entity names and titles help BM25, but many questions use
short Polish wording while the answer passage contains expanded encyclopedic
context, which lowers exact-match robustness.

### Training Data That May Help

Useful data includes non-overlapping Natural Questions training data, Polish
Wikipedia QA retrieval pairs, MKQA-style multilingual QA, and hard negatives
from entity-related but non-answer passages. Avoid NQ dev/test material and the
specific MTEB hard-negative evaluation records.

### Synthetic Data Guidance

Generate Polish factoid questions from non-evaluation Wikipedia passages. The
positive passage should explicitly contain the answer entity, date, place, or
definition. Synthetic hard negatives should mention related entities without
answering the question.

## Example Data

| Query | Positive document |
| --- | --- |
| którzy byli sędziami tańca na lodzie 2014 (41 chars) | Taniec na lodzie Phillip Schofield i Christine Bleakley powrócili do współobecności. Dean, Torvill i Karen Barber powrócili, by mentorować celebrytów. Robin Cousins, Jason Gardiner, Barber i Ashley Roberts powrócili z odpowie ... [truncated 225 chars](483 chars) |
| kiedy wyjdzie sezon 5 rubinu? (29 chars) | Lista odcinków RWBY RWBY to trwająca amerykańska seria internetowa w stylu anime, stworzona przez Rooster Teeth Productions. Premiera odbyła się 18 lipca 2013 r. Na stronie internetowej Rooster Teeth, a odcinki zostały późnie ... [truncated 225 chars](479 chars) |
| kiedy w alton towers zamknięto koryto z bali? (45 chars) | Korytarz (wieże Alton) The Flume był log Flume w Alton Towers w Staffordshire. Został otwarty w 1981 roku i został odnowiony w 2004 roku, co zbiegło się z jego sponsorowaniem przez Imperial Leather. Przejażdżka była rynną z b ... [truncated 225 chars](460 chars) |
| który grał profesora protona w teorii Wielkiego Wybuchu (55 chars) | Boba Newharta Newhart później zajął się aktorstwem, występując jako psycholog z Chicago, dr Robert Hartley w The Bob Newhart Show w latach 70., a następnie jako karczmarz z Vermont Dick Loudon w serialu Newhart z lat 80. XX w ... [truncated 225 chars](839 chars) |
| ile parków narodowych jest w indiach (36 chars) | Lista parków narodowych Indii Dalsze ustawodawstwo federalne wzmacniające ochronę dzikiej przyrody zostało wprowadzone w latach 80-tych. W lipcu 2017 r. istniały 103 parki narodowe o powierzchni 40 500 km2 (15 600 mil kwadrat ... [truncated 225 chars](285 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Polish |
| Backing dataset | NanoMTEB-Polish |
| Task / split | nq |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish) |
| Source dataset | [mteb/NQ-PLHardNegatives](https://huggingface.co/datasets/mteb/NQ-PLHardNegatives) |
| Language | pl |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 251 |
| Avg positives / query | 1.255 |
| Positives per query (min / median / max) | 1 / 1.0 / 3 |
| Queries with multiple positives | 48 (24.0%) |
| BM25 nDCG@10 | 0.3026 |
| BM25 hit@10 | 0.5500 |
| BM25 Recall@100 | 0.7649 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.6154 |
| Dense hit@10 | 0.8400 |
| Dense Recall@100 | 0.9283 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4363 |
| Reranking hybrid hit@10 | 0.7000 |
| Reranking hybrid Recall@100 | 0.9522 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 9 |
| Query length avg chars | 48.57 |
| Document length avg chars | 616.77 |

### Public Sources

- [Natural Questions: A Benchmark for Question Answering Research](https://aclanthology.org/Q19-1026/), task paper.
- [Natural Questions project page](https://ai.google.com/research/NaturalQuestions/), official dataset page.
- [mteb/NQ-PLHardNegatives](https://huggingface.co/datasets/mteb/NQ-PLHardNegatives), Polish source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish)
- Source task dataset: [mteb/NQ-PLHardNegatives](https://huggingface.co/datasets/mteb/NQ-PLHardNegatives)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Natural Questions: A Benchmark for Question Answering Research | 2019 | task paper | https://aclanthology.org/Q19-1026/ |
| Natural Questions project page | 2019 | project page | https://ai.google.com/research/NaturalQuestions/ |
| mteb/NQ-PLHardNegatives |  | dataset card | https://huggingface.co/datasets/mteb/NQ-PLHardNegatives |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Polish
  backing_dataset: NanoMTEB-Polish
  dataset_id: hakari-bench/NanoMTEB-Polish
  task_name: nq
  split_name: nq
  language: pl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Polish/nq.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone Polish NQ paper was confirmed
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 251
  positives_per_query:
    average: 1.255
    min: 1
    median: 1.0
    max: 3
    multi_positive_queries: 48
    multi_positive_query_percent: 24.0
  text_stats_chars:
    query_mean: 48.565
    document_mean: 616.7722
  bm25:
    ndcg_at_10: 0.30257924207547027
    hit_at_10: 0.55
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3025792421
      hit_at_10: 0.55
      recall_at_100: 0.764940239
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.764940239
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6153768397
      hit_at_10: 0.84
      recall_at_100: 0.9282868526
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9282868526
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4362995432
      hit_at_10: 0.7
      recall_at_100: 0.9521912351
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.045
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9521912351
      safeguard_positive_rows: 9
      rows_with_101_candidates: 9
```
