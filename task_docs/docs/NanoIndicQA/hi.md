# NanoIndicQA / hi

## Overview

`NanoIndicQA / hi` is the Hindi split of IndicQA retrieval. The queries are Hindi reading-comprehension questions, and the documents are Hindi context paragraphs that support the answer.

This task evaluates Hindi evidence paragraph retrieval. The model must rank the context paragraph that contains the answer evidence, often among long biographical, historical, or political paragraphs with overlapping vocabulary.

## Details

### What the Original Data Measures

IndicQA is part of IndicXTREME, introduced in "Towards Leaving No Indic Language Behind". It is a manually curated cloze-style reading-comprehension task across Indic languages.

In the MTEB retrieval formulation, the question is the query and the source context paragraph is the document. The Hindi split tests context retrieval for Hindi QA rather than answer extraction.

### Observed Data Profile

This Nano split contains 200 queries, 261 documents, and 201 positive qrels. Queries have 1.005 positives on average, with a minimum of 1, a median of 1.0, and a maximum of 2. One query is multi-positive. Queries average 56.91 characters, and documents average 2,550.77 characters.

Observed examples ask about Art Deco buildings, the caste background of the Nanda dynasty, a temple construction in Bengal without Akbar's permission, Akbar's reign, and the renaming of Prayagraj to Allahabad. Several sampled questions target long biography or historical passages.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4545, hit@10 of 0.6400, and recall@100 of 0.8856. The candidate pool contains the full 261-document corpus. BM25 is weaker here than in several other IndicQA splits.

The weakness comes from long Hindi paragraphs that share broad political, historical, and biographical vocabulary. Exact term matching may retrieve a paragraph about Akbar, Mughal history, or architecture without selecting the exact context needed for the question.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.6511, hit@10 of 0.7900, and recall@100 of 0.8557. Dense retrieval is the strongest direct ranking profile.

Dense retrieval improves top-10 ranking substantially, suggesting that semantic question-context matching helps with long Hindi paragraphs. Its recall@100 is lower than BM25, so it is better at ranking the top results than at broad candidate coverage.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.5738, hit@10 of 0.7300, and recall@100 of 0.9652. It uses 100 candidates per query, with seven rank-101 safeguard positives.

Hybrid retrieval gives the best recall@100 but does not match dense retrieval on top-10 ranking. It is therefore valuable as a reranking pool, while dense retrieval is the stronger first-stage ranker.

### Metric Interpretation for Model Researchers

`NanoIndicQA / hi` is a Hindi small-corpus context retrieval task where dense and hybrid profiles serve different roles. Dense retrieval is better for immediate top-10 quality, while hybrid retrieval is better for candidate coverage.

Since almost every query has one positive, nDCG@10 and hit@10 are direct measures of correct-context placement. Recall@100 diagnoses whether the candidate generator supplies the positive to a downstream reranker.

### Query and Relevance Type Tendencies

Queries are Hindi factual or cloze-style questions. Documents are long Hindi context paragraphs, often about Indian history, rulers, architecture, cities, religion, and political events.

The relevance relation is evidence support. The positive paragraph contains the fact or explanation needed to answer the query.

### Representative Failure Modes

BM25 may retrieve a paragraph with the same named entity but the wrong event or date. Dense retrieval may select a semantically similar biography or historical passage without the exact evidence. Hybrid retrieval improves recall but still requires reranking for precise support.

Long paragraphs can dilute the answer signal because many unrelated facts appear in one context.

### Training Data That May Help

Useful training data includes Hindi extractive QA, Hindi Wikipedia passage retrieval, multilingual IndicQA context retrieval, and hard negatives from the same biography, region, dynasty, or political topic.

Training should exclude this split's questions and positive context paragraphs.

### Model Improvement Notes

Improving this task requires Hindi language coverage, long-context handling, and evidence-sensitive ranking. Models should preserve named entities, dates, places, and relation cues while handling paraphrased questions.

For reranking, the model should verify that the paragraph contains the requested answer evidence rather than simply matching a broad historical topic.

## Example Data

### Public Sources

This task is documented through the IndicXTREME paper, the `mteb/IndicQARetrieval` dataset card, and the upstream `ai4bharat/IndicQA` dataset card. The Nano split is published in `hakari-bench/NanoIndicQA`.

### Source Reference Table

| Source | Role |
| --- | --- |
| [Towards Leaving No Indic Language Behind](https://arxiv.org/abs/2212.05409) | IndicXTREME and IndicQA benchmark paper. |
| [mteb/IndicQARetrieval](https://huggingface.co/datasets/mteb/IndicQARetrieval) | MTEB retrieval task dataset card. |
| [ai4bharat/IndicQA](https://huggingface.co/datasets/ai4bharat/IndicQA) | Upstream IndicQA dataset card. |
| [hakari-bench/NanoIndicQA](https://huggingface.co/datasets/hakari-bench/NanoIndicQA) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A Hindi question asking where Art Deco buildings are most numerous. | A paragraph about architectural influences, European forms, and Mumbai-style built heritage. |
| A question asking which varna the Nanda dynasty kings belonged to. | A historical paragraph drawing on Puranic, Jain, Buddhist, and Greek accounts of the Nandas. |
| A question asking who began building a temple in Bengal without Akbar's permission. | A paragraph about Akbar's religious policy and Raja Man Singh's temple construction. |
| A question asking who ruled Delhi from 1542 to 1605. | A long paragraph about Akbar, his religious interests, and rule. |
| A question asking in which year Prayagraj was named Allahabad. | A paragraph about Akbar and historical naming context. |
