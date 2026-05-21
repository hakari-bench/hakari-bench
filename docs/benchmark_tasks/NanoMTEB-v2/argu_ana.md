# NanoMTEB-v2 / argu_ana

## Overview

`argu_ana` is the ArguAna retrieval task in NanoMTEB-v2. Queries are long
arguments from debate topics, and the relevant document is the paired
counterargument.

## Details

### What the Original Data Measures

[Retrieval of the Best Counterargument without Prior Topic Knowledge](https://aclanthology.org/P18-1023/)
defines ArguAna as a task for finding the best opposing argument for a given
argument without knowing the debate topic in advance. The paper emphasizes that
good counterarguments should address similar aspects while taking an opposing
stance, so the task is not ordinary semantic similarity. [MTEB](https://arxiv.org/abs/2210.07316)
includes ArguAna in its retrieval suite and evaluates retrieval primarily with
nDCG@10.

### Observed Data Profile

The NanoMTEB-v2 split has 199 queries, 8,626 documents, and 199 positive qrels.
Each query has one positive. Queries average 1,199.80 characters and documents
average 1,029.60 characters. The text is long-form debate prose with topic
labels, claims, premises, examples, and citations.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.3326 and hit@10 = 0.7085. It finds a positive in the top 10 for 141 of 199
queries, but no positive is ranked first and the median best rank is 5. The
ranking is helped by shared debate vocabulary, yet the positive is stance-opposed
rather than a duplicate or supporting passage.

### Training Data That May Help

Useful training data includes non-overlapping argument-counterargument pairs,
debate pro/con data, stance-labeled argument pairs, and hard negatives from
same-topic same-stance arguments.

### Synthetic Data Guidance

Synthetic examples should generate long argument pairs where the positive
attacks a premise, consequence, or policy framing of the query. Include
same-topic same-stance negatives so the model must learn counterargument
matching rather than only topical similarity.

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
| Nano set | NanoMTEB-v2 |
| Backing dataset | NanoMTEB-v2 |
| Task / split | argu_ana |
| Source task | ArguAna |
| Hugging Face dataset | [hakari-bench/NanoMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2) |
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

- Nano dataset: [hakari-bench/NanoMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2)
- Source dataset: [mteb/arguana](https://huggingface.co/datasets/mteb/arguana)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Retrieval of the Best Counterargument without Prior Topic Knowledge | 2018 | source task paper | https://aclanthology.org/P18-1023/ |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| mteb/arguana | 2024 | dataset card | https://huggingface.co/datasets/mteb/arguana |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-v2
  backing_dataset: NanoMTEB-v2
  dataset_id: hakari-bench/NanoMTEB-v2
  task_name: argu_ana
  split_name: argu_ana
  source_task: ArguAna
  source_dataset_id: mteb/arguana
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-v2/argu_ana.md
  source_research:
    primary_source_type: task_paper_and_benchmark_paper
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
    ndcg_at_10: 0.3325660140573749
    hit_at_10: 0.7085427135678392
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: MTEB ArguAna test split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoMTEB-v2 argu_ana queries, qrels, and positive documents
    useful_training_data:
      - argument-counterargument pairs outside this evaluation split
      - stance-labeled debate arguments
      - same-topic same-stance hard negatives
    synthetic_data:
      document_generation: stance-opposed counterarguments with shared aspects
      question_generation: long debate arguments as queries
      answerability: positive must counter the query rather than support it
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2
    source_urls:
      - label: ArguAna paper
        url: https://aclanthology.org/P18-1023/
      - label: MTEB arXiv
        url: https://arxiv.org/abs/2210.07316
      - label: mteb/arguana
        url: https://huggingface.co/datasets/mteb/arguana
    source_notes: []
  references:
    - title: Retrieval of the Best Counterargument without Prior Topic Knowledge
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
