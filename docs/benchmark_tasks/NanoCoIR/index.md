# NanoCoIR

## Overview

NanoCoIR is the Nano task group for CoIR, a code information retrieval benchmark.
It covers ten English code-oriented retrieval settings: natural-language
developer requests retrieving code, code retrieving text, code retrieving code,
programming dialogue retrieving assistant responses, StackOverflow-style QA, and
Text-to-SQL retrieval. The group is useful because it does not reduce code
retrieval to one query shape: models must handle short search phrases, long
problem statements, multi-turn dialogue histories, executable programs, API
snippets, and cross-language or cross-framework equivalence.

The CoIR paper treats code retrieval as a family of query-document format
mismatches rather than only semantic code search. NanoCoIR preserves that idea
in small splits: APPS and Text-to-SQL become text-to-code retrieval,
CodeSearchNet appears as both code-to-text and code-continuation retrieval, and
CodeTransOcean becomes code-to-code equivalence across languages or frameworks.
The group is therefore a probe of developer intent, program semantics, and
code/prose alignment at the same time.

## Details

### What the Original Group Measures

[CoIR: A Comprehensive Benchmark for Code Information Retrieval Models](https://arxiv.org/abs/2407.02883)
introduces CoIR as a benchmark for code information retrieval across diverse
query and document formats rather than a single semantic-code-search setup. In
NanoCoIR, that breadth appears as ten compact splits derived from APPS, CoSQA,
CodeSearchNet, CodeTransOcean, OpenCodeInterpreter-style code feedback data,
StackOverflow QA data, and synthetic Text-to-SQL data. The group therefore tests
whether a retriever can connect developer intent with source code, SQL, code
answers, documentation summaries, and equivalent programs.

Several subtasks intentionally reverse or reshape familiar datasets. CodeSearchNet
appears both as code-to-text retrieval, where a code snippet retrieves its
documentation, and as CodeSearchNet-CCR, where a function prefix retrieves its
continuation. CodeTransOcean appears as cross-language and cross-framework
similar-code retrieval rather than generation. APPS and Synthetic Text-to-SQL
become text-to-code retrieval tasks. This mix makes NanoCoIR a group-level probe
of code retrieval robustness rather than a collection of near-duplicate
program-search tasks.

### Subtask Coverage

The ten subtasks cover five retrieval families:

- **Text-to-code:** `NanoApps`, `NanoCosQA`, and `NanoSyntheticText2SQL` map
  natural-language specifications or search phrases to Python or SQL code.
- **Code-to-text:** `NanoCodeSearchNet` maps source code to short docstrings or
  documentation summaries.
- **Code-to-code:** `NanoCodeSearchNetCCR`, `NanoCodeTransOceanContest`, and
  `NanoCodeTransOceanDL` retrieve code continuations or semantically equivalent
  programs across languages and frameworks.
- **Hybrid code dialogue and answer retrieval:** `NanoCodeFeedbackST`,
  `NanoCodeFeedbackMT`, and `NanoStackOverflowQA` retrieve assistant or
  community answers that mix prose, code, and diagnostic explanation.
- **Cross-language and API equivalence:** the CodeTransOcean splits require
  matching behavior despite Python/C++ or deep-learning-framework vocabulary
  shifts.

All NanoCoIR splits in the current group are English-labeled code tasks and all
observed qrels are single-positive. The difficulty is not from multiple
acceptable answers per query; it is from connecting long-form developer intent,
program structure, identifiers, library APIs, and executable behavior to one
target item.

### Observed Group Profile

Across the ten splits, NanoCoIR contains 1,850 queries, 1,850 positive qrels, and
76,295 split-local candidate documents. The document count is a sum across
subtasks, not a deduplicated group-wide corpus size. Nine subtasks have 200
queries; `NanoCodeTransOceanDL` has 50 queries and a much smaller 266-document
candidate pool.

Query length varies widely. `NanoCosQA` has very short web-search-style queries
averaging 36.10 characters, while `NanoCodeFeedbackMT` has multi-turn dialogue
queries averaging 4,468.62 characters. Document length also changes by task:
`NanoCodeSearchNet` targets short summaries averaging 86.07 characters, while
`NanoCodeTransOceanDL`, `NanoCodeFeedbackST`, and `NanoCodeFeedbackMT` use much
longer code or answer documents. This range matters because a model that works
well on short keyword-code retrieval may not be strong on long problem
statements, dialogue-state tracking, or code equivalence across APIs.

### BM25 Difficulty

The group has a wide lexical baseline range. Query-weighted BM25 nDCG@10 is
0.5965 and query-weighted hit@10 is 0.6962, but the task-level spread is large:
`NanoApps` has nDCG@10 = 0.0097 and hit@10 = 0.0150, while
`NanoCodeSearchNetCCR` has nDCG@10 = 0.8922 and hit@10 = 0.9700. This spread is
the main reason to read NanoCoIR by subtask rather than only by group average.

BM25 is weakest where the query describes behavior and the positive is compact
code with little literal overlap, as in APPS problem-to-solution retrieval. It is
strongest where source and target share identifiers, comments, local variable
names, or dialogue terms, as in code continuation and single-turn code feedback.
The middle band includes CoSQA, Synthetic Text-to-SQL, CodeTransOcean, and
StackOverflow QA, where lexical anchors help but do not fully solve intent,
schema, translation, or diagnostic matching.

### Training Data That May Help

Useful training data should be selected per retrieval family rather than pooled
blindly. For text-to-code subtasks, APPS-style problem-solution pairs, CoSQA
query-code pairs, CodeSearchNet Python functions, and Text-to-SQL prompt-query
pairs are directly relevant. For hybrid QA and dialogue subtasks, useful sources
include code-assistant instruction-answer data, StackOverflow question-answer
pairs, issue-to-fix discussions, and examples that preserve stack traces,
framework names, and executable snippets. For code-to-code subtasks, useful
sources include function continuation pairs, repository-local code context, code
translation data, and cross-framework API examples.

Training should avoid NanoCoIR evaluation queries, qrels, and positive documents.
When using the original public datasets, upstream test or evaluation splits that
likely overlap with CoIR-derived evaluation examples should be excluded unless an
explicit overlap audit has been performed. Memorizing APPS solutions,
StackOverflow answers, SQL statements, or CodeSearchNet docstrings can inflate
retrieval scores without teaching general code retrieval behavior.

### Synthetic Data Guidance

Synthetic data for NanoCoIR should preserve code semantics. Text-to-code
generation should pair realistic developer requests, competitive-programming
statements, search phrases, or database questions with runnable code or valid
SQL. Code-to-text generation should create concise summaries that match actual
function behavior, not only identifier names. Code-to-code generation should
create equivalent programs across languages, frameworks, or local contexts while
keeping API constraints and edge cases intact.

For dialogue and QA subtasks, synthetic conversations should include user
instructions, prior code, errors, execution feedback, and assistant responses
whose relevance depends on the preceding context. Generated negatives should be
nearby in language, API, or algorithm family but wrong in behavior. Evaluation
queries and positive documents from NanoCoIR should not be used as seeds for
synthetic generation.

### Benchmark Information Leakage

Some public source datasets are not safe to use as raw training data even when
their Hugging Face split is named `train`. CoIR derives compact evaluation
splits from upstream benchmark sources, and the public upstream files can still
contain the same examples used by NanoCoIR. This is especially important for the
CodeFeedback subtasks.

An audit of the two CodeFeedback sources found direct overlap with the NanoCoIR
evaluation rows. For `NanoCodeFeedbackMT`, scanning the 66,383-row
`m-a-p/Code-Feedback` train file found normalized exact matches for 200/200 Nano
queries against reconstructed dialogue prefixes and 200/200 Nano positives
against final assistant responses. For `NanoCodeFeedbackST`, scanning the
156,526-row `m-a-p/CodeFeedback-Filtered-Instruction` train file found
normalized exact matches for 200/200 Nano queries, 199/200 Nano positives, and
200/200 Nano query-positive concatenations. Token fingerprints and 7-token
shingle containment checks confirmed the same high-risk overlap pattern.

Training on these raw public train files can produce inflated NanoCoIR scores by
memorizing benchmark queries and positive documents. Systems that use these
sources for training should first remove any source row whose query, dialogue
prefix, final answer, positive document, or query-positive concatenation matches
NanoCoIR evaluation data by normalized text, token fingerprint, or high shingle
containment. Reported high scores from models trained on unfiltered CodeFeedback
sources should be treated as potentially contaminated until an overlap audit is
available.

The same split-safety principle applies to the other NanoCoIR families. APPS,
CoSQA, Synthetic Text-to-SQL, CodeSearchNet, CodeTransOcean, and StackOverflow
QA all have upstream train/test or train/dev/test partitions in CoIR. Training
should use only train-side or otherwise non-overlapping rows, then remove any
NanoCoIR query, qrel positive, code, SQL, answer, URL/id, or token fingerprint.
Using upstream test-derived rows can inflate scores on NanoApps, NanoCosQA,
NanoSyntheticText2SQL, NanoCodeSearchNet, NanoCodeSearchNetCCR,
NanoCodeTransOceanContest, NanoCodeTransOceanDL, or NanoStackOverflowQA.

## Task Summary

| Task | Retrieval shape | Queries | Docs | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars | Source status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [NanoApps](NanoApps.md) | problem statement to Python solution | 200 | 8,754 | 0.0097 | 0.0150 | 1,675.41 | 573.12 | CoIR + APPS paper |
| [NanoCodeFeedbackMT](NanoCodeFeedbackMT.md) | multi-turn dialogue to assistant response | 200 | 10,000 | 0.7311 | 0.8050 | 4,468.62 | 1,468.16 | CoIR + OpenCodeInterpreter paper |
| [NanoCodeFeedbackST](NanoCodeFeedbackST.md) | single instruction to assistant response | 200 | 10,000 | 0.8755 | 0.9300 | 730.51 | 1,538.73 | CoIR + related OpenCodeInterpreter paper |
| [NanoCodeSearchNet](NanoCodeSearchNet.md) | code snippet to natural-language summary | 200 | 10,000 | 0.6471 | 0.7700 | 636.26 | 86.07 | CoIR + CodeSearchNet paper |
| [NanoCodeSearchNetCCR](NanoCodeSearchNetCCR.md) | function prefix to code continuation | 200 | 10,000 | 0.8922 | 0.9700 | 372.82 | 158.42 | CoIR + CodeSearchNet paper |
| [NanoCodeTransOceanContest](NanoCodeTransOceanContest.md) | Python program to equivalent C++ program | 200 | 1,008 | 0.5361 | 0.6850 | 1,009.56 | 1,528.72 | CoIR + CodeTransOcean paper |
| [NanoCodeTransOceanDL](NanoCodeTransOceanDL.md) | cross-framework deep-learning code equivalence | 50 | 266 | 0.5458 | 0.9400 | 2,153.80 | 1,644.99 | CoIR + CodeTransOcean paper |
| [NanoCosQA](NanoCosQA.md) | short web query to Python function | 200 | 6,267 | 0.3574 | 0.5200 | 36.10 | 307.61 | CoIR + CoSQA paper |
| [NanoStackOverflowQA](NanoStackOverflowQA.md) | developer question to StackOverflow answer | 200 | 10,000 | 0.7403 | 0.8150 | 1,361.81 | 1,218.06 | CoIR + Stack Overflow data page |
| [NanoSyntheticText2SQL](NanoSyntheticText2SQL.md) | database question to SQL query | 200 | 10,000 | 0.5918 | 0.6950 | 102.94 | 130.60 | CoIR + Gretel dataset card |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoCoIR |
| Backing dataset | NanoCoIR |
| Hugging Face dataset | [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR) |
| Language | en |
| Category | code |
| Subtasks | 10 |
| Total queries | 1,850 |
| Split-local documents | 76,295 |
| Positive qrels | 1,850 |
| Positives per query | exactly 1.00 for every subtask |
| Query-weighted BM25 nDCG@10 | 0.5965 |
| Query-weighted BM25 hit@10 | 0.6962 |
| Mean query length | 1,181.89 chars, weighted by query count |
| Mean document length | 719.89 chars, weighted by split-local document count |

### Public Sources

- [CoIR: A Comprehensive Benchmark for Code Information Retrieval Models](https://arxiv.org/abs/2407.02883); 2025; Xiangyang Li et al.; DOI: `10.18653/v1/2025.acl-long.1072`.
- [Measuring Coding Challenge Competence With APPS](https://arxiv.org/abs/2105.09938); 2021; Dan Hendrycks et al.
- [OpenCodeInterpreter: Integrating Code Generation with Execution and Refinement](https://arxiv.org/abs/2402.14658); 2024; Tianyu Zheng et al.
- [CodeSearchNet Challenge: Evaluating the State of Semantic Code Search](https://arxiv.org/abs/1909.09436); 2019; Hamel Husain et al.
- [CodeTransOcean: A Comprehensive Multilingual Benchmark for Code Translation](https://arxiv.org/abs/2310.04951); 2023; Weixiang Yan et al.
- [CoSQA: 20,000+ Web Queries for Code Search and Question Answering](https://arxiv.org/abs/2105.13239); 2021; Junjie Huang et al.
- [Stack Overflow Data](https://www.kaggle.com/datasets/stackoverflow/stacksample/data); source data page.
- [Synthetic-Text-To-SQL](https://huggingface.co/datasets/gretelai/synthetic_text_to_sql); source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR)
- Source datasets:
  [codeparrot/apps](https://huggingface.co/datasets/codeparrot/apps),
  [m-a-p/Code-Feedback](https://huggingface.co/datasets/m-a-p/Code-Feedback),
  [m-a-p/CodeFeedback-Filtered-Instruction](https://huggingface.co/datasets/m-a-p/CodeFeedback-Filtered-Instruction),
  [code-search-net/code_search_net](https://huggingface.co/datasets/code-search-net/code_search_net),
  [CoIR-Retrieval/CodeSearchNet-ccr](https://huggingface.co/datasets/CoIR-Retrieval/CodeSearchNet-ccr),
  [WeixiangYan/CodeTransOcean](https://huggingface.co/datasets/WeixiangYan/CodeTransOcean),
  [CoIR-Retrieval/cosqa](https://huggingface.co/datasets/CoIR-Retrieval/cosqa),
  [CoIR-Retrieval/stackoverflow-qa](https://huggingface.co/datasets/CoIR-Retrieval/stackoverflow-qa),
  [gretelai/synthetic_text_to_sql](https://huggingface.co/datasets/gretelai/synthetic_text_to_sql).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CoIR: A Comprehensive Benchmark for Code Information Retrieval Models | 2025 | benchmark paper | https://arxiv.org/abs/2407.02883 |
| Measuring Coding Challenge Competence With APPS | 2021 | source task paper | https://arxiv.org/abs/2105.09938 |
| OpenCodeInterpreter: Integrating Code Generation with Execution and Refinement | 2024 | source or related task paper | https://arxiv.org/abs/2402.14658 |
| CodeSearchNet Challenge: Evaluating the State of Semantic Code Search | 2019 | source task paper | https://arxiv.org/abs/1909.09436 |
| CodeTransOcean: A Comprehensive Multilingual Benchmark for Code Translation | 2023 | source task paper | https://arxiv.org/abs/2310.04951 |
| CoSQA: 20,000+ Web Queries for Code Search and Question Answering | 2021 | source task paper | https://arxiv.org/abs/2105.13239 |
| Stack Overflow Data | 2025 | source data page | https://www.kaggle.com/datasets/stackoverflow/stacksample/data |
| Synthetic-Text-To-SQL | 2024 | dataset card | https://huggingface.co/datasets/gretelai/synthetic_text_to_sql |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoCoIR
  backing_dataset: NanoCoIR
  dataset_id: hakari-bench/NanoCoIR
  language: en
  category: code
  document_path: docs/benchmark_tasks/NanoCoIR/index.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 10
    queries: 1850
    split_local_documents: 76295
    positive_qrels: 1850
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_tasks: 0
    multi_positive_queries: 0
  text_stats_chars:
    query_mean_weighted_by_queries: 1181.8908108108108
    document_mean_weighted_by_documents: 719.8876597417917
  bm25:
    ndcg_at_10_query_weighted: 0.5964998831489635
    hit_at_10_query_weighted: 0.6962162162162162
    ndcg_at_10_unweighted_task_mean: 0.5926997035618973
    hit_at_10_unweighted_task_mean: 0.7145
    source: dataset_bm25_column
    easiest_task_by_ndcg_at_10: NanoCodeSearchNetCCR
    hardest_task_by_ndcg_at_10: NanoApps
  tasks:
    - name: NanoApps
      path: docs/benchmark_tasks/NanoCoIR/NanoApps.md
      retrieval_shape: problem_statement_to_python_solution
      queries: 200
      documents: 8754
      positive_qrels: 200
      bm25_ndcg_at_10: 0.009653382790366965
      bm25_hit_at_10: 0.015
    - name: NanoCodeFeedbackMT
      path: docs/benchmark_tasks/NanoCoIR/NanoCodeFeedbackMT.md
      retrieval_shape: multi_turn_dialogue_to_assistant_response
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.7311153823775425
      bm25_hit_at_10: 0.805
    - name: NanoCodeFeedbackST
      path: docs/benchmark_tasks/NanoCoIR/NanoCodeFeedbackST.md
      retrieval_shape: single_instruction_to_assistant_response
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.8754924057812555
      bm25_hit_at_10: 0.93
    - name: NanoCodeSearchNet
      path: docs/benchmark_tasks/NanoCoIR/NanoCodeSearchNet.md
      retrieval_shape: code_snippet_to_natural_language_summary
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.6470749577416152
      bm25_hit_at_10: 0.77
    - name: NanoCodeSearchNetCCR
      path: docs/benchmark_tasks/NanoCoIR/NanoCodeSearchNetCCR.md
      retrieval_shape: function_prefix_to_code_continuation
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.8921900411147616
      bm25_hit_at_10: 0.97
    - name: NanoCodeTransOceanContest
      path: docs/benchmark_tasks/NanoCoIR/NanoCodeTransOceanContest.md
      retrieval_shape: python_program_to_equivalent_cpp_program
      queries: 200
      documents: 1008
      positive_qrels: 200
      bm25_ndcg_at_10: 0.5360624784473309
      bm25_hit_at_10: 0.685
    - name: NanoCodeTransOceanDL
      path: docs/benchmark_tasks/NanoCoIR/NanoCodeTransOceanDL.md
      retrieval_shape: cross_framework_deep_learning_code_equivalence
      queries: 50
      documents: 266
      positive_qrels: 50
      bm25_ndcg_at_10: 0.5457652860119118
      bm25_hit_at_10: 0.94
    - name: NanoCosQA
      path: docs/benchmark_tasks/NanoCoIR/NanoCosQA.md
      retrieval_shape: short_web_query_to_python_function
      queries: 200
      documents: 6267
      positive_qrels: 200
      bm25_ndcg_at_10: 0.3573610255127629
      bm25_hit_at_10: 0.52
    - name: NanoStackOverflowQA
      path: docs/benchmark_tasks/NanoCoIR/NanoStackOverflowQA.md
      retrieval_shape: developer_question_to_stackoverflow_answer
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.7403011377737236
      bm25_hit_at_10: 0.815
    - name: NanoSyntheticText2SQL
      path: docs/benchmark_tasks/NanoCoIR/NanoSyntheticText2SQL.md
      retrieval_shape: database_question_to_sql_query
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.5919819380677027
      bm25_hit_at_10: 0.695
  learning:
    leakage_note: exclude NanoCoIR evaluation queries, qrels, and positive documents; audit upstream CoIR source splits before using public source data for training; raw CodeFeedback public train files contain NanoCodeFeedback evaluation rows
    leakage_audit:
      codefeedback_mt:
        source_dataset: m-a-p/Code-Feedback
        source_train_rows_scanned: 66383
        normalized_exact_query_matches: 200
        normalized_exact_positive_matches: 200
        risk: raw public train leaks NanoCodeFeedbackMT evaluation rows
      codefeedback_st:
        source_dataset: m-a-p/CodeFeedback-Filtered-Instruction
        source_train_rows_scanned: 156526
        normalized_exact_query_matches: 200
        normalized_exact_positive_matches: 199
        normalized_exact_query_positive_matches: 200
        risk: raw public train leaks NanoCodeFeedbackST evaluation rows
    split_leakage_risk:
      apps: use APPS train-side rows only; exclude NanoApps problem statements and solutions
      cosqa: use CoSQA train-side rows only; exclude NanoCosQA queries and Python functions
      synthetic_text_to_sql: use Gretel train split only; exclude NanoSyntheticText2SQL prompts, SQL, and schema context
      codesearchnet: use CodeSearchNet train-side rows only; exclude NanoCodeSearchNet code-docstring and CCR prefix-continuation pairs
      codetransocean: use CodeTransOcean train or validation rows only; exclude NanoCodeTransOcean contest and DL code pairs
      stackoverflow_qa: use StackOverflow QA train-side rows only; exclude NanoStackOverflowQA questions, answers, URLs, ids, and code blocks
    useful_training_data:
      - APPS-style problem-to-solution retrieval pairs
      - CoSQA and CodeSearchNet query-code or code-summary pairs
      - code-assistant instruction-answer and multi-turn feedback data
      - StackOverflow question-answer pairs with code and diagnostic context
      - code translation, code continuation, and cross-framework API examples
      - Text-to-SQL prompt-query pairs with schema-aware supervision
    synthetic_data:
      document_generation: runnable code, valid SQL, code answers, code continuations, and equivalent programs with realistic identifiers, APIs, errors, and constraints
      question_generation: natural developer requests, short web queries, long programming statements, dialogue histories, and database questions grounded in the generated or selected document
      answerability: each positive must satisfy executable behavior, API semantics, SQL intent, or developer-answer relevance rather than sharing only surface words
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoCoIR
    source_urls:
      - label: CoIR arXiv
        url: https://arxiv.org/abs/2407.02883
      - label: CoIR ACL Anthology
        url: https://aclanthology.org/2025.acl-long.1072/
      - label: codeparrot/apps
        url: https://huggingface.co/datasets/codeparrot/apps
      - label: m-a-p/Code-Feedback
        url: https://huggingface.co/datasets/m-a-p/Code-Feedback
      - label: m-a-p/CodeFeedback-Filtered-Instruction
        url: https://huggingface.co/datasets/m-a-p/CodeFeedback-Filtered-Instruction
      - label: code-search-net/code_search_net
        url: https://huggingface.co/datasets/code-search-net/code_search_net
      - label: CoIR-Retrieval/CodeSearchNet-ccr
        url: https://huggingface.co/datasets/CoIR-Retrieval/CodeSearchNet-ccr
      - label: WeixiangYan/CodeTransOcean
        url: https://huggingface.co/datasets/WeixiangYan/CodeTransOcean
      - label: CoIR-Retrieval/cosqa
        url: https://huggingface.co/datasets/CoIR-Retrieval/cosqa
      - label: CoIR-Retrieval/stackoverflow-qa
        url: https://huggingface.co/datasets/CoIR-Retrieval/stackoverflow-qa
      - label: gretelai/synthetic_text_to_sql
        url: https://huggingface.co/datasets/gretelai/synthetic_text_to_sql
    source_notes: []
  references:
    - title: "CoIR: A Comprehensive Benchmark for Code Information Retrieval Models"
      url: https://arxiv.org/abs/2407.02883
      year: 2025
      doi: 10.18653/v1/2025.acl-long.1072
      is_paper: true
      source_confidence: definitive_paper_link
    - title: Measuring Coding Challenge Competence With APPS
      url: https://arxiv.org/abs/2105.09938
      year: 2021
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "OpenCodeInterpreter: Integrating Code Generation with Execution and Refinement"
      url: https://arxiv.org/abs/2402.14658
      year: 2024
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "CodeSearchNet Challenge: Evaluating the State of Semantic Code Search"
      url: https://arxiv.org/abs/1909.09436
      year: 2019
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "CodeTransOcean: A Comprehensive Multilingual Benchmark for Code Translation"
      url: https://arxiv.org/abs/2310.04951
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "CoSQA: 20,000+ Web Queries for Code Search and Question Answering"
      url: https://arxiv.org/abs/2105.13239
      year: 2021
      is_paper: true
      source_confidence: definitive_paper_link
```
