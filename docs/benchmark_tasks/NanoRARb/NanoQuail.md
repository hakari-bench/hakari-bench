# NanoRARb / NanoQuail

## Overview

`NanoQuail` recasts QuAIL reading-comprehension questions as answer retrieval.
The query includes a passage, question, and answer context; the positive
document is the correct answer option.

## Details

### What the Original Data Measures

[RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347)
uses QuAIL as a commonsense and reading-comprehension retrieval task. [Getting
Closer to AI Complete Question Answering: A Set of Prerequisite Real Tasks](https://ojs.aaai.org/index.php/AAAI/article/view/6398)
introduces QuAIL as question answering over passages requiring comprehension and
prerequisite reasoning.

This split stresses long-query understanding because the relevant answer is a
short option selected from a long narrative context.

### Observed Data Profile

The Nano split has 200 queries, 10,000 candidate documents, and 200 positive
qrels. Queries average 1,813.76 characters, while answer documents average only
25.02 characters.

Observed queries are long story passages followed by questions. Some positives
are regular answer phrases, and others are generic options such as "not enough
information."

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.0215
and hit@10 = 0.0350. It ranks 2 positives first.

The low lexical score is expected: many answer options are short and generic,
while the query contains long distractor context.

### Training Data That May Help

Helpful data includes reading-comprehension answer selection, long-passage QA,
and retrieval tasks where the answer is a short option grounded in a narrative
passage. Exclude NanoRARb evaluation passages and answers.

### Synthetic Data Guidance

Generate narrative passages with questions and concise answer options. Include
generic but valid answers, paraphrased answer options, and distractors that
match passage words without answering the question.

## Example Data

| Query | Positive document |
| --- | --- |
| Context: It took Erin an hour and forty-five minutes to drive from their half-million dollar home in Plano to the small rented cabin at Lake Texoma, near the Oklahoma state line. It was Thursday night, and she could have been ... [truncated 225 chars](1562 chars) | will have an argument with Erin (31 chars) |
| Context: I actually managed a kind of sleep there, kneeling with the circulation cut off to my legs, my head in canvas twilight. My body had squirted a year's supply of adrenalin into my bloodstream in the space of 30 minutes ... [truncated 225 chars](1943 chars) | After someone pulled the hood off their head. (45 chars) |
| Context: I'm a senior at Cesar Chavez high in San Francisco's sunny Mission district, and that makes me one of the most surveilled people in the world. My name is Marcus Yallow, but back when this story starts, I was going by ... [truncated 225 chars](1746 chars) | After I was told to report to the administration office immediately. (68 chars) |
| Context: Candy watched the bearded man drive his silver BMW into the convenience store parking lot and pull around to the side, near the back corner of the building. There were plenty of open slots in the front, so she figure ... [truncated 225 chars](1746 chars) | After the bearded man drove his silver BMW into the convenience store parking lot. (82 chars) |
| Context: They re-shackled and re-hooded me and left me there. A long time later, the truck started to move, rolling downhill, and then I was hauled back to my feet. I immediately fell over. My legs were so asleep they felt li ... [truncated 225 chars](1831 chars) | After they took off my hood. (28 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRARb |
| Backing dataset | NanoRARb |
| Task / split | NanoQuail |
| Hugging Face dataset | [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.0522 |
| BM25 hit@10 | 0.1250 |
| BM25 Recall@100 | 0.2850 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.1174 |
| Dense hit@10 | 0.2150 |
| Dense Recall@100 | 0.4600 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.0982 |
| Reranking hybrid hit@10 | 0.1900 |
| Reranking hybrid Recall@100 | 0.4650 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 107 |
| Query length avg chars | 1813.76 |
| Document length avg chars | 25.02 |

### Public Sources

- [RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347).
- [Getting Closer to AI Complete Question Answering: A Set of Prerequisite Real Tasks](https://ojs.aaai.org/index.php/AAAI/article/view/6398).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | https://arxiv.org/abs/2404.06347 |
| Getting Closer to AI Complete Question Answering: A Set of Prerequisite Real Tasks | 2020 | proceedings paper | https://ojs.aaai.org/index.php/AAAI/article/view/6398 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoRARb
  backing_dataset: NanoRARb
  dataset_id: hakari-bench/NanoRARb
  task_name: NanoQuail
  split_name: NanoQuail
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRARb/NanoQuail.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
  text_stats_chars:
    query_mean: 1813.755
    document_mean: 25.0175
  bm25:
    ndcg_at_10: 0.05219901067998609
    hit_at_10: 0.125
    source: dataset_candidate_subset
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoRARb
    source_urls:
    - label: RAR-b arXiv
      url: https://arxiv.org/abs/2404.06347
    - label: QuAIL AAAI
      url: https://ojs.aaai.org/index.php/AAAI/article/view/6398
  references:
  - title: 'RAR-b: Reasoning as Retrieval Benchmark'
    url: https://arxiv.org/abs/2404.06347
    year: 2024
    is_paper: true
  - title: 'Getting Closer to AI Complete Question Answering: A Set of Prerequisite
      Real Tasks'
    url: https://ojs.aaai.org/index.php/AAAI/article/view/6398
    year: 2020
    is_paper: true
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.0521990107
      hit_at_10: 0.125
      recall_at_100: 0.285
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.285
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.1174317869
      hit_at_10: 0.215
      recall_at_100: 0.46
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.46
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.0981772835
      hit_at_10: 0.19
      recall_at_100: 0.465
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.535
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.465
      safeguard_positive_rows: 107
      rows_with_101_candidates: 107
```
