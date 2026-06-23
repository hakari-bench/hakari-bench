# NanoMTEB-v2 / touche2020_v3

## Overview

`NanoMTEB-v2 / touche2020_v3` is an English argument retrieval task from Touché 2020. Queries are short controversial questions, and relevant documents are argumentative passages or debate-style texts that address those questions. Touché 2020 Task 1 focused on argument retrieval: systems should retrieve passages containing relevant arguments, often with pro or con positions. This Nano split is small in query count but dense in relevance judgments, with 49 questions and 1,704 positive qrels. It is useful for studying retrieval when each information need has many relevant passages and where ranking quality depends on argument usefulness, not just topical match.

## Details

### What the Original Data Measures

Touché 2020 measures argument retrieval for controversial questions. A relevant document should contain an argument that helps address the question, whether it supports, opposes, or otherwise contributes to the debate. This differs from fact retrieval because relevance can include multiple positions and many acceptable passages.

The MTEB version exposes the task as English retrieval over a web/debate-style document collection. Documents are often longer than ordinary passage datasets and may contain lists of points, claims, examples, and argumentative framing.

### Observed Data Profile

The Nano split contains 49 queries, 10,000 documents, and 1,704 positive qrel rows. Queries have 34.77551 positives on average, with a median of 33 and a maximum of 65. Every query is multi-positive. Queries average 43.43 characters, while documents average 2,386.21 characters.

The examples include homework, direct-to-consumer prescription drug advertising, child vaccination requirements, abortion legality, and standardized testing. Relevant documents may present pro arguments, con arguments, or structured debate material.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.8424, hit@10 of 1.0000, and recall@100 of 0.9243. BM25 is very strong because controversial questions contain topic terms that repeat throughout relevant debate passages.

However, the high score should not be read as solving argument quality. BM25 can find the controversy topic, but it may not rank the most useful, well-supported, or directly responsive arguments first. The task's many positives make hit@10 easy; fine ranking among relevant and partially relevant passages is the harder issue.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.8810, hit@10 of 1.0000, and recall@100 of 0.9343. Dense retrieval improves over BM25 in both nDCG@10 and recall@100. This suggests that semantic matching helps identify argumentative relevance beyond repeated topic words.

Dense retrieval is useful when a passage answers the controversy through paraphrase, policy framing, ethical reasoning, or examples that do not repeat the query exactly. It still needs to distinguish usable arguments from broad commentary.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates with no safeguard positives. It reaches nDCG@10 of 0.8835, hit@10 of 1.0000, and recall@100 of 0.9495. This is the strongest profile overall, though the margin over dense retrieval is small.

The hybrid result shows that sparse topic matching and dense argument-intent matching are complementary. Because every query has many positives, a hybrid pool can expose more diverse arguments to a reranker, including both exact-topic passages and semantically responsive passages.

### Metric Interpretation for Model Researchers

Hit@10 is saturated and therefore not very informative. nDCG@10 and recall@100 are more useful. nDCG@10 captures whether high-quality relevant arguments appear early; recall@100 shows whether the candidate pool covers enough of the many relevant passages for downstream reranking or diversification.

This task should be analyzed as many-positive argument retrieval rather than single-answer search. A model can look strong on hit rate while still failing to rank the best arguments.

### Query and Relevance Type Tendencies

Queries are short controversial questions, usually phrased as "Should..." or "Is..." questions. Relevant documents are longer argumentative passages, debate posts, or structured lists of points. They may support either side of the controversy.

The relevance relation is argumentative usefulness for the question. A passage must address the issue with a usable argument, not just mention the topic.

### Representative Failure Modes

Common failures include retrieving generic commentary instead of an argument, ranking off-aspect passages that discuss the same controversy, failing to distinguish pro and con argumentative roles, and over-ranking long documents with many repeated topic terms. Dense systems may retrieve semantically broad passages; sparse systems may retrieve keyword-heavy but weak arguments.

### Training Data That May Help

Useful training data includes argument retrieval collections, debate passages aligned to controversial questions, stance corpora, claim-evidence corpora, and hard negatives from the same topic with weak or off-target argumentation. Multi-positive training is required because each query has many relevant arguments.

### Model Improvement Notes

Models should learn argument responsiveness and not only topicality. Rerankers should be trained to identify whether a passage gives a clear reason, evidence, or counterpoint for the question. Diversification may also matter because the relevant set often spans multiple argumentative stances and aspects.

## Example Data

| Query | Positive document |
| --- | --- |
| Is homework beneficial? [23 chars] | First, there are three arguments for why homework is excellent and ought to continue in modern schools. 1. Homework aids doer-learners. It is generally accepted that there are three types of learners:... [200 / 3,553 chars] |
| Should prescription drugs be advertised directly to consumers? [62 chars] | Many ads don't include enough information on how well drugs work. For example, Lunesta is advertised by a moth floating through a bedroom window, above a peacefully sleeping person. Actually, Lunesta... [200 / 1,682 chars] |
| Should any vaccines be required for children? [45 chars] | Not a full case yet.. Just some little points I put together... Governments should not have the right to intervene in the health decisions parents make for their children. 31% of parents believe they... [200 / 4,497 chars] |
| Should abortion be legal? [25 chars] | Abortions should be legal as Personhood begins after a fetus becomes viable or after birth, not at conception. According to the U.S. Supreme Court a person is to get their age when they are out of the... [200 / 309 chars] |
| Do standardized tests improve education? [40 chars] | Resolved: The SAT, ACT, and other standardized tests provided more insight into a high school student's preparedness for education at elite colleges and universities than high school GPA and therefore... [200 / 4,159 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of Touché 2020: Argument Retrieval | 2020 | source task paper | [https://downloads.webis.de/touche/publications/papers/bondarenko_2020d.pdf](https://downloads.webis.de/touche/publications/papers/bondarenko_2020d.pdf) |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |
| mteb/webis-touche2020-v3 |  | dataset card | [https://huggingface.co/datasets/mteb/webis-touche2020-v3](https://huggingface.co/datasets/mteb/webis-touche2020-v3) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Is homework beneficial? | A debate-style passage giving several arguments for why homework should continue in modern schools. |
| Should prescription drugs be advertised directly to consumers? | A passage arguing that many drug advertisements do not include enough information about effectiveness. |
| Should any vaccines be required for children? | A passage presenting points against government intervention in parents' health decisions for children. |
| Should abortion be legal? | A passage arguing about personhood, fetal viability, and legal status. |
| Do standardized tests improve education? | A passage discussing whether standardized tests provide useful insight into college preparedness. |
