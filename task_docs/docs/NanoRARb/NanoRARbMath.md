# NanoRARb / NanoRARbMath

## Overview

`NanoRARbMath` is an English mathematical reasoning retrieval task from NanoRARb. It recasts math problem solving as retrieval: the query is a math word problem or formal problem, and the relevant document is the corresponding worked solution or answer text. Each query has one positive solution. Unlike many short-answer NanoRARb tasks, BM25 is already strong because problems and solutions often share equations, symbols, variables, and named quantities. Dense retrieval is stronger for top-rank quality, while `reranking_hybrid` gives the best recall@100.

## Details

### What the Original Data Measures

RAR-b builds a pooled numerical reasoning retrieval task from MATH and GSM8K-style evaluation questions, with MetaMathQA-style answer material used to enlarge the corpus. Related source tasks include grade-school word problems, competition-style mathematical problem solving, and synthetic or bootstrapped math reasoning data.

In this retrieval setting, the target is not a general textbook passage. It is the solution text that corresponds to the query problem. The model must connect problem statements to the correct derivation among many math solutions.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Every query has exactly one positive. Queries average 201.33 characters, while solution documents average 481.33 characters.

Examples include triangle geometry, rotation matrices, inverse trigonometric simplification, angle-addition identities, and law-of-cosines transformations. Positive documents often contain formulas, intermediate derivations, and final answers.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.6147, hit@10 of 0.7900, and recall@100 of 0.9450. This is a strong sparse profile. Mathematical notation, variables, expressions, and named operations are frequently repeated from problem to solution.

BM25 is therefore far more effective here than in many commonsense NanoRARb tasks. Its limitation is that shared symbols can also appear in near-miss solutions that solve a different quantity or apply a different transformation.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.7818, hit@10 of 0.8850, and recall@100 of 0.9400. Dense retrieval is the strongest top-rank profile. It improves ranking quality even though its recall@100 is slightly below BM25.

This suggests that embeddings capture some mathematical problem-solution relation beyond symbol overlap. Dense retrieval can connect a problem to the kind of derivation needed, not only to repeated notation.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with five rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.7350, hit@10 of 0.8700, and recall@100 of 0.9750. Hybrid retrieval has the best candidate coverage but lower top-rank quality than dense retrieval.

This is a useful split for separating first-stage ranking from reranking pool quality. Dense retrieval is better as a ranked list, while hybrid retrieval gives a reranker the broadest access to the gold solution.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures how early the correct solution appears, hit@10 measures whether it is in the first ten results, and recall@100 measures whether a later reranker can see it.

For NanoRARbMath, BM25 is a serious baseline because of notation overlap, dense retrieval is the best top-rank baseline, and hybrid retrieval is the best coverage baseline. Improvements should demonstrate mathematical reasoning alignment, not just equation matching.

### Query and Relevance Type Tendencies

Queries are math problems with variables, diagrams encoded as text, trigonometric expressions, geometry conditions, or algebraic constraints. Relevant documents are worked solutions with derivation steps and final values.

Relevance is exact problem-solution correspondence. A solution with similar symbols or topic is wrong if it solves a different problem or reaches a different result.

### Representative Failure Modes

Common failures include retrieving a solution with similar formulas but a different target quantity, confusing angle identities, matching geometry diagrams by variable names rather than constraints, and selecting a generic worked solution that shares notation but not the problem. BM25 overweights symbol overlap; dense retrieval can still blur similar solution templates.

### Training Data That May Help

Useful training data includes math problem-to-solution retrieval, GSM8K and MATH-style reasoning pairs outside the evaluation examples, verifier data, and synthetic worked solutions with near-miss distractors. Evaluation queries, solutions, and answer-pool entries should be excluded.

### Model Improvement Notes

Models should learn to align a mathematical problem with the correct derivation path. Hard negatives should share symbols, equation forms, or topic tags but solve a different value or apply an invalid step. Hybrid candidate generation is useful for reranking, but top-rank models should reason over mathematical structure.

## Example Data

| Query | Positive document |
| --- | --- |
| Problem: Let $ABC$ be a triangle with $\angle A = 45^\circ$. Let $P$ be a point on side $\overline{BC}$ with $PB = 3$ and $PC = 5$. Let $O$ be the circumcenter of triangle $ABC$. Determine the length $OP$. [205 chars] | Using the extended Sine law, we find the circumradius of $ABC$ to be $R = \frac{BC}{2\sin A} = 4\sqrt 2$. [asy] unitsize(0.8 cm); pair A, B, C, O, P; A = (0,0); B = (2,2); C = (5,0); P = interp(B,C,3/8); O = circumcenter(A,B,C); draw(A--B--C--cycle); draw(circumcircle(A,B,C)); draw(O--P); label("$A$", A, W); label("$B$", B, N); label("$C$", C, E); dot("$O$", O, S); dot("$P$", P, NE); [/asy] By considering the power of point $P$, we find that $R^2 - OP^2 = PB \cdot PC = 15$. So $OP = \sqrt{R^2 - 15} = \sqrt{ 16 \cdot 2 - 15} = \boxed{\sqrt{17}}$. [557 chars] |
| Problem: Find the matrix that corresponds to rotating about the origin by an angle of $45^\circ$ clockwise. [107 chars] | The transformation that rotates about the origin by an angle of $45^\circ$ clockwise takes $\begin{pmatrix} 1 \\ 0 \end{pmatrix}$ to $\begin{pmatrix} 1/\sqrt{2} \\ -1/\sqrt{2} \end{pmatrix}$ and $\begin{pmatrix} 0 \\ 1 \end{pmatrix}$ to $\begin{pmatrix} 1/\sqrt{2} \\ 1/\sqrt{2} \end{pmatrix},$ so the matrix is \[\boxed{\begin{pmatrix} 1/\sqrt{2} & 1/\sqrt{2} \\ -1/\sqrt{2} & 1/\sqrt{2} \end{pmatrix}}.\] [406 chars] |
| Problem: Compute $\sin^{-1} (\sin 3) + \sin^{-1} (\sin 4) + \sin^{-1} (\sin 5).$ All functions are in radians. [111 chars] | Since $\sin (\pi - 3) = \sin 3$ and $-\frac{\pi}{2} \le \pi - 3 \le \frac{\pi}{2},$ \[\sin^{-1} (\sin 3) = \pi - 3.\]Since $\sin (\pi - 4) = \sin 4$ and $-\frac{\pi}{2} \le \pi - 4 \le \frac{\pi}{2},$ \[\sin^{-1} (\sin 4) = \pi - 4.\]Since $\sin (5 - 2 \pi) = \sin 5$ and $-\frac{\pi}{2} \le 5 - 2 \pi \le \frac{\pi}{2},$ \[\sin^{-1} (\sin 5) = 5 - 2 \pi.\]Therefore, \[\sin^{-1} (\sin 3) + \sin^{-1} (\sin 4) + \sin^{-1} (\sin 5) = (\pi - 3) + (\pi - 4) + (5 - 2 \pi) = \boxed{-2}.\] [484 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | [https://arxiv.org/abs/2404.06347](https://arxiv.org/abs/2404.06347) |
| Training Verifiers to Solve Math Word Problems | 2021 | arXiv paper | [https://arxiv.org/abs/2110.14168](https://arxiv.org/abs/2110.14168) |
| Measuring Mathematical Problem Solving With the MATH Dataset | 2021 | arXiv paper | [https://arxiv.org/abs/2103.03874](https://arxiv.org/abs/2103.03874) |
| MetaMath: Bootstrap Your Own Mathematical Questions for Large Language Models | 2023 | arXiv paper | [https://arxiv.org/abs/2309.12284](https://arxiv.org/abs/2309.12284) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| A geometry problem asks for `OP` in a triangle with angle `A = 45` degrees and side segments on `BC`. | A solution uses the extended sine law to compute the circumradius and derive the requested length. |
| Find the matrix for a 45-degree clockwise rotation about the origin. | A solution maps basis vectors to rotated coordinates and forms the rotation matrix. |
| Compute a sum of inverse-sine expressions in radians. | A solution rewrites each term using principal-value identities such as `sin(pi - x) = sin x`. |
| Find an angle from a tangent expression involving sine and cosine addition formulas. | A solution applies angle-addition identities to simplify numerator and denominator. |
| Determine possible values of angle `C` from an equation involving `a`, `b`, and `c`. | A solution applies the law of cosines and squares the relation to constrain `cos C`. |
