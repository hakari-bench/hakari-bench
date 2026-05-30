# NanoMTEB-Dutch / legal_qanl

## Overview

`legal_qanl` is a Dutch legal question-to-law retrieval task from MTEB-NL.
Queries are natural-language legal questions, and documents are Dutch law
article chunks with statute, chapter, article, and provision text. The Nano
split contains 102 queries, 10,000 documents, and 157 positive qrel rows. It is
a multi-positive task: 41 queries have more than one positive, with an average
of 1.54 positives per query and a maximum of eight.

The task evaluates statute retrieval rather than general web QA. BM25 is very
strong because legal questions often repeat formal nouns, statute names, powers,
or procedural terms found in the relevant law article. Dense retrieval is also
strong but slightly lower than BM25. `reranking_hybrid` has the best nDCG@10
and recall@100, showing that hybrid search is useful when legal terminology and
semantic question intent both matter. The task is especially relevant for RAG
systems that need to ground Dutch legal answers in source provisions.

## Details

### What the Original Data Measures

[Retrieval-Augmented Generation for Long-form Question Answering in Dutch](https://aclanthology.org/2024.nllp-1.12/)
introduces a Dutch legal QA dataset where answers are tied to Dutch legal
source material. The retrieval component is designed to find law articles or
article chunks that ground long-form legal answers. MTEB-NL includes this task
as LegalQANLRetrieval.

This benchmark is therefore about legal source retrieval. Questions often ask
when a permit may be refused, when an objection may be filed, when an exemption
can be withdrawn, when a person has no right to assistance, or when a legal
community is dissolved. The target documents are formal statutory provisions,
not conversational answers.

### Observed Data Profile

The split has 102 queries over 10,000 documents. Queries average 104.29
characters, which is longer than most headline or duplicate-question tasks.
Documents average 665.01 characters and often begin with statute and article
metadata before the provision text. The metadata structure is important because
legal relevance can depend on the exact law, chapter, section, and article.

The qrels are notably multi-positive. 40.20% of queries have multiple positive
documents, and one query has eight positives. This means retrieval quality
should not be reduced to finding a single article. Several provisions may
jointly ground an answer, or multiple article chunks may be acceptable evidence
for the same legal question.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.8143, hit@10 = 0.9804, and recall@100 = 0.9618 over
top-500 candidate lists. The high hit rate reflects the formal vocabulary of
law. Queries and provisions often share terms such as permit, objection,
exemption, assistance, article names, authorities, deadlines, and legal
conditions.

The remaining challenge is precision among similar provisions. Several
articles can mention the same authority, procedure, or statute but differ in
scope, exception, or condition. BM25 can identify the correct legal area, but
ranking the exact grounding article requires understanding the legal relation
asked by the query.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.8050, hit@10 =
0.9608, and recall@100 = 0.9108. Dense retrieval is strong but trails BM25.
This suggests that exact legal terminology and article metadata are highly
valuable. Dense representations capture semantic question intent, but may lose
some specificity around formal legal wording.

Dense retrieval is most useful when a question paraphrases a provision or uses
plain-language wording for a legal concept. Its likely failure mode is
retrieving a semantically related provision that belongs to the wrong article,
condition, or exception.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.8455, hit@10 =
0.9706, and recall@100 = 0.9745, with 100 to 101 candidates per query and one
rank-101 safeguard row. It has the best nDCG@10 and recall@100, even though
BM25 has the highest hit@10. This is the most useful overall candidate profile
for reranking.

Hybrid search fits legal retrieval well. BM25 preserves exact statute and
article terms, while dense retrieval helps with questions phrased in everyday
Dutch. The hybrid pool should give rerankers strong coverage of relevant legal
provisions and adjacent hard negatives, enabling more precise legal grounding.

### Metric Interpretation for Model Researchers

This task has 157 positives for 102 queries, so multi-positive evaluation is
important. Hit@10 is already very high and can hide differences in ranking
quality. nDCG@10 and recall@100 are more informative because they reflect how
well systems rank or cover multiple relevant provisions.

The pattern also warns against dense-only conclusions. In formal legal text,
lexical overlap is not a shallow baseline; it encodes statute names, article
language, and procedural terms. The best systems should combine exact legal
terms with semantic understanding of the question.

### Query and Relevance Type Tendencies

Queries are Dutch legal questions about powers, rights, conditions, deadlines,
exceptions, permit rules, and procedural actions. Relevant documents are law
article chunks that explicitly ground the answer. Many queries begin with
"when" or ask which legal authority may act under a condition.

Relevance is source grounding. A passage about the same statute is not always
sufficient; it must contain the provision that answers the specific legal
question. Multiple provisions can be relevant when an answer requires several
legal conditions or cross-referenced article chunks.

### Representative Failure Modes

BM25 can fail by over-ranking adjacent provisions with the same legal terms but
different conditions. Dense retrieval can fail by finding a semantically
similar law article that lacks the exact rule. Hybrid retrieval can still place
nearby provisions above the true positive when both share statute metadata and
related legal vocabulary.

Text normalization can also matter. Some query samples contain encoding
artifacts while documents may contain normal Dutch accents. Robust retrieval
should avoid losing matches because of encoding differences.

### Training Data That May Help

Useful training data includes non-overlapping Dutch legal QA pairs with statute
attributions, Dutch law article search or citation data, public legal question-
answer data with source articles, and hard negatives from adjacent law articles
and similar provisions. Training should exclude LegalQA-NL evaluation
questions, qrels, and law article chunks used by this Nano split.

Synthetic data can be generated from non-evaluation Dutch legal provisions.
Create questions about powers, rights, conditions, deadlines, and exceptions.
The positive article should explicitly answer the question, and hard negatives
should come from nearby articles or similar legal powers.

### Model Improvement Notes

Improving this task requires legal-structure awareness. Models should encode
statute names, article hierarchy, and formal conditions, not only the free-text
question. Multi-positive training should be preserved because several
provisions may jointly ground a legal answer.

For rerankers, the key behavior is legal scope discrimination: does the
candidate article answer this specific legal question, or does it merely belong
to the same statute or procedure? Hybrid retrieval provides a strong candidate
pool for that decision.

## Example Data

### Public Sources

- [Retrieval-Augmented Generation for Long-form Question Answering in Dutch](https://aclanthology.org/2024.nllp-1.12/), 2024.
- [MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch](https://arxiv.org/abs/2509.12340), 2025.
- [clips/mteb-nl-legalqa-pr](https://huggingface.co/datasets/clips/mteb-nl-legalqa-pr), source dataset card.
- [MTEB project repository](https://github.com/embeddings-benchmark/mteb).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Retrieval-Augmented Generation for Long-form Question Answering in Dutch | 2024 | ACL paper | https://aclanthology.org/2024.nllp-1.12/ |
| MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch | 2025 | arXiv paper | https://arxiv.org/abs/2509.12340 |
| clips/mteb-nl-legalqa-pr |  | dataset card | https://huggingface.co/datasets/clips/mteb-nl-legalqa-pr |
| MTEB project repository |  | repository | https://github.com/embeddings-benchmark/mteb |

### Representative Snippets

| Query | Positive passage |
| --- | --- |
| Wanneer wordt een vergunning voor ruimtevaartactiviteiten geweigerd? | A Dutch law article chunk lists conditions under which a space-activity permit must be refused. |
| Wanneer kan het bezwaarschrift worden ingediend voor een WOB verzoek? | A Dutch provision describes the special objection or appeal rule under the public information law. |
| Wanneer kan een ontheffing volgens de Opiumwet worden ingetrokken? | A Dutch legal article states conditions under which an exemption can be withdrawn. |
| Wanneer heeft iemand geen recht op bijstand? | A Dutch provision lists exclusions from social assistance, including deprivation of liberty and other legal conditions. |
| Wanneer wordt de gemeenschap van rechtswege ontbonden? | A Dutch civil-code article describes when the legal community of property is dissolved by operation of law. |
