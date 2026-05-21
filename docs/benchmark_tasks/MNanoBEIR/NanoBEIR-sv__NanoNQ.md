# MNanoBEIR / NanoBEIR-sv / NanoNQ

## Overview

Natural Questions is an answer-oriented Wikipedia retrieval benchmark.
`NanoBEIR-sv__NanoNQ` uses Swedish translated search questions to retrieve
Swedish translated answer passages.

## Details

### What the Original Data Measures

[Natural Questions](https://aclanthology.org/Q19-1026/) uses real search
questions with Wikipedia evidence. BEIR evaluates retrieval, and MMTEB provides
the multilingual context.

### Observed Data Profile

The task has 50 queries, 5,035 documents, and 57 positive qrels. Most queries
have one positive, with 7 multi-positive queries. Queries average 46.04
characters, and documents average 526.09 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3026 and hit@10 = 0.4400. The median first-positive
rank is 14.0, so many questions need semantic answer matching.

### Training Data That May Help

Useful data includes non-overlapping Swedish open-domain QA, Wikipedia passage
retrieval, and multilingual query-passage data. Exclude Natural Questions,
BEIR, NanoBEIR, and translated evaluation examples.

### Synthetic Data Guidance

Generate Swedish natural questions from encyclopedia passages. Hard negatives
should share entities but not answer the question.

## Example Data

| Query | Positive document |
| --- | --- |
| Var hålls Final Four detta år? (30 chars) | NCAA Division I:s herrarnas basketturnering 2018 var en turnering med utslagning för 68 lag för att kora herrarnas nationella mästare i collegebasket för NCAA Division I för säsongen 2017–18. Den 80:e upplagan av turneringen ... [truncated 225 chars](323 chars) |
| Var Nattens Häxer ursprungligen en Disney-film? (47 chars) | Nightmare Before Christmas uppstod från ett dikt skrivet av Tim Burton 1982, medan han arbetade som animatör på Walt Disney Feature Animation. Efter framgången med Vincent samma år började Walt Disney Studios överväga att gör ... [truncated 225 chars](612 chars) |
| Varför finns Ängeln i norr? (27 chars) | Enligt Gormley hade en ängel tre betydelser: först, att symbolisera att kolgruvarbetare arbetade under platsen för dess uppförande i två århundraden; andra, att förstå övergången från en industriell till en informationsålder, ... [truncated 225 chars](303 chars) |
| Var i grundlagen nämndes tre-femtedelskompromissen ursprungligen? (65 chars) | Tre-femtedelskompromissen finns i Artikel 1, Avsnitt 2, Paragraf 3 i USA:s konstitution, som lyder: (99 chars) |
| Vem sjunger "Someone's Watching Me" tillsammans med Michael Jackson? (68 chars) | "Somebody's Watching Me" är en låt av den amerikanska sångaren Rockwell från hans debutalbum Somebody's Watching Me (1984). Den släpptes som Rockwells debutsingel och förstasingel från albumet den 14 januari 1984 av Motown. D ... [truncated 225 chars](348 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-sv |
| Task / split | NanoNQ |
| Hugging Face dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |
| Language | sv |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,035 |
| Positive qrels | 57 |
| Positives per query avg | 1.14 |
| Positives per query min / median / max | 1 / 1.0 / 2 |
| Multi-positive queries | 7 (14.00%) |
| BM25 nDCG@10 | 0.3026 |
| BM25 hit@10 | 0.4400 |
| Query length avg chars | 46.04 |
| Document length avg chars | 526.09 |

### Public Sources

- [Natural Questions](https://aclanthology.org/Q19-1026/), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Natural Questions: a Benchmark for Question Answering Research | 2019 | task paper | https://aclanthology.org/Q19-1026/ |
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
  task_name: NanoNQ
  split_name: NanoNQ
  language: sv
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoNQ.md
  source_research: {primary_source_type: task_paper, paper_pdf_or_html_checked: true, no_paper_note: null}
  counts: {queries: 50, documents: 5035, positive_qrels: 57}
  positives_per_query: {average: 1.14, min: 1, median: 1.0, max: 2, multi_positive_queries: 7, multi_positive_query_percent: 14.0}
  text_stats_chars: {query_mean: 46.04, document_mean: 526.092552}
  bm25: {ndcg_at_10: 0.3025981597, hit_at_10: 0.44, source: dataset_bm25_column}
```
