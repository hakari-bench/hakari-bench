# MNanoBEIR / NanoBEIR-vi / NanoSCIDOCS

## Overview

SCIDOCS is scientific-document retrieval. `NanoBEIR-vi__NanoSCIDOCS` uses
Vietnamese translated paper-title style queries to retrieve scientific abstracts.

## Details

### What the Original Data Measures

[SPECTER](https://arxiv.org/abs/2004.07180) evaluates scientific document
representations over SCIDOCS. BEIR includes it as scientific retrieval, and
MMTEB provides multilingual context.

### Observed Data Profile

The task has 50 queries, 2,210 documents, and 244 qrels. Every query is
multi-positive, usually 3 to 5 positives. Queries average 76.14 characters, and
documents average 952.55 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.2839 and hit@10 = 0.8000. Median first-positive rank is
3.0, so scientific topical matching remains important.

### Training Data That May Help

Use non-overlapping scientific retrieval, citation ranking, Vietnamese
abstracts, and multilingual academic search. Exclude SCIDOCS, SPECTER
evaluation data, BEIR, and NanoBEIR.

### Synthetic Data Guidance

Generate Vietnamese paper-title queries from abstracts, with same-field hard
negatives that describe different contributions.

## Example Data

| Query | Positive document |
| --- | --- |
| Bộ chuyển đổi tăng áp đa mức DC-DC mới (38 chars) | Tóm tắt: Các bộ chuyển đổi nguồn điện đa mức đang nổi lên như một loại tùy chọn bộ chuyển đổi năng lượng mới cho các ứng dụng công suất cao. Các bộ chuyển đổi nguồn điện đa mức thường tổng hợp sóng điện áp bậc thang từ nhiều ... [truncated 225 chars](920 chars) |
| Học Lĩnh Vực Ngẫu Nhiên Markov Gauss Thưa Nhanh Dựa Trên Phân Tích Cholesky (75 chars) | Văn bản đã được dịch: (21 chars) |
| Tổng hợp kết cấu sử dụng mạng nơ-ron tích chập (46 chars) | Trong công trình này, chúng tôi nghiên cứu ảnh hưởng của độ sâu của mạng nơ-ron tích chập đến độ chính xác của nó trong bối cảnh nhận diện hình ảnh quy mô lớn. Đóng góp chính của chúng tôi là một đánh giá kỹ lưỡng về các mạng ... [truncated 225 chars](908 chars) |
| Antenna vòng tròn băng thông phẳng với phân cực tròn cho hệ thống RFID (70 chars) | Trong bài báo này, một kỹ thuật cấp nguồn dải uốn ngang (HMS) được đề xuất để đạt được sự khớp trở tốt và các mô hình bức xạ đối xứng cho một ăng-ten patch xếp chồng phân cực tròn băng thông rộng được cấp nguồn đơn, phù hợp c ... [truncated 225 chars](1256 chars) |
| Thiết kế máy theo dõi nhịp tim kỹ thuật số tiên tiến sử dụng các linh kiện điện tử cơ bản (89 chars) | Trong bài báo này, chúng tôi trình bày thiết kế và phát triển một thiết bị tích hợp mới để đo nhịp tim bằng đầu ngón tay nhằm cải thiện việc ước lượng nhịp tim. Khi các bệnh liên quan đến tim mạch ngày càng gia tăng, nhu cầu ... [truncated 225 chars](1160 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-vi |
| Task / split | NanoSCIDOCS |
| Hugging Face dataset | [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi) |
| Language | vi |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,210 |
| Positive qrels | 244 |
| Positives per query avg | 4.88 |
| Positives per query min / median / max | 3 / 5.0 / 5 |
| Multi-positive queries | 50 (100.00%) |
| BM25 nDCG@10 | 0.2839 |
| BM25 hit@10 | 0.8000 |
| BM25 Recall@100 | 0.6311 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3201 |
| Dense hit@10 | 0.7200 |
| Dense Recall@100 | 0.5779 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3202 |
| Reranking hybrid hit@10 | 0.8000 |
| Reranking hybrid Recall@100 | 0.6639 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 76.14 |
| Document length avg chars | 952.55 |

### Public Sources

- [SPECTER](https://arxiv.org/abs/2004.07180), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SPECTER: Document-level Representation Learning using Citation-informed Transformers | 2020 | task paper | https://arxiv.org/abs/2004.07180 |
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
  task_name: NanoSCIDOCS
  split_name: NanoSCIDOCS
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-vi__NanoSCIDOCS.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 2210
    positive_qrels: 244
  positives_per_query:
    average: 4.88
    min: 3
    median: 5.0
    max: 5
    multi_positive_queries: 50
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 76.14
    document_mean: 952.545701
  bm25:
    ndcg_at_10: 0.28393793836357395
    hit_at_10: 0.8
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2839379384
      hit_at_10: 0.8
      recall_at_100: 0.631147541
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.631147541
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3200653777
      hit_at_10: 0.72
      recall_at_100: 0.5778688525
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5778688525
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3202252994
      hit_at_10: 0.8
      recall_at_100: 0.6639344262
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6639344262
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
