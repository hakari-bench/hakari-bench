# NanoBIRCO

## Overview

NanoBIRCO is the compact Nano version of BIRCO, a benchmark built around
retrieval tasks with complex objectives. Unlike many short-query retrieval
benchmarks, BIRCO queries are often paragraph-length descriptions of a goal:
refute this argument, find clinical trials for this patient, retrieve research
abstracts for this nuanced need, recover a masked literary quotation, or identify
a book from a vague memory. NanoBIRCO keeps that emphasis in five smaller
English subtasks.

The group is useful because every subtask asks for more than topical similarity.
A topically related passage can still be wrong if it does not counter the
argument, satisfy trial eligibility, match the research objective, provide the
missing quotation, or identify the remembered book.

## Details

### What the Original Group Measures

[BIRCO: A Benchmark of Information Retrieval Tasks with Complex Objectives](https://arxiv.org/abs/2402.14151)
frames retrieval as objective satisfaction rather than generic semantic
matching. NanoBIRCO carries over five BIRCO task families: ArguAna-style
counterargument retrieval, clinical-trial matching, DORIS-MAE scientific
abstract retrieval, RELIC literary quotation retrieval, and WhatsThatBook book
identification.

The shared pattern is that query text is rich and often underspecified. Clinical
trial matching has to interpret patient criteria and exclusions. RELIC has to
connect literary analysis around a masked quotation to the original passage.
WhatsThatBook asks the retriever to resolve incomplete memories of plot,
characters, or setting. These objectives make the benchmark sensitive to
reasoning over constraints and descriptions, not just matching rare words.

### Subtask Coverage

- **NanoBIRCOArguAna:** long debate arguments retrieving counterarguments that
  directly challenge the query stance.
- **NanoBIRCOClinicalTrial:** patient case reports retrieving eligible or
  relevant clinical-trial records.
- **NanoBIRCODorisMae:** paragraph-length scientific research needs retrieving
  matching abstracts.
- **NanoBIRCORelic:** literary analysis with masked quotations retrieving the
  missing literary quotation or source passage.
- **NanoBIRCOWTB:** vague user memories retrieving the intended book in the
  WhatsThatBook setting.

All tasks are English natural-language retrieval tasks. ArguAna, RELIC, and WTB
are single-positive in the Nano qrels, while ClinicalTrial and DORIS-MAE contain
many multi-positive queries.

### Observed Group Profile

The five task pages report 408 queries, 2,909 positive qrels, and 18,789
split-local candidate documents. Query text is long across the whole group:
the query-count-weighted average is 925.24 characters, and every subtask averages
roughly 497 characters or more. `NanoBIRCOArguAna`, `NanoBIRCORelic`, and
`NanoBIRCODorisMae` all average around one thousand query characters.

Documents average 988.13 characters when weighted by split-local document count.
`NanoBIRCORelic` has shorter documents than the other subtasks, while
clinical-trial, scientific, and argument documents are typically paragraph-scale
or longer. The group has 65 multi-positive queries, concentrated in the
ClinicalTrial and DORIS-MAE style tasks.

### BM25 Difficulty

NanoBIRCO is lexically difficult. Using the dataset-provided BM25 candidate
columns, query-weighted BM25 nDCG@10 is 0.1822 and hit@10 is 0.3750. The strongest
subtask is `NanoBIRCOArguAna` (nDCG@10 = 0.4051, hit@10 = 0.7551), where long
arguments and counterarguments often share topical vocabulary. The weakest
subtasks are `NanoBIRCORelic` (0.0633, 0.1200) and `NanoBIRCOWTB` (0.0751,
0.1100), where the target depends on missing quotations or fuzzy book memories.

The group therefore measures whether a retriever can use constraints, stance,
genre, and implicit clues. BM25 can retrieve topical neighbors, but it often
cannot tell whether a document actually fulfills the query's objective.

### Training Data That May Help

Useful training data includes non-overlapping BIRCO-style objective retrieval
pairs, argument-counterargument data, clinical trial eligibility matching data,
scientific abstract recommendation or review-search data, literary quotation
and citation retrieval, and book-description or recommendation search data.
ClinicalTrial and DORIS-MAE should be trained with multi-positive objectives when
possible, because many queries can have several valid documents.

Training should exclude NanoBIRCO evaluation queries, qrels, and positive
documents. Since BIRCO tasks are small and source-specific, public source splits
should be checked carefully for overlap before being used for supervised
training.

### Synthetic Data Guidance

Synthetic data should preserve the objective behind each query. Generate long
queries with explicit constraints, missing information, or stance requirements,
then pair them with documents that actually satisfy those requirements. For
clinical-trial data, include inclusion and exclusion criteria. For literary and
book-memory tasks, include partial, noisy, or indirect clues. For argument data,
make the positive a counterargument rather than a same-topic passage.

Negatives should be close enough to share surface vocabulary but fail a key
objective: a trial excludes the patient, an abstract studies a related but wrong
condition, a book has a similar setting but different plot, or an argument agrees
with the query instead of rebutting it.

## Task Summary

| Task | Retrieval focus | Queries | Docs | Positive qrels | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| [NanoBIRCOArguAna](NanoBIRCOArguAna.md) | argument to counterargument | 98 | 3,081 | 98 | 0.4051 | 0.7551 | 1,123.99 | 1,140.06 |
| [NanoBIRCOClinicalTrial](NanoBIRCOClinicalTrial.md) | patient case to clinical trial | 50 | 3,375 | 1,042 | 0.1194 | 0.6200 | 497.02 | 1,174.27 |
| [NanoBIRCODorisMae](NanoBIRCODorisMae.md) | research need to scientific abstract | 60 | 5,544 | 1,569 | 0.2469 | 0.4167 | 995.48 | 1,220.29 |
| [NanoBIRCORelic](NanoBIRCORelic.md) | literary context to missing quotation | 100 | 5,023 | 100 | 0.0633 | 0.1200 | 1,016.30 | 477.33 |
| [NanoBIRCOWTB](NanoBIRCOWTB.md) | vague memory to book | 100 | 1,766 | 100 | 0.0751 | 0.1100 | 811.30 | 1,091.25 |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBIRCO |
| Backing dataset | NanoBIRCO |
| Hugging Face dataset | [hakari-bench/NanoBIRCO](https://huggingface.co/datasets/hakari-bench/NanoBIRCO) |
| Language | en |
| Category | natural language |
| Subtasks | 5 |
| Total queries | 408 |
| Split-local documents | 18,789 |
| Positive qrels | 2,909 |
| Average positives / query | 7.13 |
| Queries with multiple positives | 65 |
| Query-weighted BM25 nDCG@10 | 0.1822 |
| Query-weighted BM25 hit@10 | 0.3750 |
| Mean query length | 925.24 chars, weighted by query count |
| Mean document length | 988.13 chars, weighted by split-local document count |

### Public Sources

- [BIRCO: A Benchmark of Information Retrieval Tasks with Complex Objectives](https://arxiv.org/abs/2402.14151); 2024; DOI: `10.48550/arXiv.2402.14151`.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBIRCO](https://huggingface.co/datasets/hakari-bench/NanoBIRCO)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| BIRCO: A Benchmark of Information Retrieval Tasks with Complex Objectives | 2024 | benchmark paper | https://arxiv.org/abs/2402.14151 |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoBIRCO
  backing_dataset: NanoBIRCO
  dataset_id: hakari-bench/NanoBIRCO
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBIRCO/index.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 5
    queries: 408
    split_local_documents: 18789
    positive_qrels: 2909
  positives_per_query:
    average: 7.129901960784314
    min: 1
    median: 1.0
    max: 100
    multi_positive_tasks: 2
    multi_positive_queries: 65
  text_stats_chars:
    query_mean_weighted_by_queries: 925.2377450686275
    document_mean_weighted_by_documents: 988.1341209377294
  bm25:
    ndcg_at_10_query_weighted: 0.182175196075
    hit_at_10_query_weighted: 0.3750000000009804
    source: dataset_bm25_column
    strongest_task_by_ndcg_at_10: NanoBIRCOArguAna
    weakest_task_by_ndcg_at_10: NanoBIRCORelic
  tasks:
    - name: NanoBIRCOArguAna
      path: docs/benchmark_tasks/NanoBIRCO/NanoBIRCOArguAna.md
      retrieval_focus: argument_to_counterargument
      queries: 98
      documents: 3081
      positive_qrels: 98
      bm25_ndcg_at_10: 0.4051
      bm25_hit_at_10: 0.7551
    - name: NanoBIRCOClinicalTrial
      path: docs/benchmark_tasks/NanoBIRCO/NanoBIRCOClinicalTrial.md
      retrieval_focus: patient_case_to_clinical_trial
      queries: 50
      documents: 3375
      positive_qrels: 1042
      bm25_ndcg_at_10: 0.1194
      bm25_hit_at_10: 0.62
    - name: NanoBIRCODorisMae
      path: docs/benchmark_tasks/NanoBIRCO/NanoBIRCODorisMae.md
      retrieval_focus: research_need_to_scientific_abstract
      queries: 60
      documents: 5544
      positive_qrels: 1569
      bm25_ndcg_at_10: 0.2469
      bm25_hit_at_10: 0.4167
    - name: NanoBIRCORelic
      path: docs/benchmark_tasks/NanoBIRCO/NanoBIRCORelic.md
      retrieval_focus: literary_context_to_missing_quotation
      queries: 100
      documents: 5023
      positive_qrels: 100
      bm25_ndcg_at_10: 0.0633
      bm25_hit_at_10: 0.12
    - name: NanoBIRCOWTB
      path: docs/benchmark_tasks/NanoBIRCO/NanoBIRCOWTB.md
      retrieval_focus: vague_memory_to_book
      queries: 100
      documents: 1766
      positive_qrels: 100
      bm25_ndcg_at_10: 0.0751
      bm25_hit_at_10: 0.11
  learning:
    leakage_note: exclude NanoBIRCO evaluation queries, qrels, and positive documents; audit BIRCO source overlap before training
    useful_training_data:
      - BIRCO-style objective retrieval pairs
      - argument-counterargument retrieval data
      - clinical trial eligibility matching data
      - scientific abstract recommendation and review-search data
      - literary quotation retrieval data
      - book-description and recommendation search data
    synthetic_data:
      document_generation: trial records, abstracts, counterarguments, literary passages, and book descriptions with explicit objective-satisfying details
      question_generation: long natural-language objectives with constraints, missing information, stance, or vague memory clues
      answerability: positives must satisfy the stated objective, not only share topic vocabulary
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBIRCO
    source_urls:
      - label: BIRCO arXiv
        url: https://arxiv.org/abs/2402.14151
  references:
    - title: "BIRCO: A Benchmark of Information Retrieval Tasks with Complex Objectives"
      url: https://arxiv.org/abs/2402.14151
      year: 2024
      doi: 10.48550/arXiv.2402.14151
      is_paper: true
      source_confidence: definitive_paper_link
```
