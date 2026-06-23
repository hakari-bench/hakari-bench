# NanoBRIGHT / NanoBrightTheoremQATheorems

## Overview

NanoBrightTheoremQATheorems is the theorem-definition retrieval slice of NanoBRIGHT. Queries are applied mathematical or scientific problems, and relevant documents are theorem statements, definitions, or proof-oriented entries used in the solution. The task evaluates whether retrieval systems can infer the formal theorem behind an applied prompt and retrieve the corresponding theorem document.

## Details

### What the Original Data Measures

BRIGHT aligns TheoremQA-style queries with theorem statements from sources such as ProofWiki. The query is a concrete scenario or problem, while the relevant document is a formal theorem statement or definition. This creates an even sharper query-document mismatch than the question-retrieval version: the user-facing problem and the theorem page may share very little wording.

The task measures theorem identification. A model must infer that a scenario about placing flags, arranging guests, coloring tournament edges, or computing combinations requires a particular theorem such as the Pigeonhole Principle, Ramsey's Theorem, a permutation construction, or a binomial or multinomial identity.

### Observed Data Profile

The task contains 76 queries, 10,000 documents, and 151 relevance judgments. It has 1.99 positives per query on average, a minimum of 1, a median of 2.0, a maximum of 7, and 47 multi-positive queries, or 61.84% of the set.

Queries average 415.62 characters, and documents average 401.12 characters. Documents are compact theorem statements or proof snippets with mathematical tags. The corpus therefore contains many formal pages that are lexically similar to one another but only a few are theorem-equivalent to the query.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.0198, hit@10 of 0.0526, and recall@100 of 0.1457 using the top-500 BM25 candidate subset. This is an extremely weak lexical profile. Exact word overlap rarely identifies the theorem because applied prompts use story language and theorem pages use formal names, assumptions, and notation.

The weakness is expected and informative. A query about flags in a sandbox may require the Pigeonhole Principle without saying "pigeonhole." A tournament-coloring story may require Ramsey's Theorem without naming it. BM25 cannot reliably infer these hidden theorem links.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.1653, hit@10 of 0.3553, and recall@100 of 0.4305. Dense retrieval is the strongest profile across the reported metrics. It improves substantially over BM25, showing that semantic representations capture some relation between applied problem structure and theorem text.

Even so, the absolute scores remain modest. Formal theorem retrieval requires mathematical abstraction that general embeddings only partially capture. A strong model needs to connect scenario constraints to theorem assumptions and conclusion forms.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.0895, hit@10 of 0.2237, and recall@100 of 0.4106. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 30 safeguard rows, candidate counts from 100 to 101, and a mean of 100.39 candidates.

Hybrid retrieval improves greatly over BM25 but remains below dense retrieval on all headline metrics. Sparse signals add some coverage for mathematical tags and shared objects, but the fused ranking is hurt by lexical mismatch. Dense retrieval is the best observed first-stage method for this theorem-definition task.

### Metric Interpretation for Model Researchers

This is one of the clearest dense-over-BM25 tasks in NanoBRIGHT. BM25 almost fails because theorem relevance is implicit. Dense retrieval provides meaningful gains, but the remaining gap shows that theorem retrieval is not solved by generic semantic similarity.

Researchers should treat this as a problem-to-theorem alignment benchmark. The relevant document is a formal object needed for the solution. Models should be judged on whether they recover the theorem, not whether they find a same-topic math page.

### Query and Relevance Type Tendencies

Queries include applied counting, graph, linear algebra, combinatorics, probability, and geometry scenarios. Positive documents are theorem pages such as multinomial theorem, sample matrix independence tests, pigeonhole principle, permutation construction, and Ramsey's Theorem.

The relevance relation is necessity for solution. A theorem page is positive if that theorem is needed to solve the query. A document with similar tags but a different theorem is a hard negative.

### Representative Failure Modes

Likely failures include retrieving theorem pages from the same mathematical area but with the wrong conclusion, matching symbols or tags without matching assumptions, missing the theorem name when it is implicit, and confusing related combinatorial tools such as combinations, permutations, pigeonhole arguments, and Ramsey theory.

BM25 is especially poor because the query rarely contains the theorem title. Dense retrieval can still confuse neighboring theorem concepts. Hybrid retrieval helps only when lexical tags align, and can under-rank theorem-equivalent pages when formal wording differs.

### Training Data That May Help

Useful training data includes theorem-labeled problem datasets, ProofWiki-style theorem retrieval, symbolic math problem-to-theorem pairs, and hard negatives from the same mathematical area but a different theorem.

Synthetic data should generate applied math scenarios from theorem statements, then train retrieval to the theorem definition or proof page. Positives should be theorem statements actually needed in the solution. Hard negatives should share tags such as graph theory, linear algebra, or combinatorics while not supporting the solution.

### Model Improvement Notes

Strong systems should infer theorem candidates from problem structure. Dense retrieval is the strongest observed baseline, but theorem-aware training, symbolic feature extraction, or reranking over assumptions and conclusions is likely necessary for large gains.

The low BM25 score makes this task a good stress test for models that claim mathematical reasoning in retrieval. Improvements should focus on mapping story problems to formal theorem statements, not on surface paraphrase.

## Example Data

| Query | Positive document |
| --- | --- |
| A teacher wants to create a special team for a project and needs to pick 3 students out of a class o... [100 / 264 chars] | \section{Multinomial Theorem} Tags: Multinomial Coefficients, Binomial Coefficients, Discrete Mathematics, Proofs by Induction, Algebra \begin{theorem} Let $x_1, x_2, \ldots, x_k \in F$, where $F$ is... [200 / 1,275 chars] |
| Imagine you're a graphic designer working on a 3D modeling project. You have three arrows: the first... [100 / 504 chars] | \section{Sample Matrix Independence Test} Tags: Linear Second Order ODEs, Linear Algebra \begin{theorem} Let $V$ be a vector space of real or complex-valued functions on a set $J$. Let $f_1, \ldots, f... [200 / 1,157 chars] |
| Suppose you have a square sandbox of dimension 1 inch by 1 inch. You have 19 flags that you are goin... [100 / 412 chars] | \section{Pigeonhole Principle} Tags: Pigeonhole Principle, Named Theorems, Combinatorics \begin{theorem} Let $S$ be a finite set whose cardinality is $n$. Let $S_1, S_2, \ldots, S_k$ be a partition of... [200 / 1,575 chars] |
| Imagine you're organizing a small dinner party with 8 friends and you have 2 identical round tables... [100 / 274 chars] | \section{Construction of Permutations} Tags: Factorials, Combinatorics, Counting Arguments, Permutation Theory, Construction of Permutations, Permutations \begin{theorem} The ${}^n P_n$ permutations o... [200 / 520 chars] |
| Imagine you're organizing a tournament with teams from different cities, and each match can end in o... [100 / 525 chars] | \section{Ramsey's Theorem} Tags: Ramsey Theory, Named Theorems, Combinatorics \begin{theorem} In any coloring of the edges of a sufficiently large complete graph, one will find monochromatic complete... [200 / 1,743 chars] |

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
| Pick 3 students from a class when order does not matter. | A theorem page states a multinomial or binomial coefficient identity. |
| Determine whether three vectors in a 3D modeling scenario are independent. | A theorem page gives a matrix-based independence test. |
| Place 19 flags in a unit square and guarantee a small hoop can cover some pair. | A theorem page states the Pigeonhole Principle. |
| Seat 8 friends at two identical round tables without leaving one empty. | A theorem page describes construction and counting of permutations. |
| Find guaranteed patterns in a two-color tournament graph. | A theorem page states Ramsey's Theorem for monochromatic complete subgraphs. |
