# NanoMTEB-Scandinavian / swedn

## Overview

SWE-DN is a Swedish summarization corpus based on Dagens Nyheter articles, with
headlines, summaries, article text, and categories. The Scandinavian benchmark
turns this into retrieval by using a headline as the query and both the compact
summary and the longer article as positives. In the Nano split, every headline
has two positives, so the model should retrieve both forms of the same news
item. The queries are often quoted or editorial in style, while documents range
from short preambles to long articles and opinion pieces.

## Details

### What the Original Data Measures

The [SweDN 1.0 resource page](https://spraakbanken.gu.se/resurser/swedn)
describes SWE-DN as a Swedish text summarization corpus based on 1,963,576
Dagens Nyheter articles from 2000-2020, filtered to resemble CNN/DailyMail.
The resource lists 38,121 news articles with corresponding preambles and fields
including headline, summary, article, and category.

The SuperLim paper describes SweDN as a summarization task in which the lead
paragraph serves as the ground-truth summary. SEB converts summarization pairs
into retrieval by using headlines as queries and both summaries and articles as
positive corpus documents.

### Observed Data Profile

The Nano split has 200 Swedish queries, 2,046 documents, and 400 positive qrels.
Every query has exactly two positives. Queries average 45.26 characters, and
documents average 2,895.97 characters. Documents range from short preambles to
long news and opinion articles.

The queries are headlines, often quoted or editorial in style. The two-positive
setup means a retriever should retrieve both the compact summary and the longer
article for a headline.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.7081 and hit@10 = 0.8950. BM25 ranks a positive first for 146 queries and
retrieves at least one positive in the top 10 for 179 queries. Headline/article
term overlap helps, but abstractive headlines and opinion framing can push
positives down the ranking.

### Training Data That May Help

Useful training data includes non-overlapping SWE-DN headline-summary-article
pairs, Swedish news title-to-article retrieval, and hard negatives from the same
section or date. Training should account for the two-positive structure.

### Synthetic Data Guidance

Generate Swedish news articles with headlines and lead summaries. Use headline
queries and mark both the summary and the article as positives. Hard negatives
should share topic, outlet style, or named entities but describe a different
event or opinion.

## Example Data

| Query | Positive document |
| --- | --- |
| Gående är oskyddade i trafiken (30 chars) | Tror många cyklister glömmer att oavsett var en gående person befinner sig i trafiken så räknas de fortfarande som oskyddade gentemot all annan fordonstrafik och enligt lagen räknas cykel som ett fordon. Detta verkar helt glö ... [truncated 225 chars](419 chars) |
| Det är inte gratis att plocka bär (33 chars) | Skogens bär ingår i ett ekologiskt system och är knappast till för enbart människan. Det är inte gratis att plocka bär. Det kostar både tid och pengar. Det kräver utrustning och transporter. Väl på plats i bärskogen ger det e ... [truncated 225 chars](351 chars) |
| ”Skollagen ger barnen rätt till skolgång” (41 chars) | På DN-debatt (24/6) skriver regeringens nationelle samordnare för arbetet med utsatta EES-medborgare Martin Valfridsson tillsammans med Rickard Klerfors, om EU-migranters barns rätt till skolgång. De hävdar att ”det svenska s ... [truncated 225 chars](4289 chars) |
| ”Etablerade sanningar i politiken gäller inte längre” (53 chars) | Årets riksdagsval tydliggjorde att historiskt etablerade sanningar om väljarkåren inte längre gäller. Profetior från erfarna statsvetare om hur stora försprång som är möjliga att hämta in kom på skam, liksom vilka slutsatser ... [truncated 225 chars](7338 chars) |
| ”Ge barnen blodmat i stället för vegetariskt” (45 chars) | Det är inte bara en fråga om klimatet när man som förskolan Gitarren i Umeå väljer bort kött och köttprodukter till barn. Ingen talar om viktiga mineraler som barnen går miste om. Det är väl känt att järn är ett av det viktig ... [truncated 225 chars](1382 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Scandinavian |
| Backing dataset | NanoMTEB-Scandinavian |
| Task / split | swedn |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Scandinavian](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Scandinavian) |
| Language | sv |
| Category | natural_language |
| Queries | 200 |
| Documents | 2,046 |
| Positive qrels | 400 |
| BM25 nDCG@10 | 0.7081 |
| BM25 hit@10 | 0.8950 |
| BM25 Recall@100 | 0.8375 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7757 |
| Dense hit@10 | 0.9100 |
| Dense Recall@100 | 0.9025 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.7398 |
| Reranking hybrid hit@10 | 0.8800 |
| Reranking hybrid Recall@100 | 0.9400 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 2 |
| Query length avg chars | 45.26 |
| Document length avg chars | 2,895.97 |

### Public Sources

- [The Scandinavian Embedding Benchmarks](https://arxiv.org/abs/2406.02396); 2024; Kenneth Enevoldsen et al.
- [SweDN 1.0 resource page](https://spraakbanken.gu.se/resurser/swedn); Språkbanken Text.
- [Superlim: A Swedish Language Understanding Evaluation Benchmark](https://aclanthology.org/2023.emnlp-main.506/); 2023; Aleksandrs Berdicevskis et al.
- [mteb/SwednRetrieval dataset card](https://huggingface.co/datasets/mteb/SwednRetrieval).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Scandinavian](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Scandinavian)
- Source task: [mteb/SwednRetrieval](https://huggingface.co/datasets/mteb/SwednRetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| The Scandinavian Embedding Benchmarks | 2024 | arXiv paper | https://arxiv.org/abs/2406.02396 |
| SweDN 1.0 | 2025 | resource page | https://spraakbanken.gu.se/resurser/swedn |
| Superlim: A Swedish Language Understanding Evaluation Benchmark | 2023 | ACL Anthology paper | https://aclanthology.org/2023.emnlp-main.506/ |
| mteb/SwednRetrieval | 2024 | dataset card | https://huggingface.co/datasets/mteb/SwednRetrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Scandinavian
  backing_dataset: NanoMTEB-Scandinavian
  dataset_id: hakari-bench/NanoMTEB-Scandinavian
  task_name: swedn
  split_name: swedn
  language: sv
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Scandinavian/swedn.md
  source_research:
    primary_source_type: resource_page_and_benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: CLARIN/SweDN resource page and SuperLim/SEB papers were checked;
      the separate CLARIN annual conference paper was not fully reviewed in this pass.
  counts:
    queries: 200
    documents: 2046
    positive_qrels: 400
  positives_per_query:
    average: 2.0
    min: 2
    median: 2.0
    max: 2
    multi_positive_queries: 200
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 45.26
    document_mean: 2895.9706744868035
  bm25:
    ndcg_at_10: 0.7081125173979356
    hit_at_10: 0.895
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude Nano headlines, qrels, and matching SWE-DN summary/article
      documents
    useful_training_data:
    - non-overlapping SWE-DN headline-summary-article pairs
    - Swedish news title-to-article retrieval pairs
    - same-section and same-date hard negatives
    - multi-positive news retrieval examples
    synthetic_data:
      document_generation: Swedish news articles and lead summaries with headline,
        date, section, and named entities
      question_generation: Swedish headline queries, including opinion and quote-style
        headlines
      answerability: both the summary and the full article can be positive for a headline
        query
    multi_positive_training: treat_summary_and_article_as_valid_positives
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Scandinavian
    source_urls:
    - label: Scandinavian Embedding Benchmarks
      url: https://arxiv.org/abs/2406.02396
    - label: SweDN 1.0
      url: https://spraakbanken.gu.se/resurser/swedn
    - label: Superlim paper
      url: https://aclanthology.org/2023.emnlp-main.506/
    - label: mteb/SwednRetrieval
      url: https://huggingface.co/datasets/mteb/SwednRetrieval
    source_notes:
    - SEB states that summarization datasets are converted by using headlines as queries
      and summaries/articles as corpus positives.
  references:
  - title: SweDN 1.0
    url: https://spraakbanken.gu.se/resurser/swedn
    year: 2025
    doi: 10.23695/36v9-9017
    is_paper: false
    source_confidence: official_resource_page
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7081125174
      hit_at_10: 0.895
      recall_at_100: 0.8375
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8375
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7757365464
      hit_at_10: 0.91
      recall_at_100: 0.9025
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9025
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.7398145343
      hit_at_10: 0.88
      recall_at_100: 0.94
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.01
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.94
      safeguard_positive_rows: 2
      rows_with_101_candidates: 2
```
