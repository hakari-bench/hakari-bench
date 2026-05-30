# NanoFaMTEB-v2 / miracl_fa

## Overview

`miracl_fa` is a Persian MIRACL retrieval task in NanoFaMTEB-v2. The queries are short Persian information-seeking questions, and the documents are Persian Wikipedia-style passages drawn from a hard-negative MIRACL retrieval pool.

This task evaluates whether a model can retrieve fact-bearing Persian passages for natural web-search questions. Many queries contain explicit entities or named concepts, but the hard-negative construction makes the task more demanding than title matching: competing passages may share names, topics, or related relations while missing the requested answer.

## Details

### What the Original Data Measures

FaMTEB includes MIRACL as a Persian retrieval resource for evaluating multilingual and Persian embedding models. MIRACL itself is designed around ad hoc retrieval over Wikipedia-style passages, with queries that resemble real information needs.

The public source used here is `mteb/MIRACLRetrievalHardNegatives`. Its dataset card describes hard negatives pooled from BM25, e5-multilingual-large, and e5-mistral-instruct rankings. As a result, the Nano task is useful for comparing lexical matching, dense semantic retrieval, and hybrid candidate construction under a Persian retrieval setting with already challenging negatives.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 427 positive qrels. Queries have 2.14 positives on average, with a minimum of 1, a median of 2.0, and a maximum of 8. There are 105 multi-positive queries, or 52.5% of the split. Queries average 39.99 characters, and documents average 413.55 characters.

Observed examples ask factual questions about international relations, Iranian ministers, geographic regions, provincial capitals, and plant taxonomy. Positive documents are usually compact encyclopedia passages centered on the requested entity, event, place, or definition.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4929, hit@10 of 0.8000, and recall@100 of 0.9555 with a top-500 candidate pool. This is a high recall profile: exact Persian terms, entity names, and answer-bearing keywords allow BM25 to include relevant passages in the candidate set for most queries.

The weaker nDCG@10 shows that lexical matching is less reliable at ordering the most useful passages near the top. MIRACL hard negatives often share topic words with positives, so BM25 can retrieve passages about a related country, minister, city, or concept without ranking the precise answer passage first.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.6318, hit@10 of 0.8750, and recall@100 of 0.8993. Dense retrieval is the strongest top-ranking signal in this task, improving nDCG substantially over BM25.

This suggests that semantic similarity helps distinguish the requested fact from nearby lexical matches. Dense retrieval can connect question intent to a passage even when the passage does not repeat every query term exactly. Its recall@100 is lower than BM25, so it is better as a top-ranking signal than as the only broad candidate generator.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.5931, hit@10 of 0.9050, and recall@100 of 0.9906. It uses 100 candidates per query, with one query containing a rank-101 safeguard positive.

This is the best coverage profile. Hybrid retrieval combines BM25's exact-term recall with dense retrieval's ability to prefer semantically matching passages. For MIRACL-Fa, that means the hybrid pool is especially useful for reranking experiments: nearly all relevant passages are present in the top-100 candidate set, even though dense-only ranking has the best nDCG@10 among the three initial profiles.

### Metric Interpretation for Model Researchers

`miracl_fa` separates candidate coverage from first-stage ranking quality. BM25 provides broad lexical recall, dense retrieval provides stronger top-10 ordering, and reranking_hybrid provides the most complete top-100 candidate pool.

Researchers should treat nDCG@10 as a measure of how well a model prioritizes the exact answer passage among hard negatives. Recall@100 is also important because more than half of the queries have multiple positives. A reranker that starts from the hybrid pool can test passage-ordering ability without being heavily limited by first-stage candidate misses.

### Query and Relevance Type Tendencies

Queries are short Persian questions, often asking "what", "where", or "who" style factual needs. They frequently include an entity name or a distinctive concept. Relevant passages are encyclopedia-like and usually contain the answer in a concise descriptive paragraph.

The relevance relation is direct: a passage is positive when it supplies the requested fact or definition. The difficulty comes from related passages that share entities or topical vocabulary but do not answer the exact question.

### Representative Failure Modes

BM25 may over-rank a passage that repeats query terms but concerns the wrong relation. Dense retrieval may prefer a semantically related passage while missing a rare named entity or exact title. Hybrid retrieval reduces both problems, but reranking still has to choose between very similar Persian encyclopedia passages.

Another common risk is partial relevance for multi-positive queries. A model may retrieve one correct passage while failing to cover alternative valid passages or related supporting descriptions.

### Training Data That May Help

Useful training data includes Persian Wikipedia retrieval, MIRACL-style query-passage pairs, multilingual hard-negative retrieval data, Persian QA search logs, and entity-centric contrastive pairs. Hard negatives should mention the same entity, country, location, office, or scientific term while omitting the requested answer.

Training should exclude MIRACL-Fa rows sampled into this Nano split.

### Model Improvement Notes

A strong model for this task should preserve exact Persian entity matching while also representing the relation asked by the query. Improvements may come from Persian-aware tokenization, multilingual retrieval pretraining, and hard-negative mining that forces the model to distinguish "same topic" from "answers the question".

For reranking, the most useful behavior is precise discrimination among near-duplicate or topically adjacent passages. The hybrid pool already has very high recall, so the remaining challenge is top-10 ordering.

## Example Data

### Public Sources

This task is documented through the FaMTEB paper and the `mteb/MIRACLRetrievalHardNegatives` dataset card. MTEB provides the broader benchmark framework, and MIRACL provides the original multilingual retrieval benchmark context.

### Source Reference Table

| Source | Role |
| --- | --- |
| [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571) | Persian embedding benchmark paper. |
| [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316) | General embedding benchmark framework. |
| [MIRACL project](http://miracl.ai/) | Original MIRACL benchmark context. |
| [mteb/MIRACLRetrievalHardNegatives](https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives) | Public hard-negative source dataset card. |
| [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A Persian question asking which countries have friendly relations with Israel. | A passage about Israeli foreign relations and historical recognition by Iran before 1979. |
| A question asking who currently holds Iran's Ministry of Culture and Islamic Guidance. | A biographical passage about Mohammad Mehdi Esmaeili and his ministerial role. |
| A question asking where the Bermuda Triangle is located. | A passage defining the region in the western North Atlantic Ocean. |
| A question asking which city is the capital of Nova Scotia. | A passage identifying Halifax as the capital and major city of the province. |
| A question asking about the genus or type of a fern-like plant. | A passage about an extinct tree-like plant with fern-like leaves. |
