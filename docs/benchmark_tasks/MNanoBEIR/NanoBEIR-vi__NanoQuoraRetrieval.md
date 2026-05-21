# MNanoBEIR / NanoBEIR-vi / NanoQuoraRetrieval

## Overview

QuoraRetrieval is duplicate-question retrieval. `NanoBEIR-vi__NanoQuoraRetrieval`
uses Vietnamese translated questions to retrieve Vietnamese translated duplicate
questions.

## Details

### What the Original Data Measures

The source is [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs).
BEIR adapts it as duplicate-question retrieval, and MMTEB provides multilingual
context.

### Observed Data Profile

The task has 50 queries, 5,046 documents, and 70 qrels. Ten queries have
multiple positives. Queries average 57.26 characters, and documents average
62.69 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.7236 and hit@10 = 0.9000. Median first-positive rank is
1.0, so many duplicates remain lexically close.

### Training Data That May Help

Use Vietnamese paraphrase retrieval and multilingual duplicate-question data,
excluding Quora, BEIR, NanoBEIR, and translated evaluation pairs.

### Synthetic Data Guidance

Generate Vietnamese paraphrase clusters with hard negatives sharing entities or
phrases but asking a different question.

## Example Data

| Query | Positive document |
| --- | --- |
| Có được cười vào những câu chuyện cười của chính mình không? (60 chars) | Có kỳ lạ không khi cười với những câu đùa của chính mình? (57 chars) |
| Điều dối trá tốt nhất mà bạn từng tạo ra là gì? (47 chars) | Lời nói dối được chế tác tốt nhất mà bạn từng nói là gì? (56 chars) |
| Tại sao Quora thường gợi ý những câu trả lời trong nguồn cấp dữ liệu của tôi chê bai Donald Trump? (98 chars) | Tại sao Quora dường như chỉ có những câu trả lời chủ quan, thiên lệch cho các câu hỏi về Donald Trump? (102 chars) |
| Làm thế nào tôi có thể làm cho cơ thể mình mạnh mẽ? (51 chars) | Làm thế nào để tôi trở nên mạnh mẽ về thể chất? (47 chars) |
| Một vệ tinh lượng tử sẽ hoạt động như thế nào? (46 chars) | Một vệ tinh lượng tử hoạt động như thế nào và một số ứng dụng chính của nó sẽ là gì? (84 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-vi |
| Task / split | NanoQuoraRetrieval |
| Hugging Face dataset | [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi) |
| Language | vi |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,046 |
| Positive qrels | 70 |
| Positives per query avg | 1.40 |
| Positives per query min / median / max | 1 / 1.0 / 6 |
| Multi-positive queries | 10 (20.00%) |
| BM25 nDCG@10 | 0.7236 |
| BM25 hit@10 | 0.9000 |
| Query length avg chars | 57.26 |
| Document length avg chars | 62.69 |

### Public Sources

- [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Quora Question Pairs | 2017 | dataset competition | https://kaggle.com/competitions/quora-question-pairs |
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
  task_name: NanoQuoraRetrieval
  split_name: NanoQuoraRetrieval
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-vi__NanoQuoraRetrieval.md
  source_research: {primary_source_type: benchmark_or_dataset_source, paper_pdf_or_html_checked: true, no_paper_note: No standalone task paper was confirmed; the dataset competition and BEIR benchmark paper are the public sources used here.}
  counts: {queries: 50, documents: 5046, positive_qrels: 70}
  positives_per_query: {average: 1.4, min: 1, median: 1.0, max: 6, multi_positive_queries: 10, multi_positive_query_percent: 20.0}
  text_stats_chars: {query_mean: 57.26, document_mean: 62.691042}
  bm25: {ndcg_at_10: 0.7236441389, hit_at_10: 0.9, source: dataset_bm25_column}
```
