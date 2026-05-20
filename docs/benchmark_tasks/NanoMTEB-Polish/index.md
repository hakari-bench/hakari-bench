# NanoMTEB-Polish

> [!NOTE]
> This page was prepared by manual review of source papers, dataset cards,
> repository metadata, and sampled benchmark data. It may contain mistakes;
> please treat it as a reference aid rather than a definitive source.

## Overview

NanoMTEB-Polish is a compact Polish retrieval group dominated by translated
community-question duplicate retrieval. Ten of its fourteen subtasks are Polish
CQADupStack splits covering Android, English-language usage, GIS, Mathematica,
Physics, Programmers, Statistics, TeX, Webmasters, and WordPress. The remaining
tasks cover Polish financial QA retrieval, Natural Questions-style fact
retrieval, PUGG Polish Wikipedia QA retrieval, and Quora duplicate-question
retrieval.

The group is useful because it stresses Polish paraphrase and duplicate
retrieval across many technical domains. It also includes broader QA and finance
retrieval tasks, so it is not only a translated Stack Exchange benchmark.

## Details

### What the Original Group Measures

Most NanoMTEB-Polish tasks descend from BEIR or MTEB retrieval datasets adapted
to Polish. The CQADupStack family measures duplicate community-question
retrieval: given a question, rank other posts that ask the same or an equivalent
question. In the Polish splits, the original community QA domains are preserved
but the evaluated text is Polish, usually through CLARIN or MTEB Polish
packaging.

The non-CQADupStack splits add different retrieval shapes. FiQA retrieves
financial answer passages for finance questions. NQ-PLHardNegatives retrieves
Wikipedia-style answer passages for Polish fact questions. PUGG is a native
Polish QA/IR resource built from Polish Wikipedia-style passages. Quora-PL
retrieves duplicate short questions and is the most direct paraphrase-retrieval
task in the group.

### Subtask Coverage

The fourteen subtasks cover five retrieval families:

- **Polish technical duplicate retrieval:** Android, GIS, Mathematica, TeX,
  Webmasters, WordPress, Programmers, Statistics, Physics, and English-language
  usage CQADupStack splits.
- **Financial QA retrieval:** `fiqa` retrieves explanatory or opinionated
  financial answers.
- **Open-domain fact retrieval:** `nq` retrieves answer-bearing
  Wikipedia-style passages from Natural Questions-derived data.
- **Native Polish QA retrieval:** `pugg` retrieves Polish passages for short
  factoid questions.
- **Short duplicate-question retrieval:** `quora` retrieves Polish paraphrase
  question duplicates.

All splits are Polish in the current Nano group. The CQADupStack tasks often
contain translated technical tokens, code snippets, product names, formulas, or
Stack Exchange formatting, so robust models need both Polish language handling
and domain-specific terminology.

### Observed Group Profile

Across the fourteen splits, NanoMTEB-Polish contains 2,800 queries, 8,151
positive qrels, and 140,000 split-local candidate documents. Every split has
200 queries and 10,000 candidate documents. The document count is a sum across
subtasks, not a deduplicated group-wide corpus size. The average is 2.91
positives per query, and 1,002 queries have more than one positive.

Queries are short, with a query-weighted mean of 54.80 characters. Documents
are much longer for most CQADupStack and FiQA splits, averaging 807.31
characters overall, but Quora documents average only 64.64 characters because
they are short questions. Some CQADupStack splits have very large duplicate
clusters: several tasks have a maximum of 100 positives for one query.

### BM25 Difficulty

The query-weighted BM25 baseline reaches nDCG@10 = 0.3442 and hit@10 = 0.5064.
Because every split has 200 queries, the query-weighted and unweighted task
means are the same. The easiest split is `quora` with nDCG@10 = 0.7705 and
hit@10 = 0.9100, where short duplicate questions often share key words. `pugg`
is also strong at nDCG@10 = 0.6390 because many Polish fact questions include
distinctive entities or definitions.

BM25 is weakest on `cqadupstack_mathematica` with nDCG@10 = 0.2129, followed by
several CQADupStack technical domains. These tasks require duplicate-intent
matching rather than topical matching. The inspected examples show positives
often appearing at BM25 rank 90 to 100 even when the surface domain is correct:
Mathematica graph automorphisms, TeX package creation, WordPress enqueueing,
NQ accounting questions, and FiQA emergency-fund questions all require matching
the same underlying problem or answer relation, not only shared terms.

### Training Data That May Help

Useful training data includes non-overlapping Polish duplicate-question pairs,
translated or native Stack Exchange duplicates, Polish paraphrase data, Polish
technical QA, Polish Wikipedia QA retrieval, FiQA-style finance QA, and PUGG
training records. For the CQADupStack family, hard negatives should come from
the same technical site and share product names, function names, formulas,
packages, or terminology while asking a different question.

Training should exclude NanoMTEB-Polish evaluation queries, qrels, and positive
documents, plus upstream test records from the translated MTEB/CLARIN sources.
Duplicate-question benchmarks are especially leakage-sensitive because
memorizing duplicate clusters can directly improve retrieval scores.

### Synthetic Data Guidance

Synthetic data should preserve the duplicate or answer-retrieval shape of each
task. For CQADupStack-style data, generate Polish posts and duplicate questions
that describe the same technical problem with different wording, examples, or
software versions. For Quora-style data, keep questions short and paraphrastic.
For PUGG and NQ, generate answerable Polish fact questions from non-evaluation
Wikipedia passages. For FiQA, generate finance questions with explanatory
answers and caveats.

Hard negatives should be near duplicates in topic but not in intent: the same
LaTeX command with a different rendering issue, the same WordPress hook with a
different behavior, the same finance instrument with a different decision, or a
related entity passage that does not answer the question. Nano evaluation
queries and positive documents should not be used as seeds.

## Task Summary

| Task | Retrieval shape | Queries | Docs | Positive qrels | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars | Source status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [cqadupstack_android](cqadupstack_android.md) | Polish Android duplicate question retrieval | 200 | 10,000 | 809 | 0.3407 | 0.5100 | 59.26 | 626.68 | CQADupStack-PL + MTEB |
| [cqadupstack_english](cqadupstack_english.md) | Polish English-usage duplicate retrieval | 200 | 10,000 | 1,356 | 0.3188 | 0.4850 | 46.52 | 488.14 | CQADupStack-PL + MTEB |
| [cqadupstack_gis](cqadupstack_gis.md) | Polish GIS duplicate question retrieval | 200 | 10,000 | 313 | 0.2423 | 0.3800 | 60.61 | 965.97 | CQADupStack-PL + MTEB |
| [cqadupstack_mathematica](cqadupstack_mathematica.md) | Polish Mathematica duplicate retrieval | 200 | 10,000 | 506 | 0.2129 | 0.3550 | 50.41 | 1,088.52 | CQADupStack-PL + MTEB |
| [cqadupstack_physics](cqadupstack_physics.md) | Polish physics duplicate question retrieval | 200 | 10,000 | 621 | 0.3359 | 0.5450 | 58.80 | 814.74 | CQADupStack-PL + MTEB |
| [cqadupstack_programmers](cqadupstack_programmers.md) | Polish software-engineering duplicate retrieval | 200 | 10,000 | 634 | 0.3241 | 0.4700 | 59.12 | 1,075.30 | CQADupStack-PL + MTEB |
| [cqadupstack_stats](cqadupstack_stats.md) | Polish statistics duplicate question retrieval | 200 | 10,000 | 373 | 0.2662 | 0.3800 | 60.95 | 1,016.61 | CQADupStack-PL + MTEB |
| [cqadupstack_tex](cqadupstack_tex.md) | Polish TeX duplicate question retrieval | 200 | 10,000 | 843 | 0.2615 | 0.4350 | 50.30 | 1,106.13 | CQADupStack-PL + MTEB |
| [cqadupstack_webmasters](cqadupstack_webmasters.md) | Polish webmaster duplicate retrieval | 200 | 10,000 | 882 | 0.2550 | 0.3950 | 59.75 | 739.15 | CQADupStack-PL + MTEB |
| [cqadupstack_wordpress](cqadupstack_wordpress.md) | Polish WordPress duplicate retrieval | 200 | 10,000 | 344 | 0.3139 | 0.4250 | 55.80 | 1,040.60 | CQADupStack-PL + MTEB |
| [fiqa](fiqa.md) | Polish finance question to answer passage | 200 | 10,000 | 534 | 0.2353 | 0.4550 | 68.51 | 808.82 | FiQA + MTEB |
| [nq](nq.md) | Polish fact question to answer passage | 200 | 10,000 | 251 | 0.3021 | 0.5500 | 48.57 | 616.77 | NQ + MTEB |
| [pugg](pugg.md) | Polish factoid question to Wikipedia passage | 200 | 10,000 | 200 | 0.6390 | 0.7950 | 36.19 | 850.31 | PUGG paper |
| [quora](quora.md) | Polish duplicate short-question retrieval | 200 | 10,000 | 485 | 0.7705 | 0.9100 | 52.51 | 64.64 | Quora + MTEB |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Polish |
| Backing dataset | NanoMTEB-Polish |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish) |
| Language | pl |
| Category | natural_language |
| Subtasks | 14 |
| Total queries | 2,800 |
| Split-local documents | 140,000 |
| Positive qrels | 8,151 |
| Positives per query | 2.91 average |
| Multi-positive queries | 1,002 |
| Query-weighted BM25 nDCG@10 | 0.3442 |
| Query-weighted BM25 hit@10 | 0.5064 |
| Mean query length | 54.80 chars, weighted by query count |
| Mean document length | 807.31 chars, weighted by split-local document count |

### Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://ir.webis.de/anthology/2015.adcs_conference-2015.3/); 2015.
- [BEIR-PL: Zero Shot Information Retrieval Benchmark for the Polish Language](https://aclanthology.org/2024.lrec-main.194/); 2024.
- [FiQA challenge site](https://sites.google.com/view/fiqa/).
- [Natural Questions](https://ai.google.com/research/NaturalQuestions/).
- [Developing PUGG for Polish: A Modern Approach to KBQA, MRC, and IR Dataset Construction](https://aclanthology.org/2024.findings-acl.652/); 2024.
- [First Quora Dataset Release: Question Pairs](https://quoradata.quora.com/First-Quora-Dataset-Release-Question-Pairs).
- [Massive Text Embedding Benchmark (MTEB)](https://github.com/embeddings-benchmark/mteb).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish)
- Source dataset examples:
  [mteb/CQADupstack-Android-PL](https://huggingface.co/datasets/mteb/CQADupstack-Android-PL),
  [mteb/CQADupstack-English-PL](https://huggingface.co/datasets/mteb/CQADupstack-English-PL),
  [mteb/FiQA-PL](https://huggingface.co/datasets/mteb/FiQA-PL),
  [mteb/NQ-PLHardNegatives](https://huggingface.co/datasets/mteb/NQ-PLHardNegatives),
  [clarin-pl/PUGG_IR](https://huggingface.co/datasets/clarin-pl/PUGG_IR),
  [mteb/Quora-PLHardNegatives](https://huggingface.co/datasets/mteb/Quora-PLHardNegatives).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | source task paper | https://ir.webis.de/anthology/2015.adcs_conference-2015.3/ |
| BEIR-PL: Zero Shot Information Retrieval Benchmark for the Polish Language | 2024 | benchmark paper | https://aclanthology.org/2024.lrec-main.194/ |
| FiQA challenge site | 2018 | benchmark page | https://sites.google.com/view/fiqa/ |
| Natural Questions | 2019 | benchmark page | https://ai.google.com/research/NaturalQuestions/ |
| Developing PUGG for Polish: A Modern Approach to KBQA, MRC, and IR Dataset Construction | 2024 | source task paper | https://aclanthology.org/2024.findings-acl.652/ |
| First Quora Dataset Release: Question Pairs | 2017 | dataset page | https://quoradata.quora.com/First-Quora-Dataset-Release-Question-Pairs |
| Massive Text Embedding Benchmark (MTEB) | 2022 | benchmark repository | https://github.com/embeddings-benchmark/mteb |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoMTEB-Polish
  backing_dataset: NanoMTEB-Polish
  dataset_id: hakari-bench/NanoMTEB-Polish
  language: pl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Polish/index.md
  source_research:
    primary_source_type: multiple_dataset_cards_and_source_references
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 14
    queries: 2800
    split_local_documents: 140000
    positive_qrels: 8151
  positives_per_query:
    average: 2.9110714285714288
    min: 1
    median_task_median: 2.0
    max: 100
    multi_positive_tasks: 13
    multi_positive_queries: 1002
  text_stats_chars:
    query_mean_weighted_by_queries: 54.80464285714286
    document_mean_weighted_by_documents: 807.3122
  bm25:
    ndcg_at_10_query_weighted: 0.34415714285714283
    hit_at_10_query_weighted: 0.5064285714285715
    ndcg_at_10_unweighted_task_mean: 0.34415714285714283
    hit_at_10_unweighted_task_mean: 0.5064285714285715
    source: dataset_bm25_column
    easiest_task_by_ndcg_at_10: quora
    hardest_task_by_ndcg_at_10: cqadupstack_mathematica
  tasks:
    - name: cqadupstack_android
      path: docs/benchmark_tasks/NanoMTEB-Polish/cqadupstack_android.md
      retrieval_shape: polish_android_duplicate_question_retrieval
      queries: 200
      documents: 10000
      positive_qrels: 809
      bm25_ndcg_at_10: 0.3407
      bm25_hit_at_10: 0.51
    - name: cqadupstack_english
      path: docs/benchmark_tasks/NanoMTEB-Polish/cqadupstack_english.md
      retrieval_shape: polish_english_usage_duplicate_retrieval
      queries: 200
      documents: 10000
      positive_qrels: 1356
      bm25_ndcg_at_10: 0.3188
      bm25_hit_at_10: 0.485
    - name: cqadupstack_gis
      path: docs/benchmark_tasks/NanoMTEB-Polish/cqadupstack_gis.md
      retrieval_shape: polish_gis_duplicate_question_retrieval
      queries: 200
      documents: 10000
      positive_qrels: 313
      bm25_ndcg_at_10: 0.2423
      bm25_hit_at_10: 0.38
    - name: cqadupstack_mathematica
      path: docs/benchmark_tasks/NanoMTEB-Polish/cqadupstack_mathematica.md
      retrieval_shape: polish_mathematica_duplicate_retrieval
      queries: 200
      documents: 10000
      positive_qrels: 506
      bm25_ndcg_at_10: 0.2129
      bm25_hit_at_10: 0.355
    - name: cqadupstack_physics
      path: docs/benchmark_tasks/NanoMTEB-Polish/cqadupstack_physics.md
      retrieval_shape: polish_physics_duplicate_question_retrieval
      queries: 200
      documents: 10000
      positive_qrels: 621
      bm25_ndcg_at_10: 0.3359
      bm25_hit_at_10: 0.545
    - name: cqadupstack_programmers
      path: docs/benchmark_tasks/NanoMTEB-Polish/cqadupstack_programmers.md
      retrieval_shape: polish_software_engineering_duplicate_retrieval
      queries: 200
      documents: 10000
      positive_qrels: 634
      bm25_ndcg_at_10: 0.3241
      bm25_hit_at_10: 0.47
    - name: cqadupstack_stats
      path: docs/benchmark_tasks/NanoMTEB-Polish/cqadupstack_stats.md
      retrieval_shape: polish_statistics_duplicate_question_retrieval
      queries: 200
      documents: 10000
      positive_qrels: 373
      bm25_ndcg_at_10: 0.2662
      bm25_hit_at_10: 0.38
    - name: cqadupstack_tex
      path: docs/benchmark_tasks/NanoMTEB-Polish/cqadupstack_tex.md
      retrieval_shape: polish_tex_duplicate_question_retrieval
      queries: 200
      documents: 10000
      positive_qrels: 843
      bm25_ndcg_at_10: 0.2615
      bm25_hit_at_10: 0.435
    - name: cqadupstack_webmasters
      path: docs/benchmark_tasks/NanoMTEB-Polish/cqadupstack_webmasters.md
      retrieval_shape: polish_webmaster_duplicate_retrieval
      queries: 200
      documents: 10000
      positive_qrels: 882
      bm25_ndcg_at_10: 0.255
      bm25_hit_at_10: 0.395
    - name: cqadupstack_wordpress
      path: docs/benchmark_tasks/NanoMTEB-Polish/cqadupstack_wordpress.md
      retrieval_shape: polish_wordpress_duplicate_retrieval
      queries: 200
      documents: 10000
      positive_qrels: 344
      bm25_ndcg_at_10: 0.3139
      bm25_hit_at_10: 0.425
    - name: fiqa
      path: docs/benchmark_tasks/NanoMTEB-Polish/fiqa.md
      retrieval_shape: polish_finance_question_to_answer_passage
      queries: 200
      documents: 10000
      positive_qrels: 534
      bm25_ndcg_at_10: 0.2353
      bm25_hit_at_10: 0.455
    - name: nq
      path: docs/benchmark_tasks/NanoMTEB-Polish/nq.md
      retrieval_shape: polish_fact_question_to_answer_passage
      queries: 200
      documents: 10000
      positive_qrels: 251
      bm25_ndcg_at_10: 0.3021
      bm25_hit_at_10: 0.55
    - name: pugg
      path: docs/benchmark_tasks/NanoMTEB-Polish/pugg.md
      retrieval_shape: polish_factoid_question_to_wikipedia_passage
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.639
      bm25_hit_at_10: 0.795
    - name: quora
      path: docs/benchmark_tasks/NanoMTEB-Polish/quora.md
      retrieval_shape: polish_duplicate_short_question_retrieval
      queries: 200
      documents: 10000
      positive_qrels: 485
      bm25_ndcg_at_10: 0.7705
      bm25_hit_at_10: 0.91
  learning:
    leakage_note: exclude NanoMTEB-Polish evaluation queries, qrels, positive documents, and upstream translated test duplicate clusters from training
    useful_training_data:
      - Polish duplicate-question and paraphrase retrieval pairs
      - translated or native Stack Exchange duplicate question pairs
      - Polish technical QA in Android, GIS, Mathematica, TeX, WordPress, and webmaster domains
      - Polish Wikipedia QA retrieval and PUGG training data
      - FiQA-style financial question-answer retrieval
      - hard negatives from the same forum, entity family, or finance topic
    synthetic_data:
      document_generation: Polish technical posts, finance answers, Wikipedia passages, and short duplicate questions in source-like style
      question_generation: duplicate Polish questions, factoid questions, finance questions, and technical troubleshooting questions grounded in generated or selected documents
      answerability: positives must preserve duplicate intent or answer evidence, not only broad topic overlap
    multi_positive_training: preserve_duplicate_clusters_and_multi_positive_qrels
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish
    source_urls:
      - label: CQADupStack paper
        url: https://ir.webis.de/anthology/2015.adcs_conference-2015.3/
      - label: BEIR-PL ACL Anthology
        url: https://aclanthology.org/2024.lrec-main.194/
      - label: FiQA challenge
        url: https://sites.google.com/view/fiqa/
      - label: Natural Questions
        url: https://ai.google.com/research/NaturalQuestions/
      - label: PUGG paper
        url: https://aclanthology.org/2024.findings-acl.652/
      - label: Quora Question Pairs
        url: https://quoradata.quora.com/First-Quora-Dataset-Release-Question-Pairs
      - label: MTEB repository
        url: https://github.com/embeddings-benchmark/mteb
    source_notes: []
  references:
    - title: "CQADupStack: A Benchmark Data Set for Community Question-Answering Research"
      url: https://ir.webis.de/anthology/2015.adcs_conference-2015.3/
      year: 2015
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "BEIR-PL: Zero Shot Information Retrieval Benchmark for the Polish Language"
      url: https://aclanthology.org/2024.lrec-main.194/
      year: 2024
      is_paper: true
      source_confidence: definitive_paper_link
    - title: FiQA challenge site
      url: https://sites.google.com/view/fiqa/
      year: 2018
      is_paper: false
      source_confidence: benchmark_page
    - title: Natural Questions
      url: https://ai.google.com/research/NaturalQuestions/
      year: 2019
      is_paper: false
      source_confidence: benchmark_page
    - title: "Developing PUGG for Polish: A Modern Approach to KBQA, MRC, and IR Dataset Construction"
      url: https://aclanthology.org/2024.findings-acl.652/
      year: 2024
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "First Quora Dataset Release: Question Pairs"
      url: https://quoradata.quora.com/First-Quora-Dataset-Release-Question-Pairs
      year: 2017
      is_paper: false
      source_confidence: dataset_source_reference
```
