# MNanoBEIR / NanoBEIR-ar / NanoQuoraRetrieval

## Overview

Quora duplicate-question retrieval asks a system to retrieve questions that are
semantically equivalent to a query question. `NanoBEIR-ar__NanoQuoraRetrieval`
is the Arabic MNanoBEIR version: both queries and documents are Arabic
translated user questions, and a positive document is another question with the
same underlying intent. The task tests paraphrase retrieval rather than
answer-passage retrieval.

## Details

### What the Original Data Measures

No standalone task paper was confirmed for Quora duplicate-question retrieval.
[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) groups Quora under
duplicate-question retrieval and describes the task as short questions with
binary relevance, where relevant documents are duplicate questions rather than
answer passages. The Quora Question Pairs dataset record provides the upstream
duplicate-question source.

[MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595)
provides the multilingual benchmark context for the Arabic Nano version. The
Arabic task is therefore a compact translated duplicate-question retrieval
benchmark: systems must find semantically equivalent user questions under
Arabic wording, transliteration, and paraphrase variation.

### Observed Data Profile

The sampled Arabic Nano task has 50 queries, 5,046 documents, and 70 positive
qrel rows. Queries average 1.40 positives; 10 of 50 queries have more than one
positive, and one query has 6 positives. The average query length is 43.22
characters, and the average document length is 58.16 characters.

The inspected pairs are short duplicate questions: translating Kannada text to
English or Hindi, how ISIS is funded, the biggest lie someone invented, how a
quantum satellite works, and why people think touching a pregnant woman's belly
is acceptable. Positives often preserve the same intent with small wording
changes. This is closer to FAQ deduplication and semantic paraphrase matching
than to evidence retrieval.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.6640 and hit@10 = 0.8200. BM25 ranks a positive first for 28 of 50 queries,
and the median first-positive rank is 1. Every query has a positive within the
top 100.

BM25 is strong when the duplicate retains rare content words, but it can miss
duplicates that change the phrasing or scope. In Arabic translation, a model
must distinguish true duplicate intent from related but not equivalent
questions. The best retrievers should rank all members of a duplicate cluster
highly, not just find one lexical neighbor.

### Training Data That May Help

Useful training data includes non-overlapping Quora duplicate-question pairs,
Arabic or multilingual paraphrase datasets, FAQ duplicate pairs,
StackExchange-style duplicate links, and supervised intent-equivalence data.
Training should exclude Quora, BEIR, NanoBEIR, or translated duplicate records
likely to overlap with these evaluation questions.

Because this task has some multi-positive clusters, training with multiple
positives per anchor question can improve cluster-level ranking.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation questions and
generate Arabic paraphrases that preserve the same answer intent while varying
word order, specificity, grammar, and politeness.

For joint generation, create clusters of short Arabic questions around the same
intent, with several positives per anchor. Synthetic positives should be
answer-equivalent duplicate questions, not merely related questions on the same
topic.

## Example Data

| Query | Positive document |
| --- | --- |
| هل من الجيد أن يضحك الشخص على نكاته الخاصة؟ (43 chars) | هل من الغريب أن أضحك على نكتي الخاصة؟ (37 chars) |
| ما هو أفضل كذبة اخترعتها في حياتك؟ (34 chars) | ما هي أكبر كذبة اخترعتها في حياتك؟ (34 chars) |
| لماذا يقترح موقع كورا باستمرار إجابات تهاجم دونالد ترامب في محتوى صفحتي؟ (72 chars) | لماذا تبدو إجابات موقع كورا حول أسئلة عن دونالد ترامب موضوعية ومتحيزة؟ (70 chars) |
| كيف يمكنني أن أصبح قويًا جسديًا؟ (32 chars) | كيف أصبح قويًا جسديًا؟ (22 chars) |
| كيف يعمل قمر صناعي كمي؟ (23 chars) | كيف يعمل قمر صناعي كمي؟ وما هي بعض الأغراض الرئيسية له؟ (55 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-ar |
| Task / split | NanoQuoraRetrieval |
| Hugging Face dataset | [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar) |
| Language | ar |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,046 |
| Positive qrels | 70 |
| Avg positives / query | 1.40 |
| Positives per query (min / median / max) | 1 / 1.00 / 6 |
| Queries with multiple positives | 10 (20.0%) |
| BM25 nDCG@10 | 0.6640 |
| BM25 hit@10 | 0.8200 |
| Query length avg chars | 43.22 |
| Document length avg chars | 58.16 |

### Public Sources

- [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs); 2017; dataset competition/source record.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025; Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Marton Kardos, Ashwin Mathur, and others; DOI: `10.48550/arXiv.2502.13595`.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Quora Question Pairs | 2017 | dataset | https://kaggle.com/competitions/quora-question-pairs |
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
  backing_dataset: NanoBEIR-ar
  dataset_id: hakari-bench/NanoBEIR-ar
  task_name: NanoQuoraRetrieval
  split_name: NanoQuoraRetrieval
  language: ar
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ar__NanoQuoraRetrieval.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone Quora duplicate-question retrieval paper was confirmed; the BEIR benchmark paper and Quora Question Pairs dataset record were used
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
    query_mean: 43.22
    document_mean: 58.162307
  bm25:
    ndcg_at_10: 0.6639835794
    hit_at_10: 0.82
    source: dataset_bm25_column
  learning:
    original_train_split: unknown
    evaluation_split_origin: MNanoBEIR Arabic NanoBEIR task split from hakari-bench/NanoBEIR-ar
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding Quora, BEIR, or NanoBEIR records likely to overlap with these evaluation duplicate questions
    useful_training_data:
      - non-overlapping Quora duplicate-question pairs
      - Arabic or multilingual paraphrase datasets
      - FAQ and community-question duplicate pairs
      - supervised intent-equivalence data
    synthetic_data:
      document_generation: short Arabic user questions grouped by shared intent
      question_generation: Arabic paraphrased duplicate questions with varied wording, specificity, and grammar
      answerability: positives should be answer-equivalent duplicate questions, not merely related questions
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar
    source_urls:
      - label: Quora Question Pairs
        url: https://kaggle.com/competitions/quora-question-pairs
      - label: BEIR paper
        url: https://arxiv.org/abs/2104.08663
      - label: MMTEB paper
        url: https://arxiv.org/abs/2502.13595
      - label: Zeta Alpha NanoBEIR collection
        url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes:
      - Arabic task is a multilingual NanoBEIR adaptation of the original English BEIR task
  references:
    - title: Quora Question Pairs
      url: https://kaggle.com/competitions/quora-question-pairs
      year: 2017
      doi: null
      is_paper: false
      source_confidence: probably_correct
    - title: "BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models"
      url: https://arxiv.org/abs/2104.08663
      year: 2021
      doi: 10.48550/arXiv.2104.08663
      is_paper: true
      source_confidence: benchmark_context_paper
    - title: "MMTEB: Massive Multilingual Text Embedding Benchmark"
      url: https://arxiv.org/abs/2502.13595
      year: 2025
      doi: 10.48550/arXiv.2502.13595
      is_paper: true
      source_confidence: benchmark_context_paper
    - title: "NanoBEIR: Smaller BEIR dataset subsets"
      url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
      year: 2024
      doi: null
      is_paper: false
      source_confidence: dataset_collection
```
