# NanoMTEB-French / xpqa_fra_fra

## Overview

`xpqa_fra_fra` is the monolingual French xPQA product retrieval split. Queries
are French customer questions, and documents are short French answer snippets.
The Nano split contains 200 queries, 1,547 documents, and 424 positive qrels,
with an average of 2.12 positives per query. Documents average 76.98 characters
and often contain concise answer evidence such as yes/no polarity,
compatibility, material, dimensions, or customer experience. Compared with the
cross-lingual xPQA French splits, this task is more lexically accessible, but it
still tests whether retrieval models understand answerability in short
e-commerce text.

## Details

### What the Original Data Measures

[xPQA: Cross-Lingual Product Question Answering across 12 Languages](https://arxiv.org/abs/2305.09249)
focuses on product QA across languages. In the monolingual French split, both
questions and answer snippets are French, but the task remains product-domain
candidate ranking: a model must retrieve snippets that contain enough
information to answer practical shopping or usage questions.

Unlike passage retrieval, documents are answer-sized snippets. The model must
distinguish direct answers from snippets that merely mention a similar product
or property.

### Observed Data Profile

The split has 200 French queries, 1,547 French documents, and 424 positive
judgments. Queries average 54.61 characters, and documents average 76.98
characters. Each query has one to five positives, with a median of two; 102
queries, or 51.0%, have multiple positives.

Questions ask about Android boxes, Fitbit extensions, plastic versus glass,
smartphone compatibility, blue-light protection, instruction manuals, product
weight, repair suitability, drawer size, and gaming headset compatibility.
Documents are short answer snippets, often with polarity or customer-report
language.

### BM25 Evaluation Profile

BM25 is relatively strong here, reaching nDCG@10 of 0.5644, hit@10 of 0.7550,
and recall@100 of 0.8042. The monolingual setting gives BM25 access to shared
French terms, product names, dimensions, and property words. Compared with the
cross-lingual XPQA splits, exact term overlap is much more informative.

BM25 still misses a meaningful share of positives. Product questions often use
paraphrases, and answer snippets may phrase the same property differently. A
query about compatibility, for example, may be answered by a customer statement
that does not repeat the exact product wording.

### Dense Evaluation Profile

Dense retrieval is strongest at top-10 ranking, with nDCG@10 of 0.6400,
hit@10 of 0.8050, and recall@100 of 0.8703. Dense retrieval improves over BM25
by capturing semantic equivalence between a customer question and a concise
answer. It is especially useful when the answer contains a reformulation, a
customer-use statement, or polarity that is not captured by shared keywords
alone.

The gap is smaller than in cross-lingual XPQA because BM25 already has a useful
monolingual signal. This makes `xpqa_fra_fra` a balanced diagnostic: models
need both lexical precision and semantic answerability.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile reaches nDCG@10 of 0.6208, hit@10 of 0.7700,
and recall@100 of 0.8915. It has the highest recall@100 of the three candidate
profiles, while dense remains slightly stronger in nDCG@10 and hit@10. Candidate
lists contain 100 to 101 rows, with 16 safeguard-positive rows.

This is a good example of hybrid search doing what it is meant to do: it
combines lexical and dense evidence to expose more relevant snippets to a
downstream reranker. The top ranking is still not automatically better than
dense, but the broader candidate coverage is useful for reranking experiments.

### Metric Interpretation for Model Researchers

`xpqa_fra_fra` is dense-favorable at top-10 and hybrid-favorable for recall.
BM25 is competitive because the query and documents are both French, dense
retrieval improves early ranking, and `reranking_hybrid` provides the broadest
top-100 relevant coverage. This three-way pattern is useful for studying whether
a model should be evaluated as a first-stage retriever, a candidate generator,
or a reranking input source.

Because many queries have multiple positives, recall@100 should be read as
coverage of answerable snippets rather than only one target document. nDCG@10
and hit@10 then show whether the candidate source places useful answers early
enough for user-facing retrieval.

### Query and Relevance Type Tendencies

Queries are French product questions about practical shopping and use details.
Positive documents are snippets that directly answer the question, sometimes
with yes/no polarity and sometimes with a customer description. Several snippets
can be relevant when they answer the same question in different wording.

Relevance is not the same as product topicality. A snippet about the same
product is insufficient if it does not answer the requested property. This
distinction makes same-product hard negatives particularly valuable.

### Representative Failure Modes

BM25 can miss positives when the query and answer use different French
formulations, or when the answer is a customer statement rather than a direct
metadata field. Dense retrieval can retrieve a semantically related snippet that
answers a neighboring property. Hybrid retrieval can increase recall while
still ranking a lexically obvious but non-answering snippet too high.

Polarity and negation are critical. A "Non" answer can be close in topic but
opposite in meaning to a positive expectation, so models need to preserve the
actual answer value.

### Training Data That May Help

Useful training data includes xPQA French train examples, French e-commerce QA
pairs, customer-question to answer-snippet retrieval pairs, and same-product or
same-category hard negatives. Training should exclude xPQA test examples, Nano
queries, qrels, and positive product snippets.

Synthetic data should create short French product answer snippets with
polarity, dimensions, materials, care instructions, compatibility, and customer
evidence. Multi-positive training is appropriate because several snippets may
answer the same question.

### Model Improvement Notes

Strong models should combine French lexical matching with semantic
answerability. Dense encoders should handle paraphrase, short snippets,
polarity, and product attributes. Rerankers should learn to reject snippets that
share product vocabulary but fail to answer the specific question.

## Example Data

| Query | Positive document |
| --- | --- |
| bonjour, quels sont les avantages de cette box android, comparée aux autres ? merci [83 chars] | Un client dit qu'en comparison aux autres box Android qu'il a eu, celle-là est une des meilleurs parce qu'elle est facile à installer et a une grande capacité de stockage. [171 chars] |
| sur quel produit fitbit avez vous essayé cette extension ? [58 chars] | Un client dit que ce produit fonctionnait très bien sur un Fitbit Charge. [73 chars] |
| bonjour, la vitre est-elle en verre ou en plastique? [52 chars] | Un client dit que la vitre est en plastique transparent et qu'elle protège bien les photos. [91 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| xPQA: Cross-Lingual Product Question Answering across 12 Languages | 2023 | Paper | [https://arxiv.org/abs/2305.09249](https://arxiv.org/abs/2305.09249) |
| MTEB: Massive Text Embedding Benchmark | 2023 | Paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |
| mteb/XPQARetrieval | 2025 | Dataset card | [https://huggingface.co/datasets/mteb/XPQARetrieval](https://huggingface.co/datasets/mteb/XPQARetrieval) |

### Representative Snippets

| Query | Positive document |
| --- | --- |
| bonjour, quels sont les avantages de cette box android, comparee aux autres ? merci | A French customer answer saying the box is easy to install and has large storage capacity. |
| sur quel produit fitbit avez vous essaye cette extension ? | A French customer answer saying it worked well on a Fitbit Charge. |
| bonjour, la vitre est-elle en verre ou en plastique ? | A French snippet saying the transparent front is plastic and protects photos. |
| cet article est-il compatible avec un smartphone de 5.5 pouces ? | A French yes-answer saying it is compatible with any handlebar and any device. |
| bonjour est ce anti lumiere bleue ? | Non, ce produit n'est pas anti-lumiere bleue. |
