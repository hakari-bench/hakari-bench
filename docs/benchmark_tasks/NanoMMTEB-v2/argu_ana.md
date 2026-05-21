# NanoMMTEB-v2 / argu_ana

## Overview

`argu_ana` is the ArguAna argument retrieval task. Queries are long debate
arguments, and the relevant document is the paired counterargument. The task
tests whether a retriever can match the same issue and aspect while recognizing
opposition rather than simple topical similarity.

## Details

### What the Original Data Measures

[Retrieval of the Best Counterargument without Prior Topic Knowledge](https://aclanthology.org/P18-1023/)
defines ArguAna as retrieval of the best counterargument for a given argument
without access to the prior debate topic. [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316)
includes ArguAna in its English retrieval suite, where retrieval uses nDCG@10 as
the main metric.

### Observed Data Profile

The split contains 199 queries, 8,626 documents, and 199 positive qrels. Each
query has one positive. Queries average 1,199.80 characters and documents
average 1,029.60 characters. The text is long debate prose with topic labels,
claims, warrants, examples, and citations.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.3326
and hit@10 = 0.7085. Shared debate vocabulary helps BM25 find the topic, but a
true positive must oppose the query; same-topic supporting arguments are strong
lexical distractors.

### Training Data That May Help

Helpful data includes non-overlapping argument-counterargument pairs, debate
stance pairs, argument mining data, and same-topic same-stance hard negatives.
Training on only duplicate or paraphrase retrieval is not enough because the
positive often disagrees with the query.

### Synthetic Data Guidance

Generate long argument and counterargument pairs where the positive challenges a
premise, consequence, analogy, or policy framing. Add same-topic supporting
arguments as negatives so the model must learn opposition and aspect matching.
Do not seed synthetic examples from evaluation arguments.

## Example Data

| Query | Positive document |
| --- | --- |
| Opposition to partial birth abortion is part of a strategy intended to ban abortion in general Partial-birth abortions form a tiny proportion of all abortions, but from a medical and psychological point of view they ought to ... [truncated 225 chars](704 chars) | pregnancy philosophy ethics life family house would ban partial birth abortions Although many people who are against partial-birth abortion are against abortion in general, there is no necessary link, as partial-birth abortio ... [truncated 225 chars](691 chars) |
| New Technology Humanity has revolutionized the world repeatedly through such monumental inventions as agriculture, steel, anti-biotics, and microchips. And as technology has improved, so too has the rate at which technology i ... [truncated 225 chars](1013 chars) | climate house believes were too late global climate change Technological improvements will almost certainly be developed for those who can afford them (as most technology is). However, climate change will have the greatest ef ... [truncated 225 chars](391 chars) |
| Being vegetarian reduces risks of food poisoning Almost all dangerous types of food poisoning are passed on through meat or eggs. So Campylobacter bacteria, the most common cause of food poisoning in England, are usually foun ... [truncated 225 chars](810 chars) | animals environment general health health general weight philosophy ethics Food safety and hygiene are very important for everyone, and governments should act to ensure that high standards are in place particularly in restaur ... [truncated 225 chars](1580 chars) |
| Collisions are a part of the game. First, collisions are part of the tradition of baseball. They have been part of the game for a very long time. Fans, players, and managers all expect home plate hits to occur from time to ti ... [truncated 225 chars](2256 chars) | team sports house believes major league baseball should continue allow collisions Collisions are much less a part of the game than people believe. The notion that collisions have been in the game for ages is a widely held mis ... [truncated 225 chars](1584 chars) |
| Community radio gives voices to the people rather than imposing those of the powerful. The events of the Arab Spring (and previous events such as the revolutions of 1989) have shown that effective means of communicating are v ... [truncated 225 chars](1266 chars) | media and good government house believes community radio good Community radio can indeed do the many wondrous things that Prop seems to trust it to do. It can also do more or less anything else. If proposition is trying to de ... [truncated 225 chars](558 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMMTEB-v2 |
| Backing dataset | NanoMMTEB-v2 |
| Task / split | argu_ana |
| Hugging Face dataset | [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2) |
| Source dataset | [mteb/arguana](https://huggingface.co/datasets/mteb/arguana) |
| Language | en |
| Category | natural_language |
| Queries | 199 |
| Documents | 8626 |
| Positive qrels | 199 |
| BM25 nDCG@10 | 0.3326 |
| BM25 hit@10 | 0.7085 |
| Query length avg chars | 1199.80 |
| Document length avg chars | 1029.60 |

### Public Sources

- [Retrieval of the Best Counterargument without Prior Topic Knowledge](https://aclanthology.org/P18-1023/).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316).
- [mteb/arguana](https://huggingface.co/datasets/mteb/arguana).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2)
- Source dataset: [mteb/arguana](https://huggingface.co/datasets/mteb/arguana)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Retrieval of the Best Counterargument without Prior Topic Knowledge | 2018 | task paper | https://aclanthology.org/P18-1023/ |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| mteb/arguana | 2024 | dataset card | https://huggingface.co/datasets/mteb/arguana |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMMTEB-v2
  backing_dataset: NanoMMTEB-v2
  dataset_id: hakari-bench/NanoMMTEB-v2
  task_name: argu_ana
  split_name: argu_ana
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMMTEB-v2/argu_ana.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 199
    documents: 8626
    positive_qrels: 199
  positives_per_query:
    average: 1.0
    min: 1
    median: 1
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 1199.8040201005026
    document_mean: 1029.6044516577788
  bm25:
    ndcg_at_10: 0.33261674263127566
    hit_at_10: 0.7085427135678392
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: do not train on this Nano split's queries, qrels, or paired counterarguments
    useful_training_data:
      - argument-counterargument pairs outside the evaluation split
      - stance-labeled debate data
      - same-topic same-stance hard negatives
    synthetic_data:
      document_generation: stance-opposed counterarguments with shared debate aspects
      question_generation: long debate arguments with explicit claims and warrants
      answerability: positive document must counter the query rather than support it
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2
    source_urls:
      - label: ArguAna paper
        url: https://aclanthology.org/P18-1023/
      - label: MTEB arXiv
        url: https://arxiv.org/abs/2210.07316
      - label: mteb/arguana
        url: https://huggingface.co/datasets/mteb/arguana
    source_notes: []
  references:
    - title: "Retrieval of the Best Counterargument without Prior Topic Knowledge"
      url: https://aclanthology.org/P18-1023/
      year: 2018
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "MTEB: Massive Text Embedding Benchmark"
      url: https://arxiv.org/abs/2210.07316
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
```
