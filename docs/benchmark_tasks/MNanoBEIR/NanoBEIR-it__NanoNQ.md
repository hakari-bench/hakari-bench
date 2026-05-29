# MNanoBEIR / NanoBEIR-it / NanoNQ

## Overview

Natural Questions is a question-answering retrieval benchmark. `NanoBEIR-it__NanoNQ`
uses Italian translated questions to retrieve Italian translated Wikipedia
passages containing answer evidence.

## Details

### What the Original Data Measures

[Natural Questions](https://aclanthology.org/Q19-1026/) introduced real Google
search questions paired with Wikipedia answers and annotations. BEIR includes
NQ as open-domain QA retrieval, and MMTEB provides the multilingual benchmark
context for this Italian version.

### Observed Data Profile

The sampled task has 50 queries, 5,035 documents, and 57 positive qrels. Most
queries have one positive, while 7 queries have two. Queries average 54.32
characters and documents average 575.90 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3750 and hit@10 = 0.4800. The median first-positive
rank is 14, so the task needs semantic answer matching beyond short lexical
overlap.

### Training Data That May Help

Useful data includes non-overlapping open-domain QA retrieval, Wikipedia
question-passage pairs, and Italian or multilingual answer retrieval data.
Exclude Natural Questions, BEIR, NanoBEIR, and overlapping translated passages.

### Synthetic Data Guidance

Generate Italian information-seeking questions from non-evaluation Wikipedia
paragraphs. Hard negatives should contain related entities but not the answer.

## Example Data

| Query | Positive document |
| --- | --- |
| Dove si terrà la Final Four quest'anno? (39 chars) | L'80ª edizione del Torneo di Pallacanestro Maschile della Divisione I della NCAA 2018 è stato un torneo a eliminazione diretta con 68 squadre per determinare il campione nazionale di pallacanestro della Divisione I della NCAA ... [truncated 225 chars](367 chars) |
| L'incubo prima di Natale è stato originariamente un film Disney? (64 chars) | Il film "Nightmare Before Christmas" ha avuto origine da una poesia scritta da Tim Burton nel 1982, mentre lavorava come animatore presso la Walt Disney Feature Animation. Grazie al successo di "Vincent" nello stesso anno, la ... [truncated 225 chars](706 chars) |
| Perché l'Angelo del Nord si trova lì? (37 chars) | Secondo Gormley, il significato dell'angelo era triplice: innanzitutto, per indicare che sotto il sito della sua costruzione, i minatori di carbone avevano lavorato per due secoli; in secondo luogo, per comprendere la transiz ... [truncated 225 chars](370 chars) |
| Dove era originariamente stabilito il compromesso dei tre quinti nella Costituzione degli Stati Uniti? (102 chars) | Il Compromesso dei Tre Quinti è contenuto nell'Articolo 1, Sezione 2, Clausola 3 della Costituzione degli Stati Uniti, che recita: (130 chars) |
| Chi canta "Somebody's Watching Me" con Michael Jackson? (55 chars) | "Somebody's Watching Me" è un brano del cantante americano Rockwell, tratto dal suo album di debutto omonimo Somebody's Watching Me (1984). È stato pubblicato come primo singolo di Rockwell e singolo di lancio dell'album il 1 ... [truncated 225 chars](384 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-it |
| Task / split | NanoNQ |
| Hugging Face dataset | [hakari-bench/NanoBEIR-it](https://huggingface.co/datasets/hakari-bench/NanoBEIR-it) |
| Language | it |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,035 |
| Positive qrels | 57 |
| Avg positives / query | 1.14 |
| Positives per query (min / median / max) | 1 / 1.00 / 2 |
| Queries with multiple positives | 7 (14.0%) |
| BM25 nDCG@10 | 0.3750 |
| BM25 hit@10 | 0.4800 |
| BM25 Recall@100 | 0.7895 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.5133 |
| Dense hit@10 | 0.7000 |
| Dense Recall@100 | 0.8772 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4545 |
| Reranking hybrid hit@10 | 0.6600 |
| Reranking hybrid Recall@100 | 0.8947 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 4 |
| Query length avg chars | 54.32 |
| Document length avg chars | 575.90 |

### Public Sources

- [Natural Questions: A Benchmark for Question Answering Research](https://aclanthology.org/Q19-1026/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-it](https://huggingface.co/datasets/hakari-bench/NanoBEIR-it)
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
  backing_dataset: NanoBEIR-it
  dataset_id: hakari-bench/NanoBEIR-it
  task_name: NanoNQ
  split_name: NanoNQ
  language: it
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-it__NanoNQ.md
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
    query_mean: 54.32
    document_mean: 575.90149
  bm25:
    ndcg_at_10: 0.375010605688528
    hit_at_10: 0.48
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3750106057
      hit_at_10: 0.48
      recall_at_100: 0.7894736842
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7894736842
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.513285839
      hit_at_10: 0.7
      recall_at_100: 0.8771929825
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8771929825
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4544851181
      hit_at_10: 0.66
      recall_at_100: 0.8947368421
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.08
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8947368421
      safeguard_positive_rows: 4
      rows_with_101_candidates: 4
```
