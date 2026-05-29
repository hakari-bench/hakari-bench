# MNanoBEIR / NanoBEIR-no / NanoDBPedia

## Overview

DBpedia-Entity is an entity retrieval benchmark. `NanoBEIR-no__NanoDBPedia`
uses Norwegian translated entity-style queries to retrieve Norwegian translated
DBpedia entity descriptions.

## Details

### What the Original Data Measures

[DBpedia-Entity V2](https://doi.org/10.1145/3077136.3080751) evaluates entity
search over DBpedia. [BEIR](https://arxiv.org/abs/2104.08663) includes it as an
entity retrieval task, and [MMTEB](https://arxiv.org/abs/2502.13595) provides
the multilingual benchmark context for this Norwegian split.

### Observed Data Profile

The sampled Norwegian Nano task has 50 queries, 6,045 documents, and 1,158
positive qrel rows. It is strongly multi-positive, averaging 23.16 positives per
query. Queries are short entity needs averaging 36.86 characters, while
documents are compact entity descriptions averaging 331.00 characters.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.4684 and hit@10 = 0.8400. Entity name overlap makes many records easy, but
category-style queries still need ranking among many plausible entities.

### Training Data That May Help

Useful training data includes non-overlapping entity search, Wikipedia/DBpedia
entity linking, multilingual entity retrieval, and short-query passage retrieval
data. Training should exclude DBpedia-Entity, BEIR, NanoBEIR, and translated
entity records likely to overlap.

### Synthetic Data Guidance

Generate Norwegian entity needs from non-evaluation entity descriptions.
Include both exact-name and category-style queries, with hard negatives from
related entities.

## Example Data

| Query | Positive document |
| --- | --- |
| Fitzgerald bilutstillingssenter i Chambersburg, PA (50 chars) | Fitzgerald Auto Malls er en familieeid og drevet bilforhandler som ble grunnlagt i 1966, med sin første lokalisering åpnet i Bethesda, Maryland. Per 2014, Fitzgerald Auto Malls var rangert som nummer 59 på listen over 'Topp 1 ... [truncated 225 chars](424 chars) |
| Hvor kan jeg finne samlingen av kortfortellinger fra 1994 av Alice Munro? (73 chars) | Alice Ann Munro (/ˈælɨs ˌæn mʌnˈroʊ/, født Laidlaw /ˈleɪdlɔː/; født 10. juli 1931) er en kanadisk forfatter. Munros arbeid er blitt beskrevet som å ha revolusjonert kortprosasjangeren, spesielt i sin tendens til å bevege seg ... [truncated 225 chars](491 chars) |
| Galloromersk arkitektur i Paris (31 chars) | Kunst i Paris er en artikkel om kunstkulturen og historien i Paris, Frankrikes hovedstad. I århundrer har Paris tiltrukket kunstnere fra hele verden, som kommer til byen for å utdanne seg og finne inspirasjon i byens kunstner ... [truncated 225 chars](300 chars) |
| De tidligere jugoslaviske republikkene (38 chars) | Den jugoslaviske grunnloven av 1974 var den fjerde og siste grunnloven for Den sosialistiske føderale republikken Jugoslavia. Den trådte i kraft 21. februar. Med 406 opprinnelige artikler var den jugoslaviske grunnloven av 19 ... [truncated 225 chars](436 chars) |
| Filmer innspilt i Venezia (25 chars) | En liten romanse er en amerikansk romantisk komedie fra 1979, innspilt i Technicolor og Panavision, regissert av George Roy Hill og med Laurence Olivier, Thelonious Bernard og Diane Lane i hennes filmdebut. Manusforfatterne v ... [truncated 225 chars](376 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-no |
| Task / split | NanoDBPedia |
| Hugging Face dataset | [hakari-bench/NanoBEIR-no](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no) |
| Language | no |
| Category | natural_language |
| Queries | 50 |
| Documents | 6,045 |
| Positive qrels | 1,158 |
| Avg positives / query | 23.16 |
| Positives per query (min / median / max) | 1 / 18.00 / 81 |
| Queries with multiple positives | 48 (96.0%) |
| BM25 nDCG@10 | 0.4684 |
| BM25 hit@10 | 0.8400 |
| BM25 Recall@100 | 0.5173 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.5506 |
| Dense hit@10 | 0.9000 |
| Dense Recall@100 | 0.6468 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.5184 |
| Reranking hybrid hit@10 | 0.9200 |
| Reranking hybrid Recall@100 | 0.6373 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 36.86 |
| Document length avg chars | 331.00 |

### Public Sources

- [DBpedia-Entity V2](https://doi.org/10.1145/3077136.3080751).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-no](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| DBpedia-Entity V2 | 2017 | task paper | https://doi.org/10.1145/3077136.3080751 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: MNanoBEIR
  backing_dataset: NanoBEIR-no
  dataset_id: hakari-bench/NanoBEIR-no
  task_name: NanoDBPedia
  split_name: NanoDBPedia
  language: 'no'
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-no__NanoDBPedia.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 6045
    positive_qrels: 1158
  positives_per_query:
    average: 23.16
    min: 1
    median: 18.0
    max: 81
    multi_positive_queries: 48
    multi_positive_query_percent: 96.0
  text_stats_chars:
    query_mean: 36.86
    document_mean: 331.001323
  bm25:
    ndcg_at_10: 0.46835456227809047
    hit_at_10: 0.84
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4683545623
      hit_at_10: 0.84
      recall_at_100: 0.5172711572
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5172711572
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5506162036
      hit_at_10: 0.9
      recall_at_100: 0.6468048359
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6468048359
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.5183912406
      hit_at_10: 0.92
      recall_at_100: 0.6373056995
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6373056995
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
