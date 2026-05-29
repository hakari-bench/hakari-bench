# NanoBRIGHT

## Overview

NanoBRIGHT is the Nano task group for BRIGHT, a reasoning-intensive retrieval
benchmark. It covers twenty English retrieval splits drawn from mathematical
problem solving, theorem-based STEM reasoning, programming tasks, StackExchange
question answering, and long-document web retrieval.

The BRIGHT paper frames these tasks as retrieval problems where ordinary
keyword or semantic similarity is not enough. NanoBRIGHT keeps that premise in
compact form: the positive document may share the same theorem, algorithm,
mechanism, cited source, or problem-solving skill without paraphrasing the
query. The group is therefore useful for testing whether a retriever can find
evidence that supports a reasoning step, not only text that looks topically
similar.

## Details

### What the Original Group Measures

[BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval](https://arxiv.org/abs/2407.12883)
introduces BRIGHT to test retrieval settings where keyword or ordinary semantic
matching is not enough. The paper describes queries from naturally occurring or
carefully curated human data, including StackExchange posts, AoPS math problems,
LeetCode problems, Pony programming exercises, and TheoremQA-derived questions.
The intended retrieval target is a document useful for solving or supporting the
query, not necessarily a document that repeats the query wording.

The NanoBRIGHT group preserves that design in compact form. AoPS retrieves
problems that share the same mathematical skill. LeetCode retrieves solved
programming problems with related algorithmic structure. TheoremQAQuestions
retrieves solved STEM problems that use the same theorem, while
TheoremQATheorems retrieves formal theorem statements. The StackExchange-style
tasks retrieve cited or validated supporting pages, and the paired long-document
variants retrieve the full source pages instead of short passage chunks.

### Subtask Coverage

The twenty subtasks fall into four retrieval families:

- **Mathematical and theorem reasoning:** `NanoBrightAops`,
  `NanoBrightTheoremQAQuestions`, and `NanoBrightTheoremQATheorems` test whether
  retrieval can connect applied or contest-style problems to the same theorem,
  proof idea, or problem-solving skill.
- **Programming and code reasoning:** `NanoBrightLeetcode`, `NanoBrightPony`,
  and `NanoBrightPonyLong` test algorithmic similarity and language-specific
  programming evidence, including a long-document variant for Pony reference
  material.
- **StackExchange evidence retrieval:** Biology, Earth Science, Economics,
  Psychology, Robotics, Stack Overflow, and Sustainable Living splits use user
  questions as queries and cited or validated supporting web passages as
  positives.
- **Long-document evidence retrieval:** the `Long` variants for the
  StackExchange domains retrieve complete cited source pages. These have far
  fewer candidate documents than the passage tasks, but the documents can be
  tens of thousands of characters long.

This mixture makes NanoBRIGHT a group-level probe for reasoning-aware
retrieval. A strong model should not only match entities or technical terms; it
should connect a problem to the mechanism, theorem, algorithm, documentation
section, or cited evidence that actually resolves it.

### Observed Group Profile

Across the twenty splits, NanoBRIGHT contains 2,245 queries, 9,287 positive
qrels, and 121,771 split-local candidate documents. The document count is a sum
over split-local pools, not a deduplicated corpus size. All splits are labeled
English. Every split has at least some multi-positive queries, and the group
average is 4.14 positives per query. The global median is 2 positives per query,
but the distribution is uneven: many long-document and theorem splits are close
to single-positive, while `NanoBrightPony` averages 19.81 positives per query
and `NanoBrightEconomics` contains one query with 85 positives.

The observed query shapes are intentionally diverse. AoPS and TheoremQA queries
are compact mathematical scenarios. LeetCode queries are long programming
problem statements averaging 1,459.30 characters. Robotics and Stack Overflow
queries can include logs, code, package names, and environment details, with
Robotics averaging 2,179.45 query characters. The long-document variants have
much longer documents: EarthScienceLong averages 70,649.63 characters per
document and StackoverflowLong averages 77,578.44 characters.

### BM25 Difficulty

The query-weighted BM25 nDCG@10 across NanoBRIGHT is 0.2156, with
query-weighted hit@10 of 0.4454. This is low for a group with many technical
terms, and it matches the BRIGHT paper's motivation: many positives are relevant
because they share a reasoning path rather than surface wording.

The task-level spread is large. `NanoBrightTheoremQATheorems` is the hardest
split by nDCG@10, with BM25 nDCG@10 = 0.0123 and hit@10 = 0.0263; applied
scenario queries rarely look like formal theorem statements. `NanoBrightPony`
is also very difficult for nDCG@10 despite many positives, because short Pony
programming tasks can share basic programming vocabulary with many wrong
documents. `NanoBrightEarthScienceLong` is the easiest split by nDCG@10
(0.3282), but even there BM25 finds a positive in the top ten for only about
half of the queries. Long-document splits sometimes improve hit rate because
they collapse passage-level evidence into fewer full pages, but they also add
large amounts of boilerplate and unrelated context.

### Training Data That May Help

Useful training data should be selected by reasoning family. For the
mathematical splits, use non-overlapping theorem-labeled solved problems,
contest math problem families, and proof-skill retrieval pairs. For programming
splits, use algorithm-problem similarity data, documentation retrieval,
language-reference QA, and code tasks with hard negatives from the same API or
algorithm family. For StackExchange evidence retrieval, use question-to-cited
source pairs, scientific or technical QA with references, and web evidence
retrieval data where the document supports the answer instead of merely
containing an answer string.

Training must exclude NanoBRIGHT evaluation queries, positives, qrels, and
source pages. For public BRIGHT-derived or source datasets, upstream examples
that overlap with the Nano evaluation splits should be removed unless an
explicit overlap audit has been performed. The long-document variants are
especially sensitive to leakage because a full cited page can contain many
passages related to several evaluation questions.

### Synthetic Data Guidance

Synthetic data for NanoBRIGHT should preserve the hidden reasoning relation.
For math and theorem tasks, generate applied scenarios and positive solved
problems or theorem statements that share the same theorem without reusing the
same story. For programming tasks, generate realistic problem statements and
positive solutions or documentation pages where relevance depends on the
algorithm, language feature, or API behavior. For StackExchange tasks, generate
questions with enough context to require evidence retrieval, then pair them with
source-like passages that support the mechanism or cited claim.

Hard negatives should be close in domain and vocabulary but wrong in the key
reasoning step. A biology negative can mention the same organism but explain a
different mechanism; a theorem negative can use the same mathematical objects
but require a different theorem; a Stack Overflow negative can be from the same
library but not resolve the reported behavior. Avoid using NanoBRIGHT query or
positive text as seeds for synthetic generation.

## Task Summary

| Task | Retrieval shape | Queries | Docs | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars | Source status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [NanoBrightAops](NanoBrightAops.md) | math problem to same-skill problem | 111 | 10,000 | 0.1443 | 0.5225 | 319.61 | 549.07 | BRIGHT paper |
| [NanoBrightBiology](NanoBrightBiology.md) | Biology question to cited passage | 103 | 10,000 | 0.2489 | 0.5049 | 523.03 | 473.93 | BRIGHT paper |
| [NanoBrightBiologyLong](NanoBrightBiologyLong.md) | Biology question to full cited page | 103 | 498 | 0.2540 | 0.4466 | 523.03 | 36,923.73 | BRIGHT paper |
| [NanoBrightEarthScience](NanoBrightEarthScience.md) | Earth Science question to cited passage | 116 | 10,000 | 0.3163 | 0.6552 | 476.71 | 716.25 | BRIGHT paper |
| [NanoBrightEarthScienceLong](NanoBrightEarthScienceLong.md) | Earth Science question to full cited page | 116 | 587 | 0.3282 | 0.5345 | 476.71 | 70,649.63 | BRIGHT paper |
| [NanoBrightEconomics](NanoBrightEconomics.md) | Economics question to cited passage | 103 | 10,000 | 0.2160 | 0.4466 | 739.57 | 532.57 | BRIGHT paper |
| [NanoBrightEconomicsLong](NanoBrightEconomicsLong.md) | Economics question to full cited page | 103 | 515 | 0.2510 | 0.3592 | 739.57 | 38,615.97 | BRIGHT paper |
| [NanoBrightLeetcode](NanoBrightLeetcode.md) | programming problem to algorithmically similar problem | 142 | 10,000 | 0.2705 | 0.5915 | 1,459.30 | 1,079.62 | BRIGHT paper |
| [NanoBrightPony](NanoBrightPony.md) | Pony task to supporting passage | 112 | 6,183 | 0.0362 | 0.2946 | 388.97 | 306.50 | BRIGHT paper |
| [NanoBrightPonyLong](NanoBrightPonyLong.md) | Pony task to full reference document | 112 | 577 | 0.2674 | 0.9464 | 388.97 | 3,553.13 | BRIGHT paper |
| [NanoBrightPsychology](NanoBrightPsychology.md) | Psychology question to cited passage | 101 | 10,000 | 0.1475 | 0.3168 | 693.16 | 504.47 | BRIGHT paper |
| [NanoBrightPsychologyLong](NanoBrightPsychologyLong.md) | Psychology question to full cited page | 101 | 509 | 0.2270 | 0.3366 | 693.16 | 40,097.47 | BRIGHT paper |
| [NanoBrightRobotics](NanoBrightRobotics.md) | Robotics question to cited passage | 101 | 10,000 | 0.0888 | 0.2376 | 2,179.45 | 382.35 | BRIGHT paper |
| [NanoBrightRoboticsLong](NanoBrightRoboticsLong.md) | Robotics question to full cited page | 101 | 505 | 0.2193 | 0.3465 | 2,179.45 | 35,895.20 | BRIGHT paper |
| [NanoBrightStackoverflow](NanoBrightStackoverflow.md) | developer question to cited technical passage | 117 | 10,000 | 0.2043 | 0.3932 | 1,292.97 | 1,120.63 | BRIGHT paper |
| [NanoBrightStackoverflowLong](NanoBrightStackoverflowLong.md) | developer question to full technical page | 117 | 1,846 | 0.3084 | 0.5214 | 1,292.97 | 77,578.44 | BRIGHT paper |
| [NanoBrightSustainableLiving](NanoBrightSustainableLiving.md) | sustainability question to cited passage | 108 | 10,000 | 0.2845 | 0.5185 | 682.84 | 733.62 | BRIGHT paper |
| [NanoBrightSustainableLivingLong](NanoBrightSustainableLivingLong.md) | sustainability question to full cited page | 108 | 551 | 0.3038 | 0.4815 | 682.84 | 38,204.30 | BRIGHT paper |
| [NanoBrightTheoremQAQuestions](NanoBrightTheoremQAQuestions.md) | applied theorem scenario to same-theorem problem | 194 | 10,000 | 0.1416 | 0.2990 | 425.64 | 543.43 | BRIGHT paper |
| [NanoBrightTheoremQATheorems](NanoBrightTheoremQATheorems.md) | applied theorem scenario to formal theorem | 76 | 10,000 | 0.0123 | 0.0263 | 415.62 | 401.12 | BRIGHT paper |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBRIGHT |
| Backing dataset | NanoBRIGHT |
| Hugging Face dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |
| Language | en |
| Category | natural_language |
| Subtasks | 20 |
| Total queries | 2,245 |
| Split-local documents | 121,771 |
| Positive qrels | 9,287 |
| Positives per query | avg 4.14, min 1, median 2, max 85 |
| Multi-positive queries | 1,234 (54.97%) |
| Query-weighted BM25 nDCG@10 | 0.2792 |
| Query-weighted BM25 hit@10 | 0.5318 |
| Query-weighted BM25 Recall@100 | 0.6539 |
| Query-weighted Dense nDCG@10 | 0.3736 |
| Query-weighted Dense hit@10 | 0.6343 |
| Query-weighted Dense Recall@100 | 0.7155 |
| Query-weighted Reranking hybrid nDCG@10 | 0.3635 |
| Query-weighted Reranking hybrid hit@10 | 0.6566 |
| Query-weighted Reranking hybrid Recall@100 | 0.7625 |
| Mean query length | 821.82 chars, weighted by query count |
| Mean document length | 2,930.58 chars, weighted by split-local document count |

### Public Sources

- [BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval](https://arxiv.org/abs/2407.12883); 2024; Hongjin Su et al.; DOI: `10.48550/arXiv.2407.12883`.
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

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoBRIGHT
  backing_dataset: NanoBRIGHT
  dataset_id: hakari-bench/NanoBRIGHT
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBRIGHT/index.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 20
    queries: 2245
    split_local_documents: 121771
    positive_qrels: 9287
  positives_per_query:
    average: 4.136748329621381
    min: 1
    median: 2
    max: 85
    multi_positive_tasks: 20
    multi_positive_queries: 1234
    multi_positive_query_percent: 54.96659242761692
  text_stats_chars:
    query_mean_weighted_by_queries: 821.8240534521158
    document_mean_weighted_by_documents: 2930.579086974731
  bm25:
    ndcg_at_10_query_weighted: 0.2791868132
    hit_at_10_query_weighted: 0.5318485523
    ndcg_at_10_unweighted_task_mean: 0.2135341449588916
    hit_at_10_unweighted_task_mean: 0.4389759255612618
    source: dataset_candidate_subset
    easiest_task_by_ndcg_at_10: NanoBrightEarthScienceLong
    hardest_task_by_ndcg_at_10: NanoBrightTheoremQATheorems
  tasks:
  - name: NanoBrightAops
    path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightAops.md
    retrieval_shape: math_problem_to_same_skill_problem
    queries: 111
    documents: 10000
    positive_qrels: 524
    bm25_ndcg_at_10: 0.14432700131414306
    bm25_hit_at_10: 0.5225225225225225
  - name: NanoBrightBiology
    path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightBiology.md
    retrieval_shape: biology_question_to_cited_passage
    queries: 103
    documents: 10000
    positive_qrels: 372
    bm25_ndcg_at_10: 0.2489409555054503
    bm25_hit_at_10: 0.5048543689320388
  - name: NanoBrightBiologyLong
    path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightBiologyLong.md
    retrieval_shape: biology_question_to_full_cited_page
    queries: 103
    documents: 498
    positive_qrels: 134
    bm25_ndcg_at_10: 0.2540185992266564
    bm25_hit_at_10: 0.44660194174757284
  - name: NanoBrightEarthScience
    path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightEarthScience.md
    retrieval_shape: earth_science_question_to_cited_passage
    queries: 116
    documents: 10000
    positive_qrels: 579
    bm25_ndcg_at_10: 0.31634958706490335
    bm25_hit_at_10: 0.6551724137931034
  - name: NanoBrightEarthScienceLong
    path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightEarthScienceLong.md
    retrieval_shape: earth_science_question_to_full_cited_page
    queries: 116
    documents: 587
    positive_qrels: 186
    bm25_ndcg_at_10: 0.3282261995195742
    bm25_hit_at_10: 0.5344827586206896
  - name: NanoBrightEconomics
    path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightEconomics.md
    retrieval_shape: economics_question_to_cited_passage
    queries: 103
    documents: 10000
    positive_qrels: 800
    bm25_ndcg_at_10: 0.2159843773721903
    bm25_hit_at_10: 0.44660194174757284
  - name: NanoBrightEconomicsLong
    path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightEconomicsLong.md
    retrieval_shape: economics_question_to_full_cited_page
    queries: 103
    documents: 515
    positive_qrels: 109
    bm25_ndcg_at_10: 0.25101039352381815
    bm25_hit_at_10: 0.3592233009708738
  - name: NanoBrightLeetcode
    path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightLeetcode.md
    retrieval_shape: programming_problem_to_algorithmically_similar_problem
    queries: 142
    documents: 10000
    positive_qrels: 262
    bm25_ndcg_at_10: 0.270523544902632
    bm25_hit_at_10: 0.5915492957746479
  - name: NanoBrightPony
    path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightPony.md
    retrieval_shape: pony_task_to_supporting_passage
    queries: 112
    documents: 6183
    positive_qrels: 2219
    bm25_ndcg_at_10: 0.036171605156298615
    bm25_hit_at_10: 0.29464285714285715
  - name: NanoBrightPonyLong
    path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightPonyLong.md
    retrieval_shape: pony_task_to_full_reference_document
    queries: 112
    documents: 577
    positive_qrels: 769
    bm25_ndcg_at_10: 0.267432389671051
    bm25_hit_at_10: 0.9464285714285714
  - name: NanoBrightPsychology
    path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightPsychology.md
    retrieval_shape: psychology_question_to_cited_passage
    queries: 101
    documents: 10000
    positive_qrels: 692
    bm25_ndcg_at_10: 0.14754529592509114
    bm25_hit_at_10: 0.31683168316831684
  - name: NanoBrightPsychologyLong
    path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightPsychologyLong.md
    retrieval_shape: psychology_question_to_full_cited_page
    queries: 101
    documents: 509
    positive_qrels: 116
    bm25_ndcg_at_10: 0.22701053658053216
    bm25_hit_at_10: 0.33663366336633666
  - name: NanoBrightRobotics
    path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightRobotics.md
    retrieval_shape: robotics_question_to_cited_passage
    queries: 101
    documents: 10000
    positive_qrels: 518
    bm25_ndcg_at_10: 0.08879149656934751
    bm25_hit_at_10: 0.2376237623762376
  - name: NanoBrightRoboticsLong
    path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightRoboticsLong.md
    retrieval_shape: robotics_question_to_full_cited_page
    queries: 101
    documents: 505
    positive_qrels: 106
    bm25_ndcg_at_10: 0.21929135808585956
    bm25_hit_at_10: 0.3465346534653465
  - name: NanoBrightStackoverflow
    path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightStackoverflow.md
    retrieval_shape: developer_question_to_cited_technical_passage
    queries: 117
    documents: 10000
    positive_qrels: 478
    bm25_ndcg_at_10: 0.2043421382260914
    bm25_hit_at_10: 0.39316239316239315
  - name: NanoBrightStackoverflowLong
    path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightStackoverflowLong.md
    retrieval_shape: developer_question_to_full_technical_page
    queries: 117
    documents: 1846
    positive_qrels: 129
    bm25_ndcg_at_10: 0.308370058146309
    bm25_hit_at_10: 0.5213675213675214
  - name: NanoBrightSustainableLiving
    path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightSustainableLiving.md
    retrieval_shape: sustainability_question_to_cited_passage
    queries: 108
    documents: 10000
    positive_qrels: 575
    bm25_ndcg_at_10: 0.2845443821290713
    bm25_hit_at_10: 0.5185185185185185
  - name: NanoBrightSustainableLivingLong
    path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightSustainableLivingLong.md
    retrieval_shape: sustainability_question_to_full_cited_page
    queries: 108
    documents: 551
    positive_qrels: 129
    bm25_ndcg_at_10: 0.30381074672192243
    bm25_hit_at_10: 0.48148148148148145
  - name: NanoBrightTheoremQAQuestions
    path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightTheoremQAQuestions.md
    retrieval_shape: applied_theorem_scenario_to_same_theorem_problem
    queries: 194
    documents: 10000
    positive_qrels: 439
    bm25_ndcg_at_10: 0.14164450412856855
    bm25_hit_at_10: 0.29896907216494845
  - name: NanoBrightTheoremQATheorems
    path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightTheoremQATheorems.md
    retrieval_shape: applied_theorem_scenario_to_formal_theorem
    queries: 76
    documents: 10000
    positive_qrels: 151
    bm25_ndcg_at_10: 0.012347729408321562
    bm25_hit_at_10: 0.02631578947368421
  learning:
    leakage_note: exclude NanoBRIGHT evaluation queries, qrels, positive passages,
      and full cited source pages; audit upstream BRIGHT and source splits before
      using public source data for training
    useful_training_data:
    - theorem-labeled solved problems and contest math problem families
    - algorithm-problem similarity pairs and programming documentation retrieval data
    - StackExchange questions paired with cited or expert-validated supporting sources
    - scientific, technical, and policy QA with explicit evidence documents
    - long-document retrieval data where the positive is a full source page
    synthetic_data:
      document_generation: solved problems, theorem statements, code solutions, technical
        documentation, and cited source passages with explicit reasoning support
      question_generation: applied scenarios, StackExchange-style questions, programming
        tasks, and evidence-seeking prompts grounded in the generated or selected
        document
      answerability: each positive must support the same theorem, algorithm, mechanism,
        cited claim, or documentation need rather than sharing only surface terms
    multi_positive_training: multi_positive_reasoning_and_evidence_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBRIGHT
    source_urls:
    - label: BRIGHT arXiv
      url: https://arxiv.org/abs/2407.12883
    - label: BRIGHT project
      url: https://brightbenchmark.github.io/
    - label: xlangai/BRIGHT
      url: https://huggingface.co/datasets/xlangai/BRIGHT
    - label: mteb/BRIGHT
      url: https://huggingface.co/datasets/mteb/BRIGHT
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
      query_weighted_ndcg_at_10: 0.2791868132
      query_weighted_hit_at_10: 0.5318485523
      query_weighted_recall_at_100: 0.6538506962
      source: dataset_candidate_subset
    dense:
      query_weighted_ndcg_at_10: 0.373566337
      query_weighted_hit_at_10: 0.634298441
      query_weighted_recall_at_100: 0.7154744051
      source: dataset_candidate_subset
    reranking_hybrid:
      query_weighted_ndcg_at_10: 0.363476371
      query_weighted_hit_at_10: 0.6565701559
      query_weighted_recall_at_100: 0.7625301648
      source: dataset_candidate_subset
```
