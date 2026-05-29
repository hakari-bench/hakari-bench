# NanoVNMTEB / nq_vn

## Overview

`nq_vn` is the Vietnamese Natural Questions retrieval task from VN-MTEB. Queries
are translated real search questions, and documents are translated
Wikipedia-style passages. The task tests passage retrieval for factual
information needs where the answer-bearing passage may be an entity page,
location page, list page, or topic description.

## Details

### What the Original Data Measures

[Natural Questions: A Benchmark for Question Answering Research](https://aclanthology.org/Q19-1026/)
collects real anonymized Google search queries and pairs them with Wikipedia
pages from top search results. Annotators mark long answers and short answers
when present, making the benchmark closer to real user information needs than
questions written after seeing a paragraph.

[BEIR](https://arxiv.org/abs/2104.08663) adapts NQ for retrieval: the query is
the natural question and the model must retrieve relevant Wikipedia passages.
[VN-MTEB](https://aclanthology.org/2026.findings-eacl.86/) translates and
filters the source data into Vietnamese.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 234 positive qrel rows.
Most queries are single-positive, but 32 queries have multiple positives and the
maximum is 3. Queries average 39.40 characters. Documents average 557.60
characters and can range from short entity summaries to longer Wikipedia
passages.

Observed examples ask about the main industry in the Canadian Shield, who plays
at the Prudential Center, books by Abul Kalam Azad, whom Ursula from The Little
Mermaid was based on, and when Marathon was renamed Snickers. These are concise
factoid or entity-attribute questions.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.6789
and hit@10 = 0.8450. Named entities and rare terms make lexical retrieval
useful, but nDCG is lower than the `nano_nq` source variant, indicating more
ranking misses within the top 10.

The median first relevant rank is 1, so many queries are easy to hit, while the
harder cases require matching the requested attribute inside the correct
Wikipedia passage.

### Training Data That May Help

Useful training data includes official Natural Questions train data where
permitted, Vietnamese Wikipedia QA, non-overlapping question-to-passage
retrieval pairs, and translated NQ data with overlap removed. The translated
test queries, qrels, documents, and positive passages used by this Nano split
should be excluded.

Because NQ is widely used in retrieval training, overlap checks are important
before reusing any translated or multilingual NQ-derived data.

### Synthetic Data Guidance

For document-to-query generation, use non-evaluation Vietnamese Wikipedia
passages and generate short search questions asking for a specific entity
attribute, date, location, role, title, or list membership.

For joint generation, create entity passages and realistic short questions, with
hard negatives that mention the same entity but do not contain the requested
attribute. Do not seed generation from this evaluation split.

## Example Data

| Query | Positive document |
| --- | --- |
| ai la cha của Dylan trong Bates Motel (37 chars) | Danh sách nhân vật trong phim Bates Motel Dylan Massett (do Max Thieriot thủ vai) [3] là con trai xa lạ của Norma và là anh cùng cha khác mẹ với Norman. Sau khi lớn lên hầu như tự lực cánh sinh, anh rất khôn ngoan, mạnh mẽ và ... [truncated 225 chars](2150 chars) |
| mùa 5 của Ruby ra khi nào (25 chars) | Danh sách tập RWBY RWBY là một loạt phim hoạt hình trực tuyến Mỹ được sản xuất bởi Rooster Teeth Productions. Phim ra mắt vào ngày 18 tháng 7 năm 2013 trên trang web Rooster Teeth, và sau đó các tập phim được tải lên YouTube ... [truncated 225 chars](486 chars) |
| câu nói blue moon xuất phát từ đâu (34 chars) | Trăng xanh Một giả thuyết đã được đưa ra rằng thuật ngữ "trăng xanh" cho "tháng nhuận" xuất hiện từ dân gian, trong đó "xanh" thay thế cho belewe không còn được hiểu nghĩa là "bất trung". Ý nghĩa gốc của nó sẽ là "Trăng phản ... [truncated 225 chars](476 chars) |
| danh sách sách viết bởi abul kalam azad (39 chars) | Abul Kalam Azad Maulana Azad được cho là một trong những nhà văn tiếng Urdu vĩ đại nhất của thế kỷ 20. Ông đã viết nhiều sách bao gồm cả Ấn Độ giành được tự do, Ghubar-e-Khatir, Tazkirah, Tarjumanul Quran, v.v. (211 chars) |
| sông nào liên quan đến thành phố rome (37 chars) | Tiber Sông Tiber (/ ˈtaɪbər /, tiếng Latin Tiberis,[1] tiếng Ý Tevere, phát âm tiếng Ý: [ˈteːvere] ) [2] là con sông dài thứ ba ở Ý, bắt nguồn từ dãy núi Apennine ở Emilia-Romagna và chảy 406 km (252 dặm) qua Tuscany, Umbria ... [truncated 225 chars](513 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoVNMTEB |
| Backing dataset | NanoVNMTEB |
| Task / split | nq_vn |
| Hugging Face dataset | [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB) |
| Source dataset | [GreenNode/nq-vn](https://huggingface.co/datasets/GreenNode/nq-vn) |
| Language | vi |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 234 |
| Avg positives / query | 1.17 |
| Positives per query (min / median / max) | 1 / 1 / 3 |
| Queries with multiple positives | 32 (16.00%) |
| BM25 nDCG@10 | 0.5882 |
| BM25 hit@10 | 0.7450 |
| BM25 Recall@100 | 0.8718 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7981 |
| Dense hit@10 | 0.9000 |
| Dense Recall@100 | 0.9658 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6826 |
| Reranking hybrid hit@10 | 0.8300 |
| Reranking hybrid Recall@100 | 0.9957 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 39.40 |
| Document length avg chars | 557.60 |

### Public Sources

- [Natural Questions: A Benchmark for Question Answering Research](https://aclanthology.org/Q19-1026/), 2019.
- [Natural Questions official page](https://ai.google.com/research/NaturalQuestions/), official dataset page.
- [VN-MTEB: Vietnamese Massive Text Embedding Benchmark](https://aclanthology.org/2026.findings-eacl.86/), 2026.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [GreenNode/nq-vn](https://huggingface.co/datasets/GreenNode/nq-vn), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB)
- Source dataset: [GreenNode/nq-vn](https://huggingface.co/datasets/GreenNode/nq-vn)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Natural Questions: A Benchmark for Question Answering Research | 2019 | ACL/TACL paper | https://aclanthology.org/Q19-1026/ |
| Natural Questions official page |  | project page | https://ai.google.com/research/NaturalQuestions/ |
| VN-MTEB: Vietnamese Massive Text Embedding Benchmark | 2026 | ACL paper | https://aclanthology.org/2026.findings-eacl.86/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| GreenNode/nq-vn |  | dataset card | https://huggingface.co/datasets/GreenNode/nq-vn |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoVNMTEB
  backing_dataset: NanoVNMTEB
  dataset_id: hakari-bench/NanoVNMTEB
  task_name: nq_vn
  split_name: nq_vn
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/NanoVNMTEB/nq_vn.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://aclanthology.org/Q19-1026/
    additional_source_urls:
    - https://ai.google.com/research/NaturalQuestions/
    - https://aclanthology.org/2026.findings-eacl.86/
    - https://arxiv.org/abs/2104.08663
    - https://huggingface.co/datasets/GreenNode/nq-vn
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 234
  positives_per_query:
    average: 1.17
    min: 1
    median: 1.0
    max: 3
    multi_positive_queries: 32
    multi_positive_query_percent: 16.0
  text_stats_chars:
    query_mean: 39.4
    document_mean: 557.6
  bm25:
    ndcg_at_10: 0.5882327266882935
    hit_at_10: 0.745
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: translated VN-MTEB NQ test split from GreenNode/nq-vn
    train_eval_overlap_audit: not_audited
    leakage_note: Exclude translated NQ-VN test queries, qrels, documents, and positive
      passages used by this Nano split.
    useful_training_data:
    - official Natural Questions training examples with overlap removed
    - Vietnamese Wikipedia QA
    - non-overlapping question-to-passage retrieval pairs
    - translated NQ data with overlap removed
    synthetic_data:
      document_generation: Vietnamese Wikipedia-style entity and topic passages with
        explicit attributes.
      question_generation: Short Vietnamese search questions asking for a specific
        entity attribute, date, location, role, title, or list membership.
      answerability: Each question should be answerable from the passage, with same-entity
        different-attribute negatives.
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoVNMTEB
    source_urls:
    - label: Natural Questions ACL Anthology
      url: https://aclanthology.org/Q19-1026/
    - label: Natural Questions official page
      url: https://ai.google.com/research/NaturalQuestions/
    - label: VN-MTEB ACL Anthology
      url: https://aclanthology.org/2026.findings-eacl.86/
    - label: BEIR arXiv
      url: https://arxiv.org/abs/2104.08663
    - label: GreenNode/nq-vn
      url: https://huggingface.co/datasets/GreenNode/nq-vn
    source_notes: []
  references:
  - title: 'Natural Questions: A Benchmark for Question Answering Research'
    url: https://aclanthology.org/Q19-1026/
    year: 2019
    doi: 10.1162/tacl_a_00276
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
  - title: GreenNode/nq-vn
    url: https://huggingface.co/datasets/GreenNode/nq-vn
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
      ndcg_at_10: 0.5882327267
      hit_at_10: 0.745
      recall_at_100: 0.8717948718
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8717948718
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.798112531
      hit_at_10: 0.9
      recall_at_100: 0.9658119658
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9658119658
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.6825894352
      hit_at_10: 0.83
      recall_at_100: 0.9957264957
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9957264957
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
