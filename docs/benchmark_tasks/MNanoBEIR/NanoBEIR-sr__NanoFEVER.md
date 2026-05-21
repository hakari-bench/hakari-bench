# MNanoBEIR / NanoBEIR-sr / NanoFEVER

## Overview

FEVER is a Wikipedia evidence retrieval task for factual claims.
`NanoBEIR-sr__NanoFEVER` uses Serbian translated claims and Wikipedia-style
evidence passages.

## Details

### What the Original Data Measures

[FEVER](https://arxiv.org/abs/1803.05355) was built for fact extraction and
verification over Wikipedia, where systems retrieve evidence for claims before
labeling them. BEIR evaluates the retrieval step, and MMTEB gives the
multilingual benchmark context.

### Observed Data Profile

The sampled task has 50 queries, 4,996 documents, and 57 positive qrels. Most
queries have one positive, with a small multi-positive tail. Queries average
46.14 characters, and documents average 1,184.60 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.6486 and hit@10 = 0.7800. The median first-positive
rank is 1.5, showing that named entities and claim terms help BM25, though some
Serbian translated claims still need semantic evidence matching.

### Training Data That May Help

Useful data includes non-overlapping claim-evidence retrieval, Serbian
Wikipedia evidence mining, and multilingual fact-checking. Exclude FEVER, BEIR,
NanoBEIR, and direct translations of evaluation claims or evidence pages.

### Synthetic Data Guidance

Generate short Serbian factual claims from non-evaluation encyclopedia
passages. Pair each claim with the passage that verifies or refutes it, and use
hard negatives from related entities or neighboring events.

## Example Data

| Query | Positive document |
| --- | --- |
| Kith Godčo je poznavao Grateful Dead. (37 chars) | Grateful Dead je bila američka rok grupa osnovana 1965. godine u Palo Altu u Kaliforniji. Sa sastavom koji je varirao od kvinteta do septeta, bend je poznat po svom jedinstvenom i eklektičnom stilu, koji je spajao elemente ro ... [truncated 225 chars](2888 chars) |
| "Taarak Mehta Ka Ooltah Chashmah" je sitkom. (44 chars) | "Taarak Mehta Ka Ooltah Chashmah" (na engleskom: "Taarak Mehta's Different Perspective") je najduže trajuća indijska sitkom serija koju proizvodi Neela Tele Films Private Limited. Serija je počela sa emitovanjem 28. jula 2008 ... [truncated 225 chars](590 chars) |
| Tajni i tehnološki napredni avioni proizvođeni su u Burbanku u Kaliforniji. (75 chars) | Burbank je grad u okrugu Los Anđeles u južnoj Kaliforniji, Sjedinjene Države, 19 km severozapadno od centra Los Anđelesa. Prema popisu iz 2010. godine, stanovništvo je iznosilo 103.340. Poznat kao "Medijska prestonica sveta" ... [truncated 225 chars](1321 chars) |
| Nero je osoba. (14 chars) | Termin Julijevsko-Klaudijevska dinastija odnosi se na prvih pet rimskih careva — Avgusta, Tiberija, Kaligulu, Klaudija i Nerona — ili na porodicu kojoj su pripadali. Oni su vladali Rimskim Carstvom od njegovog formiranja pod ... [truncated 225 chars](2025 chars) |
| "Scream 2" je isključivo nemački film. (38 chars) | Scream 2 je američki slasher film iz 1997. godine koji je režirao Wes Craven, a scenario napisao Kevin Williamson. U filmu glume David Arquette, Neve Campbell, Courteney Cox, Sarah Michelle Gellar, Jamie Kennedy, Laurie Metca ... [truncated 225 chars](2427 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-sr |
| Task / split | NanoFEVER |
| Hugging Face dataset | [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr) |
| Language | sr |
| Category | natural_language |
| Queries | 50 |
| Documents | 4,996 |
| Positive qrels | 57 |
| Positives per query avg | 1.14 |
| Positives per query min / median / max | 1 / 1.0 / 3 |
| Multi-positive queries | 6 (12.00%) |
| BM25 nDCG@10 | 0.6486 |
| BM25 hit@10 | 0.7800 |
| Query length avg chars | 46.14 |
| Document length avg chars | 1,184.60 |

### Public Sources

- [FEVER: a Large-scale Dataset for Fact Extraction and VERification](https://arxiv.org/abs/1803.05355).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FEVER: a Large-scale Dataset for Fact Extraction and VERification | 2018 | task paper | https://arxiv.org/abs/1803.05355 |
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
  task_name: NanoFEVER
  split_name: NanoFEVER
  language: sr
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sr__NanoFEVER.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 4996
    positive_qrels: 57
  positives_per_query:
    average: 1.14
    min: 1
    median: 1.0
    max: 3
    multi_positive_queries: 6
    multi_positive_query_percent: 12.0
  text_stats_chars:
    query_mean: 46.14
    document_mean: 1184.604283
  bm25:
    ndcg_at_10: 0.6485836944
    hit_at_10: 0.78
    source: dataset_bm25_column
```
