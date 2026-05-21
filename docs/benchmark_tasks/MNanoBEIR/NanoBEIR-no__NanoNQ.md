# MNanoBEIR / NanoBEIR-no / NanoNQ

## Overview

Natural Questions is an open-domain question answering retrieval benchmark.
`NanoBEIR-no__NanoNQ` uses Norwegian translated questions to retrieve Norwegian
translated Wikipedia passages containing answer evidence.

## Details

### What the Original Data Measures

[Natural Questions](https://aclanthology.org/Q19-1026/) introduced real Google
search questions paired with Wikipedia answers and annotations. BEIR includes
NQ as open-domain QA retrieval, and MMTEB provides the multilingual benchmark
context for this Norwegian version.

### Observed Data Profile

The sampled task has 50 queries, 5,035 documents, and 57 positive qrels. Most
queries have one positive, while 7 queries have two. Queries average 48.04
characters and documents average 521.96 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3011 and hit@10 = 0.4800. The median first-positive
rank is 13.5. Short translated questions often need answer semantics beyond
exact lexical overlap.

### Training Data That May Help

Useful data includes non-overlapping open-domain QA retrieval, Wikipedia
question-passage pairs, and Norwegian or multilingual answer retrieval data.
Training should exclude Natural Questions, BEIR, NanoBEIR, and overlapping
translated passages.

### Synthetic Data Guidance

Generate Norwegian information-seeking questions from non-evaluation Wikipedia
paragraphs. Hard negatives should contain related entities but not the answer.

## Example Data

| Query | Positive document |
| --- | --- |
| Hvor blir Final Four avholdt i år? (34 chars) | Turneringen om NCAA Division I menns college-basketball i 2018 var en 68-lags utslagningsturnering som skulle kåre nasjonal mester i college-basketball for sesongen 2017–18. Den 80. utgaven av turneringen startet 13. mars 201 ... [truncated 225 chars](295 chars) |
| Var Nattens Hær opprinnelig en Disney-film? (43 chars) | The Nightmare Before Christmas hadde sin opprinnelse i et dikt skrevet av Tim Burton i 1982, mens han jobbet som animator ved Walt Disney Feature Animation. Med suksessen til Vincent samme år begynte Walt Disney Studios å vur ... [truncated 225 chars](629 chars) |
| Hvorfor står Engelen i Nord-England der? (40 chars) | Ifølge Gormley hadde en engel en trefoldig betydning: først for å indikere at kullgruvearbeidere hadde jobbet i to århundrer under stedet der den ble bygget, andre for å fange overgangen fra en industriell til en informasjons ... [truncated 225 chars](302 chars) |
| Hvor i den amerikanske grunnloven ble 3/5-kompromisset opprinnelig nevnt? (73 chars) | Tre-femtedelskompromisset finnes i Artikkel 1, Avsnitt 2, Punkt 3 i Den amerikanske grunnloven, som lyder: (106 chars) |
| Hvem synger "Somebody's Watching Me" sammen med Michael Jackson? (64 chars) | "Somebody's Watching Me" er en sang av den amerikanske sangeren Rockwell fra hans debutalbum med samme navn (1984). Den ble utgitt som Rockwells debutsingel og første singel fra albumet 14. januar 1984, av Motown. Den innehol ... [truncated 225 chars](347 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-no |
| Task / split | NanoNQ |
| Hugging Face dataset | [hakari-bench/NanoBEIR-no](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no) |
| Language | no |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,035 |
| Positive qrels | 57 |
| Avg positives / query | 1.14 |
| Positives per query (min / median / max) | 1 / 1.00 / 2 |
| Queries with multiple positives | 7 (14.0%) |
| BM25 nDCG@10 | 0.3011 |
| BM25 hit@10 | 0.4800 |
| Query length avg chars | 48.04 |
| Document length avg chars | 521.96 |

### Public Sources

- [Natural Questions: A Benchmark for Question Answering Research](https://aclanthology.org/Q19-1026/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-no](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Natural Questions: A Benchmark for Question Answering Research | 2019 | task paper | https://aclanthology.org/Q19-1026/ |
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
  task_name: NanoNQ
  split_name: NanoNQ
  language: "no"
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-no__NanoNQ.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 5035
    positive_qrels: 57
  positives_per_query:
    average: 1.14
    min: 1
    median: 1.0
    max: 2
    multi_positive_queries: 7
    multi_positive_query_percent: 14.0
  text_stats_chars:
    query_mean: 48.04
    document_mean: 521.956902
  bm25:
    ndcg_at_10: 0.3011019999
    hit_at_10: 0.48
    source: dataset_bm25_column
```
