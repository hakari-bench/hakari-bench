# NanoCodeRAG / NanoCodeRAGProgrammingSolutions

## Overview

NanoCodeRAGProgrammingSolutions is an English code-retrieval task in NanoCodeRAG, sampled from the programming-solutions retrieval source of CodeRAG-Bench. The query is a short natural-language Python programming prompt, and the target document is the compact solution code that implements it.

This task is useful for studying prompt-to-code retrieval. The relevant document may be only a few lines of Python and may share little surface wording with the prompt. A model must map requested behavior, inputs, outputs, and constraints to executable code patterns such as loops, comparisons, tuple operations, divisor checks, and list transformations.

## Details

### What the Original Data Measures

CodeRAG-Bench uses programming solutions as one of its retrieval sources for code-generation support. The benchmark paper describes this source as basic programming problems with canonical solutions, including HumanEval- and MBPP-style examples. Such retrieved snippets can directly support code generation when the prompt asks for a similar function.

This Nano task isolates that prompt-to-solution retrieval setting. The positive document is the code solution associated with the prompt. Relevance depends on exact behavioral implementation, not on shared words.

### Observed Data Profile

This Nano split contains 200 queries, 984 documents, and 200 positive qrels. Each query has exactly one positive solution. Queries average 78.28 characters, and documents average 189.05 characters. Both sides are short, but they use different representational forms.

Observed prompts ask for monotonic-array checks, sums of common divisors, adding a list to a tuple, extracting a minimum-value record from tuples, and comparing divisor sums. Documents are compact Python functions with small loops, comprehensions, imports, or helper functions.

### BM25 Evaluation Profile

BM25 performs extremely poorly on this task. It reaches nDCG@10 of 0.0512, hit@10 of 0.0800, and recall@100 of 0.3650 with a top-500 candidate pool. The prompt and solution often use almost no shared vocabulary. A request for "sum of common divisors" may be implemented with `%`, `range`, and accumulator variables rather than repeated natural-language words.

This is one of the clearest cases where term frequency is not enough. Some queries are very short, and some code snippets contain generic Python tokens that appear everywhere. BM25 may retrieve code with similar imports, keywords, or function names while missing the actual behavior.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is the dominant result, with nDCG@10 of 0.7646, hit@10 of 0.8900, and recall@100 of 0.9650. Dense retrieval substantially outperforms BM25 because it can connect natural-language task descriptions to code semantics.

Dense similarity can associate "check whether an array is monotonic" with comparisons across adjacent elements, or "sum of common divisors" with loops over divisibility tests. The remaining errors likely involve short prompts with common operation words, or near-miss code snippets that solve related but different tasks.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.2151, hit@10 of 0.3550, and recall@100 of 0.9650. It uses top-100 candidates with optional rank-101 safeguards; seven rows contain 101 candidates and seven safeguard-positive rows are recorded. Its recall matches dense retrieval, but its top ranking is much weaker.

This pattern shows that hybrid coverage can be good even when lexical ranking is noisy. The problem is ordering: BM25-style candidates can add many code snippets that share generic Python surface forms but do not implement the requested behavior. Dense retrieval is the better top-rank signal for this task, while a hybrid pool needs a strong semantic reranker.

### Metric Interpretation for Model Researchers

NanoCodeRAGProgrammingSolutions is a dense-dominant prompt-to-code retrieval task. It directly tests whether models can represent algorithmic behavior across natural language and code. BM25's low recall@100 means lexical-only candidate generation would be a serious bottleneck.

The reranking_hybrid profile is also informative: it can recover positives by rank 100 but fails to place them well. This means the key challenge is not only candidate inclusion but behavior-aware ordering among short, similar Python functions.

### Query and Relevance Type Tendencies

Queries are short Python programming prompts. They describe a desired function, transformation, predicate, or computation. Documents are small Python implementations, often without long comments or explanatory prose.

Relevance is exact implementation behavior. A function that solves a neighboring problem, such as product instead of sum or increasing-only instead of monotonic, is non-relevant even if the words look similar.

### Representative Failure Modes

BM25 retrieves generic snippets that share Python keywords, imports, or short identifiers. Dense retrieval may confuse nearby algorithmic tasks, especially when prompts are short and documents are compact. Hybrid retrieval can recover the correct snippet but rank a lexically attractive wrong function above it.

Another failure mode is under-specification. Short prompts may omit examples or edge cases, so many code snippets appear plausible. Strong models need to represent subtle distinctions such as first versus last, sum versus count, and all elements versus adjacent pairs.

### Training Data That May Help

Useful training data includes non-overlapping HumanEval and MBPP style prompt-to-code pairs, APPS and CodeContests natural-language-to-code solutions, CodeSearchNet summary-to-code retrieval pairs, and execution-verified Python functions with behaviorally similar hard negatives.

Leakage filtering is critical because CodeRAG-Bench reports a small programming-solutions source corpus of about 1,100 entries. Training should exclude NanoCodeRAG programming prompts, qrels, positive solution snippets, matching function names, solution bodies, tests, and token fingerprints.

### Model Improvement Notes

Improving this task requires behavior-aware code retrieval. Models should encode control flow, operators, comparisons, helper functions, and edge-case behavior in a way that aligns with natural-language prompts.

For reranking, execution-informed or test-informed signals may be useful. A ranker should prefer code that implements the requested function, not code that merely shares tokens or a broad task category.

## Example Data

| Query | Positive document |
| --- | --- |
| # Write a python function to check whether the given array is monotonic or not. [79 chars] | def is_Monotonic(A): return (all(A[i] <= A[i + 1] for i in range(len(A) - 1)) or all(A[i] >= A[i + 1] for i in range(len(A) - 1))) [149 chars] |
| # Write a python function to find the sum of common divisors of two given numbers. [82 chars] | def sum(a,b): sum = 0 for i in range (1,min(a,b)): if (a % i == 0 and b % i == 0): sum += i return sum [143 chars] |
| # Write a function to add the given list to the given tuples. [61 chars] | def add_lists(test_list, test_tup): res = tuple(list(test_tup) + test_list) return (res) [94 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [CodeRAG-Bench: Can Retrieval Augment Code Generation?](https://arxiv.org/abs/2406.14497) | Benchmark paper describing the retrieval sources and code-generation setting. |
| [CodeRAG-Bench project page](https://code-rag-bench.github.io/) | Project page for the benchmark. |
| [CodeRAG-Bench GitHub](https://github.com/code-rag-bench/code-rag-bench) | Repository for benchmark resources. |
| [code-rag-bench/programming-solutions](https://huggingface.co/datasets/code-rag-bench/programming-solutions) | Public source dataset card. |
| [hakari-bench/NanoCodeRAG](https://huggingface.co/datasets/hakari-bench/NanoCodeRAG) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| Asks for a Python function to check whether an array is monotonic. | A function returns whether all adjacent pairs are nondecreasing or nonincreasing. |
| Asks for the sum of common divisors of two numbers. | A function loops over possible divisors and accumulates values dividing both inputs. |
| Asks to add a list to a tuple. | A function converts the tuple to a list, appends the list contents, and returns a tuple. |
| Asks to extract the record with the minimum indexed value from tuples. | A function uses an itemgetter-style key to select the tuple with the smallest target field. |
| Asks whether two numbers have the same sum of divisors. | Helper code computes divisor sums and compares the results. |
