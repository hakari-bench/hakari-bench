# NanoBRIGHT / NanoBrightAops

## Overview

`NanoBrightAops` is the AoPS math-competition slice of BRIGHT. Queries are
mathematical problems, and relevant documents are solved problems that rely on
the same underlying problem-solving skill or theorem rather than the same
surface wording.

## Details

### What the Original Data Measures

[BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval](https://arxiv.org/abs/2407.12883)
defines BRIGHT as "level 3" retrieval, where relevance requires reasoning
rather than keyword or direct semantic overlap. For AoPS, the paper reports that
math competition problems are sourced from American and International Math
Olympiad-style material and annotated with problem-solving skills from AoPS
Wiki. A solved problem is positive when its solution uses the same skill as the
query's solution.

### Observed Data Profile

The split has 111 queries, 10,000 documents, and 524 positive qrels. Queries
average 319.61 characters and are mostly competition-style math prompts with
LaTeX notation and multiple-choice answers. Documents average 549.07 characters
and include solved STEM problems. Almost every query has multiple positives:
the average is 4.72 positives per query, with a median of 4.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.1443 and hit@10 = 0.5225. Only 1 query has a positive ranked first, and the
median best positive rank is 8. This matches the BRIGHT paper's claim that
surface overlap is weak: two problems can share a theorem or counting technique
while using entirely different stories, variables, and notation.

### Training Data That May Help

Useful data includes non-overlapping math competition problems with worked
solutions, theorem- or skill-labeled problem pairs, AoPS-style explanations, and
hard negatives from the same broad topic but using a different technique.

### Synthetic Data Guidance

Generate solved competition problems grouped by explicit skills such as Vieta's
formulas, parity, inclusion-exclusion, or geometry angle chasing. Synthetic
queries should be full math problems, and positives should be different-looking
problems whose solutions require the same skill. Do not seed generation with
this Nano split's queries or positives.

## Example Data

| Query | Positive document |
| --- | --- |
| Two quadrilaterals are considered the same if one can be obtained from the other by a rotation and a translation. How many different convex cyclic quadrilaterals are there with integer sides and perimeter equal to 32? $\textb ... [truncated 225 chars](339 chars) | How many non-congruent triangles with perimeter 7 have integer side lengths? The longest side cannot be greater than 3, since otherwise the remaining two sides would not be long enough to form a triangle. The only possible tr ... [truncated 225 chars](315 chars) |
| In the diagram below, angle $ABC$ is a right angle. Point $D$ is on $\overline{BC}$, and $\overline{AD}$ bisects angle $CAB$. Points $E$ and $F$ are on $\overline{AB}$ and $\overline{AC}$, respectively, so that $AE=3$ and $AF ... [truncated 225 chars](323 chars) | Consider the set of all triangles $OPQ$ where $O$ is the origin and $P$ and $Q$ are distinct points in the plane with nonnegative integer coordinates $(x,y)$ such that $41x + y = 2009$. Find the number of such distinct triang ... [truncated 225 chars](1183 chars) |
| Determine the maximum value of $m^2 + n^2$, where $m$ and $n$ are integers satisfying $m, n \in \{ 1,2, \ldots , 1981 \}$ and $( n^2 - mn - m^2 )^2 = 1$. (153 chars) | The Fibonacci sequence $1,1,2,3,5,8,13,21,\ldots$ starts with two 1s, and each term afterwards is the sum of its two predecessors. Which one of the ten digits is the last to appear in the units position of a number in the Fib ... [truncated 225 chars](705 chars) |
| Triangle $ABC$ has $AC = 450$ and $BC = 300$. Points $K$ and $L$ are located on $\overline{AC}$ and $\overline{AB}$ respectively so that $AK = CK$, and $\overline{CL}$ is the angle bisector of angle $C$. Let $P$ be the point ... [truncated 225 chars](1166 chars) | In triangle $ABC$, medians $AD$ and $CE$ intersect at $P$, $PE=1.5$, $PD=2$, and $DE=2.5$. What is the area of $AEDC$? Note that $1.5^2 + 2^2 = 2.5^2,$ so $\triangle PED$ has a right angle at $P.$ (Alternatively, you could no ... [truncated 225 chars](899 chars) |
| The mean, median, and mode of the $7$ data values $60, 100, x, 40, 50, 200, 90$ are all equal to $x$. What is the value of $x$? $\textbf{(A)}\ 50 \qquad\textbf{(B)}\ 60 \qquad\textbf{(C)}\ 75 \qquad\textbf{(D)}\ 90 \qquad\tex ... [truncated 225 chars](239 chars) | The sum of 49 consecutive integers is $7^5$. What is their median? The sum of a set of integers is the product of the mean of the integers and the number of integers, and the median of a set of consecutive integers is the sam ... [truncated 225 chars](293 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBRIGHT |
| Backing dataset | NanoBRIGHT |
| Task / split | NanoBrightAops |
| Source task | AoPS |
| Hugging Face dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| Language | en |
| Category | natural_language |
| Queries | 111 |
| Documents | 10000 |
| Positive qrels | 524 |
| Positives per query | avg 4.72, min 1, median 4, max 8 |
| Multi-positive queries | 109 (98.20%) |
| BM25 nDCG@10 | 0.1443 |
| BM25 hit@10 | 0.5225 |
| Query length avg chars | 319.61 |
| Document length avg chars | 549.07 |

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
  task_name: NanoBrightAops
  split_name: NanoBrightAops
  source_task: AoPS
  source_dataset_id: xlangai/BRIGHT
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightAops.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 111
    documents: 10000
    positive_qrels: 524
  positives_per_query:
    average: 4.7207207207207205
    min: 1
    median: 4
    max: 8
    multi_positive_queries: 109
    multi_positive_query_percent: 98.1981981981982
  text_stats_chars:
    query_mean: 319.6126126126126
    document_mean: 549.0736
  bm25:
    ndcg_at_10: 0.14432700131414306
    hit_at_10: 0.5225225225225225
    source: dataset_bm25_column
  learning:
    original_train_split: unknown
    evaluation_split_origin: BRIGHT AoPS evaluation split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoBRIGHT AoPS queries, positives, and same-skill evaluation pairs
    useful_training_data:
      - non-overlapping math competition problems with worked solutions
      - theorem- or skill-labeled solved problem pairs
      - AoPS-style explanations and hard negatives from nearby skills
    synthetic_data:
      document_generation: solved competition problems grouped by explicit theorem or skill
      question_generation: full math contest prompts requiring the same skill as the positive
      answerability: positives should use the same problem-solving skill despite different surface wording
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
    - title: "BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval"
      url: https://arxiv.org/abs/2407.12883
      year: 2024
      doi: 10.48550/arXiv.2407.12883
      is_paper: true
      source_confidence: definitive_paper_link
```
