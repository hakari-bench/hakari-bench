# NanoMTEB-Misc / en

## Overview

`NanoMTEB-Misc / en` is the English split of EuroPIRQ retrieval. English
synthetic questions retrieve English passages derived from DGT-Acquis
paragraph-level European Union legal and administrative texts.

## Details

### What the Original Data Measures

The [EuroPIRQ dataset card](https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval)
describes EuroPIRQ as European Parallel Information Retrieval Queries built
from DGT-Acquis paragraph-level corpus chunks. The card states that English,
Finnish, and Portuguese passages were selected as aligned triplets, cleaned,
language-checked, and paired with 100 synthetic questions per language.

[MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595)
frames these community-contributed multilingual retrieval tasks as part of a
larger expansion of MTEB. No standalone EuroPIRQ task paper was confirmed in
this pass; the interpretation here is based on the dataset card, MMTEB/MTEB
metadata, and observed Nano samples.

### Observed Data Profile

The split has 100 queries, 9,422 documents, and 100 positive qrel rows. Every
query has one positive passage. Queries average 140.43 characters and documents
average 550.09 characters. The observed passages are formal EU legal,
committee, court, and administrative text.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.9491 and hit@10 = 0.9700. It ranks 92 positives at rank 1 and 97 in the top
10.

This is mostly a lexical retrieval task in English: synthetic questions often
reuse distinctive names, institutions, legal terms, or dates from the target
passage. The few misses come from near-duplicate legal boilerplate or similar
procedural passages.

### Training Data That May Help

Training data from legal and EU-domain passage retrieval, synthetic
question-passage pairs, and DGT-Acquis-style parallel corpora should help.
Hard negatives should be same-institution or same-regulation passages with
overlapping legal phrasing.

### Synthetic Data Guidance

Generate questions from non-evaluation EU legal and administrative paragraphs.
Preserve exact names, directives, dates, and institutions in some questions,
but also include paraphrases that require semantic matching. Use near-duplicate
legal passages as hard negatives.

## Example Data

| Query | Positive document |
| --- | --- |
| What is required for the ongoing process of building and operating an integrated market? (88 chars) | Finally, building a fully integrated market is not a definite task with a finite end, but rather an ongoing process requiring constant effort, vigilance and updating. There are always new challenges and, as obstacles to makin ... [truncated 225 chars](504 chars) |
| How do high-speed train connections contribute to social and economic cohesion in the EU? (89 chars) | However, the Commission notes that air transport is not the only driver of development in terms of regional accessibility. High-speed train connections also make a significant contribution to social and economic cohesion in t ... [truncated 225 chars](498 chars) |
| What are the challenges faced by Member States in implementing national lifelong learning strategies and instruments? (117 chars) | The implementation of national lifelong learning strategies and instruments, which are key to enabling not only young people, but also adults, to acquire, maintain and develop knowledge, skills and competences throughout thei ... [truncated 225 chars](581 chars) |
| How does Article 56 EC affect the taxation of dividends received by a resident company from a non-resident company in which it holds less than 10% of the voting rights? (168 chars) | Article 56 EC is, furthermore, to be interpreted as meaning that it precludes legislation of a Member State which exempts from corporation tax dividends which a resident company receives from another resident company, where t ... [truncated 225 chars](564 chars) |
| What is the purpose of requiring undertakings to provide sufficient information in Form RS? (91 chars) | Given the above mechanism, it is crucial to the smooth operation of Article 4(5) that all Member States where the case is reviewable under national competition law, and which are hence competent to examine the case under nati ... [truncated 225 chars](515 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Misc |
| Backing dataset | NanoMTEB-Misc |
| Task / split | en |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Misc](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Misc) |
| Source dataset | [eherra/EuroPIRQ-retrieval](https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval) |
| Language | en |
| Category | natural_language |
| Queries | 100 |
| Documents | 9,422 |
| Positive qrels | 100 |
| BM25 nDCG@10 | 0.9414 |
| BM25 hit@10 | 0.9700 |
| BM25 Recall@100 | 1.0000 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.9255 |
| Dense hit@10 | 0.9600 |
| Dense Recall@100 | 0.9900 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.9438 |
| Reranking hybrid hit@10 | 0.9800 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 140.43 |
| Document length avg chars | 550.09 |

### Public Sources

- [EuroPIRQ-retrieval dataset card](https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval), construction and data-field description.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595), benchmark context.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), original benchmark framework.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Misc](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Misc)
- Source task dataset: [eherra/EuroPIRQ-retrieval](https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| EuroPIRQ-retrieval | 2025 | dataset card | https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| MTEB: Massive Text Embedding Benchmark | 2022 | benchmark paper | https://arxiv.org/abs/2210.07316 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Misc
  backing_dataset: NanoMTEB-Misc
  dataset_id: hakari-bench/NanoMTEB-Misc
  task_name: en
  split_name: en
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Misc/en.md
  source_research:
    primary_source_type: dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: No standalone EuroPIRQ task paper was confirmed; dataset card and
      MMTEB/MTEB sources were checked.
  counts:
    queries: 100
    documents: 9422
    positive_qrels: 100
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 140.43
    document_mean: 550.09
  bm25:
    ndcg_at_10: 0.9414178570853677
    hit_at_10: 0.97
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.9414178571
      hit_at_10: 0.97
      recall_at_100: 1.0
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 100
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.9254743803
      hit_at_10: 0.96
      recall_at_100: 0.99
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 100
      query_coverage: 1.0
      relevant_coverage_at_100: 0.99
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.9438077136
      hit_at_10: 0.98
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 100
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
