# NanoVNMTEB / quora_vn

## Overview

VN-MTEB turns the Quora duplicate-question retrieval task into Vietnamese using
its translation and filtering pipeline. The source task comes from Quora
Question Pairs as used by BEIR, where relevance means semantic duplication
rather than answer relevance. In this Nano split, translated Vietnamese
questions retrieve translated candidate questions, often with multiple
duplicates per query. The sampled data includes everyday and factual questions
plus translation artifacts, so the model must find paraphrased duplicates
without relying on exact wording.

## Details

### What the Original Data Measures

No standalone task paper was confirmed for the original Quora Question Pairs
release. The interpretation here is based on the official Quora data release
page, the [BEIR](https://arxiv.org/abs/2104.08663) benchmark paper, VN-MTEB,
and observed samples. BEIR describes Quora as duplicate-question retrieval and
states that the original release contains 404,290 question pairs; BEIR adds
transitive closures, splits the data, removes split overlaps, and ensures a
question in one split does not appear in another.

[VN-MTEB](https://aclanthology.org/2026.findings-eacl.86/) translates and
filters the source data into Vietnamese. This makes the task a translated
duplicate-question retrieval benchmark rather than native Vietnamese Quora data.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 452 positive qrel rows.
The average is 2.26 positives per query; 67 queries have multiple positives and
the maximum is 57. Queries average 76.51 characters. Documents average 129.22
characters, much shorter than the scientific and argument-retrieval tasks.

Observed examples include morning routines, the Pentagon Papers, India's
surgical strike, weight loss, and nightmares. Some positive documents contain
translation-helper framing such as "I want to translate this sentence...", so
models should tolerate noisy translated wrappers while still matching the
underlying duplicate question.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.8626
and hit@10 = 0.9800. Short duplicate questions often share key words, and the
median first relevant rank is 1.

The hard cases are paraphrases or noisy translations where the same question is
embedded inside extra text. nDCG remains useful because some queries have many
duplicates and the best system should rank several variants highly.

### Training Data That May Help

Useful training data includes non-overlapping Quora duplicate-question pairs,
Vietnamese duplicate-question and paraphrase data, translated duplicate pairs
with overlap removed, and hard negatives that share entities but ask different
intents. The translated test questions, qrels, and positive questions used by
this Nano split should be excluded.

Because one third of queries have multiple positives, multi-positive training is
more faithful than forcing one duplicate per query.

### Synthetic Data Guidance

For document-to-query generation, use non-evaluation question pairs and create
Vietnamese paraphrases that preserve the same user intent. Include natural
duplicates, noisy translated variants, and short forum-style wording.

For joint generation, create clusters of equivalent Vietnamese questions plus
near duplicates that share keywords but ask a different relation or decision.
Do not seed generation from this evaluation split.

## Example Data

| Query | Positive document |
| --- | --- |
| Xiaomi Redmi note 4 ra mắt ở Ấn Độ vào ngày nào? (48 chars) | Hãy chuyển câu này sang tiếng Việt: Khi nào Xiaomi Redmi note 4 sẽ ra mắt ở Ấn Độ? (83 chars) |
| Có khả năng Trump sẽ thắng cuộc bầu cử không? (45 chars) | Nếu bạn muốn dịch câu này sang tiếng Việt, hãy viết câu đó ở dưới này. Trump có cơ hội thắng cử không? (103 chars) |
| Có nên thực hiện một phim truyền hình dựa trên bộ phim Shiva Trilogy? (69 chars) | Chào các bạn, Nếu bộ ba Shiva được chuyển thể thành một series phim truyền hình thì nó sẽ như thế nào? (103 chars) |
| Donald Trump bị một số phương tiện truyền thông gọi là "điên" vì những hành vi của ông ta. Bạn có nghĩ Donald Trump mắc bệnh tâm thần không? (140 chars) | Mạng xã hội còn có thể được sử dụng để tìm kiếm các dịch vụ và sản phẩm mới. Donald Trump có ổn định về mặt tinh thần không? (125 chars) |
| Trang Facebook của bạn trai tôi đã bị hack và anh ấy không còn truy cập được email của mình nữa vì nó được thiết lập bởi người yêu cũ và Hotmail sẽ không thiết lập lại vì chúng tôi không có đủ thông tin. Các bạn có gợi ý gì k ... [truncated 225 chars](230 chars) | Tất cả các trường trên đều là những trường tư thục. Trang Facebook của bạn trai tôi đã bị hack và anh ta không còn quyền truy cập vào email vì nó được thiết lập bởi bạn gái cũ của anh ta và Hotmail sẽ không đặt lại nó vì chún ... [truncated 225 chars](366 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoVNMTEB |
| Backing dataset | NanoVNMTEB |
| Task / split | quora_vn |
| Hugging Face dataset | [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB) |
| Source dataset | [GreenNode/quora-vn](https://huggingface.co/datasets/GreenNode/quora-vn) |
| Language | vi |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 452 |
| Avg positives / query | 2.26 |
| Positives per query (min / median / max) | 1 / 1 / 57 |
| Queries with multiple positives | 67 (33.50%) |
| BM25 nDCG@10 | 0.8345 |
| BM25 hit@10 | 0.9600 |
| BM25 Recall@100 | 0.9403 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8259 |
| Dense hit@10 | 0.9350 |
| Dense Recall@100 | 0.9049 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8510 |
| Reranking hybrid hit@10 | 0.9600 |
| Reranking hybrid Recall@100 | 0.9624 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 76.51 |
| Document length avg chars | 129.22 |

### Public Sources

- [First Quora Dataset Release: Question Pairs](https://quoradata.quora.com/First-Quora-Dataset-Release-Question-Pairs), official data release.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [VN-MTEB: Vietnamese Massive Text Embedding Benchmark](https://aclanthology.org/2026.findings-eacl.86/), 2026.
- [GreenNode/quora-vn](https://huggingface.co/datasets/GreenNode/quora-vn), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB)
- Source dataset: [GreenNode/quora-vn](https://huggingface.co/datasets/GreenNode/quora-vn)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| First Quora Dataset Release: Question Pairs |  | dataset release | https://quoradata.quora.com/First-Quora-Dataset-Release-Question-Pairs |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| VN-MTEB: Vietnamese Massive Text Embedding Benchmark | 2026 | ACL paper | https://aclanthology.org/2026.findings-eacl.86/ |
| GreenNode/quora-vn |  | dataset card | https://huggingface.co/datasets/GreenNode/quora-vn |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoVNMTEB
  backing_dataset: NanoVNMTEB
  dataset_id: hakari-bench/NanoVNMTEB
  task_name: quora_vn
  split_name: quora_vn
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/NanoVNMTEB/quora_vn.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2104.08663
    additional_source_urls:
    - https://quoradata.quora.com/First-Quora-Dataset-Release-Question-Pairs
    - https://aclanthology.org/2026.findings-eacl.86/
    - https://huggingface.co/datasets/GreenNode/quora-vn
    no_paper_note: No standalone Quora retrieval task paper was confirmed; BEIR and
      the official Quora data release describe the source task.
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 452
  positives_per_query:
    average: 2.26
    min: 1
    median: 1.0
    max: 57
    multi_positive_queries: 67
    multi_positive_query_percent: 33.5
  text_stats_chars:
    query_mean: 76.51
    document_mean: 129.215
  bm25:
    ndcg_at_10: 0.8345337070261717
    hit_at_10: 0.96
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: translated VN-MTEB Quora test split from GreenNode/quora-vn
    train_eval_overlap_audit: not_audited
    leakage_note: Exclude translated Quora-VN test questions, qrels, and positive
      duplicate questions used by this Nano split.
    useful_training_data:
    - non-overlapping Quora duplicate-question pairs
    - Vietnamese duplicate-question and paraphrase data
    - translated duplicate-question pairs with overlap removed
    - same-entity hard negatives with different intent
    synthetic_data:
      document_generation: Vietnamese forum-style questions and noisy translated variants.
      question_generation: Vietnamese paraphrases preserving the same user intent.
      answerability: Equivalent questions should be clustered, with same-keyword non-duplicates
        as hard negatives.
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoVNMTEB
    source_urls:
    - label: Quora Question Pairs release
      url: https://quoradata.quora.com/First-Quora-Dataset-Release-Question-Pairs
    - label: BEIR arXiv
      url: https://arxiv.org/abs/2104.08663
    - label: VN-MTEB ACL Anthology
      url: https://aclanthology.org/2026.findings-eacl.86/
    - label: GreenNode/quora-vn
      url: https://huggingface.co/datasets/GreenNode/quora-vn
    source_notes: []
  references:
  - title: 'BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
      Retrieval Models'
    url: https://arxiv.org/abs/2104.08663
    year: 2021
    doi: 10.48550/arXiv.2104.08663
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'VN-MTEB: Vietnamese Massive Text Embedding Benchmark'
    url: https://aclanthology.org/2026.findings-eacl.86/
    year: 2026
    doi: 10.18653/v1/2026.findings-eacl.86
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'First Quora Dataset Release: Question Pairs'
    url: https://quoradata.quora.com/First-Quora-Dataset-Release-Question-Pairs
    year: null
    doi: null
    is_paper: false
    source_confidence: probably_correct
  - title: GreenNode/quora-vn
    url: https://huggingface.co/datasets/GreenNode/quora-vn
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
      ndcg_at_10: 0.834533707
      hit_at_10: 0.96
      recall_at_100: 0.9402654867
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9402654867
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8259395743
      hit_at_10: 0.935
      recall_at_100: 0.9048672566
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9048672566
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8510204725
      hit_at_10: 0.96
      recall_at_100: 0.9623893805
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9623893805
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
