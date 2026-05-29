# NanoMTEB-French / xpqa_eng_fra

## Overview

`xpqa_eng_fra` is an xPQA retrieval split where French product questions are
matched to English product-answer candidates. The retriever must bridge the
French question to an English snippet that contains enough product information
to answer it.

## Details

### What the Original Data Measures

[xPQA: Cross-Lingual Product Question Answering across 12 Languages](https://arxiv.org/abs/2305.09249)
introduces cross-lingual product QA and defines candidate ranking as selecting
the best English candidate containing information to answer a non-English
question. The paper emphasizes that e-commerce questions are domain-specific
and that rankers trained on other domains transfer poorly.

### Observed Data Profile

The Nano split has 200 mostly French queries, 1,674 mostly English documents,
and 451 positive qrels. Queries average 54.61 characters, documents average
137.30 characters, and 52.5% of queries have multiple positives. Sampled
questions ask about warranty, volume, Android TV boxes, dimensions, and mold
height.

Documents are short product metadata or customer-answer snippets, including
JSON-like fields such as `warranty_description` and `item_dimensions`.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.1030 and hit@10 = 0.1750. The median best rank is 98.0. The cross-lingual
direction makes lexical matching weak except for product codes, units, and
shared numerals.

### Training Data That May Help

Useful training data includes xPQA train examples, French-to-English product
QA ranking pairs, bilingual e-commerce FAQ, and hard negatives from the same
product category. Training should exclude xPQA test examples, Nano queries,
qrels, and positive product candidates.

### Synthetic Data Guidance

Generate French product questions and English snippets with specifications,
warranty fields, dimensions, compatibility, volume, and customer-review
evidence. Use multiple positives where several snippets answer the same
question.

## Example Data

| Query | Positive document |
| --- | --- |
| bonjour, quels sont les avantages de cette box android, comparée aux autres ? merci (83 chars) | i have had several different android boxes and find this one of the best // easy to set up and lots of memory storage. (118 chars) |
| sur quel produit fitbit avez vous essayé cette extension ? (58 chars) | this worked great as an extender for the fitbit charge. (55 chars) |
| bonjour, la vitre est-elle en verre ou en plastique? (52 chars) | the front transparent plastic is a good protect the pictures. (61 chars) |
| cet article est-il "compatible" avec un smartphone de 5.5 pouces ? (66 chars) | it is described as being appropriate for any handlebar and any device. (70 chars) |
| bonjour est ce anti lumière bleue? (34 chars) | Product description does not mention anti blue light features. (62 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-French |
| Backing dataset | NanoMTEB-French |
| Task / split | xpqa_eng_fra |
| Hugging Face dataset | [hakari-bench/NanoMTEB-French](https://huggingface.co/datasets/hakari-bench/NanoMTEB-French) |
| Language | fr, en |
| Category | natural_language |
| Queries | 200 |
| Documents | 1674 |
| Positive qrels | 451 |
| Avg positives / query | 2.25 |
| Positives per query (min / median / max) | 1 / 2.0 / 5 |
| Queries with multiple positives | 105 (52.50%) |
| BM25 nDCG@10 | 0.1061 |
| BM25 hit@10 | 0.2050 |
| BM25 Recall@100 | 0.3149 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3639 |
| Dense hit@10 | 0.5850 |
| Dense Recall@100 | 0.7384 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.1775 |
| Reranking hybrid hit@10 | 0.3200 |
| Reranking hybrid Recall@100 | 0.6918 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 49 |
| Query length avg chars | 54.61 |
| Document length avg chars | 137.30 |

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
  task_name: xpqa_eng_fra
  split_name: xpqa_eng_fra
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-French/xpqa_eng_fra.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1674
    positive_qrels: 451
  positives_per_query:
    average: 2.255
    min: 1
    median: 2.0
    max: 5
    multi_positive_queries: 105
    multi_positive_query_percent: 52.5
  text_stats_chars:
    query_mean: 54.61
    document_mean: 137.30465949820788
  bm25:
    ndcg_at_10: 0.10613785256932198
    hit_at_10: 0.205
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude xPQA test examples, Nano queries, qrels, and positive product
      candidates
    useful_training_data:
    - xPQA train examples
    - French-to-English product QA retrieval pairs
    - bilingual e-commerce FAQ data
    - hard negatives from the same product category
    synthetic_data:
      document_generation: English product snippets with specifications, warranty
        fields, dimensions, compatibility, volume, and review evidence
      question_generation: French product questions asking about those properties
      answerability: each positive snippet should contain enough information to answer
        the French question
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
      ndcg_at_10: 0.1061378526
      hit_at_10: 0.205
      recall_at_100: 0.3148558758
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.3148558758
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3638927092
      hit_at_10: 0.585
      recall_at_100: 0.7383592018
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7383592018
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.1774886686
      hit_at_10: 0.32
      recall_at_100: 0.6917960089
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.245
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6917960089
      safeguard_positive_rows: 49
      rows_with_101_candidates: 49
```
