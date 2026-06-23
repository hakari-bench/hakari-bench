# NanoMTEB-German / xmarket_de

## Overview

`xmarket_de` is the German XMarket product retrieval task. Queries are very
short German category or shopping-intent labels, and documents are marketplace
product titles and descriptions. The Nano split contains 182 queries, 10,000
documents, and 4,124 positive qrels. It is strongly multi-positive: each query
has 22.66 positives on average, the median is 7.5, and 85.16% of queries have
more than one positive. Queries average only 14.57 characters, while documents
average 456.99 characters. This task is useful for evaluating product-category
retrieval, multilingual marketplace text, and multi-positive ranking behavior.

## Details

### What the Original Data Measures

[Cross-Market Product Recommendation](https://arxiv.org/abs/2109.05929)
introduced XMarket as a cross-market and cross-lingual e-commerce resource from
Amazon marketplaces. The source benchmark studies product recommendation and
market adaptation across local markets and languages. The MTEB-style retrieval
packaging turns product category or shopping-intent labels into queries and
product metadata into documents.

In the German split, relevance is category membership or shopping-intent match.
This differs from QA retrieval: there may be many relevant products for a
single query, and the query can be only one or two category words.

### Observed Data Profile

The split has 182 queries, 10,000 product documents, and 4,124 positive
judgments. Query text is extremely short. Documents are product titles or
descriptions with brand, material, dimensions, color, use case, and sometimes
mixed German-English marketplace language.

Examples include categories such as ink cartridges, hand tools, embroidery
thread, pottery, and boards. Positive documents can be short product names or
longer snippets containing brand and product attributes. The combination of
short queries and many positives makes this a ranking-and-coverage task rather
than a single-document evidence task.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2012, hit@10 of 0.4780, and recall@100 of 0.1360.
Despite many positives per query, lexical retrieval finds a top-10 positive for
less than half of the queries and covers only a small fraction of relevant
products by rank 100. Exact category words often do not appear in product
titles, and product descriptions may use brand names, materials, or English
phrasing instead of the German category label.

BM25 is useful when the query term is a direct product word, but weak when the
category relation is implicit. This is common in e-commerce, where a product can
belong to a category without repeating the category name.

### Dense Evaluation Profile

Dense retrieval is the strongest candidate profile, with nDCG@10 of 0.2268,
hit@10 of 0.5659, and recall@100 of 0.2209. The improvement over BM25 shows
that embedding similarity captures some category-product semantics and some
German-English product-language variation. It can retrieve products that satisfy
a category even when the exact label is absent.

The absolute scores are still modest. The query is often too short to specify
fine-grained intent, and many product categories have broad, noisy candidate
sets. Strong models need e-commerce category knowledge, multilingual product
normalization, and robustness to mixed-language titles.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile reaches nDCG@10 of 0.2210, hit@10 of 0.5385,
and recall@100 of 0.2097. It is close to dense retrieval but slightly lower in
all three metrics. Candidate lists contain 100 to 101 rows, with 48
safeguard-positive rows.

This suggests that hybrid search helps recover some positives that lexical
matching alone misses, but dense product-category semantics remain the stronger
signal. The hybrid pool may still be useful for reranking because it mixes exact
product terms with semantic category matches, but it does not surpass dense
retrieval on this Nano split.

### Metric Interpretation for Model Researchers

`xmarket_de` is dense-favorable, but all candidate profiles have low
recall@100 relative to the number of positives. This is expected for
multi-positive e-commerce retrieval with broad categories and short queries.
Hit@10 measures whether at least one relevant product appears early, while
recall@100 measures how much of the relevant product set is exposed.

nDCG@10 should be interpreted as early ranking quality under many possible
positives. It does not require recovering all relevant products, but a model
with better category coverage should improve both hit@10 and recall@100.

### Query and Relevance Type Tendencies

Queries are short German product categories or shopping-intent labels. Positive
documents are products that belong to the category or satisfy the intent.
Documents may be German, English, or mixed-language marketplace text, and may
include brand-heavy titles with sparse descriptive information.

Relevance is many-to-many. A category can have dozens of relevant products, and
a product description may be relevant without repeating the category label.
This supports multi-positive objectives and category-aware hard negatives.

### Representative Failure Modes

BM25 fails when products omit the category word, use English names, or describe
the category through material and use case. Dense retrieval can over-generalize
nearby categories, such as craft tools, art supplies, or office materials.
Hybrid retrieval can inherit lexical noise from brand names and product
variants while not fully resolving category hierarchy.

Another failure mode is marketplace noise: product snippets can contain
irrelevant marketing text, multilingual fragments, or accessory terms that make
category matching ambiguous.

### Training Data That May Help

Useful training data includes non-overlapping XMarket product metadata,
multilingual e-commerce category-product pairs, German query-to-product click
or purchase pairs, and hard negatives from neighboring product categories.
Training should exclude XMarket German evaluation products, qrels, and
category-product pairs likely to overlap with the Nano split.

Synthetic data should generate marketplace product titles and descriptions with
brand, material, dimensions, color, and use case, then pair them with short
German category labels or shopping-intent queries. Multi-positive training is
essential because each category can map to many products.

### Model Improvement Notes

Models should learn category-product relations rather than only keyword
overlap. Dense encoders need multilingual product-title robustness and
category-hierarchy awareness. Rerankers should use product attributes, not only
brand names, to determine whether an item satisfies the query.

## Example Data

| Query | Positive document |
| --- | --- |
| Minen, Patronen & Tintenlöscher [31 chars] | Noodler's Tinte - 90 ml - Schwarz [33 chars] |
| Handwerkzeuge [13 chars] | AFA Tooling - (4 Pcs) Radio Removal Tool, OEM: 1C0-051-530 - Wird nicht brechen oder biegen [91 chars] |
| Stick- & Nähgarn [16 chars] | Clover Stickwerkzeug clover needlecraft this old art of embroidery using a fine hook on a fine cloth tightly stretched in a frame called tambour is reborn with kantan couture bead embroidery tool. bas... [200 / 321 chars] |
| Töpferei [8 chars] | Makin's Clay Tonpistole, Mehrfarbig [35 chars] |
| Tafeln [6 chars] | Sculpey S2 Original-Polymer Clay 1,75 Pounds/Pkg [48 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Cross-Market Product Recommendation | 2021 | Paper | [https://arxiv.org/abs/2109.05929](https://arxiv.org/abs/2109.05929) |
| XMRec project page | 2021 | Project page | [https://xmrec.github.io/](https://xmrec.github.io/) |
| mteb/XMarket | 2025 | Dataset card | [https://huggingface.co/datasets/mteb/XMarket](https://huggingface.co/datasets/mteb/XMarket) |

### Representative Snippets

| Query | Positive document |
| --- | --- |
| Minen, Patronen & Tintenloscher | Noodler's Tinte - 90 ml - Schwarz. |
| Handwerkzeuge | A radio-removal tool product title with OEM part information. |
| Stick- & Nahgarn | A Clover embroidery-tool snippet describing tambour and bead embroidery. |
| Topferei | Makin's Clay Tonpistole, Mehrfarbig. |
| Tafeln | Sculpey Original polymer clay package. |
