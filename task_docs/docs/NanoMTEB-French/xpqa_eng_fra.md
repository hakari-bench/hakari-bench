# NanoMTEB-French / xpqa_eng_fra

## Overview

`xpqa_eng_fra` is a cross-lingual product-question retrieval task from xPQA.
Queries are French product questions, while documents are English product
answer candidates or snippets. The Nano split contains 200 queries, 1,674
documents, and 451 positive qrels. Unlike single-answer QA tasks, this split has
an average of 2.255 positives per query, and 52.5% of queries have multiple
positive snippets. The task is a strong diagnostic for cross-lingual retrieval
in e-commerce: the model must connect French customer wording to English
specifications, reviews, warranties, dimensions, compatibility statements, and
other product facts.

## Details

### What the Original Data Measures

[xPQA: Cross-Lingual Product Question Answering across 12 Languages](https://arxiv.org/abs/2305.09249)
introduced a cross-lingual product QA benchmark where non-English questions are
matched to English candidates containing answer evidence. The benchmark is
domain-specific: product questions often ask about compatibility, size, warranty,
materials, setup, accessories, or subjective experience. These cues differ from
general web QA and from Wikipedia-style retrieval.

In `xpqa_eng_fra`, the retrieval model sees French questions and English
candidate documents. The goal is not only translation, but answerability: a
positive snippet must contain enough information to answer the product question.

### Observed Data Profile

The split has 200 mostly French queries, 1,674 mostly English documents, and
451 positive judgments. Queries average 54.61 characters, and documents average
137.30 characters. Each query has between one and five positives, with a median
of two. Documents are short product snippets, sometimes written as customer
answers and sometimes as metadata-like fields such as warranty descriptions or
dimensions.

The multiple-positive structure matters. A model does not need to retrieve a
single canonical answer; it should retrieve any snippet that answers the
question. This makes recall valuable, but the cross-lingual direction and short
snippets make candidate generation difficult.

### BM25 Evaluation Profile

BM25 is weak in this cross-lingual direction, reaching nDCG@10 of 0.1061,
hit@10 of 0.2050, and recall@100 of 0.3149. This is expected: French query
terms rarely match English answer text except through shared product codes,
brand names, units, numbers, and occasional cognates. BM25 can surface useful
candidates when the question contains a model name or dimension, but most of
the answerability signal is not lexical within a single language.

The low recall@100 means a BM25-only top-100 pool would be a poor base for
reranking. Many positive snippets never reach the candidate set, so a reranker
would be bounded before it can use semantic evidence.

### Dense Evaluation Profile

Dense retrieval is much stronger, with nDCG@10 of 0.3639, hit@10 of 0.5850,
and recall@100 of 0.7384. This indicates that harrier-oss-270m can bridge a
meaningful amount of French-to-English product semantics. It can connect
questions about an Android box, a Fitbit extension, blue-light protection, or
phone compatibility to English snippets that answer those questions.

The task remains difficult because product language is terse and specific.
Dense models must distinguish compatible from incompatible, material from
dimension, and evidence-bearing answers from vague product descriptions. Strong
performance likely reflects both multilingual alignment and product-domain
representation.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile reaches nDCG@10 of 0.1775, hit@10 of 0.3200,
and recall@100 of 0.6918. It improves substantially over BM25 recall, but it
does not approach the dense-only top-10 quality. The candidate lists contain
100 to 101 entries, and 49 rows use the rank-101 safeguard to force a relevant
candidate into the pool.

This pattern shows that hybrid search recovers part of the dense signal while
retaining useful lexical anchors, but lexical evidence can still dilute ranking
quality in a strongly cross-lingual task. For downstream reranking, the hybrid
pool is more usable than BM25 alone, but dense candidates are the cleaner
starting point for this split.

### Metric Interpretation for Model Researchers

`xpqa_eng_fra` is dense-favorable and cross-lingual. BM25 is limited by
language mismatch, dense retrieval is the leading candidate source, and
`reranking_hybrid` lands between them. Recall@100 is particularly important
because more than half the queries have multiple positives; a strong candidate
generator should retrieve at least one answerable snippet and preferably several
for robust reranking.

nDCG@10 measures whether answerable snippets are ranked early, while hit@10
measures whether any positive is available to a top-k consumer. Because
positives are short and domain-specific, improvements should be interpreted as
progress in multilingual product QA retrieval rather than broad passage
retrieval alone.

### Query and Relevance Type Tendencies

Queries are customer-style French product questions. They often ask about
warranty, volume, dimensions, compatibility, materials, accessories, setup, and
subjective advantages. Documents are short English snippets that may come from
product metadata, customer answers, or review-like evidence.

Relevance is answerability-based. A document is positive if it contains enough
information to answer the question, not merely because it mentions the same
product. Multiple snippets can be relevant for the same query when they provide
the same answer or complementary evidence.

### Representative Failure Modes

BM25 fails when translation is required or when the useful English answer uses
different vocabulary from the French question. Dense retrieval can fail by
matching the product category but missing the specific property being asked,
such as compatibility, material, or warranty. Hybrid retrieval can over-rank
snippets with shared numbers or product terms even when they do not answer the
question.

Another common failure mode is confusing vague product descriptions with direct
answers. For this task, relevance depends on whether the snippet resolves the
customer's question, not whether it describes the product generally.

### Training Data That May Help

Useful training data includes xPQA train examples, French-to-English product QA
retrieval pairs, bilingual e-commerce FAQ data, and hard negatives from the
same product category. Training should exclude xPQA test examples, Nano
queries, qrels, and positive product candidates.

Synthetic data should pair French product questions with English snippets
containing concrete evidence: warranty fields, dimensions, compatibility,
volume, accessory lists, material descriptions, and customer-use statements.
Multi-positive training is appropriate because several snippets can answer the
same question.

### Model Improvement Notes

Models should combine multilingual alignment with product-domain specificity.
Dense encoders need to preserve small but decisive details such as units,
negation, compatibility constraints, and material terms. Rerankers should be
trained to judge answerability directly, because topical similarity to the same
product is not enough.

## Example Data

| Query | Positive document |
| --- | --- |
| bonjour, quels sont les avantages de cette box android, comparée aux autres ? merci [83 chars] | i have had several different android boxes and find this one of the best // easy to set up and lots of memory storage. [118 chars] |
| sur quel produit fitbit avez vous essayé cette extension ? [58 chars] | this worked great as an extender for the fitbit charge. [55 chars] |
| bonjour, la vitre est-elle en verre ou en plastique? [52 chars] | the front transparent plastic is a good protect the pictures. [61 chars] |
| cet article est-il "compatible" avec un smartphone de 5.5 pouces ? [66 chars] | it is described as being appropriate for any handlebar and any device. [70 chars] |
| bonjour est ce anti lumière bleue? [34 chars] | Product description does not mention anti blue light features. [62 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| xPQA: Cross-Lingual Product Question Answering across 12 Languages | 2023 | Paper | [https://arxiv.org/abs/2305.09249](https://arxiv.org/abs/2305.09249) |
| MTEB: Massive Text Embedding Benchmark | 2023 | Paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |
| mteb/XPQARetrieval | 2025 | Dataset card | [https://huggingface.co/datasets/mteb/XPQARetrieval](https://huggingface.co/datasets/mteb/XPQARetrieval) |

### Representative Snippets

| Query | Positive document |
| --- | --- |
| bonjour, quels sont les avantages de cette box android, comparee aux autres ? merci | An English customer answer saying the Android box is easy to set up and has lots of memory storage. |
| sur quel produit fitbit avez vous essaye cette extension ? | An English snippet saying it worked as an extender for the Fitbit Charge. |
| bonjour, la vitre est-elle en verre ou en plastique ? | An English snippet saying the front transparent part is plastic. |
| cet article est-il compatible avec un smartphone de 5.5 pouces ? | An English snippet describing suitability for any handlebar and device. |
| bonjour est ce anti lumiere bleue ? | An English snippet saying the product description does not mention anti-blue-light features. |
