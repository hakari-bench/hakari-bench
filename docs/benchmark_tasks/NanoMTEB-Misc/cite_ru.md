# NanoMTEB-Misc / cite_ru

## Overview

`NanoMTEB-Misc / cite_ru` is the Russian direct-citation retrieval task from
RuSciBench. A Russian scientific paper title and abstract retrieve abstracts of
papers directly cited by that query paper.

## Details

### What the Original Data Measures

[RuSciBench: Open Benchmark for Russian and English Scientific Document
Representations](https://doi.org/10.1134/S1064562424602191) introduces
RuSciBench as a benchmark for scientific texts from eLibrary.ru and the Russian
Science Citation Index. Its retrieval section defines direct citation prediction
as retrieving papers directly cited by an anchor paper, using a retrieval setup
where all non-positive corpus documents are treated as negatives.

This split measures Russian scientific-document representation at the abstract
level. Relevance is not topical similarity alone: a relevant document is one of
the papers actually cited by the query paper.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 1,000 positive qrel rows.
Each query has exactly five positive citation targets. Queries are long,
averaging 1,399.06 characters, because they contain titles plus abstracts.
Documents average 926.86 characters.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.5081 and hit@10 = 0.8750. It ranks 131 queries at rank 1 and finds at least
one cited paper in the top 10 for 175 queries.

Lexical matching is strong for direct citations when the query and cited paper
share terminology, methodology, or domain-specific phrases. The harder cases
require recognizing citation relationships across broader scientific context
where abstracts use different wording.

### Training Data That May Help

Useful data includes non-overlapping Russian citation graphs, scientific title
and abstract pairs, SPECTER-style citation training, and Russian/English
scientific bilingual embeddings. Hard negatives should be topically close
papers from the same discipline that are not citation-linked.

### Synthetic Data Guidance

Synthetic data should start from real scientific abstracts and construct
citation-like positives only when a plausible bibliographic relation is known
or carefully simulated from cited-paper metadata. Generate hard negatives from
same-field abstracts with overlapping terminology. Avoid using generic topic
classification pairs as positives; citation retrieval is stricter than topical
similarity.

## Example Data

| Query | Positive document |
| --- | --- |
| Развитие геоинформационных компетенций у студентов, обучающихся по образовательной программе "История; География" по направлению подготовки 44.03.05 Педагогическое образование В данной статье приводятся основные принципы разр ... [truncated 225 chars](2647 chars) | Интеграция средств информационно-коммуникационных технологий в процессе подготовки студентов по профилю "Географическое образование" Настоящая статья посвящена одной из наиболее актуальных проблем современного профессионально ... [truncated 225 chars](1687 chars) |
| ОЦЕНКА СИСТЕМ УДОБРЕНИЯ ПРИ ВОЗДЕЛЫВАНИИ ОЗИМОЙ РЖИ В УСЛОВИЯХ РАДИОАКТИВНОГО ЗАГРЯЗНЕНИЯ ТЕРРИТОРИИ Представлены результаты длительного опыта по изучению совместного действия минеральных и органических удобрений на урожайнос ... [truncated 225 chars](902 chars) | ВЛИЯНИЕ ДЛИТЕЛЬНОГО ПРИМЕНЕНИЯ ОРГАНИЧЕСКИХ И МИНЕРАЛЬНЫХ УДОБРЕНИЙ И СИДЕРАТА НА УРОЖАЙНОСТЬ И КАЧЕСТВО ЗЕРНА ОЗИМОЙ РЖИ В условиях Брянской области при радиоактивном загрязнении получения стабильных и высоких урожаев озимой ... [truncated 225 chars](1260 chars) |
| Решение задачи горного давления с нелинейной функцией разупрочнения методом конечных разностей Приводится вариант решения задачи определения горного давления с учетом дилатансии для плоской, близкой к осесимметричной задачи. ... [truncated 225 chars](939 chars) | Физически нелинейно-пластическая задача о распределении напряжений вокруг выработки кругового очертания Выполнена постановка физически нелинейно-пластической задачи о распределении напряжений вокруг выработки кругового очерта ... [truncated 225 chars](951 chars) |
| Восприятие Японии в российском общественном сознании Япония долгое время оставалось страной, закрытой для России. По некоторым источникам, знакомство с её жителями началось в XVII в., а первую непосредственную информацию о бы ... [truncated 225 chars](2177 chars) | ЯПОНИЯ И ЯПОНЦЫ В ЗЕРКАЛЕ РУССКОЙ ФРАЗЕОЛОГИИ В статье рассматриваются русские фразеологизмы с этнонимом «японец» и его производными («японский городовой», «японский бог», «япона мама (мать)» и др.): их происхождение, значени ... [truncated 225 chars](348 chars) |
| МОДЕЛИРОВАНИЕ МЕХАНИЧЕСКИХ ХАРАКТЕРИСТИК МАСЛОНАПОЛНЕННЫХ КОМПОЗИТОВ Рассмотрены некоторые аспекты создания композитных материалов с модифицированной матрицей на основе ароматического полиамида фенилона марки ФС-2. Эффективны ... [truncated 225 chars](576 chars) | АНАЛИЗ ВЛИЯНИЯ НАПОЛНЕНИЯ КОМПОЗИТА МАСЛОМ НА СОСТОЯНИЕ ПОВЕРХНОСТИ МЕТАЛЛИЧЕСКОГО КОНТРТЕЛА Исследовано изменение топографии металлического контртела после трения с маслонаполненным композитным материалом. В качестве матрицы ... [truncated 225 chars](1074 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Misc |
| Backing dataset | NanoMTEB-Misc |
| Task / split | cite_ru |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Misc](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Misc) |
| Source dataset | [mlsa-iai-msu-lab/ru_sci_bench_cite_retrieval](https://huggingface.co/datasets/mlsa-iai-msu-lab/ru_sci_bench_cite_retrieval) |
| Language | ru |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 1,000 |
| Positives per query | avg 5.00 / min 5 / median 5 / max 5 |
| Multi-positive queries | 200 |
| BM25 nDCG@10 | 0.5081 |
| BM25 hit@10 | 0.8750 |
| Query length avg chars | 1,399.06 |
| Document length avg chars | 926.86 |

### Public Sources

- [RuSciBench: Open Benchmark for Russian and English Scientific Document Representations](https://doi.org/10.1134/S1064562424602191), Doklady Mathematics 2024.
- [RuSciBench dataset card](https://huggingface.co/datasets/mlsa-iai-msu-lab/ru_sci_bench_cite_retrieval), task and source-data description.
- [RuSciBench code repository](https://github.com/mlsa-iai-msu-lab/ru_sci_bench_mteb), benchmark implementation.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Misc](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Misc)
- Source task dataset: [mlsa-iai-msu-lab/ru_sci_bench_cite_retrieval](https://huggingface.co/datasets/mlsa-iai-msu-lab/ru_sci_bench_cite_retrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RuSciBench: Open Benchmark for Russian and English Scientific Document Representations | 2024 | benchmark paper | https://doi.org/10.1134/S1064562424602191 |
| mlsa-iai-msu-lab/ru_sci_bench_cite_retrieval |  | dataset card | https://huggingface.co/datasets/mlsa-iai-msu-lab/ru_sci_bench_cite_retrieval |
| ru_sci_bench_mteb |  | code repository | https://github.com/mlsa-iai-msu-lab/ru_sci_bench_mteb |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Misc
  backing_dataset: NanoMTEB-Misc
  dataset_id: hakari-bench/NanoMTEB-Misc
  task_name: cite_ru
  split_name: cite_ru
  language: ru
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Misc/cite_ru.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 1000
  positives_per_query:
    average: 5.0
    min: 5
    median: 5.0
    max: 5
    multi_positive_queries: 200
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 1399.06
    document_mean: 926.86
  bm25:
    ndcg_at_10: 0.5081
    hit_at_10: 0.875
    source: dataset_bm25_column
  example_count: 5
```
