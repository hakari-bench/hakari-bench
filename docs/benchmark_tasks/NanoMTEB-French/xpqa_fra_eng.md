# NanoMTEB-French / xpqa_fra_eng

## Overview

`xpqa_fra_eng` is an xPQA retrieval split where English product questions are
matched to French answer snippets. The retriever must find French product
information that answers the English question.

## Details

### What the Original Data Measures

[xPQA: Cross-Lingual Product Question Answering across 12 Languages](https://arxiv.org/abs/2305.09249)
collects product questions from marketplaces and annotates candidate relevance
for product-answer ranking. This split reverses the usual non-English query to
English candidate direction: English queries retrieve French candidates.

### Observed Data Profile

The Nano split has 200 English queries, 1,547 French documents, and 437
positive qrels. Queries average 52.11 characters, documents average 76.98
characters, and 53.5% of queries have multiple positives. Sampled examples ask
about fingerprint readers, tie length, toothpaste compatibility, Toshiba
Satellite batteries, and washing.

Documents are short French answer snippets, often with `Oui`, `Non`, or `Un
client dit`. The key challenge is cross-lingual matching plus product-specific
polarity and constraints.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2585 and hit@10 = 0.3450. This is still hard for BM25, but easier than the
French-query-to-English-candidate direction in this Nano sample, likely because
some product names and technical tokens survive across languages.

### Training Data That May Help

Useful data includes xPQA train examples, English-to-French product QA
retrieval, bilingual product descriptions, and hard negatives from the same
product. Training should exclude xPQA test examples, Nano queries, qrels, and
positive snippets.

### Synthetic Data Guidance

Generate English product questions and French snippets with yes/no polarity,
compatibility claims, measurements, model names, and customer-reported facts.
Use multiple positive snippets when several answers satisfy the same question.

## Example Data

| Query | Positive document |
| --- | --- |
| what is the width of a module? (30 chars) | La largeur d'un module est de 4,21 inch. (40 chars) |
| for the color do you have white ones as in the photo? (53 chars) | Non. La couleur disponible est violet et gris. (46 chars) |
| hello, does this spray make hair greasy? thank you. (51 chars) | Oui. Un client dit que cela rend ses cheveux un peu huileux. (60 chars) |
| hello, no instructions without the box, does anyone know where we can find it? (78 chars) | Oui. Un client dit que vous pouvez télécharger le manuel et guide d'utilisation rapide sur la page Amazon. (106 chars) |
| is this razor compatible with protector 3 blades? thank you. (60 chars) | Non. Un client dit qu'il n'est pas possible d'ajouter les lames d'autres fabricants. (84 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-French |
| Backing dataset | NanoMTEB-French |
| Task / split | xpqa_fra_eng |
| Hugging Face dataset | [hakari-bench/NanoMTEB-French](https://huggingface.co/datasets/hakari-bench/NanoMTEB-French) |
| Language | en, fr |
| Category | natural_language |
| Queries | 200 |
| Documents | 1547 |
| Positive qrels | 437 |
| Avg positives / query | 2.19 |
| Positives per query (min / median / max) | 1 / 2.0 / 5 |
| Queries with multiple positives | 107 (53.50%) |
| BM25 nDCG@10 | 0.2918 |
| BM25 hit@10 | 0.3800 |
| BM25 Recall@100 | 0.3684 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.6479 |
| Dense hit@10 | 0.8100 |
| Dense Recall@100 | 0.8993 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3724 |
| Reranking hybrid hit@10 | 0.5000 |
| Reranking hybrid Recall@100 | 0.8398 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 13 |
| Query length avg chars | 52.11 |
| Document length avg chars | 76.98 |

### Public Sources

- [xPQA: Cross-Lingual Product Question Answering across 12 Languages](https://arxiv.org/abs/2305.09249); 2023; Xiaoyu Shen et al.
- [mteb/XPQARetrieval dataset card](https://huggingface.co/datasets/mteb/XPQARetrieval).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316); 2023; Niklas Muennighoff et al.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-French](https://huggingface.co/datasets/hakari-bench/NanoMTEB-French)
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
  nano_set: NanoMTEB-French
  backing_dataset: NanoMTEB-French
  dataset_id: hakari-bench/NanoMTEB-French
  task_name: xpqa_fra_eng
  split_name: xpqa_fra_eng
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-French/xpqa_fra_eng.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1547
    positive_qrels: 437
  positives_per_query:
    average: 2.185
    min: 1
    median: 2.0
    max: 5
    multi_positive_queries: 107
    multi_positive_query_percent: 53.5
  text_stats_chars:
    query_mean: 52.11
    document_mean: 76.98125404007757
  bm25:
    ndcg_at_10: 0.2918097312851351
    hit_at_10: 0.38
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude xPQA test examples, Nano queries, qrels, and positive product
      snippets
    useful_training_data:
    - xPQA train examples
    - English-to-French product QA retrieval pairs
    - bilingual product descriptions and customer answers
    - same-product hard negatives
    synthetic_data:
      document_generation: French product answer snippets with yes/no polarity, compatibility
        claims, measurements, model names, and customer-reported facts
      question_generation: English product questions asking about those properties
      answerability: each positive snippet should contain enough information to answer
        the English question
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-French
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
      ndcg_at_10: 0.2918097313
      hit_at_10: 0.38
      recall_at_100: 0.3684210526
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.3684210526
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6479011019
      hit_at_10: 0.81
      recall_at_100: 0.8993135011
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8993135011
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.372430571
      hit_at_10: 0.5
      recall_at_100: 0.8398169336
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.065
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8398169336
      safeguard_positive_rows: 13
      rows_with_101_candidates: 13
```
