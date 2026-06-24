# NanoMTEB-Polish / quora

## Overview

`quora` is the Polish NanoMTEB version of a Quora Question Pairs hard-negative retrieval task. The source benchmark is duplicate-question detection: given one short question, the system must retrieve questions that express the same user intent. In this Polish version, both queries and documents are short question texts, and relevance is based on semantic duplication rather than answer-bearing evidence.

The Nano split contains 200 queries, 10,000 documents, and 485 positive relevance judgments. Queries average about 53 characters and documents about 65 characters, making this a short-text paraphrase retrieval task. The average positives per query is 2.425, 72 queries have multiple positives, and the largest cluster has 33 positives. The task therefore tests both one-to-one paraphrase retrieval and duplicate clusters of common questions.

## Details

### What the Original Data Measures

Quora Question Pairs was released as a dataset of question pairs labeled for duplicate meaning. In retrieval form, the task asks whether a model can rank semantically equivalent questions above hard negatives. A relevant document should ask the same question, not just mention the same topic.

This task is important because short-question paraphrases expose subtle differences. Two questions can be duplicates with different word order or synonyms, while two other questions can share most words but ask a different condition, entity, or action. The Polish version adds translated wording and Polish morphology to that paraphrase problem.

### Observed Data Profile

The text is much shorter than passage-retrieval tasks. Many queries and documents are single-sentence questions with little context. Examples include questions about getting into Harvard, random facts about oneself, improving a data-analytics CV, emotional exhaustion, and whether an iPhone is worth its price.

Because the documents are short, exact content words often dominate. But the model still needs semantic paraphrase ability. A duplicate may replace "get into Harvard" with "get into Harvard University" or "emotionally exhausted" with "overcome emotional exhaustion." These are easy for humans but require robust representation of intent.

### BM25 Evaluation Profile

BM25 is very strong, with nDCG@10 of 0.7704, hit@10 of 0.9100, and recall@100 of 0.8309. This reflects the short-text nature of the task. Duplicate questions often share key content words, and there is little long-document noise. Exact overlap on names, nouns, and verbs gives BM25 a high baseline.

BM25 still has clear limitations. It can miss duplicates that use different wording, and it can over-rank near negatives that share terms while changing the question's meaning. In Quora-style data, a small change in condition or requested action can make two similar questions non-duplicates.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run is strongest at top ranks, with nDCG@10 of 0.9073, hit@10 of 0.9600, and recall@100 of 0.9526. Dense retrieval excels because the task is essentially semantic paraphrase matching. It can connect equivalent questions even when wording changes, while still using shared content words when they are present.

The dense gain over an already strong BM25 baseline is meaningful. It shows that short-question duplicate retrieval is not only lexical. Embedding similarity captures intent-level equivalence, which is exactly what the task rewards.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reports nDCG@10 of 0.8207, hit@10 of 0.9500, and recall@100 of 0.9691. Candidate lists contain exactly 100 items, and no rows use the positive safeguard. Hybrid retrieval has the best recall@100 but lower top-10 ranking than dense retrieval.

This suggests that hybrid search is excellent for preserving duplicate candidates, but lexical fusion can disturb the dense ordering at the very top. For direct search, dense retrieval is the stronger baseline. For reranking, hybrid candidates are attractive because they keep more positives available.

### Metric Interpretation for Model Researchers

This split is dense-favorable for direct ranking and hybrid-favorable for recall. BM25 is already strong because duplicate questions share short lexical cues, but dense retrieval clearly improves nDCG@10. Hybrid retrieval should be interpreted as a candidate-generation tool rather than a final-ranking winner.

Because query and document lengths are short, score differences are less affected by long-document noise. This makes the task a clean diagnostic for paraphrase representation. A model that improves over dense retrieval here is likely better at short-text semantic equivalence.

### Query and Relevance Type Tendencies

Representative pairs include "How do I get into Harvard?" and "How do I get into Harvard University?", questions about random facts about oneself, improving a CV to get data-analytics interviews, overcoming emotional exhaustion, and whether an iPhone is worth the price. These examples are direct paraphrases with minor lexical or syntactic changes.

Harder examples likely involve shared topics but different intent. A good model must preserve the exact question focus: action, target entity, condition, and requested outcome.

### Representative Failure Modes

BM25 may fail when paraphrases use different words, or when a near negative shares the same content words but changes the meaning. Dense retrieval may overgeneralize and retrieve questions with similar sentiment or topic but different user intent. Hybrid retrieval can inherit both issues: exact lexical matches and broad semantic neighbors can both be false positives.

Another failure mode is ignoring small modifiers. Words like "really", "worth", "best", "should", or a changed entity can alter the question. Duplicate retrieval requires matching the full intent, not just the topic.

### Training Data That May Help

Useful training data includes non-overlapping Quora Question Pairs data, Polish paraphrase datasets, translated duplicate-question pairs, and hard negatives that are topically similar but non-duplicate. Short question-pair supervision is more relevant here than long passage retrieval data.

Hard negatives should be close: questions that share many tokens but change the entity, time, condition, or desired action. These examples teach the model not to treat topical overlap as duplicate meaning.

### Model Improvement Notes

Dense models can improve by representing short Polish questions at intent level while preserving small semantic modifiers. Sparse systems already perform well, but they need synonym and paraphrase robustness to close the gap. Hybrid systems are useful for recall, especially before a reranker that can resolve near-duplicate distinctions.

For evaluation, nDCG@10 is the clearest indicator of direct paraphrase retrieval quality, while recall@100 is useful for candidate generation. This split makes dense ranking quality easy to observe because the texts are short and the duplicate relation is direct.

## Example Data

| Query | Positive document |
| --- | --- |
| Jak dostać się na Harvard? [26 chars] | Jak dostać się na Uniwersytet Harvarda? [39 chars] |
| Czym jest 10-20 przypadkowych rzeczy o sobie? [45 chars] | Jakie są 10 przypadkowych faktów o Tobie? [41 chars] |
| Co powinienem zrobić w swoim CV, aby uzyskać wywiady z zakresu analityki danych? [80 chars] | Co powinienem poprawić w swoim CV, aby uzyskać wywiady z zakresu analityki danych? [82 chars] |

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| Quora Question Pairs release | Original duplicate-question dataset source. |
| MTEB paper | Retrieval benchmark framing for Quora. |
| MTEB task card | Polish hard-negative retrieval packaging. |

### Representative Snippets

- A query asks how to get into Harvard; the relevant document asks how to get into Harvard University.
- A query asks for ten random things about oneself; the relevant document asks for ten random facts about you.
- A query asks what to change in a CV to get data-analytics interviews; the relevant document asks what to improve in the same CV context.
- A query asks how to cope with feeling emotionally exhausted; the relevant document asks how to overcome emotional exhaustion.
- A query asks whether the iPhone is really worth its price; the relevant document asks whether the iPhone is worth it.
