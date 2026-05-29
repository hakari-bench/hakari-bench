# NanoMTEB-German / xmarket_de

## Overview

`xmarket_de` is the German subset of the XMarket retrieval task in
`NanoMTEB-German`. Queries are short product-category or shopping-intent labels,
and documents are product metadata snippets. The retriever must rank products
that belong to or satisfy the category, often with many relevant products for a
single query.

## Details

### What the Original Data Measures

[Cross-Market Product Recommendation](https://arxiv.org/abs/2109.05929)
introduces XMarket as a cross-market and cross-lingual e-commerce dataset built
from Amazon marketplaces. The paper reports 18 local markets, 16 product
categories, 11 languages, and 52.5 million user-item interactions, and studies
market adaptation for product recommendation. The German example in the paper is
motivating: preferences in one market should not be blindly imported into
another market.

The MTEB XMarket task adapts this e-commerce source into text retrieval. In the
observed German Nano split, the query text is a short category label such as
`Pinsel`, `Stifte`, or `Spielzeug`, and positives are product titles or product
descriptions. This measures category-to-product retrieval rather than factual QA.

### Observed Data Profile

The Nano split has 182 queries, 10,000 documents, and 4,124 positive qrels. It
is strongly multi-positive: average positives per query is 22.66, the median is
7.5, and 85.16% of queries have more than one positive. Queries are very short,
averaging 14.57 characters. Documents average 451.12 characters, but many are
short product titles with brand, material, size, or color.

The sampled positives include craft brushes, world-map posters, colored pencils,
rugs or protective mats, and bead-design boards. Some documents are German,
some retain English product names, and some are mixed-language marketplace text.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2408 and hit@10 = 0.4286. Despite many positives per query, BM25 finds a
positive in the top 10 for fewer than half of the queries.

The main difficulty is that category relevance is broader than exact term
matching. A `Spielzeug` query can be relevant to a bead board without using the
word `Spielzeug`, and `Teppiche, Dämm- & Schutzmatten` includes product variants
with sparse or noisy descriptions. A strong model needs German and English
e-commerce semantics, category hierarchy, brand/product normalization, and
multi-positive ranking.

### Training Data That May Help

Useful training data includes non-overlapping XMarket product metadata,
category-product pairs, multilingual e-commerce search logs, query-to-product
click or purchase pairs, and hard negatives from neighboring categories. Data
from the same German evaluation products or qrels should be excluded unless a
leaderboard explicitly permits it.

Because the source benchmark is cross-market, multilingual product data can help
when it preserves market-specific category meaning. Training should avoid
collapsing all markets into English-only category labels.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation product metadata and
generate concise German category or shopping-intent queries that can retrieve
the product. For joint generation, create realistic product titles and
descriptions with brand, material, dimensions, color, and use case, then assign
one or more category queries.

Synthetic data should include many positives per category and hard negatives
from nearby categories. Do not use Nano evaluation product snippets or qrels as
generation seeds.

## Example Data

| Query | Positive document |
| --- | --- |
| Minen, Patronen & Tintenlöscher (31 chars) | Noodler's Tinte - 90 ml - Schwarz (33 chars) |
| Handwerkzeuge (13 chars) | AFA Tooling - (4 Pcs) Radio Removal Tool, OEM: 1C0-051-530 - Wird nicht brechen oder biegen (91 chars) |
| Stick- & Nähgarn (16 chars) | Clover Stickwerkzeug clover needlecraft this old art of embroidery using a fine hook on a fine cloth tightly stretched in a frame called tambour is reborn with kantan couture bead embroidery tool. basic techniques with this t ... [truncated 225 chars](321 chars) |
| Töpferei (8 chars) | Makin's Clay Tonpistole, Mehrfarbig (35 chars) |
| Tafeln (6 chars) | Sculpey S2 Original-Polymer Clay 1,75 Pounds/Pkg (48 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-German |
| Backing dataset | NanoMTEB-German |
| Task / split | xmarket_de |
| Hugging Face dataset | [hakari-bench/NanoMTEB-German](https://huggingface.co/datasets/hakari-bench/NanoMTEB-German) |
| Language | de, en |
| Category | natural_language |
| Queries | 182 |
| Documents | 10,000 |
| Positive qrels | 4,124 |
| Avg positives / query | 22.66 |
| Positives per query (min / median / max) | 1 / 7.5 / 100 |
| Queries with multiple positives | 155 (85.16%) |
| BM25 nDCG@10 | 0.2012 |
| BM25 hit@10 | 0.4780 |
| BM25 Recall@100 | 0.1360 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2268 |
| Dense hit@10 | 0.5659 |
| Dense Recall@100 | 0.2209 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.2210 |
| Reranking hybrid hit@10 | 0.5385 |
| Reranking hybrid Recall@100 | 0.2097 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 48 |
| Query length avg chars | 14.57 |
| Document length avg chars | 451.12 |

### Public Sources

- [Cross-Market Product Recommendation](https://arxiv.org/abs/2109.05929); 2021; Hamed Bonab, Mohammad Aliannejadi, Ali Vardasbi, Evangelos Kanoulas, and James Allan; DOI: `10.1145/3459637.3482493`.
- [XMRec project page](https://xmrec.github.io/).
- [mteb/XMarket dataset card](https://huggingface.co/datasets/mteb/XMarket).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-German](https://huggingface.co/datasets/hakari-bench/NanoMTEB-German)
- Source dataset: [mteb/XMarket](https://huggingface.co/datasets/mteb/XMarket)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Cross-Market Product Recommendation | 2021 | arXiv paper | https://arxiv.org/abs/2109.05929 |
| XMRec project page | 2021 | project page | https://xmrec.github.io/ |
| mteb/XMarket | 2025 | dataset card | https://huggingface.co/datasets/mteb/XMarket |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-German
  backing_dataset: NanoMTEB-German
  dataset_id: hakari-bench/NanoMTEB-German
  task_name: xmarket_de
  split_name: xmarket_de
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-German/xmarket_de.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2109.05929
    additional_source_urls:
    - https://xmrec.github.io/
    - https://huggingface.co/datasets/mteb/XMarket
  counts:
    queries: 182
    documents: 10000
    positive_qrels: 4124
  positives_per_query:
    average: 22.6593406593
    min: 1
    median: 7.5
    max: 100
    multi_positive_queries: 155
    multi_positive_query_percent: 85.1648351648
  text_stats_chars:
    query_mean: 14.5714285714
    document_mean: 451.1196
  bm25:
    ndcg_at_10: 0.20122867213175316
    hit_at_10: 0.47802197802197804
    source: dataset_candidate_subset
  learning:
    original_train_split: unknown
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude XMarket German evaluation products, qrels, and category-product
      pairs likely to overlap with the Nano split
    useful_training_data:
    - non-overlapping XMarket product metadata
    - multilingual e-commerce category-product pairs
    - German query-to-product click or purchase pairs
    - hard negatives from neighboring product categories
    synthetic_data:
      document_generation: marketplace product titles and descriptions with brand,
        material, dimensions, color, and use case
      question_generation: short German category labels and shopping-intent queries
        with multiple relevant products
      answerability: each product should clearly belong to the category or satisfy
        the shopping intent
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-German
    source_urls:
    - label: Cross-Market Product Recommendation arXiv
      url: https://arxiv.org/abs/2109.05929
    - label: XMRec project page
      url: https://xmrec.github.io/
    - label: mteb/XMarket
      url: https://huggingface.co/datasets/mteb/XMarket
    source_notes: []
  references:
  - title: Cross-Market Product Recommendation
    url: https://arxiv.org/abs/2109.05929
    year: 2021
    doi: 10.1145/3459637.3482493
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2012286721
      hit_at_10: 0.478021978
      recall_at_100: 0.1360329777
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 182
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1360329777
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2268383516
      hit_at_10: 0.5659340659
      recall_at_100: 0.2209020369
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 182
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2209020369
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.2210180066
      hit_at_10: 0.5384615385
      recall_at_100: 0.2097478177
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.263736
      query_count: 182
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2097478177
      safeguard_positive_rows: 48
      rows_with_101_candidates: 48
```
