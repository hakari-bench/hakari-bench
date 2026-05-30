# NanoBIRCO / NanoBIRCOArguAna

## Overview

NanoBIRCOArguAna is a compact Nano task derived from the BIRCO benchmark's ArguAna-style counterargument retrieval setting. Each query is a paragraph-length debate argument, and the relevant document is a counterargument passage that directly challenges it. The retrieval goal is not topical similarity, but finding the opposing argumentative move. This makes the task useful for evaluating complex-objective retrieval, stance-aware ranking, long argument matching, and counterargument selection.

## Details

### What the Original Data Measures

BIRCO was introduced to evaluate information retrieval tasks with complex objectives, where relevance requires more than semantic similarity. In its ArguAna-style task, both queries and documents are debate passages, and the positive document should counter the query's stance or reasoning. A semantically similar same-side passage can therefore be a bad result.

This task is stricter than ordinary argument-topic retrieval. A model must identify the query's claim, evidence, causal assumptions, value judgment, and policy conclusion, then retrieve a passage that challenges that reasoning. The decisive relevance condition is discourse function: the candidate should rebut, oppose, or undermine the query argument.

### Observed Data Profile

The task contains 98 queries, 3,081 documents, and 98 relevance judgments. Each query has exactly one positive passage, so the positives-per-query average is 1.0, with minimum 1, median 1.0, maximum 1, and no multi-positive queries.

Queries and documents are both long. Queries average 1,123.99 characters, and documents average 1,140.11 characters. Many examples are structured debate passages about policy, education, health, gender, human rights, international relations, or social issues. The long text makes it easy for a retriever to match topic words while missing the actual counterargument relation.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4293, hit@10 of 0.7755, and recall@100 of 0.9796 using the top-500 BM25 candidate subset. Lexical matching is useful because query and counterargument often share debate motion vocabulary, policy names, institutions, or domain labels.

The top-rank score remains modest because the correct counterargument competes with many same-topic passages. BM25 can identify the debate area, but it cannot reliably determine whether a candidate supports the same side, attacks the premise, or addresses a different aspect of the issue.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.5062, hit@10 of 0.8776, and recall@100 of 0.9796. Dense retrieval is the strongest direct top-rank profile. It improves both nDCG@10 and hit@10 over BM25 while preserving the same recall@100.

This suggests that embedding similarity helps capture argumentative relatedness beyond exact wording. Dense retrieval is better at finding counterarguments that engage the same reasoning target, even when the surface terms differ. However, the recall value also shows that dense alone does not exceed BM25 in candidate completeness.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.4932, hit@10 of 0.8673, and recall@100 of 1.0000. It uses exactly 100 candidates per query, with no safeguard rows. The hybrid profile has complete recall@100, while dense retrieval has the best nDCG@10 and hit@10.

This makes reranking_hybrid the most reliable candidate pool for a downstream stance-aware reranker. BM25 contributes topic and phrase coverage, while dense retrieval contributes semantic counterargument matching. The combined pool ensures the positive is available for every query within the top 100.

### Metric Interpretation for Model Researchers

Because every query has one positive, hit@10 directly measures whether the counterargument is visible, and nDCG@10 measures how early it appears. recall@100 is a reranking-readiness metric. The best use of this task is to test whether models retrieve opposition, not merely same-topic passages.

The comparison shows that BM25 is a strong but incomplete topic matcher, dense retrieval is the best direct ranker, and reranking_hybrid is the best candidate source for complete coverage. This task is a compact diagnostic for complex objective retrieval.

### Query and Relevance Type Tendencies

Queries include arguments about sports shooting and firearms, feminisation of labor, education campaigns, migration restrictions, and HIV workplace disclosure. Positive documents usually address the same motion but challenge the query's stance or reasoning.

The task rewards identifying the rebuttal target. A passage can share many words with the query but still be wrong if it supports the same side or discusses a different premise. Long argument structure matters more than raw topical similarity.

### Representative Failure Modes

Likely failures include retrieving same-side arguments, matching debate labels without stance awareness, missing a counterargument that targets a specific premise, and over-weighting frequent topic terms in long passages. BM25 may be too lexical, while dense retrieval may still conflate support and opposition unless trained on counterargument labels.

### Training Data That May Help

Useful training data includes BIRCO or ArguAna training and development pairs that do not overlap the benchmark split, stance-labeled argument-counterargument datasets, claim-rebuttal corpora, debate passage retrieval pairs, and hard negatives from same-topic same-side arguments. Generic semantic similarity data is not sufficient and can be harmful if it rewards supportive paraphrases.

### Model Improvement Notes

A model targeting this task should represent stance direction and rebuttal relation over long passages. Sparse systems need topic coverage but cannot stop there. Dense systems should train on counterargument positives and same-topic support negatives. Hybrid systems are valuable for reranking because the observed profile reaches complete recall@100.

## Example Data

### Public Sources

The original task is based on BIRCO's complex-objective retrieval benchmark, with NanoBIRCO providing the compact dataset packaging.

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original benchmark paper | [BIRCO](https://arxiv.org/abs/2402.14151) |
| Project repository | [BIRCO GitHub repository](https://github.com/BIRCO-benchmark/BIRCO) |
| NanoBIRCO dataset | [hakari-bench/NanoBIRCO](https://huggingface.co/datasets/hakari-bench/NanoBIRCO) |

Representative query and positive counterargument snippets:

| Query | Positive document snippet |
| --- | --- |
| Sports shooting desensitizes people to the lethal nature of firearms. | Shooting is a major sport enjoyed by many law-abiding people who have the right to take part. |
| Where are the men in the feminisation of labour? | Gender and development work has recognized the importance of bringing men into the picture. |
| Run education campaigns instead. | Educational campaigns can work, but they can only do so much in making genuine progress. |
| Restrictions on migration would benefit people in cities economically and socially. | People who move to cities have chosen to move because they want a new and better life. |
| The risks of ignorance and prejudice are too high for HIV-positive workers. | Employers can be trusted to use sensitive information responsibly. |
