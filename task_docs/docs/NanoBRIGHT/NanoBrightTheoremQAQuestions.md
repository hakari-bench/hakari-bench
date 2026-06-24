# NanoBRIGHT / NanoBrightTheoremQAQuestions

## Overview

NanoBrightTheoremQAQuestions is the TheoremQA question-retrieval slice of NanoBRIGHT. Queries are applied or story-like mathematical and scientific questions, while relevant documents are solved STEM problems that require the same theorem or underlying method. The task evaluates whether retrieval systems can identify shared mathematical reasoning when the surface wording, setting, and objects differ.

## Details

### What the Original Data Measures

BRIGHT uses TheoremQA-derived questions to create a theorem-centered retrieval task. Questions are rewritten as concrete scenarios while preserving the theorem required for the solution. A document is positive when it is a solved problem that uses the same theorem, not merely when it shares the same story or keywords.

This makes the task a reasoning-abstraction benchmark. A party, family tree, road trip, graph, or counting story may correspond to a formal theorem in combinatorics, graph theory, calculus, algebra, probability, or linear algebra. The retrieval system must infer the mathematical structure behind the prompt.

### Observed Data Profile

The task contains 194 queries, 10,000 documents, and 439 relevance judgments. It has 2.26 positives per query on average, a minimum of 1, a median of 2.0, a maximum of 7, and 116 multi-positive queries, or 59.79% of the set.

Queries average 425.64 characters, and documents average 543.43 characters. Both sides are short enough for passage retrieval, but lexical overlap is intentionally unreliable because the query may be a concrete scenario while the document is a solved formal problem.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.1646, hit@10 of 0.3608, and recall@100 of 0.4875 using the top-500 BM25 candidate subset. These scores are low relative to many practical-domain BRIGHT tasks. Lexical matching helps only when the query and solved problem share mathematical objects such as graph, coefficient, group, or vertex cover.

The limitation is fundamental: the positive relation is theorem equivalence, not word overlap. A query about selecting students may require the same counting theorem as a binomial expansion problem. BM25 often misses this because the concrete scenarios deliberately obscure the shared theorem.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.2798, hit@10 of 0.5670, and recall@100 of 0.6241. Dense retrieval is the strongest profile for nDCG@10 and hit@10. It improves substantially over BM25, showing that embedding similarity captures some theorem-level or mathematical-intent relation beyond terms.

Dense retrieval is still far from solved. It can connect applied prompts to related solved problems, but theorem identity often requires symbolic reasoning or structured mathematical abstraction. The results show meaningful semantic gains without eliminating the need for specialized math-aware reranking.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.2316, hit@10 of 0.5000, and recall@100 of 0.6560. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 38 safeguard rows, candidate counts from 100 to 101, and a mean of 100.20 candidates.

Hybrid retrieval has the best recall@100 but does not beat dense retrieval for top-10 ranking. This means sparse signals can help expose additional positives, but the fused order is less effective than dense ranking for placing theorem-equivalent problems near the top.

### Metric Interpretation for Model Researchers

This task is a dense-favorable theorem-abstraction benchmark. BM25 is weak because surface terms do not define relevance. Dense retrieval gives the best first-page quality, while reranking_hybrid gives the broadest candidate coverage for downstream reranking.

Researchers should evaluate whether retrieved problems share the actual theorem, not whether they share mathematical vocabulary. A graph query and a graph document can be unrelated if one asks for vertex cover and the other asks for acyclicity. Conversely, very different stories can be relevant when they use the same theorem.

### Query and Relevance Type Tendencies

Queries include applied scenarios about family trees, selecting students, group order, elevation functions, graph coverage, tournaments, probability, and algebraic formulas. Positive documents are solved STEM problems that use the same theorem or method, such as binomial theorem, group order, vertex cover, or graph-cycle criteria.

The relevance relation is method-level equivalence. Documents are relevant because their solution depends on the same theorem, not because they are paraphrases.

### Representative Failure Modes

Likely failures include matching story objects rather than theorem structure, retrieving solved problems from the same broad area but with a different theorem, missing a positive when the theorem is implicit, and confusing related concepts such as combinations, binomial expansion, permutations, and multinomial coefficients.

BM25 is vulnerable to scenario mismatch. Dense retrieval can still confuse nearby mathematical ideas. Hybrid retrieval improves coverage but needs a math-aware reranker to restore dense-like top precision while keeping recall.

### Training Data That May Help

Useful training data includes non-overlapping theorem-labeled STEM problems, TheoremQA train-style questions, solved problems grouped by theorem, and hard negatives from the same broad topic but using a different theorem.

Synthetic data should generate applied scenarios from theorem-labeled solved problems while preserving the required theorem. Positives should be solved problems using the same theorem, not paraphrases of the same story. Hard negatives should share mathematical objects but require a different theorem.

### Model Improvement Notes

Strong models should build theorem-aware representations. Dense retrieval is the strongest observed first-stage method, but specialized training on problem-to-theorem and problem-to-problem equivalence is likely needed. Reranking should compare required assumptions, mathematical objects, and solution steps rather than only text similarity.

The observed hybrid recall advantage suggests a practical pipeline: use hybrid or dense-plus-sparse candidate generation, then apply a theorem-aware reranker or symbolic reasoning layer.

## Example Data

| Query | Positive document |
| --- | --- |
| Imagine you have a family tree of 100 members, and you're trying to figure out how many ways you can assign one person to be the 'ancestor' such that the family tree still makes sense with everyone else coming after them in the lineage. How many different ways can you do this? [277 chars] | If there exists an ordered numbering of the nodes such that for each node there are no links going to a lower-numbered node, then there are no directed cycles in a directed graph. True or false? True. If there exists an ordered numbering of the nodes such that for each node there are no links going to a lower-numbered node, then it means that the graph can be topologically sorted. A topological sort of a directed acyclic graph (DAG) is a linear ordering of its vertices such that for every directed edge uv from vertex u to vertex v, u comes before v in the ordering. Therefore, if a graph can be topologically sorted, it must be a DAG, which means there are no directed cycles in the graph. Therefore, the answer is True. [730 chars] |
| A teacher wants to create a special team for a project and needs to pick 3 students out of a class of 20. Assuming each student has an equal chance to be selected and the order in which they are chosen doesn't matter, how many different teams can the teacher form? [264 chars] | What is the coefficient of $x^2y^5$ for the formula $(x + 2y)^7$? We can use the binomial theorem to expand $(x+2y)^7$ as follows: $$(x+2y)^7 = \sum_{k=0}^{7} \binom{7}{k} x^{7-k}(2y)^k$$ To find the coefficient of $x^2y^5$, we need to find the term in the expansion where $x$ has exponent 2 and $y$ has exponent 5. This occurs when $k=5$, so we can substitute $k=5$ into the formula above to get: $$\binom{7}{5} x^{7-5}(2y)^5 = 21x^2(32y^5) = 672x^2y^5$$ Therefore, the coefficient of $x^2y^5$ for the formula $(x+2y)^7$ is $\boxed{672}$. [539 chars] |
| You're organizing a book club represented by the group S_3 * Z_2. What is its order? [84 chars] | What is the order of group Z_{18}? The order of a group is the number of elements in the group. In this case, Z_{18} is the group of integers modulo 18 under addition. The elements of this group are {0, 1, 2, ..., 17}. Therefore, the order of group Z_{18} is 18. Therefore, the answer is 18. [293 chars] |

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
| Choose an ancestor in a family tree so all relationships still make sense. | A solved graph problem states a criterion for directed graphs with no cycles. |
| Pick 3 students from a class when order does not matter. | A solved binomial-expansion problem uses combinatorial coefficients. |
| Find the order of a group formed from smaller groups. | A solved problem computes the order of a modular arithmetic group. |
| Reason about elevation gain along a path from sea level to a mountain. | A solved calculus-style problem analyzes function behavior and existence. |
| Place cameras to cover roads in a small neighborhood graph. | A solved graph problem asks for a minimum vertex cover. |
