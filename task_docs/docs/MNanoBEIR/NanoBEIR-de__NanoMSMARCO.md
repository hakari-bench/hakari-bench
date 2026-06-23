# MNanoBEIR / NanoBEIR-de / NanoMSMARCO

## Overview

This task is the German NanoBEIR version of MS MARCO, a web question answering and passage ranking benchmark built from real search-engine queries. The original MS MARCO dataset was designed around user information needs rather than questions written from a known paragraph, so the retrieval problem is noisy, practical, and often underspecified. In this NanoBEIR slice, each query is a short German web-search style question and the system must retrieve the German answer-bearing passage from a pool of 5,043 documents. There are 50 queries and 50 positive relevance judgments, with exactly one positive passage per query. The task is therefore a compact diagnostic for short-query answer passage retrieval: models must connect everyday German questions to concise passages that directly answer them, even when surface wording is incomplete, informal, or only partially overlaps with the document text.

## Details

### What the Original Data Measures

MS MARCO measures the ability to rank passages for real user questions drawn from Bing search logs. Unlike many curated QA datasets, its questions were not authored to match a specific evidence paragraph. They include definitions, procedural questions, consumer information needs, medical or legal-looking queries, fragments, entity questions, and ambiguous phrasing. In BEIR and NanoBEIR, the task is evaluated as passage retrieval: the model is not asked to generate the answer, but to place the answer-bearing passage high enough for a reader or reranker to use.

### Observed Data Profile

The German Nano task has 50 queries, 5,043 documents, and 50 positives. Every query has one relevant passage, so the benchmark emphasizes finding the single best answer document rather than assembling multiple evidence pieces. Average query length is about 41 characters, making this one of the more short-query-oriented German NanoBEIR tasks. Documents average about 364 characters and usually contain a direct explanatory answer in a few sentences. Example topics include medical definitions, song performers, television roles, desert geography, and word meanings.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.350, Hit@10 of 0.540, and Recall@100 of 0.800. This is a moderate sparse-retrieval profile: lexical matching often finds candidates because queries contain distinctive nouns, names, or phrases, but top-10 ranking is limited by the short and answer-seeking nature of the queries. A question such as a definition request may share only one important term with the relevant passage, while several distractors can repeat the same term without answering the information need. BM25 is strongest when the query contains rare entities, quoted titles, or specific terminology, and weakest when the passage answers by paraphrase or explanatory context.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline is stronger here than BM25, with nDCG@10 of 0.473, Hit@10 of 0.680, and Recall@100 of 0.940. This indicates that semantic answerability is central to this task. Dense retrieval can connect short German questions to passages that use different wording but express the answer relation, such as connecting "what does a term mean" to a definition paragraph or matching a practical question to an explanatory passage. The high Recall@100 suggests that dense candidates usually include the positive passage, although exact top placement still leaves room for stronger models and rerankers.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.439, Hit@10 of 0.680, and Recall@100 of 0.940, with a top-100 candidate set and three safeguard rows at 101 candidates. It matches dense recall and Hit@10 but trails dense nDCG@10, which means the hybrid candidate strategy successfully preserves answer-bearing passages but does not always order them as well as dense retrieval alone. This is an important diagnostic: hybrid search is useful for coverage, but on short MS MARCO-style questions the semantic signal can dominate the first page of results. Sparse terms still help protect entity-heavy and exact-title queries.

### Metric Interpretation for Model Researchers

Because each query has only one positive, Hit@10 and Recall@100 are straightforward measures of whether the answer passage was found. nDCG@10 adds rank sensitivity and is the most useful signal for comparing models that retrieve the positive somewhere in the first page but differ in exact placement. The gap between BM25 Recall@100 and dense or hybrid Recall@100 suggests that candidate generation is a major part of the task; if a system cannot place the single positive in the candidate pool, later reranking cannot recover it.

### Query and Relevance Type Tendencies

Queries are short and often look like web-search questions rather than complete academic prompts. They ask what something is, who performed a song, where a geographic category appears, how long a food can be stored, or what a phrase means. Relevant documents are usually concise answer passages. The model must infer the answer-bearing relation, not merely detect topical similarity. Passages sharing the same named entity but not answering the question should be treated as hard negatives.

### Representative Failure Modes

BM25 can over-rank passages that repeat the head term but do not answer the question. Dense retrieval can over-rank semantically related explanations that fit the broad topic but miss the exact entity, time span, or definition requested. Hybrid retrieval inherits both risks: it improves coverage by combining lexical and semantic evidence, but the final order can still favor a plausible distractor over the only positive passage.

### Training and Leakage Considerations

MS MARCO is widely used for retriever and reranker training, so leakage audits are essential. Evaluation should exclude MS MARCO, BEIR, NanoBEIR, and translated records likely to overlap with these queries or passages. Useful non-overlapping data includes German or multilingual web QA retrieval pairs, search-query-to-answer-passage corpora, and noisy user-question datasets. Synthetic data should generate concise German web questions from answer passages while preserving direct answerability.

### Model Improvement Signals

A strong model for this task should combine robust German query understanding with precise answer-passage discrimination. Training should include short and underspecified queries, paraphrased definitions, entity questions, and hard negatives that share the same topic but not the answer. Improvements in dense retrieval should appear as higher nDCG@10 without losing Recall@100, while hybrid systems should show that sparse exact-match benefits do not disrupt semantic ordering.

## Example Data

| Query | Positive document |
| --- | --- |
| Was ist das Ruminationssyndrom? [31 chars] | Ruminationssyndrom, auch Merykismus genannt, ist eine nicht näher bezeichnete Essstörung, die das Erbrechen von Nahrung verursacht. Obwohl es im DSM-IV nicht als spezifische Essstörung identifiziert wird, wurden bestimmte Kriterien für die Diagnose der Störung festgelegt. [272 chars] |
| Wer hat den Song "Here I Go Again" gesungen? [44 chars] | Für andere Verwendungen siehe Here I Go Again (Bedeutungsübersicht). Here I Go Again ist ein Lied der britischen Rockband Whitesnake. Ursprünglich erschien das Lied 1982 auf ihrem Album Saints & Sinners. Für das gleichnamige Album Whitesnake aus dem Jahr 1987 wurde es neu aufgenommen. Im selben Jahr wurde das Lied erneut in einer neuen Radio-Mix-Version aufgenommen. [368 chars] |
| Wen spielt Cameron Boyce in Liv und Maddie? [43 chars] | Bereitet euch auf ordentlich Lacher vor, Leute. In einem exklusiven Vorab-Blick auf die Folge vom 19. April von Liv & Maddie mit dem Titel „Prom-A-Rooney.“ Natürlich. Im lustigen Clip sehen wir den Jessie-Star Cameron Boyce in eine andere Disney-Serie wechseln, um Maddie (Shelby Wulfert) zu treffen. Seine Figur ist, ähm, ziemlich exzentrisch! [344 chars] |

## Public Sources

- [MS MARCO paper](https://arxiv.org/abs/1611.09268)
- [MS MARCO dataset site](https://microsoft.github.io/msmarco/Datasets.html)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| MS MARCO paper (https://arxiv.org/abs/1611.09268) |
| MS MARCO dataset site (https://microsoft.github.io/msmarco/Datasets.html) |
| BEIR benchmark (https://github.com/beir-cellar/beir) |
| MMTEB benchmark (https://arxiv.org/abs/2502.13595) |
| NanoBEIR dataset (https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
