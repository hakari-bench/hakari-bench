# NanoBRIGHT / NanoBrightBiology

## Overview

`NanoBrightBiology` is the Biology StackExchange slice of BRIGHT. Queries are
real user posts, and relevant documents are passages from web pages cited by
answers and judged to help address the question.

## Details

### What the Original Data Measures

[BRIGHT](https://arxiv.org/abs/2407.12883) states that its StackExchange tasks
use posts from knowledge-intensive domains and define relevance through cited
web documents in high-quality answers, followed by expert validation. For these
tasks, positives are not necessarily direct answers; they are supporting
documents that contain information needed to reason toward an answer.

### Observed Data Profile

The split has 103 queries, 10,000 documents, and 372 positive qrels. Queries
average 523.03 characters and often include detailed biological or perceptual
questions. Documents average 473.93 characters because the source web pages are
split into shorter passages. The task is strongly multi-positive, averaging
3.61 positives per query with a maximum of 19.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2489 and hit@10 = 0.5049. It ranks 26 queries with a positive first, and the
median best positive rank is 10. Lexical matching can catch terms such as
"fluoride" or "phototropism", but many biology questions require connecting a
lay question to a technical mechanism or cited concept.

### Training Data That May Help

Useful data includes non-overlapping Biology StackExchange posts with cited
references, biology QA with source citations, Wikipedia or textbook retrieval
pairs, and hard negatives about the same organism or mechanism but a different
explanation.

### Synthetic Data Guidance

Generate biology questions with enough context to require mechanism-level
retrieval, then pair them with cited passages about the relevant concept. Hard
negatives should share entities or terminology while failing to support the
specific biological explanation.

## Example Data

| Query | Positive document |
| --- | --- |
| What is the longest-lasting protein in a human body? Protein life times are, on average, not particularly long, on a human life timescale. I was wondering, how old is the oldest protein in a human body? Just to clarify, I mea ... [truncated 225 chars](1199 chars) | Characteristics[edit] Elastin is a very long-lived protein, with a half-life of over 78 years in humans. (104 chars) |
| Is kissing a natural human activity? The word natural here is meant in contrast to it being a sociological construct. Is kissing in all its forms something natural for humans? Is it instinctively erotic? Or is it just a conve ... [truncated 225 chars](435 chars) | Biology and evolution[edit] Black-tailed prairie dogs "kissing." Prairie dogs use a nuzzle of this variety to greet their relatives. Within the natural world of other animals, there are numerous analogies to kissing, notes Cr ... [truncated 225 chars](3310 chars) |
| What types of light can't a plant photosynthesize in? I have a plant on my desk, and it got me to wondering: Can my plant use the light from my monitors to photosynthesize? If so, what light (apart from green light, to a degr ... [truncated 225 chars](509 chars) | Chlorophyll is any of several related green pigments found in cyanobacteria and in the chloroplasts of algae and plants. Its name is derived from the Greek words χλωρός, khloros ("pale green") and φύλλον, phyllon ("leaf"). Ch ... [truncated 225 chars](712 chars) |
| If Tumors have lots of mutations in them how is it the immune system can't detect them? If a cancerous tumor has a lot of mutations in them why can't the immune system detect them? If a person has cancer could this somehow al ... [truncated 225 chars](425 chars) | In transplant rejection[edit] In a transplant procedure, as of an organ or stem cells, MHC molecules themselves act as antigens and can provoke immune response in the recipient, thus causing transplant rejection. MHC molecule ... [truncated 225 chars](3065 chars) |
| Could viruses be used as antibiotics? Could we use viruses that only affect bacteria to act as antibiotics? The more bacteria, the more times the virus divides, so the stronger it gets. Is this practical? (204 chars) | Applications[edit] Collection[edit] Phages for therapeutic use can be collected from environmental sources that likely contain high quantities of bacteria and bacteriophages, such as effluent outlets, sewage, or even soil. Th ... [truncated 225 chars](7339 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBRIGHT |
| Backing dataset | NanoBRIGHT |
| Task / split | NanoBrightBiology |
| Source task | Biology StackExchange |
| Hugging Face dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| Language | en |
| Category | natural_language |
| Queries | 103 |
| Documents | 10000 |
| Positive qrels | 372 |
| Positives per query | avg 3.61, min 1, median 3, max 19 |
| Multi-positive queries | 93 (90.29%) |
| BM25 nDCG@10 | 0.2489 |
| BM25 hit@10 | 0.5049 |
| Query length avg chars | 523.03 |
| Document length avg chars | 473.93 |

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
  task_name: NanoBrightBiology
  split_name: NanoBrightBiology
  source_task: Biology StackExchange
  source_dataset_id: xlangai/BRIGHT
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightBiology.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 103
    documents: 10000
    positive_qrels: 372
  positives_per_query:
    average: 3.6116504854368934
    min: 1
    median: 3
    max: 19
    multi_positive_queries: 93
    multi_positive_query_percent: 90.29126213592232
  text_stats_chars:
    query_mean: 523.0291262135922
    document_mean: 473.9342
  bm25:
    ndcg_at_10: 0.2489409555054503
    hit_at_10: 0.5048543689320388
    source: dataset_bm25_column
  learning:
    original_train_split: unknown
    evaluation_split_origin: BRIGHT Biology StackExchange evaluation split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoBRIGHT Biology queries, cited positives, and linked answer pages
    useful_training_data:
      - non-overlapping Biology StackExchange posts with cited sources
      - biology QA with source citations
      - biology textbook or Wikipedia retrieval pairs
    synthetic_data:
      document_generation: biology mechanism passages from source-like web references
      question_generation: detailed Biology StackExchange-style questions
      answerability: positives should support the biological explanation rather than merely share entities
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
