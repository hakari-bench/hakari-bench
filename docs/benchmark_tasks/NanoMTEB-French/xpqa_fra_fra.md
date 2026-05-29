# NanoMTEB-French / xpqa_fra_fra

## Overview

`xpqa_fra_fra` is the French-to-French xPQA retrieval split. Queries are French
product questions, and documents are short French product-answer snippets. The
retriever must rank snippets that answer practical shopping questions about
instructions, size, compatibility, material, and product condition.

## Details

### What the Original Data Measures

[xPQA: Cross-Lingual Product Question Answering across 12 Languages](https://arxiv.org/abs/2305.09249)
is built for product question answering with candidate ranking and answer
generation. This split is monolingual French, but it still uses the same
product-domain candidate ranking setup: retrieve the snippet that contains the
answer information.

### Observed Data Profile

The Nano split has 200 French queries, 1,547 French documents, and 424
positive qrels. Queries average 54.61 characters, documents average 76.98
characters, and 51.0% of queries have multiple positives. Sampled questions ask
for an instruction manual, shoe weight, leather sofa repair, drawer size, and
Nintendo Switch headset compatibility.

Documents are concise answer-like snippets. Many are polarity statements or
customer-reported facts, so small wording differences can reverse relevance.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.5551 and hit@10 = 0.7350. This is much easier for BM25 than the cross-lingual
xPQA French splits, but sampled positives at ranks 34 and 100 show that
paraphrase and product-domain wording still matter.

### Training Data That May Help

Useful data includes xPQA French train examples, French e-commerce QA,
customer-question to answer-snippet pairs, and hard negatives from the same
product. Training should exclude xPQA test examples, Nano queries, qrels, and
positive snippets.

### Synthetic Data Guidance

Generate French product questions and short French answer snippets with yes/no
polarity, compatibility, dimensions, materials, care instructions, and customer
experience language. Use multiple positives when several snippets answer the
same question.

## Example Data

| Query | Positive document |
| --- | --- |
| bonjour, quels sont les avantages de cette box android, comparée aux autres ? merci (83 chars) | Un client dit qu'en comparison aux autres box Android qu'il a eu, celle-là est une des meilleurs parce qu'elle est facile à installer et a une grande capacité de stockage. (171 chars) |
| sur quel produit fitbit avez vous essayé cette extension ? (58 chars) | Un client dit que ce produit fonctionnait très bien sur un Fitbit Charge. (73 chars) |
| bonjour, la vitre est-elle en verre ou en plastique? (52 chars) | Un client dit que la vitre est en plastique transparent et qu'elle protège bien les photos. (91 chars) |
| cet article est-il "compatible" avec un smartphone de 5.5 pouces ? (66 chars) | Oui. Un client dit que c'est compatible avec n'importe quelle guidon et n'importe quel appareil. (96 chars) |
| bonjour est ce anti lumière bleue? (34 chars) | Non, ce produit n'est pas anti-lumière bleue. (45 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-French |
| Backing dataset | NanoMTEB-French |
| Task / split | xpqa_fra_fra |
| Hugging Face dataset | [hakari-bench/NanoMTEB-French](https://huggingface.co/datasets/hakari-bench/NanoMTEB-French) |
| Language | fr |
| Category | natural_language |
| Queries | 200 |
| Documents | 1547 |
| Positive qrels | 424 |
| Avg positives / query | 2.12 |
| Positives per query (min / median / max) | 1 / 2.0 / 5 |
| Queries with multiple positives | 102 (51.00%) |
| BM25 nDCG@10 | 0.5644 |
| BM25 hit@10 | 0.7550 |
| BM25 Recall@100 | 0.8042 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.6400 |
| Dense hit@10 | 0.8050 |
| Dense Recall@100 | 0.8703 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6208 |
| Reranking hybrid hit@10 | 0.7700 |
| Reranking hybrid Recall@100 | 0.8915 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 16 |
| Query length avg chars | 54.61 |
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
  task_name: xpqa_fra_fra
  split_name: xpqa_fra_fra
  language: fr
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-French/xpqa_fra_fra.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1547
    positive_qrels: 424
  positives_per_query:
    average: 2.12
    min: 1
    median: 2.0
    max: 5
    multi_positive_queries: 102
    multi_positive_query_percent: 51.0
  text_stats_chars:
    query_mean: 54.61
    document_mean: 76.98125404007757
  bm25:
    ndcg_at_10: 0.5644155504497677
    hit_at_10: 0.755
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude xPQA test examples, Nano queries, qrels, and positive product
      snippets
    useful_training_data:
    - xPQA French train examples
    - French e-commerce QA pairs
    - customer-question to answer-snippet retrieval pairs
    - same-product and same-category hard negatives
    synthetic_data:
      document_generation: short French product answer snippets with polarity, dimensions,
        materials, care instructions, compatibility, and customer evidence
      question_generation: French product questions asking practical shopping and
        usage details
      answerability: each positive snippet should directly answer the question, including
        polarity when applicable
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
      ndcg_at_10: 0.5644155504
      hit_at_10: 0.755
      recall_at_100: 0.804245283
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.804245283
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6399800631
      hit_at_10: 0.805
      recall_at_100: 0.8702830189
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8702830189
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.6207984794
      hit_at_10: 0.77
      recall_at_100: 0.891509434
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.08
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.891509434
      safeguard_positive_rows: 16
      rows_with_101_candidates: 16
```
