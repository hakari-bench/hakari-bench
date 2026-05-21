# NanoBEIR-en / NanoQuoraRetrieval

## Overview

Quora duplicate-question retrieval asks a system to retrieve questions that are
semantically equivalent to a query question. `NanoQuoraRetrieval` is the compact
English BEIR/NanoBEIR version of this task. Queries and documents are short
user-written questions, and a relevant document is another Quora question that
asks the same underlying information need. The task tests paraphrase matching,
duplicate intent detection, and robustness to informal wording.

## Details

### What the Original Data Measures

No standalone task paper was confirmed for the Quora duplicate-question
retrieval dataset, but the BEIR benchmark paper does discuss how Quora is used
inside BEIR. [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of
Information Retrieval Models](https://arxiv.org/abs/2104.08663) groups Quora
under Duplicate-Question Retrieval and reports it as a binary-relevance English
task with 5,000 development queries, 10,000 test queries, 522,931 corpus
questions, about 1.6 relevant documents per query, and short average query and
document lengths. The paper also states that the Quora pairs were split into
train, dev, and test with overlaps removed so that a question in one split does
not appear in another split, which matters when choosing training data.
The interpretation below combines that BEIR paper evidence with the Quora
Question Pairs dataset record, BEIR/NanoBEIR metadata, ir_datasets
documentation, and observed Nano sample data.

The task measures whether a retriever can find another question with the same
intent, not whether it can find an answer passage. The relevant document is a
duplicate or near-duplicate question. This makes the task closer to paraphrase
retrieval, FAQ deduplication, and community-question routing than to open-domain
passage retrieval. A strong model must preserve intent while ignoring many
surface differences in wording, grammar, specificity, or question style.

### Observed Data Profile

The sampled task is dominated by short consumer-style questions rather than
formal search queries. The query openings are mostly direct interrogatives:
`what` and `how` account for most queries, with smaller numbers of `why`,
`can`, `does`, `is`, and `which` questions. The positive documents are also
questions, so the model must compare two formulations of an information need
instead of mapping a question to an answer-bearing passage.

The multi-positive clusters are the most informative part of the sample. One
query, "How do I overcome depression without psychiatric help?", has six
positives that preserve the same intent while varying the wording: professional
help, medicine or therapy, therapists, external help, and doing it alone. "How
do I improve on my math skills?" has five positives ranging from a close lexical
match ("How can I improve my math skills?") to variants with `maths` and more
personal phrasing. Other clusters cover medical school success, Ancient Rome
inventions, CS-student laptop recommendations, career interests, and chatbot
creation. These clusters show that a useful model should learn intent
equivalence over question rewrites, not just sentence similarity.

The sampled corpus is mostly made of short standalone questions, but it also
contains some longer Quora-style questions with personal context. Those longer
documents are not the norm, but they are useful reminders that the retrieval
unit is still a question: a candidate may include background details while the
relevant match depends on the core intent. The task also includes near-duplicate
questions with slightly different scope. For example, "How can I get a
commercial pilot's license?" is paired with both "How do I get a pilot's
license?" and "How do I get and maintain a pilot's license?", so the relevance
label tolerates some broadening or added maintenance context when the practical
information need remains close.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.7864
and hit@10 = 0.9400. This high baseline is expected because many positives share
important content words: `pilot's license`, `Ancient Rome`, `favorite pet`, or
`math skills`. In the inspected BM25 candidate ranking, 33 of the 70 positive
qrel rows are ranked first, and the median positive rank is 2. Lexical matching
therefore works well when the duplicate keeps the same rare phrase.

The failures are still useful. For "Which are the best laptops for CS
students?", BM25 ranks positives only at 23, 26, and 35 because candidates such
as "best laptops for university students" or "best laptops for computer science
and engineering students" share many words but are not labeled as the same
duplicate-question cluster. For "How is ISIS funded and how do they operate?",
the positive "How does ISIS get its money?" appears at rank 18, while BM25 is
distracted by generic `funded`, `money`, or `operate` questions. For "What are
the pros & cons of the demonization?", the positive about `demonetisation` is at
rank 17, behind unrelated `pros and cons` questions. These cases show that the
task is easy when duplicate questions reuse distinctive terms, but harder when
the model must normalize typos, morphology, abbreviations, or the central
entity-intent pair while ignoring generic question templates.

Because some queries have multiple positives, nDCG@10 is more informative than a
single-hit metric. A system should rank the whole acceptable duplicate cluster
highly: for the depression query, the best positive is rank 1 but other positives
appear at ranks 2, 3, 7, 15, and 37, so a model can still improve cluster-level
ordering even when hit@10 is already satisfied.

### Training Data That May Help

Use Quora duplicate-question training pairs or equivalent
paraphrase/duplicate-question datasets that are unlikely to overlap with the
benchmark. Public QQP or Quora-derived dev/test sets should preferably be
excluded when they may contain the same questions as the evaluation task.
Helpful auxiliary data includes FAQ duplicate pairs, community-question
paraphrase pairs, StackExchange duplicate question links, and supervised
intent-equivalence pairs.

### Synthetic Data Guidance

For document-to-question generation, start from non-evaluation questions and
generate alternate user questions that preserve intent while varying wording,
specificity, grammar, and word order. For joint generation, create clusters of
short questions around the same intent, with several positives per anchor
question. Synthetic positives should be genuinely answer-equivalent; related but
not duplicate questions should not be labeled positive.

## Example Data

| Query | Positive document |
| --- | --- |
| Is it okay to laugh at your own jokes? (38 chars) | Is it weird to laugh at my own jokes? (37 chars) |
| What is the best lie you ever spun? (35 chars) | What's the best-crafted lie you've ever told? (45 chars) |
| Why does Quora frequently suggest answers to my feed that put down Donald Trump? (80 chars) | Why does Quora only seem to have subjective, biased answers to questions about Donald Trump? (92 chars) |
| How can I make my self physically strong? (41 chars) | How do I make myself physically strong? (39 chars) |
| How will a quantum satellite work? (34 chars) | How does a Quantum satellite work and what would be some of its primary uses? (77 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBEIR-en |
| Backing dataset | NanoBEIR-en |
| Task / split | NanoQuoraRetrieval |
| Hugging Face dataset | [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en) |
| Language | en |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,046 |
| Positive qrels | 70 |
| Avg positives / query | 1.40 |
| Positives per query (min / median / max) | 1 / 1.00 / 6 |
| Queries with multiple positives | 10 (20.0%) |
| BM25 nDCG@10 | 0.7864 |
| BM25 hit@10 | 0.9400 |
| Query length avg chars | 47.96 |
| Document length avg chars | 54.81 |

### Public Sources

- [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs); 2017; dataset competition/source record.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych.
- [ir_datasets BEIR documentation](https://ir-datasets.com/beir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Quora Question Pairs | 2017 | dataset | https://kaggle.com/competitions/quora-question-pairs |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | paper | https://arxiv.org/abs/2104.08663 |
| ir_datasets BEIR documentation |  | dataset documentation | https://ir-datasets.com/beir |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoBEIR-en
  backing_dataset: NanoBEIR-en
  dataset_id: hakari-bench/NanoBEIR-en
  task_name: NanoQuoraRetrieval
  split_name: NanoQuoraRetrieval
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBEIR-en/NanoQuoraRetrieval.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone Quora duplicate-question retrieval paper was confirmed; the BEIR benchmark paper was inspected for Quora construction and evaluation context
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
    query_mean: 47.96
    document_mean: 54.808165
  bm25:
    ndcg_at_10: 0.7864009435
    hit_at_10: 0.94
    source: dataset_bm25_column
  learning:
    original_train_split: unknown
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding upstream dev/test data or other Quora-derived data likely to overlap with the BEIR/NanoBEIR evaluation questions
    useful_training_data:
      - non-overlapping Quora duplicate-question training pairs
      - FAQ and community-question duplicate pairs
      - supervised paraphrase and intent-equivalence datasets
    synthetic_data:
      document_generation: short user questions grouped by shared intent
      question_generation: paraphrased duplicate questions with varied wording and grammar
      answerability: positives should be answer-equivalent duplicate questions, not merely related questions
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-en
    source_urls:
      - label: Quora Question Pairs
        url: https://kaggle.com/competitions/quora-question-pairs
      - label: ir_datasets BEIR documentation
        url: https://ir-datasets.com/beir
      - label: Zeta Alpha NanoBEIR collection
        url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes: []
  references:
    - title: Quora Question Pairs
      url: https://kaggle.com/competitions/quora-question-pairs
      year: 2017
      doi: null
      is_paper: false
      source_confidence: probably_correct
    - title: 'BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models'
      url: https://arxiv.org/abs/2104.08663
      year: 2021
      doi: 10.48550/arXiv.2104.08663
      is_paper: true
      source_confidence: benchmark_context_paper
```
