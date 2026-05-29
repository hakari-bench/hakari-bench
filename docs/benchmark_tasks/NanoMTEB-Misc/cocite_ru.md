# NanoMTEB-Misc / cocite_ru

## Overview

`NanoMTEB-Misc / cocite_ru` is the Russian co-citation retrieval task from
RuSciBench. A Russian scientific paper title and abstract retrieve abstracts of
papers that are co-cited with it.

## Details

### What the Original Data Measures

[RuSciBench: Open Benchmark for Russian and English Scientific Document
Representations](https://doi.org/10.1134/S1064562424602191) presents
RuSciBench as a benchmark for Russian and English scientific document
representations based on eLibrary.ru. The paper defines the co-citation task as
retrieving papers co-cited with the query paper, specifically papers cited by at
least five common papers in the source citation graph.

This split measures a looser bibliographic relation than direct citation.
Relevant documents may be scientifically related without sharing exact phrases
or without one paper citing the other.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 1,000 positive qrel rows.
Each query has five positive co-citation targets. Queries average 961.80
characters and documents average 908.88 characters. The samples cover biology,
medicine, ecology, statistics, and economics, with long title-plus-abstract
fields.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.3593 and hit@10 = 0.7150. It ranks 92 positives at rank 1 and finds a
positive in the top 10 for 143 queries.

BM25 is weaker here than on direct citation because co-citation can link papers
through community usage rather than explicit lexical overlap. It still works
when papers share narrow scientific terminology, but it misses relations where
the query and positive abstracts are adjacent in a research area rather than
near duplicates.

### Training Data That May Help

Citation-network representation learning, Russian scientific abstract
retrieval, co-citation pair mining, and SPECTER-style objectives are useful.
Hard negatives should include same-domain papers that are not co-cited, because
general topical similarity is not sufficient.

### Synthetic Data Guidance

Use real or simulated citation graphs to create positives, then generate
query-positive pairs from paper abstracts. Include negatives from the same
topic, method, and journal class. Avoid treating arbitrary same-topic abstracts
as positives unless a co-citation relation is known.

## Example Data

| Query | Positive document |
| --- | --- |
| Трансформация промышленности в цифровой экономике: проблемы и перспективы В статье проведен анализ актуального состояния цифровизации российской промышленности, рассмотрены проблемы и выявлены перспективы трансформации промыш ... [truncated 225 chars](1319 chars) | Soft power: опыт Российской Федерации через призму международных отношений В статье рассматриваются аспекты использования «мягкой силы» в процессе формирования межнациональных связей. Особое внимание уделяется позиции России ... [truncated 225 chars](652 chars) |
| КОЛЕБАНИЯ ДОННОГО ДАВЛЕНИЯ Дан обзор экспериментальных исследований низкочастотных колебаний, которые могут возникать при сверхзвуковом обтекании донной области. Приведены работы, в которых низкочастотные колебания впервые бы ... [truncated 225 chars](619 chars) | Об исследовании колебательного движения газового подвеса ротора турбохолодильных и детандерных машин. Часть II. Колебания давления в соплах питающей системы на сверхкритическом режиме работы Рассмотрен колебательный режим, во ... [truncated 225 chars](634 chars) |
| ЭФФЕКТИВНОСТЬ БЮДЖЕТНОГО ФИНАНСИРОВАНИЯ СЕЛЬСКОГО ХОЗЯЙСТВА НА РЕГИОНАЛЬНОМ УРОВНЕ Дана оценка эффективности финансирования сельскохозяйственного производства в Новосибирской области, определены его объемы, обеспечивающие рас ... [truncated 225 chars](250 chars) | ПЛЕМЕННАЯ РАБОТА В МОЛОЧНОМ СКОТОВОДСТВЕ Рассматривается проблема улучшения генетического потенциала в молочном скотоводстве на современном этапе развития АПК. Приводятся основные причины, сдерживающие наращивание производств ... [truncated 225 chars](713 chars) |
| ЭКОНОМИЧЕСКИЕ ПРОБЛЕМЫ НАУЧНО-ТЕХНИЧЕСКОГО ПРОГРЕССА В ИССЛЕДОВАНИЯХ ИНСТИТУТА ЭКОНОМИКИ РАН В статье дан ретроспективный анализ экономических проблем научно-технического прогресса и инновационной экономики, представленных в ... [truncated 225 chars](894 chars) | Уголовное правоприменение в контексте процедуры банкротства В статье кратко рассмотрены составы банкротных преступлений, а также основные причины неприменения норм об ответственности за данные деяния. Проанализированы существ ... [truncated 225 chars](495 chars) |
| Опытно-промышленная эксплуатация многозвенных автопоездов SCANIA в Удачнинском ГОКе В настоящее время в АК «АЛРОСА» (ОАО) для увеличения минерально-сырьевой базы, прорабатывается вопрос о разработке удаленных беднотоварных ме ... [truncated 225 chars](425 chars) | ПРОБЛЕМЫ ВНЕДРЕНИЯ МОДУЛЬНЫХ БОЛЬШЕГРУЗНЫХ АВТОПОЕЗДОВ В целях повышения эффективности автоперевозок, сокращения расхода топлива и токсичности отработавших газов предложены рекомендации по обеспечению безопасности и скорейшем ... [truncated 225 chars](330 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Misc |
| Backing dataset | NanoMTEB-Misc |
| Task / split | cocite_ru |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Misc](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Misc) |
| Source dataset | [mlsa-iai-msu-lab/ru_sci_bench_cocite_retrieval](https://huggingface.co/datasets/mlsa-iai-msu-lab/ru_sci_bench_cocite_retrieval) |
| Language | ru |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 1,000 |
| Positives per query | avg 5.00 / min 5 / median 5 / max 5 |
| Multi-positive queries | 200 |
| BM25 nDCG@10 | 0.3920 |
| BM25 hit@10 | 0.7300 |
| BM25 Recall@100 | 0.5960 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4249 |
| Dense hit@10 | 0.7550 |
| Dense Recall@100 | 0.6620 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4346 |
| Reranking hybrid hit@10 | 0.7550 |
| Reranking hybrid Recall@100 | 0.6810 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 18 |
| Query length avg chars | 961.80 |
| Document length avg chars | 908.88 |

### Public Sources

- [RuSciBench: Open Benchmark for Russian and English Scientific Document Representations](https://doi.org/10.1134/S1064562424602191), Doklady Mathematics 2024.
- [RuSciBench co-citation dataset card](https://huggingface.co/datasets/mlsa-iai-msu-lab/ru_sci_bench_cocite_retrieval), task and source-data description.
- [RuSciBench code repository](https://github.com/mlsa-iai-msu-lab/ru_sci_bench_mteb), benchmark implementation.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Misc](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Misc)
- Source task dataset: [mlsa-iai-msu-lab/ru_sci_bench_cocite_retrieval](https://huggingface.co/datasets/mlsa-iai-msu-lab/ru_sci_bench_cocite_retrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RuSciBench: Open Benchmark for Russian and English Scientific Document Representations | 2024 | benchmark paper | https://doi.org/10.1134/S1064562424602191 |
| mlsa-iai-msu-lab/ru_sci_bench_cocite_retrieval |  | dataset card | https://huggingface.co/datasets/mlsa-iai-msu-lab/ru_sci_bench_cocite_retrieval |
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
  task_name: cocite_ru
  split_name: cocite_ru
  language: ru
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Misc/cocite_ru.md
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
    query_mean: 961.8
    document_mean: 908.88
  bm25:
    ndcg_at_10: 0.3920323427330925
    hit_at_10: 0.73
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3920323427
      hit_at_10: 0.73
      recall_at_100: 0.596
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.596
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4249331349
      hit_at_10: 0.755
      recall_at_100: 0.662
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.662
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4346494972
      hit_at_10: 0.755
      recall_at_100: 0.681
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.09
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.681
      safeguard_positive_rows: 18
      rows_with_101_candidates: 18
```
