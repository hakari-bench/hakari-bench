# NanoCoIR

## Overview

NanoCoIR is the compact Nano set for CoIR, a code information retrieval
benchmark. It covers ten English code-oriented retrieval settings: natural
language developer requests retrieving code, code retrieving text, code
retrieving code, programming dialogue retrieving assistant responses,
StackOverflow-style QA, and Text-to-SQL retrieval. The group is useful because
it does not reduce code retrieval to one query shape.

The CoIR setting treats code retrieval as a family of format mismatches.
Developer intent, program behavior, identifiers, API usage, SQL schemas,
dialogue history, and code summaries can all be the relevant signal. BM25 shows
where identifiers and repeated technical terms dominate, dense retrieval tests
whether program semantics and developer intent align, and `reranking_hybrid`
shows whether exact code tokens and semantic similarity recover different
candidate sets.

## What This Group Measures

[CoIR: A Comprehensive Benchmark for Code Information Retrieval Models](https://arxiv.org/abs/2407.02883)
introduces CoIR as a benchmark for code retrieval across diverse query and
document formats. NanoCoIR keeps ten compact splits derived from APPS, CoSQA,
CodeSearchNet, CodeTransOcean, code feedback data, StackOverflow QA, and
synthetic Text-to-SQL.

The shared measurement target is code/prose alignment. A relevant document may
be runnable code, a docstring, a code continuation, an equivalent program, a SQL
statement, or a mixed prose-and-code answer. A model that only matches keywords
will miss behavior; a model that only matches broad semantics may miss exact
APIs, schemas, identifiers, and error messages.

## Task Families

- **Text-to-code retrieval:** `NanoApps`, `NanoCosQA`, and
  `NanoSyntheticText2SQL` map specifications, search phrases, or database
  questions to code or SQL.
- **Code-to-text retrieval:** `NanoCodeSearchNet` maps code snippets to
  documentation-like summaries.
- **Code-to-code retrieval:** `NanoCodeSearchNetCCR`,
  `NanoCodeTransOceanContest`, and `NanoCodeTransOceanDL` retrieve code
  continuations or semantically equivalent programs across languages or
  frameworks.
- **Dialogue and QA retrieval:** `NanoCodeFeedbackST`,
  `NanoCodeFeedbackMT`, and `NanoStackOverflowQA` retrieve assistant or
  community answers that mix explanation and code.

## Dataset Shape

NanoCoIR contains 10 task pages, 1,850 queries, 76,295 split-local documents,
and 1,850 positive qrel rows. All tasks are single-positive in the current
metadata. Nine tasks have 200 queries; `NanoCodeTransOceanDL` has 50.

Text length varies sharply. `NanoCosQA` has very short search-style queries,
while `NanoCodeFeedbackMT` has multi-turn dialogue histories averaging more
than 4,000 characters. Documents range from short CodeSearchNet summaries and
SQL statements to long code-feedback answers and cross-framework code examples.
This makes global averages less informative than per-task interpretation.

## Retrieval Behavior

### BM25 Profile

BM25 is strongest when identifiers, function names, comments, error messages,
or dialogue terms repeat across query and document. It performs very well on
code feedback, code continuation, StackOverflow QA, and some CodeSearchNet
formats. It is extremely weak on `NanoApps`, where a long programming problem
must retrieve a solution with little direct lexical overlap.

Sparse retrieval is not a naive baseline for code tasks; it captures exact
tokens that often matter. But it can fail when relevance depends on algorithmic
behavior, schema semantics, or cross-language equivalence.

### Dense Profile

Dense retrieval is the best profile for most NanoCoIR tasks. It substantially
improves APPS, CodeSearchNet, CoSQA, Text-to-SQL, CodeTransOcean, and code
feedback retrieval by connecting intent and program behavior beyond exact
token overlap. It is especially useful when natural-language problem statements
need to retrieve compact code or SQL.

Dense retrieval still has to preserve code-specific details. A semantically
near answer with the wrong library, schema column, edge case, framework, or
language behavior is not relevant. Strong dense performance here should be read
as code-aware semantic matching, not generic sentence similarity.

### Reranking Hybrid Profile

`reranking_hybrid` is strongest where exact code tokens and semantic intent are
both needed. It leads on `NanoCodeSearchNetCCR` and is competitive on feedback,
StackOverflow, and Text-to-SQL tasks. In several dense-led tasks, hybrid still
provides a useful candidate pool because BM25 may recover exact identifiers
that dense retrieval misses.

For reranker experiments, NanoCoIR is a candidate-generation stress test. If
the first stage drops the exact API, schema, or equivalent implementation, a
reranker cannot recover the answer.

## Task Summary

| Task | Retrieval shape | Queries | Docs | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [NanoApps](NanoApps.md) | programming problem to solution code | 200 | 8,754 | 0.0084 | 0.2528 | 0.1655 | Dense |
| [NanoCodeFeedbackMT](NanoCodeFeedbackMT.md) | multi-turn code dialogue to assistant answer | 200 | 10,000 | 0.7403 | 0.9177 | 0.8035 | Dense |
| [NanoCodeFeedbackST](NanoCodeFeedbackST.md) | single-turn code prompt to assistant answer | 200 | 10,000 | 0.8722 | 0.9532 | 0.9115 | Dense |
| [NanoCodeSearchNet](NanoCodeSearchNet.md) | code to documentation summary | 200 | 10,000 | 0.6099 | 0.9687 | 0.8678 | Dense |
| [NanoCodeSearchNetCCR](NanoCodeSearchNetCCR.md) | code prefix to continuation | 200 | 10,000 | 0.8834 | 0.8519 | 0.9073 | Reranking hybrid |
| [NanoCodeTransOceanContest](NanoCodeTransOceanContest.md) | contest code to equivalent code | 200 | 1,008 | 0.4869 | 0.8231 | 0.7157 | Dense |
| [NanoCodeTransOceanDL](NanoCodeTransOceanDL.md) | deep-learning code to equivalent framework code | 50 | 266 | 0.5581 | 0.6327 | 0.5956 | Dense |
| [NanoCosQA](NanoCosQA.md) | developer search query to code | 200 | 6,267 | 0.3049 | 0.6733 | 0.4792 | Dense |
| [NanoStackOverflowQA](NanoStackOverflowQA.md) | StackOverflow question to answer | 200 | 10,000 | 0.7482 | 0.8836 | 0.8328 | Dense |
| [NanoSyntheticText2SQL](NanoSyntheticText2SQL.md) | natural-language database question to SQL | 200 | 10,000 | 0.2240 | 0.9567 | 0.5577 | Dense |

## Interpretation Notes for Model Researchers

NanoCoIR should be read by query-document format. Text-to-code, code-to-text,
code-to-code, dialogue, and SQL retrieval stress different capabilities. A
model that is excellent on CodeSearchNet summaries may still be weak on APPS
problem solving or CodeTransOcean cross-framework equivalence.

The BM25/dense contrast is central. BM25-led or BM25-competitive rows show the
importance of exact identifiers and code tokens. Dense-led rows show intent and
behavior matching. Hybrid-led rows show candidate complementarity, especially
when exact tokens and semantic program structure both matter.

## Training and Leakage Notes

Useful training data includes APPS-style problem-solution pairs, CoSQA
query-code data, CodeSearchNet functions and summaries, Text-to-SQL pairs,
StackOverflow QA, code-assistant dialogue, code translation data, framework
equivalence examples, and hard negatives from nearby APIs or algorithms.

Exclude NanoCoIR evaluation queries, positives, qrels, SQL statements, code
snippets, docstrings, and direct synthetic variants. Public code datasets often
have duplicated examples across splits and repositories, so overlap audits are
important before training.

## Public Sources

- [CoIR: A Comprehensive Benchmark for Code Information Retrieval Models](https://arxiv.org/abs/2407.02883), 2024.

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| CoIR: A Comprehensive Benchmark for Code Information Retrieval Models | 2024 | paper | [https://arxiv.org/abs/2407.02883](https://arxiv.org/abs/2407.02883) |
