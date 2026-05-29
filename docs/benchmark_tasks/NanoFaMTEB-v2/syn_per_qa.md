# NanoFaMTEB-v2 / syn_per_qa

## Overview

`syn_per_qa` is a synthetic Persian QA retrieval task. Queries are Persian
questions, and documents are answer passages generated or curated for the
synthetic QA setting.

## Details

### What the Original Data Measures

[FaMTEB](https://arxiv.org/abs/2502.11571) states that many new Persian datasets
were generated with LLMs, including synthetic datasets for retrieval and RAG
systems. This split uses `MCINext/synthetic-persian-qa-retrieval`. [MTEB](https://arxiv.org/abs/2210.07316)
provides the retrieval benchmark framework.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 200 positive qrels. Queries
average 59.81 characters and documents average 306.22 characters. Every query
has one positive.

Observed examples cover general facts, history, and explanatory questions. The
positive passages are concise Persian answers.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.8609
and hit@10 = 0.9400. It ranks 156 positives first.

The synthetic QA format produces strong lexical overlap between question and
answer, making BM25 a high baseline.

### Training Data That May Help

Helpful data includes Persian QA pairs, synthetic QA retrieval, and RAG passage
matching. Exclude evaluation questions and answer passages.

### Synthetic Data Guidance

Generate diverse Persian questions and answer passages with explicit grounding.
Hard negatives should answer related but distinct questions.

## Example Data

| Query | Positive document |
| --- | --- |
| آیا بینگ راسل در فیلم‌های معروفی مانند 'دود اسلحه' نقش داشته است؟ (65 chars) | بله، بینگ راسل در مجموعه تلویزیونی 'دود اسلحه' که از سال ۱۹۵۶ تا ۱۹۷۴ پخش می‌شد، نقش Ed Shelby را ایفا کرد. این مجموعه یکی از محبوب‌ترین و شناخته‌شده‌ترین سریال‌های وسترن در تاریخ تلویزیون است. (193 chars) |
| کتاب تحقیق در عملیات پیشرفته در چه انتشاراتی منتشر شده است؟ (59 chars) | این کتاب توسط انتشارات دانشگاه شهید بهشتی منتشر شده است. این انتشارات به عنوان یکی از مراکز معتبر در نشر آثار علمی و پژوهشی در ایران شناخته می‌شود. (147 chars) |
| آیا این آیه در مکه نازل شده است؟ (32 chars) | نه، این آیه در مدینه بر پیامبر اسلام صلی الله علیه و آله نازل گردیده است. (73 chars) |
| چگونه می‌توان نسخه چاپی کتاب رباعیات شیخ شیراز سعدی را تهیه کرد؟ (64 chars) | نسخه چاپی این کتاب را می‌توانید از طاقچه سفارش دهید. طاقچه یک پلتفرم آنلاین برای خرید کتاب است که امکان دسترسی به کتاب‌های مختلف را برای کاربران فراهم می‌کند. (158 chars) |
| چرا مصر همواره در کانون توجه ایرانیان قرار داشته است؟ (53 chars) | مصر به دلایل مختلفی همواره در کانون توجه ایرانیان قرار داشته است. این توجه نه تنها به لحاظ تمدنی و فرهنگی بلکه به دلیل جایگاه مهمی که هر دو کشور در خاورمیانه دارند، شکل گرفته است. همچنین اشتراکات اسلامی و علاقه به اهل بیت علی ... [truncated 225 chars](266 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoFaMTEB-v2 |
| Backing dataset | NanoFaMTEB-v2 |
| Task / split | syn_per_qa |
| Hugging Face dataset | [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) |
| Language | fa |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.8609 |
| BM25 hit@10 | 0.9400 |
| BM25 Recall@100 | 0.9900 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.9204 |
| Dense hit@10 | 0.9600 |
| Dense Recall@100 | 0.9750 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.9173 |
| Reranking hybrid hit@10 | 0.9550 |
| Reranking hybrid Recall@100 | 0.9950 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 59.81 |
| Document length avg chars | 306.22 |

### Public Sources

- [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316).
- [MCINext/synthetic-persian-qa-retrieval dataset card](https://huggingface.co/datasets/MCINext/synthetic-persian-qa-retrieval).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2)
- Source dataset: [MCINext/synthetic-persian-qa-retrieval](https://huggingface.co/datasets/MCINext/synthetic-persian-qa-retrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FaMTEB: Massive Text Embedding Benchmark in Persian Language | 2025 | arXiv paper | https://arxiv.org/abs/2502.11571 |
| MTEB: Massive Text Embedding Benchmark | 2023 | arXiv paper | https://arxiv.org/abs/2210.07316 |
| MCINext/synthetic-persian-qa-retrieval | 2025 | dataset card | https://huggingface.co/datasets/MCINext/synthetic-persian-qa-retrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoFaMTEB-v2
  backing_dataset: NanoFaMTEB-v2
  dataset_id: hakari-bench/NanoFaMTEB-v2
  task_name: syn_per_qa
  split_name: syn_per_qa
  language: fa
  category: natural_language
  document_path: docs/benchmark_tasks/NanoFaMTEB-v2/syn_per_qa.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
  text_stats_chars:
    query_mean: 59.81
    document_mean: 306.2192
  bm25:
    ndcg_at_10: 0.860901094377185
    hit_at_10: 0.94
    source: dataset_candidate_subset
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2
    source_urls:
    - label: FaMTEB arXiv
      url: https://arxiv.org/abs/2502.11571
    - label: MCINext/synthetic-persian-qa-retrieval
      url: https://huggingface.co/datasets/MCINext/synthetic-persian-qa-retrieval
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
      ndcg_at_10: 0.8609010944
      hit_at_10: 0.94
      recall_at_100: 0.99
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.99
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.9203869088
      hit_at_10: 0.96
      recall_at_100: 0.975
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.975
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.9173240657
      hit_at_10: 0.955
      recall_at_100: 0.995
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.005
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.995
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
