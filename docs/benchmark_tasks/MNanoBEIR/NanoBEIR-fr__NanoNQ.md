# MNanoBEIR / NanoBEIR-fr / NanoNQ

## Overview

Natural Questions is a Wikipedia question answering benchmark built from real
Google search questions. `NanoBEIR-fr__NanoNQ` is the French MNanoBEIR version:
French translated natural questions must retrieve French translated Wikipedia
passages that contain the answer. The task tests open-domain evidence retrieval
for naturally phrased questions.

## Details

### What the Original Data Measures

[Natural Questions: a Benchmark for Question Answering
Research](https://aclanthology.org/Q19-1026/) introduces real, anonymized,
aggregated Google search queries paired with Wikipedia pages from top search
results. Annotators identify long answers, usually paragraphs or HTML regions,
and short answers when possible.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes NQ as a QA
retrieval task. [MMTEB: Massive Multilingual Text Embedding
Benchmark](https://arxiv.org/abs/2502.13595) provides the multilingual context
for this French split.

### Observed Data Profile

The sampled French Nano task has 50 queries, 5,035 documents, and 57 positive
qrel rows. Most queries have one positive, while 7 queries have multiple
positives. The average query length is 58.70 characters, and the average
document length is 588.82 characters.

The inspected questions ask about Kubo, Islamia College Peshawar,
sustainability, The Curse of Oak Island, and the Pennsylvania House of
Representatives. Documents are French translated Wikipedia answer passages.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.4383 and hit@10 = 0.6600. BM25 ranks a positive first for 11 queries, and
the median first-positive rank is 4.

Lexical matching helps for distinctive titles and names, but the model still
needs to retrieve the passage containing the answer, not just any page sharing
one entity from the question.

### Training Data That May Help

Useful training data includes non-overlapping Natural Questions retrieval data,
open-domain QA evidence retrieval pairs, French or multilingual Wikipedia QA
datasets, and question-to-passage supervision with real user questions. Training
should exclude NQ, BEIR, NanoBEIR, or translated records likely to overlap with
these examples.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation French Wikipedia
passages and generate natural search questions whose answers are present in the
passage. Include who, when, where, how many, and title-based questions.

## Example Data

| Query | Positive document |
| --- | --- |
| Où se déroule le Final Four cette année ? (41 chars) | Le tournoi de basket-ball universitaire de la Division I de la NCAA 2018 était un tournoi à élimination directe de 68 équipes visant à désigner le champion national de basket-ball universitaire de la Division I de la NCAA pou ... [truncated 225 chars](383 chars) |
| Le film "L'Étrange Noël de Monsieur Jack" était-il à l'origine un film de Disney ? (82 chars) | L'idée de L'Étrange Noël de Monsieur Jack est née d'un poème écrit par Tim Burton en 1982, alors qu'il travaillait comme animateur chez Walt Disney Feature Animation. Grâce au succès de Vincent la même année, les studios Walt ... [truncated 225 chars](678 chars) |
| Pourquoi l'Ange du Nord se trouve-t-il à cet endroit ? (54 chars) | Selon Gormley, la signification de cet ange est triple : d'abord, pour indiquer que sous le site de sa construction, des mineurs de charbon ont travaillé pendant deux siècles ; ensuite, pour marquer la transition d'une ère in ... [truncated 225 chars](345 chars) |
| Où le compromis des trois cinquièmes était-il initialement mentionné dans la Constitution ? (91 chars) | Le Compromis des trois cinquièmes se trouve à l'Article 1, Section 2, Clause 3 de la Constitution des États-Unis, qui stipule : (127 chars) |
| Qui chante "Someone's Watching Me" en duo avec Michael Jackson ? (64 chars) | “Somebody's Watching Me” est une chanson du chanteur américain Rockwell issue de son premier album studio éponyme, Somebody's Watching Me (1984). Elle a été publiée en tant que premier single et single phare de l'album le 14 ... [truncated 225 chars](389 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-fr |
| Task / split | NanoNQ |
| Hugging Face dataset | [hakari-bench/NanoBEIR-fr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-fr) |
| Language | fr |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,035 |
| Positive qrels | 57 |
| Avg positives / query | 1.14 |
| Positives per query (min / median / max) | 1 / 1.00 / 2 |
| Queries with multiple positives | 7 (14.0%) |
| BM25 nDCG@10 | 0.4460 |
| BM25 hit@10 | 0.7000 |
| BM25 Recall@100 | 0.8947 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.5970 |
| Dense hit@10 | 0.7600 |
| Dense Recall@100 | 0.9649 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.5556 |
| Reranking hybrid hit@10 | 0.7600 |
| Reranking hybrid Recall@100 | 0.9474 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 2 |
| Query length avg chars | 58.70 |
| Document length avg chars | 588.82 |

### Public Sources

- [Natural Questions: a Benchmark for Question Answering Research](https://aclanthology.org/Q19-1026/).
- [Natural Questions dataset page](https://ai.google.com/research/NaturalQuestions).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-fr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-fr)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Natural Questions: a Benchmark for Question Answering Research | 2019 | task paper | https://aclanthology.org/Q19-1026/ |
| Natural Questions dataset page |  | dataset page | https://ai.google.com/research/NaturalQuestions |
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
  task_name: NanoNQ
  split_name: NanoNQ
  language: fr
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-fr__NanoNQ.md
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
    query_mean: 58.7
    document_mean: 588.822244
  bm25:
    ndcg_at_10: 0.4460475552589896
    hit_at_10: 0.7
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4460475553
      hit_at_10: 0.7
      recall_at_100: 0.8947368421
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8947368421
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5970023213
      hit_at_10: 0.76
      recall_at_100: 0.9649122807
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9649122807
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.5556330439
      hit_at_10: 0.76
      recall_at_100: 0.9473684211
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.04
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9473684211
      safeguard_positive_rows: 2
      rows_with_101_candidates: 2
```
