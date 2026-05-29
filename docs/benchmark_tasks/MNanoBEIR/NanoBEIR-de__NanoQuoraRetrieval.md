# MNanoBEIR / NanoBEIR-de / NanoQuoraRetrieval

## Overview

Quora Question Pairs is a duplicate-question dataset. `NanoBEIR-de__NanoQuoraRetrieval`
is the German MNanoBEIR version: each query is a German translated question, and
the system must retrieve semantically duplicate German translated questions. The
task tests paraphrase-level question retrieval rather than evidence passage
retrieval.

## Details

### What the Original Data Measures

[Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs) is
the public competition dataset for identifying whether two Quora questions have
the same intent. No standalone task paper was confirmed for the retrieval
version. [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of
Information Retrieval Models](https://arxiv.org/abs/2104.08663) includes Quora
as a duplicate-question retrieval task and uses it to represent semantic
equivalence retrieval rather than answer evidence retrieval.

[MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595)
provides the multilingual benchmark context for this German Nano split.

### Observed Data Profile

The sampled German Nano task has 50 queries, 5,046 documents, and 70 positive
qrel rows. Queries average 1.40 positives, with 10 multi-positive queries. The
average query length is 55.72 characters, and the average document length is
65.12 characters.

The inspected pairs are short question paraphrases: improving math skills,
handling guilt, coping with depression, how ISIS is financed, and identifying
career interests. Some positives are near-identical, while others preserve the
same intent with different wording.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.6688 and hit@10 = 0.8000. BM25 ranks a positive first for 32 queries, and the
median first-positive rank is 1.

BM25 is strong when duplicate questions share many tokens, but this task still
tests semantic equivalence. A retriever should match `Wie werde ich
Schuldgefühle los?` to a question about dealing with guilt, and should handle
minor spelling or lexical variants such as `Mathekenntnisse` versus
`Mathematikkenntnisse`.

### Training Data That May Help

Useful training data includes non-overlapping duplicate-question pairs,
paraphrase datasets, German and multilingual semantic textual similarity data,
and hard-negative question retrieval examples where topic overlap is not enough.

Training should exclude Quora Question Pairs, BEIR, NanoBEIR, or translated
duplicate-question records likely to overlap with these evaluation questions.

### Synthetic Data Guidance

For document-to-query generation, start from short German questions and generate
alternative phrasings that preserve intent. Include exact near-duplicates,
lexical substitutions, changed word order, and compressed variants.

For hard negatives, generate questions on the same topic but with a different
intent so that models learn duplicate intent rather than topical similarity
alone.

## Example Data

| Query | Positive document |
| --- | --- |
| Ist es in Ordnung, über seine eigenen Witze zu lachen? (54 chars) | Ist es merkwürdig, über meine eigenen Witze zu lachen? (54 chars) |
| Welche ist die beste Lüge, die du je erzählt hast? (50 chars) | Welche ist die beste Lüge, die du je erzählt hast? (50 chars) |
| Warum schlägt Quora mir häufig Antworten vor, die Donald Trump kritisieren? (75 chars) | Warum gibt es auf Quora nur voreingenommene Antworten zu Fragen über Donald Trump? (82 chars) |
| Wie werde ich körperlich fit? (29 chars) | Wie kann ich körperlich fit werden? (35 chars) |
| Wie funktioniert ein Quanten-Satellit? (38 chars) | Wie funktioniert ein Quanten-Satellit und welche Hauptanwendungen hätte er? (75 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-de |
| Task / split | NanoQuoraRetrieval |
| Hugging Face dataset | [hakari-bench/NanoBEIR-de](https://huggingface.co/datasets/hakari-bench/NanoBEIR-de) |
| Language | de |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,046 |
| Positive qrels | 70 |
| Avg positives / query | 1.40 |
| Positives per query (min / median / max) | 1 / 1.00 / 6 |
| Queries with multiple positives | 10 (20.0%) |
| BM25 nDCG@10 | 0.7177 |
| BM25 hit@10 | 0.8800 |
| BM25 Recall@100 | 0.9286 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8323 |
| Dense hit@10 | 0.9000 |
| Dense Recall@100 | 0.9143 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.7982 |
| Reranking hybrid hit@10 | 0.9000 |
| Reranking hybrid Recall@100 | 0.9429 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 55.72 |
| Document length avg chars | 65.12 |

### Public Sources

- [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs); 2017; DataCanary, hilfialkaff, Lili Jiang, Meg Risdal, Nikhil Dandekar, tomtung.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025; Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Marton Kardos, Ashwin Mathur, and others; DOI: `10.48550/arXiv.2502.13595`.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-de](https://huggingface.co/datasets/hakari-bench/NanoBEIR-de)
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
  backing_dataset: NanoBEIR-de
  dataset_id: hakari-bench/NanoBEIR-de
  task_name: NanoQuoraRetrieval
  split_name: NanoQuoraRetrieval
  language: de
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-de__NanoQuoraRetrieval.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone Quora retrieval task paper was confirmed; interpretation
      uses the Quora Question Pairs dataset page and BEIR benchmark framing
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
    query_mean: 55.72
    document_mean: 65.11633
  bm25:
    ndcg_at_10: 0.7177470760377256
    hit_at_10: 0.88
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: MNanoBEIR German NanoBEIR task split from hakari-bench/NanoBEIR-de
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding Quora Question Pairs, BEIR, or NanoBEIR records
      likely to overlap with these evaluation questions
    useful_training_data:
    - non-overlapping duplicate-question pairs
    - German and multilingual paraphrase datasets
    - semantic textual similarity data
    - hard-negative question retrieval examples
    synthetic_data:
      document_generation: short German questions from broad consumer, career, technical,
        and personal topics
      question_generation: duplicate German question paraphrases with varied wording
        but preserved intent
      answerability: positives should be semantically duplicate questions, not merely
        topically related questions
    multi_positive_training: useful
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-de
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
    - German task is a multilingual NanoBEIR adaptation of the original English BEIR
      task
    - BEIR frames this source as duplicate-question retrieval
  references:
  - title: Quora Question Pairs
    url: https://kaggle.com/competitions/quora-question-pairs
    year: 2017
    doi: null
    is_paper: false
    source_confidence: definitive_dataset_page
  - title: 'BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
      Retrieval Models'
    url: https://arxiv.org/abs/2104.08663
    year: 2021
    doi: 10.48550/arXiv.2104.08663
    is_paper: true
    source_confidence: benchmark_context_paper
  - title: 'MMTEB: Massive Multilingual Text Embedding Benchmark'
    url: https://arxiv.org/abs/2502.13595
    year: 2025
    doi: 10.48550/arXiv.2502.13595
    is_paper: true
    source_confidence: benchmark_context_paper
  - title: 'NanoBEIR: Smaller BEIR dataset subsets'
    url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    year: 2024
    doi: null
    is_paper: false
    source_confidence: dataset_collection
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.717747076
      hit_at_10: 0.88
      recall_at_100: 0.9285714286
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9285714286
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8323202091
      hit_at_10: 0.9
      recall_at_100: 0.9142857143
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9142857143
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.798200166
      hit_at_10: 0.9
      recall_at_100: 0.9428571429
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.02
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9428571429
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
