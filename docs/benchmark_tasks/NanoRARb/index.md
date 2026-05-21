# NanoRARb

## Overview

NanoRARb is the Nano task group for RAR-b, the Reasoning as Retrieval Benchmark.
It converts reasoning problems into retrieval tasks: the query is a question,
story context, code prompt, math problem, spatial scene, or temporal reasoning
prompt, and the relevant document is the correct answer, continuation, entity,
solution, or implementation from a large answer pool.

The group is useful because it tests whether embedding retrievers can do more
than topical search. Many positive documents are only a few words long, while
the query may require abductive, physical, social, temporal, mathematical,
spatial, reading-comprehension, or programming reasoning. Lexical overlap is
often weak or actively misleading, so the group is a compact stress test for
reasoning-level semantic retrieval.

## Details

### What the Original Group Measures

[RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347)
asks whether retrievers can solve reasoning problems after those problems are
recast as information retrieval. Instead of retrieving topical documents, RAR-b
builds answer pools from reasoning datasets and evaluates whether the retriever
can rank the ground-truth answer near the top. The paper argues that current
retrievers can be far from competent on reasoning-intensive retrieval, even when
they perform well on ordinary semantic textual similarity or IR tasks.

NanoRARb keeps that formulation in compact form. It includes classic reasoning
datasets such as ARC-Challenge, AlphaNLI, HellaSwag, PIQA, QuAIL, Social IQA,
SpartQA, WinoGrande, TempReason, code reasoning data, and math problem-solving
data. Each split uses the common Nano retrieval structure: queries, candidate
answer documents, qrels, and dataset-provided BM25 rankings.

### Subtask Coverage

The seventeen subtasks cover six reasoning families:

- **Commonsense and answer selection:** `NanoARCChallenge`, `NanoAlphaNLI`,
  `NanoHellaSwag`, `NanoPIQA`, `NanoSIQA`, and `NanoWinoGrande` test science
  QA, abductive story bridging, plausible event continuation, physical
  commonsense, social commonsense, and referent resolution.
- **Reading and spatial reasoning:** `NanoQuail` selects short answers from long
  narrative passages, while `NanoSpartQA` requires tracking spatial relations
  among blocks, shapes, colors, and positions.
- **Code reasoning:** `NanoRARbCode` maps function signatures and docstrings to
  executable implementations.
- **Math reasoning:** `NanoRARbMath` retrieves worked mathematical solutions for
  GSM8K/MATH-style problems.
- **Temporal arithmetic and temporal knowledge:** `NanoTempReasonL1`,
  `NanoTempReasonL2Pure`, `NanoTempReasonL2Fact`, `NanoTempReasonL2Context`,
  `NanoTempReasonL3Pure`, `NanoTempReasonL3Fact`, and
  `NanoTempReasonL3Context` ask for dates, entities active at a time, or
  before/after entity relations.
- **Long-context reasoning:** the TempReason context splits and QuAIL place
  short answer strings behind very long query contexts, including fact lists
  that can exceed tens of thousands of characters.

All observed NanoRARb splits are English-labeled in the task metadata, although
the group-level dataset is categorized as multilingual in the benchmark config.
Sixteen splits are single-positive for every query. `NanoSpartQA` is the only
observed multi-positive split, with 92 multi-positive queries and up to three
positives per query.

### Observed Group Profile

Across the seventeen splits, NanoRARb contains 3,400 queries, 3,584 positive
qrels, and 156,037 split-local candidate documents. Each split has 200 queries.
The document count is a sum across subtasks, not a deduplicated group-wide
corpus size. Queries average 4,012.63 characters when weighted by query count,
but this mean is dominated by the TempReason context tasks:
`NanoTempReasonL2Context` averages 28,755.18 characters and
`NanoTempReasonL3Context` averages 31,804.13 characters. In contrast, `NanoPIQA`
queries average only 37.89 characters.

Documents are usually short answers rather than passages. The weighted document
mean is 74.15 characters. Many temporal and WinoGrande answers are short entity
strings, while code and math documents are longer because they contain
implementations or worked solutions. The sampled data includes short science
answer options, story middle events, physical procedures, social-intent answers,
spatial object descriptions, one-word referents, dates, entity names, Python code
snippets, and mathematical derivations.

### BM25 Difficulty

BM25 is weak on NanoRARb overall: query-weighted nDCG@10 is 0.1246 and
query-weighted hit@10 is 0.1982. This is expected for a benchmark designed to
measure reasoning as retrieval. The answer is often semantically or logically
entailed by the query, not lexically similar to it.

The task-level range is large. `NanoRARbMath` is easiest for BM25
(nDCG@10 = 0.5348, hit@10 = 0.6600) because solutions repeat equations,
symbols, and quantities from the problem. `NanoWinoGrande` also has high hit@10
(0.7950) because the correct referent often appears in the sentence, although
top-1 ranking still requires resolving the blank. `NanoAlphaNLI` and
`NanoSpartQA` are in the middle because hypotheses or spatial answer phrases can
share story entities or object labels.

The hardest tasks are those where the answer string has little lexical overlap
with the query. `NanoTempReasonL2Pure` has nDCG@10 = 0.0000 and hit@10 = 0.0000;
the answer must be inferred from temporal knowledge, not copied from the
question. `NanoRARbCode`, `NanoQuail`, `NanoSIQA`, and the TempReason context
tasks also have very low lexical scores because the query describes behavior,
passage meaning, social intent, or long interval facts while the answer is a
short phrase or implementation.

### Training Data That May Help

Useful training data should be selected by reasoning family. For commonsense
tasks, use abductive story reasoning, HellaSwag-style continuation, physical and
social commonsense QA, Winograd/coreference examples, and ARC-style science
answer selection. For long-context and reading tasks, use passage QA and
answer-option retrieval where the target may be short or generic. For spatial
and temporal tasks, use scene-graph QA, textual spatial reasoning, temporal
interval QA, date arithmetic, and entity-time retrieval. For code and math, use
docstring-to-code retrieval, HumanEval/MBPP-style tasks outside the evaluation
examples, GSM8K/MATH problem-solution pairs, and verifier or worked-solution
data.

Training should exclude NanoRARb evaluation queries, qrels, candidate answers,
solutions, and code snippets. Because RAR-b builds large answer pools from
reasoning datasets, using upstream evaluation examples or pooled answer strings
without an overlap audit can leak the exact target answer. For TempReason and
SpartQA, preserve the underlying relation structure rather than training only on
surface question-answer pairs.

### Synthetic Data Guidance

Synthetic data for NanoRARb should keep the reasoning relation explicit. Good
examples pair a reasoning query with an answer that is correct for a causal,
physical, social, mathematical, temporal, spatial, code, or reading-comprehension
reason. Hard negatives should be close to the query vocabulary but fail the
reasoning condition: a plausible story event that does not explain the ending, a
physical procedure that uses the same object incorrectly, a temporal entity from
the wrong interval, a code snippet with similar identifiers but wrong behavior,
or a math solution that solves a neighboring expression.

Synthetic answer pools should also include short generic candidates. Several
RAR-b tasks are hard precisely because the positive is a short phrase such as a
name, date, referent, or "not enough information"; removing such candidates
would make the retrieval problem less faithful to the original benchmark.

## Task Summary

| Task | Retrieval shape | Queries | Docs | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars | Source status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [NanoARCChallenge](NanoARCChallenge.md) | science question to answer option | 200 | 9,350 | 0.0394 | 0.0800 | 126.66 | 30.94 | RAR-b + ARC paper |
| [NanoAlphaNLI](NanoAlphaNLI.md) | story observations to explanatory event | 200 | 10,000 | 0.2936 | 0.4450 | 103.79 | 43.84 | RAR-b + AlphaNLI paper |
| [NanoHellaSwag](NanoHellaSwag.md) | activity context to plausible continuation | 200 | 10,000 | 0.1166 | 0.2000 | 114.68 | 62.15 | RAR-b + HellaSwag paper |
| [NanoPIQA](NanoPIQA.md) | physical goal to procedure/solution | 200 | 10,000 | 0.1571 | 0.2350 | 37.89 | 98.01 | RAR-b + PIQA paper |
| [NanoQuail](NanoQuail.md) | long passage question to short answer | 200 | 10,000 | 0.0215 | 0.0350 | 1,813.76 | 25.02 | RAR-b + QuAIL paper |
| [NanoRARbCode](NanoRARbCode.md) | code prompt/docstring to implementation | 200 | 10,000 | 0.0263 | 0.0350 | 470.08 | 256.00 | RAR-b + code source papers |
| [NanoRARbMath](NanoRARbMath.md) | math problem to worked solution | 200 | 10,000 | 0.5348 | 0.6600 | 201.32 | 481.33 | RAR-b + GSM8K/MATH/MetaMath |
| [NanoSIQA](NanoSIQA.md) | social context and question to answer | 200 | 10,000 | 0.0278 | 0.0450 | 126.94 | 21.51 | RAR-b + Social IQA paper |
| [NanoSpartQA](NanoSpartQA.md) | spatial scene question to answer phrase | 200 | 1,592 | 0.2321 | 0.3350 | 654.85 | 49.80 | RAR-b + SpartQA paper |
| [NanoTempReasonL1](NanoTempReasonL1.md) | date arithmetic question to date | 200 | 10,000 | 0.0125 | 0.0350 | 49.88 | 9.00 | RAR-b + TempReason paper |
| [NanoTempReasonL2Context](NanoTempReasonL2Context.md) | long temporal facts to active entity | 200 | 10,000 | 0.0287 | 0.0650 | 28,755.18 | 19.91 | RAR-b + TempReason paper |
| [NanoTempReasonL2Fact](NanoTempReasonL2Fact.md) | temporal facts to active entity | 200 | 10,000 | 0.0969 | 0.1950 | 1,744.39 | 19.91 | RAR-b + TempReason paper |
| [NanoTempReasonL2Pure](NanoTempReasonL2Pure.md) | temporal question to active entity | 200 | 10,000 | 0.0000 | 0.0000 | 52.95 | 19.91 | RAR-b + TempReason paper |
| [NanoTempReasonL3Context](NanoTempReasonL3Context.md) | long temporal facts to before/after entity | 200 | 10,000 | 0.0262 | 0.0600 | 31,804.13 | 19.88 | RAR-b + TempReason paper |
| [NanoTempReasonL3Fact](NanoTempReasonL3Fact.md) | temporal facts to before/after entity | 200 | 10,000 | 0.0679 | 0.1400 | 1,981.07 | 19.88 | RAR-b + TempReason paper |
| [NanoTempReasonL3Pure](NanoTempReasonL3Pure.md) | temporal relation question to entity | 200 | 10,000 | 0.0057 | 0.0100 | 65.13 | 19.88 | RAR-b + TempReason paper |
| [NanoWinoGrande](NanoWinoGrande.md) | masked sentence to referent | 200 | 5,095 | 0.4306 | 0.7950 | 111.97 | 7.68 | RAR-b + WinoGrande paper |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRARb |
| Backing dataset | NanoRARb |
| Hugging Face dataset | [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb) |
| Language | multilingual group config; observed task metadata is English |
| Category | natural_language |
| Subtasks | 17 |
| Total queries | 3,400 |
| Split-local documents | 156,037 |
| Positive qrels | 3,584 |
| Positives per query | avg 1.05, min 1, median 1.0, max 3 |
| Multi-positive tasks | 1 |
| Query-weighted BM25 nDCG@10 | 0.1246 |
| Query-weighted BM25 hit@10 | 0.1982 |
| Mean query length | 4,012.63 chars, weighted by query count |
| Mean document length | 74.15 chars, weighted by split-local document count |

### Public Sources

- [RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347); 2024; Chenghao Xiao, G. Thomas Hudson, and Noura Al Moubayed.
- [Think you have solved question answering? Try ARC, the AI2 Reasoning Challenge](https://arxiv.org/abs/1803.05457); 2018; Peter Clark et al.
- [Abductive Commonsense Reasoning](https://arxiv.org/abs/1908.05739); 2019; Chandra Bhagavatula et al.
- [HellaSwag: Can a Machine Really Finish Your Sentence?](https://arxiv.org/abs/1905.07830); 2019; Rowan Zellers et al.
- [PIQA: Reasoning about Physical Commonsense in Natural Language](https://arxiv.org/abs/1911.11641); 2020; Yonatan Bisk et al.
- [Getting Closer to AI Complete Question Answering: A Set of Prerequisite Real Tasks](https://ojs.aaai.org/index.php/AAAI/article/view/6398); 2020; QuAIL source paper.
- [Social IQa: Commonsense Reasoning about Social Interactions](https://arxiv.org/abs/1904.09728); 2019; Maarten Sap et al.
- [SpartQA: A Textual Question Answering Benchmark for Spatial Reasoning](https://arxiv.org/abs/2104.05832); 2021; SpartQA source paper.
- [WinoGrande: An Adversarial Winograd Schema Challenge at Scale](https://arxiv.org/abs/1907.10641); 2019; Keisuke Sakaguchi et al.
- [Towards Benchmarking and Improving the Temporal Reasoning Capability of Large Language Models](https://arxiv.org/abs/2306.08952); 2023; TempReason source paper.
- [CodeSearchNet Challenge: Evaluating the State of Semantic Code Search](https://arxiv.org/abs/1909.09436); 2019; Hamel Husain et al.
- [OctoPack: Instruction Tuning Code Large Language Models](https://arxiv.org/abs/2308.07124); 2023; Muennighoff et al.
- [Training Verifiers to Solve Math Word Problems](https://arxiv.org/abs/2110.14168), [Measuring Mathematical Problem Solving With the MATH Dataset](https://arxiv.org/abs/2103.03874), and [MetaMath](https://arxiv.org/abs/2309.12284).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | benchmark paper | https://arxiv.org/abs/2404.06347 |
| Think you have solved question answering? Try ARC, the AI2 Reasoning Challenge | 2018 | source task paper | https://arxiv.org/abs/1803.05457 |
| Abductive Commonsense Reasoning | 2019 | source task paper | https://arxiv.org/abs/1908.05739 |
| HellaSwag: Can a Machine Really Finish Your Sentence? | 2019 | source task paper | https://arxiv.org/abs/1905.07830 |
| PIQA: Reasoning about Physical Commonsense in Natural Language | 2020 | source task paper | https://arxiv.org/abs/1911.11641 |
| Getting Closer to AI Complete Question Answering: A Set of Prerequisite Real Tasks | 2020 | source task paper | https://ojs.aaai.org/index.php/AAAI/article/view/6398 |
| Social IQa: Commonsense Reasoning about Social Interactions | 2019 | source task paper | https://arxiv.org/abs/1904.09728 |
| SpartQA: A Textual Question Answering Benchmark for Spatial Reasoning | 2021 | source task paper | https://arxiv.org/abs/2104.05832 |
| WinoGrande: An Adversarial Winograd Schema Challenge at Scale | 2019 | source task paper | https://arxiv.org/abs/1907.10641 |
| Towards Benchmarking and Improving the Temporal Reasoning Capability of Large Language Models | 2023 | source task paper | https://arxiv.org/abs/2306.08952 |
| CodeSearchNet Challenge: Evaluating the State of Semantic Code Search | 2019 | source task paper | https://arxiv.org/abs/1909.09436 |
| OctoPack: Instruction Tuning Code Large Language Models | 2023 | source task paper | https://arxiv.org/abs/2308.07124 |
| Training Verifiers to Solve Math Word Problems | 2021 | source task paper | https://arxiv.org/abs/2110.14168 |
| Measuring Mathematical Problem Solving With the MATH Dataset | 2021 | source task paper | https://arxiv.org/abs/2103.03874 |
| MetaMath: Bootstrap Your Own Mathematical Questions for Large Language Models | 2023 | source task paper | https://arxiv.org/abs/2309.12284 |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoRARb
  backing_dataset: NanoRARb
  dataset_id: hakari-bench/NanoRARb
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRARb/index.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 17
    queries: 3400
    split_local_documents: 156037
    positive_qrels: 3584
  positives_per_query:
    average: 1.0541176470588236
    min: 1
    median: 1.0
    max: 3
    multi_positive_tasks: 1
    multi_positive_queries: 92
  text_stats_chars:
    query_mean_weighted_by_queries: 4012.627941176471
    document_mean_weighted_by_documents: 74.15082961092561
  bm25:
    ndcg_at_10_query_weighted: 0.12457058823529413
    hit_at_10_query_weighted: 0.19823529411764707
    ndcg_at_10_unweighted_task_mean: 0.12457058823529413
    hit_at_10_unweighted_task_mean: 0.19823529411764707
    source: dataset_bm25_column
    easiest_task_by_ndcg_at_10: NanoRARbMath
    hardest_task_by_ndcg_at_10: NanoTempReasonL2Pure
  tasks:
    - name: NanoARCChallenge
      path: docs/benchmark_tasks/NanoRARb/NanoARCChallenge.md
      retrieval_shape: science_question_to_answer_option
      queries: 200
      documents: 9350
      positive_qrels: 200
      bm25_ndcg_at_10: 0.0394
      bm25_hit_at_10: 0.08
    - name: NanoAlphaNLI
      path: docs/benchmark_tasks/NanoRARb/NanoAlphaNLI.md
      retrieval_shape: story_observations_to_explanatory_event
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.2936
      bm25_hit_at_10: 0.445
    - name: NanoHellaSwag
      path: docs/benchmark_tasks/NanoRARb/NanoHellaSwag.md
      retrieval_shape: activity_context_to_plausible_continuation
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.1166
      bm25_hit_at_10: 0.2
    - name: NanoPIQA
      path: docs/benchmark_tasks/NanoRARb/NanoPIQA.md
      retrieval_shape: physical_goal_to_procedure_solution
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.1571
      bm25_hit_at_10: 0.235
    - name: NanoQuail
      path: docs/benchmark_tasks/NanoRARb/NanoQuail.md
      retrieval_shape: long_passage_question_to_short_answer
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.0215
      bm25_hit_at_10: 0.035
    - name: NanoRARbCode
      path: docs/benchmark_tasks/NanoRARb/NanoRARbCode.md
      retrieval_shape: code_prompt_docstring_to_implementation
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.0263
      bm25_hit_at_10: 0.035
    - name: NanoRARbMath
      path: docs/benchmark_tasks/NanoRARb/NanoRARbMath.md
      retrieval_shape: math_problem_to_worked_solution
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.5348
      bm25_hit_at_10: 0.66
    - name: NanoSIQA
      path: docs/benchmark_tasks/NanoRARb/NanoSIQA.md
      retrieval_shape: social_context_question_to_answer
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.0278
      bm25_hit_at_10: 0.045
    - name: NanoSpartQA
      path: docs/benchmark_tasks/NanoRARb/NanoSpartQA.md
      retrieval_shape: spatial_scene_question_to_answer_phrase
      queries: 200
      documents: 1592
      positive_qrels: 384
      bm25_ndcg_at_10: 0.2321
      bm25_hit_at_10: 0.335
    - name: NanoTempReasonL1
      path: docs/benchmark_tasks/NanoRARb/NanoTempReasonL1.md
      retrieval_shape: date_arithmetic_question_to_date
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.0125
      bm25_hit_at_10: 0.035
    - name: NanoTempReasonL2Context
      path: docs/benchmark_tasks/NanoRARb/NanoTempReasonL2Context.md
      retrieval_shape: long_temporal_facts_to_active_entity
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.0287
      bm25_hit_at_10: 0.065
    - name: NanoTempReasonL2Fact
      path: docs/benchmark_tasks/NanoRARb/NanoTempReasonL2Fact.md
      retrieval_shape: temporal_facts_to_active_entity
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.0969
      bm25_hit_at_10: 0.195
    - name: NanoTempReasonL2Pure
      path: docs/benchmark_tasks/NanoRARb/NanoTempReasonL2Pure.md
      retrieval_shape: temporal_question_to_active_entity
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.0
      bm25_hit_at_10: 0.0
    - name: NanoTempReasonL3Context
      path: docs/benchmark_tasks/NanoRARb/NanoTempReasonL3Context.md
      retrieval_shape: long_temporal_facts_to_before_after_entity
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.0262
      bm25_hit_at_10: 0.06
    - name: NanoTempReasonL3Fact
      path: docs/benchmark_tasks/NanoRARb/NanoTempReasonL3Fact.md
      retrieval_shape: temporal_facts_to_before_after_entity
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.0679
      bm25_hit_at_10: 0.14
    - name: NanoTempReasonL3Pure
      path: docs/benchmark_tasks/NanoRARb/NanoTempReasonL3Pure.md
      retrieval_shape: temporal_relation_question_to_entity
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.0057
      bm25_hit_at_10: 0.01
    - name: NanoWinoGrande
      path: docs/benchmark_tasks/NanoRARb/NanoWinoGrande.md
      retrieval_shape: masked_sentence_to_referent
      queries: 200
      documents: 5095
      positive_qrels: 200
      bm25_ndcg_at_10: 0.4306
      bm25_hit_at_10: 0.795
  learning:
    leakage_note: exclude NanoRARb evaluation queries, qrels, candidate answers, code snippets, math solutions, temporal answer strings, and upstream evaluation rows used in RAR-b answer pools
    useful_training_data:
      - ARC-style science answer selection and explanation-backed multiple-choice QA
      - abductive, physical, social, event-continuation, and Winograd-style commonsense data
      - long-passage reading-comprehension answer selection and textual spatial reasoning data
      - temporal interval QA, date arithmetic, and entity-time retrieval examples
      - docstring-to-code retrieval and HumanEval or MBPP-style code tasks outside evaluation rows
      - GSM8K, MATH, verifier, and worked-solution retrieval data outside evaluation rows
    synthetic_data:
      document_generation: concise answer strings, plausible continuations, referents, temporal entities, code implementations, and worked math solutions
      question_generation: reasoning prompts with enough context to determine one correct answer or a small set of correct answer strings
      answerability: positives must satisfy the reasoning relation rather than repeat query words
    multi_positive_training: mostly_single_positive_with_spartqa_multi_positive_spatial_answers
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoRARb
    source_urls:
      - label: RAR-b arXiv
        url: https://arxiv.org/abs/2404.06347
      - label: ARC arXiv
        url: https://arxiv.org/abs/1803.05457
      - label: AlphaNLI arXiv
        url: https://arxiv.org/abs/1908.05739
      - label: HellaSwag arXiv
        url: https://arxiv.org/abs/1905.07830
      - label: PIQA arXiv
        url: https://arxiv.org/abs/1911.11641
      - label: QuAIL AAAI
        url: https://ojs.aaai.org/index.php/AAAI/article/view/6398
      - label: Social IQA arXiv
        url: https://arxiv.org/abs/1904.09728
      - label: SpartQA arXiv
        url: https://arxiv.org/abs/2104.05832
      - label: WinoGrande arXiv
        url: https://arxiv.org/abs/1907.10641
      - label: TempReason arXiv
        url: https://arxiv.org/abs/2306.08952
    source_notes: []
  references:
    - title: "RAR-b: Reasoning as Retrieval Benchmark"
      url: https://arxiv.org/abs/2404.06347
      year: 2024
      doi: 10.48550/arXiv.2404.06347
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "Think you have solved question answering? Try ARC, the AI2 Reasoning Challenge"
      url: https://arxiv.org/abs/1803.05457
      year: 2018
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "Abductive Commonsense Reasoning"
      url: https://arxiv.org/abs/1908.05739
      year: 2019
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "HellaSwag: Can a Machine Really Finish Your Sentence?"
      url: https://arxiv.org/abs/1905.07830
      year: 2019
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "PIQA: Reasoning about Physical Commonsense in Natural Language"
      url: https://arxiv.org/abs/1911.11641
      year: 2020
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "Getting Closer to AI Complete Question Answering: A Set of Prerequisite Real Tasks"
      url: https://ojs.aaai.org/index.php/AAAI/article/view/6398
      year: 2020
      is_paper: true
      source_confidence: probably_correct
    - title: "Social IQa: Commonsense Reasoning about Social Interactions"
      url: https://arxiv.org/abs/1904.09728
      year: 2019
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "SpartQA: A Textual Question Answering Benchmark for Spatial Reasoning"
      url: https://arxiv.org/abs/2104.05832
      year: 2021
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "WinoGrande: An Adversarial Winograd Schema Challenge at Scale"
      url: https://arxiv.org/abs/1907.10641
      year: 2019
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "Towards Benchmarking and Improving the Temporal Reasoning Capability of Large Language Models"
      url: https://arxiv.org/abs/2306.08952
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
```
