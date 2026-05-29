# MNanoBEIR / NanoBEIR-vi / NanoSciFact

## Overview

SciFact is scientific claim evidence retrieval. `NanoBEIR-vi__NanoSciFact` uses
Vietnamese translated scientific claims to retrieve abstract evidence.

## Details

### What the Original Data Measures

[SciFact](https://arxiv.org/abs/2004.14974) evaluates scientific claim
verification using abstracts. BEIR uses the retrieval portion, and MMTEB
provides multilingual context.

### Observed Data Profile

The task has 50 queries, 2,919 documents, and 56 qrels. Most queries have one
positive. Queries average 100.06 characters, and documents average 1,489.56
characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.7134 and hit@10 = 0.8600. Median first-positive rank is
1.0, so scientific terminology provides strong anchors.

### Training Data That May Help

Use Vietnamese scientific claim verification, biomedical abstract retrieval, and
multilingual evidence retrieval. Exclude SciFact, BEIR, NanoBEIR, and translated
evaluation claims.

### Synthetic Data Guidance

Generate Vietnamese scientific claims from abstracts with hard negatives that
share entities or methods but do not support the claim.

## Example Data

| Query | Positive document |
| --- | --- |
| Quy định của Ly49Q về chức năng của màng raft trong sự di chuyển của bạch cầu trung tính đến các vị trí viêm. (109 chars) | Các bạch cầu trung tính nhanh chóng trải qua quá trình phân cực và di chuyển theo hướng để xâm nhập vào các vị trí nhiễm trùng và viêm. Ở đây, chúng tôi cho thấy rằng một thụ thể MHC I ức chế, Ly49Q, là rất quan trọng cho sự ... [truncated 225 chars](1134 chars) |
| Liệu pháp kháng retrovirus và tác động của nó đến việc giảm tỷ lệ bệnh lao trên một loạt các mức CD4. (101 chars) | NỀN TẢNG Nhiễm virus suy giảm miễn dịch ở người (HIV) là yếu tố nguy cơ mạnh nhất dẫn đến bệnh lao và đã thúc đẩy sự tái phát của nó, đặc biệt là ở khu vực hạ Sahara châu Phi. Năm 2010, ước tính có 1,1 triệu trường hợp lao mớ ... [truncated 225 chars](2179 chars) |
| Sự điều chỉnh tăng nhanh và biểu hiện cơ bản cao hơn của các gen được kích thích bởi interferon có làm giảm sự sống sót của các nơ-ron tế bào hạt bị nhiễm virus West Nile không? (177 chars) | Mặc dù độ nhạy cảm của các tế bào thần kinh trong não đối với nhiễm trùng vi sinh vật là một yếu tố quyết định chính trong kết quả lâm sàng, nhưng rất ít điều được biết về các yếu tố phân tử điều chỉnh độ nhạy cảm này. Ở đây, ... [truncated 225 chars](1233 chars) |
| Sàng lọc ung thư cổ tử cung nguyên phát với phát hiện HPV có độ nhạy dọc cao hơn so với tế bào học thông thường để phát hiện loạn sản biểu mô cổ tử cung cấp 2? (159 chars) | NỀN TẢNG Sàng lọc ung thư cổ tử cung dựa trên việc xét nghiệm virus papilloma ở người (HPV) làm tăng độ nhạy trong việc phát hiện các tổn thương nội biểu mô cổ tử cung độ cao (độ 2 hoặc 3), nhưng không rõ liệu sự gia tăng này ... [truncated 225 chars](2422 chars) |
| Chặn tương tác giữa TDP-43 và protein phức hợp hô hấp I ND3 và ND6 dẫn đến tăng cường mất neuron do TDP-43 gây ra. (114 chars) | Các đột biến gen trong protein liên kết DNA TAR (TARDBP, còn được gọi là TDP-43) gây ra bệnh xơ cứng teo cơ một bên (ALS), và sự gia tăng hiện diện của TDP-43 (được mã hóa bởi TARDBP) trong tế bào chất là một đặc điểm mô bệnh ... [truncated 225 chars](1368 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-vi |
| Task / split | NanoSciFact |
| Hugging Face dataset | [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi) |
| Language | vi |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,919 |
| Positive qrels | 56 |
| Positives per query avg | 1.12 |
| Positives per query min / median / max | 1 / 1.0 / 4 |
| Multi-positive queries | 4 (8.00%) |
| BM25 nDCG@10 | 0.7134 |
| BM25 hit@10 | 0.8600 |
| BM25 Recall@100 | 0.9107 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.6644 |
| Dense hit@10 | 0.7800 |
| Dense Recall@100 | 0.9107 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.7632 |
| Reranking hybrid hit@10 | 0.8600 |
| Reranking hybrid Recall@100 | 0.9107 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 5 |
| Query length avg chars | 100.06 |
| Document length avg chars | 1,489.56 |

### Public Sources

- [SciFact](https://arxiv.org/abs/2004.14974), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SciFact: Fact or Fiction: Verifying Scientific Claims | 2020 | task paper | https://arxiv.org/abs/2004.14974 |
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
  task_name: NanoSciFact
  split_name: NanoSciFact
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-vi__NanoSciFact.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 2919
    positive_qrels: 56
  positives_per_query:
    average: 1.12
    min: 1
    median: 1.0
    max: 4
    multi_positive_queries: 4
    multi_positive_query_percent: 8.0
  text_stats_chars:
    query_mean: 100.06
    document_mean: 1489.560466
  bm25:
    ndcg_at_10: 0.7133773596512494
    hit_at_10: 0.86
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7133773597
      hit_at_10: 0.86
      recall_at_100: 0.9107142857
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9107142857
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6643905183
      hit_at_10: 0.78
      recall_at_100: 0.9107142857
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9107142857
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.7631645795
      hit_at_10: 0.86
      recall_at_100: 0.9107142857
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.1
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9107142857
      safeguard_positive_rows: 5
      rows_with_101_candidates: 5
```
