# NanoRARb / NanoTempReasonL2Pure

## Overview

`NanoTempReasonL2Pure` is an English temporal reasoning retrieval task from NanoRARb. The query is a temporal question without supporting facts, and the relevant document is the correct short answer string. Each query has one positive answer. This is the hardest L2 formulation because retrieval must rely on temporal knowledge encoded in the model rather than on facts included in the query. BM25 is effectively unable to solve the top ranks, dense retrieval is the strongest profile, and `reranking_hybrid` improves candidate availability over BM25 but remains weaker than dense retrieval.

## Details

### What the Original Data Measures

RAR-b converts TempReason tasks into retrieval tasks where the target output is an answer document. TempReason is designed to test temporal reasoning over facts such as offices, heads of government, team membership, and dated roles.

The pure variant removes the supporting fact list from the query. The retriever sees only the question and date, so success depends on whether the representation can associate the question with the correct temporal answer without explicit evidence in the query text.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Every query has exactly one positive. Queries average 52.96 characters, while answer documents average 19.91 characters.

Examples ask which office Patricia de Lille held in September 2015, which parliamentary position Lord Douglas Gordon-Hallyburton held in October 1833, who led Russia in July 1999, which team Glynn Snodin played for in January 1992, and who led Romania in May 1935.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.0000, hit@10 of 0.0000, and recall@100 of 0.0050. This is a near-complete failure mode for lexical retrieval.

The reason is structural. The query usually contains an entity, relation, and date, while the relevant document is only the answer string. Unless the answer words overlap with the query by accident, BM25 has little evidence to rank the correct document. Term frequency cannot supply missing temporal knowledge.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.0483, hit@10 of 0.1050, and recall@100 of 0.4850. Dense retrieval is clearly stronger than BM25, but the absolute score is still low.

This profile shows that embedding similarity can recover some associations between question wording, entities, relations, dates, and plausible answer strings. However, the model must retrieve a short answer without seeing supporting evidence, so many correct answers are semantically distant from the query surface.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 134 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.0033, hit@10 of 0.0100, and recall@100 of 0.3300. Hybrid retrieval improves substantially over BM25 in recall@100 but is much weaker than dense retrieval at the top ranks.

This indicates that the sparse side contributes little for this pure setting. The hybrid pool can still expose additional candidates for a reranker, but the task mainly rewards dense semantic and memorized temporal associations rather than lexical matching.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 reflects how early the exact answer string is ranked, hit@10 reflects whether it is available in the first ten candidates, and recall@100 reflects whether a second-stage reranker can access it.

For `NanoTempReasonL2Pure`, recall@100 is useful but should not be overread as reasoning success. A candidate can be retrieved from broad association, while a final model still needs to decide whether the answer is temporally valid for the target date.

### Query and Relevance Type Tendencies

Queries are short temporal questions. Relevant documents are short entity, role, team, or office strings. The answer is determined by a temporal fact that is not included in the query.

Relevance is exact answer validity for the specified time. A historically related answer is wrong if it held before or after the target date.

### Representative Failure Modes

Common failures include retrieving a more famous role for the same entity, choosing an adjacent office holder, overvaluing entity popularity, selecting an answer from the wrong time interval, and ranking semantically related but temporally invalid names. BM25 fails because the answer string is usually absent from the query; dense retrieval can still confuse nearby temporal states.

### Training Data That May Help

Useful training data includes temporal QA without explicit facts, entity-time relation triples, historical office-holder timelines, sports roster timelines, and contrastive pairs with nearby dates. Evaluation queries, answers, and qrels should be excluded.

### Model Improvement Notes

Models need stronger temporal knowledge and better date-conditioned retrieval behavior. Hard negatives should share the same entity and relation but differ by interval. This split is useful for identifying whether a retriever has learned temporal associations beyond lexical overlap.

## Example Data

| Query | Positive document |
| --- | --- |
| Which position did Patricia de Lille hold in Sep, 2015? [55 chars] | mayor of Cape Town [18 chars] |
| Which position did Lord Douglas Gordon-Hallyburton hold in Oct, 1833? [69 chars] | Member of the 11th Parliament of the United Kingdom [51 chars] |
| Who was the head of Russia in Jul, 1999? [40 chars] | Sergei Stepashin [16 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | [https://arxiv.org/abs/2404.06347](https://arxiv.org/abs/2404.06347) |
| Towards Benchmarking and Improving the Temporal Reasoning Capability of Large Language Models | 2023 | arXiv paper | [https://arxiv.org/abs/2306.08952](https://arxiv.org/abs/2306.08952) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Which position did Patricia de Lille hold in Sep, 2015? | Mayor of Cape Town. |
| Which position did Lord Douglas Gordon-Hallyburton hold in Oct, 1833? | Member of the 11th Parliament of the United Kingdom. |
| Who was the head of Russia in Jul, 1999? | Sergei Stepashin. |
| Which team did Glynn Snodin play for in Jan, 1992? | Leeds United F.C. |
| Who was the head of Romania in May, 1935? | Gheorghe Tatarescu. |
