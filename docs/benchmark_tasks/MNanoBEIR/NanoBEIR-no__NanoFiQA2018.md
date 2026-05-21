# MNanoBEIR / NanoBEIR-no / NanoFiQA2018

## Overview

FiQA is a financial question-answer retrieval dataset. `NanoBEIR-no__NanoFiQA2018`
uses Norwegian translated personal-finance questions to retrieve Norwegian
translated answer passages.

## Details

### What the Original Data Measures

[FiQA 2018](https://doi.org/10.1145/3184558.3192301) was created for financial
opinion and question answering data. BEIR uses its retrieval version as a
finance-domain retrieval task, and MMTEB provides the multilingual benchmark
context for the Norwegian adaptation.

### Observed Data Profile

The sampled Norwegian task has 50 queries, 4,598 documents, and 123 positive
qrels. Queries average 64.68 characters and ask practical tax, investing, loan,
pricing, and contracting questions. Documents average 910.83 characters and are
forum-style financial answers.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.1955 and hit@10 = 0.4200. The median first-positive
rank is 21.5, making this one of the harder Norwegian lexical splits in this
batch. Strong models need financial-domain semantics and answer matching.

### Training Data That May Help

Useful data includes non-overlapping financial QA, Norwegian finance forum
retrieval, tax and investing question-answer pairs, and multilingual finance
retrieval data. Training should exclude FiQA, BEIR, NanoBEIR, and translated
answer passages likely to overlap.

### Synthetic Data Guidance

Generate Norwegian finance questions from non-evaluation answer passages,
keeping the question realistic and specific. Hard negatives should share
financial terms but answer a different decision or jurisdictional issue.

## Example Data

| Query | Positive document |
| --- | --- |
| Hvilken type avkastning gir Vanguard? (37 chars) | Fra Vanguards side - Dette virket som den enkleste siden S&P-data er lett å finne. Jeg bruker MoneyChimp for å bekrefte at Vanguards side tilbyr CAGR, ikke aritmetisk gjennomsnitt. Merk: Vanguard oppgir 'For amerikanske aksje ... [truncated 225 chars](381 chars) |
| Hva er skattekonsekvensene av å frilanse? (41 chars) | Hvis du har inntekt i USA, må du betale amerikansk inntektsskatt på det, med mindre det finnes en avtale mellom ditt land og USA som sier noe annet. (148 chars) |
| Hva betyr høy eller lav volum? (30 chars) | Den daglige volumet sammenlignes vanligvis med gjennomsnittlig daglig volum over de siste 50 dagene for en aksje. Høyt volum regnes vanligvis som 2 eller flere ganger gjennomsnittlig daglig volum over de siste 50 dagene for d ... [truncated 225 chars](730 chars) |
| Hvordan bruke kredittkortpoeng til å dekke skattefradragsberettigede bedriftsutgifter? (86 chars) | For enkelhets skyld, la oss starte med å se på kontanttilbakebetaling. Generelt sett er kontanttilbakebetaling fra kredittkort for personlig bruk ikke skattepliktig, men for bedriftsbruk er det skattepliktig (slags, jeg vil f ... [truncated 225 chars](3648 chars) |
| Hvordan skal jeg skatteføre meg når jeg er frilanser? (53 chars) | For skatteformål må du registrere deg både som ansatt (med T4-skjemaer og automatisk trekk i skatt) og som selvstendig næringsdrivende. Jeg var i samme situasjon selv i fjor. Ansatt og selvstendig næringsdrivende er en publik ... [truncated 225 chars](715 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-no |
| Task / split | NanoFiQA2018 |
| Hugging Face dataset | [hakari-bench/NanoBEIR-no](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no) |
| Language | no |
| Category | natural_language |
| Queries | 50 |
| Documents | 4,598 |
| Positive qrels | 123 |
| Avg positives / query | 2.46 |
| Positives per query (min / median / max) | 1 / 2.00 / 15 |
| Queries with multiple positives | 28 (56.0%) |
| BM25 nDCG@10 | 0.1955 |
| BM25 hit@10 | 0.4200 |
| Query length avg chars | 64.68 |
| Document length avg chars | 910.83 |

### Public Sources

- [FiQA 2018](https://doi.org/10.1145/3184558.3192301).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-no](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FiQA 2018 | 2018 | task paper | https://doi.org/10.1145/3184558.3192301 |
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
  backing_dataset: NanoBEIR-no
  dataset_id: hakari-bench/NanoBEIR-no
  task_name: NanoFiQA2018
  split_name: NanoFiQA2018
  language: "no"
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-no__NanoFiQA2018.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 4598
    positive_qrels: 123
  positives_per_query:
    average: 2.46
    min: 1
    median: 2.0
    max: 15
    multi_positive_queries: 28
    multi_positive_query_percent: 56.0
  text_stats_chars:
    query_mean: 64.68
    document_mean: 910.829491
  bm25:
    ndcg_at_10: 0.1954865692
    hit_at_10: 0.42
    source: dataset_bm25_column
```
