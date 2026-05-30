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
| Find a path through a grid while removing a limited number of obstacles. | A solved grid problem uses deque-based search over empty and obstacle cells. |
| Two people water plants from opposite ends with capacity constraints. | A related watering problem tracks remaining water while traversing plants in order. |
| Count or characterize islands in a binary grid. | A positive document implements an island-style grid traversal or perimeter routine. |
| Find the longest chain of ordered pairs. | A related sequence problem uses longest-increasing-subsequence-style dynamic programming. |
| Solve a take-turns number game with winning conditions. | A related game problem computes optimal play over possible guesses or states. |
