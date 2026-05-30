# NanoLaw / NanoLeCaRDv2

## Overview

`NanoLaw / NanoLeCaRDv2` is a Chinese legal case retrieval task based on
LeCaRDv2. Queries and documents are Chinese criminal case records, and the
retrieval goal is to find legally related cases under a multi-aspect relevance
definition. The Nano split has 159 queries, 3,795 documents, and 3,896 positive
qrel rows. Every query has multiple positives, with more than 24 positives per
query on average. Current diagnostics show that `reranking_hybrid` is the
strongest observed profile across nDCG@10, hit@10, and recall@100. Dense
retrieval is also stronger than BM25, while BM25 remains a high-performing
lexical baseline because Chinese criminal judgments share charge names and
formulaic court language.

## Details

### What the Original Data Measures

LeCaRDv2 is introduced as a large-scale Chinese legal case retrieval dataset
created from millions of Chinese criminal case documents. The paper argues that
earlier Chinese legal retrieval datasets were limited by scale, candidate
pooling, and narrow relevance definitions. LeCaRDv2 broadens relevance to
include characterization, penalty, and procedure, and uses legal expert
annotation over candidate pools.

The MTEB task frames LeCaRDv2 as retrieving case documents most relevant to a
query scenario. In this Nano split, the query itself is a long criminal case
document or fact section, and relevant documents are related criminal cases.
The task is therefore a legal case similarity benchmark, not just a charge-name
lookup task.

### Observed Data Profile

The Nano split contains 159 queries, 3,795 documents, and 3,896 positive qrel
rows. Every query is multi-positive. Positives per query average 24.50, with a
minimum of 4, a median of 28, and a maximum of 30. Queries average 4,259.44
characters, while documents average 7,231.82 characters.

Representative cases involve theft, fraud, illegal absorption of public
deposits, picking quarrels and provoking trouble, robbery, production or sale
of counterfeit medicine, illegal fishing, gambling, and organized criminal
activity. Texts include court names, docket numbers, prosecution statements,
trial procedure, facts, reasoning, charges, and sentencing details. This makes
the benchmark a long-form legal similarity task with many relevant cases per
query.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.6528, hit@10 = 0.9497, and recall@100 = 0.7523. BM25 is
strong because criminal case documents repeat charge names, court formulas,
procedural language, and statutory vocabulary. If two cases involve the same
offence or similar court-language patterns, sparse retrieval can surface many
relevant candidates.

BM25 is nevertheless below dense retrieval and hybrid retrieval. The reason is
the relevance definition: relatedness is not only shared charge text. Cases may
be relevant because they align on characterization, penalty, procedure, or
material facts. A sparse model can over-rank cases that repeat the same offence
label while missing cases that are legally similar in sentencing pattern or
procedural posture.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.6940, hit@10 = 0.9560, and recall@100 = 0.8611.
Dense retrieval improves over BM25 across the main reported metrics. This
suggests that semantic case similarity and legal-fact representation are
important in LeCaRDv2, especially where relevant cases share factual patterns
or penalty considerations beyond exact charge names.

The dense gains are especially meaningful because documents are long and
multi-positive. A dense model can group cases by overall criminal conduct,
procedure, and sentencing context, not just by repeated words. Still, dense
retrieval must preserve exact legal labels and factual details; otherwise it
may retrieve broadly similar but legally mismatched cases.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 or 101 candidates per
query, with 1 safeguard positive row and a mean of 100.006289 candidates. It
achieves nDCG@10 = 0.7225, hit@10 = 0.9686, and recall@100 = 0.8619, making it
the strongest observed profile. The improvement over dense is moderate but
consistent, and the improvement over BM25 is clear.

This is a strong example of hybrid search matching the structure of a legal
retrieval task. BM25 contributes charge labels, statutory terms, court formulas,
and named procedural phrases. Dense retrieval contributes fact-pattern and
legal-similarity matching. The hybrid set combines these signals and provides
the best early ranking and candidate coverage among the three profiles.

### Metric Interpretation for Model Researchers

This task is heavily multi-positive. Hit@10 is high for all methods because
many queries have large relevant sets, so at least one relevant case is often
retrieved. nDCG@10 is more informative because it rewards ranking multiple
relevant cases high. Recall@100 measures how much of the large positive set is
available for later reranking.

The metric pattern indicates that `NanoLeCaRDv2` is not solved by sparse
charge matching alone. BM25 is strong, dense retrieval is stronger, and hybrid
retrieval is strongest. This makes the task useful for evaluating whether legal
retrieval systems combine exact offence vocabulary with semantic legal
similarity.

### Query and Relevance Type Tendencies

Queries are long Chinese criminal case records or fact sections. Relevant
documents are other criminal cases related by legal characterization, penalty,
procedure, or material facts. Relevance is therefore set-based and graded by
legal relatedness, not a single exact answer.

The task rewards models that can identify charge-level similarity, sentencing
patterns, procedural posture, defendant conduct, and legally material facts.
Because every query has many positives, a model should retrieve a diverse set
of related cases rather than only the closest lexical duplicate.

### Representative Failure Modes

BM25 can fail by overmatching charge names while ignoring differences in facts,
penalty, or procedure. Dense retrieval can fail by retrieving cases that are
generally similar but miss exact offence elements or procedural conditions.
Hybrid retrieval reduces both risks but can still rank highly formulaic court
documents above more legally relevant cases.

Long-document representation is another challenge. Court records contain
procedural headers, party information, facts, reasoning, and sentencing. A model
that overweights boilerplate may miss the factual or legal section that drives
relevance.

### Training Data That May Help

Useful training data includes Chinese legal case retrieval, criminal charge and
fact-section retrieval pairs, court-document similarity data, sentencing
similarity supervision, and same-charge hard negatives. Training should preserve
large positive sets per query because LeCaRDv2 relevance is multi-positive and
multi-aspect.

For comparable evaluation, training should exclude NanoLeCaRDv2 queries, qrels,
and relevant criminal case documents. Synthetic data can help when it generates
Chinese criminal judgments with facts, reasoning, and sentencing, and pairs
them with positives aligned on characterization, penalty, or procedure.

### Model Improvement Notes

Dense retrievers should learn legal-fact similarity and sentencing/procedure
alignment while preserving exact Chinese charge terms. Sparse systems benefit
from Chinese legal tokenization, charge phrase handling, and weighting of court
formulae versus material facts. Rerankers should compare the sections that
matter legally: alleged conduct, court findings, charge characterization,
penalty reasoning, and procedure.

For hybrid systems, `NanoLeCaRDv2` is a strong fit. Exact terms and semantic
legal similarity both matter, and the observed `reranking_hybrid` profile is
the best of the three candidate sets.

## Example Data

Representative queries include Chinese criminal judgments about theft, fraud,
illegal absorption of public deposits, picking quarrels and provoking trouble,
and robbery or related offences. Positive documents are other criminal case
judgments with related charges, factual patterns, procedure, or sentencing
reasoning.

### Public Sources

- [LeCaRDv2: A Large-Scale Chinese Legal Case Retrieval Dataset](https://arxiv.org/abs/2310.17609),
  2023.
- [THUIR LeCaRDv2 repository](https://github.com/THUIR/LeCaRDv2), source
  repository.
- [mteb/LeCaRDv2](https://huggingface.co/datasets/mteb/LeCaRDv2), MTEB source
  dataset.
- [hakari-bench/NanoLaw](https://huggingface.co/datasets/hakari-bench/NanoLaw),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| LeCaRDv2: A Large-Scale Chinese Legal Case Retrieval Dataset | 2023 | arXiv paper | https://arxiv.org/abs/2310.17609 |
| THUIR LeCaRDv2 | 2023 | GitHub repository | https://github.com/THUIR/LeCaRDv2 |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A Chinese theft judgment with court, indictment, trial, facts, and sentencing details. | Another theft judgment with related criminal history, facts, or penalty reasoning. |
| A judgment involving fraud and forged official documents or seals. | A fraud judgment with related conduct and trial findings. |
| A long illegal-absorption-of-public-deposits case. | Another financial-crime judgment involving related public-deposit conduct and defendants. |
| A case about picking quarrels and provoking trouble. | A judgment involving similar public-order conduct and sentencing context. |
| A robbery or robbery-snatching appeal judgment. | A related criminal judgment involving robbery, snatching, or associated offence patterns. |
