# NanoFaMTEB-v2 / syn_per_qa

## Overview

`syn_per_qa` is a synthetic Persian QA retrieval task in NanoFaMTEB-v2. The query is a Persian question, and the target document is a concise answer passage generated or curated for the synthetic QA setting.

This task evaluates direct question-to-answer retrieval for Persian RAG systems. Unlike the chatbot FAQ task, the queries are already clean questions rather than long dialogues. The task is therefore a useful high-baseline benchmark for answer passage matching.

## Details

### What the Original Data Measures

FaMTEB reports that many new Persian datasets were generated with LLMs, including synthetic datasets for retrieval and RAG systems. `syn_per_qa` uses `MCINext/synthetic-persian-qa-retrieval`, evaluated through the MTEB retrieval framework.

The task measures whether a retriever can map a Persian question to the short passage that answers it. Because the data is synthetic, question and answer wording often align clearly, but the benchmark still tests Persian semantic matching, named entities, and answer sufficiency.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 200 positive qrels. Each query has exactly one positive. Queries average 59.81 characters, and documents average 306.22 characters.

Observed examples ask whether an actor appeared in a known television series, which publisher released a book, whether a verse was revealed in Mecca, how to obtain a print copy of a book, and why Egypt has attracted Iranian attention. Positive documents are concise Persian answer passages.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.8609, hit@10 of 0.9400, and recall@100 of 0.9900 with a top-500 candidate pool. This is a very strong lexical profile.

The synthetic QA format often repeats key entities, titles, and answer concepts between question and passage. BM25 can therefore locate the correct passage for most queries. The remaining errors likely come from semantically equivalent wording, broad background passages, or distractors that share the same named entity.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.9204, hit@10 of 0.9600, and recall@100 of 0.9750. Dense retrieval is the strongest direct top-ranking profile.

Dense retrieval improves nDCG and hit rate over BM25 by matching the question's answer intent rather than only repeated words. It can connect a question to an answer passage even when the passage is explanatory and does not mirror the question exactly. Its recall@100 is slightly below BM25, but still very high.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.9173, hit@10 of 0.9550, and recall@100 of 0.9950. It uses 100 candidates per query, with one rank-101 safeguard positive.

Hybrid retrieval is best for candidate coverage and nearly matches dense retrieval on top-10 ranking. This makes it a strong reranking pool: it combines BM25's broad exact-match coverage with dense retrieval's answer-intent matching.

### Metric Interpretation for Model Researchers

`syn_per_qa` is a high-scoring synthetic QA retrieval task. It is useful for checking whether a model handles clean Persian question-answer matching, but it may be less discriminative than harder web, scientific, or dialogue tasks.

Since each query has one positive, nDCG@10 and hit@10 directly reflect whether the correct answer passage appears near the top. Recall@100 shows that BM25 and hybrid pools almost always include the answer, so reranking experiments should focus on fine ordering rather than candidate recovery.

### Query and Relevance Type Tendencies

Queries are natural Persian questions about general facts, history, books, religious context, public figures, and explanations. Documents are answer passages, usually short and self-contained.

The relevance relation is direct answerability: the positive document should answer the question, not merely discuss the same topic.

### Representative Failure Modes

BM25 may over-rank a passage with the same entity name but no direct answer. Dense retrieval may prefer a plausible explanatory passage that is semantically close but not the labeled answer. Hybrid retrieval reduces candidate misses, but reranking can still confuse similar synthetic answer passages.

Because the data is synthetic, another risk is overfitting to templated wording. Models trained only on similar generated QA may perform well here while being less robust on noisy user queries.

### Training Data That May Help

Useful training data includes Persian QA pairs, synthetic QA retrieval, RAG passage matching, translated open-domain QA, and hard negatives that answer related but distinct questions.

Training should exclude evaluation questions and answer passages from this split.

### Model Improvement Notes

Improving this task requires answer-intent matching and strong Persian entity handling. Models should identify whether a passage actually contains the answer and not only whether it shares the topic.

For reranking, the main opportunity is rejecting related answer-like passages and choosing the one that directly addresses the question. Because candidate recall is already very high, improvements will mostly come from top-rank precision.

## Example Data

| Query | Positive document |
| --- | --- |
| آیا بینگ راسل در فیلم‌های معروفی مانند 'دود اسلحه' نقش داشته است؟ [65 chars] | بله، بینگ راسل در مجموعه تلویزیونی 'دود اسلحه' که از سال ۱۹۵۶ تا ۱۹۷۴ پخش می‌شد، نقش Ed Shelby را ایفا کرد. این مجموعه یکی از محبوب‌ترین و شناخته‌شده‌ترین سریال‌های وسترن در تاریخ تلویزیون است. [193 chars] |
| کتاب تحقیق در عملیات پیشرفته در چه انتشاراتی منتشر شده است؟ [59 chars] | این کتاب توسط انتشارات دانشگاه شهید بهشتی منتشر شده است. این انتشارات به عنوان یکی از مراکز معتبر در نشر آثار علمی و پژوهشی در ایران شناخته می‌شود. [147 chars] |
| آیا این آیه در مکه نازل شده است؟ [32 chars] | نه، این آیه در مدینه بر پیامبر اسلام صلی الله علیه و آله نازل گردیده است. [73 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571) | Persian embedding benchmark paper. |
| [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316) | General embedding benchmark framework. |
| [MCINext/synthetic-persian-qa-retrieval](https://huggingface.co/datasets/MCINext/synthetic-persian-qa-retrieval) | Public source dataset card. |
| [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A question asking whether Bing Russell appeared in a well-known television western. | An answer passage confirming the role and giving context about the series. |
| A question asking which publisher released an advanced operations research book. | A passage naming Shahid Beheshti University Press and describing the publisher. |
| A question asking whether a verse was revealed in Mecca. | A short answer stating that it was revealed in Medina. |
| A question asking how to obtain a print copy of a book of Saadi quatrains. | A passage explaining that the print copy can be ordered from an online book platform. |
| A question asking why Egypt has long attracted Iranian attention. | An explanatory passage discussing cultural, civilizational, regional, and religious reasons. |
