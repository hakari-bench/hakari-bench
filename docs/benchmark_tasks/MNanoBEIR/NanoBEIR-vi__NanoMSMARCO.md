# MNanoBEIR / NanoBEIR-vi / NanoMSMARCO

## Overview

MS MARCO is web passage retrieval. `NanoBEIR-vi__NanoMSMARCO` uses Vietnamese
translated web questions to retrieve answer-bearing passages.

## Details

### What the Original Data Measures

[MS MARCO](https://arxiv.org/abs/1611.09268) uses real web-search questions and
answer passages. BEIR includes it as passage retrieval, and MMTEB provides
multilingual context.

### Observed Data Profile

The task has 50 queries, 5,043 documents, and 50 qrels. Every query has one
positive. Queries average 34.92 characters, and documents average 335.01
characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3423 and hit@10 = 0.5600. Median first-positive rank is
8.5, so answer-aware semantic matching matters.

### Training Data That May Help

Use Vietnamese web QA, query logs, and multilingual passage retrieval. Exclude
MS MARCO, BEIR, NanoBEIR, and translated overlaps.

### Synthetic Data Guidance

Generate concise Vietnamese web queries from answer passages, with term-sharing
hard negatives that do not answer the question.

## Example Data

| Query | Positive document |
| --- | --- |
| hội chứng suy nghĩ lặp lại là gì (32 chars) | Hội chứng nhai lại. Hội chứng nhai lại, còn được gọi là Merycism, là một loại rối loạn ăn uống không được xác định cụ thể nào khác, gây ra việc trào ngược thức ăn. Mặc dù nó không được xác định là một rối loạn ăn uống cụ thể ... [truncated 225 chars](296 chars) |
| ai đã hát bài here i go again (29 chars) | Đối với các mục đích khác, xem Here I Go Again (phân định). Here I Go Again là một bài hát của ban nhạc rock người Anh Whitesnake. Ban đầu được phát hành trong album năm 1982 của họ, Saints & Sinners, bài hát đã được thu âm l ... [truncated 225 chars](355 chars) |
| ai là người mà cameron boyce đóng trong liv và maddie (53 chars) | Chuẩn bị cho những tiếng cười nghiêng ngả, các bạn ơi. Trong một đoạn clip độc quyền của tập phim ngày 19 tháng 4 của Liv & Maddie có tên “Prom-A-Rooney.” Rõ ràng rồi. Trong đoạn clip hài hước này, chúng ta thấy ngôi sao Jess ... [truncated 225 chars](349 chars) |
| các sa mạc lớn của trái đất chủ yếu xảy ra ở đâu (48 chars) | Phần còn lại của các sa mạc trên Trái Đất nằm ngoài các khu vực cực. Sa mạc lớn nhất là Sa mạc Sahara, một sa mạc cận nhiệt đới ở Bắc Phi. (138 chars) |
| nghĩa của từ "copper" trong tiếng lóng chỉ cảnh sát (51 chars) | Dựa trên những phát hiện hiện tại, có vẻ như từ "copper" (một cảnh sát, nghĩa đen là 'người bắt giữ') có trước từ "cop" (có thể được sử dụng bằng lời và có nghĩa là bắt giữ hoặc khi là danh từ có nghĩa là một cảnh sát). Có th ... [truncated 225 chars](408 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-vi |
| Task / split | NanoMSMARCO |
| Hugging Face dataset | [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi) |
| Language | vi |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,043 |
| Positive qrels | 50 |
| BM25 nDCG@10 | 0.3423 |
| BM25 hit@10 | 0.5600 |
| BM25 Recall@100 | 0.9200 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4934 |
| Dense hit@10 | 0.6800 |
| Dense Recall@100 | 1.0000 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4454 |
| Reranking hybrid hit@10 | 0.6800 |
| Reranking hybrid Recall@100 | 0.9800 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 34.92 |
| Document length avg chars | 335.01 |

### Public Sources

- [MS MARCO](https://arxiv.org/abs/1611.09268), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MS MARCO: A Human Generated MAchine Reading COmprehension Dataset | 2016 | task paper | https://arxiv.org/abs/1611.09268 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: MNanoBEIR
  backing_dataset: NanoBEIR-vi
  dataset_id: hakari-bench/NanoBEIR-vi
  task_name: NanoMSMARCO
  split_name: NanoMSMARCO
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-vi__NanoMSMARCO.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 5043
    positive_qrels: 50
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 34.92
    document_mean: 335.008725
  bm25:
    ndcg_at_10: 0.34232813811772245
    hit_at_10: 0.56
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3423281381
      hit_at_10: 0.56
      recall_at_100: 0.92
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.92
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4934200557
      hit_at_10: 0.68
      recall_at_100: 1.0
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4454273106
      hit_at_10: 0.68
      recall_at_100: 0.98
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.02
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.98
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
