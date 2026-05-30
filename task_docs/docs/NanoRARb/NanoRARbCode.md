# NanoRARb / NanoRARbCode

## Overview

`NanoRARbCode` is an English code reasoning retrieval task from NanoRARb. Queries are programming prompts, function signatures, and docstrings, while documents are candidate code implementations. Each query has one positive implementation. The task measures whether a retriever can map behavioral specifications to executable code, not merely match identifiers. BM25 and dense retrieval are both weak, with BM25 slightly ahead of dense, while `reranking_hybrid` is the strongest profile because it combines identifier overlap with semantic specification matching.

## Details

### What the Original Data Measures

RAR-b includes a code reasoning retrieval task built from program-synthesis and code-search style data. It uses HumanEvalPack and MBPP-style evaluation prompts, with answer corpora enlarged using code-search and instruction-tuned code data. Source references include CodeSearchNet and OctoPack.

In this task, the document is the code answer itself. A correct retrieval model must connect a natural-language specification and function signature to a code snippet that implements the required behavior.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Every query has exactly one positive. Queries average 470.08 characters, and code documents average 256.00 characters.

Examples include summing ASCII codes for uppercase characters, collecting odd values from a Collatz sequence, returning a rounded average as binary, producing rolling maxima, and swapping case or reversing strings under conditions. Queries often include docstrings and examples; positives are compact Python implementations.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.1318, hit@10 of 0.2150, and recall@100 of 0.4450. BM25 is slightly stronger than dense retrieval. It benefits from shared function names, identifiers, literals, and API words between prompt and implementation.

However, lexical retrieval remains weak. Many correct implementations use different variable names or concise logic that does not repeat the full behavioral specification. Matching words is not the same as matching program semantics.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.1173, hit@10 of 0.2000, and recall@100 of 0.4350. Dense retrieval is close to BM25 but slightly weaker. This suggests that general-purpose embedding similarity has limited ability to represent executable behavior from code snippets.

Dense retrieval may capture broad task type, such as string processing or list iteration, but still fail to distinguish exact conditions, return formats, and edge cases.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 85 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.1773, hit@10 of 0.3000, and recall@100 of 0.5750. Hybrid retrieval is clearly strongest.

The result shows that code retrieval benefits from combining sparse identifiers and literals with semantic task similarity. BM25 contributes exact names and syntax; dense retrieval contributes broader functional similarity. A reranker can exploit the combined pool to judge behavior more precisely.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures how early the correct implementation appears, hit@10 measures whether it is in the first ten candidates, and recall@100 measures whether a reranker can see it.

For NanoRARbCode, top-rank scores remain low. A strong system needs program-semantic retrieval or reranking that can reason about examples, edge cases, and code behavior.

### Query and Relevance Type Tendencies

Queries are code prompts with signatures, docstrings, and sometimes examples. Relevant documents are code snippets, often function bodies. The target relation is implementation correctness.

Relevance is behavioral. A candidate can share identifiers or APIs and still be wrong if it fails the specified edge case or output format.

### Representative Failure Modes

Common failures include matching function names without behavior, confusing similar string or list transformations, missing output-format requirements such as binary conversion, and selecting code that handles common cases but fails edge cases. Dense retrieval can blur tasks with similar structure; BM25 can overvalue identifiers and comments.

### Training Data That May Help

Useful training data includes code search, docstring-to-code retrieval, unit-test-backed program synthesis pairs, and HumanEval or MBPP-style tasks outside the evaluation queries. Evaluation prompts and solutions should be excluded.

### Model Improvement Notes

Models should learn specification-to-implementation semantics. Hard negatives should share identifiers, APIs, or control-flow shape but fail tests or edge cases. Hybrid candidate generation is valuable, but final ranking likely needs code-aware reranking or execution-informed supervision.

## Example Data

### Public Sources

- [RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347), benchmark paper.
- [CodeSearchNet Challenge: Evaluating the State of Semantic Code Search](https://arxiv.org/abs/1909.09436), source reference.
- [OctoPack: Instruction Tuning Code Large Language Models](https://arxiv.org/abs/2308.07124), source reference.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | https://arxiv.org/abs/2404.06347 |
| CodeSearchNet Challenge: Evaluating the State of Semantic Code Search | 2019 | arXiv paper | https://arxiv.org/abs/1909.09436 |
| OctoPack: Instruction Tuning Code Large Language Models | 2023 | arXiv paper | https://arxiv.org/abs/2308.07124 |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Implement `digitSum`, returning the sum of ASCII codes for uppercase characters only. | Return 0 for an empty string and sum `ord(char)` for uppercase characters. |
| Implement `get_odd_collatz`, returning sorted odd numbers in a Collatz sequence. | Build odd values while iterating Collatz updates and return the sorted list. |
| Implement `rounded_avg`, averaging integers from `n` through `m` and returning binary. | Return -1 when `m < n`; otherwise sum the range and return `bin(round(...))`. |
| Implement `rolling_max` over a list of integers. | Track a running maximum and append it for each element. |
| Implement `solve`, swapping case for letters or reversing when no letters exist. | Swap alphabetic character case, track whether any letter was seen, and reverse otherwise. |
