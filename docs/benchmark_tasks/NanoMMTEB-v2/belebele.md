# NanoMMTEB-v2 / belebele

## Overview

`belebele` is a multilingual retrieval adaptation of the Belebele reading
comprehension benchmark. Queries are questions in many language variants, and
the retriever must return the passage that supports the answer. The task probes
cross-script multilingual matching and passage-level comprehension cues.

## Details

### What the Original Data Measures

[The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122 Language Variants](https://arxiv.org/abs/2308.16884)
introduces a fully parallel multiple-choice reading-comprehension benchmark over
FLORES-200 passages. The paper emphasizes broad language coverage, parallel
passages, and curated questions that should require reading the passage. In this
retrieval version, the question becomes the query and the answer-bearing passage
is the positive document.

### Observed Data Profile

The Nano split has 376 queries, 10,000 documents, and 376 positive qrels. Each
query has one positive. Queries average 95.39 characters, and documents average
509.21 characters. The sample visibly mixes scripts and languages, including
Arabic romanization, English, Hindi, Hebrew, Burmese-script text, and many
non-English passages.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.1402
and hit@10 = 0.2154. Lexical matching is weak because many questions and
passages are in different scripts or low-resource language variants, and the
question often asks about a passage fact without repeating many exact tokens.

### Training Data That May Help

Useful training data includes non-overlapping Belebele/FLORES passage-question
pairs, multilingual reading-comprehension retrieval, native-language QA pairs,
and cross-script hard negatives from the same FLORES topic. Avoid using the
evaluation question-passage pairs as supervised retrieval data.

### Synthetic Data Guidance

Generate native-language questions from non-evaluation passages across many
scripts. Include distractor passages that share topic, entities, or translated
content but do not answer the question. Synthetic data should preserve the
answerability constraint from reading comprehension: the passage must explicitly
support the answer.

## Example Data

| Query | Positive document |
| --- | --- |
| Vad är enligt avsnittet inte ett bra knep för att spela dragspel? (65 chars) | Se till att din hand är så avslappnad som möjligt medan du fortfarande träffar alla noter korrekt. Försök också att inte göra många överflödiga rörelser med fingrarna. På det här sättet tröttar du ut dig själv så lite som möj ... [truncated 225 chars](440 chars) |
| وفقاً للفقرة، ما الذي لا يُعتبر نصيحة دقيقة للعزف الناجح على الأكورديون؟ (72 chars) | Make sure your hand is as relaxed as possible while still hitting all the notes correctly - also try not to make much extraneous motion with your fingers. This way, you will tire yourself out as little as possible. Remember t ... [truncated 225 chars](399 chars) |
| According to the passage, what would not be considered an accurate tip for successfully playing the accordion? (110 chars) | تأكد من استرخاء يدك قدر الإمكان مع الاستمرار في ضرب كل النغمات بشكل صحيح - حاول كذلك عدم القيام بحركاتٍ غريبةٍ بأصابعك. لن تبذل مجهوداً كبيراً إذا اتبعت تلك الطريقة. ضع نصب عينيك أنه ليس عليك الضغط على مفاتيح الأكورديون بقوةٍ ... [truncated 225 chars](364 chars) |
| Čo sa podľa úryvku nepovažuje za presné odporúčanie, ako dobre hrať na akordeóne? (81 chars) | Make sure your hand is as relaxed as possible while still hitting all the notes correctly - also try not to make much extraneous motion with your fingers. This way, you will tire yourself out as little as possible. Remember t ... [truncated 225 chars](399 chars) |
| anuchhed anusar, kun MySpace suvidhaley padhna samasya vayeka vidyarthiharulai faidajanak huna sakchha? (103 chars) | MySpace is the third most popular website used in the United States and has 54 million profiles currently. These websites have gotten a lot of attention, especially in the education setting. There are positive aspects to thes ... [truncated 225 chars](638 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMMTEB-v2 |
| Backing dataset | NanoMMTEB-v2 |
| Task / split | belebele |
| Hugging Face dataset | [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2) |
| Source dataset | [mteb/belebele](https://huggingface.co/datasets/mteb/belebele) |
| Language | multilingual |
| Category | natural_language |
| Queries | 376 |
| Documents | 10000 |
| Positive qrels | 376 |
| BM25 nDCG@10 | 0.0903 |
| BM25 hit@10 | 0.1383 |
| BM25 Recall@100 | 0.2207 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2781 |
| Dense hit@10 | 0.3404 |
| Dense Recall@100 | 0.4787 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.1782 |
| Reranking hybrid hit@10 | 0.2473 |
| Reranking hybrid Recall@100 | 0.4122 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 221 |
| Query length avg chars | 95.39 |
| Document length avg chars | 509.21 |

### Public Sources

- [The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122 Language Variants](https://arxiv.org/abs/2308.16884).
- [mteb/belebele](https://huggingface.co/datasets/mteb/belebele).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2)
- Source dataset: [mteb/belebele](https://huggingface.co/datasets/mteb/belebele)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122 Language Variants | 2024 | task paper | https://arxiv.org/abs/2308.16884 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| mteb/belebele | 2024 | dataset card | https://huggingface.co/datasets/mteb/belebele |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMMTEB-v2
  backing_dataset: NanoMMTEB-v2
  dataset_id: hakari-bench/NanoMMTEB-v2
  task_name: belebele
  split_name: belebele
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMMTEB-v2/belebele.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 376
    documents: 10000
    positive_qrels: 376
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 95.3936170212766
    document_mean: 509.2113
  bm25:
    ndcg_at_10: 0.0903338585074925
    hit_at_10: 0.13829787234042554
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: do not train on this Nano split's questions, qrels, or positive
      passages
    useful_training_data:
    - non-overlapping Belebele or FLORES passage-question pairs
    - multilingual reading-comprehension retrieval data
    - native-language QA retrieval pairs
    - cross-script hard negatives
    synthetic_data:
      document_generation: native-language short passages in FLORES-like domains
      question_generation: questions answerable only from the associated passage
      answerability: positive passage must explicitly support the answer
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2
    source_urls:
    - label: Belebele arXiv
      url: https://arxiv.org/abs/2308.16884
    - label: mteb/belebele
      url: https://huggingface.co/datasets/mteb/belebele
    - label: MMTEB arXiv
      url: https://arxiv.org/abs/2502.13595
    source_notes: []
  references:
  - title: 'The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122
      Language Variants'
    url: https://arxiv.org/abs/2308.16884
    year: 2024
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'MMTEB: Massive Multilingual Text Embedding Benchmark'
    url: https://arxiv.org/abs/2502.13595
    year: 2025
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.0903338585
      hit_at_10: 0.1382978723
      recall_at_100: 0.2207446809
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 376
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2207446809
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2781240391
      hit_at_10: 0.3404255319
      recall_at_100: 0.4787234043
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 376
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4787234043
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.178216765
      hit_at_10: 0.2473404255
      recall_at_100: 0.4122340426
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.587766
      query_count: 376
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4122340426
      safeguard_positive_rows: 221
      rows_with_101_candidates: 221
```
