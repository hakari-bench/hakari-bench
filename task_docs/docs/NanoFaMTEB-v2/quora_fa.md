# NanoFaMTEB-v2 / quora_fa

## Overview

`quora_fa` is a Persian duplicate-question retrieval task in NanoFaMTEB-v2. The query is a Persian question, and the documents are candidate questions that may express the same intent with different wording.

This task evaluates semantic question matching rather than passage answer retrieval. Many positives are close paraphrases with shared topic words, so lexical retrieval is strong, but the best models must also recognize equivalent meaning when word order, specificity, or phrasing changes.

## Details

### What the Original Data Measures

FaMTEB includes translated and Persian retrieval datasets for evaluating Persian text embeddings. `quora_fa` uses `MCINext/quora-fa-v2`, a Persian Quora-style duplicate-question dataset evaluated through the MTEB retrieval framework.

The original Quora-style task measures whether two questions ask the same thing. In retrieval form, each query question must retrieve semantically equivalent questions from a large pool. This makes the task a direct test of paraphrase retrieval, not document topicality or answer extraction.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 candidate questions, and 570 positive qrels. Queries have 2.85 positives on average, with a minimum of 1, a median of 1.0, and a maximum of 47. There are 80 multi-positive queries, or 40.0% of the split. Queries average 48.67 characters, and candidate documents average 60.81 characters.

Observed examples ask about drama series, whether mathematics is art or science, the best classical music piece, GMAT training institutes in Delhi/NCR, and the strengths of the Indian army. Positives are alternate Persian wordings of the same question.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.8393, hit@10 of 0.9550, and recall@100 of 0.8895 with a top-500 candidate pool. This is a strong lexical baseline. Duplicate questions often share rare entities, topical nouns, and short phrase fragments.

BM25's limitation appears when equivalent questions use different wording. It may miss paraphrases that replace a key word, change the syntactic form, or ask the same intent at a different level of specificity. It may also over-rank near-topic questions that share the same subject but ask a different thing.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.9122, hit@10 of 0.9500, and recall@100 of 0.9298. Dense retrieval is the strongest nDCG@10 profile and improves recall over BM25.

This is the expected pattern for duplicate-question retrieval. Embedding similarity can model paraphrase equivalence beyond exact token overlap, so it ranks semantically equivalent questions higher even when wording differs. The slight hit@10 advantage for BM25 is less important than dense retrieval's stronger ranking quality and broader positive coverage.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.8861, hit@10 of 0.9850, and recall@100 of 0.9439. It uses 100 candidates per query, with one rank-101 safeguard positive.

Hybrid retrieval is strongest for candidate coverage and top-10 hit rate. Dense retrieval is still the best direct top-ranking signal, but hybrid retrieval creates the most complete reranking pool by combining exact question-term overlap with semantic paraphrase matching.

### Metric Interpretation for Model Researchers

`quora_fa` is a clean semantic similarity task. BM25 is high because duplicates often preserve the same content words, but dense retrieval better captures paraphrase. reranking_hybrid is most useful when the goal is to feed a reranker with a high-coverage candidate list.

nDCG@10 is the main ranking indicator because many queries have one or a few positives. Recall@100 is important for the subset of queries with many duplicate variants, especially the query with as many as 47 positives.

### Query and Relevance Type Tendencies

Queries and documents are both short questions. They tend to be everyday, opinion, factual, education, music, technology, or general knowledge questions. Positives are questions that ask the same thing, not passages that answer the query.

The relevance boundary is semantic equivalence. A question about the same topic is not necessarily positive if it asks for a different comparison, recommendation, cause, or fact.

### Representative Failure Modes

BM25 may confuse questions that share the same noun phrase but differ in intent. Dense retrieval may over-generalize and retrieve broadly similar opinion questions that are not duplicates. Hybrid retrieval reduces candidate misses but still requires reranking to distinguish exact duplicate intent from near-topic similarity.

Questions with many acceptable paraphrases can be difficult because some positives may be short, informal, or structurally different from the query.

### Training Data That May Help

Useful training data includes Persian question paraphrase pairs, duplicate-question retrieval, multilingual Quora translations, natural question rewrites, and hard negatives that share the main topic but ask a different intent.

Training should exclude evaluation question IDs and their positive duplicate labels from this Nano split.

### Model Improvement Notes

Improving this task requires strong sentence-level semantic matching in Persian. Models should handle reordering, synonymy, added or removed modifiers, and formal versus informal question phrasing.

For reranking, the key behavior is recognizing equivalence rather than topical relatedness. A good reranker should reject questions that sound related but would receive a different answer.

## Example Data

| Query | Positive document |
| --- | --- |
| بهترین سریال‌های درام کدام‌اند؟ [31 chars] | بهترین سریال‌های درام کدام‌ها هستند؟ [36 chars] |
| آیا ریاضیات را به عنوان هنر می‌بینید یا علم؟ [44 chars] | آیا ریاضی هنر است یا علم؟ [25 chars] |
| به نظر شما بهترین آهنگ کلاسیک تمام دوران کدام است؟ [50 chars] | بهترین قطعه موسیقی کلاسیک تمام دوران کدام است؟ [46 chars] |
| بهترین موسسات آموزش آزمون جی‌مات در دهلی/NCR کدام‌ها هستند؟ [59 chars] | بهترین موسسه آموزش آزمون جی‌مات در منطقه دهلی ان‌سی‌آر کدام است؟ [64 chars] |
| بهترین نقاط قوت ارتش هند کدامند؟ [32 chars] | بزرگترین نقاط قوت ارتش هند کدامند؟ [34 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571) | Persian embedding benchmark paper. |
| [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316) | General embedding benchmark framework. |
| [MCINext/quora-fa-v2](https://huggingface.co/datasets/MCINext/quora-fa-v2) | Public source dataset card. |
| [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A question asking which drama series are best. | A paraphrased question asking for the best drama shows. |
| A question asking whether mathematics should be considered art or science. | A shorter question asking whether math is art or science. |
| A question asking for the best classical song or piece of all time. | A paraphrase asking for the best classical music piece ever. |
| A question asking for top GMAT training institutes in Delhi/NCR. | A reworded question asking which GMAT coaching institute is best in the same region. |
| A question asking about the best strengths of the Indian army. | A paraphrase asking for the greatest strengths of the Indian army. |
