# NanoBRIGHT / NanoBrightAops

## Overview

NanoBrightAops is the compact NanoBRIGHT slice for AoPS-style math competition retrieval. Each query is a full mathematical problem, and relevant documents are solved problems that rely on the same underlying problem-solving skill. The retrieval goal is not to find the same story, notation, or formula, but to find problems whose solutions use similar reasoning. This makes the task useful for evaluating reasoning-intensive retrieval, mathematical skill matching, and multi-positive retrieval over worked contest problems.

## Details

### What the Original Data Measures

BRIGHT was introduced as a benchmark for reasoning-intensive retrieval where relevance often requires "level 3" reasoning rather than lexical or direct semantic overlap. In the AoPS slice, math competition problems are associated with solution skills or theorems. A positive document is another solved problem whose solution requires the same skill as the query.

This is different from ordinary math text retrieval. Two relevant problems may use different variables, stories, numbers, diagrams, and answer formats. The model must infer the technique, such as parity, Vieta's formulas, triangle inequalities, median facts, or geometric angle chasing, rather than simply matching surface notation.

### Observed Data Profile

The task contains 111 queries, 10,000 documents, and 524 relevance judgments. It is strongly multi-positive, with an average of 4.72 positives per query. The minimum is 1, the median is 4.0, the maximum is 8, and 109 queries are multi-positive, or 98.20% of the set.

Queries average 319.61 characters, while documents average 549.07 characters. Queries are contest-style math prompts with formulas, LaTeX notation, multiple-choice answers, and geometric or combinatorial setups. Documents are solved problems or problem-solution passages. The relevant relation is solution skill, not shared wording.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.1433, hit@10 of 0.5135, and recall@100 of 0.6336 using the top-500 BM25 candidate subset. This is a weak-to-moderate lexical profile. BM25 can find positives when problems share explicit mathematical objects, such as triangles, medians, Fibonacci numbers, or integer side lengths.

The limitation is clear: many same-skill problems look lexically unrelated. A counting problem and a geometry problem may share no story terms even if both require the same combinatorial idea. BM25 therefore acts mainly as a surface-topic candidate generator and misses many reasoning equivalents.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.2623, hit@10 of 0.6847, and recall@100 of 0.7118. Dense retrieval is the strongest direct top-rank profile. It improves nDCG@10 and hit@10 substantially over BM25, showing that embedding similarity can capture some problem-structure and skill similarity beyond exact terms.

The score is still far from solved. Math skill matching requires recognizing the hidden solution method, and a general dense retriever may conflate topic, notation, and difficulty with actual theorem or technique. Dense retrieval helps, but reasoning-specific training is still needed.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.2167, hit@10 of 0.5946, and recall@100 of 0.7500. It uses a top-100 candidate range with an optional rank-101 safeguard; this slice has 5 safeguard rows, candidate counts from 100 to 101, and a mean of 100.05 candidates. Hybrid has the best recall@100, while dense retrieval has the best top-10 ranking.

This suggests that hybrid search is useful for candidate completeness. BM25 preserves exact mathematical terms and notation, while dense retrieval adds structural similarity. A downstream reranker with access to solution reasoning could use the high-recall hybrid pool effectively.

### Metric Interpretation for Model Researchers

Because nearly every query has multiple positives, hit@10 is not enough. nDCG@10 measures whether several same-skill problems are ranked early, while recall@100 measures whether a reranker can access the broader skill cluster. The dense top-rank lead and hybrid recall lead should be read as complementary strengths.

The comparison shows that BM25 is limited by surface mismatch, dense retrieval is better for direct skill-like matching, and reranking_hybrid gives the broadest candidate pool. This task is a compact test of whether retrieval models can retrieve by reasoning pattern.

### Query and Relevance Type Tendencies

Queries include cyclic quadrilateral counting, angle bisectors in right triangles, integer equations involving quadratic expressions, triangle medians and areas, and mean-median-mode conditions. Positive documents can look quite different but share a theorem, counting method, algebraic recurrence, or geometric observation.

The task rewards abstracting from problem statement to solution method. A relevant document may not share the same objects, and an irrelevant document may share many terms while requiring a different technique.

### Representative Failure Modes

Likely failures include retrieving problems with the same mathematical nouns but different methods, missing same-skill problems with different stories, over-ranking similar notation, and under-covering multi-positive skill clusters. BM25 is too literal, while dense retrieval can still confuse topical similarity with solution equivalence.

### Training Data That May Help

Useful training data includes non-overlapping math competition problems with worked solutions, theorem- or skill-labeled problem pairs, AoPS-style explanations, and hard negatives from nearby topics but different skills. Multi-positive objectives are important because each skill may have several valid problem matches.

### Model Improvement Notes

A model targeting this task should represent solution strategy, not just problem text. Sparse systems need math-aware tokenization but will remain limited. Dense systems should train on worked-solution and skill labels. Hybrid systems are useful candidate generators because exact notation and semantic structure both contribute to recall.

## Example Data

| Query | Positive document |
| --- | --- |
| Two quadrilaterals are considered the same if one can be obtained from the other by a rotation and a translation. How many different convex cyclic quadrilaterals are there with integer sides and perimeter equal to 32? $\textbf{(A)}\ 560 \qquad \textbf{(B)}\ 564 \qquad \textbf{(C)}\ 568 \qquad \textbf{(D)}\ 1498 \qquad \textbf{(E)}\ 2255$ [339 chars] | How many non-congruent triangles with perimeter 7 have integer side lengths? The longest side cannot be greater than 3, since otherwise the remaining two sides would not be long enough to form a triangle. The only possible triangles have side lengths $1$--$3$--$3$ or $2$--$2$--$3$. Hence the answer is $\boxed{2}.$ [315 chars] |
| In the diagram below, angle $ABC$ is a right angle. Point $D$ is on $\overline{BC}$, and $\overline{AD}$ bisects angle $CAB$. Points $E$ and $F$ are on $\overline{AB}$ and $\overline{AC}$, respectively, so that $AE=3$ and $AF=10$. Given that $EB=9$ and $FC=27$, find the integer closest to the area of quadrilateral $DCFG$. [323 chars] | Consider the set of all triangles $OPQ$ where $O$ is the origin and $P$ and $Q$ are distinct points in the plane with nonnegative integer coordinates $(x,y)$ such that $41x + y = 2009$. Find the number of such distinct triangles whose area is a positive integer. Let the two points $P$ and $Q$ be defined with coordinates; $P=(x_1,y_1)$ and $Q=(x_2,y_2)$ We can calculate the area of the parallelogram with the determinant of the matrix of the coordinates of the two points(shoelace theorem). $\det \left(\begin{array}{c} P \\ Q\end{array}\right)=\det \left(\begin{array}{cc}x_1 &y_1\\x_2&y_2\end{array}\right).$ Since the triangle has half the area of the parallelogram, we just need the determinant to be even. The determinant is \[(x_1)(y_2)-(x_2)(y_1)=(x_1)(2009-41(x_2))-(x_2)(2009-41(x_1))=2009(x_1)-41(x_1)(x_2)-2009(x_2)+41(x_1)(x_2)=2009((x_1)-(x_2))\] Since $2009$ is not even, $((x_1)-(x_2))$ must be even, thus the two $x$'s must be of the same parity. Also note that the maximum value fo... [1,000 / 1,183 chars] |
| Determine the maximum value of $m^2 + n^2$, where $m$ and $n$ are integers satisfying $m, n \in \{ 1,2, \ldots , 1981 \}$ and $( n^2 - mn - m^2 )^2 = 1$. [153 chars] | The Fibonacci sequence $1,1,2,3,5,8,13,21,\ldots$ starts with two 1s, and each term afterwards is the sum of its two predecessors. Which one of the ten digits is the last to appear in the units position of a number in the Fibonacci sequence? $\textbf{(A)} \ 0 \qquad \textbf{(B)} \ 4 \qquad \textbf{(C)} \ 6 \qquad \textbf{(D)} \ 7 \qquad \textbf{(E)} \ 9$ Note that any digits other than the units digit will not affect the answer. So to make computation quicker, we can just look at the Fibonacci sequence in $\bmod{10}$: $1,1,2,3,5,8,3,1,4,5,9,4,3,7,0,7,7,4,1,5,6,....$ The last digit to appear in the units position of a number in the Fibonacci sequence is $6 \Longrightarrow \boxed{\mathrm{C}}$. [705 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original benchmark paper | [BRIGHT](https://arxiv.org/abs/2407.12883) |
| Project page | [BRIGHT project page](https://brightbenchmark.github.io/) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| NanoBRIGHT dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |

Representative query and positive problem snippets:

| Query | Positive document snippet |
| --- | --- |
| How many convex cyclic quadrilaterals have integer sides and perimeter 32? | How many non-congruent triangles with perimeter 7 have integer side lengths? |
| A right-triangle angle-bisector problem with points on two sides. | A lattice-coordinate triangle counting problem constrained by a linear equation. |
| Maximize m^2 + n^2 subject to an integer quadratic equation. | A Fibonacci sequence problem asks which digit appears last in the units position. |
| A triangle problem with medians, an angle bisector, and an area target. | A triangle median problem uses a right triangle formed by median intersection lengths. |
| Mean, median, and mode of seven values are all equal to x. | A consecutive-integer sum problem uses the relation between mean and median. |
