# NanoMTEB-Polish / pugg

## Overview

The PUGG paper builds Polish KBQA, machine-reading, and information-retrieval
data from natural Polish questions and Wikipedia-derived passages. This Nano
split is the IR view: each short Polish factoid question has one positive
passage containing the answer. The sampled questions involve definitions,
fictional characters, family relations in fiction, Polish borders, sports, and
popular culture, so the benchmark probes compact Polish encyclopedic retrieval
rather than translated English QA alone.

## Details

### What the Original Data Measures

[Developing PUGG for Polish: A Modern Approach to KBQA, MRC, and IR Dataset Construction](https://aclanthology.org/2024.findings-acl.652/)
introduces PUGG as a Polish dataset covering KBQA, MRC, and IR. The paper
reports that PUGG targets low-resource Polish QA, uses natural questions, and
constructs IR passages from relevant Wikipedia articles segmented into shorter
windows. This Nano task is the IR view of that Polish source data.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and exactly 200 positive qrels, so
each query has one positive. Queries are short, averaging 36.19 characters, and
documents average 850.31 characters. Examples include definitions, comic-book
characters, family relations in fiction, Poland's borders, and sports facts.

### BM25 Difficulty

BM25 is strong here, reaching nDCG@10 = 0.6390 and hit@10 = 0.7950. It ranks 98
positives first and 159 in the top 10. Short entity-rich questions often share
names or key nouns with the correct passage, so lexical retrieval is a strong
baseline, though semantic models still matter for paraphrased definitions and
implicit answer wording.

### Training Data That May Help

Useful data includes non-overlapping PUGG training records, Polish Wikipedia QA
retrieval pairs, Polish KBQA/MRC datasets, and hard negatives from related
Wikipedia entities. The exact evaluation questions and positive passages should
not be used in training.

### Synthetic Data Guidance

Generate Polish factoid questions from non-evaluation Wikipedia passages. The
positive document should explicitly contain the answer, and synthetic negatives
should be topically close but lack the answer. Keep questions short and natural,
matching the observed PUGG style.

## Example Data

| Query | Positive document |
| --- | --- |
| kto napisał balladyne? (22 chars) | Balladyna – dramat romantyczny w pięciu aktach, napisany przez Juliusza Słowackiego w Genewie w 1834 roku, a wydany w Paryżu w roku 1839. == Opis dramatu == Dramat miał być prawdopodobnie jedną z sześciu części planowanego pr ... [truncated 225 chars](867 chars) |
| co obiecano polakom w akcie 5 listopada? (40 chars) | 5 listopada 1916 w wyniku konferencji w Pszczynie władze niemieckie i austro-węgierskie wydały proklamację, z podpisami swych generalnych gubernatorów von Beselera i Kuka, zawierającą obietnicę powstania Królestwa Polskiego, ... [truncated 225 chars](964 chars) |
| jakie pouczenia wynikają z biblijnej opowieści o stworzeniu świata? (67 chars) | Stworzenie świata – pojęcie biblijne wyjaśniające naturę i sposób powstania wszechświata. W ujęciu judeo-chrześcijańskim zarówno niebo (materialne i duchowe), jak i ziemia i wszystko co istnieje jest dziełem Boga-Stwórcy. Wsz ... [truncated 225 chars](931 chars) |
| z kim zareczyl sie tadeusz? (27 chars) | Tadeusz Soplica ("pan Tadeusz") – postać literacka, tytułowy bohater poematu epickiego "Pan Tadeusz" (1834) Adama Mickiewicza; syn Jacka Soplicy, bratanek Sędziego, dziedzic Soplicowa. Młody, przystojny, zakochany w Zosi, wpl ... [truncated 225 chars](867 chars) |
| ile procent ludzi ma blond włosy? (33 chars) | Blond – kolor włosów, występujący u niektórych ssaków, wywołany przez niewielką ilość barwnika – melaniny. Zazwyczaj przez kolor ten rozumie się odcienie od jasnego brązu poprzez żółty aż do niemalże białego. Ocenia się, że w ... [truncated 225 chars](857 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Polish |
| Backing dataset | NanoMTEB-Polish |
| Task / split | pugg |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish) |
| Source dataset | [clarin-pl/PUGG_IR](https://huggingface.co/datasets/clarin-pl/PUGG_IR) |
| Language | pl |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.6390 |
| BM25 hit@10 | 0.7950 |
| BM25 Recall@100 | 0.8750 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7817 |
| Dense hit@10 | 0.8850 |
| Dense Recall@100 | 0.9300 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.7146 |
| Reranking hybrid hit@10 | 0.8300 |
| Reranking hybrid Recall@100 | 0.9800 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 4 |
| Query length avg chars | 36.19 |
| Document length avg chars | 850.31 |

### Public Sources

- [Developing PUGG for Polish: A Modern Approach to KBQA, MRC, and IR Dataset Construction](https://aclanthology.org/2024.findings-acl.652/), task paper.
- [clarin-pl/PUGG_IR](https://huggingface.co/datasets/clarin-pl/PUGG_IR), source dataset card.
- [PUGG GitHub repository](https://github.com/CLARIN-PL/PUGG), source implementation repository.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish)
- Source task dataset: [clarin-pl/PUGG_IR](https://huggingface.co/datasets/clarin-pl/PUGG_IR)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Developing PUGG for Polish: A Modern Approach to KBQA, MRC, and IR Dataset Construction | 2024 | task paper | https://aclanthology.org/2024.findings-acl.652/ |
| clarin-pl/PUGG_IR |  | dataset card | https://huggingface.co/datasets/clarin-pl/PUGG_IR |
| PUGG GitHub repository |  | repository | https://github.com/CLARIN-PL/PUGG |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Polish
  backing_dataset: NanoMTEB-Polish
  dataset_id: hakari-bench/NanoMTEB-Polish
  task_name: pugg
  split_name: pugg
  language: pl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Polish/pugg.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
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
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 36.19
    document_mean: 850.3113
  bm25:
    ndcg_at_10: 0.6389833559515614
    hit_at_10: 0.795
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.638983356
      hit_at_10: 0.795
      recall_at_100: 0.875
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.875
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7817220666
      hit_at_10: 0.885
      recall_at_100: 0.93
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.93
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.7146291925
      hit_at_10: 0.83
      recall_at_100: 0.98
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.02
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.98
      safeguard_positive_rows: 4
      rows_with_101_candidates: 4
```
