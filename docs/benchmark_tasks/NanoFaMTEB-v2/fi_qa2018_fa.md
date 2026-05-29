# NanoFaMTEB-v2 / fi_qa2018_fa

## Overview

`fi_qa2018_fa` is a Persian financial QA retrieval task. Queries are finance
questions, and positive documents are answer passages or forum-style financial
explanations.

## Details

### What the Original Data Measures

[FaMTEB](https://arxiv.org/abs/2502.11571) includes Persian retrieval datasets
derived from translated BEIR-style tasks and new Persian data. This split uses
`MCINext/fiqa-fa-v2`, a Persian FiQA retrieval variant, evaluated under the MTEB
retrieval framework described by [MTEB](https://arxiv.org/abs/2210.07316).

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 534 positive qrels. Queries
average 65.78 characters, while documents average 763.49 characters. Positives
per query average 2.67 and can reach 12.

Observed queries ask about stock price ranges, price-to-book ratios, and
financial instruments. Documents are explanatory Persian passages, sometimes
with URLs or investment terminology.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column and the best-ranked positive,
BM25 reaches nDCG@10 = 0.3888 and hit@10 = 0.5300. It ranks 51 positives first.

BM25 is moderately useful but not dominant, because financial answers can explain
concepts without repeating the exact wording of the question.

### Training Data That May Help

Helpful data includes Persian finance QA, translated FiQA pairs, investment FAQ
retrieval, and financial forum answer selection. Exclude evaluation queries and
answer passages from this split.

### Synthetic Data Guidance

Generate Persian finance questions about ratios, securities, taxes, and personal
finance. Positives should give direct explanations; hard negatives should share
financial terms but answer a different question.

## Example Data

| Query | Positive document |
| --- | --- |
| مالیات بر سهام یا صندوق‌های قابل معامله در بورس (ETF) (53 chars) | اگر سهامی را بفروشید و هیچ توزیعی نداشته باشید، سود شما مشمول مالیات طبق ماده ۱۰٠١ می‌شود. اما همه سودهای محقق شده به عنوان مالیات شناسایی نمی‌شوند. و برخی از سودهایی که ممکن است محقق نشده باشند، به عنوان مالیات شناسایی خواهن ... [truncated 225 chars](1940 chars) |
| ال عال از چه نرخی برای تبدیل مبلغ نهایی پرداخت به شکل استفاده می‌کند؟ (69 chars) | نرخ "چک و حواله" توسط هر بانک چندین بار در طول روز و بر اساس بازار تعیین می‌شود. این نرخ با نرخ "نقد/اسکناس" که آن هم توسط هر بانک تعیین می‌شود و همچنین "نرخ نماینده" (שער היציג) که توسط بانک اسرائیل تعیین می‌گردد، متفاوت است ... [truncated 225 chars](630 chars) |
| کارمزد‌هایی که کارگزاری‌ها بابت هر معامله به بورس‌ها پرداخت می‌کنند چقدر است؟ (77 chars) | پاسخی قطعی برای این سوال وجود ندارد، اما کلیاتی در این زمینه وجود دارد. اکثر بورس‌ها تمایزی بین طرف منفعل و طرف فعال یک معامله قائل می‌شوند. شرکت‌کننده منفعل، سفارشی است که در زمان معامله در بازار وجود داشته است. این سفارشی ا ... [truncated 225 chars](1192 chars) |
| آیا درآمد حاصل از کار آزاد یک شهروند آمریکایی در حالی که در خارج از کشور زندگی می‌کند، مشمول مالیات بر درآمد ایالتی می‌شود؟ (123 chars) | مالیات ایالتی وجود ندارد، اما ایتالیا نیز با دولت فدرال آمریکا پیمان مالیاتی مطلوبی دارد. بررسی کنید که چگونه می‌توانید مالیات فدرال خود را به ۵٪ کاهش دهید؛ البته مطالعه‌ی آن کمی طولانی است: http://www.irs.gov/businesses/inte ... [truncated 225 chars](658 chars) |
| نرخ تورم چقدر است؟ (18 chars) | چیزی به نام شاخص قیمت مصرف‌کننده (CPI) وجود دارد. اساساً یک سبد کالا وجود دارد که افرادی که این شاخص را محاسبه می‌کنند، برای آن خرید می‌کنند. این سبد کالا بسیار مفصل‌تر است تا دقت بالاتری داشته باشد، اما در نهایت آن‌ها هر سال ... [truncated 225 chars](650 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoFaMTEB-v2 |
| Backing dataset | NanoFaMTEB-v2 |
| Task / split | fi_qa2018_fa |
| Hugging Face dataset | [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) |
| Language | fa |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 534 |
| Positives per query | avg 2.67, min 1, median 2.0, max 12 |
| BM25 nDCG@10 | 0.2923 |
| BM25 hit@10 | 0.5300 |
| BM25 Recall@100 | 0.6180 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3525 |
| Dense hit@10 | 0.6150 |
| Dense Recall@100 | 0.6948 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3722 |
| Reranking hybrid hit@10 | 0.6500 |
| Reranking hybrid Recall@100 | 0.7247 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 25 |
| Query length avg chars | 65.78 |
| Document length avg chars | 763.49 |

### Public Sources

- [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316).
- [MCINext/fiqa-fa-v2 dataset card](https://huggingface.co/datasets/MCINext/fiqa-fa-v2).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2)
- Source dataset: [MCINext/fiqa-fa-v2](https://huggingface.co/datasets/MCINext/fiqa-fa-v2)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FaMTEB: Massive Text Embedding Benchmark in Persian Language | 2025 | arXiv paper | https://arxiv.org/abs/2502.11571 |
| MTEB: Massive Text Embedding Benchmark | 2023 | arXiv paper | https://arxiv.org/abs/2210.07316 |
| MCINext/fiqa-fa-v2 | 2025 | dataset card | https://huggingface.co/datasets/MCINext/fiqa-fa-v2 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoFaMTEB-v2
  backing_dataset: NanoFaMTEB-v2
  dataset_id: hakari-bench/NanoFaMTEB-v2
  task_name: fi_qa2018_fa
  split_name: fi_qa2018_fa
  language: fa
  category: natural_language
  document_path: docs/benchmark_tasks/NanoFaMTEB-v2/fi_qa2018_fa.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 534
  positives_per_query:
    average: 2.67
    min: 1
    median: 2.0
    max: 12
    multi_positive_queries: 113
  text_stats_chars:
    query_mean: 65.775
    document_mean: 763.4903
  bm25:
    ndcg_at_10: 0.2923185989510702
    hit_at_10: 0.53
    source: dataset_candidate_subset
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2
    source_urls:
    - label: FaMTEB arXiv
      url: https://arxiv.org/abs/2502.11571
    - label: MCINext/fiqa-fa-v2
      url: https://huggingface.co/datasets/MCINext/fiqa-fa-v2
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
      ndcg_at_10: 0.292318599
      hit_at_10: 0.53
      recall_at_100: 0.6179775281
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6179775281
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3525202666
      hit_at_10: 0.615
      recall_at_100: 0.6947565543
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6947565543
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3722161762
      hit_at_10: 0.65
      recall_at_100: 0.7247191011
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.125
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7247191011
      safeguard_positive_rows: 25
      rows_with_101_candidates: 25
```
