# NanoCMTEB / ecom

## Overview

NanoCMTEB `ecom` is a Chinese and mixed-script e-commerce product retrieval task. Queries are very short marketplace search strings, and documents are compact product-title-like descriptions. The task measures whether retrieval systems can match exact product intent, including brand names, product categories, aliases, variants, and model numbers.

## Details

### What the Original Data Measures

The task belongs to the Multi-CPR and C-MTEB Chinese retrieval families. Multi-CPR includes e-commerce search as a real product-search domain collected from search systems and annotated for relevance. The source task is short-query product retrieval rather than explanatory passage retrieval.

The query may be only a few characters and may contain Chinese, Japanese, English, brand names, numbers, or transliterations. The relevant document is usually a product title containing the matching product and variant. Relevance depends on exact shopping intent, not broad topical similarity.

### Observed Data Profile

The task contains 200 queries, 10,000 documents, and 200 relevance judgments. It is strictly single-positive in the Nano labels: every query has exactly 1 positive, with 0 multi-positive queries.

Queries average 6.89 characters, and documents average 33.09 characters. This is one of the shortest-text NanoCMTEB tasks. Documents are compact product titles with brands, attributes, package sizes, model names, and promotional wording.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.5913, hit@10 of 0.7550, and recall@100 of 0.8250 using the top-500 BM25 candidate subset. This is a strong lexical baseline because product search often depends on exact terms, aliases, and model strings.

BM25's limitation is that product titles contain variant expansions, mixed scripts, synonyms, and brand or model formatting differences. A query may omit key title words, use an alias, or include a compact model shorthand. Exact term frequency is useful but not sufficient.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.8052, hit@10 of 0.9100, and recall@100 of 0.9550. Dense retrieval is the strongest top-ranking profile by a large margin. It substantially improves over BM25 in nDCG@10 and hit@10.

This indicates that embedding similarity helps with product aliases, variant expansion, and mixed-script matching. Dense retrieval can connect a short query such as a brand or model shorthand to a longer product title that contains the same product intent in expanded form.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.7025, hit@10 of 0.8350, and recall@100 of 0.9600. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 8 safeguard rows, candidate counts from 100 to 101, and a mean of 100.04 candidates.

Hybrid retrieval has the best recall@100 but trails dense retrieval for top-10 ranking. This means sparse terms add a little candidate coverage for exact product strings, while dense retrieval orders the best matches more effectively.

### Metric Interpretation for Model Researchers

This task is dense-favorable despite its short, identifier-heavy text. BM25 is strong because exact product terms matter, but dense retrieval is better at ranking the intended product title near the top. Reranking_hybrid is useful for candidate coverage, especially when exact aliases or rare model strings are present.

Because each query has one positive, hit@10 and nDCG@10 are closely tied to whether the system finds the intended product, not a family of acceptable alternatives. Small mistakes in model number, variant, size, or brand should be treated as serious retrieval errors.

### Query and Relevance Type Tendencies

Queries include short product requests such as sausage seasoning, nasal irrigator supplies, hair treatment masks, children's pajamas, camera models, household goods, beverages, appliances, and mixed-script branded products. Positive documents are marketplace-style product titles.

The relevance relation is exact product-intent matching. Same-category products are often hard negatives when they differ by variant, model, brand, quantity, or intended use.

### Representative Failure Modes

Likely failures include matching the right category but wrong brand, missing a model alias, confusing Japanese or English brand tokens, over-ranking a related variant, and treating promotional attributes as central relevance signals.

BM25 is vulnerable to formatting and alias mismatch. Dense retrieval can over-generalize within a product category. Hybrid retrieval improves recall but may still need product-aware reranking to resolve variants.

### Training Data That May Help

Useful training data includes product search query-title pairs, marketplace click logs, brand and model alias pairs, Chinese-Japanese product search data, and same-category product hard negatives.

Synthetic data should generate compact marketplace product titles with brands, models, attributes, sizes, and promotion terms, then create short search queries with aliases and variants. Hard negatives should preserve high lexical overlap while differing by product variant or family.

### Model Improvement Notes

Strong systems should handle short queries, mixed scripts, aliases, and exact variant constraints. Dense retrieval is the strongest observed first-stage method, but sparse matching remains important for rare model numbers and brand strings.

The task is a useful benchmark for product-search retrieval where semantic similarity must be balanced against exact catalog intent.

## Example Data

| Query | Positive document |
| --- | --- |
| 奥尔良味香肠调理 [8 chars] | 畅之味香肠调料五组合香肠调料台湾风味黑胡椒香辣蒜香新奥尔良 [29 chars] |
| 吉莫特洗鼻器 [6 chars] | 新品吉莫特洗鼻专用洗鼻盐 医生推荐儿童成人洗鼻瑜伽洗鼻盐60包 [31 chars] |
| 约肤深层滋润免蒸发膜 [10 chars] | 约肤免蒸发膜修护干枯倒膜改善毛躁头发护理水疗顺滑护发素女柔顺 [30 chars] |
| 童装韩版睡衣 [6 chars] | 女童睡衣法兰绒秋冬季儿童珊瑚绒加厚保暖女孩家居服中大童装套装 [30 chars] |
| 尼康z62 [5 chars] | Nikon/尼康z6ii z7ii二代z6z7全画幅微单机身Z62Z72 2代24-70套机 [46 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Task paper | [Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval](https://arxiv.org/abs/2203.03367) |
| Benchmark paper | [C-Pack: Packed Resources For General Chinese Embeddings](https://arxiv.org/abs/2309.07597) |
| Source dataset | [mteb/EcomRetrieval](https://huggingface.co/datasets/mteb/EcomRetrieval) |
| NanoCMTEB dataset | [hakari-bench/NanoCMTEB](https://huggingface.co/datasets/hakari-bench/NanoCMTEB) |

Representative query and positive source snippets:

| Query | Positive document snippet |
| --- | --- |
| 奥尔良味香肠调理 | A product title for multi-flavor sausage seasoning including New Orleans flavor. |
| 吉莫特洗鼻器 | A product title for nasal washing salt compatible with a nasal irrigation product. |
| 约肤深层滋润免蒸发膜 | A product title for a hair repair and moisturizing treatment mask. |
| 童装韩版睡衣 | A product title for children's Korean-style warm pajamas. |
| 尼康z62 | A product title for Nikon Z6II or related camera body and kit variants. |
