# NanoMTEB-Spanish / xpqa_spa_spa

## Overview

`xpqa_spa_spa` is the Spanish-to-Spanish xPQA retrieval split. Queries are
Spanish product questions and documents are Spanish product-answer snippets.
The retriever must find short candidate answers that address practical product
questions about size, compatibility, materials, quantities, and usage.

## Details

### What the Original Data Measures

[xPQA: Cross-Lingual Product Question Answering across 12 Languages](https://arxiv.org/abs/2305.09249)
collects product questions from Amazon marketplaces and annotates whether
candidate product information fully or partially answers each question. Although
xPQA focuses on cross-lingual product QA, this split tests the Spanish
monolingual retrieval condition.

### Observed Data Profile

The Nano split has 200 Spanish queries, 1,941 Spanish documents, and 488
positive qrels. Queries average 45.16 characters, documents average 68.28
characters, and 63.5% of queries have multiple positives. Sampled questions ask
whether a probe measures humidity, whether two units are included, whether a
case preserves cigars, whether a metal item is real silver, and whether a
handle is stainless steel.

Documents are short, answer-like statements. Many begin with `Sí`, `No`, or
`Un cliente ha dicho`, so polarity and product-specific attributes are central.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.4409 and hit@10 = 0.6200. This is much easier for BM25 than the cross-lingual
xPQA directions, but still not solved: sampled positives appear at ranks 88,
99, and 100 when the answer wording diverges from the question.

### Training Data That May Help

Useful data includes Spanish xPQA train examples, Spanish e-commerce QA,
customer-question to answer-snippet pairs, and hard negatives from the same
product category. Training should exclude xPQA test examples, Nano queries,
qrels, and positive snippets.

### Synthetic Data Guidance

Generate Spanish product questions and short Spanish candidate answers. Include
yes/no polarity, quantities, materials, model codes, dimensions, compatibility,
and customer-review style evidence. Preserve multiple positives when several
snippets answer the same product question.

## Example Data

| Query | Positive document |
| --- | --- |
| el pack de 3 cintas, ¿es una de cada tamaño o las 3 del mismo tamaño? (69 chars) | El paquete contiene 3 piezas de 120 cm de largo. (48 chars) |
| que son tallas grandes o justas? (32 chars) | Son de talla ajustada moldeando la curvatura del cuerpo. (56 chars) |
| és el modelo acústico o electro acústico? (41 chars) | Este producto es una guitarra electroacústica. (46 chars) |
| como se que tamaño pedir,? (26 chars) | Un cliente ha dicho que recomienda medir el diámetro de la muñeca como referencia. (82 chars) |
| si compro un pack vendran 12 unidades? (38 chars) | Sí. El paquete incluye 12 unidades. (35 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Spanish |
| Backing dataset | NanoMTEB-Spanish |
| Task / split | xpqa_spa_spa |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Spanish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Spanish) |
| Language | es |
| Category | natural_language |
| Queries | 200 |
| Documents | 1941 |
| Positive qrels | 488 |
| Avg positives / query | 2.44 |
| Positives per query (min / median / max) | 1 / 2.0 / 5 |
| Queries with multiple positives | 127 (63.50%) |
| BM25 nDCG@10 | 0.4829 |
| BM25 hit@10 | 0.7000 |
| BM25 Recall@100 | 0.7766 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.5667 |
| Dense hit@10 | 0.7650 |
| Dense Recall@100 | 0.8975 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.5582 |
| Reranking hybrid hit@10 | 0.7400 |
| Reranking hybrid Recall@100 | 0.8832 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 20 |
| Query length avg chars | 45.16 |
| Document length avg chars | 68.28 |

### Public Sources

- [xPQA: Cross-Lingual Product Question Answering across 12 Languages](https://arxiv.org/abs/2305.09249); 2023; Xiaoyu Shen et al.
- [mteb/XPQARetrieval dataset card](https://huggingface.co/datasets/mteb/XPQARetrieval).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316); 2023; Niklas Muennighoff et al.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Spanish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Spanish)
- Source dataset: [mteb/XPQARetrieval](https://huggingface.co/datasets/mteb/XPQARetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| xPQA: Cross-Lingual Product Question Answering across 12 Languages | 2023 | arXiv paper | https://arxiv.org/abs/2305.09249 |
| MTEB: Massive Text Embedding Benchmark | 2023 | arXiv paper | https://arxiv.org/abs/2210.07316 |
| mteb/XPQARetrieval | 2025 | dataset card | https://huggingface.co/datasets/mteb/XPQARetrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Spanish
  backing_dataset: NanoMTEB-Spanish
  dataset_id: hakari-bench/NanoMTEB-Spanish
  task_name: xpqa_spa_spa
  split_name: xpqa_spa_spa
  language: es
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Spanish/xpqa_spa_spa.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1941
    positive_qrels: 488
  positives_per_query:
    average: 2.44
    min: 1
    median: 2.0
    max: 5
    multi_positive_queries: 127
    multi_positive_query_percent: 63.5
  text_stats_chars:
    query_mean: 45.16
    document_mean: 68.27511591962906
  bm25:
    ndcg_at_10: 0.48289573105819505
    hit_at_10: 0.7
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude xPQA test examples, Nano queries, qrels, and positive product
      snippets
    useful_training_data:
    - Spanish xPQA train examples
    - Spanish e-commerce QA pairs
    - customer-question to answer-snippet retrieval pairs
    - same-product and same-category hard negatives
    synthetic_data:
      document_generation: short Spanish product answer snippets with polarity, quantities,
        materials, model codes, dimensions, and compatibility claims
      question_generation: Spanish product questions asking about concrete purchase
        or usage details
      answerability: each positive snippet should directly answer the question, including
        yes/no polarity when applicable
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Spanish
    source_urls:
    - label: xPQA arXiv
      url: https://arxiv.org/abs/2305.09249
    - label: mteb/XPQARetrieval
      url: https://huggingface.co/datasets/mteb/XPQARetrieval
    - label: MTEB arXiv
      url: https://arxiv.org/abs/2210.07316
    source_notes: []
  references:
  - title: 'xPQA: Cross-Lingual Product Question Answering across 12 Languages'
    url: https://arxiv.org/abs/2305.09249
    year: 2023
    doi: 10.48550/arXiv.2305.09249
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4828957311
      hit_at_10: 0.7
      recall_at_100: 0.7766393443
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7766393443
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5667196167
      hit_at_10: 0.765
      recall_at_100: 0.8975409836
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8975409836
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.5581986015
      hit_at_10: 0.74
      recall_at_100: 0.8831967213
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.1
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8831967213
      safeguard_positive_rows: 20
      rows_with_101_candidates: 20
```
