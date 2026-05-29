# NanoBRIGHT / NanoBrightTheoremQATheorems

## Overview

`NanoBrightTheoremQATheorems` is the theorem-definition retrieval slice of
BRIGHT. Queries are theorem-based mathematical or scientific problems, and
relevant documents are ProofWiki theorem statements or definitions used in the
solution.

## Details

### What the Original Data Measures

[BRIGHT](https://arxiv.org/abs/2407.12883) reports that its theorem retrieval
setting uses TheoremQA queries with a different corpus: theorem statements from
ProofWiki. The paper aligns TheoremQA theorems to ProofWiki titles and uses
GPT-4 verification, retaining only queries with at least one relevant theorem
statement. This task tests whether a retriever can infer the theorem behind an
applied problem.

### Observed Data Profile

The split has 76 queries, 10,000 documents, and 151 positive qrels. Queries
average 415.62 characters and are applied or story-like math prompts. Documents
average 401.12 characters and contain theorem or definition text with tags and
proof snippets. Positives average 1.99 per query, and 47 queries have multiple
positives.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.0123 and hit@10 = 0.0263. It ranks only 1 query with a positive first, and
the median best positive rank is 99. This is extremely hard for lexical
retrieval because the query describes an applied situation while the positive
document is a formal theorem statement with little shared wording.

### Training Data That May Help

Useful data includes theorem-labeled problem datasets, ProofWiki-style theorem
retrieval, symbolic math problem-to-theorem pairs, and hard negatives from the
same mathematical area but a different theorem.

### Synthetic Data Guidance

Generate applied math scenarios from theorem statements, then train retrieval to
the theorem definition or proof page. Positives should be theorem statements
actually needed in the solution. Hard negatives should share tags such as graph
theory, linear algebra, or combinatorics while not supporting the solution.

## Example Data

| Query | Positive document |
| --- | --- |
| A teacher wants to create a special team for a project and needs to pick 3 students out of a class of 20. Assuming each student has an equal chance to be selected and the order in which they are chosen doesn't matter, how man ... [truncated 225 chars](264 chars) | \section{Multinomial Theorem} Tags: Multinomial Coefficients, Binomial Coefficients, Discrete Mathematics, Proofs by Induction, Algebra \begin{theorem} Let $x_1, x_2, \ldots, x_k \in F$, where $F$ is a field. Then: :$\ds \par ... [truncated 225 chars](1275 chars) |
| Imagine you're a graphic designer working on a 3D modeling project. You have three arrows: the first points 1 unit right, 2 units up, and 3 units forward; the second points 4 units right, 5 units up, and 6 units forward; and ... [truncated 225 chars](504 chars) | \section{Sample Matrix Independence Test} Tags: Linear Second Order ODEs, Linear Algebra \begin{theorem} Let $V$ be a vector space of real or complex-valued functions on a set $J$. Let $f_1, \ldots, f_n$ be functions in $V$. ... [truncated 225 chars](1157 chars) |
| Suppose you have a square sandbox of dimension 1 inch by 1 inch. You have 19 flags that you are going to plant anywhere in the sandbox. You also have a circular hoop with a radius of $\frac{\sqrt 2}{6}$, which you want to put ... [truncated 225 chars](412 chars) | \section{Pigeonhole Principle} Tags: Pigeonhole Principle, Named Theorems, Combinatorics \begin{theorem} Let $S$ be a finite set whose cardinality is $n$. Let $S_1, S_2, \ldots, S_k$ be a partition of $S$ into $k$ subsets. Th ... [truncated 225 chars](1575 chars) |
| Imagine you're organizing a small dinner party with 8 friends and you have 2 identical round tables to seat them. Each table can seat any number of guests, but you want to avoid leaving a table empty. In how many different wa ... [truncated 225 chars](274 chars) | \section{Construction of Permutations} Tags: Factorials, Combinatorics, Counting Arguments, Permutation Theory, Construction of Permutations, Permutations \begin{theorem} The ${}^n P_n$ permutations of $n$ objects can be gene ... [truncated 225 chars](520 chars) |
| Imagine you're organizing a tournament with teams from different cities, and each match can end in one of two outcomes: a win for the home team (marked with red) or a win for the visiting team (marked with blue). What is the ... [truncated 225 chars](525 chars) | \section{Ramsey's Theorem} Tags: Ramsey Theory, Named Theorems, Combinatorics \begin{theorem} In any coloring of the edges of a sufficiently large complete graph, one will find monochromatic complete subgraphs. For 2 colors, ... [truncated 225 chars](1743 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBRIGHT |
| Backing dataset | NanoBRIGHT |
| Task / split | NanoBrightTheoremQATheorems |
| Source task | TheoremQA theorem retrieval |
| Hugging Face dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| Language | en |
| Category | natural_language |
| Queries | 76 |
| Documents | 10000 |
| Positive qrels | 151 |
| Positives per query | avg 1.99, min 1, median 2, max 7 |
| Multi-positive queries | 47 (61.84%) |
| BM25 nDCG@10 | 0.0198 |
| BM25 hit@10 | 0.0526 |
| BM25 Recall@100 | 0.1457 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.1653 |
| Dense hit@10 | 0.3553 |
| Dense Recall@100 | 0.4305 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.0895 |
| Reranking hybrid hit@10 | 0.2237 |
| Reranking hybrid Recall@100 | 0.4106 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 30 |
| Query length avg chars | 415.62 |
| Document length avg chars | 401.12 |

### Public Sources

- [BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval](https://arxiv.org/abs/2407.12883).
- [BRIGHT project page](https://brightbenchmark.github.io/).
- [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT)
- Source dataset: [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT)
- MTEB dataset record: [mteb/BRIGHT](https://huggingface.co/datasets/mteb/BRIGHT)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval | 2024 | benchmark paper | https://arxiv.org/abs/2407.12883 |
| BRIGHT project page | 2024 | project page | https://brightbenchmark.github.io/ |
| xlangai/BRIGHT | 2024 | dataset card | https://huggingface.co/datasets/xlangai/BRIGHT |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoBRIGHT
  backing_dataset: NanoBRIGHT
  dataset_id: hakari-bench/NanoBRIGHT
  task_name: NanoBrightTheoremQATheorems
  split_name: NanoBrightTheoremQATheorems
  source_task: TheoremQA theorem retrieval
  source_dataset_id: xlangai/BRIGHT
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightTheoremQATheorems.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 76
    documents: 10000
    positive_qrels: 151
  positives_per_query:
    average: 1.986842105263158
    min: 1
    median: 2.0
    max: 7
    multi_positive_queries: 47
    multi_positive_query_percent: 61.8421052631579
  text_stats_chars:
    query_mean: 415.61842105263156
    document_mean: 401.121
  bm25:
    ndcg_at_10: 0.019831792457299924
    hit_at_10: 0.05263157894736842
    source: dataset_candidate_subset
  learning:
    original_train_split: unknown
    evaluation_split_origin: BRIGHT TheoremQA theorem-retrieval evaluation split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoBRIGHT TheoremQATheorems queries and ProofWiki theorem
      positives
    useful_training_data:
    - theorem-labeled problem datasets
    - ProofWiki-style theorem retrieval
    - symbolic math problem-to-theorem pairs
    synthetic_data:
      document_generation: theorem statements and proof snippets with mathematical
        tags
      question_generation: applied math scenarios requiring a specific theorem
      answerability: positive theorem should be necessary for the solution
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBRIGHT
    source_urls:
    - label: BRIGHT arXiv
      url: https://arxiv.org/abs/2407.12883
    - label: BRIGHT project
      url: https://brightbenchmark.github.io/
    - label: xlangai/BRIGHT
      url: https://huggingface.co/datasets/xlangai/BRIGHT
    source_notes: []
  references:
  - title: 'BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive
      Retrieval'
    url: https://arxiv.org/abs/2407.12883
    year: 2024
    doi: 10.48550/arXiv.2407.12883
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.0198317925
      hit_at_10: 0.0526315789
      recall_at_100: 0.1456953642
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 76
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1456953642
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.165301146
      hit_at_10: 0.3552631579
      recall_at_100: 0.4304635762
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 76
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4304635762
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.0894630937
      hit_at_10: 0.2236842105
      recall_at_100: 0.4105960265
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.394737
      query_count: 76
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4105960265
      safeguard_positive_rows: 30
      rows_with_101_candidates: 30
```
