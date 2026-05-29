# NanoVNMTEB / scidocs_vn

## Overview

`scidocs_vn` is the Vietnamese SciDocs retrieval task from VN-MTEB. Queries are
translated scientific paper titles or short paper descriptions, and documents
are translated scientific document abstracts. The task tests related-paper
retrieval for citation, co-citation, and recommendation-style scientific
document matching.

## Details

### What the Original Data Measures

[SPECTER: Document-level Representation Learning using Citation-informed Transformers](https://arxiv.org/abs/2004.07180)
introduces SciDocs as an evaluation benchmark with seven document-level tasks,
including citation prediction, document classification, user activity, and
recommendation. The paper emphasizes scientific document-level representations
and uses citations as a signal of document relatedness.

[BEIR](https://arxiv.org/abs/2104.08663) includes SciDocs as a scientific
retrieval task. [VN-MTEB](https://aclanthology.org/2026.findings-eacl.86/)
translates and filters the source data into Vietnamese, so the retrieval task
mixes Vietnamese scientific prose with preserved technical names.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 988 positive qrel rows.
Every query is multi-positive: the average is 4.94 positives per query, with a
minimum of 3 and a maximum of 5. Queries average 73.36 characters. Documents
average 1,226.73 characters and are long scientific or technical abstracts.

Observed examples include MATLAB tools for electric-vehicle design, DSP image
processing with OpenCV, fingerprint matching with FingerCode, Bitcoin
transaction fees, and agile productivity factors. Positives may be related by
scientific topic or citation context rather than direct answerability.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.1396
and hit@10 = 0.4650, making this one of the hardest NanoVNMTEB tasks observed so
far. The median first relevant BM25 rank is 17.

The task is difficult because citation and recommendation relevance often
depends on methodological or topical relatedness that is not captured by exact
surface overlap. Technical keywords can also lead to same-domain but unrelated
papers.

### Training Data That May Help

Useful training data includes non-overlapping SciDocs training or evaluation
signals where permitted, scientific citation pairs, co-citation pairs,
paper-recommendation logs, and translated scientific abstract retrieval data
with overlap removed. The translated test queries, qrels, and positive abstracts
used by this Nano split should be excluded.

Multi-positive objectives are important because each query has several related
documents.

### Synthetic Data Guidance

For document-to-query generation, use non-evaluation scientific abstracts and
generate Vietnamese paper titles or related-work queries that ask for similar
methods, datasets, applications, or evaluation settings.

For joint generation, create clusters of scientific abstracts with shared
methodology or citation rationale, plus same-field hard negatives. Preserve
technical terms, datasets, algorithms, and application domains.

## Example Data

| Query | Positive document |
| --- | --- |
| Phân tích hành vi của mã độc Android (36 chars) | Về chứng nhận ứng dụng điện thoại di động nhẹ Người dùng đã bắt đầu tải về một số lượng ngày càng lớn các ứng dụng cho điện thoại di động để đáp ứng với sự tiến bộ trong các thiết bị cầm tay và mạng không dây. Số lượng ứng dụ ... [truncated 225 chars](1361 chars) |
| Liên kết một từ điển ngữ nghĩa với Wordnet và chuyển đổi sang Wordnet-LMF (73 chars) | Học cách bản đồ giữa các từ vựng trên Web ngữ nghĩa Các ngữ nghĩa học đóng một vai trò nổi bật trong Semantic Web. Chúng cho phép xuất bản dữ liệu có thể hiểu được bởi máy tính, mở ra nhiều cơ hội để xử lý thông tin tự động. ... [truncated 225 chars](2024 chars) |
| Mô tả tính độ tin cậy của phần cứng điện toán đám mây (53 chars) | Xu hướng thất bại trong một quần thể ổ đĩa lớn Được ước tính rằng trên 90% thông tin mới được sản xuất ra trên thế giới đang lưu trữ trên các phương tiện từ tính, hầu hết là trên ổ cứng. Mặc dù sự quan trọng của họ, có tương ... [truncated 225 chars](1462 chars) |
| Nhận diện thói quen hàng ngày qua các hoạt động (47 chars) | Phát hiện nhanh đối tượng sử dụng tăng cường của thác đơn giản tính năng Bài báo này mô tả một phương pháp tiếp cận học máy cho việc phát hiện vật thể hình ảnh có khả năng xử lý hình ảnh cực nhanh và đạt được tỷ lệ phát hiện ... [truncated 225 chars](1359 chars) |
| VELNET (Môi trường ảo cho học tập mạng) (39 chars) | Môi trường học tập ảo trên mạng: Một khung nghiên cứu và đánh giá sơ bộ về hiệu quả trong việc đào tạo kỹ năng CNTT cơ bản Việc sử dụng của bạn đối với kho lưu trữ JSTOR cho thấy sự chấp nhận của bạn các Điều khoản và Điều ki ... [truncated 225 chars](619 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoVNMTEB |
| Backing dataset | NanoVNMTEB |
| Task / split | scidocs_vn |
| Hugging Face dataset | [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB) |
| Source dataset | [GreenNode/scidocs-vn](https://huggingface.co/datasets/GreenNode/scidocs-vn) |
| Language | vi |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 988 |
| Avg positives / query | 4.94 |
| Positives per query (min / median / max) | 3 / 5 / 5 |
| Queries with multiple positives | 200 (100.00%) |
| BM25 nDCG@10 | 0.1613 |
| BM25 hit@10 | 0.5200 |
| BM25 Recall@100 | 0.3806 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2028 |
| Dense hit@10 | 0.5800 |
| Dense Recall@100 | 0.4565 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.2039 |
| Reranking hybrid hit@10 | 0.5650 |
| Reranking hybrid Recall@100 | 0.4676 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 26 |
| Query length avg chars | 73.36 |
| Document length avg chars | 1,226.73 |

### Public Sources

- [SPECTER: Document-level Representation Learning using Citation-informed Transformers](https://arxiv.org/abs/2004.07180), 2020.
- [SciDocs dataset page](https://allenai.org/data/scidocs), official dataset page.
- [VN-MTEB: Vietnamese Massive Text Embedding Benchmark](https://aclanthology.org/2026.findings-eacl.86/), 2026.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [GreenNode/scidocs-vn](https://huggingface.co/datasets/GreenNode/scidocs-vn), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB)
- Source dataset: [GreenNode/scidocs-vn](https://huggingface.co/datasets/GreenNode/scidocs-vn)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SPECTER: Document-level Representation Learning using Citation-informed Transformers | 2020 | arXiv paper | https://arxiv.org/abs/2004.07180 |
| SciDocs dataset page |  | project page | https://allenai.org/data/scidocs |
| VN-MTEB: Vietnamese Massive Text Embedding Benchmark | 2026 | ACL paper | https://aclanthology.org/2026.findings-eacl.86/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| GreenNode/scidocs-vn |  | dataset card | https://huggingface.co/datasets/GreenNode/scidocs-vn |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoVNMTEB
  backing_dataset: NanoVNMTEB
  dataset_id: hakari-bench/NanoVNMTEB
  task_name: scidocs_vn
  split_name: scidocs_vn
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/NanoVNMTEB/scidocs_vn.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2004.07180
    additional_source_urls:
    - https://allenai.org/data/scidocs
    - https://aclanthology.org/2026.findings-eacl.86/
    - https://arxiv.org/abs/2104.08663
    - https://huggingface.co/datasets/GreenNode/scidocs-vn
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 988
  positives_per_query:
    average: 4.94
    min: 3
    median: 5.0
    max: 5
    multi_positive_queries: 200
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 73.355
    document_mean: 1226.728
  bm25:
    ndcg_at_10: 0.1613400597766722
    hit_at_10: 0.52
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: translated VN-MTEB SCIDOCS test split from GreenNode/scidocs-vn
    train_eval_overlap_audit: not_audited
    leakage_note: Exclude translated SCIDOCS-VN test queries, qrels, and positive
      abstracts used by this Nano split.
    useful_training_data:
    - non-overlapping SciDocs citation and recommendation signals
    - scientific citation and co-citation pairs
    - paper-recommendation logs with overlap removed
    - translated scientific abstract retrieval data with overlap removed
    synthetic_data:
      document_generation: Vietnamese scientific abstracts preserving technical terms,
        datasets, algorithms, and application domains.
      question_generation: Vietnamese paper-title or related-work queries asking for
        similar methods, datasets, applications, or evaluation settings.
      answerability: Each query should have multiple related papers and same-field
        hard negatives.
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoVNMTEB
    source_urls:
    - label: SPECTER/SciDocs arXiv
      url: https://arxiv.org/abs/2004.07180
    - label: SciDocs dataset page
      url: https://allenai.org/data/scidocs
    - label: VN-MTEB ACL Anthology
      url: https://aclanthology.org/2026.findings-eacl.86/
    - label: BEIR arXiv
      url: https://arxiv.org/abs/2104.08663
    - label: GreenNode/scidocs-vn
      url: https://huggingface.co/datasets/GreenNode/scidocs-vn
    source_notes: []
  references:
  - title: 'SPECTER: Document-level Representation Learning using Citation-informed
      Transformers'
    url: https://arxiv.org/abs/2004.07180
    year: 2020
    doi: 10.48550/arXiv.2004.07180
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
  - title: GreenNode/scidocs-vn
    url: https://huggingface.co/datasets/GreenNode/scidocs-vn
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
      ndcg_at_10: 0.1613400598
      hit_at_10: 0.52
      recall_at_100: 0.3805668016
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.3805668016
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2028299676
      hit_at_10: 0.58
      recall_at_100: 0.4564777328
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4564777328
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.2038882997
      hit_at_10: 0.565
      recall_at_100: 0.467611336
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.13
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.467611336
      safeguard_positive_rows: 26
      rows_with_101_candidates: 26
```
