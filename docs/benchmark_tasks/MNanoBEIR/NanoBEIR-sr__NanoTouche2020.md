# MNanoBEIR / NanoBEIR-sr / NanoTouche2020

## Overview

Touché 2020 is an argument retrieval task for controversial questions.
`NanoBEIR-sr__NanoTouche2020` uses Serbian translated debate questions to
retrieve Serbian translated argument passages.

## Details

### What the Original Data Measures

[Touché 2020](https://doi.org/10.1007/978-3-030-58219-7_26) evaluates argument
retrieval for controversial information needs. BEIR includes it as argument
retrieval, and MMTEB provides the multilingual context.

### Observed Data Profile

The sampled task has 49 queries, 5,745 documents, and 932 positive qrels. Every
query is multi-positive, averaging 19.02 positives. Queries average 55.06
characters, while documents average 2,095.78 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.4741 and hit@10 = 1.0000. The median first-positive
rank is 1.0, so BM25 finds at least one argument for every query, but ranking
the broad positive set remains the main challenge.

### Training Data That May Help

Useful data includes non-overlapping argument retrieval, debate passages,
stance-aware ranking, and Serbian controversial-question retrieval. Exclude
Touché, BEIR, NanoBEIR, and translated evaluation arguments.

### Synthetic Data Guidance

Generate Serbian controversial questions with multiple relevant pro and con
arguments. Hard negatives should discuss the same debate topic but not the
specific stance or aspect requested by the query.

## Example Data

| Query | Positive document |
| --- | --- |
| Da li je domaći zadatak koristan? (33 chars) | Prvo, postoje tri argumenta zašto je domaći zadatak odličan i trebalo bi da se nastavi u modernim školama. 1. Domaći zadatak pomaže učenicima koji uče kroz praksu. Opšte je prihvaćeno da postoje tri tipa učenika: oni koji uče ... [truncated 225 chars](3651 chars) |
| Treba li se reklamni lekovi na recept direktno usmeravati potrošačima? (70 chars) | Mnogi oglasi ne sadrže dovoljno informacija o tome koliko lekovi delotvorno deluju. Na primer, Lunesta se reklamira leptirkom koji lebdi kroz prozor spavaće sobe, iznad osobe koja mirno spava. Zapravo, Lunesta pomaže pacijent ... [truncated 225 chars](1697 chars) |
| Da li bi neke vakcine trebalo da budu obavezne za decu? (55 chars) | Još uvek nije u potpunosti razrađeno... Samo nekoliko manjih stavki koje sam sastavio... Vlade ne bi trebalo da imaju pravo da se mešaju u zdravstvene odluke koje roditelji donose za svoju decu. Prema istraživanju Univerzitet ... [truncated 225 chars](4370 chars) |
| Da li abortus treba da bude legalan? (36 chars) | Pobačaji bi trebalo da budu legalni jer ličnost počinje nakon što fetus postane sposoban za život ili nakon rođenja, a ne u trenutku začeća. Prema stavu Vrhovnog suda SAD, osoba dobija svoje godine kada izađe iz majčine utrob ... [truncated 225 chars](325 chars) |
| Da li standardizovani testovi poboljšavaju obrazovanje? (55 chars) | Rezolucija: SAT, ACT i drugi standardizovani testovi pružaju bolji uvid u spremnost srednjoškolca za obrazovanje na elitnim koledžima i univerzitetima nego srednjoškolski prosek ocena i stoga bi trebalo da imaju veću ulogu u ... [truncated 225 chars](4097 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-sr |
| Task / split | NanoTouche2020 |
| Hugging Face dataset | [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr) |
| Language | sr |
| Category | natural_language |
| Queries | 49 |
| Documents | 5,745 |
| Positive qrels | 932 |
| Positives per query avg | 19.02 |
| Positives per query min / median / max | 6 / 19.0 / 32 |
| Multi-positive queries | 49 (100.00%) |
| BM25 nDCG@10 | 0.4741 |
| BM25 hit@10 | 1.0000 |
| BM25 Recall@100 | 0.6695 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4605 |
| Dense hit@10 | 0.9796 |
| Dense Recall@100 | 0.8004 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.5246 |
| Reranking hybrid hit@10 | 0.9796 |
| Reranking hybrid Recall@100 | 0.7650 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 55.06 |
| Document length avg chars | 2,095.78 |

### Public Sources

- [Touché 2020](https://doi.org/10.1007/978-3-030-58219-7_26), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of Touché 2020: Argument Retrieval | 2020 | task paper | https://doi.org/10.1007/978-3-030-58219-7_26 |
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
  backing_dataset: NanoBEIR-sr
  dataset_id: hakari-bench/NanoBEIR-sr
  task_name: NanoTouche2020
  split_name: NanoTouche2020
  language: sr
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sr__NanoTouche2020.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 49
    documents: 5745
    positive_qrels: 932
  positives_per_query:
    average: 19.020408
    min: 6
    median: 19.0
    max: 32
    multi_positive_queries: 49
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 55.061224
    document_mean: 2095.780679
  bm25:
    ndcg_at_10: 0.4741065989465407
    hit_at_10: 1.0
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4741065989
      hit_at_10: 1.0
      recall_at_100: 0.669527897
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 49
      query_coverage: 1.0
      relevant_coverage_at_100: 0.669527897
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4605213069
      hit_at_10: 0.9795918367
      recall_at_100: 0.8004291845
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 49
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8004291845
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.5246091018
      hit_at_10: 0.9795918367
      recall_at_100: 0.7650214592
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 49
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7650214592
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
