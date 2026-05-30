# NanoCoIR / NanoApps

## Overview

NanoApps is an English code-retrieval task in NanoCoIR, adapted from the APPS programming-challenge benchmark through CoIR. The query is a full competitive-programming problem statement, often including constraints, examples, and detailed input/output rules. The target document is a Python solution program that solves the stated problem.

This task is useful because it stresses retrieval across a large modality gap. The query is long natural-language algorithmic prose, while the relevant document is compact executable code. A model must infer algorithmic intent from the statement, connect it to implementation structure, and avoid being distracted by solutions for problems that have similar input formats or contest-style wording. It is therefore closer to problem-to-solution retrieval than API search or docstring-code matching.

## Details

### What the Original Data Measures

CoIR converts APPS into a text-to-code retrieval task. APPS itself contains programming problems collected from open-access coding challenge sites, with candidate solutions validated by test cases. In the CoIR formulation, the natural-language problem description becomes the query and code solutions form the searchable corpus.

The original data measures whether a retrieval system can recognize the implementation that satisfies a full algorithmic specification. Relevance depends on behavior, constraints, and input/output semantics, not on the presence of shared identifiers. For example, two programs may both parse integers and loop over test cases, but only one implements the correct greedy, dynamic-programming, graph, arithmetic, or simulation logic for the query.

### Observed Data Profile

This Nano split contains 200 queries, 8,754 documents, and 200 positive qrels. Each query has exactly one positive solution. Queries are long, averaging 1,675.42 characters, while documents average 573.12 characters. This imbalance is central to the task: the problem statement may be several paragraphs, but the correct solution may be a short Python program with sparse natural-language overlap.

Observed queries include competitive-programming stories and mathematical constraints about movement on strings, contest archive validation, repeated attacks on a monster, stick-length adjustment, and digit deletion. Positive documents are concise Python solutions using loops, sorting, arithmetic checks, counters, and standard input parsing. The retrieval problem is to connect those implementation patterns back to the full problem behavior.

### BM25 Evaluation Profile

BM25 performs very poorly on NanoApps. Its nDCG@10 is 0.0084, hit@10 is 0.0150, and recall@100 is 0.0750 with a top-500 candidate pool. Only a small fraction of positives are recovered near the top, which shows that word overlap between problem statements and solution code is usually weak.

This is the expected failure mode for lexical retrieval on APPS-style tasks. Problem statements contain story text, constraints, mathematical notation, and examples. Solution programs contain variable names, control flow, library imports, and arithmetic operations. BM25 can match tokens such as `input`, `print`, numbers, or occasional problem-specific words, but these are rarely sufficient to identify the correct algorithm. In this split, term frequency mostly captures superficial programming boilerplate rather than relevance.

### Dense Evaluation Profile

The dense harrier-oss-270m candidate subset is the strongest among the available profiles, with nDCG@10 of 0.2528, hit@10 of 0.3500, and recall@100 of 0.6700. The dense result is far above BM25, indicating that embedding similarity captures some relationship between algorithmic descriptions and implementation patterns.

The score is still far from saturated. Dense retrieval can often group a statement with solutions that use compatible algorithm families, but it may confuse problems with similar contest structure, similar input signatures, or similar mathematical constraints. Since there is only one positive per query, rank precision is sensitive to near-miss programs that solve a related but different problem. This makes NanoApps a strong diagnostic for whether code retrievers understand full task semantics rather than short textual hints.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.1655, hit@10 of 0.2750, and recall@100 of 0.5400. It uses top-100 candidates with optional rank-101 safeguard rows; 92 rows contain 101 candidates, and 92 safeguard positives were needed. Hybrid retrieval is much better than BM25 but weaker than dense retrieval on this split.

This pattern is informative. Hybrid search usually helps when lexical and dense signals are complementary, but NanoApps has a lexical signal that is extremely noisy. Adding BM25-style evidence can pull in code that shares surface programming tokens without solving the problem. The hybrid set still benefits from dense candidates, yet the dense-only profile is the clearer retrieval signal for this particular task.

### Metric Interpretation for Model Researchers

NanoApps is a dense-favored code retrieval task. The main difficulty is cross-representational matching from long natural-language specifications to short implementations. BM25 failure should not be interpreted as a broken candidate source; it reveals that the relevant evidence is behavioral rather than lexical.

Recall@100 is especially important. Dense retrieval recovers 67.00% of positives by rank 100, while BM25 recovers only 7.50%. This large gap means that a reranker built on BM25-only candidates would miss most correct solutions before reranking begins. For model researchers, NanoApps is a good place to test models that encode algorithms, constraints, and input-output behavior into a shared text-code representation.

### Query and Relevance Type Tendencies

Queries are long contest problem statements. They may contain narrative framing, formal constraints, examples, edge cases, and required output formats. The relevant document is a working Python solution that implements the required algorithm, often with little or no explanatory text.

Relevance is behavioral. A correct solution may use arbitrary variable names and minimal comments, so matching must rely on inferred computation. The model needs to recognize patterns such as scanning a string in fixed jumps, validating identifiers, minimizing adjustment cost, computing repeated attack counts, or counting trailing zeros after digit deletion.

### Representative Failure Modes

A frequent failure mode is retrieving a solution with the same input shape but a different algorithm. Many competitive-programming programs read `n`, arrays, strings, or multiple test cases, so shallow code structure is not enough. Another failure mode is over-weighting story words from the query, which often never appear in the code.

Dense systems may retrieve solutions from the right broad family but miss a constraint-specific detail, such as whether the optimization is over all target lengths, whether obstacles block movement, or whether a monster can be defeated in one step. Hybrid systems may inherit these semantic errors while also adding boilerplate-heavy lexical distractors.

### Training Data That May Help

Useful training data includes APPS-style problem-to-solution pairs, competitive-programming solutions with hard negatives, and long specification-to-code retrieval data. Hard negatives should be selected from programs with similar input formats or similar algorithm families but different required behavior.

Leakage control matters. The Nano split is derived from CoIR APPS test-side retrieval data. Training should exclude NanoApps queries, qrels, and positive solution documents, and should not train on APPS test-derived rows. A safer filter removes rows by normalized query text, normalized solution text, and token-fingerprint overlap.

### Model Improvement Notes

Improving NanoApps requires better alignment between natural-language problem semantics and code behavior. Stronger models should represent constraints, examples, and algorithmic objectives, not just topic words or code tokens. Pretraining or contrastive training over full problem statements and verified solutions is likely more useful than short docstring-code pairs alone.

Evaluation should also inspect candidate recall before reranking. A reranker cannot recover positives that are absent from the candidate pool, and BM25 candidates are especially weak here. Dense candidate generation is the more appropriate base for this task, with reranking focused on distinguishing near-miss solutions that share broad structure.

## Example Data

### Public Sources

NanoApps is documented through the CoIR benchmark paper and the APPS task paper. The public APPS dataset card is also relevant because it describes the source programming-challenge data used by CoIR.

### Source Reference Table

| Source | Role |
| --- | --- |
| [CoIR: A Comprehensive Benchmark for Code Information Retrieval Models](https://arxiv.org/abs/2407.02883) | Benchmark paper that adapts APPS and other code resources into retrieval tasks. |
| [Measuring Coding Challenge Competence With APPS](https://arxiv.org/abs/2105.09938) | Source task paper for the programming-problem benchmark. |
| [codeparrot/apps](https://huggingface.co/datasets/codeparrot/apps) | Public Hugging Face dataset card for APPS. |
| [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A story-style problem about moving along a line with obstacles and fixed jump length. | A short Python program scans the string from the starting mark in fixed increments and checks whether the target can be reached before an obstacle. |
| A contest-archive cleanup problem with mixed file names and numeric references. | The solution parses records, tracks valid numeric identifiers, and prints the corrected archive status. |
| A repeated-attack problem where each action damages and then regenerates monster heads. | The program compares the maximum one-shot damage and net damage to compute the minimum number of blows. |
| A stick-length adjustment problem asking for the cheapest common target length. | The solution enumerates candidate lengths and sums adjustment costs after allowing a one-unit tolerance. |
| A digit-deletion problem requiring divisibility by a power of ten. | The program scans digits from the end to count zeros and computes the minimum deletions needed. |
