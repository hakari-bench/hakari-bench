# NanoR2MED / NanoR2MEDMedicalSciences

## Overview

`NanoR2MEDMedicalSciences` is an English Q&A reference retrieval task from R2MED. Queries are Medical Sciences StackExchange posts about health, physiology, nutrition, symptoms, and medical practice. Documents are external webpages or medical-reference passages that support accepted answers. The task tests whether a retriever can map consumer-facing or practitioner-facing questions to the specific evidence needed for an answer. Dense retrieval is clearly strongest, BM25 is weaker but not negligible, and the hybrid pool gives broad coverage but lower top-rank quality than dense.

## Details

### What the Original Data Measures

R2MED positions its Q&A reference retrieval tasks as reasoning-driven retrieval: the relevant document supports the answer to a forum question, even when it does not directly paraphrase the query. Medical Sciences uses StackExchange posts with accepted or highly upvoted answers and external links.

The benchmark pipeline expands candidate positives from query, answer, and reasoning-path retrieval views, then filters them through relevance assessment and expert review. The answer acts as an implicit bridge between the user question and supporting evidence.

### Observed Data Profile

The Nano split contains 88 queries, 10,000 documents, and 244 positive qrel rows. Queries average 477.62 characters, and documents average 678.60 characters. Questions often include user context, misconceptions, or forum boilerplate.

Each query has 2.77 positives on average, with a median of 2 and a maximum of 8. Multi-positive queries account for 58 of 88 queries, or 65.91%. Examples ask whether microwave cooking is less healthy, whether acne can increase during weight loss, why pills are harder to swallow than food, how often to drink water, and whether protein supplements provide usable nutrients.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.2140, hit@10 of 0.4091, and recall@100 of 0.6598. BM25 is useful when a question contains distinctive terms such as microwave, acne, swallowing, water intake, or amino acids.

Its limitations come from everyday phrasing and broad health vocabulary. A query may use common words while the positive passage discusses a mechanism, physiological process, or nutrition concept. BM25 can find the topic but miss the evidence that actually supports the answer.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.3567, hit@10 of 0.7045, and recall@100 of 0.8197. Dense retrieval improves substantially over BM25 on all reported metrics.

This indicates that embedding similarity is better at linking informal medical questions to explanatory passages. Dense retrieval can connect a question about microwave health to nutrient loss, or a pill-swallowing question to bolus mechanics, even when surface overlap is limited.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with three rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.3320, hit@10 of 0.6136, and recall@100 of 0.7910. Hybrid retrieval is better than BM25 but below dense retrieval for top-rank quality and coverage.

The result suggests that sparse evidence adds some useful anchors but also introduces candidates that are topically similar without being answer-supporting. Dense retrieval is the stronger standalone first-stage method for this split.

### Metric Interpretation for Model Researchers

This split is multi-positive. nDCG@10 measures how well several supporting passages are ranked early, hit@10 measures whether at least one useful source is retrieved near the top, and recall@100 measures evidence coverage for reranking.

For Medical Sciences, dense retrieval is the primary baseline to beat. Hybrid retrieval remains useful as a coverage-oriented comparison, but a good reranker must prioritize answer-supporting mechanisms over broad health-topic overlap.

### Query and Relevance Type Tendencies

Queries are natural-language health questions, often written by non-specialists. Relevant passages can be medical encyclopedia sections, physiology explanations, nutrition references, or evidence summaries. The relevant document usually supports the accepted answer rather than directly mirroring the question.

Relevance depends on the specific mechanism, population, or recommendation. A passage about the same symptom or food category is not sufficient if it does not answer the user's question.

### Representative Failure Modes

Common failures include retrieving broad pages about COVID, allergies, computers, food, or nutrition when the answer requires a specific mechanism; matching forum boilerplate instead of the medical intent; and selecting passages with the same everyday word but a different recommendation. BM25 is vulnerable to broad health terms; dense retrieval can still overgeneralize among adjacent mechanisms.

### Training Data That May Help

Useful training data includes non-overlapping Medical Sciences StackExchange answer-link retrieval, consumer health QA with cited evidence, medical encyclopedia and physiology section retrieval, and hard negatives from adjacent health topics. Evaluation queries, qrels, and positive passages should be excluded.

### Model Improvement Notes

Models should learn to map lay medical questions to evidence passages that support the actual answer. Multi-positive objectives are useful because several sources can support one response. Hard negatives should share common health vocabulary while differing in mechanism, population, or recommendation.

## Example Data

### Public Sources

- [R2MED: A Benchmark for Reasoning-Driven Medical Retrieval](https://arxiv.org/abs/2505.14558), benchmark paper.
- [R2MED project page](https://r2med.github.io/).
- [R2MED GitHub repository](https://github.com/R2MED/R2MED).
- [R2MED/Medical-Sciences dataset card](https://huggingface.co/datasets/R2MED/Medical-Sciences).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| R2MED: A Benchmark for Reasoning-Driven Medical Retrieval | 2025 | arXiv paper | https://arxiv.org/abs/2505.14558 |
| R2MED project page | 2025 | project page | https://r2med.github.io/ |
| R2MED GitHub repository | 2025 | source repository | https://github.com/R2MED/R2MED |
| R2MED/Medical-Sciences | 2025 | dataset card | https://huggingface.co/datasets/R2MED/Medical-Sciences |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Is food prepared in a microwave oven less healthy? | A passage explains how water-soluble vitamins can leach into cooking water and why low-water cooking methods may preserve nutrients. |
| Is an increase in acne during weight loss normal? | A passage explains blocked pores, oil production, bacteria, white blood cells, and inflammation in pimple formation. |
| Why is swallowing pills harder than swallowing food? | A passage explains bolus position and tongue-palate action during the oral preparatory stage of swallowing. |
| How often should a person drink water, not just how much? | A passage summarizes water as the largest single constituent of the body and includes drinking water, beverages, and food water in total intake. |
| Do protein bars or shakes provide nutrients the body can use? | A passage explains amino acids as molecules that combine to form proteins and are produced when proteins are digested. |
