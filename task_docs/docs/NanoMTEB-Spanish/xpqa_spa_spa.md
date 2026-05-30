# NanoMTEB-Spanish / xpqa_spa_spa

## Overview

`xpqa_spa_spa` is the Spanish-to-Spanish xPQA retrieval split. Both queries and candidate documents are Spanish. The task models product question answering in an e-commerce setting: a user asks a short Spanish question about a product, and the retriever must find short Spanish answer snippets that address the requested detail. Unlike the cross-lingual xPQA directions, this split keeps language constant, so exact product vocabulary can help more.

The Nano split contains 200 queries, 1,941 documents, and 488 positive relevance judgments. Queries average about 45 characters, while documents average about 68 characters. The average positives per query is 2.44, and 127 queries have multiple positives. Many documents are direct answer snippets with yes/no polarity, quantities, materials, model codes, dimensions, and compatibility claims.

## Details

### What the Original Data Measures

xPQA collects product questions and candidate answer information from e-commerce data. The retrieval objective is to rank answer snippets that fully or partially answer the question. Even in the monolingual Spanish condition, this is not generic semantic search: relevance depends on product-specific facts, such as whether a pack has 12 units, whether a material is stainless steel, whether an item is real silver, or whether a product fits a specific use.

The task rewards models that preserve concrete purchase and usage details. A related product snippet is not enough unless it answers the exact question.

### Observed Data Profile

Queries are compact product questions, often asking yes/no or either/or details. Candidate documents are also short and answer-like. Many begin with `Sí`, `No`, or `Un cliente ha dicho`, followed by the relevant product fact. This makes polarity, attribute names, quantities, and product constraints central to retrieval.

Examples include questions about whether a pack of three straps contains different sizes, whether sizes run large or tight, whether a guitar model is acoustic or electro-acoustic, how to choose a size, and whether a pack includes 12 units.

### BM25 Evaluation Profile

BM25 is moderately strong, with nDCG@10 of 0.4829, hit@10 of 0.7000, and recall@100 of 0.7766. Because both query and answer are Spanish, lexical overlap on product terms, quantities, sizes, and materials helps substantially. This is much easier for BM25 than the cross-lingual XPQA directions.

BM25 still misses many positives. Answer snippets may use different wording from the question, or a customer answer may imply the property indirectly. Exact overlap can also retrieve wrong snippets from the same product category or same item.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run is strongest, with nDCG@10 of 0.5667, hit@10 of 0.7650, and recall@100 of 0.8975. Dense retrieval improves because it can match product-question intent to answer snippets even when the wording differs. It can connect a question about "tallas grandes o justas" to a snippet describing a tight, body-shaping fit.

The dense gain shows that monolingual product QA is still semantic. Product answers are short, informal, and often indirect. Dense retrieval is better at connecting the user's requested attribute to the answer evidence.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reports nDCG@10 of 0.5582, hit@10 of 0.7400, and recall@100 of 0.8832. Candidate lists contain 100 to 101 items, and 20 rows use the positive safeguard. Hybrid retrieval is close to dense but slightly lower across the reported metrics.

This suggests that lexical evidence is useful but dense retrieval already captures most of the relevant product-answer relation. Hybrid search may still be useful for a reranker because it preserves product codes and exact quantities, but dense is the best direct first-stage profile.

### Metric Interpretation for Model Researchers

This split is dense-favorable, with BM25 providing a much stronger baseline than in the cross-lingual directions. The gap between BM25 and dense reflects paraphrase and answer-style mismatch rather than translation. Hybrid retrieval is near dense but does not surpass it.

Because many queries have multiple positives, recall@100 remains important. A product question can be answered by several snippets, and systems should retrieve more than one valid answer when available. nDCG@10 measures whether the most useful snippets appear early.

### Query and Relevance Type Tendencies

Representative queries ask whether a pack contains three same-size straps, whether sizes are large or tight, whether a guitar model is electro-acoustic, how to choose a wrist size, and whether a pack contains 12 units. Relevant snippets answer with short factual claims, measurements, or customer advice.

The task is practical and detail-oriented. It rewards preserving quantities, polarity, model type, material, compatibility, and fit. Broad product similarity is not enough.

### Representative Failure Modes

BM25 may retrieve snippets sharing a product term but answering a different attribute. Dense retrieval may retrieve semantically plausible snippets from the same product category that are not specific enough. Hybrid retrieval can overvalue shared numbers or product identifiers when they do not answer the query.

Polarity confusion is a common risk. A snippet with `Sí` or `No` is only useful if it answers the exact property asked. A model also needs to distinguish between product title information and customer-experience evidence.

### Training Data That May Help

Useful training data includes Spanish xPQA train examples, Spanish e-commerce QA pairs, customer-question to answer-snippet retrieval pairs, and same-product or same-category hard negatives. Training should exclude xPQA test examples, Nano queries, qrels, and positive snippets.

Hard negatives should share the same product or category but answer another detail. Examples with wrong quantities, wrong fit, different material, or incompatible model variants are especially valuable.

### Model Improvement Notes

Dense models can improve through Spanish product-domain supervision and stronger modeling of polarity, quantities, units, and compatibility. Sparse systems can improve by preserving model codes and numeric tokens, but they need paraphrase robustness for answer snippets. Hybrid systems are useful for recall and reranking, though dense retrieval is the best direct profile here.

For evaluation, this split measures monolingual e-commerce answer retrieval. The strongest systems should rank short answer snippets by whether they answer the exact product question.

## Example Data

### Public Sources

- xPQA paper: https://arxiv.org/abs/2305.09249
- MTEB benchmark paper: https://arxiv.org/abs/2210.07316
- Source task dataset card: https://huggingface.co/datasets/mteb/XPQARetrieval

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| xPQA paper | Original product QA dataset and ranking objective. |
| MTEB paper | Benchmark context. |
| MTEB task card | Retrieval packaging. |

### Representative Snippets

- A query asks whether a pack of three straps contains one of each size or three of the same size; the relevant snippet says the package contains three 120 cm pieces.
- A query asks whether sizes are large or tight; the relevant snippet says they are tight-fitting and shape the body.
- A query asks whether a guitar is acoustic or electro-acoustic; the relevant snippet says it is an electro-acoustic guitar.
- A query asks how to know what size to order; the relevant snippet recommends measuring wrist diameter.
- A query asks whether a pack contains 12 units; the relevant snippet says yes, the package includes 12 units.
