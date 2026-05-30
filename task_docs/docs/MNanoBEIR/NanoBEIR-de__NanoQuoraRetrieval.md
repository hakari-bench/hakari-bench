# MNanoBEIR / NanoBEIR-de / NanoQuoraRetrieval

## Overview

This task is the German NanoBEIR version of Quora Question Pairs, a duplicate-question retrieval benchmark. Unlike evidence retrieval tasks, the document collection is made of questions, and the goal is to retrieve German translated questions that express the same intent as the query. The original Quora Question Pairs data was released for duplicate question detection, and BEIR frames it as a retrieval task where semantic equivalence is the relevance criterion. This NanoBEIR slice contains 50 queries, 5,046 candidate questions, and 70 positive relevance judgments. Most queries have one duplicate, while 10 queries have multiple positives. The task is therefore a compact diagnostic for paraphrase retrieval, question intent matching, and the ability to distinguish true duplicates from merely topically related questions.

## Details

### What the Original Data Measures

Quora Question Pairs measures whether two user-written questions ask the same thing. In retrieval form, a system receives one question and must rank duplicate questions above non-duplicates. This differs from passage retrieval because both query and document are short question texts, and relevance is based on intent equivalence rather than answer evidence. A positive may share many words with the query, or it may preserve the same meaning through a different phrasing, word order, or level of detail.

### Observed Data Profile

The German Nano task has 50 queries, 5,046 documents, and 70 positives. Queries average 56 characters and documents average 65 characters, so both sides are short. Positives per query average 1.40, with a maximum of six. The examples include questions about laughing at one's own jokes, lies people have told, Donald Trump answers on Quora, physical fitness, and quantum satellites. Some positives are nearly identical, while others are paraphrases that add or remove context while preserving the same intent.

### BM25 Evaluation Profile

BM25 is strong on this task, with nDCG@10 of 0.718, Hit@10 of 0.880, and Recall@100 of 0.929. This reflects the high lexical overlap often present in duplicate questions. Exact or near-exact word reuse, shared named entities, and similar question templates give sparse matching a strong signal. BM25 can rank many duplicates very highly when the query and positive differ only by word order, inflection, or a small lexical substitution. Its main weakness is that genuine paraphrases may preserve intent while changing the visible wording.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline is the strongest by nDCG@10, reaching 0.832 with Hit@10 of 0.900 and Recall@100 of 0.914. This shows that embedding similarity is especially well matched to duplicate-question retrieval. Dense retrieval can recognize that two questions ask the same thing even when one uses a different construction or adds a clarifying phrase. Its Recall@100 is slightly below BM25, which suggests that lexical overlap still catches some positives that dense retrieval does not include in the broad candidate pool, but dense ranking is clearly better at ordering duplicates near the top.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.798, Hit@10 of 0.900, and Recall@100 of 0.943, with one safeguard row at 101 candidates. This is the best recall profile and matches dense Hit@10, while sitting between BM25 and dense on nDCG@10. The hybrid result reflects the nature of the task: lexical evidence is useful because duplicates often reuse wording, but semantic similarity is needed to handle paraphrase. Hybrid retrieval therefore gives the broadest candidate coverage, while dense retrieval alone gives the cleanest top ranking in this sample.

### Metric Interpretation for Model Researchers

For duplicate-question retrieval, nDCG@10 is a useful measure of ranking quality because positives are usually few and should appear at the very top. Hit@10 is already high for all methods, so it is less discriminative. Recall@100 helps diagnose whether a candidate generator is missing alternate duplicates, especially for queries with multiple positives. A good model should not merely retrieve questions on the same topic; it should rank questions with the same user intent above related but different questions.

### Query and Relevance Type Tendencies

The query and document texts are both short user questions. Relevance depends on duplicate intent, not answer overlap. Positive pairs may differ by spelling, synonym choice, word order, specificity, or added context. Hard negatives often mention the same entities or topic but ask a different question. This makes the task sensitive to semantic textual similarity, intent preservation, and the distinction between paraphrase and topical relatedness.

### Representative Failure Modes

BM25 can miss paraphrases when a duplicate question uses different vocabulary. Dense retrieval can over-rank questions that are semantically adjacent but not duplicates, such as two questions about the same public figure or technology with different intents. Hybrid retrieval improves coverage but can still promote lexical near-matches that ask a different question. Failure analysis should compare the intended answer or action implied by each question, not just shared tokens.

### Training and Leakage Considerations

Training should exclude Quora Question Pairs, BEIR, NanoBEIR, and translated duplicate-question records likely to overlap with this evaluation slice. Useful non-overlapping data includes German and multilingual paraphrase pairs, semantic textual similarity data, duplicate-question corpora, and hard-negative question retrieval examples. Synthetic data should generate alternate German phrasings of short questions while also creating same-topic non-duplicates for contrastive training.

### Model Improvement Signals

A strong model should improve top-rank duplicate placement without confusing topic overlap for equivalence. Useful training signals include paraphrase pairs, near-duplicate templates, lexical substitutions, and hard negatives that change the requested relation or answer. Hybrid systems should preserve exact duplicate detection while allowing dense similarity to lift paraphrases that use different wording.

## Example Data

| Query | Positive Document |
|---|---|
| Ist es in Ordnung, über seine eigenen Witze zu lachen? | Ist es merkwürdig, über meine eigenen Witze zu lachen? |
| Welche ist die beste Lüge, die du je erzählt hast? | Welche ist die beste Lüge, die du je erzählt hast? |
| Warum schlägt Quora mir häufig Antworten vor, die Donald Trump kritisieren? | Warum gibt es auf Quora nur voreingenommene Antworten zu Fragen über Donald Trump? |
| Wie werde ich körperlich fit? | Wie kann ich körperlich fit werden? |
| Wie funktioniert ein Quanten-Satellit? | Wie funktioniert ein Quanten-Satellit und welche Hauptanwendungen hätte er? |

## Public Sources

- [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| Quora Question Pairs | https://kaggle.com/competitions/quora-question-pairs |
| BEIR benchmark | https://github.com/beir-cellar/beir |
| MMTEB benchmark | https://arxiv.org/abs/2502.13595 |
| NanoBEIR dataset | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
