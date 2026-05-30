# NanoRuMTEB / ru_bq

## Overview

`ru_bq` is a Russian KBQA evidence retrieval task from NanoRuMTEB. The queries are concise Russian open-domain questions derived from RuBQ 2.0, and the documents are Russian Wikipedia paragraphs. The retriever must find paragraphs that support the answer relation, not just paragraphs about the same entity. Dense retrieval is the strongest top-rank profile, `reranking_hybrid` has the best recall@100, and BM25 is a strong but clearly weaker lexical baseline.

## Details

### What the Original Data Measures

RuBQ 2.0 is a Russian question answering dataset over knowledge-base relations, with questions, answers, SPARQL queries, and verified Wikipedia evidence for many questions.

ruMTEB includes RuBQRetrieval as a Russian retrieval benchmark. In the Nano task, the query is a KBQA-style question and the relevant documents are answer-bearing paragraphs from Russian Wikipedia.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 334 positive qrel rows. Queries average 52.19 characters, while documents average 484.49 characters. Positives per query average 1.67, with a minimum of 1, a median of 1, and a maximum of 4. There are 89 multi-positive queries, 44.5% of the split.

Example questions ask what Christmas Eve is otherwise called, which river Baghdad stands on, which theater Vladimir Vysotsky performed in, who created Alisa Selezneva, and which city is the capital of the Swiss Confederation.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.6979, hit@10 of 0.8400, and recall@100 of 0.9042. BM25 often succeeds when the subject entity, answer entity, or relation words appear directly in the paragraph.

Its limitation is relation matching. A paragraph about the same person, book, city, or country is not enough unless it contains the requested relation. Lexical overlap can retrieve same-entity distractors that do not answer the question.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.8739, hit@10 of 0.9400, and recall@100 of 0.9341. Dense retrieval is the strongest top-rank profile.

This indicates that embedding similarity handles Russian relation questions better than term frequency. It can connect question forms such as capital, author, location, alias, and family relation to evidence paragraphs even when wording differs.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 2 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.7767, hit@10 of 0.8950, and recall@100 of 0.9790. Hybrid retrieval has the best coverage but lower early ranking than dense retrieval.

The result shows that sparse entity matching expands the candidate pool, while dense retrieval better orders the answer-bearing paragraphs. Hybrid is a useful reranking source when relation-aware second-stage scoring is available.

### Metric Interpretation for Model Researchers

Because many queries have multiple positives, nDCG@10 measures whether answer-bearing evidence is ranked early, hit@10 measures whether at least one positive appears in the first ten, and recall@100 measures evidence availability for reranking.

For `ru_bq`, dense nDCG@10 is the strongest first-stage signal. Hybrid recall@100 is important for systems that can re-check the requested relation inside candidate paragraphs.

### Query and Relevance Type Tendencies

Queries are short Russian questions about entities and relations. Relevant documents are Russian Wikipedia paragraphs that explicitly support the answer. They may include broader article context rather than answer-only snippets.

Relevance is relation evidence. A paragraph that names the entity but omits the requested answer relation is not relevant.

### Representative Failure Modes

Common failures include retrieving a same-entity paragraph without the relation, confusing capitals or locations, overmatching author or work names, and missing paraphrased relation expressions. BM25 is sensitive to shared entity terms; dense retrieval can still confuse closely related relations.

### Training Data That May Help

Useful training data includes non-overlapping RuBQ questions and supporting paragraphs, Russian KBQA evidence retrieval, Wikidata relation questions paired with Russian Wikipedia evidence, and Russian open-domain QA with entity hard negatives. Evaluation questions, positive paragraphs, and qrels should be excluded.

### Model Improvement Notes

Models should encode entity relation semantics and Russian morphology. Hard negatives should come from the same article, same entity type, or same relation family but omit the answer. Dense retrieval is the best direct ranker, while hybrid retrieval is useful for high-recall candidate generation.

## Example Data

### Public Sources

- [RuBQ 2.0: An Innovated Russian Question Answering Dataset](https://openreview.net/forum?id=P5UQFFoQ4PJ), task paper.
- [The Russian-focused embedders' exploration: ruMTEB benchmark and Russian embedding model design](https://arxiv.org/abs/2408.12503), ruMTEB paper.
- [RuBQ project repository](https://github.com/vladislavneon/RuBQ), source repository.
- [RuBQ Zenodo record](https://doi.org/10.5281/zenodo.4345696), dataset record.
- [ai-forever/rubq-retrieval](https://huggingface.co/datasets/ai-forever/rubq-retrieval), source dataset card.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RuBQ 2.0: An Innovated Russian Question Answering Dataset | 2021 | OpenReview paper | https://openreview.net/forum?id=P5UQFFoQ4PJ |
| The Russian-focused embedders' exploration: ruMTEB benchmark and Russian embedding model design | 2025 | arXiv paper | https://arxiv.org/abs/2408.12503 |
| RuBQ project repository | 2021 | source repository | https://github.com/vladislavneon/RuBQ |
| RuBQ Zenodo record | 2020 | dataset record | https://doi.org/10.5281/zenodo.4345696 |
| ai-forever/rubq-retrieval | 2025 | dataset card | https://huggingface.co/datasets/ai-forever/rubq-retrieval |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Как иначе называется канун Рождества Христова? | Paragraph mentioning Christmas Eve and Christmas-related holidays. |
| На какой реке стоит город Багдад? | Paragraph stating that Baghdad stands on the Tigris River. |
| В каком театре выступал Владимир Высоцкий? | Paragraph about Vysotsky's work in theater collectives. |
| Кто придумал Алису Селезневу? | Paragraph describing Alisa Selezneva as a character by Kir Bulychev. |
| Какой из городов является столицей Швейцарской конфедерации? | Paragraph about Switzerland and its capital context. |
