# NanoMuPLeR / lt

## Overview

`NanoMuPLeR / lt` is the Lithuanian split of MuPLeR-retrieval. It evaluates
retrieval of Lithuanian EU legal passages from synthetic Lithuanian legal
questions. Each query has a single relevant DGT-Acquis-derived passage.

## Details

### What the Original Data Measures

The [MuPLeR-retrieval dataset card](https://huggingface.co/datasets/mteb/MuPLeR-retrieval)
describes a multilingual parallel legal retrieval dataset built from DGT-Acquis
passages and synthetic queries. [An overview of the European Union's highly multilingual parallel corpora](https://link.springer.com/article/10.1007/s10579-014-9277-0)
is the cited source reference for DGT-Acquis and related EU parallel corpora.

### Observed Data Profile

The split has 200 Lithuanian queries, 10,000 documents, and 200 single-positive
qrels. Queries average 143.04 characters and documents average 621.81
characters. The sample covers EU import taxation, state-aid compensation,
procurement criteria, nuclear-policy priorities, and pre-accession production
rules.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.8115 and hit@10 = 0.8750, with 148 positives at rank 1
and 175 in the top 10. The split has strong lexical cues through dates,
percentages, institutions, and legal terms, so BM25 is a high baseline.

### Training Data That May Help

Useful data includes non-overlapping Lithuanian EUR-Lex/DGT-Acquis retrieval
pairs, Lithuanian legal QA, and multilingual legal bitext with hard negatives
from related provisions. Avoid MuPLeR evaluation query-passage pairs.

### Synthetic Data Guidance

Generate Lithuanian questions from non-evaluation EU legal passages. Preserve
the exact condition, numeric threshold, and institutional context, and pair with
near negatives that are legally adjacent but answer a different point.

## Example Data

| Query | Positive document |
| --- | --- |
| Kada turėjo įsigalioti harmonizuotas minimalus €380 už 1 kubinį metrą akcizas gazoliui ir benzinui? (99 chars) | Šiuo pasiūlymu iš dalies keičiama Direktyva 2003/96/EB (EMD) dėl gazolio, naudojamo kaip degalai, apmokestinimo tvarkos, kuri taikoma visose Europos Sąjungos šalyse. Praktiškai šiuo pasiūlymu numatoma pamažu didinti minimalų ... [truncated 225 chars](535 chars) |
| Kuris mokestis už ES vidaus importą vis dar buvo taikomas septynių valstybių narių: dviem ≤0,5%, vienai 0,6%, keturioms 1%? (123 chars) | Dauguma ES 25 valstybių narių laikėsi Tarybos 1985 m. rekomendacijos ir visiškai panaikino mokestį; šiuo metu jį taiko tik septynios valstybės narės: Lenkija ir Portugalija taiko 0,5 proc. arba mažesnės normos mokestį, Kipras ... [truncated 225 chars](620 chars) |
| Kokia valdymo struktūra buvo siūloma trumpalaikiam visų narių metrologijos mokslinių tyrimų bandomajam projektui, kurio terminas būtų apribotas iki 2013 m.? (156 chars) | Apibendrinant, EESRK mano, kad būtų tikslingiau nuspręsti įgyvendinti bandomąjį Europos metrologijos mokslinių tyrimų (EMMT) projektą, kurio terminas būtų apribotas iki 2013 m., remiantis i MERA Plus, ir parengiamuosiuose pas ... [truncated 225 chars](743 chars) |
| Kiek laiko suinteresuotos šalys turi pranešti apie save po pranešimo paskelbimo, kad išsaugotų procedūrines teises ir pateiktų individualius reikalavimus? (154 chars) | Jei tyrimo metu atsižvelgiama į šalių prašymus (nusiskundimus), visos suinteresuotos šalys per 40 dienų nuo šio pranešimo paskelbimo Europos Sąjungos oficialiajame leidinyje, jei nenurodyta kitaip, turi pranešti apie save Kom ... [truncated 225 chars](595 chars) |
| Kuris ES organas pritarė Tarybos patvirtintam veiksmų planui sustiprinti įtariamųjų ir kaltinamųjų procesines teises ir jį įtraukė į Stokholmo programą? (152 chars) | Įtariamųjų ir kaltinamųjų baudžiamuosiuose procesuose teisių apsauga yra viena iš pagrindinių Sąjungos vertybių, kuri yra labai svarbi siekiant išlaikyti valstybių narių tarpusavio pasitikėjimą ir visuomenės pasitikėjimą Sąju ... [truncated 225 chars](556 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMuPLeR |
| Backing dataset | NanoMuPLeR |
| Task / split | lt |
| Hugging Face dataset | [hakari-bench/NanoMuPLeR](https://huggingface.co/datasets/hakari-bench/NanoMuPLeR) |
| Source dataset | [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval) |
| Language | lt |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.8115 |
| BM25 hit@10 | 0.8750 |
| BM25 Recall@100 | 0.9650 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7495 |
| Dense hit@10 | 0.8800 |
| Dense Recall@100 | 0.9300 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8442 |
| Reranking hybrid hit@10 | 0.9350 |
| Reranking hybrid Recall@100 | 0.9850 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 3 |
| Query length avg chars | 143.04 |
| Document length avg chars | 621.81 |

### Public Sources

- [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval), source dataset card.
- [An overview of the European Union's highly multilingual parallel corpora](https://link.springer.com/article/10.1007/s10579-014-9277-0), DGT-Acquis source reference paper.
- [DGT-Acquis](https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en), European Commission source-corpus page.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMuPLeR](https://huggingface.co/datasets/hakari-bench/NanoMuPLeR)
- Source task dataset: [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MuPLeR: Multilingual Parallel Legal Retrieval |  | dataset card | https://huggingface.co/datasets/mteb/MuPLeR-retrieval |
| An overview of the European Union's highly multilingual parallel corpora | 2014 | source paper | https://link.springer.com/article/10.1007/s10579-014-9277-0 |
| DGT-Acquis |  | source corpus | https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMuPLeR
  backing_dataset: NanoMuPLeR
  dataset_id: hakari-bench/NanoMuPLeR
  task_name: lt
  split_name: lt
  language: lt
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMuPLeR/lt.md
  source_research:
    primary_source_type: dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone MuPLeR technical paper was confirmed
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
    query_mean: 143.04
    document_mean: 621.81
  bm25:
    ndcg_at_10: 0.8115401687176116
    hit_at_10: 0.875
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8115401687
      hit_at_10: 0.875
      recall_at_100: 0.965
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.965
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7495275134
      hit_at_10: 0.88
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
      ndcg_at_10: 0.844159313
      hit_at_10: 0.935
      recall_at_100: 0.985
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.015
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.985
      safeguard_positive_rows: 3
      rows_with_101_candidates: 3
```
