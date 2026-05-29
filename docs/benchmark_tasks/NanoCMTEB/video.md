# NanoCMTEB / video

## Overview

Multi-CPR introduced entertainment-video search as one of its real Alibaba
domain retrieval settings, with human relevance judgments over short
query-passage pairs. This NanoCMTEB split keeps that industrial search flavor:
very short Chinese or mixed-script video queries must retrieve compact video
title or metadata-like records. The observed examples include dance-exam
videos, TV dramas, performer/title searches, animation episodes, and device
troubleshooting clips, so matching often depends on names, titles, seasons, and
script variants rather than long semantic context.

## Details

### What the Original Data Measures

[Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval](https://arxiv.org/abs/2203.03367)
introduces an entertainment-video domain alongside e-commerce and medical
retrieval. The paper states that the data comes from real Alibaba search
systems and includes human annotated query-passage relevance pairs, making the
task an industrial domain-specific retrieval problem rather than a clean QA
dataset.

[C-Pack](https://arxiv.org/abs/2309.07597) includes `VideoRetrieval` in the
C-MTEB retrieval group. This split tests whether embedding models can connect
short, sometimes noisy user searches to video titles, names, casts, and metadata.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrels. Each
query has exactly one positive in the Nano labels. Queries average 7.07
characters and documents average 30.52 characters, though occasional metadata
records are longer. Detected language is mainly Chinese with Japanese, English,
Korean names, romanization, and mixed-script titles.

The examples include dance-exam videos, TV dramas, device troubleshooting
videos, performer/title searches, and animation episodes. Matching often
depends on title normalization, abbreviated forms, model names, or entertainment
entity aliases.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.0400 and hit@10 = 0.0450. It ranks a positive first for 7 queries. Exact
title overlap helps for some examples, but misspellings, romanization, mixed
scripts, and very short queries leave many positives outside the top 10.

### Training Data That May Help

Useful training data includes video search query-title pairs, entertainment
metadata retrieval, title alias tables, multilingual title normalization, and
hard negatives sharing cast members, series names, or episode numbers.

### Synthetic Data Guidance

Synthetic data should generate short video titles and metadata with cast,
series, episode, device, or performer fields, then create abbreviated user
queries. Hard negatives should share series names or people but differ in
episode, season, device model, or media object.

## Example Data

| Query | Positive document |
| --- | --- |
| 游泳和悦悦 (5 chars) | 悦悦游泳20170817 21m (16 chars) |
| 甲状腺的检查 (6 chars) | 科普时间 专业仪器如何检查甲状腺 (16 chars) |
| BAMBINo (7 chars) | bambino2016 恩率 oppa (19 chars) |
| 明天依然爱你泰国电视剧普通话版 (15 chars) | 明天依然爱你 15 (9 chars) |
| 秃鹰档案国语 (6 chars) | 秃鹰档案 杀手行动失败 黑老大凶残霸道 立马派人杀人灭口 (28 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoCMTEB |
| Backing dataset | NanoCMTEB |
| Task / split | video |
| Hugging Face dataset | [hakari-bench/NanoCMTEB](https://huggingface.co/datasets/hakari-bench/NanoCMTEB) |
| Language | zh |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.6897 |
| BM25 hit@10 | 0.8050 |
| BM25 Recall@100 | 0.8950 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8629 |
| Dense hit@10 | 0.9500 |
| Dense Recall@100 | 0.9850 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8103 |
| Reranking hybrid hit@10 | 0.9200 |
| Reranking hybrid Recall@100 | 0.9950 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 7.07 |
| Document length avg chars | 30.52 |

### Public Sources

- [Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval](https://arxiv.org/abs/2203.03367); 2022; Dingkun Long et al.
- [C-Pack: Packed Resources For General Chinese Embeddings](https://arxiv.org/abs/2309.07597); 2024; Shitao Xiao et al.
- [mteb/VideoRetrieval dataset card](https://huggingface.co/datasets/mteb/VideoRetrieval).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoCMTEB](https://huggingface.co/datasets/hakari-bench/NanoCMTEB)
- Source dataset: [mteb/VideoRetrieval](https://huggingface.co/datasets/mteb/VideoRetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval | 2022 | task paper | https://arxiv.org/abs/2203.03367 |
| C-Pack: Packed Resources For General Chinese Embeddings | 2024 | benchmark paper | https://arxiv.org/abs/2309.07597 |
| mteb/VideoRetrieval | unknown | Hugging Face dataset | https://huggingface.co/datasets/mteb/VideoRetrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoCMTEB
  backing_dataset: NanoCMTEB
  dataset_id: hakari-bench/NanoCMTEB
  task_name: video
  split_name: video
  language: zh
  category: natural_language
  document_path: docs/benchmark_tasks/NanoCMTEB/video.md
  source_research:
    primary_source_type: task_paper_and_benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 7.07
    document_mean: 30.5164
  bm25:
    ndcg_at_10: 0.6896746207440746
    hit_at_10: 0.805
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: VideoRetrieval dev
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoCMTEB video queries, qrels, and video metadata passages
    useful_training_data:
    - video search query-title pairs
    - entertainment metadata retrieval pairs
    - multilingual title alias pairs
    - same-series and same-cast hard negatives
    synthetic_data:
      document_generation: compact Chinese video titles and metadata records
      question_generation: short user video-search strings with aliases and romanization
      answerability: positives should identify the intended video or metadata record
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoCMTEB
    source_urls:
    - label: Multi-CPR arXiv
      url: https://arxiv.org/abs/2203.03367
    - label: C-Pack arXiv
      url: https://arxiv.org/abs/2309.07597
    - label: mteb/VideoRetrieval
      url: https://huggingface.co/datasets/mteb/VideoRetrieval
    source_notes: []
  references:
  - title: 'Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval'
    url: https://arxiv.org/abs/2203.03367
    year: 2022
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'C-Pack: Packed Resources For General Chinese Embeddings'
    url: https://arxiv.org/abs/2309.07597
    year: 2024
    is_paper: true
    source_confidence: definitive_benchmark_paper
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6896746207
      hit_at_10: 0.805
      recall_at_100: 0.895
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.895
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8628599086
      hit_at_10: 0.95
      recall_at_100: 0.985
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.985
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8103028152
      hit_at_10: 0.92
      recall_at_100: 0.995
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.005
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.995
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
