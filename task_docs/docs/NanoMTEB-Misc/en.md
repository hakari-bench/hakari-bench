# NanoMTEB-Misc / en

## Overview

`en` is the English EuroPIRQ retrieval split. Queries are synthetic English
questions, and documents are English passages derived from DGT-Acquis
paragraph-level European Union legal and administrative texts. The Nano split
contains 100 queries, 9,422 documents, and 100 positive qrels, with exactly one
positive passage per query. Queries average 140.43 characters, and documents
average 550.09 characters. The task is a high-precision legal and
administrative passage retrieval benchmark where synthetic questions often
reuse distinctive institutions, articles, directives, and procedural language.

## Details

### What the Original Data Measures

The [EuroPIRQ dataset card](https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval)
describes European Parallel Information Retrieval Queries built from
DGT-Acquis paragraph-level corpus chunks. English, Finnish, and Portuguese
passages are aligned, cleaned, language-checked, and paired with synthetic
questions. No standalone EuroPIRQ task paper was confirmed; interpretation is
based on the dataset card and MTEB/MMTEB benchmark context.

In this English split, retrieval measures whether a model can map a generated
question to the source EU legal or administrative paragraph. The passages are
formal and often contain dense legal references, institutions, and procedural
phrasing.

### Observed Data Profile

The split has 100 English queries, 9,422 documents, and 100 positive judgments.
Every query has one positive. Questions are longer than typical factoid queries
because they ask about legal interpretation, institutional procedure, or policy
effect. Documents are medium-length EU legal, committee, court, and
administrative passages.

Examples ask about integrated markets, high-speed train connections,
lifelong-learning strategies, Article 56 EC taxation, and Form RS information
requirements. These questions often preserve distinctive wording from the
positive passage.

### BM25 Evaluation Profile

BM25 is very strong, with nDCG@10 of 0.9414, hit@10 of 0.9700, and recall@100
of 1.0000. This indicates that the English EuroPIRQ split is highly lexical.
Synthetic questions frequently contain exact legal terms, named institutions,
article numbers, or policy phrases that appear in the target passage.

The remaining errors are likely near-duplicate legal boilerplate cases, where
several passages share procedural language and only one is the positive. BM25 is
therefore a near-ceiling baseline.

### Dense Evaluation Profile

Dense retrieval is also strong, with nDCG@10 of 0.9255, hit@10 of 0.9600, and
recall@100 of 0.9900. It successfully maps most questions to the corresponding
passage, but it is slightly weaker than BM25 in both top ordering and coverage.
This suggests that exact legal wording and references are particularly valuable
in this split.

For model researchers, dense underperformance relative to BM25 should be read
as a precision issue in formal legal text rather than a failure of general
semantic matching.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile is the best overall, with nDCG@10 of 0.9438,
hit@10 of 0.9800, and recall@100 of 1.0000. It slightly improves over BM25 at
top-10 and preserves full recall. Candidate lists contain exactly 100 entries,
with no safeguard-positive rows.

This is a near-ceiling hybrid case. Lexical evidence does most of the work, but
semantic matching helps resolve a few passages where wording is paraphrased or
where multiple legal passages share surface terms.

### Metric Interpretation for Model Researchers

`en` is a high-scoring lexical/hybrid task. BM25 and `reranking_hybrid` are
near ceiling, while dense retrieval is close behind. Since every query has one
positive, nDCG@10 directly reflects whether the exact source passage is ranked
early, and recall@100 reflects candidate recoverability.

The task is useful for regression checks and for legal-domain precision
analysis. It is less useful as a hard semantic benchmark unless questions are
rewritten to reduce lexical overlap.

### Query and Relevance Type Tendencies

Queries are English synthetic questions about EU law, administrative procedure,
transport policy, education strategy, competition law, and taxation. Positive
documents are formal passages from EU legal or administrative material.

Relevance is source-passage identity. A passage with similar legal wording may
be a hard negative if it is not the paragraph that answers the generated
question.

### Representative Failure Modes

BM25 can confuse near-duplicate legal boilerplate or passages sharing article
numbers and institution names. Dense retrieval can rank a semantically related
legal paragraph that lacks the exact procedural detail. Hybrid retrieval
reduces both risks but still operates near a ceiling where small ordering
differences matter.

Formal EU text can also include long nested clauses, making it easy for models
to match the topic while missing the precise condition being asked.

### Training Data That May Help

Useful training data includes legal and EU-domain passage retrieval pairs,
synthetic question-passage pairs, DGT-Acquis-style parallel corpora, and hard
negatives from the same institution, regulation, or court decision. Training
should exclude EuroPIRQ evaluation questions and positive passages that overlap
with this Nano split.

Synthetic data should generate questions from non-evaluation EU legal and
administrative paragraphs, preserving exact names, directives, dates, and
institutions in some questions while adding paraphrases in others.

### Model Improvement Notes

Models should preserve exact legal references and institutional terms while
handling controlled paraphrase. Dense encoders can improve by training on
near-duplicate legal hard negatives. Rerankers should focus on the specific
condition or procedural relation in the question.

## Example Data

| Query | Positive document |
| --- | --- |
| What is required for the ongoing process of building and operating an integrated market? [88 chars] | Finally, building a fully integrated market is not a definite task with a finite end, but rather an ongoing process requiring constant effort, vigilance and updating. There are always new challenges a... [200 / 504 chars] |
| How do high-speed train connections contribute to social and economic cohesion in the EU? [89 chars] | However, the Commission notes that air transport is not the only driver of development in terms of regional accessibility. High-speed train connections also make a significant contribution to social a... [200 / 498 chars] |
| What are the challenges faced by Member States in implementing national lifelong learning strategies... [100 / 117 chars] | The implementation of national lifelong learning strategies and instruments, which are key to enabling not only young people, but also adults, to acquire, maintain and develop knowledge, skills and co... [200 / 581 chars] |
| How does Article 56 EC affect the taxation of dividends received by a resident company from a non-re... [100 / 168 chars] | Article 56 EC is, furthermore, to be interpreted as meaning that it precludes legislation of a Member State which exempts from corporation tax dividends which a resident company receives from another... [200 / 564 chars] |
| What is the purpose of requiring undertakings to provide sufficient information in Form RS? [91 chars] | Given the above mechanism, it is crucial to the smooth operation of Article 4(5) that all Member States where the case is reviewable under national competition law, and which are hence competent to ex... [200 / 515 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| EuroPIRQ-retrieval | 2025 | Dataset card | [https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval](https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | Benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| MTEB: Massive Text Embedding Benchmark | 2022 | Benchmark paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |

### Representative Snippets

| Query | Positive document excerpt |
| --- | --- |
| What is required for building and operating an integrated market? | A passage describing integrated markets as an ongoing process requiring effort and updating. |
| How do high-speed train connections contribute to cohesion in the EU? | A passage noting that high-speed trains contribute to social and economic cohesion. |
| What challenges affect lifelong learning strategies and instruments? | A passage about implementing national lifelong-learning strategies for young people and adults. |
| How does Article 56 EC affect taxation of dividends from non-resident companies? | A legal passage interpreting Article 56 EC and corporation-tax treatment. |
| What is the purpose of requiring undertakings to provide information in Form RS? | A competition-law passage about the operation of Article 4(5) and Member State review. |
