# NanoFaMTEB-v2 / fever_fa

## Overview

`fever_fa` is a Persian fact-verification retrieval task. The query is a short
claim, and the model retrieves Persian evidence passages.

## Details

### What the Original Data Measures

[FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571)
states that a substantial part of its retrieval data comes from BEIR-style tasks
translated into Persian, plus hard-negative retrieval datasets. [MTEB](https://arxiv.org/abs/2210.07316)
provides the shared retrieval evaluation protocol. This split uses
`MCINext/FEVER_FA_test_top_250_only_w_correct-v2`, a Persian FEVER hard-negative
dataset.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 229 positive qrels. Queries are
short Persian factual claims averaging 47.09 characters. Documents average
523.29 characters and are mostly encyclopedia-style evidence passages.

Some queries have multiple positives, with 1.15 positives per query on average
and up to 4.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column and the best-ranked positive
per query, BM25 reaches nDCG@10 = 0.8240 and hit@10 = 0.9000. It ranks 149
positives first.

Lexical retrieval is very strong because claims often name the entity and the
evidence document begins with the same entity title.

### Training Data That May Help

Helpful training data includes Persian fact-checking retrieval, translated FEVER
claim-evidence pairs, and entity-centric Wikipedia evidence retrieval. Exclude
NanoFaMTEB-v2 rows and translated duplicates from the evaluation split.

### Synthetic Data Guidance

Generate Persian factual claims over encyclopedia passages. Positives should
contain direct evidence, while hard negatives should share the named entity but
not support the claim.

## Example Data

| Query | Positive document |
| --- | --- |
| یک پرنده بر فراز آشیانه نسترن تنها یک جایزه اسکار را برنده شد. (62 chars) | بر فراز آشیانه فاخته (فیلم) پرواز بر فراز آشیانه فاخته فیلمی آمریکایی محصول سال ۱۹۷۵ به کارگردانی میلوش فورمن، بر اساس رمانی به همین نام از کن کسی است. جک نیکلسون در این فیلم بازی کرده و لوئیز فletcher، ویلیام ردفیلد، ویل سام ... [truncated 225 chars](925 chars) |
| دره رود سالت در کنار رودخانه می‌سی‌سی‌پی قرار دارد. (51 chars) | دره رودخانه سالت دره رودخانه نمک در مرکز آریزونا یک دره وسیع در امتداد رودخانه نمک است که منطقه کلان‌شهری فینیکس را در خود جای داده است. اگرچه این اصطلاح جغرافیایی هنوز هم برای شناسایی این منطقه استفاده می‌شود، نام «دره آفتاب ... [truncated 225 chars](527 chars) |
| اسکای یوکی یک شرکت مخابراتی بریتانیایی است. (43 chars) | بریتانیا پادشاهی متحد بریتانیای کبیر و ایرلند شمالی، که معمولاً به عنوان پادشاهی متحد (بریتانیا) شناخته می‌شود، کشوری مستقل در اروپای غربی است. این کشور در سواحل شمال غربی سرزمین اصلی اروپا واقع شده و شامل جزیرهٔ بریتانیای کب ... [truncated 225 chars](4136 chars) |
| کایا اسکودلاریو یک کارگردان است. (32 chars) | کایا اسکودلاریو کایا اسکودلاریو-دیویس (زاده کایا رز هامفری؛ ۱۳ مارس ۱۹۹۲) بازیگر انگلیسی است. او با نقش آفرینی در نقش افی استونم در سریال درام نوجوان شبکه E4 به نام Skins (۲۰۰۷-۲۰۱۰) وارد دنیای بازیگری شد و به خاطر آن مورد تو ... [truncated 225 chars](1535 chars) |
| در سال ۲۰۱۲، شهر سیمی ولی در کالیفرنیا گزارش داد که درآمد متوسط خانوار در این شهر برای اولین بار در یک دهه گذشته، از میانگین کشوری پایین‌تر رفته است. (149 chars) | سیمی ولی، کالیفرنیا شهر سیمی ولی (از واژه چوماش، شیمیی) در دره‌ای به همین نام، در گوشه جنوب شرقی شهرستان ونتورا، کالیفرنیا، ایالات متحده واقع شده است. سیمی ولی در فاصله ۳۰ مایلی مرکز شهر لس‌آنجلس قرار دارد و بخشی از منطقه بزر ... [truncated 225 chars](1485 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoFaMTEB-v2 |
| Backing dataset | NanoFaMTEB-v2 |
| Task / split | fever_fa |
| Hugging Face dataset | [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) |
| Language | fa |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 229 |
| Positives per query | avg 1.15, min 1, median 1.0, max 4 |
| BM25 nDCG@10 | 0.8025 |
| BM25 hit@10 | 0.9000 |
| BM25 Recall@100 | 0.9432 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8972 |
| Dense hit@10 | 0.9450 |
| Dense Recall@100 | 0.9170 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8396 |
| Reranking hybrid hit@10 | 0.9250 |
| Reranking hybrid Recall@100 | 0.9825 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 47.09 |
| Document length avg chars | 523.29 |

### Public Sources

- [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316).
- [MCINext/FEVER_FA_test_top_250_only_w_correct-v2 dataset card](https://huggingface.co/datasets/MCINext/FEVER_FA_test_top_250_only_w_correct-v2).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2)
- Source dataset: [MCINext/FEVER_FA_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/MCINext/FEVER_FA_test_top_250_only_w_correct-v2)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FaMTEB: Massive Text Embedding Benchmark in Persian Language | 2025 | arXiv paper | https://arxiv.org/abs/2502.11571 |
| MTEB: Massive Text Embedding Benchmark | 2023 | arXiv paper | https://arxiv.org/abs/2210.07316 |
| MCINext/FEVER_FA_test_top_250_only_w_correct-v2 | 2025 | dataset card | https://huggingface.co/datasets/MCINext/FEVER_FA_test_top_250_only_w_correct-v2 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoFaMTEB-v2
  backing_dataset: NanoFaMTEB-v2
  dataset_id: hakari-bench/NanoFaMTEB-v2
  task_name: fever_fa
  split_name: fever_fa
  language: fa
  category: natural_language
  document_path: docs/benchmark_tasks/NanoFaMTEB-v2/fever_fa.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 229
  positives_per_query:
    average: 1.145
    min: 1
    median: 1.0
    max: 4
    multi_positive_queries: 24
  text_stats_chars:
    query_mean: 47.09
    document_mean: 523.2888
  bm25:
    ndcg_at_10: 0.8025116003961094
    hit_at_10: 0.9
    source: dataset_candidate_subset
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2
    source_urls:
    - label: FaMTEB arXiv
      url: https://arxiv.org/abs/2502.11571
    - label: MCINext/FEVER_FA_test_top_250_only_w_correct-v2
      url: https://huggingface.co/datasets/MCINext/FEVER_FA_test_top_250_only_w_correct-v2
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
      ndcg_at_10: 0.8025116004
      hit_at_10: 0.9
      recall_at_100: 0.943231441
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.943231441
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.897209781
      hit_at_10: 0.945
      recall_at_100: 0.9170305677
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9170305677
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8395603435
      hit_at_10: 0.925
      recall_at_100: 0.9825327511
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.005
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9825327511
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
