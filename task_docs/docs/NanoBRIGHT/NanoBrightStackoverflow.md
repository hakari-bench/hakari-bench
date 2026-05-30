# NanoBRIGHT / NanoBrightStackoverflow

## Overview

NanoBrightStackoverflow is the Stack Overflow slice of NanoBRIGHT. Queries are developer questions with code snippets, configuration context, platform details, and symptoms, while relevant documents are cited passages such as API documentation, technical references, blog posts, or framework pages. The task evaluates whether retrieval systems can find the source that explains the API behavior, language feature, command, or configuration needed to resolve a programming issue.

## Details

### What the Original Data Measures

BRIGHT's StackExchange construction uses real posts as queries and cited or validated sources as positives. For Stack Overflow, this creates a practical documentation retrieval task: the answer may depend on a JavaScript comparator rule, a WinSCP command, a DAX function, a C++ constexpr limitation, or a framework-specific configuration behavior.

The task measures more than code-token overlap. A query can contain long code blocks, failed attempts, environment descriptions, and user interpretation. The relevant passage may explain a general API rule or platform behavior that solves the issue without repeating the exact code.

### Observed Data Profile

The task contains 117 queries, 10,000 documents, and 478 relevance judgments. It has 4.09 positives per query on average, a minimum of 1, a median of 2.0, a maximum of 59, and 81 multi-positive queries, or 69.23% of the set.

Queries average 1,292.97 characters and documents average 1,120.63 characters. Both sides are relatively long for passage retrieval, often including snippets, command examples, API signatures, or documentation excerpts. This makes the task sensitive to both exact identifiers and semantic interpretation.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3685, hit@10 of 0.5897, and recall@100 of 0.6506 using the top-500 BM25 candidate subset. Sparse retrieval is useful because Stack Overflow questions frequently contain exact API names, language constructs, command flags, function names, product names, and error fragments.

The limitation is that a query can contain many incidental identifiers. BM25 may match the wrong part of a code snippet or retrieve a same-library page that does not explain the behavior. It is strong, but not enough to capture symptom-to-documentation relations by itself.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.4033, hit@10 of 0.5726, and recall@100 of 0.7469. Dense retrieval improves nDCG@10 and recall@100 over BM25, though BM25 has a slightly higher hit@10. This indicates that semantic matching helps find supporting documentation beyond exact token overlap.

Dense retrieval is useful when the question describes a desired behavior or failure symptom and the source explains the underlying API concept. It can connect code examples to documentation about comparator contracts, random functions, launch options, policy filters, or compile-time constructs.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.4686, hit@10 of 0.7009, and recall@100 of 0.8096. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 14 safeguard rows, candidate counts from 100 to 101, and a mean of 100.12 candidates.

The hybrid profile is strongest across all reported metrics. It benefits from exact API names and error tokens while also capturing semantic links between symptoms and documentation. For Stack Overflow-style retrieval, the observed data strongly supports using sparse and dense signals together.

### Metric Interpretation for Model Researchers

This task is a practical hybrid-search benchmark. BM25 is strong because exact identifiers matter. Dense retrieval is strong because many questions describe behavior rather than naming the exact concept. Reranking_hybrid combines both and gives the best top-10 ranking and candidate coverage.

Researchers should evaluate whether models distinguish the document that solves the issue from merely related documentation. Hit@10 is important for whether a developer sees at least one useful source, while recall@100 matters for downstream reranking, answer generation, or tool-assisted documentation lookup.

### Query and Relevance Type Tendencies

Queries include JavaScript table sorting, SFTP file operations, DAX row-level security, JSON-only LLM responses, C++ constexpr initialization, framework configuration, SQL behavior, and scripting issues. Positive documents include MDN-style references, Microsoft Learn pages, WinSCP documentation, cppreference pages, OpenAI documentation, and technical blog passages.

The relevance relation is operational support. A positive passage explains the API rule, command option, platform behavior, or language feature needed to fix or implement the user's task.

### Representative Failure Modes

Likely failures include matching the same library but the wrong API, over-ranking code-token overlap that does not solve the problem, missing a relevant documentation page because the query describes a symptom, and confusing user attempts with the actual needed concept.

BM25 is vulnerable to noisy code snippets and incidental identifiers. Dense retrieval can overlook exact function names or version-specific details. Hybrid retrieval reduces both risks, but final reranking still needs to judge whether the source resolves the issue.

### Training Data That May Help

Useful training data includes non-overlapping Stack Overflow questions with cited links, documentation retrieval and API usage examples, issue-to-document troubleshooting pairs, and hard negatives from the same library or framework but a different failure mode.

Synthetic data should generate developer questions with realistic code snippets, environment details, and symptoms. Positives should explain the API behavior or configuration needed to solve the issue. Hard negatives should share names and syntax but not address the actual problem.

### Model Improvement Notes

Strong systems should combine exact matching for identifiers with semantic matching for behavior. Query decomposition can help identify the language, framework, error, attempted code, and desired outcome. Rerankers should be trained to prefer authoritative documentation or precise explanatory passages over generally related pages.

The observed metrics make reranking_hybrid the best candidate source for this task. Improvements should focus on grounding the match in the specific API behavior and filtering out same-library distractors.

## Example Data

### Public Sources

The original task is based on BRIGHT's reasoning-intensive retrieval benchmark, with NanoBRIGHT providing the compact dataset packaging.

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original benchmark paper | [BRIGHT](https://arxiv.org/abs/2407.12883) |
| Project page | [BRIGHT project page](https://brightbenchmark.github.io/) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| NanoBRIGHT dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |

Representative query and positive source snippets:

| Query | Positive document snippet |
| --- | --- |
| Sort a JavaScript-populated table body by internal IP number. | A JavaScript reference passage explains comparator consistency and sort behavior. |
| Copy and delete masked files from an SFTP folder using WinSCP. | A WinSCP documentation passage describes client commands and scripting behavior. |
| Implement DAX row-level security using LOOKUPVALUE. | A Microsoft documentation page explains DAX function behavior and evaluation context. |
| Force an LLM agent to respond only with JSON strings. | A model documentation passage discusses generation behavior and implementation guidance. |
| Initialize a constexpr C++ array with generated values. | A cppreference-style page explains compile-time utility constructs. |
