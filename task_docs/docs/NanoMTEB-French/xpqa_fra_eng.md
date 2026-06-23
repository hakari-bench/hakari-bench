# NanoMTEB-French / xpqa_fra_eng

## Overview

`xpqa_fra_eng` is a cross-lingual xPQA product retrieval task in which English
product questions are matched to French answer snippets. The Nano split
contains 200 queries, 1,547 documents, and 437 positive qrels. More than half
of the queries have multiple positives, with an average of 2.185 positives per
query. Documents are short French snippets averaging 76.98 characters, often
containing yes/no polarity, dimensions, compatibility statements, model names,
or customer-reported facts. This makes the task a focused test of whether a
retrieval model can bridge English customer questions to concise French product
evidence.

## Details

### What the Original Data Measures

[xPQA: Cross-Lingual Product Question Answering across 12 Languages](https://arxiv.org/abs/2305.09249)
defines a product question-answering benchmark where retrieval models rank
candidate snippets that contain answer evidence. The dataset is designed around
e-commerce questions rather than general encyclopedic QA, so the relevant
signals include specifications, compatibility, dimensions, materials, and
customer usage reports.

This split reverses a common cross-lingual direction: the queries are English,
and the answer candidates are French. The model must therefore translate the
question intent into French product-answer language while preserving exact
constraints such as polarity and measurements.

### Observed Data Profile

The split has 200 English queries, 1,547 French documents, and 437 positive
judgments. Queries average 52.11 characters, and documents average 76.98
characters. Each query has between one and five positives, with a median of two;
107 queries, or 53.5%, have multiple positives.

Documents are short and answer-like. Many begin with "Oui", "Non", or a
customer-report formulation. Because snippets are compact, relevance often
turns on a single phrase: whether an item fits a device, whether a product makes
hair greasy, whether instructions are available, or what width a module has.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2918, hit@10 of 0.3800, and recall@100 of 0.3684.
This is low in absolute terms but stronger than the French-query to English
candidate direction in this Nano set. BM25 can benefit from shared product
names, model numbers, units, and technical terms that survive across languages.
However, the core answerability signal remains cross-lingual, so exact term
frequency is not enough for most queries.

The low recall@100 means a lexical candidate pool misses many relevant snippets.
For downstream reranking, BM25 alone is therefore a weak candidate generator
despite occasionally surfacing obvious product-code matches.

### Dense Evaluation Profile

Dense retrieval is clearly strongest, with nDCG@10 of 0.6479, hit@10 of
0.8100, and recall@100 of 0.8993. This suggests that harrier-oss-270m captures
the cross-lingual relationship between English product questions and French
answer snippets much better than lexical matching. It can align question
properties such as width, color, compatibility, instructions, and material with
short French evidence.

This task is a useful dense-model diagnostic because the documents are too
short to hide behind broad topical similarity. The model must preserve the
specific asked property and the answer polarity. Strong performance indicates
good multilingual product-domain alignment.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile reaches nDCG@10 of 0.3724, hit@10 of 0.5000,
and recall@100 of 0.8398. It improves substantially over BM25 and recovers most
of the dense recall, but it remains far below dense retrieval in top-10 ranking.
Candidate lists contain 100 to 101 rows, with 13 safeguard-positive rows.

This pattern shows that hybrid search is valuable for candidate coverage but
not sufficient for top-rank ordering in this direction. The lexical component
adds useful anchors, yet the strongest signal is semantic translation between
English questions and French product answers.

### Metric Interpretation for Model Researchers

`xpqa_fra_eng` is dense-favorable. BM25 is limited by cross-lingual mismatch,
the dense candidate column dominates both nDCG@10 and recall@100, and
`reranking_hybrid` sits between them. The most important metric is recall@100
for candidate generation, because multi-positive queries benefit from exposing
several answerable snippets to a reranker.

nDCG@10 remains important because many snippets are near misses: they mention
the same product type but answer a different property. A strong model must rank
evidence-bearing snippets above merely related product text.

### Query and Relevance Type Tendencies

Queries are English customer questions about practical product details. They
ask about dimensions, color, greasiness, instructions, compatibility, model fit,
and maintenance. Positive documents are French snippets that directly answer
the question, often with polarity or a customer statement.

Relevance is answerability-based and may be multi-positive. Several French
snippets can be relevant if they each answer the same English question. This
supports multi-positive training objectives and recall-oriented evaluation.

### Representative Failure Modes

BM25 fails when the English query and French answer share no product names or
technical tokens. Dense retrieval can fail by matching the right product
category but the wrong property, such as retrieving a compatibility answer for a
size question. Hybrid retrieval can over-rank candidates with shared numbers or
brand names even when they do not answer the query.

Polarity is another common issue. A snippet beginning with "Non" may be
semantically close to the query but opposite to the expected answer. Models need
to treat yes/no evidence as part of relevance, not as incidental text.

### Training Data That May Help

Useful training data includes xPQA train examples, English-to-French product QA
retrieval pairs, bilingual product descriptions and customer answers, and
same-product hard negatives. Training should exclude xPQA test examples, Nano
queries, qrels, and positive product snippets.

Synthetic data should generate English product questions and French answer
snippets with explicit polarity, compatibility claims, measurements, model
names, and customer-reported facts. Hard negatives should share the product or
category but answer a different property.

### Model Improvement Notes

Models should combine cross-lingual alignment with fine-grained product
semantics. Dense encoders need to preserve measurements, negation, and
compatibility constraints. Rerankers should compare the asked property against
the snippet's actual answer rather than relying on broad product similarity.

## Example Data

| Query | Positive document |
| --- | --- |
| what is the width of a module? [30 chars] | La largeur d'un module est de 4,21 inch. [40 chars] |
| for the color do you have white ones as in the photo? [53 chars] | Non. La couleur disponible est violet et gris. [46 chars] |
| hello, does this spray make hair greasy? thank you. [51 chars] | Oui. Un client dit que cela rend ses cheveux un peu huileux. [60 chars] |
| hello, no instructions without the box, does anyone know where we can find it? [78 chars] | Oui. Un client dit que vous pouvez télécharger le manuel et guide d'utilisation rapide sur la page Amazon. [106 chars] |
| is this razor compatible with protector 3 blades? thank you. [60 chars] | Non. Un client dit qu'il n'est pas possible d'ajouter les lames d'autres fabricants. [84 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| xPQA: Cross-Lingual Product Question Answering across 12 Languages | 2023 | Paper | [https://arxiv.org/abs/2305.09249](https://arxiv.org/abs/2305.09249) |
| MTEB: Massive Text Embedding Benchmark | 2023 | Paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |
| mteb/XPQARetrieval | 2025 | Dataset card | [https://huggingface.co/datasets/mteb/XPQARetrieval](https://huggingface.co/datasets/mteb/XPQARetrieval) |

### Representative Snippets

| Query | Positive document |
| --- | --- |
| what is the width of a module? | La largeur d'un module est de 4,21 inch. |
| for the color do you have white ones as in the photo? | Non. La couleur disponible est violet et gris. |
| hello, does this spray make hair greasy? thank you. | Oui. Un client dit que cela rend ses cheveux un peu huileux. |
| hello, no instructions without the box, does anyone know where we can find it? | A French customer statement saying the manual and quick-use guide can be downloaded from Amazon. |
| is this razor compatible with protector 3 blades? thank you. | A French snippet saying blades from other manufacturers cannot be added. |
