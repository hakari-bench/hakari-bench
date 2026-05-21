# NanoMTEB-German

## Overview

NanoMTEB-German is the compact German retrieval group for MTEB-style evaluation.
It contains five retrieval tasks: German legal precedent retrieval, German
open-domain QA passage retrieval, GermanQuAD context retrieval, Munich municipal
service retrieval, and German e-commerce category-to-product retrieval. The
group tests German retrieval across very different document types, from long
court decisions to short product metadata and government-service pages.

The group is small, but its retrieval relations are deliberately different.
GerDaLIR asks for long legal decisions from legal passages, GermanDPR and
GermanQuAD ask for answer-bearing Wikipedia contexts, the Munich service task
maps citizen wording to administrative pages, and XMarket maps short category
queries to many relevant products. The group is best read as a mix of legal,
encyclopedic, civic, and marketplace retrieval rather than as generic German QA.

## Details

### What the Original Group Measures

The group is not tied to one source paper. It collects German retrieval-family
tasks used in MTEB and related multilingual MTEB coverage. GermanDPR and
GermanQuAD measure native German question-to-context retrieval over German
Wikipedia. GerDaLIR measures German legal information retrieval from Open Legal
Data case material. The Munich government-service task measures citizen
question-to-service-page retrieval. XMarket adapts cross-market e-commerce data
into a German category-to-product retrieval task.

At group level, NanoMTEB-German asks whether a model can handle German language
retrieval across legal, encyclopedic, administrative, and marketplace text. It
also mixes single-positive and multi-positive tasks: the QA and government
service splits are exact context or page retrieval, while XMarket has many
relevant products per short category query.

### Subtask Coverage

The five subtasks cover four retrieval families:

- **German legal retrieval:** `ger_da_lir` retrieves long German legal case
  documents for legal reasoning passages.
- **German QA context retrieval:** `german_dpr` and `german_qu_ad` retrieve
  German Wikipedia passages that contain answers to fact questions.
- **German public-service retrieval:** `gov_service` retrieves Munich municipal
  service descriptions for citizen questions.
- **German e-commerce retrieval:** `xmarket_de` retrieves product metadata for
  short product-category or shopping-intent queries.

All tasks are German-language retrieval except `xmarket_de`, which is marked
multilingual because German marketplace data often contains English brand,
product, or category text. The group therefore measures German retrieval
robustness as well as cross-lingual noise inside German product metadata.

### Observed Group Profile

Across the five splits, NanoMTEB-German contains 982 queries, 4,959 positive
qrels, and 23,455 split-local candidate documents. The document count is a sum
across subtasks, not a deduplicated group-wide corpus size. The group average is
5.05 positives per query, but that average is driven by `xmarket_de`, which has
4,124 positive qrels for 182 queries. The three QA/service splits are exactly
single-positive, and `ger_da_lir` is only lightly multi-positive.

The query and document lengths vary sharply. `xmarket_de` has the shortest
queries, averaging 14.57 characters, while `ger_da_lir` uses long legal passages
averaging 879.53 characters. Documents range from 105 short municipal service
pages to 10,000 long legal case documents. The query-weighted mean query length
is 218.99 characters, and the document-weighted mean document length is
8,099.81 characters because the legal corpus is very long.

### BM25 Difficulty

The query-weighted BM25 baseline reaches nDCG@10 = 0.5455 and hit@10 = 0.7424.
The easiest split is `german_qu_ad` with nDCG@10 = 0.9042 and hit@10 = 0.9750,
where the small answer-context corpus and direct Wikipedia questions make
lexical retrieval very strong. The hardest split is `xmarket_de` with nDCG@10 =
0.2408 and hit@10 = 0.4286, despite having many positives per query.

The hard cases differ by subtask. In GerDaLIR, long decisions and legal
boilerplate dilute lexical signals. In GermanDPR and GermanQuAD, the correct
answer passage may not repeat the question wording exactly. In government
service retrieval, many pages share formal words such as documents,
applications, fees, and appointments. In XMarket, category relevance can be
broader than exact product-title overlap, and product metadata may be noisy or
mixed-language.

### Training Data That May Help

Useful training data includes non-overlapping GermanDPR and GermanQuAD
question-context pairs, German Wikipedia passage retrieval, GerDaLIR train data
or other legal citation retrieval data, German public-administration FAQ and
service-page mappings, and multilingual e-commerce category-product pairs.
Training should exclude NanoMTEB-German evaluation queries, qrels, and positive
documents, plus upstream test examples from the source datasets.

Hard negatives should be task-specific. For legal retrieval, negatives should
share statutes or legal vocabulary but differ in precedent relevance. For
Wikipedia QA, negatives should come from related pages or passages with a
different answer. For government services, negatives should be nearby municipal
procedures. For XMarket, negatives should be products in neighboring categories.

### Synthetic Data Guidance

Synthetic data should preserve each task's document genre. German Wikipedia
examples should use answer-bearing passages and self-contained German questions.
Legal examples should keep German legal phrasing, procedural posture, and
statutory vocabulary. Government-service examples should include required
documents, fees, deadlines, authorities, and eligibility conditions. E-commerce
examples should use concise German category queries and product metadata with
brand, material, size, color, and use case.

Synthetic negatives should be close enough to force fine-grained ranking, and
Nano evaluation documents or qrels should not be used as seeds.

## Task Summary

| Task | Retrieval shape | Lang | Queries | Docs | Positive qrels | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars | Source status |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [ger_da_lir](ger_da_lir.md) | legal passage to German case document | de | 200 | 10,000 | 235 | 0.5444 | 0.6900 | 879.53 | 18,071.48 | GerDaLIR source + MTEB |
| [german_dpr](german_dpr.md) | German fact question to Wikipedia passage | de | 200 | 2,876 | 200 | 0.4230 | 0.7900 | 63.71 | 1,288.60 | GermanDPR source + MTEB |
| [german_qu_ad](german_qu_ad.md) | GermanQuAD question to context paragraph | de | 200 | 474 | 200 | 0.9042 | 0.9750 | 54.88 | 1,937.65 | GermanQuAD source + MTEB |
| [gov_service](gov_service.md) | citizen question to municipal service page | de | 200 | 105 | 200 | 0.5875 | 0.8000 | 63.88 | 1,244.25 | dataset card + MTEB |
| [xmarket_de](xmarket_de.md) | German category label to product metadata | multilingual | 182 | 10,000 | 4,124 | 0.2408 | 0.4286 | 14.57 | 451.12 | XMarket paper + MTEB |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-German |
| Backing dataset | NanoMTEB-German |
| Hugging Face dataset | [hakari-bench/NanoMTEB-German](https://huggingface.co/datasets/hakari-bench/NanoMTEB-German) |
| Languages | de, multilingual |
| Category | natural_language |
| Subtasks | 5 |
| Total queries | 982 |
| Split-local documents | 23,455 |
| Positive qrels | 4,959 |
| Positives per query | 5.05 average |
| Multi-positive queries | 184 |
| Query-weighted BM25 nDCG@10 | 0.5455 |
| Query-weighted BM25 hit@10 | 0.7424 |
| Mean query length | 218.99 chars, weighted by query count |
| Mean document length | 8,099.81 chars, weighted by split-local document count |

### Public Sources

- [GerDaLIR source repository](https://github.com/lavis-nlp/GerDaLIR).
- [GermanDPR source dataset](https://huggingface.co/datasets/deepset/germandpr).
- [GermanQuAD source dataset](https://huggingface.co/datasets/deepset/germanquad).
- [LHM-Dienstleistungen-QA](https://huggingface.co/datasets/it-at-m/LHM-Dienstleistungen-QA).
- [Cross-Market Product Recommendation](http://dx.doi.org/10.1145/3459637.3482493); 2021; XMarket source paper.
- [Massive Text Embedding Benchmark (MTEB)](https://github.com/embeddings-benchmark/mteb).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-German](https://huggingface.co/datasets/hakari-bench/NanoMTEB-German)
- Source datasets:
  [mteb/GerDaLIR](https://huggingface.co/datasets/mteb/GerDaLIR),
  [mteb/GermanDPR](https://huggingface.co/datasets/mteb/GermanDPR),
  [mteb/germanquad-retrieval](https://huggingface.co/datasets/mteb/germanquad-retrieval),
  [it-at-m/LHM-Dienstleistungen-QA](https://huggingface.co/datasets/it-at-m/LHM-Dienstleistungen-QA),
  [mteb/XMarket](https://huggingface.co/datasets/mteb/XMarket).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| GerDaLIR source reference | 2021 | source repository | https://github.com/lavis-nlp/GerDaLIR |
| GermanDPR source reference | 2021 | dataset card | https://huggingface.co/datasets/deepset/germandpr |
| GermanQuAD-Retrieval source reference | 2021 | dataset card | https://huggingface.co/datasets/deepset/germanquad |
| GermanGovServiceRetrieval source reference | 2022 | dataset card | https://huggingface.co/datasets/it-at-m/LHM-Dienstleistungen-QA |
| Cross-Market Product Recommendation | 2021 | source task paper | http://dx.doi.org/10.1145/3459637.3482493 |
| Massive Text Embedding Benchmark (MTEB) | 2022 | benchmark repository | https://github.com/embeddings-benchmark/mteb |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoMTEB-German
  backing_dataset: NanoMTEB-German
  dataset_id: hakari-bench/NanoMTEB-German
  language: de
  languages:
    - de
    - multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-German/index.md
  source_research:
    primary_source_type: multiple_dataset_cards_and_source_references
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 5
    queries: 982
    split_local_documents: 23455
    positive_qrels: 4959
  positives_per_query:
    average: 5.04989816700611
    min: 1
    median_task_median: 1.0
    max: 100
    multi_positive_tasks: 2
    multi_positive_queries: 184
  text_stats_chars:
    query_mean_weighted_by_queries: 218.9928716904224
    document_mean_weighted_by_documents: 8099.812278879512
  bm25:
    ndcg_at_10_query_weighted: 0.5454870786727087
    hit_at_10_query_weighted: 0.7423625254635439
    ndcg_at_10_unweighted_task_mean: 0.5400028974
    hit_at_10_unweighted_task_mean: 0.73671428572
    source: dataset_bm25_column
    easiest_task_by_ndcg_at_10: german_qu_ad
    hardest_task_by_ndcg_at_10: xmarket_de
  tasks:
    - name: ger_da_lir
      path: docs/benchmark_tasks/NanoMTEB-German/ger_da_lir.md
      retrieval_shape: legal_passage_to_german_case_document
      language: de
      queries: 200
      documents: 10000
      positive_qrels: 235
      bm25_ndcg_at_10: 0.5444239126
      bm25_hit_at_10: 0.69
    - name: german_dpr
      path: docs/benchmark_tasks/NanoMTEB-German/german_dpr.md
      retrieval_shape: german_fact_question_to_wikipedia_passage
      language: de
      queries: 200
      documents: 2876
      positive_qrels: 200
      bm25_ndcg_at_10: 0.4230457645
      bm25_hit_at_10: 0.79
    - name: german_qu_ad
      path: docs/benchmark_tasks/NanoMTEB-German/german_qu_ad.md
      retrieval_shape: germanquad_question_to_context_paragraph
      language: de
      queries: 200
      documents: 474
      positive_qrels: 200
      bm25_ndcg_at_10: 0.9042226524
      bm25_hit_at_10: 0.975
    - name: gov_service
      path: docs/benchmark_tasks/NanoMTEB-German/gov_service.md
      retrieval_shape: citizen_question_to_municipal_service_page
      language: de
      queries: 200
      documents: 105
      positive_qrels: 200
      bm25_ndcg_at_10: 0.5875118162
      bm25_hit_at_10: 0.8
    - name: xmarket_de
      path: docs/benchmark_tasks/NanoMTEB-German/xmarket_de.md
      retrieval_shape: german_category_label_to_product_metadata
      language: multilingual
      queries: 182
      documents: 10000
      positive_qrels: 4124
      bm25_ndcg_at_10: 0.2408103413
      bm25_hit_at_10: 0.4285714286
  learning:
    leakage_note: exclude NanoMTEB-German evaluation queries, qrels, positive documents, and upstream test examples from the source datasets
    useful_training_data:
      - GermanDPR and GermanQuAD train question-context pairs
      - German Wikipedia passage retrieval with hard negatives
      - German legal passage-to-case and citation retrieval pairs
      - German municipal service question-page mappings
      - multilingual e-commerce category-product retrieval pairs
      - task-specific hard negatives from related pages, services, cases, or product categories
    synthetic_data:
      document_generation: German Wikipedia passages, legal decisions, municipal service pages, and product metadata in the appropriate genre
      question_generation: German fact questions, legal reasoning passages, citizen service questions, and concise product-category queries grounded in the generated or selected document
      answerability: positives must satisfy the exact answer, service, precedent, or category relation rather than only sharing German keywords
    multi_positive_training: preserve_xmarket_category_product_multi_positive_structure
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-German
    source_urls:
      - label: GerDaLIR source reference
        url: https://github.com/lavis-nlp/GerDaLIR
      - label: mteb/GerDaLIR
        url: https://huggingface.co/datasets/mteb/GerDaLIR
      - label: deepset/germandpr
        url: https://huggingface.co/datasets/deepset/germandpr
      - label: mteb/GermanDPR
        url: https://huggingface.co/datasets/mteb/GermanDPR
      - label: deepset/germanquad
        url: https://huggingface.co/datasets/deepset/germanquad
      - label: mteb/germanquad-retrieval
        url: https://huggingface.co/datasets/mteb/germanquad-retrieval
      - label: it-at-m/LHM-Dienstleistungen-QA
        url: https://huggingface.co/datasets/it-at-m/LHM-Dienstleistungen-QA
      - label: XMarket paper DOI
        url: http://dx.doi.org/10.1145/3459637.3482493
      - label: mteb/XMarket
        url: https://huggingface.co/datasets/mteb/XMarket
    source_notes: []
  references:
    - title: GerDaLIR source reference
      url: https://github.com/lavis-nlp/GerDaLIR
      year: 2021
      is_paper: false
      source_confidence: dataset_source_reference
    - title: GermanDPR source reference
      url: https://huggingface.co/datasets/deepset/germandpr
      year: 2021
      is_paper: false
      source_confidence: dataset_source_reference
    - title: GermanQuAD-Retrieval source reference
      url: https://huggingface.co/datasets/deepset/germanquad
      year: 2021
      is_paper: false
      source_confidence: dataset_source_reference
    - title: GermanGovServiceRetrieval source reference
      url: https://huggingface.co/datasets/it-at-m/LHM-Dienstleistungen-QA
      year: 2022
      is_paper: false
      source_confidence: dataset_source_reference
    - title: Cross-Market Product Recommendation
      url: http://dx.doi.org/10.1145/3459637.3482493
      year: 2021
      is_paper: true
      source_confidence: definitive_paper_link
    - title: Massive Text Embedding Benchmark (MTEB)
      url: https://github.com/embeddings-benchmark/mteb
      year: 2022
      is_paper: false
      source_confidence: benchmark_repository
```
