# NanoRARb / NanoPIQA

## Overview

`NanoPIQA` retrieves the likely solution for a physical commonsense goal. The
query is a practical goal or problem, and the positive document is the correct
procedure or affordance-based answer.

## Details

### What the Original Data Measures

[RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347)
uses PIQA as a physical commonsense reasoning retrieval task. [PIQA: Reasoning
about Physical Commonsense in Natural Language](https://arxiv.org/abs/1911.11641)
introduces questions about everyday physical interactions, object affordances,
and plausible actions.

The retrieval version asks whether the correct physical solution is nearest to
the goal in a large answer pool.

### Observed Data Profile

The Nano split has 200 queries, 10,000 candidate documents, and 200 positive
qrels. Queries average 37.89 characters, and answer documents average 98.01
characters.

Observed queries are short practical prompts such as wearing clothing,
discouraging flies, or reusing a spray bottle.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.1571
and hit@10 = 0.2350. It ranks 16 positives first.

BM25 helps when solution text repeats object names, but many examples require
physical commonsense rather than exact lexical overlap.

### Training Data That May Help

Helpful training data includes physical commonsense QA, how-to retrieval, and
goal-to-procedure pairs. Exclude NanoRARb queries and answer documents.

### Synthetic Data Guidance

Generate household or physical goals with plausible and implausible procedures.
Hard negatives should mention the same objects but use unsafe, irrelevant, or
physically impossible actions.

## Example Data

| Query | Positive document |
| --- | --- |
| How to light a candle with a deep seated wick? (46 chars) | invert the candle upside down and use the lighter to reach into the wick to light it (84 chars) |
| How to grow a plant. (20 chars) | Bury seed in soil and add 1 cup of water daily. (47 chars) |
| How can I get free gym memberships? (35 chars) | Check with your health insurance co., many times they'll reimburse your gym costs. (82 chars) |
| Neatly wrap up an extension cord. (33 chars) | Wrap the cord around your hand and elbow. (41 chars) |
| napkin (6 chars) | hold ice cream scoop to keep hands warm (39 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRARb |
| Backing dataset | NanoRARb |
| Task / split | NanoPIQA |
| Hugging Face dataset | [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.1571 |
| BM25 hit@10 | 0.2350 |
| Query length avg chars | 37.89 |
| Document length avg chars | 98.01 |

### Public Sources

- [RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347).
- [PIQA: Reasoning about Physical Commonsense in Natural Language](https://arxiv.org/abs/1911.11641).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | https://arxiv.org/abs/2404.06347 |
| PIQA: Reasoning about Physical Commonsense in Natural Language | 2020 | arXiv paper | https://arxiv.org/abs/1911.11641 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoRARb
  backing_dataset: NanoRARb
  dataset_id: hakari-bench/NanoRARb
  task_name: NanoPIQA
  split_name: NanoPIQA
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRARb/NanoPIQA.md
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
    query_mean: 37.89
    document_mean: 98.01
  bm25:
    ndcg_at_10: 0.1571
    hit_at_10: 0.235
    source: dataset_bm25_column
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoRARb
    source_urls:
      - label: RAR-b arXiv
        url: https://arxiv.org/abs/2404.06347
      - label: PIQA arXiv
        url: https://arxiv.org/abs/1911.11641
  references:
    - title: "RAR-b: Reasoning as Retrieval Benchmark"
      url: https://arxiv.org/abs/2404.06347
      year: 2024
      is_paper: true
    - title: "PIQA: Reasoning about Physical Commonsense in Natural Language"
      url: https://arxiv.org/abs/1911.11641
      year: 2020
      is_paper: true
```
