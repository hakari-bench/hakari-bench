# NanoBRIGHT / NanoBrightPony

## Overview

NanoBrightPony is the Pony programming-language documentation retrieval slice of NanoBRIGHT. Queries are coding tasks that must be solved in Pony, and relevant documents are short manual passages describing the syntax, control flow, operators, errors, primitives, or library features needed for implementation. The task is useful for evaluating retrieval in a rare programming language where the query describes a programming goal but the relevant text explains language constructs.

## Details

### What the Original Data Measures

BRIGHT includes Pony as a rare-language code retrieval task. The query typically contains a natural-language problem and a Pony function template. Positives are documentation passages from the Pony manual that a programmer would need to implement the solution. This is different from retrieving solution code: the relevant document may explain loops, variables, operators, collections, or error handling rather than the algorithm itself.

The task measures whether a retriever can infer implementation requirements from a coding problem. A task about summing unique elements may require local variables, loops, array access, comparison, and arithmetic. Those manual passages may not repeat the problem's story words, so direct lexical overlap is weak.

### Observed Data Profile

The task contains 112 queries, 6,183 documents, and 2,219 relevance judgments. It is almost entirely multi-positive: there are 19.81 positives per query on average, a minimum of 1, a median of 21.0, a maximum of 28, and 111 multi-positive queries, or 99.11% of the set.

Queries average 388.97 characters and documents average 306.50 characters. The short document length means positives are fine-grained manual passages. The high number of positives reflects that one programming task may require many language features, not just one exact section.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.0496, hit@10 of 0.3304, and recall@100 of 0.2438 using the top-500 BM25 candidate subset. These scores are low, but BM25 is still stronger than dense retrieval for recall@100. Lexical matching helps when templates or problem statements contain terms that overlap with manual language, such as array, operator, variable, loop, or string.

The weakness is that many necessary constructs are implicit. A query may not say "infix operator" or "local variable" even when the solution requires those manual sections. BM25 therefore misses relevant documentation when the implementation step must be inferred rather than named.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.0219, hit@10 of 0.1429, and recall@100 of 0.0518. Dense retrieval is the weakest profile here. General embedding similarity appears poor at connecting LeetCode-style tasks and Pony syntax documentation.

This is a useful caution for rare-language documentation retrieval. A dense model may understand the broad programming problem but still fail to map it to the exact language features. The semantic gap between "solve this algorithmic task" and "read this Pony manual section" is larger than ordinary text similarity.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.0780, hit@10 of 0.4375, and recall@100 of 0.1717. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 8 safeguard rows, candidate counts from 100 to 101, and a mean of 100.07 candidates.

The hybrid profile is best for nDCG@10 and hit@10, but BM25 remains better for recall@100. This means combining sparse and dense signals improves the very top of the ranking, while the dense component can reduce the broader relevant-document coverage compared with BM25 alone. For reranking, hybrid gives a more useful first page, but BM25 may expose more total positives.

### Metric Interpretation for Model Researchers

This task is difficult because relevance is implementation-dependency retrieval. The best nDCG@10 is only 0.0780, and even hit@10 under the hybrid profile is 0.4375. A model needs to infer which Pony constructs are needed from the coding problem and then retrieve manual passages that explain those constructs.

Researchers should not interpret low dense scores as a simple language-domain mismatch only. The deeper issue is that the query and positive document occupy different roles: task description versus documentation. Strong systems may need code-generation traces, tool-use supervision, or explicit labels connecting tasks to language features.

### Query and Relevance Type Tendencies

Queries describe programming tasks such as reducing stones, summing unique elements, counting good pairs, manipulating digits, or checking string properties, usually with a Pony template. Positive passages describe local variables, infix or unary operators, control structures, loops, strings, arrays, and other manual topics.

The relevance relation is functional: a document is relevant if it teaches a construct needed to implement the task. Many positives can be valid for one query because a complete solution may need multiple syntax features.

### Representative Failure Modes

Likely failures include retrieving manual passages that share a word with the problem but are not needed, missing implicit constructs such as loops or comparisons, confusing algorithmic similarity with language documentation relevance, and under-ranking common manual sections that are required across many tasks.

BM25 fails when construct names are absent from the query. Dense retrieval fails when it embeds the programming story but not the implementation requirements. Hybrid retrieval improves the first page but can still miss many relevant manual fragments.

### Training Data That May Help

Useful training data includes non-overlapping Pony documentation retrieval pairs, rare-language coding tasks with documentation references, API documentation search pairs, and program-synthesis examples labeled with required language constructs.

Synthetic data should generate Pony coding tasks with templates and map each task to the exact manual sections needed to solve it. Hard negatives should discuss nearby constructs, such as related operators or control structures, that look plausible but would not implement the task.

### Model Improvement Notes

Strong systems for this task should model a chain from task to implementation plan to documentation need. Sparse matching is important because exact construct names are decisive when present. Dense models need domain-specific training that links programming tasks to manual concepts rather than only code or natural-language similarity.

The observed scores suggest that reranking_hybrid is the best top-10 pool, but BM25 should not be discarded for broader candidate generation. A reranker trained on task-to-documentation relevance could improve substantially over both profiles.

## Example Data

| Query | Positive document |
| --- | --- |
| I will use the programming language pony. Problem: You are given an array of integers stones where s... [100 / 730 chars] | So first we ask if there are any more names to get. If there are then we get a name and see if it's "Jack" or "Jill". If it is we're done and we break out of the loop, handing back the name we've foun... [200 / 676 chars] |
| I will use the programming language pony. Problem: You are given an integer array nums. The unique e... [100 / 323 chars] | We can see that it makes more sense for the unary operator to be applied before either infix as it only acts on a single number in the expression so it is never ambiguous. Unary operators can also be... [200 / 380 chars] |
| I will use the programming language pony. Problem: Given an array of integers nums, write a function... [100 / 281 chars] | # Local variables Local variables in Pony work very much as they do in other languages, allowing you to store temporary values while you perform calculations. Local variables live within a chunk of co... [200 / 1,245 chars] |
| I will use the programming language pony. Problem: Given an integer number n, write a function that... [100 / 370 chars] | # Infix Operators Infix operators take two operands and are written between those operands. Arithmetic and comparison operators are the most common: ```pony 1 + 2 a < b ``` Pony has pretty much the sa... [200 / 248 chars] |
| I will use the programming language pony. Problem: A string s is nice if, for every letter of the al... [100 / 592 chars] | So first we ask if there are any more names to get. If there are then we get a name and see if it's "Jack" or "Jill". If it is we're done and we break out of the loop, handing back the name we've foun... [200 / 676 chars] |

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
| Implement a stone-smashing array problem in Pony. | A manual passage explains looping and breaking out of repeated control flow. |
| Return the sum of array elements that appear exactly once. | A documentation passage explains unary operators and precedence behavior. |
| Count good index pairs in an integer array. | A Pony manual section describes local variables and scoped temporary values. |
| Compute the product-minus-sum value of the digits of an integer. | A manual passage explains infix arithmetic and comparison operators. |
| Check whether a string is nice with matching uppercase and lowercase letters. | A control-flow passage explains repeated checks and stopping conditions. |
