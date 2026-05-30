# NanoMedical / NanoMedicalQA

## Overview

`NanoMedical / NanoMedicalQA` is an English medical FAQ retrieval task. Queries are short consumer-health questions, and candidate documents are trusted-source answer passages. The task is connected to medical question answering work using Recognizing Question Entailment and MedQuAD-style trusted medical QA resources. In this Nano split, each query has exactly one positive document, so the main challenge is retrieving the right answer type for a disease or condition. It is useful for studying consumer-health retrieval where disease names are strong lexical anchors but relevance depends on whether the passage answers symptoms, diagnosis, prevention, treatment, or definition.

## Details

### What the Original Data Measures

The source paper studies medical question answering through question entailment and reliable answer retrieval. It introduces MedQuAD, a large collection of medical question-answer pairs from trusted sources, and emphasizes matching user questions to already answered medical questions and their answers.

This retrieval task presents the same problem in direct form: the query is a medical question, and the target document is an answer-bearing passage. The answer text is consumer-facing guidance rather than a scientific abstract.

### Observed Data Profile

The Nano split contains 200 queries, 2,007 documents, and 200 positive qrel rows. Each query has exactly one positive. Queries average 54.23 characters, while documents average 1,102.43 characters.

The examples ask about nocardiosis symptoms, babesiosis treatment, zoonotic hookworm diagnosis, lymphatic filariasis prevention, and hookworm prevention. Many queries follow FAQ templates such as `What are the symptoms`, `How to diagnose`, `How to prevent`, or `What are the treatments`.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.5439, hit@10 of 0.8550, and recall@100 of 0.9200. BM25 performs well because disease names, parasite names, and answer-type words often repeat in the answer passage.

Its main weakness is answer-type confusion. A passage about the correct disease may describe symptoms when the query asks for treatment, or define a condition when the query asks for prevention. Sparse matching can find the disease neighborhood but may not select the exact FAQ section.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.7308, hit@10 of 0.8850, and recall@100 of 0.9250. Dense retrieval is clearly stronger than BM25 in top-rank quality, while recall@100 is only slightly higher.

This indicates that semantic modeling helps distinguish answer types and match question intent. Dense retrieval can better rank a treatment answer above a definition answer when both share the same condition name.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 6 queries carrying a rank-101 safeguard positive. It reaches nDCG@10 of 0.6510, hit@10 of 0.8650, and recall@100 of 0.9700. Hybrid retrieval has the best recall@100, but dense retrieval remains strongest by nDCG@10 and hit@10.

This shows that lexical and dense signals are complementary for coverage, while dense retrieval is better at top-rank answer-type selection. A reranker can benefit from the hybrid pool if it explicitly learns FAQ answer categories.

### Metric Interpretation for Model Researchers

This is a single-positive task, so nDCG@10 and hit@10 are direct measures of whether the one correct answer passage appears early. Recall@100 shows candidate-generation completeness for reranking.

Because questions are templated, high performance can hide answer-type errors. Researchers should inspect whether failures retrieve the right condition but wrong section.

### Query and Relevance Type Tendencies

Queries are concise medical FAQ questions about symptoms, treatments, diagnosis, prevention, definitions, or causes. Relevant documents are longer consumer-health guidance passages from trusted medical sources.

The relevance relation is exact answer type for the condition. A same-disease passage is not enough if it answers a different question.

### Representative Failure Modes

Common failures include retrieving the correct disease but wrong answer type, confusing similar parasites or infections, ranking broad overview passages above specific treatment or diagnosis passages, and over-weighting repeated organism names. Dense systems can still miss exact disease variants; sparse systems often miss the question intent.

### Training Data That May Help

Useful training data includes non-overlapping medical FAQ retrieval pairs, consumer-health question-answer datasets, MedQuAD-style trusted-source QA pairs, and answer-type reranking data for definition, diagnosis, prevention, symptoms, and treatment. Overlapping MedQuAD pages and near-duplicate templated questions should be excluded for clean evaluation.

### Model Improvement Notes

Models should learn both disease matching and answer-type discrimination. Hard negatives should use the same disease name but a different answer type. Rerankers should treat question words such as diagnose, prevent, symptoms, and treatments as central relevance signals, not incidental tokens.

## Example Data

### Public Sources

- [A question-entailment approach to question answering](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3119-4), 2019.
- [DOI record](https://doi.org/10.1186/s12859-019-3119-4).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| A question-entailment approach to question answering | 2019 | BMC Bioinformatics article | https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3119-4 |
| A question-entailment approach to question answering | 2019 | DOI | https://doi.org/10.1186/s12859-019-3119-4 |

### Representative Snippets

| Query | Relevant answer excerpt |
| --- | --- |
| What are the symptoms of Nocardiosis ? | An answer explaining that symptoms vary by affected body part and listing lung infection symptoms such as fever, weight loss, and night sweats. |
| What are the treatments for Parasites - Babesiosis ? | An answer explaining that effective treatments are available and that asymptomatic people usually do not need treatment. |
| How to diagnose Parasites - Zoonotic Hookworm ? | An answer describing cutaneous larva migrans diagnosis based on signs, symptoms, and exposure history. |
| How to prevent Parasites - Lymphatic Filariasis ? | An answer recommending avoiding mosquito bites, especially between dusk and dawn. |
| How to prevent Parasites - Hookworm ? | An answer recommending not walking barefoot in contaminated areas and avoiding skin contact with contaminated soil. |
