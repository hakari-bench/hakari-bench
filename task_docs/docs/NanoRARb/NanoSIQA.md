# NanoRARb / NanoSIQA

## Overview

`NanoSIQA` is an English social commonsense retrieval task from NanoRARb. It recasts SocialIQA as retrieval: the query describes a social situation and asks about a likely intention, reaction, motivation, or next event, while the relevant document is the correct short answer phrase. Each query has one positive answer among 10,000 candidates. This is one of the harder NanoRARb tasks because answers are extremely short and often do not repeat the situation wording. Dense retrieval improves over BM25, but absolute scores remain low.

## Details

### What the Original Data Measures

RAR-b converts SocialIQA into full answer retrieval. The original SocialIQA benchmark targets commonsense reasoning about social interactions, including what a person intended, how someone would feel, what might happen next, or why an action occurred.

In this retrieval version, the model must retrieve the answer phrase itself. The task tests social plausibility and inference over interpersonal context rather than topical document retrieval.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Every query has exactly one positive. Queries average 126.94 characters, while answer documents average only 21.51 characters.

Examples include a student taking parental warnings seriously, a person with many friends, reading a biography of Hillary Clinton, intimacy between two people, and feeling ashamed after stealing from a locker. Positive documents are short phrases such as `study very hard`, `know more about Hillary Clinton`, or `ashamed`.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.0239, hit@10 of 0.0400, and recall@100 of 0.1850. BM25 is extremely weak because the correct answer often contains few or none of the query's distinctive words.

Sparse retrieval may work when an answer repeats a named entity, but most social inferences are expressed as short generic phrases. Term frequency is not enough to infer intent, emotion, or likely consequence.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.0618, hit@10 of 0.1250, and recall@100 of 0.3850. Dense retrieval improves over BM25 across all metrics. It captures some semantic relationship between a situation and a likely answer phrase.

The low absolute score shows that social commonsense answer retrieval remains difficult. Many candidate answers are short and broadly plausible, and embeddings may rank a reasonable but incorrect phrase above the gold answer.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 133 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.0405, hit@10 of 0.0700, and recall@100 of 0.3350. Hybrid retrieval improves over BM25 but trails dense retrieval.

The large safeguard count indicates that many positives sit near the edge of the compact candidate pool. Sparse overlap adds limited value because the answer phrases are too short and generic. Dense retrieval is the stronger first-stage profile.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 reflects the rank of the correct answer phrase, hit@10 measures whether it appears in the first ten candidates, and recall@100 measures candidate availability for reranking.

For SIQA, dense retrieval is the baseline to beat, but better models likely need social reasoning and answer-selection supervision rather than only semantic embeddings.

### Query and Relevance Type Tendencies

Queries describe social contexts and ask why someone acted, how they might feel, or what will happen. Relevant documents are concise answer phrases. The answer may be an emotion, intention, activity, or consequence.

Relevance is social plausibility. A candidate that names the same person or setting is wrong if it implies the wrong intention, reaction, or outcome.

### Representative Failure Modes

Common failures include selecting a generic feeling instead of the specific expected reaction, matching a person or object without the right intent, confusing motivation with consequence, and ranking plausible but non-gold actions. BM25 almost entirely misses implicit answers; dense retrieval can over-rank common social phrases.

### Training Data That May Help

Useful training data includes social commonsense QA, intent and effect prediction, dialogue commonsense, story-based social inference, and retrieval-formatted answer selection. Evaluation examples and answer documents should be excluded.

### Model Improvement Notes

Models should learn situation-to-answer social inference over very short documents. Hard negatives should mention the same person, setting, or social relationship but imply a wrong emotion, intention, or consequence. Cross-encoder reranking may be especially important because short answer phrases lack standalone context.

## Example Data

| Query | Positive document |
| --- | --- |
| Context: Cameron's parents told them to do well at school or they would be grounded. Cameron took th... [100 / 160 chars] | study very hard [15 chars] |
| Context: Riley had a lot of friends. Question: What will happen to Riley? [73 chars] | they will play with Riley [25 chars] |
| Context: Sydney is a fan of Hillary Clinton. One day she found a biography of Hillary Clinton. Sydne... [100 / 154 chars] | know more about Hillary Clinton [31 chars] |
| Context: Austin knew Quinn intimately and they slept together many times. Question: Why did Austin d... [100 / 107 chars] | found QUinn attractive [22 chars] |
| Context: Quinn knew Ash well enough that they broken into and stole a jacket from Ash's locker. Ques... [100 / 138 chars] | ashamed [7 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | [https://arxiv.org/abs/2404.06347](https://arxiv.org/abs/2404.06347) |
| SocialIQA: Commonsense Reasoning about Social Interactions | 2019 | arXiv paper | [https://arxiv.org/abs/1904.09728](https://arxiv.org/abs/1904.09728) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Cameron's parents said to do well at school or be grounded, and Cameron took them seriously. | Study very hard. |
| Riley had a lot of friends. | They will play with Riley. |
| Sydney found a biography of Hillary Clinton and wanted to read it. | Know more about Hillary Clinton. |
| Austin knew Quinn intimately and they slept together many times. | Found Quinn attractive. |
| Quinn broke into Ash's locker and stole a jacket. | Ashamed. |
