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
| A teacher wants to create a special team for a project and needs to pick 3 students out of a class of 20. Assuming each student has an equal chance to be selected and the order in which they are chosen doesn't matter, how many different teams can the teacher form? [264 chars] | \section{Multinomial Theorem} Tags: Multinomial Coefficients, Binomial Coefficients, Discrete Mathematics, Proofs by Induction, Algebra \begin{theorem} Let $x_1, x_2, \ldots, x_k \in F$, where $F$ is a field. Then: :$\ds \paren {x_1 + x_2 + \cdots + x_m}^n = \sum_{k_1 \mathop + k_2 \mathop + \mathop \cdots \mathop + k_m \mathop = n} \binom n {k_1, k_2, \ldots, k_m} {x_1}^{k_1} {x_2}^{k_2} \cdots {x_m}^{k_m}$ where: :$m \in \Z_{> 0}$ is a positive integer :$n \in \Z_{\ge 0}$ is a non-negative integer :$\dbinom n {k_1, k_2, \ldots, k_m} = \dfrac {n!} {k_1! \, k_2! \, \cdots k_m!}$ denotes a multinomial coefficient. The sum is taken for all non-negative integers $k_1, k_2, \ldots, k_m$ such that $k_1 + k_2 + \cdots + k_m = n$, and with the understanding that wherever $0^0$ may appear it shall be considered to have a value of $1$. The '''multinomial theorem''' is a generalization of the Binomial Theorem. \end{theorem} \begin{proof} The proof proceeds by induction on $m$. For each $m \in \N... [1,000 / 1,275 chars] |
| Imagine you're a graphic designer working on a 3D modeling project. You have three arrows: the first points 1 unit right, 2 units up, and 3 units forward; the second points 4 units right, 5 units up, and 6 units forward; and the third points 7 units right, 8 units up, and 9 units forward. You can combine arrows by adding any multiple of their right, up, and forward displacements (linear combinations). Can you create a new arrow using a combination of these three without directly tracing any of t... [500 / 504 chars] | \section{Sample Matrix Independence Test} Tags: Linear Second Order ODEs, Linear Algebra \begin{theorem} Let $V$ be a vector space of real or complex-valued functions on a set $J$. Let $f_1, \ldots, f_n$ be functions in $V$. Let '''samples''' $x_1, \ldots, x_n$ from $J$ be given. Define the '''sample matrix''' : :$S = \begin{bmatrix} \map {f_1} {x_1} & \cdots & \map {f_n} {x_1} \\ \vdots & \ddots & \vdots \\ \map {f_1} {x_n} & \cdots & \map {f_n} {x_n} \\ \end{bmatrix}$ Let $S$ be invertible. Then $f_1, \ldots, f_n$ are linearly independent in $V$. \end{theorem} \begin{proof} The definition of linear independence is applied. Assume a linear combination of the functions $f_1, \ldots, f_n$ is the zero function: {{begin-eqn}} {{eqn \| n = 1 \| l = \sum_{i \mathop = 1}^n c_i \map {f_i} x \| r = 0 \| c = for all $x$ }} {{end-eqn}} Let $\vec c$ have components $c_1, \ldots, c_n$. For $i = 1, \ldots, n$ replace $x = x_i$ in $(1)$. There are $n$ linear homogeneous algebraic equations, written as:... [1,000 / 1,157 chars] |
| Suppose you have a square sandbox of dimension 1 inch by 1 inch. You have 19 flags that you are going to plant anywhere in the sandbox. You also have a circular hoop with a radius of $\frac{\sqrt 2}{6}$, which you want to put in the sandbox to include as many flags as possible. What is the minimum number of flags you can ensure will always be within the hoop no matter how the flags are planted in the sandbox? [412 chars] | \section{Pigeonhole Principle} Tags: Pigeonhole Principle, Named Theorems, Combinatorics \begin{theorem} Let $S$ be a finite set whose cardinality is $n$. Let $S_1, S_2, \ldots, S_k$ be a partition of $S$ into $k$ subsets. Then: :at least one subset $S_i$ of $S$ contains at least $\ceiling {\dfrac n k}$ elements where $\ceiling {\, \cdot \,}$ denotes the ceiling function. \end{theorem} \begin{proof} {{AimForCont}} no subset $S_i$ of $S$ has as many as $\ceiling {\dfrac n k}$ elements. Then the maximum number of elements of any $S_i$ would be $\ceiling {\dfrac n k} - 1$. So the total number of elements of $S$ would be no more than $k \paren {\ceiling {\dfrac n k} - 1} = k \ceiling {\dfrac n k} - k$. There are two cases: :$n$ is divisible by $k$ :$n$ is not divisible by $k$. Suppose $k \divides n$. Then $\ceiling {\dfrac n k} = \dfrac n k$ is an integer and: :$k \ceiling {\dfrac n k} - k = n - k$ Thus: :$\ds \card S = \sum_{i \mathop = 1}^k \card {S_i} \le n - k < n$ This contradicts the... [1,000 / 1,575 chars] |

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
