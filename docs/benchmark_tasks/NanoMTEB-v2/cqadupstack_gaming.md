# NanoMTEB-v2 / cqadupstack_gaming

## Overview

CQADupStack defines retrieval over StackExchange duplicate-question links, and
the Gaming slice applies that setup to player questions and game-specific
problem reports. In this NanoMTEB-v2 task, short Gaming StackExchange titles
retrieve longer candidate posts that ask the same or near-duplicate question.
Because the corpus mixes game names, quests, mechanics, platforms, versions,
and spoiler-prone descriptions, a retriever must identify the same player
intent rather than only match a popular title or generic gameplay term.

## Details

### What the Original Data Measures

[CQADupStack](https://eltimster.github.io/www/pubs/adcs2015.pdf) is a benchmark
for community question-answering research built from StackExchange subforums and
annotated with duplicate-question links. The paper provides predefined retrieval
and classification splits. [MTEB](https://arxiv.org/abs/2210.07316) includes
CQADupStack retrieval variants, including Gaming, as short-query retrieval tasks.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 415 positive qrels. Queries
average 47.62 characters, while documents average 481.08 characters and contain
question titles plus body text. Positives average 2.08 per query, but the median
is 1 and one query has 22 positives.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.4888 and hit@10 = 0.6850. It ranks 81 queries with a positive first, and the
median best positive rank is 3. The task is often lexical because game names and
mechanics repeat, but duplicate questions may phrase the same gameplay issue
with different wording.

### Training Data That May Help

Useful data includes StackExchange duplicate-question pairs, gaming FAQ pairs,
short-title-to-long-question retrieval data, and hard negatives from the same
game or tag.

### Synthetic Data Guidance

Generate several differently worded questions about the same game mechanic, and
include hard negatives from the same game that ask about a different mechanic.

## Example Data

| Query | Positive document |
| --- | --- |
| How can a monk tank effectively for a group? (44 chars) | Monk skills suited for CC and tanking > **Possible Duplicate:** > How can a monk tank effectively for a group? When playing with my friends (who play ranged classes), I mostly end up tanking / crowd controlling with my monk. ... [truncated 225 chars](298 chars) |
| Portal 2 Offline Co-op on Mac (29 chars) | Can we play Portal 2 co-op on one PC or Mac? Is there a way to play Portal 2 co-op on a single PC or Mac? If so, do we need two keyboards, or two mice, or what? Do we need to buy two copies of the game? Note: The _wireless_ X ... [truncated 225 chars](389 chars) |
| What type of buildings offer what level of jobs? (48 chars) | Who works in medium value commercial properties? I have some §§ (medium-wealth) buildings that are closed or closing due to a lack of workers. Yet, of my 10,652 §§ workers, 3,205 are unemployed and 152 are commuting out. This ... [truncated 225 chars](305 chars) |
| At what rate do players and commanders receive resources per resource node? (75 chars) | How are resources gained, distributed, and spent? > **Possible Duplicate:** > At what rate do players and commanders receive resources per resource node? I'm unclear on how resources gained by aliens and marines are gained an ... [truncated 225 chars](1478 chars) |
| How many forms of Vivilion are there? (37 chars) | Vivillon's Pattern 3DS Locations - Who do I need to trade with? According to Vivillon's Pokedex Entry, they have different wing patterns depending on their original location in the world: > Vivillon with many different patter ... [truncated 225 chars](765 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-v2 |
| Backing dataset | NanoMTEB-v2 |
| Task / split | cqadupstack_gaming |
| Source task | CQADupstackGamingRetrieval |
| Hugging Face dataset | [hakari-bench/NanoMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2) |
| Source dataset | [mteb/cqadupstack-gaming](https://huggingface.co/datasets/mteb/cqadupstack-gaming) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 415 |
| Positives per query | avg 2.08, min 1, median 1, max 22 |
| Multi-positive queries | 65 (32.50%) |
| BM25 nDCG@10 | 0.5073 |
| BM25 hit@10 | 0.6850 |
| BM25 Recall@100 | 0.7759 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.6375 |
| Dense hit@10 | 0.7900 |
| Dense Recall@100 | 0.8506 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.5970 |
| Reranking hybrid hit@10 | 0.7800 |
| Reranking hybrid Recall@100 | 0.8771 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 10 |
| Query length avg chars | 47.62 |
| Document length avg chars | 481.08 |

### Public Sources

- [CQADupStack](https://eltimster.github.io/www/pubs/adcs2015.pdf).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316).
- [mteb/cqadupstack-gaming](https://huggingface.co/datasets/mteb/cqadupstack-gaming).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2)
- Source dataset: [mteb/cqadupstack-gaming](https://huggingface.co/datasets/mteb/cqadupstack-gaming)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | source task paper | https://eltimster.github.io/www/pubs/adcs2015.pdf |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| mteb/cqadupstack-gaming | 2024 | dataset card | https://huggingface.co/datasets/mteb/cqadupstack-gaming |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-v2
  backing_dataset: NanoMTEB-v2
  dataset_id: hakari-bench/NanoMTEB-v2
  task_name: cqadupstack_gaming
  split_name: cqadupstack_gaming
  source_task: CQADupstackGamingRetrieval
  source_dataset_id: mteb/cqadupstack-gaming
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-v2/cqadupstack_gaming.md
  source_research:
    primary_source_type: task_paper_and_benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 415
  positives_per_query:
    average: 2.075
    min: 1
    median: 1.0
    max: 22
    multi_positive_queries: 65
    multi_positive_query_percent: 32.5
  text_stats_chars:
    query_mean: 47.62
    document_mean: 481.0841
  bm25:
    ndcg_at_10: 0.5072558726076217
    hit_at_10: 0.685
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: MTEB CQADupStack Gaming test split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoMTEB-v2 cqadupstack_gaming duplicate-question pairs
    useful_training_data:
    - StackExchange duplicate-question pairs
    - gaming forum duplicate questions
    - same-game hard negatives
    synthetic_data:
      document_generation: long forum questions about game mechanics
      question_generation: short duplicate-style gaming question titles
      answerability: positive should be a duplicate or near-duplicate question
    multi_positive_training: recommended
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2
    source_urls:
    - label: CQADupStack paper
      url: https://eltimster.github.io/www/pubs/adcs2015.pdf
    - label: MTEB arXiv
      url: https://arxiv.org/abs/2210.07316
    - label: mteb/cqadupstack-gaming
      url: https://huggingface.co/datasets/mteb/cqadupstack-gaming
    source_notes: []
  references:
  - title: 'CQADupStack: A Benchmark Data Set for Community Question-Answering Research'
    url: https://eltimster.github.io/www/pubs/adcs2015.pdf
    year: 2015
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'MTEB: Massive Text Embedding Benchmark'
    url: https://arxiv.org/abs/2210.07316
    year: 2023
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5072558726
      hit_at_10: 0.685
      recall_at_100: 0.7759036145
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7759036145
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6374744295
      hit_at_10: 0.79
      recall_at_100: 0.8506024096
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8506024096
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.5970008563
      hit_at_10: 0.78
      recall_at_100: 0.8771084337
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.05
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8771084337
      safeguard_positive_rows: 10
      rows_with_101_candidates: 10
```
