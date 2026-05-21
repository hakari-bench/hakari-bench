# MNanoBEIR / NanoBEIR-sv / NanoTouche2020

## Overview

Touché 2020 is argument retrieval for controversial questions.
`NanoBEIR-sv__NanoTouche2020` uses Swedish translated debate questions to
retrieve Swedish translated argument passages.

## Details

### What the Original Data Measures

[Touché 2020](https://doi.org/10.1007/978-3-030-58219-7_26) evaluates argument
retrieval for controversial information needs. BEIR includes it as argument
retrieval, and MMTEB provides multilingual context.

### Observed Data Profile

The task has 49 queries, 5,745 documents, and 932 positive qrels. Every query
has multiple positives, averaging 19.02. Queries average 40.96 characters, and
documents average 2,158.81 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.4296 and hit@10 = 0.9592. The median first-positive
rank is 1.0, so hit rate is high, but ordering many relevant arguments remains
hard.

### Training Data That May Help

Use non-overlapping debate retrieval, Swedish argument passages, stance-aware
ranking, and controversial-question retrieval. Exclude Touché, BEIR, NanoBEIR,
and translated evaluation arguments.

### Synthetic Data Guidance

Generate Swedish controversial questions with multiple pro and con arguments.
Hard negatives should share the topic but not answer the specific aspect.

## Example Data

| Query | Positive document |
| --- | --- |
| Är läxor bra? (13 chars) | Först och främst finns det tre argument för varför läxor är utmärkta och bör fortsätta i moderna skolor. 1. Läxor hjälper gör-lärarna. Det är allmänt accepterat att det finns tre typer av lärande: de som lär sig genom att hör ... [truncated 225 chars](3658 chars) |
| Bör receptbelagda läkemedel annonseras direkt till konsumenter? (63 chars) | Många annonser innehåller inte tillräckligt med information om hur väl läkemedel fungerar. Till exempel annonseras Lunesta av en fjäril som flyger in genom ett sovrumsfönster, över en person som sover lugnt. Faktum är att Lun ... [truncated 225 chars](1768 chars) |
| Skall barn behöva några vacciner? (33 chars) | Det är inte ett fullständigt fall ännu... bara några små punkter jag samlat ihop... Regeringar bör inte ha rätt att ingripa i de hälsoval som föräldrar gör för sina barn. Enligt en undersökning från 2010 genomförd av Universi ... [truncated 225 chars](4244 chars) |
| Bör abort vara lagligt? (23 chars) | Abort ska vara lagligt eftersom personlighet börjar när fostret är livskraftigt eller efter födseln, inte vid befruktningen. Enligt USA:s högsta domstol får en person sin ålder när de är utanför moderns livmoder och andas syr ... [truncated 225 chars](286 chars) |
| Förbättrar standardiserade prov utbildningen? (45 chars) | Löst: SAT, ACT och andra standardiserade tester ger mer insikt i en gymnasieelevers beredskap för utbildning på elituniversitet och högskolor än gymnasiebetyget och bör därför spela en större roll i antagningsprocessen. För a ... [truncated 225 chars](4148 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-sv |
| Task / split | NanoTouche2020 |
| Hugging Face dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |
| Language | sv |
| Category | natural_language |
| Queries | 49 |
| Documents | 5,745 |
| Positive qrels | 932 |
| Positives per query avg | 19.02 |
| Positives per query min / median / max | 6 / 19.0 / 32 |
| Multi-positive queries | 49 (100.00%) |
| BM25 nDCG@10 | 0.4296 |
| BM25 hit@10 | 0.9592 |
| Query length avg chars | 40.96 |
| Document length avg chars | 2,158.81 |

### Public Sources

- [Touché 2020](https://doi.org/10.1007/978-3-030-58219-7_26), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv)
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
  backing_dataset: NanoBEIR-sv
  dataset_id: hakari-bench/NanoBEIR-sv
  task_name: NanoTouche2020
  split_name: NanoTouche2020
  language: sv
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoTouche2020.md
  source_research: {primary_source_type: task_paper, paper_pdf_or_html_checked: true, no_paper_note: null}
  counts: {queries: 49, documents: 5745, positive_qrels: 932}
  positives_per_query: {average: 19.020408, min: 6, median: 19.0, max: 32, multi_positive_queries: 49, multi_positive_query_percent: 100.0}
  text_stats_chars: {query_mean: 40.959184, document_mean: 2158.807137}
  bm25: {ndcg_at_10: 0.4296395191, hit_at_10: 0.9591836735, source: dataset_bm25_column}
```
