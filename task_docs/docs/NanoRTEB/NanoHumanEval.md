# NanoRTEB / NanoHumanEval

## Overview

`NanoHumanEval` is an English docstring-to-code retrieval task from NanoRTEB. The query is a compact Python programming task description, and the relevant document is the corresponding implementation body from HumanEval. Each query has one positive among 158 code documents. Dense retrieval is strong because it captures specification-to-implementation semantics, while `reranking_hybrid` has the best nDCG@10 and matched recall@100. BM25 is useful but weaker because short code bodies often do not share enough surface text with the natural-language description.

## Details

### What the Original Data Measures

HumanEval was introduced to evaluate large language models trained on code. The original benchmark contains hand-written Python programming problems, tests, and reference-like function behavior for functional-correctness evaluation.

RTEB converts the generation setting into retrieval. The model receives the function description as a query and must retrieve the matching implementation body. This makes the task closer to semantic code search than competitive-programming retrieval.

### Observed Data Profile

The Nano split contains 158 queries, 158 documents, and 158 positive qrel rows. Every query has exactly one positive. Queries average 291.16 characters, while code documents average 176.99 characters.

Example tasks include filtering strings by prefix, computing maximum nested-parentheses depth, checking whether a number is a product of three primes, counting fruit items from a string description, and validating balanced brackets.

### BM25 Evaluation Profile

The BM25 candidate subset uses the full 158-document pool and reaches nDCG@10 of 0.3405, hit@10 of 0.5443, and recall@100 of 0.9051. BM25 works when descriptions and code share variable names, operators, or literal strings.

The weakness is semantic compression. A short implementation can satisfy a long docstring without repeating its words, and many Python functions share common tokens such as loops, returns, list comprehensions, or helper names.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses the full 158-document pool and reaches nDCG@10 of 0.5666, hit@10 of 0.7975, and recall@100 of 0.9937. Dense retrieval is the best profile for top-ten hit rate.

This shows that embedding similarity captures function-level intent better than lexical matching. It can connect a description such as checking balanced brackets to a stack or depth-counting implementation even when wording differs.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 1 row receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.5770, hit@10 of 0.7405, and recall@100 of 0.9937. Hybrid retrieval slightly improves nDCG@10 over dense retrieval while sharing the same recall@100.

The result suggests that sparse code tokens and dense function semantics are complementary for early ordering. Exact symbols help when the query names operations or literals, while dense similarity handles the core specification.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures how early the exact implementation appears, hit@10 measures whether it is in the first ten candidates, and recall@100 measures whether a reranker can access it.

For `NanoHumanEval`, the candidate pool is small, so recall is high for dense and hybrid retrieval. The main research signal is early ranking among compact implementations with similar Python structure.

### Query and Relevance Type Tendencies

Queries are concise function specifications, sometimes with examples or constraints. Relevant documents are short Python implementation bodies. The task often requires mapping natural language to control flow, string operations, arithmetic, or list processing.

Relevance is exact specification-to-implementation correspondence. Code with similar structure is wrong if it implements a different edge case or returns a different value.

### Representative Failure Modes

Common failures include retrieving a function with similar loop structure, confusing string and list tasks, overmatching shared variable names, and ranking a plausible but semantically different implementation. BM25 overweights tokens; dense retrieval can blur nearby algorithmic intentions.

### Training Data That May Help

Useful training data includes docstring-to-code retrieval, Python function search, unit-test-linked code examples, and hard negatives from functions with similar signatures or control flow. Evaluation prompts, implementations, and qrels should be excluded.

### Model Improvement Notes

Models should represent function intent, input-output behavior, and edge cases. Hard negatives should share variable names, operations, or control flow while differing in specification. Hybrid retrieval is a strong first-stage choice because exact code tokens and semantic function matching both matter.

## Example Data

### Public Sources

- [Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374), task paper.
- [openai/openai_humaneval](https://huggingface.co/datasets/openai/openai_humaneval), source dataset card.
- [Introducing RTEB: A New Standard for Retrieval Evaluation](https://huggingface.co/blog/rteb), benchmark article.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Evaluating Large Language Models Trained on Code | 2021 | task paper | https://arxiv.org/abs/2107.03374 |
| openai/openai_humaneval |  | dataset card | https://huggingface.co/datasets/openai/openai_humaneval |
| Introducing RTEB: A New Standard for Retrieval Evaluation | 2025 | benchmark article | https://huggingface.co/blog/rteb |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Filter a list of strings to those that start with a given prefix. | A list comprehension using `startswith(prefix)`. |
| Return the deepest nesting level for groups of parentheses. | Code tracks current and maximum depth while scanning characters. |
| Return true if a number is the product of three prime numbers. | Code checks primality and searches prime factor triples. |
| Determine how many mango fruits are in a described basket. | Code extracts numeric counts from the string and subtracts them. |
| Check whether every opening bracket has a closing bracket. | Code updates a depth counter and rejects negative depth. |
