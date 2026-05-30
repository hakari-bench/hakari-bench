# NanoRTEB / NanoFreshStack

## Overview

`NanoFreshStack` is an English technical-document retrieval task from NanoRTEB. The query is a realistic developer question, often from recent or niche software contexts, and relevant documents are technical documentation, release notes, tests, or code-adjacent text that support the answer. Most queries have multiple positives. BM25 is useful for exact API names and error messages, dense retrieval improves semantic matching, and `reranking_hybrid` is the strongest overall profile by combining exact technical anchors with broader documentation relevance.

## Details

### What the Original Data Measures

FreshStack was introduced to build realistic retrieval benchmarks for technical documents. It focuses on practical developer information needs, recent domains, documentation corpora, community questions, and nugget-level support labels.

RTEB includes FreshStack as an English technical retrieval task. The Nano split asks whether a retriever can connect long developer questions to the documentation or code-adjacent files that support an answer.

### Observed Data Profile

The Nano split contains 200 queries, 3,770 documents, and 1,522 positive qrel rows. Queries average 1,660.21 characters, while documents average 4,983.03 characters. Positives per query average 7.61, with a minimum of 1, a median of 7, and a maximum of 21. There are 189 multi-positive queries, 94.5% of the split.

Example queries involve Godot input behavior, Angular template binding errors, Angular signals without zone.js, Godot Android export cache directories, and Angular server-side rendering with ngrx state.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.2768, hit@10 of 0.6850, and recall@100 of 0.6196. BM25 can match exact framework names, API symbols, error strings, class names, and version-specific terminology.

Its limitation is that technical questions are long and often include code blocks, logs, and narrative debugging context. The relevant document may describe the underlying behavior without repeating the exact phrasing from the question.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.3396, hit@10 of 0.7750, and recall@100 of 0.7523. Dense retrieval improves both top-rank quality and broad coverage over BM25.

This indicates that semantic matching helps map developer problems to relevant documentation sections, especially when the question describes symptoms rather than naming the exact concept.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 4 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.3482, hit@10 of 0.7600, and recall@100 of 0.7674. Hybrid retrieval is the strongest profile for nDCG@10 and recall@100, while dense retrieval has slightly higher hit@10.

This tradeoff is typical for technical documentation search. Sparse retrieval protects exact API and error-token matches, while dense retrieval recovers conceptually relevant docs. The combined pool is especially useful when a query has several supporting documents.

### Metric Interpretation for Model Researchers

Because most queries have multiple positives, nDCG@10 measures whether several supporting documents are ranked early, hit@10 measures whether at least one support appears in the first ten, and recall@100 measures how much support is available for reranking.

For `NanoFreshStack`, hit@10 alone can hide weak coverage. A good retriever should find multiple supporting documents across docs, release notes, and related source text.

### Query and Relevance Type Tendencies

Queries are long developer questions with error messages, code snippets, framework versions, and expected-versus-observed behavior. Relevant documents are technical pages or code-adjacent files that explain the behavior or support an answer.

Relevance is support for the information need. A document can mention the same framework or API and still be wrong if it addresses a different lifecycle hook, version, component, or runtime behavior.

### Representative Failure Modes

Common failures include overmatching API names while missing the relevant behavior, retrieving documentation for the wrong framework version, ranking generic guides above specific troubleshooting sections, and missing support documents when the query uses symptom descriptions. BM25 overweights exact tokens; dense retrieval can blur nearby technical concepts.

### Training Data That May Help

Useful training data includes technical-document retrieval, StackOverflow-to-doc linking, issue-to-doc search, API documentation examples, and hard negatives from the same framework version or symbol family. Evaluation queries, documents, and qrels should be excluded.

### Model Improvement Notes

Models should preserve exact API names, error strings, and versions while learning symptom-to-document semantic matching. Hard negatives should share the same framework, API, or error family but differ in lifecycle, version, or behavior. Hybrid retrieval is the best first-stage profile for broad candidate generation.

## Example Data

### Public Sources

- [FreshStack: Building Realistic Benchmarks for Evaluating Retrieval on Technical Documents](https://arxiv.org/abs/2504.13128), task paper.
- [FreshStack project site](https://fresh-stack.github.io/), project page.
- [mteb/FreshStackRetrieval](https://huggingface.co/datasets/mteb/FreshStackRetrieval), source dataset card.
- [Introducing RTEB: A New Standard for Retrieval Evaluation](https://huggingface.co/blog/rteb), benchmark article.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FreshStack: Building Realistic Benchmarks for Evaluating Retrieval on Technical Documents | 2025 | task paper | https://arxiv.org/abs/2504.13128 |
| FreshStack project site | 2025 | project page | https://fresh-stack.github.io/ |
| mteb/FreshStackRetrieval |  | dataset card | https://huggingface.co/datasets/mteb/FreshStackRetrieval |
| Introducing RTEB: A New Standard for Retrieval Evaluation | 2025 | benchmark article | https://huggingface.co/blog/rteb |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| A Godot user reports delayed button display causing hover state not to update until the mouse moves. | A Godot InputEventMouse class document describes mouse input events. |
| An Angular template fails with a type error involving a `menu-item` binding. | An Angular binding guide explains dynamic text, property, and attribute binding. |
| An Angular 16 signals example does not update after disabling zone.js. | Angular documentation discusses zone pollution and change detection behavior. |
| A Godot Android export creates a `.godot/exported` directory that affects editor behavior. | Godot release-note text discusses export and editor behavior fixes. |
| An Angular SSR application with ngrx has questions about pre-rendered state. | An Angular SSR guide points to the server-side rendering documentation. |
