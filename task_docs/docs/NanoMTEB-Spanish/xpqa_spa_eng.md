# NanoMTEB-Spanish / xpqa_spa_eng

## Overview

`xpqa_spa_eng` is the reverse cross-lingual direction of xPQA for the Spanish NanoMTEB set. Queries are English product questions, while candidate documents are mostly Spanish product-answer snippets. The retriever must bridge an English user question to a Spanish answer candidate that contains enough product information to answer it. This tests cross-lingual e-commerce retrieval in the English-to-Spanish direction.

The Nano split contains 200 queries, 1,941 documents, and 469 positive relevance judgments. Queries average about 47 characters, while documents average about 68 characters. The average number of positives per query is 2.345, and 121 queries have multiple positives. Candidate documents are short, answer-like Spanish snippets, often starting with `Sí`, `No`, or `Un cliente ha dicho`.

## Details

### What the Original Data Measures

xPQA frames product QA as candidate ranking and answer generation. A relevant candidate should contain enough product information to answer the question. The dataset emphasizes that e-commerce QA requires domain-specific ranking because product snippets differ from encyclopedia passages: they contain model codes, units, compatibility statements, review-like claims, and terse yes/no answers.

In this split, the query and document languages differ. English product questions must be matched to Spanish snippets. Lexical retrieval can only exploit language-independent strings such as numbers, model names, product codes, or units.

### Observed Data Profile

The documents are compact Spanish answer snippets. Many contain direct polarity, such as `Sí`, followed by a short product claim. Others report what a customer said. Queries ask about restraints, face washing, UV protection, iPhone 7 Plus accessories, blade length, capacity, color codes, sowing season, and aquarium salt measurement.

The short document length makes ranking sensitive to small details. A snippet can be topically related to the same product but not answer the asked property. The model must preserve exact attribute matching across languages.

### BM25 Evaluation Profile

BM25 is weak, with nDCG@10 of 0.1227, hit@10 of 0.1850, and recall@100 of 0.2154. It succeeds mostly when the query and document share language-independent tokens such as `iPhone 7 Plus`, numbers, units, or color codes like `RAL 7048`.

This poor lexical performance is expected. English words such as `protect`, `UV rays`, or `wash my face` generally do not match Spanish snippets like `protege`, `rayos ultravioleta`, or `utilizables`. BM25 provides a low baseline for the true cross-lingual problem.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run is clearly strongest, with nDCG@10 of 0.4872, hit@10 of 0.7300, and recall@100 of 0.8593. Dense retrieval captures cross-lingual product-question semantics far better than lexical matching. It can connect English yes/no questions to Spanish answer snippets and recognize product attributes across languages.

The dense profile is much stronger than in `xpqa_eng_spa`, which may reflect shorter Spanish answer snippets with direct polarity and simpler answer phrasing. Still, errors remain because snippets are terse and product details are fine-grained.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reports nDCG@10 of 0.1444, hit@10 of 0.2200, and recall@100 of 0.7889. Candidate lists contain 100 to 101 items, and 35 rows use the positive safeguard. Hybrid recall is much better than BM25 but still below dense recall, and its top-10 ranking remains weak.

The result shows that lexical evidence is not a reliable final-ranking signal in this cross-lingual direction. Hybrid candidates may preserve additional positives through numeric or code overlap, but dense retrieval is the main useful retriever.

### Metric Interpretation for Model Researchers

This split is strongly dense-favorable. The gap between BM25 and dense retrieval measures the value of cross-lingual product representation. Hybrid retrieval improves recall over BM25 but does not improve top-rank ordering because lexical overlap is sparse and often incidental.

Multi-positive relevance means recall@100 is important. Several snippets can answer the same question, and dense retrieval is much more likely to preserve them. Rerankers should operate on semantically strong candidate pools rather than relying on lexical fusion.

### Query and Relevance Type Tendencies

Representative queries ask whether a mount holds at 0 and 90 degrees, what type of restraint is used, whether a product can be used to wash the face, whether it protects from UV rays, and when more iPhone 7 Plus inventory will arrive. Relevant Spanish snippets answer with short claims, customer reports, or yes/no statements.

The task often depends on polarity and product property. A model must identify whether the snippet directly answers the asked property, not merely whether it mentions the same product.

### Representative Failure Modes

BM25 fails whenever there are no shared cross-lingual tokens. Dense retrieval may retrieve a plausible Spanish product snippet from the same product area that does not answer the exact question. Hybrid retrieval may overvalue a shared model code or number even when the answer attribute is wrong.

Another failure mode is polarity confusion. A snippet saying `Sí` or `No` may be relevant only if it answers the same yes/no question. Polarity without the right attribute is not enough.

### Training Data That May Help

Useful training data includes xPQA train examples, English-to-Spanish product QA retrieval pairs, translated product QA pairs, and same-product hard negatives. Training should exclude xPQA test examples, Nano queries, qrels, and positive product snippets.

Hard negatives should share the same product or category but answer a different property. They should include conflicting yes/no polarity, wrong sizes, and adjacent compatibility claims.

### Model Improvement Notes

Dense models can improve with product-domain multilingual supervision, especially for yes/no polarity, units, model codes, and compatibility. Sparse retrieval is mostly useful for product identifiers. Hybrid retrieval can help preserve candidates but should be followed by a semantic reranker that compares the English question to the Spanish evidence.

For evaluation, this split is a strong test of cross-lingual answer-snippet retrieval, not general translation. The model must preserve fine product details across languages.

## Example Data

| Query | Positive document |
| --- | --- |
| do you have anything that holds at 0 and 90 degrees and doesn't turn on its own? [80 chars] | Sí. Un cliente ha dicho que soporta la televisión a 0 y 90 grados. [66 chars] |
| what type of restraint do you have? [35 chars] | Un cliente ha dicho que utilizó ganchos con tiras. [50 chars] |
| can it be used to wash my face? [31 chars] | Sí. Son utilizables para cualquier parte del cuerpo. [52 chars] |

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| xPQA paper | Cross-lingual product QA task and candidate-ranking formulation. |
| MTEB paper | Benchmark context. |
| MTEB task card | Retrieval packaging. |

### Representative Snippets

- An English query asks whether a mount holds at 0 and 90 degrees; the relevant Spanish snippet says a customer reported it supports the TV at those angles.
- A query asks what type of restraint is used; the relevant snippet says a customer used hooks with straps.
- A query asks whether it can be used to wash the face; the relevant snippet says it can be used on any part of the body.
- A query asks whether it protects from UV rays; the relevant snippet says it protects children from ultraviolet light and sunburn.
- A query asks about more iPhone 7 Plus stock; the relevant snippet discusses the screen protector for iPhone 7 Plus.
