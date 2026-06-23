# NanoRTEB / NanoMBPP

## Overview

`NanoMBPP` is an English short-description-to-code retrieval task from NanoRTEB. The query is a basic Python programming task description, and the relevant document is the matching Python implementation from MBPP. Each query has one positive among 972 code documents. Dense retrieval is overwhelmingly stronger than BM25 for early ranking, while `reranking_hybrid` has the best recall@100 but much weaker nDCG@10 than dense retrieval. The task highlights how short natural-language specifications often require semantic code matching rather than lexical overlap.

## Details

### What the Original Data Measures

MBPP, Mostly Basic Python Programming, was introduced as a benchmark for program synthesis with large language models. It contains entry-level Python tasks, reference programs, and tests.

RTEB converts this generation benchmark into retrieval. The system receives a short task description and must retrieve the correct implementation from a corpus of small Python programs.

### Observed Data Profile

The Nano split contains 200 queries, 972 documents, and 200 positive qrel rows. Every query has exactly one positive. Queries average 78.40 characters, while code documents average 180.80 characters.

Example tasks include checking whether divisor sums are equal, finding the element that occurs an odd number of times, extracting words at least four characters long with regex, counting integral coordinates inside a square, and sorting with comb sort.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.0875, hit@10 of 0.1500, and recall@100 of 0.3700. BM25 is weak for this split.

The reason is that the query is a short natural-language description, while the document is compact Python code. The correct implementation may use variable names, helper functions, or library calls that do not repeat the query terms. Shared words are sparse and often not enough to identify behavior.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.7599, hit@10 of 0.8850, and recall@100 of 0.9400. Dense retrieval is the best first-stage profile by a large margin.

This shows that embedding similarity is highly effective for mapping simple programming intent to implementation behavior. It can connect descriptions of algorithms or operations to code even when exact tokens differ.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 8 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.2305, hit@10 of 0.3500, and recall@100 of 0.9600. Hybrid retrieval improves recall@100 slightly over dense retrieval but is much weaker at early ranking.

This suggests that sparse signals add some candidate coverage but harm top-rank order when mixed into the first-stage ranking. For reranking, the hybrid pool may be useful, but dense retrieval is the better direct ranker.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures how early the exact implementation appears, hit@10 measures whether it appears in the first ten candidates, and recall@100 measures reranker availability.

For `NanoMBPP`, dense nDCG@10 is the clearest quality signal. Hybrid recall@100 is useful only if a strong code-aware reranker follows it.

### Query and Relevance Type Tendencies

Queries are short task descriptions for small Python functions. Relevant documents are concise implementations with loops, conditionals, regex use, arithmetic, or data-structure operations.

Relevance is exact task behavior. A function with similar keywords or algorithmic shape is wrong if it returns a different output or misses a specified condition.

### Representative Failure Modes

Common failures include retrieving a function with similar keywords but different behavior, confusing list and string operations, matching on library names such as `re` without matching the intended pattern, and overranking generic loops. BM25 lacks semantic intent; dense retrieval can still confuse closely related beginner tasks.

### Training Data That May Help

Useful training data includes MBPP-style task-code pairs, docstring-to-code retrieval, introductory Python exercises, and hard negatives from functions with similar keywords but different outputs. Evaluation prompts, implementations, and qrels should be excluded.

### Model Improvement Notes

Models should encode input-output behavior, small algorithmic requirements, and edge cases. Hard negatives should share task vocabulary, function shape, or library use but differ in required behavior. Dense retrieval is the strongest first-stage approach for this task.

## Example Data

| Query | Positive document |
| --- | --- |
| Write a python function to check whether the sum of divisors are same or not. [77 chars] | import math def divSum(n): sum = 1; i = 2; while(i * i <= n): if (n % i == 0): sum = (sum + i +math.floor(n / i)); i += 1; return sum; def areEquivalent(num1,num2): return divSum(num1) == divSum(num2)... [200 / 269 chars] |
| Write a python function to find the element occurring odd number of times. [74 chars] | def get_Odd_Occurrence(arr,arr_size): for i in range(0,arr_size): count = 0 for j in range(0,arr_size): if arr[i] == arr[j]: count+=1 if (count % 2 != 0): return arr[i] return -1 [275 chars] |
| Write a function to find all words which are at least 4 characters long in a string by using regex. [99 chars] | import re def find_char_long(text): return (re.findall(r"\b\w{4,}\b", text)) [80 chars] |
| Write a python function to count the number of integral co-ordinates that lie inside a square. [94 chars] | def count_Intgral_Points(x1,y1,x2,y2): return ((y2 - y1 - 1) * (x2 - x1 - 1)) [83 chars] |
| Write a function to sort a list of elements using comb sort. [60 chars] | def comb_sort(nums): shrink_fact = 1.3 gaps = len(nums) swapped = True i = 0 while gaps > 1 or swapped: gaps = int(float(gaps) / shrink_fact) swapped = False i = 0 while gaps + i < len(nums): if nums[... [200 / 424 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Program Synthesis with Large Language Models | 2021 | task paper | [https://arxiv.org/abs/2108.07732](https://arxiv.org/abs/2108.07732) |
| google-research-datasets/mbpp |  | dataset card | [https://huggingface.co/datasets/google-research-datasets/mbpp](https://huggingface.co/datasets/google-research-datasets/mbpp) |
| Introducing RTEB: A New Standard for Retrieval Evaluation | 2025 | benchmark article | [https://huggingface.co/blog/rteb](https://huggingface.co/blog/rteb) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Check whether the sums of divisors of two numbers are the same. | Code computes divisor sums and compares them. |
| Find the element occurring an odd number of times. | Code counts occurrences and returns an item with odd count. |
| Find all words at least four characters long using regex. | Code uses a regular expression matching word lengths of four or more. |
| Count integral coordinates that lie inside a square. | Code computes the product of interior coordinate counts. |
| Sort a list using comb sort. | Code applies a shrinking gap and swaps out-of-order elements. |
