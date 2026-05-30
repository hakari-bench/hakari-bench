# NanoBEIR-en / NanoArguAna

## Overview

NanoArguAna is the compact English NanoBEIR version of ArguAna, an argument retrieval task where each query is a long debate argument and the relevant document is its best counterargument. The retrieval target is not a duplicate, summary, or supporting passage. It is an opposing argument that addresses the same topic and aspects while challenging the query's claim, premise, consequence, or policy framing. This makes the task useful for evaluating stance-aware retrieval, long argumentative text matching, and counterargument selection.

## Details

### What the Original Data Measures

ArguAna was introduced for retrieving the best counterargument without prior topic knowledge. The original formulation assumes that a good counterargument should be related to the same debate issue but should oppose the query argument's stance or reasoning. This makes the task different from ordinary semantic similarity, because a passage that is too similar in stance may be a bad result.

The BEIR version frames ArguAna as argument retrieval, and the NanoBEIR version keeps the long-form debate structure in a compact sample. A model must read enough of each passage to identify the claim, premises, examples, and argumentative target. Simple topical matching is often necessary but not sufficient.

### Observed Data Profile

The task contains 50 queries, 3,635 documents, and 50 relevance judgments. Each query has exactly one positive counterargument, so the positives-per-query average is 1.0, with minimum 1, median 1.0, maximum 1, and no multi-positive queries.

The text is much longer than most NanoBEIR tasks. Queries average 1,201.78 characters, and documents average 1,011.79 characters. Both sides often contain titles, claims, evidence, examples, citations, and policy implications. The retrieval problem is therefore long-passage argument matching rather than short query search.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4650, hit@10 of 0.7600, and recall@100 of 1.0000 using the top-500 BM25 candidate subset. The perfect recall@100 shows that lexical matching is very effective at candidate generation. Debate pairs usually share topic vocabulary, named entities, policy terms, and issue-specific phrases.

The weaker nDCG@10 shows the core difficulty. BM25 can find the right topic but may rank same-side arguments, broad topical discussions, or near-duplicates above the actual counterargument. The task requires recognizing an opposing move, not merely repeated words.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.5787, hit@10 of 0.9200, and recall@100 of 0.9400. Dense retrieval is the strongest direct top-rank profile. It substantially improves hit@10 and nDCG@10 over BM25, which suggests that embedding similarity helps capture argumentative relatedness beyond exact term overlap.

The recall@100 drop relative to BM25 is still important. Dense retrieval is better at placing good counterarguments near the top when it finds them, but it misses some positives from the top-100 candidate window. This is a typical tradeoff for long argumentative text: semantic matching improves ordering, while sparse matching preserves exact topical coverage.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.5422, hit@10 of 0.8800, and recall@100 of 1.0000. It uses exactly 100 candidates per query, with no safeguard rows. The hybrid profile restores BM25's complete recall@100 while retaining much of the dense top-10 improvement.

This makes reranking_hybrid the most attractive candidate pool for downstream counterargument reranking. BM25 contributes reliable topic and phrase coverage, while dense retrieval contributes broader argument similarity. A second-stage model trained for stance and attack relations should benefit from the complete candidate coverage.

### Metric Interpretation for Model Researchers

Because each query has one positive, hit@10 is easy to interpret: the intended counterargument is either visible or not. nDCG@10 captures how early it appears, which matters for practical argument search. recall@100 indicates whether a reranker has access to the positive.

The comparison shows that BM25 is best for candidate completeness, dense retrieval is best for direct top-rank ordering, and reranking_hybrid combines complete recall with stronger top-rank behavior than BM25. This task is useful for testing whether a model can retrieve opposition, not just semantic similarity.

### Query and Relevance Type Tendencies

Queries cover debates about constitutional reform, airport expansion, consumer choice, cyber attacks, religious speech, health policy, education, and international affairs. The positive document usually addresses the same debate issue while challenging a premise, feasibility claim, value judgment, or predicted consequence.

The task rewards recognizing argumentative structure. A relevant passage may repeat many query terms, but it must function as a counterargument. Same-topic same-stance passages are especially dangerous negatives.

### Representative Failure Modes

Likely failures include retrieving support arguments instead of counterarguments, over-ranking the query-side position, matching on topic vocabulary while missing stance, and failing to process long passages where the decisive counterpoint appears late. BM25 may be too lexical, while dense retrieval may treat related support and opposition as similarly relevant.

### Training Data That May Help

Useful training data includes non-overlapping argument-counterargument pairs, debate portal pro/con responses, argument attack and support relation datasets, stance-classified arguments, and hard negatives from same-topic same-stance passages. Training data should avoid upstream ArguAna or idebate pairs that overlap the evaluation material.

### Model Improvement Notes

A model targeting this task should combine long-document topical recall with explicit stance and attack-relation awareness. Sparse systems need robust long-passage term handling. Dense systems need counterargument-specific positives and same-topic support negatives. Hybrid systems are promising because the observed candidate pool keeps full recall while improving over pure lexical ranking.

## Example Data

### Public Sources

The original task is based on ArguAna, with BEIR providing the retrieval benchmark framing and NanoBEIR providing the compact English dataset packaging.

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset paper | [Retrieval of the Best Counterargument without Prior Topic Knowledge](https://aclanthology.org/P18-1023/) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Source dataset card | [mteb/arguana](https://huggingface.co/datasets/mteb/arguana) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-en dataset | [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en) |

Representative query and counterargument snippets:

| Query | Positive document snippet |
| --- | --- |
| The public is apathetic to reform of the House of Lords. | The AV campaign cannot be compared to reform to the House of Lords, and political spin should not be mistaken for apathy. |
| The expansion of Heathrow is vital for the economy. | The business community is far from united in its support of a third runway. |
| People are given too much choice, which makes them less happy. | People are unhappy because they cannot have everything, not because choice itself is stressful. |
| Cyber attacks are often carried out by non-state actors. | In cases involving non-state actors, a state may still retaliate if another state is unwilling or unable to act. |
| Religious certainty can justify hatred, so free speech must come second. | Nobody is forced to commit violence by another person's words, and responsibility remains with the actor. |
