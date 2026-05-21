# MNanoBEIR / NanoBEIR-it / NanoSCIDOCS

## Overview

SCIDOCS is a scientific-document retrieval benchmark. `NanoBEIR-it__NanoSCIDOCS`
uses Italian translated paper titles or scientific queries to retrieve Italian
translated paper abstracts or document descriptions.

## Details

### What the Original Data Measures

[SPECTER](https://arxiv.org/abs/2004.07180) introduced scientific document
representations and the SCIDOCS evaluation suite. BEIR includes SCIDOCS as a
scientific retrieval task, and MMTEB provides multilingual context.

### Observed Data Profile

The sampled task has 50 queries, 2,210 documents, and 244 positive qrels. Every
query has multiple positives, usually five. Queries average 89.52 characters,
and documents average 1,062.02 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.2867 and hit@10 = 0.7200. Scientific vocabulary helps
lexical matching, but cross-paper relatedness often requires semantic and
disciplinary context.

### Training Data That May Help

Useful data includes non-overlapping citation recommendation, related-paper
retrieval, scientific abstract retrieval, and Italian or multilingual scholarly
text pairs. Exclude SCIDOCS, SPECTER evaluation data, BEIR, and NanoBEIR.

### Synthetic Data Guidance

Generate Italian paper-title or abstract queries from non-evaluation scholarly
abstracts. Hard negatives should be in the same research area but not the same
method, dataset, or claim.

## Example Data

| Query | Positive document |
| --- | --- |
| Convertitore Elevatore CC-CC a Più Livelli Innovativo (53 chars) | I convertitori di tensione a sorgente multlivello stanno emergendo come una nuova categoria di opzioni di convertitori di potenza per applicazioni ad alta potenza. I convertitori di tensione a sorgente multlivello solitamente ... [truncated 225 chars](1122 chars) |
| Apprendimento di Campi Markoviani Gaussiani Sparsi Veloci Basato sulla Fattorizzazione di Cholesky (98 chars) | Sure, please provide the English document text that you need translated into Italian. (85 chars) |
| Sintesi delle Texture Utilizzando Reti Neurali Convoluzionali (61 chars) | In questo lavoro indaghiamo l'effetto della profondità della rete convoluzionale sulla sua accuratezza nel contesto del riconoscimento delle immagini su larga scala. Il nostro principale contributo è una valutazione approfond ... [truncated 225 chars](988 chars) |
| Antenna ad anello anulare planare a banda larga con polarizzazione circolare per sistema RFID (93 chars) | In questo articolo, viene proposta una tecnica di alimentazione a striscia meandrante orizzontale (HMS) per ottenere un buon adattamento di impedenza e schemi di radiazione simmetrici frontali per un'antenna a patch impilata ... [truncated 225 chars](1481 chars) |
| Progettazione di un monitor digitale avanzato del battito cardiaco utilizzando componenti elettronici di base (109 chars) | In questo articolo, abbiamo presentato il design e lo sviluppo di un nuovo dispositivo integrato per misurare la frequenza cardiaca utilizzando la punta del dito, al fine di migliorare la stima della frequenza cardiaca. Poich ... [truncated 225 chars](1397 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-it |
| Task / split | NanoSCIDOCS |
| Hugging Face dataset | [hakari-bench/NanoBEIR-it](https://huggingface.co/datasets/hakari-bench/NanoBEIR-it) |
| Language | it |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,210 |
| Positive qrels | 244 |
| Avg positives / query | 4.88 |
| Positives per query (min / median / max) | 3 / 5.00 / 5 |
| Queries with multiple positives | 50 (100.0%) |
| BM25 nDCG@10 | 0.2867 |
| BM25 hit@10 | 0.7200 |
| Query length avg chars | 89.52 |
| Document length avg chars | 1,062.02 |

### Public Sources

- [SPECTER: Document-level Representation Learning using Citation-informed Transformers](https://arxiv.org/abs/2004.07180).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-it](https://huggingface.co/datasets/hakari-bench/NanoBEIR-it)
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
  backing_dataset: NanoBEIR-it
  dataset_id: hakari-bench/NanoBEIR-it
  task_name: NanoSCIDOCS
  split_name: NanoSCIDOCS
  language: it
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-it__NanoSCIDOCS.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 2210
    positive_qrels: 244
  positives_per_query:
    average: 4.88
    min: 3
    median: 5.0
    max: 5
    multi_positive_queries: 50
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 89.52
    document_mean: 1062.021719
  bm25:
    ndcg_at_10: 0.2866801578
    hit_at_10: 0.72
    source: dataset_bm25_column
```
