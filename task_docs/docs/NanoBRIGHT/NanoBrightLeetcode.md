# NanoBRIGHT / NanoBrightLeetcode

## Overview

NanoBrightLeetcode is the LeetCode-style coding retrieval slice of NanoBRIGHT. Queries are full algorithmic programming problem statements, and relevant documents are solved problems that share the same algorithmic design or data-structure technique. The task is useful for evaluating whether retrieval models can see past story wording, variable names, and examples to identify problems that require similar solution strategies.

## Details

### What the Original Data Measures

BRIGHT includes LeetCode as a reasoning-intensive code and algorithm retrieval task. The query is a programming problem, while positives are similar solved problems. Documents can include a problem statement, constraints, examples, and a Python solution. Relevance is based on algorithmic similarity, not simple duplicate text.

This means the task measures retrieval over latent solution structure. Two problems may both require BFS, dynamic programming, greedy scheduling, union-find, monotonic stacks, or game-state search, even when their surface stories differ. Conversely, two problems can share words about arrays, grids, plants, or games while requiring different methods.

### Observed Data Profile

The task contains 142 queries, 10,000 documents, and 262 relevance judgments. It has 1.85 positives per query on average, with a minimum of 1, a median of 1.0, a maximum of 5, and 70 multi-positive queries, or 49.30% of the set.

Queries average 1,459.30 characters, which reflects full problem statements with examples and constraints. Documents average 1,079.62 characters and often include code plus explanatory problem text. The unusually long queries make this task different from ordinary code search: the retriever must compress a complete problem into an algorithmic representation.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2655, hit@10 of 0.5493, and recall@100 of 0.7939 using the top-500 BM25 candidate subset. Lexical matching is helpful when related problems share terms such as grid, obstacle, island, chain, subsequence, watering, or game.

The limitation is that story-level overlap is not the same as algorithmic equivalence. A grid problem may require shortest path, connected components, dynamic programming, or flood fill. An array problem may require greedy choice, binary search, or prefix sums. BM25 can often find related-looking problems, but it cannot reliably identify the shared solution pattern.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.3024, hit@10 of 0.6127, and recall@100 of 0.8168. Dense retrieval improves over BM25 on every reported metric, which suggests that embedding similarity captures some algorithmic abstraction beyond token overlap.

Dense retrieval is useful when two problem statements use different surface narratives but encode the same computational structure. It can connect obstacle-removal grid search to shortest-path variants, interval chains to subsequence-style dynamic programming, or game descriptions to minimax or DP formulations. Still, the margin over BM25 is modest, showing that general text embeddings only partially capture algorithmic reasoning.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.3048, hit@10 of 0.6268, and recall@100 of 0.8550. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 12 safeguard rows, candidate counts from 100 to 101, and a mean of 100.08 candidates.

The hybrid profile is the strongest across all reported metrics, although dense is close for nDCG@10. This indicates that both sources of evidence matter. BM25 preserves useful cues from constraints, entities, and data-structure names, while dense retrieval better captures abstract algorithmic similarity. The combined pool is the best observed starting point for reranking.

### Metric Interpretation for Model Researchers

This task is a good diagnostic for whether a retrieval model has learned code-problem semantics rather than only text similarity. BM25's high recall@100 relative to its low nDCG@10 shows that exact words can place positives somewhere in the pool, but the top ranking requires stronger reasoning about algorithms. Dense improves the ranking, and reranking_hybrid improves both hit@10 and recall@100.

Researchers should pay attention to differences between broad topical retrieval and solution-pattern retrieval. A model that retrieves any grid problem is not necessarily useful; the relevant problem should share the transformation or algorithm needed to solve the query. Rerankers should compare constraints, allowed operations, objective functions, and state transitions.

### Query and Relevance Type Tendencies

Queries are full coding problems about grids, obstacles, watering simulations, islands, pair chains, guessing games, arrays, graphs, and dynamic programming states. Positive documents may include Python implementations and problem statements that use different stories but similar methods.

The relevance relation is algorithmic analogy. A positive is often another problem whose solution technique transfers to the query. Matching examples, variable names, or object nouns is less important than matching graph traversal, recurrence design, greedy ordering, search state, or data structure.

### Representative Failure Modes

Likely failures include retrieving problems with the same data type but a different algorithm, over-ranking story similarity, missing a positive because the target uses different nouns, and treating code text as ordinary prose without understanding the solution pattern.

BM25 tends to over-weight repeated statement words. Dense retrieval can over-match broad programming concepts while missing constraints that change the solution. Hybrid retrieval improves coverage, but a final model still needs to reason over examples, constraints, and algorithm categories.

### Training Data That May Help

Useful training data includes non-overlapping coding-problem similarity pairs, solved algorithm problems with tags, code-search and algorithm explanation pairs, and hard negatives that share input types but require a different method.

Synthetic data should generate complete programming problems with examples, constraints, and reference solutions. Positives should use the same algorithmic idea despite different story wording. Hard negatives should use similar objects or data structures but require a different design, such as BFS versus DP or greedy versus exhaustive search.

### Model Improvement Notes

Strong systems should encode both natural-language problem statements and solution structure. Sparse matching helps retain constraints and named data structures. Dense retrieval helps find analogous problems across different wording. Code-aware reranking or late interaction over constraints, examples, and solution snippets is likely useful.

The observed scores make reranking_hybrid the best candidate source for this slice. However, the small gap between dense and hybrid at nDCG@10 suggests that improvements should focus on algorithmic discrimination rather than only broader candidate recall.

## Example Data

| Query | Positive document |
| --- | --- |
| You are given a **0-indexed** 2D integer array `grid` of size `m x n`. Each cell has one of two values: * `0` represents an **empty** cell, * `1` represents an **obstacle** that may be removed. You can move up, down, left, or right from and to an empty cell. Return _the **minimum** number of **obstacles** to **remove** so you can move from the upper left corner_ `(0, 0)` _to the lower right corner_ `(m - 1, n - 1)`. **Example 1:** **Input:** grid = \[\[0,1,1\],\[1,1,0\],\[1,1,0\]\] **Output:** 2... [500 / 1,162 chars] | from collections import deque """You are given an `m x n` integer matrix `grid` where each cell is either `0` (empty) or `1` (obstacle). You can move up, down, left, or right from and to an empty cell in **one step**. Return _the minimum number of **steps** to walk from the upper left corner_ `(0, 0)` _to the lower right corner_ `(m - 1, n - 1)` _given that you can eliminate **at most**_ `k` _obstacles_. If it is not possible to find such walk return `-1`. **Example 1:** **Input:** grid = \[\[0,0,0\],\[1,1,0\],\[0,0,0\],\[0,1,1\],\[0,0,0\]\], k = 1 **Output:** 6 **Explanation:** The shortest path without eliminating any obstacle is 10. The shortest path with one obstacle elimination at position (3,2) is 6. Such path is (0,0) -> (0,1) -> (0,2) -> (1,2) -> (2,2) -> **(3,2)** -> (4,2). **Example 2:** **Input:** grid = \[\[0,1,1\],\[1,1,1\],\[1,0,0\]\], k = 1 **Output:** -1 **Explanation:** We need to eliminate at least two obstacles to find such a walk. **Constraints:** * `m == grid.lengt... [1,000 / 2,061 chars] |
| Alice and Bob want to water `n` plants in their garden. The plants are arranged in a row and are labeled from `0` to `n - 1` from left to right where the `ith` plant is located at `x = i`. Each plant needs a specific amount of water. Alice and Bob have a watering can each, **initially full**. They water the plants in the following way: * Alice waters the plants in order from **left to right**, starting from the `0th` plant. Bob waters the plants in order from **right to left**, starting from the... [500 / 2,955 chars] | from collections import defaultdict """You want to water `n` plants in your garden with a watering can. The plants are arranged in a row and are labeled from `0` to `n - 1` from left to right where the `ith` plant is located at `x = i`. There is a river at `x = -1` that you can refill your watering can at. Each plant needs a specific amount of water. You will water the plants in the following way: * Water the plants in order from left to right. * After watering the current plant, if you do not have enough water to **completely** water the next plant, return to the river to fully refill the watering can. * You **cannot** refill the watering can early. You are initially at the river (i.e., `x = -1`). It takes **one step** to move **one unit** on the x-axis. Given a **0-indexed** integer array `plants` of `n` integers, where `plants[i]` is the amount of water the `ith` plant needs, and an integer `capacity` representing the watering can capacity, return _the **number of steps** needed to... [1,000 / 3,089 chars] |
| You are given an `m x n` binary matrix `grid`. An island is a group of `1`'s (representing land) connected **4-directionally** (horizontal or vertical.) You may assume all four edges of the grid are surrounded by water. The **area** of an island is the number of cells with a value `1` in the island. Return _the maximum **area** of an island in_ `grid`. If there is no island, return `0`. **Example 1:** **Input:** grid = \[\[0,0,1,0,0,0,0,1,0,0,0,0,0\],\[0,0,0,0,0,0,0,1,1,1,0,0,0\],\[0,1,1,0,1,0,0... [500 / 979 chars] | def islandPerimeter(grid): """You are given `row x col` `grid` representing a map where `grid[i][j] = 1` represents land and `grid[i][j] = 0` represents water. Grid cells are connected **horizontally/vertically** (not diagonally). The `grid` is completely surrounded by water, and there is exactly one island (i.e., one or more connected land cells). The island doesn't have "lakes ", meaning the water inside isn't connected to the water around the island. One cell is a square with side length 1. The grid is rectangular, width and height don't exceed 100. Determine the perimeter of the island. **Example 1:** **Input:** grid = \[\[0,1,0,0\],\[1,1,1,0\],\[0,1,0,0\],\[1,1,0,0\]\] **Output:** 16 **Explanation:** The perimeter is the 16 yellow stripes in the image above. **Example 2:** **Input:** grid = \[\[1\]\] **Output:** 4 **Example 3:** **Input:** grid = \[\[1,0\]\] **Output:** 4 **Constraints:** * `row == grid.length` * `col == grid[i].length` * `1 <= row, col <= 100` * `grid[i][j]` is `... [1,000 / 1,442 chars] |

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
| Find a path through a grid while removing a limited number of obstacles. | A solved grid problem uses deque-based search over empty and obstacle cells. |
| Two people water plants from opposite ends with capacity constraints. | A related watering problem tracks remaining water while traversing plants in order. |
| Count or characterize islands in a binary grid. | A positive document implements an island-style grid traversal or perimeter routine. |
| Find the longest chain of ordered pairs. | A related sequence problem uses longest-increasing-subsequence-style dynamic programming. |
| Solve a take-turns number game with winning conditions. | A related game problem computes optimal play over possible guesses or states. |
