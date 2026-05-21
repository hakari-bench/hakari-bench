# MNanoBEIR / NanoBEIR-it / NanoNFCorpus

## Overview

NFCorpus is a biomedical and nutrition-focused retrieval benchmark.
`NanoBEIR-it__NanoNFCorpus` uses Italian translated health queries to retrieve
Italian translated biomedical documents.

## Details

### What the Original Data Measures

[NFCorpus](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf)
was built for medical information retrieval over nutrition and health claims.
[BEIR](https://arxiv.org/abs/2104.08663) includes it as a biomedical retrieval
task, and [MMTEB](https://arxiv.org/abs/2502.13595) provides the multilingual
benchmark context.

### Observed Data Profile

The sampled Italian Nano task has 50 queries, 2,953 documents, and 1,651
positive qrels. It is highly multi-positive, averaging 33.02 positives per
query. Queries are often very short health phrases; documents are long
biomedical abstracts averaging 1,725.46 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3633 and hit@10 = 0.7200. Short queries and many
technical abstracts make the task sensitive to domain vocabulary and synonymy,
although exact biomedical terms can give BM25 useful anchors.

### Training Data That May Help

Useful training data includes non-overlapping biomedical IR, nutrition QA,
clinical abstract retrieval, and Italian or multilingual health retrieval.
Exclude NFCorpus, BEIR, NanoBEIR, and overlapping medical abstracts.

### Synthetic Data Guidance

Generate Italian health search phrases from non-evaluation biomedical
abstracts. Include short layperson queries and technical queries, with hard
negatives that share symptoms, foods, or organisms but address a different
finding.

## Example Data

| Query | Positive document |
| --- | --- |
| Frullati di cioccolato salutari (31 chars) | Obiettivo: Studiare la relazione tra il consumo di ciliegie e il rischio di attacchi di gotta ricorrenti tra individui affetti da gotta. Metodi: Abbiamo condotto uno studio caso-crossover per esaminare le associazioni di un i ... [truncated 225 chars](1901 chars) |
| etica medica (12 chars) | SFONDO: Uno dei principali problemi nel controllare il colesterolo sierico attraverso l'intervento dietetico sembra essere la necessità di migliorare l'aderenza del paziente. OBIETTIVI: Esplorare le molte domande riguardanti ... [truncated 225 chars](2032 chars) |
| fave (4 chars) | Negli ultimi 20 anni, l'interesse crescente per la biochimica, la nutrizione e la farmacologia della L-arginina ha portato a studi estesi per esplorare i suoi ruoli nutrizionali e terapeutici nel trattamento e nella prevenzio ... [truncated 225 chars](1443 chars) |
| Cosa contengono esattamente i nugget di pollo? (46 chars) | SCOPO: Determinare i componenti dei nuggets di pollo di due catene di fast food nazionali. CONTESTO: I nuggets di pollo sono diventati un componente fondamentale della dieta americana. Abbiamo cercato di determinare la compos ... [truncated 225 chars](807 chars) |
| Grassi saturi (13 chars) | L'interesse per la possibilità che l'alimentazione materna durante la gravidanza possa influenzare lo sviluppo di disturbi allergici nei bambini è in aumento. Lo studio prospettico attuale ha esaminato l'associazione tra l'as ... [truncated 225 chars](2262 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-it |
| Task / split | NanoNFCorpus |
| Hugging Face dataset | [hakari-bench/NanoBEIR-it](https://huggingface.co/datasets/hakari-bench/NanoBEIR-it) |
| Language | it |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,953 |
| Positive qrels | 1,651 |
| Avg positives / query | 33.02 |
| Positives per query (min / median / max) | 1 / 23.50 / 100 |
| Queries with multiple positives | 47 (94.0%) |
| BM25 nDCG@10 | 0.3633 |
| BM25 hit@10 | 0.7200 |
| Query length avg chars | 28.52 |
| Document length avg chars | 1,725.46 |

### Public Sources

- [NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-it](https://huggingface.co/datasets/hakari-bench/NanoBEIR-it)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | task paper | https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf |
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
  task_name: NanoNFCorpus
  split_name: NanoNFCorpus
  language: it
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-it__NanoNFCorpus.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 2953
    positive_qrels: 1651
  positives_per_query:
    average: 33.02
    min: 1
    median: 23.5
    max: 100
    multi_positive_queries: 47
    multi_positive_query_percent: 94.0
  text_stats_chars:
    query_mean: 28.52
    document_mean: 1725.457501
  bm25:
    ndcg_at_10: 0.3632787151
    hit_at_10: 0.72
    source: dataset_bm25_column
```
