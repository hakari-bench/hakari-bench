# MNanoBEIR / NanoBEIR-fr / NanoQuoraRetrieval

## Overview

Quora Question Pairs is a duplicate-question dataset. `NanoBEIR-fr__NanoQuoraRetrieval`
is the French MNanoBEIR version: each query is a French translated question, and
the system must retrieve semantically duplicate French translated questions. The
task tests paraphrase-level intent matching rather than evidence retrieval.

## Details

### What the Original Data Measures

[Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs) is
the public competition dataset for identifying whether two Quora questions have
the same intent. No standalone task paper was confirmed for the retrieval
version. [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of
Information Retrieval Models](https://arxiv.org/abs/2104.08663) includes Quora
as a duplicate-question retrieval task.

[MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595)
provides the multilingual benchmark context for this French Nano split.

### Observed Data Profile

The sampled French Nano task has 50 queries, 5,046 documents, and 70 positive
qrel rows. Queries average 1.40 positives, with 10 multi-positive queries. The
average query length is 61.22 characters, and the average document length is
71.51 characters.

The inspected examples ask about improving math skills, overcoming guilt,
depression without professional help, ISIS financing, and discovering career
aspirations. Some pairs are exact duplicates; others preserve intent with
different wording.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.6828 and hit@10 = 0.8400. BM25 ranks a positive first for 29 queries, and
the median first-positive rank is 1.

BM25 is strong when duplicates share tokens, but the task still measures intent
equivalence. A retriever should distinguish true duplicates from same-topic
questions with different information needs.

### Training Data That May Help

Useful training data includes non-overlapping duplicate-question pairs, French
and multilingual paraphrase datasets, semantic textual similarity data, and
hard-negative question retrieval examples. Training should exclude Quora
Question Pairs, BEIR, NanoBEIR, or translated duplicate-question records likely
to overlap with these examples.

### Synthetic Data Guidance

For document-to-query generation, start from short French questions and
generate alternative phrasings that preserve intent. Include same-topic hard
negatives where topic overlap is high but the question is not a duplicate.

## Example Data

| Query | Positive document |
| --- | --- |
| Est-ce que c'est permis de rire de ses propres blagues ? (56 chars) | Est-ce que c'est bizarre de rire de mes propres blagues ? (57 chars) |
| Quel est le plus gros mensonge que tu aies jamais raconté ? (59 chars) | Quel est le plus beau mensonge que vous ayez jamais raconté ? (61 chars) |
| Pourquoi Quora suggère-t-il fréquemment des réponses dans mon fil d'actualité qui critiquent Donald Trump ? (107 chars) | Pourquoi Quora ne propose-t-il que des réponses partisanes aux questions sur Donald Trump ? (91 chars) |
| Comment renforcer ma condition physique ? (41 chars) | Comment puis-je améliorer ma condition physique ? (49 chars) |
| Comment fonctionne un satellite quantique ? (43 chars) | Comment fonctionne un satellite quantique et quelles seraient ses principales utilisations ? (92 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-fr |
| Task / split | NanoQuoraRetrieval |
| Hugging Face dataset | [hakari-bench/NanoBEIR-fr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-fr) |
| Language | fr |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,046 |
| Positive qrels | 70 |
| Avg positives / query | 1.40 |
| Positives per query (min / median / max) | 1 / 1.00 / 6 |
| Queries with multiple positives | 10 (20.0%) |
| BM25 nDCG@10 | 0.6828 |
| BM25 hit@10 | 0.8400 |
| Query length avg chars | 61.22 |
| Document length avg chars | 71.51 |

### Public Sources

- [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-fr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-fr)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Quora Question Pairs | 2017 | dataset page | https://kaggle.com/competitions/quora-question-pairs |
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
  backing_dataset: NanoBEIR-fr
  dataset_id: hakari-bench/NanoBEIR-fr
  task_name: NanoQuoraRetrieval
  split_name: NanoQuoraRetrieval
  language: fr
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-fr__NanoQuoraRetrieval.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone Quora retrieval task paper was confirmed; interpretation uses the Quora Question Pairs dataset page and BEIR benchmark framing
  counts:
    queries: 50
    documents: 5046
    positive_qrels: 70
  positives_per_query:
    average: 1.4
    min: 1
    median: 1.0
    max: 6
    multi_positive_queries: 10
    multi_positive_query_percent: 20.0
  text_stats_chars:
    query_mean: 61.22
    document_mean: 71.512089
  bm25:
    ndcg_at_10: 0.6827535757
    hit_at_10: 0.84
    source: dataset_bm25_column
```
