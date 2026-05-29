# NanoMTEB-Spanish / xpqa_spa_eng

## Overview

`xpqa_spa_eng` is an xPQA retrieval split where English product questions are
matched to Spanish product-answer candidates. The retriever must bridge the
English question to a Spanish snippet that contains enough product information
to answer it.

## Details

### What the Original Data Measures

[xPQA: Cross-Lingual Product Question Answering across 12 Languages](https://arxiv.org/abs/2305.09249)
frames product QA as candidate ranking plus answer generation. The ranking task
selects the candidate that contains the answer information, and the paper
highlights that product-domain supervision is more effective than transferring
from Wikipedia-style cross-lingual QA.

### Observed Data Profile

The Nano split has 200 English queries, 1,941 mostly Spanish documents, and
469 positive qrels. Queries average 47.42 characters, documents average 68.28
characters, and 60.5% of queries have multiple positives. Sampled questions ask
about blade length, capacity, color codes, sowing season, and aquarium salt
measurement.

Documents are compact Spanish answer snippets, often beginning with `Sí`, `No`,
or `Un cliente ha dicho`. The language direction is the reverse of
`xpqa_eng_spa`, so lexical BM25 has little shared vocabulary except numbers,
codes, and product names.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.1162 and hit@10 = 0.1750. The median best rank is 98.0. BM25 only succeeds
when language-independent tokens such as `RAL 7048`, numbers, or units align.

### Training Data That May Help

Useful training data includes xPQA train examples, English-to-Spanish product
candidate ranking pairs, translated product QA, and hard negatives from the
same product or category. Training should exclude xPQA test examples, Nano
queries, qrels, and positive snippets.

### Synthetic Data Guidance

Generate English product questions and Spanish answer snippets. Include units,
model codes, compatibility claims, customer-reported facts, and yes/no
answers. Use multiple positives when several snippets answer the same product
question, and include near-miss category negatives.

## Example Data

| Query | Positive document |
| --- | --- |
| do you have anything that holds at 0 and 90 degrees and doesn't turn on its own? (80 chars) | Sí. Un cliente ha dicho que soporta la televisión a 0 y 90 grados. (66 chars) |
| what type of restraint do you have? (35 chars) | Un cliente ha dicho que utilizó ganchos con tiras. (50 chars) |
| can it be used to wash my face? (31 chars) | Sí. Son utilizables para cualquier parte del cuerpo. (52 chars) |
| Does it protect from UV rays? (29 chars) | Sí. Proteje a tus hijos de los rayos de luz ultravioleta y de las quemaduras de sol también. (92 chars) |
| when are you going to bring more for iPhone 7 plus? (51 chars) | Un cliente ha dicho que este es el mejor protector de pantalla para el iPhone 7 Plus. (85 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Spanish |
| Backing dataset | NanoMTEB-Spanish |
| Task / split | xpqa_spa_eng |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Spanish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Spanish) |
| Language | en, es |
| Category | natural_language |
| Queries | 200 |
| Documents | 1941 |
| Positive qrels | 469 |
| Avg positives / query | 2.35 |
| Positives per query (min / median / max) | 1 / 2.0 / 5 |
| Queries with multiple positives | 121 (60.50%) |
| BM25 nDCG@10 | 0.1227 |
| BM25 hit@10 | 0.1850 |
| BM25 Recall@100 | 0.2154 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4872 |
| Dense hit@10 | 0.7300 |
| Dense Recall@100 | 0.8593 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.1444 |
| Reranking hybrid hit@10 | 0.2200 |
| Reranking hybrid Recall@100 | 0.7889 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 35 |
| Query length avg chars | 47.42 |
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
  task_name: xpqa_spa_eng
  split_name: xpqa_spa_eng
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Spanish/xpqa_spa_eng.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1941
    positive_qrels: 469
  positives_per_query:
    average: 2.345
    min: 1
    median: 2.0
    max: 5
    multi_positive_queries: 121
    multi_positive_query_percent: 60.5
  text_stats_chars:
    query_mean: 47.415
    document_mean: 68.27511591962906
  bm25:
    ndcg_at_10: 0.12268200829327501
    hit_at_10: 0.185
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude xPQA test examples, Nano queries, qrels, and positive product
      snippets
    useful_training_data:
    - xPQA train examples
    - English-to-Spanish product QA retrieval pairs
    - translated product QA pairs
    - same-product hard negatives
    synthetic_data:
      document_generation: Spanish product answer snippets with model codes, units,
        compatibility claims, and customer-reported facts
      question_generation: English product questions asking about those properties
      answerability: each positive snippet should contain enough information to answer
        the English question
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
      ndcg_at_10: 0.1226820083
      hit_at_10: 0.185
      recall_at_100: 0.2153518124
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2153518124
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4871625292
      hit_at_10: 0.73
      recall_at_100: 0.8592750533
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8592750533
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.1443653711
      hit_at_10: 0.22
      recall_at_100: 0.78891258
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.175
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.78891258
      safeguard_positive_rows: 35
      rows_with_101_candidates: 35
```
