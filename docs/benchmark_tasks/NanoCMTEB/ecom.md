# NanoCMTEB / ecom

## Overview

Multi-CPR includes e-commerce as a real Alibaba product-search domain where
short queries and short product passages make lexical matching unusually
competitive. This NanoCMTEB task keeps that product-retrieval setting:
brief Chinese or mixed-script search strings retrieve product-title-like
documents containing brands, model numbers, transliterations, Japanese or
English tokens, and category terms. The observed examples include timers,
vermouth, plaques, hair treatment products, and gas stoves, so relevance is
often a tight product-title match rather than explanatory passage matching.

## Details

### What the Original Data Measures

[Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval](https://arxiv.org/abs/2203.03367)
introduces domain-specific Chinese passage retrieval for e-commerce,
entertainment video, and medical search. The paper states that all queries and
passages in Multi-CPR are collected from real Alibaba search systems and that
each domain includes human annotated query-passage relevance pairs. It also
reports that BM25 is comparatively strong in e-commerce because product queries
and product passages are short and surface intent is often explicit.

[C-Pack](https://arxiv.org/abs/2309.07597) includes `EcomRetrieval` in C-MTEB's
retrieval category. The Nano split keeps the compact product-search character
of the original task.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrels. Each
query has exactly one positive in the Nano labels. Queries average only 6.88
characters and documents average 33.09 characters, making this the shortest
NanoCMTEB task. Detected language is mixed: mostly Chinese, but with Japanese,
English product terms, brand names, model numbers, and transliterated names.

The observed examples are product-title matches for timers, vermouth, plaques,
hair treatment products, and gas stoves. The task often depends on matching
brand, product type, variant, and shopping-intent terms.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.0132 and hit@10 = 0.0150 in the Nano subset. Although the Multi-CPR paper
found e-commerce favorable to lexical methods, this sampled candidate ranking
contains many positives near rank 100. Brand aliases, missing spaces, mixed
scripts, and product-title expansion make exact lexical matching brittle.

### Training Data That May Help

Useful training data includes product search query-title pairs, shopping click
logs, brand and model alias pairs, Chinese-Japanese product search data, and
hard negatives from products sharing brand or category but differing in model,
size, or intent.

### Synthetic Data Guidance

Synthetic data should generate compact product titles with realistic brand,
model, attribute, and promotion terms, then create short marketplace queries.
Hard negatives should differ by variant or product family while preserving high
lexical overlap.

## Example Data

| Query | Positive document |
| --- | --- |
| 奥尔良味香肠调理 (8 chars) | 畅之味香肠调料五组合香肠调料台湾风味黑胡椒香辣蒜香新奥尔良 (29 chars) |
| 吉莫特洗鼻器 (6 chars) | 新品吉莫特洗鼻专用洗鼻盐 医生推荐儿童成人洗鼻瑜伽洗鼻盐60包 (31 chars) |
| 约肤深层滋润免蒸发膜 (10 chars) | 约肤免蒸发膜修护干枯倒膜改善毛躁头发护理水疗顺滑护发素女柔顺 (30 chars) |
| 童装韩版睡衣 (6 chars) | 女童睡衣法兰绒秋冬季儿童珊瑚绒加厚保暖女孩家居服中大童装套装 (30 chars) |
| 尼康z62 (5 chars) | Nikon/尼康z6ii z7ii二代z6z7全画幅微单机身Z62Z72 2代24-70套机 (46 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoCMTEB |
| Backing dataset | NanoCMTEB |
| Task / split | ecom |
| Hugging Face dataset | [hakari-bench/NanoCMTEB](https://huggingface.co/datasets/hakari-bench/NanoCMTEB) |
| Language | zh, ja |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.5913 |
| BM25 hit@10 | 0.7550 |
| BM25 Recall@100 | 0.8250 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8052 |
| Dense hit@10 | 0.9100 |
| Dense Recall@100 | 0.9550 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.7025 |
| Reranking hybrid hit@10 | 0.8350 |
| Reranking hybrid Recall@100 | 0.9600 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 8 |
| Query length avg chars | 6.88 |
| Document length avg chars | 33.09 |

### Public Sources

- [Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval](https://arxiv.org/abs/2203.03367); 2022; Dingkun Long et al.
- [C-Pack: Packed Resources For General Chinese Embeddings](https://arxiv.org/abs/2309.07597); 2024; Shitao Xiao et al.
- [mteb/EcomRetrieval dataset card](https://huggingface.co/datasets/mteb/EcomRetrieval).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoCMTEB](https://huggingface.co/datasets/hakari-bench/NanoCMTEB)
- Source dataset: [mteb/EcomRetrieval](https://huggingface.co/datasets/mteb/EcomRetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval | 2022 | task paper | https://arxiv.org/abs/2203.03367 |
| C-Pack: Packed Resources For General Chinese Embeddings | 2024 | benchmark paper | https://arxiv.org/abs/2309.07597 |
| mteb/EcomRetrieval | unknown | Hugging Face dataset | https://huggingface.co/datasets/mteb/EcomRetrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoCMTEB
  backing_dataset: NanoCMTEB
  dataset_id: hakari-bench/NanoCMTEB
  task_name: ecom
  split_name: ecom
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoCMTEB/ecom.md
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
    query_mean: 6.885
    document_mean: 33.0862
  bm25:
    ndcg_at_10: 0.5913115532622264
    hit_at_10: 0.755
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: EcomRetrieval dev
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoCMTEB ecom queries, qrels, and product titles
    useful_training_data:
    - product search query-title pairs
    - marketplace click logs
    - brand and model alias pairs
    - same-category product hard negatives
    synthetic_data:
      document_generation: compact marketplace product titles with brands and attributes
      question_generation: short product-search queries with aliases and variants
      answerability: positives should match the exact product intent and variant
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoCMTEB
    source_urls:
    - label: Multi-CPR arXiv
      url: https://arxiv.org/abs/2203.03367
    - label: C-Pack arXiv
      url: https://arxiv.org/abs/2309.07597
    - label: mteb/EcomRetrieval
      url: https://huggingface.co/datasets/mteb/EcomRetrieval
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
      ndcg_at_10: 0.5913115533
      hit_at_10: 0.755
      recall_at_100: 0.825
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.825
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8051785288
      hit_at_10: 0.91
      recall_at_100: 0.955
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.955
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.7025095278
      hit_at_10: 0.835
      recall_at_100: 0.96
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.04
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.96
      safeguard_positive_rows: 8
      rows_with_101_candidates: 8
```
