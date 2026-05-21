# MNanoBEIR / NanoBEIR-sr / NanoSCIDOCS

## Overview

SCIDOCS is a scientific-document retrieval benchmark. `NanoBEIR-sr__NanoSCIDOCS`
uses Serbian translated paper titles or descriptions to retrieve Serbian
translated scientific abstracts.

## Details

### What the Original Data Measures

[SPECTER](https://arxiv.org/abs/2004.07180) introduced citation-informed
scientific document embeddings and evaluated on SCIDOCS. BEIR includes SCIDOCS
as scientific retrieval, and MMTEB provides the multilingual context.

### Observed Data Profile

The sampled task has 50 queries, 2,210 documents, and 244 positive qrels. Every
query is multi-positive, usually with 3 to 5 positives. Queries average 77.12
characters, and documents average 944.48 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.2561 and hit@10 = 0.7600. The median first-positive
rank is 3.0, so lexical scientific terms help, but full relevant-set ranking is
harder than finding one related paper.

### Training Data That May Help

Helpful data includes non-overlapping scientific-paper retrieval, citation and
co-citation ranking, Serbian scientific abstracts, and multilingual academic
search data. Exclude SCIDOCS, SPECTER evaluation records, BEIR, and NanoBEIR.

### Synthetic Data Guidance

Generate Serbian paper-title queries from scientific abstracts. Hard negatives
should come from the same field but describe a different contribution.

## Example Data

| Query | Positive document |
| --- | --- |
| Novi DC-DC višestepeni pojačavački pretvarač (44 chars) | Apstrakt Višenaponski pretvarači sa više nivoa postaju nova vrsta opcija za pretvarače snage u primenama velike snage. Višenaponski pretvarači tipično sintetizuju stepenasti naponski talas iz nekoliko nivoa napona istosmernih ... [truncated 225 chars](872 chars) |
| Brzo Učenje Retkih Gaussovih Markovljevih Slučajnih Polja Bazirano na Čoleskijevoj Faktorizaciji (96 chars) | Poštovani korisniče, Zahvaljujem vam se što ste me kontaktirali. Kao veštačka inteligencija, moja osnovna svrha je pružanje informacija i pomoći u različitim oblastima. Nažalost, trenutno nemam pristup spoljnim bazama podatak ... [truncated 225 chars](687 chars) |
| Sinteza teksture korišćenjem konvolucionih neuronskih mreža (59 chars) | U ovom radu istražujemo uticaj dubine konvolucione mreže na njenu tačnost u okruženju za prepoznavanje slika velikih razmera. Naš glavni doprinos je temeljna evaluacija mreža sve veće dubine, koja pokazuje da se značajno pobo ... [truncated 225 chars](819 chars) |
| Planarna širokopojasna prstenasta antena sa kružnom polarizacijom za RFID sistem (80 chars) | U ovom radu predlaže se tehnika horizontalno meandrirajuće trake (HMS) kako bi se postiglo dobro prilagođavanje impedanse i simetrični širokousmereni zračni obrasci za širokopojasnu kružno polarizovanu složenu patch antenu sa ... [truncated 225 chars](1219 chars) |
| Dizajn naprednog digitalnog monitora srčanog ritma korišćenjem osnovnih elektronskih komponenti (95 chars) | U ovom radu, predstavili smo dizajn i razvoj novog integrisanog uređaja za merenje srčanog ritma pomoću vrha prsta kako bi se poboljšalo procenjivanje otkucaja srca. Kako se srčane bolesti svakodnevno povećavaju, potreba za p ... [truncated 225 chars](1110 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-sr |
| Task / split | NanoSCIDOCS |
| Hugging Face dataset | [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr) |
| Language | sr |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,210 |
| Positive qrels | 244 |
| Positives per query avg | 4.88 |
| Positives per query min / median / max | 3 / 5.0 / 5 |
| Multi-positive queries | 50 (100.00%) |
| BM25 nDCG@10 | 0.2561 |
| BM25 hit@10 | 0.7600 |
| Query length avg chars | 77.12 |
| Document length avg chars | 944.48 |

### Public Sources

- [SPECTER](https://arxiv.org/abs/2004.07180), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SPECTER: Document-level Representation Learning using Citation-informed Transformers | 2020 | task paper | https://arxiv.org/abs/2004.07180 |
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
  task_name: NanoSCIDOCS
  split_name: NanoSCIDOCS
  language: sr
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sr__NanoSCIDOCS.md
  source_research: {primary_source_type: task_paper, paper_pdf_or_html_checked: true, no_paper_note: null}
  counts: {queries: 50, documents: 2210, positive_qrels: 244}
  positives_per_query: {average: 4.88, min: 3, median: 5.0, max: 5, multi_positive_queries: 50, multi_positive_query_percent: 100.0}
  text_stats_chars: {query_mean: 77.12, document_mean: 944.478281}
  bm25: {ndcg_at_10: 0.2561117162, hit_at_10: 0.76, source: dataset_bm25_column}
```
