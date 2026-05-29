# MNanoBEIR / NanoBEIR-vi / NanoNFCorpus

## Overview

NFCorpus is biomedical and nutrition retrieval. `NanoBEIR-vi__NanoNFCorpus`
uses Vietnamese translated health queries and scientific passages.

## Details

### What the Original Data Measures

[NFCorpus](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf)
uses health information needs with relevance judgments. BEIR includes it as
domain retrieval, and MMTEB provides multilingual context.

### Observed Data Profile

The task has 50 queries, 2,953 documents, and 1,651 qrels. It is highly
multi-positive, averaging 33.02 positives. Queries average 25.30 characters, and
documents average 1,565.89 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3099 and hit@10 = 0.6200. Median first-positive rank is
3.0, so lexical terms help but broad relevant sets still matter.

### Training Data That May Help

Use Vietnamese biomedical retrieval, medical QA, scientific abstract ranking,
and multi-positive supervision. Exclude NFCorpus, BEIR, and NanoBEIR overlaps.

### Synthetic Data Guidance

Generate Vietnamese biomedical keyword queries from scientific passages with
multiple positives for shared conditions or outcomes.

## Example Data

| Query | Positive document |
| --- | --- |
| Lợi ích sức khỏe của các loại hạt (33 chars) | Mục tiêu Nghiên cứu mối quan hệ giữa việc tiêu thụ anh đào và nguy cơ tái phát cơn gout ở những người mắc bệnh gout. Phương pháp Chúng tôi đã tiến hành một nghiên cứu trường hợp chéo để xem xét mối liên hệ của một tập hợp các ... [truncated 225 chars](1732 chars) |
| đạo đức y tế (12 chars) | BỐI CẢNH: Một trong những vấn đề chính trong việc kiểm soát cholesterol huyết thanh thông qua can thiệp chế độ ăn uống dường như là cần cải thiện sự tuân thủ của bệnh nhân. MỤC TIÊU: Khám phá nhiều câu hỏi liên quan đến các r ... [truncated 225 chars](1913 chars) |
| đậu fava (8 chars) | Trong 20 năm qua, sự quan tâm ngày càng tăng đối với sinh hóa, dinh dưỡng và dược lý của L-arginine đã dẫn đến nhiều nghiên cứu sâu rộng để khám phá vai trò dinh dưỡng và điều trị của nó trong việc điều trị và ngăn ngừa các r ... [truncated 225 chars](1275 chars) |
| Thực sự có gì trong món gà viên? (32 chars) | MỤC ĐÍCH: Để xác định thành phần của thịt gà viên từ 2 chuỗi thực phẩm quốc gia. NỀN TẢNG: Thịt gà viên đã trở thành một thành phần chính trong chế độ ăn uống của người Mỹ. Chúng tôi đã tìm cách xác định thành phần hiện tại c ... [truncated 225 chars](765 chars) |
| chất béo bão hòa (16 chars) | Sự quan tâm đã tăng lên về khả năng rằng chế độ ăn uống của mẹ trong thời kỳ mang thai có thể ảnh hưởng đến sự phát triển của các rối loạn dị ứng ở trẻ em. Nghiên cứu tiềm năng hiện tại đã xem xét mối liên hệ giữa việc mẹ tiê ... [truncated 225 chars](1968 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-vi |
| Task / split | NanoNFCorpus |
| Hugging Face dataset | [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi) |
| Language | vi |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,953 |
| Positive qrels | 1,651 |
| Positives per query avg | 33.02 |
| Positives per query min / median / max | 1 / 23.5 / 100 |
| Multi-positive queries | 47 (94.00%) |
| BM25 nDCG@10 | 0.2313 |
| BM25 hit@10 | 0.6000 |
| BM25 Recall@100 | 0.1369 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2445 |
| Dense hit@10 | 0.5800 |
| Dense Recall@100 | 0.1781 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.2638 |
| Reranking hybrid hit@10 | 0.6400 |
| Reranking hybrid Recall@100 | 0.1781 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 4 |
| Query length avg chars | 25.30 |
| Document length avg chars | 1,565.89 |

### Public Sources

- [NFCorpus](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | task paper | https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf |
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
  task_name: NanoNFCorpus
  split_name: NanoNFCorpus
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-vi__NanoNFCorpus.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 2953
    positive_qrels: 1651
  positives_per_query:
    average: 33.02
    min: 1
    median: 23.5
    max: 100
    multi_positive_queries: 47
    multi_positive_query_percent: 94.0
  text_stats_chars:
    query_mean: 25.3
    document_mean: 1565.893667
  bm25:
    ndcg_at_10: 0.23133464816377444
    hit_at_10: 0.6
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2313346482
      hit_at_10: 0.6
      recall_at_100: 0.1368867353
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1368867353
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2444596147
      hit_at_10: 0.58
      recall_at_100: 0.1780738946
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1780738946
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.2638270899
      hit_at_10: 0.64
      recall_at_100: 0.1780738946
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.08
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1780738946
      safeguard_positive_rows: 4
      rows_with_101_candidates: 4
```
