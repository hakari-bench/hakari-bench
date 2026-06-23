# NanoRARb / NanoQuail

## Overview

`NanoQuail` is an English reading-comprehension answer retrieval task from NanoRARb. It recasts QuAIL as retrieval: the query contains a long narrative passage plus a question, and the relevant document is the correct short answer option. Each query has one positive answer. The task is difficult because the query is long and full of distractor context, while the answer document is often only a short phrase. Dense retrieval improves over BM25, but both remain low; the hybrid pool gives similar recall to dense but weaker top-rank ordering.

## Details

### What the Original Data Measures

RAR-b converts QuAIL into a reasoning-as-retrieval task by pooling answer options and asking a retriever to locate the gold answer. The original QuAIL benchmark targets reading comprehension over passages that require prerequisite reasoning, narrative tracking, and question-specific interpretation.

In this Nano task, the retriever is not finding a supporting passage. It must retrieve the answer option that correctly responds to the question given the long context.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Every query has exactly one positive. Queries average 1,813.76 characters, while answer documents average only 25.02 characters.

Examples are long story or scene passages followed by questions about what happens next, when an event occurred, or which inference is supported. Some correct answers are specific event descriptions, while others are generic options such as insufficient information.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.0522, hit@10 of 0.1250, and recall@100 of 0.2850. BM25 is weak because the long query contains many words unrelated to the answer, and the answer option may be short or paraphrased.

Sparse retrieval is especially brittle when the correct answer is a generic phrase or when many answer candidates reuse common narrative terms. Exact word matching does not determine which answer is licensed by the passage and question.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.1174, hit@10 of 0.2150, and recall@100 of 0.4600. Dense retrieval improves over BM25 across all metrics. It can connect the question to a plausible answer phrase better than term frequency alone.

The absolute score remains low because the retriever must compress a long context and question into the specific answer relation. Generic or very short answer options provide little semantic signal.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 107 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.0982, hit@10 of 0.1900, and recall@100 of 0.4650. Hybrid retrieval slightly improves recall@100 over dense retrieval but has weaker top-ten ranking.

This pattern suggests that sparse overlap adds some answer coverage but can pull in many distractors from the long context. Dense retrieval is the better first-stage ranker, while hybrid retrieval is a useful coverage-oriented reranking pool.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 is mostly the rank quality of the correct answer, hit@10 measures whether it appears in the first ten candidates, and recall@100 measures whether a reranker can see it.

For QuAIL, the challenge is long-context answer selection. Improvements should come from question-focused reading comprehension rather than generic passage-answer similarity.

### Query and Relevance Type Tendencies

Queries include long narrative contexts plus a question. Relevant documents are short answer options. The answer may refer to an event, character decision, temporal relation, or inference from the passage.

Relevance is conditional on the question. A phrase that appears plausible for the passage can be wrong if it does not answer the specific question.

### Representative Failure Modes

Common failures include matching an answer phrase to an incidental passage word, ranking generic options incorrectly, losing the question focus inside the long context, and confusing chronological relations. BM25 overweights context words; dense retrieval can prefer a plausible narrative phrase that is not the gold answer.

### Training Data That May Help

Useful training data includes reading-comprehension answer selection, long-passage QA, narrative QA, and retrieval tasks where short answer options are grounded in long contexts. Evaluation passages and answers should be excluded.

### Model Improvement Notes

Models should learn question-aware compression of long contexts into answer candidates. Hard negatives should be plausible answer options that share passage words but fail the specific question. Rerankers may need explicit cross-attention over context, question, and answer.

## Example Data

| Query | Positive document |
| --- | --- |
| Context: It took Erin an hour and forty-five minutes to drive from their half-million dollar home in... [100 / 1,562 chars] | will have an argument with Erin [31 chars] |
| Context: I actually managed a kind of sleep there, kneeling with the circulation cut off to my legs,... [100 / 1,943 chars] | After someone pulled the hood off their head. [45 chars] |
| Context: I'm a senior at Cesar Chavez high in San Francisco's sunny Mission district, and that makes... [100 / 1,746 chars] | After I was told to report to the administration office immediately. [68 chars] |
| Context: Candy watched the bearded man drive his silver BMW into the convenience store parking lot a... [100 / 1,746 chars] | After the bearded man drove his silver BMW into the convenience store parking lot. [82 chars] |
| Context: They re-shackled and re-hooded me and left me there. A long time later, the truck started t... [100 / 1,831 chars] | After they took off my hood. [28 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | [https://arxiv.org/abs/2404.06347](https://arxiv.org/abs/2404.06347) |
| Getting Closer to AI Complete Question Answering: A Set of Prerequisite Real Tasks | 2020 | proceedings paper | [https://ojs.aaai.org/index.php/AAAI/article/view/6398](https://ojs.aaai.org/index.php/AAAI/article/view/6398) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| A long context describes Erin driving to a rented cabin, with a question about what may happen. | Erin will have an argument. |
| A passage describes someone sleeping under a hood and later reacting to removal. | After someone pulled the hood off their head. |
| A student narrative includes being called by school administration. | After being told to report to the administration office immediately. |
| A context describes a bearded man driving into a convenience-store parking lot. | After the man drove his BMW into the parking lot. |
| A passage describes being re-shackled, re-hooded, and later moved. | After they took off the hood. |
