# NanoMMTEB-v2 / miracl

## Overview

`miracl` is a multilingual Wikipedia retrieval task from MIRACL hard negatives.
Queries are short information needs in many languages, and documents are
Wikipedia passages. The retriever must find same-language answer-bearing
passages despite hard negatives from BM25 and dense retrievers.

## Details

### What the Original Data Measures

[Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages](https://arxiv.org/abs/2210.09984)
introduces monolingual retrieval over Wikipedia for 18 languages, with relevance
judgments created by native speakers. The MTEB hard-negative version pools top
candidates from BM25 and multilingual dense retrievers, making retrieved
documents more confusable than a random corpus sample.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 444 positive qrels. Queries
average 37.22 characters and documents average 448.21 characters. The observed
examples include Persian, English, German, Bengali, and other languages, while
documents are short Wikipedia-style passages. The task is multi-positive, with
an average of 2.22 positives per query.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.5714
and hit@10 = 0.8400. Lexical matching is useful for named entities and exact
topic terms, but cross-script tokenization, morphology, and multiple relevant
passages keep it from being a solved lexical task.

### Training Data That May Help

Useful training data includes MIRACL train splits, native-language Wikipedia
query-passage retrieval, multilingual QA retrieval, and hard negatives from the
same language and topic. Avoid using MIRACL dev/test examples that overlap with
this Nano split.

### Synthetic Data Guidance

Generate native-language questions from non-evaluation Wikipedia passages.
Include hard negatives from the same article or adjacent entities. Synthetic
questions should be natural information needs, not translated English-only
templates, and positives should explicitly answer the question.

## Example Data

| Query | Positive document |
| --- | --- |
| కిమ్మూరు గ్రామ విస్తీర్ణం ఎంత? (30 chars) | కిమ్మూరు ఇది మండల కేంద్రమైన అడ్డతీగల నుండి 25 కి. మీ. దూరం లోను, సమీప పట్టణమైన పెద్దాపురం నుండి 33 కి. మీ. దూరంలోనూ ఉంది. 2011 భారత జనగణన గణాంకాల ప్రకారం ఈ గ్రామం 249 ఇళ్లతో, 887 జనాభాతో 283 హెక్టార్లలో విస్తరించి ఉంది. గ్రామ ... [truncated 225 chars](380 chars) |
| Welche Sekte hat Jim Jones geführt? (35 chars) | William Branham In den Jahren 1956 und 1957 unterstützte William Branham den jungen Prediger des Latter-Rain Movements und späteren Sektenführer Jim Jones und trat beispielsweise als Gastprediger in einer von ihm geleiteten P ... [truncated 225 chars](541 chars) |
| متى عقدت الجمعية البرلمانية لمجلس أوروبا دورتها الأولى؟ (55 chars) | الجمعية البرلمانية لمجلس أوروبا عقدت الجمعية دورتها الأولى في ستراسبورغ في 10 أغسطس 1949. (90 chars) |
| 印度人口有多少？ (8 chars) | 印度人口 印度人口的结构主要以语言、宗教以及种姓来划分。2007年大概有11亿，2011年3月31日公布的人口普查的初步结果是12.1亿，2017年人口数为13.24亿人。印度目前是世界人口第二大国，2019年末总人口数13.687亿人。联合国《世界人口展望》2019年报告预计，大约在2027年左右，印度人口将会超过中国人口，成为世界人口最多的国家。 (177 chars) |
| Mitä voivodi tarkoittaa? (24 chars) | Voivodi Voivodi on slaavilainen arvonimi, joka alkuaan annettiin sotaa johtamaan valitulle päällikölle. Myöhemmin sitä on käytetty eräistä ruhtinaista Moldovassa, Puolassa, Transilvaniassa ja Valakiassa. Serbiassa ja Monteneg ... [truncated 225 chars](525 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMMTEB-v2 |
| Backing dataset | NanoMMTEB-v2 |
| Task / split | miracl |
| Hugging Face dataset | [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2) |
| Source dataset | [mteb/MIRACLRetrievalHardNegatives](https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives) |
| Language | multilingual |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 444 |
| Avg positives / query | 2.22 |
| Positives per query (min / median / max) | 1 / 2.0 / 8 |
| Queries with multiple positives | 155 (77.50%) |
| BM25 nDCG@10 | 0.5714 |
| BM25 hit@10 | 0.8400 |
| Query length avg chars | 37.22 |
| Document length avg chars | 448.21 |

### Public Sources

- [Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages](https://arxiv.org/abs/2210.09984).
- [MIRACL project page](https://project-miracl.github.io/).
- [mteb/MIRACLRetrievalHardNegatives](https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2)
- Source dataset: [mteb/MIRACLRetrievalHardNegatives](https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2023 | task paper | https://arxiv.org/abs/2210.09984 |
| MIRACL project page | 2023 | project page | https://project-miracl.github.io/ |
| mteb/MIRACLRetrievalHardNegatives | 2024 | dataset card | https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMMTEB-v2
  backing_dataset: NanoMMTEB-v2
  dataset_id: hakari-bench/NanoMMTEB-v2
  task_name: miracl
  split_name: miracl
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMMTEB-v2/miracl.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 444
  positives_per_query:
    average: 2.22
    min: 1
    median: 2.0
    max: 8
    multi_positive_queries: 155
    multi_positive_query_percent: 77.5
  text_stats_chars:
    query_mean: 37.215
    document_mean: 448.2123
  bm25:
    ndcg_at_10: 0.5713828743352728
    hit_at_10: 0.84
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: dev
    train_eval_overlap_audit: not_audited
    leakage_note: do not train on overlapping MIRACL dev/test queries, qrels, or positive passages
    useful_training_data:
      - MIRACL train splits
      - native-language Wikipedia retrieval pairs
      - multilingual QA retrieval data
      - same-language hard negatives
    synthetic_data:
      document_generation: native-language Wikipedia-style passages
      question_generation: natural information needs answerable from those passages
      answerability: positive passage should explicitly answer the query in the same language setting
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2
    source_urls:
      - label: MIRACL arXiv
        url: https://arxiv.org/abs/2210.09984
      - label: MIRACL project page
        url: https://project-miracl.github.io/
      - label: mteb/MIRACLRetrievalHardNegatives
        url: https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives
    source_notes: []
  references:
    - title: "Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages"
      url: https://arxiv.org/abs/2210.09984
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
```
