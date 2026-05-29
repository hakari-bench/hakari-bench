# NanoVNMTEB / treccovid_vn

## Overview

`treccovid_vn` is the Vietnamese TREC-COVID retrieval task from VN-MTEB.
Queries are translated COVID-19 biomedical information needs, and documents are
translated CORD-19 scientific article passages. The task tests pandemic
literature retrieval for evidence about SARS-CoV-2, COVID-19 treatments,
mechanisms, public-health questions, and clinical guidance.

## Details

### What the Original Data Measures

[TREC-COVID: Constructing a Pandemic Information Retrieval Test Collection](https://arxiv.org/abs/2005.04474)
describes TREC-COVID as a community evaluation over the rapidly growing CORD-19
corpus. The paper emphasizes that pandemic search changes over time, with new
topics, new documents, and evolving relevance judgments across rounds.

[BEIR](https://arxiv.org/abs/2104.08663) includes TREC-COVID as a biomedical IR
task. [VN-MTEB](https://aclanthology.org/2026.findings-eacl.86/) translates and
filters the source data into Vietnamese, so this split evaluates retrieval of
translated COVID-19 scientific literature.

### Observed Data Profile

The Nano split has 44 queries, 10,000 documents, and 4,076 positive qrel rows.
Every query has multiple positives; the average is 92.64 positives per query and
the median and maximum are both 100. Queries average 70.55 characters. Documents
average 1,315.65 characters and are scientific abstracts or article summaries.

Observed examples cover SARS-CoV-2 immunity, cytokine storm mechanisms,
remdesivir treatment, weather effects on coronavirus spread, and triage
guidelines. The positives often include broad COVID-19 abstracts, reviews, and
clinical guidance rather than a single exact answer sentence.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.9169
and hit@10 = 0.9545. COVID-19 terminology, treatment names, and biomedical
phrases provide strong lexical anchors, and the median first relevant rank is 1.

Even with high lexical scores, this remains a broad multi-positive task: a
retriever should surface multiple useful biomedical papers, not merely one
article that repeats the query terms.

### Training Data That May Help

Useful training data includes non-overlapping TREC-COVID rounds where permitted,
CORD-19 biomedical retrieval pairs, COVID-19 literature search logs, biomedical
QA, and translated scientific retrieval data with overlap removed. The
translated test topics, qrels, and positive documents used by this Nano split
should be excluded.

Training should handle temporally evolving medical evidence and should avoid
learning outdated or benchmark-specific relevance judgments as universal truth.

### Synthetic Data Guidance

For document-to-query generation, use non-evaluation COVID-19 and coronavirus
abstracts and generate Vietnamese biomedical information needs about treatments,
transmission, immunity, diagnostics, mechanisms, or guidelines.

For joint generation, create abstract-like biomedical documents and multi-answer
topics with several relevant papers plus same-disease hard negatives. Preserve
virus names, interventions, study populations, outcomes, and uncertainty.

## Example Data

| Query | Positive document |
| --- | --- |
| Chúng ta biết gì về vắc xin mRNA cho vi-rút SARS-CoV-2? (55 chars) | Chống dịch COVID-19: Đánh giá nhanh chẩn đoán, liệu pháp và vắc xin Đại dịch COVID-19 do một chủng virus corona mới, SARS-CoV-2, đã lây nhiễm hơn 4.9 triệu người và gây ra trên 300.000 ca tử vong trên toàn cầu. Sự lan truyền ... [truncated 225 chars](2093 chars) |
| Những chiếc mặt nạ nào là tốt nhất để phòng ngừa nhiễm Covid-19? (64 chars) | Đại dịch SARS, MERS và virus corona chủng mới (COVID-19), các mối đe dọa sức khỏe toàn cầu mới nhất và lớn nhất: chúng ta đã học được gì? MỤC ĐÍCH: Cung cấp tổng quan về ba loại virus corona gây chết người và xác định các lĩn ... [truncated 225 chars](2092 chars) |
| có phải giãn cách xã hội đã ảnh hưởng đến việc làm chậm sự lây lan của COVID-19 không? (86 chars) | Tăng cường phát hiện kết hợp với giãn cách xã hội và quy hoạch năng lực y tế giảm gánh nặng các trường hợp và tử vong do COVID-19: Nghiên cứu khái niệm bằng mô hình mô phỏng tính toán ngẫu nhiên Mục tiêu: Trong bối cảnh không ... [truncated 225 chars](1616 chars) |
| Protein SARS-CoV-2 có tương tác với protein của con người cho thấy tiềm năng là mục tiêu thuốc. Có thuốc đã được phê duyệt có thể được sử dụng lại dựa trên thông tin này không? (176 chars) | Cơ sở phân tử cho sự gắn kết ADP-ribose vào miền Macro-X của Nsp3 của SARS-CoV-2 Virus gây ra COVID-19, SARS-CoV-2, có một bộ gen RNA lớn mã hóa nhiều protein có thể là mục tiêu cho các loại thuốc kháng virus. Một số trong nh ... [truncated 225 chars](841 chars) |
| Những gì chúng ta biết về những người bị nhiễm Covid-19 nhưng không có triệu chứng? (83 chars) | Đường lây truyền của virus corona trên tàu Diamond Princess Đã xảy ra một đợt bùng phát COVID-19 trên tàu du thuyền Diamond Princess vào tháng Giêng và tháng Hai năm 2020. Chúng tôi đã phân tích thông tin về các trường hợp để ... [truncated 225 chars](2094 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoVNMTEB |
| Backing dataset | NanoVNMTEB |
| Task / split | treccovid_vn |
| Hugging Face dataset | [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB) |
| Source dataset | [GreenNode/trec-covid-vn](https://huggingface.co/datasets/GreenNode/trec-covid-vn) |
| Language | vi |
| Category | natural_language |
| Queries | 44 |
| Documents | 10,000 |
| Positive qrels | 4,076 |
| Avg positives / query | 92.64 |
| Positives per query (min / median / max) | 28 / 100 / 100 |
| Queries with multiple positives | 44 (100.00%) |
| BM25 nDCG@10 | 0.2811 |
| BM25 hit@10 | 0.7727 |
| BM25 Recall@100 | 0.2058 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3750 |
| Dense hit@10 | 0.9773 |
| Dense Recall@100 | 0.2463 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3551 |
| Reranking hybrid hit@10 | 0.8864 |
| Reranking hybrid Recall@100 | 0.2588 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 70.55 |
| Document length avg chars | 1,315.65 |

### Public Sources

- [TREC-COVID: Constructing a Pandemic Information Retrieval Test Collection](https://arxiv.org/abs/2005.04474), 2020.
- [TREC-COVID challenge page](https://ir.nist.gov/covidSubmit/), official challenge page.
- [VN-MTEB: Vietnamese Massive Text Embedding Benchmark](https://aclanthology.org/2026.findings-eacl.86/), 2026.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [GreenNode/trec-covid-vn](https://huggingface.co/datasets/GreenNode/trec-covid-vn), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB)
- Source dataset: [GreenNode/trec-covid-vn](https://huggingface.co/datasets/GreenNode/trec-covid-vn)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| TREC-COVID: Constructing a Pandemic Information Retrieval Test Collection | 2020 | arXiv paper | https://arxiv.org/abs/2005.04474 |
| TREC-COVID challenge page |  | project page | https://ir.nist.gov/covidSubmit/ |
| VN-MTEB: Vietnamese Massive Text Embedding Benchmark | 2026 | ACL paper | https://aclanthology.org/2026.findings-eacl.86/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| GreenNode/trec-covid-vn |  | dataset card | https://huggingface.co/datasets/GreenNode/trec-covid-vn |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoVNMTEB
  backing_dataset: NanoVNMTEB
  dataset_id: hakari-bench/NanoVNMTEB
  task_name: treccovid_vn
  split_name: treccovid_vn
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/NanoVNMTEB/treccovid_vn.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2005.04474
    additional_source_urls:
    - https://ir.nist.gov/covidSubmit/
    - https://aclanthology.org/2026.findings-eacl.86/
    - https://arxiv.org/abs/2104.08663
    - https://huggingface.co/datasets/GreenNode/trec-covid-vn
    no_paper_note: null
  counts:
    queries: 44
    documents: 10000
    positive_qrels: 4076
  positives_per_query:
    average: 92.636
    min: 28
    median: 100.0
    max: 100
    multi_positive_queries: 44
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 70.545
    document_mean: 1315.645
  bm25:
    ndcg_at_10: 0.281093225345464
    hit_at_10: 0.7727272727272727
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: translated VN-MTEB TREC-COVID test split from GreenNode/trec-covid-vn
    train_eval_overlap_audit: not_audited
    leakage_note: Exclude translated TREC-COVID-VN test topics, qrels, and positive
      documents used by this Nano split.
    useful_training_data:
    - non-overlapping TREC-COVID rounds and judgments
    - CORD-19 biomedical retrieval pairs
    - COVID-19 literature search and biomedical QA data
    - translated scientific retrieval data with overlap removed
    synthetic_data:
      document_generation: Vietnamese COVID-19 and coronavirus abstracts preserving
        virus names, interventions, populations, outcomes, and uncertainty.
      question_generation: Vietnamese biomedical information needs about treatments,
        transmission, immunity, diagnostics, mechanisms, or guidelines.
      answerability: Each topic should have many relevant papers plus same-disease
        hard negatives.
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoVNMTEB
    source_urls:
    - label: TREC-COVID arXiv
      url: https://arxiv.org/abs/2005.04474
    - label: TREC-COVID challenge page
      url: https://ir.nist.gov/covidSubmit/
    - label: VN-MTEB ACL Anthology
      url: https://aclanthology.org/2026.findings-eacl.86/
    - label: BEIR arXiv
      url: https://arxiv.org/abs/2104.08663
    - label: GreenNode/trec-covid-vn
      url: https://huggingface.co/datasets/GreenNode/trec-covid-vn
    source_notes: []
  references:
  - title: 'TREC-COVID: Constructing a Pandemic Information Retrieval Test Collection'
    url: https://arxiv.org/abs/2005.04474
    year: 2020
    doi: 10.48550/arXiv.2005.04474
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'VN-MTEB: Vietnamese Massive Text Embedding Benchmark'
    url: https://aclanthology.org/2026.findings-eacl.86/
    year: 2026
    doi: 10.18653/v1/2026.findings-eacl.86
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
      Retrieval Models'
    url: https://arxiv.org/abs/2104.08663
    year: 2021
    doi: 10.48550/arXiv.2104.08663
    is_paper: true
    source_confidence: definitive_paper_link
  - title: GreenNode/trec-covid-vn
    url: https://huggingface.co/datasets/GreenNode/trec-covid-vn
    year: null
    doi: null
    is_paper: false
    source_confidence: probably_correct
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2810932253
      hit_at_10: 0.7727272727
      recall_at_100: 0.2058390579
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 44
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2058390579
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3750221655
      hit_at_10: 0.9772727273
      recall_at_100: 0.2463199215
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 44
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2463199215
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3550643016
      hit_at_10: 0.8863636364
      recall_at_100: 0.2588321884
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 44
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2588321884
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
