# MNanoBEIR / NanoBEIR-ja / NanoTouche2020

## Overview

`NanoBEIR-ja__NanoTouche2020` is the Japanese NanoBEIR version of the Touché
2020 argument retrieval benchmark for controversial questions. The task uses
Japanese translated debate questions as queries and asks a retriever to rank
Japanese translated argument documents that address each issue. The Nano split
contains 49 queries, 5,745 documents, and 932 positive qrels. Every query is
multi-positive, with 19.02 positives per query on average. This makes the task
a broad argument retrieval benchmark: finding at least one relevant argument is
usually easy, but ranking substantive and diverse arguments above topical
mentions is harder.

## Details

### What the Original Data Measures

[Touché 2020](https://doi.org/10.1007/978-3-030-58219-7_26) evaluated argument
retrieval for controversial questions. Relevance depends on both topic match
and argumentative content: a useful result should contain a reasoned argument
that supports, opposes, or otherwise addresses the issue. BEIR includes Touché
2020 as an argument retrieval task, and this Japanese NanoBEIR version preserves
that structure after translation. Queries are short controversial questions;
documents are much longer debate-style arguments.

### Observed Data Profile

The task has 49 queries and 5,745 documents. It contains 932 positive qrels,
with positives per query ranging from 6 to 32 and a median of 19.00. Every
query is multi-positive. Queries average 21.73 characters, while documents
average 928.55 characters. The examples ask about homework, prescription drug
advertising, mandatory vaccination, abortion legality, and standardized tests.
The many-positive structure makes hit@10 high for most systems, while nDCG@10
and Recall@100 are more informative about ranking quality and coverage.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.5361, hit@10 = 0.9592, and
Recall@100 = 0.7661. BM25 is strong because controversial questions and
argument documents share topic words such as homework, drugs, vaccines,
abortion, and tests. With many positives per query, lexical matching usually
finds at least one relevant argument. Its strength is early topic anchoring,
but it can still rank long documents that merely mention the issue above
better arguments.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.4354, hit@10 =
0.9592, and Recall@100 = 0.7350. Dense retrieval ties BM25 on hit@10 but is
weaker on nDCG@10 and Recall@100. This suggests that broad embedding similarity
can find documents about the same controversy, but it is less effective at
ordering the most relevant arguments near the top. In argument retrieval, the
difference between "related opinion text" and "argument that answers the
question" matters.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 candidates per query and reaches
nDCG@10 = 0.5296, hit@10 = 1.0000, and Recall@100 = 0.7790, with no rank-101
safeguard rows. Hybrid retrieval has the best hit@10 and Recall@100, while BM25
is slightly higher on nDCG@10. This means that combining lexical and dense
signals improves coverage and ensures at least one relevant argument in the top
10 for every query, but BM25's pure lexical ordering remains marginally stronger
for the very top ranks.

### Metric Interpretation for Model Researchers

This task is a case where BM25 is difficult to beat at early ranking because
topic terms and many positives make lexical retrieval powerful. Dense retrieval
does not dominate; it broadens semantic matching but can over-rank general
topical text. Hybrid retrieval is the best candidate source because it achieves
perfect hit@10 and the highest Recall@100. Researchers should evaluate whether
a model retrieves substantive arguments, covers both sides of a debate, and
avoids long topical passages that do not directly answer the query.

### Query and Relevance Type Tendencies

Queries are short controversial questions. Relevant documents are long
argumentative passages, often including claims, evidence, examples, and
rhetorical framing. A relevant document may argue for or against the issue, so
stance alone is not the relevance criterion. The model must match the issue and
recognize argumentative content.

### Representative Failure Modes

BM25 can over-rank documents that repeat query terms but contain weak or
off-target argumentation. Dense retrieval can retrieve broad opinion passages
that discuss the same controversy without directly addressing the question.
Hybrid retrieval improves coverage but can still mix strong arguments with
topic-only distractors. Long documents also introduce partial-match errors when
only one section is relevant to the query.

### Training Data That May Help

Useful training data includes non-overlapping Touché argument retrieval, debate
portal argument collections, pro/con retrieval pairs, and Japanese or
multilingual argument quality data. Hard negatives should share the same
controversial topic but lack a direct argument for the query. Training should
exclude Touché 2020, BEIR, NanoBEIR, and overlapping translated argument
documents from this benchmark.

### Model Improvement Notes

Strong systems should combine topic matching with argument-quality and
argument-specificity signals. Candidate generation should retrieve many
relevant pro and con arguments, while reranking should prefer documents that
directly answer the controversial question with explicit reasons. Because all
queries are multi-positive, result diversity and broad relevant coverage are
important.

## Example Data

| Query | Positive document |
| --- | --- |
| 宿題は有益ですか？ | まず、宿題が優れており、現代の学校で継続されるべきであるという主張には三つの理由がある。 |
| 処方薬は消費者に直接広告されるべきでしょうか？ | 多くの広告は、薬がどれほど効果的かについて十分な情報を提供していません。 |
| 子供にワクチン接種は義務付けるべきでしょうか？ | 政府は、親が子供のために下す健康上の決定に介入する権利を持ってはいない、という主張が述べられている。 |
| 中絶は合法であるべきですか？ | 中絶は合法であるべきである。人格は受精時ではなく、胎児が生存可能になるか、あるいは出生後に始まる。 |
| 標準化されたテストは教育を改善するのか？ | SAT、ACT、その他の標準化試験は、高校生が大学教育に備えているかどうかについてより深い洞察を提供する、という議論である。 |

### Public Sources

- [Overview of Touché 2020: Argument Retrieval](https://doi.org/10.1007/978-3-030-58219-7_26).
- [Touche20-Argument-Retrieval-for-Controversial-Questions](https://doi.org/10.5281/zenodo.6862281).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of Touché 2020: Argument Retrieval | 2020 | benchmark paper | https://doi.org/10.1007/978-3-030-58219-7_26 |
| Touche20-Argument-Retrieval-for-Controversial-Questions | 2022 | dataset page | https://doi.org/10.5281/zenodo.6862281 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
