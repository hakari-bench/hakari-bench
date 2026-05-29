# NanoFaMTEB-v2 / persian_web_document

## Overview

`persian_web_document` is a Persian web document retrieval task. Queries are
very short web-search phrases, and documents are web page snippets or passages.

## Details

### What the Original Data Measures

[FaMTEB](https://arxiv.org/abs/2502.11571) reports that it adds Persian
retrieval datasets, including web-collected resources, to broaden Persian
embedding evaluation. The task metadata points to `MCINext/persian-web-document-retrieval`
and an IEEE record for the source reference. [MTEB](https://arxiv.org/abs/2210.07316)
provides the retrieval evaluation framing.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 2,186 positive qrels. Queries
are extremely short, averaging 16.35 characters. Documents average 228.31
characters, though some are much longer. Positives per query average 10.93.

Observed queries include Persian web-search terms such as music-video searches
and event names. Documents look like search-result snippets or short web pages.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column and the best-ranked positive,
BM25 reaches nDCG@10 = 0.8210 and hit@10 = 0.9500. It ranks 140 positives first.

The task is highly lexical: short web queries often appear directly in relevant
documents. Remaining difficulty comes from ambiguous short queries and many
near-duplicate web snippets.

### Training Data That May Help

Helpful data includes Persian web search logs, query-document click pairs,
Persian snippet retrieval, and hard negatives from the same search results.
Exclude evaluation queries and qrels.

### Synthetic Data Guidance

Generate short Persian web queries and snippets. Include spelling variants,
ambiguous entity names, and hard negatives that share the exact query phrase but
answer a different intent.

## Example Data

| Query | Positive document |
| --- | --- |
| فیلم سینمایی۳۵۶ روز بدون‌سانسور (31 chars) | دانلود فیلم 365 روز 1 (بدون سانسور) - فیلو دانلود فیلم 365 روز 1 (بدون سانسور) تیزر مووی (89 chars) |
| کلیپ عاشفانه (12 chars) | آپارات \| کافه کلیپ عاشقانه (27 chars) |
| واکینگ دد قسمت ۲۲ فصل ۱۱ (24 chars) | سریال مردگان متحرک :: فصل 11 قسمت 22 :: زیرنویس فارسی دانلود فصل یازدهم مجموعه واکینگ دِد(The Walking Dead - مردگان متحرک) با زیرنویس فارسی و کیفیت فول اچ دی 1080p Full HD \| رده سنی: 15+ سال \| محصول: امریکا \| ژانر:درام، وحشت، ... [truncated 225 chars](596 chars) |
| اگه ارومیه بشی روت ارس میکشم (28 chars) | دانلود آهنگ اگه ارومیه بشی روت ارس میکشم + ریمیکس (کامل + متن) دانلود آهنگ اگه ارومیه بشی روت ارس میکشم اهنگ اگه ارومیه بشی روت ارس میکشم با بالاترین کیفیت بصورت کامل Download Music Hichkas - Age Urumie Beshi دانلود (216 chars) |
| سوره قران (9 chars) | سوره بیستم قران ⚡️ [ پاســخ کامــل و درست ] سوره بیستم قران جواب سوره بیستم قران کاملا رایگان در سایت مجله اینترنتی باحال مگ (126 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoFaMTEB-v2 |
| Backing dataset | NanoFaMTEB-v2 |
| Task / split | persian_web_document |
| Hugging Face dataset | [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) |
| Language | fa |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 2186 |
| Positives per query | avg 10.93, min 1, median 9.0, max 39 |
| BM25 nDCG@10 | 0.6990 |
| BM25 hit@10 | 0.9500 |
| BM25 Recall@100 | 0.9607 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7780 |
| Dense hit@10 | 0.9700 |
| Dense Recall@100 | 0.9689 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.7703 |
| Reranking hybrid hit@10 | 0.9750 |
| Reranking hybrid Recall@100 | 0.9895 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 16.35 |
| Document length avg chars | 228.31 |

### Public Sources

- [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316).
- [PersianWebDocumentRetrieval source reference](https://ieeexplore.ieee.org/document/10553090).
- [MCINext/persian-web-document-retrieval dataset card](https://huggingface.co/datasets/MCINext/persian-web-document-retrieval).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2)
- Source dataset: [MCINext/persian-web-document-retrieval](https://huggingface.co/datasets/MCINext/persian-web-document-retrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FaMTEB: Massive Text Embedding Benchmark in Persian Language | 2025 | arXiv paper | https://arxiv.org/abs/2502.11571 |
| MTEB: Massive Text Embedding Benchmark | 2023 | arXiv paper | https://arxiv.org/abs/2210.07316 |
| PersianWebDocumentRetrieval source reference | 2024 | IEEE record | https://ieeexplore.ieee.org/document/10553090 |
| MCINext/persian-web-document-retrieval | 2025 | dataset card | https://huggingface.co/datasets/MCINext/persian-web-document-retrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoFaMTEB-v2
  backing_dataset: NanoFaMTEB-v2
  dataset_id: hakari-bench/NanoFaMTEB-v2
  task_name: persian_web_document
  split_name: persian_web_document
  language: fa
  category: natural_language
  document_path: docs/benchmark_tasks/NanoFaMTEB-v2/persian_web_document.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 2186
  positives_per_query:
    average: 10.93
    min: 1
    median: 9.0
    max: 39
    multi_positive_queries: 181
  text_stats_chars:
    query_mean: 16.35
    document_mean: 228.3112
  bm25:
    ndcg_at_10: 0.6990298407640672
    hit_at_10: 0.95
    source: dataset_candidate_subset
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2
    source_urls:
    - label: FaMTEB arXiv
      url: https://arxiv.org/abs/2502.11571
    - label: MCINext/persian-web-document-retrieval
      url: https://huggingface.co/datasets/MCINext/persian-web-document-retrieval
  references:
  - title: 'FaMTEB: Massive Text Embedding Benchmark in Persian Language'
    url: https://arxiv.org/abs/2502.11571
    year: 2025
    is_paper: true
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6990298408
      hit_at_10: 0.95
      recall_at_100: 0.9606587374
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9606587374
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7780360248
      hit_at_10: 0.97
      recall_at_100: 0.9688929552
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9688929552
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.7703212725
      hit_at_10: 0.975
      recall_at_100: 0.9894784995
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9894784995
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
