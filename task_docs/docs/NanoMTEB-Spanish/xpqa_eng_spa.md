# NanoMTEB-Spanish / xpqa_eng_spa

## Overview

`xpqa_eng_spa` is a cross-lingual product question answering retrieval task from xPQA. The query side is Spanish product questions, while the candidate documents are mostly English product-answer snippets. The task models a common e-commerce problem: a user asks a practical product question in Spanish, and the retriever must find short English text that contains enough information to answer it.

The Nano split contains 200 queries, 1,936 documents, and 491 positive relevance judgments. Queries average about 45 characters, while documents average about 123 characters. The average number of positives per query is 2.455, and 127 queries have multiple positives. This means several snippets can answer the same product question, often because multiple product details or customer answers contain the needed information.

## Details

### What the Original Data Measures

xPQA was introduced for cross-lingual product question answering across 12 languages. The ranking task selects candidate product information that fully or partially answers a question. The paper emphasizes that product-domain ranking is different from Wikipedia-style QA because answers depend on specifications, compatibility, quantities, sizes, instructions, customer claims, and product variants.

In this split, the retrieval challenge is Spanish-to-English. A Spanish question must match an English candidate snippet. Relevance depends on answer usefulness, not only topical product similarity.

### Observed Data Profile

Queries are short Spanish product questions. Documents are compact English snippets, often product titles, customer-answer fragments, specifications, or structured attributes. Some candidates may contain language-independent clues such as numbers, model codes, sizes, or product names. Others require cross-lingual semantic matching.

Examples include questions about whether a pack contains one of each size or three of the same size, whether clothing sizes run large or tight, whether a guitar is acoustic or electro-acoustic, how to choose a wrist size, and whether a pack includes 12 units.

### BM25 Evaluation Profile

BM25 is weak, with nDCG@10 of 0.0986, hit@10 of 0.1950, and recall@100 of 0.2546. This is expected in the Spanish-to-English direction. Most useful answer snippets do not share Spanish query words. BM25 succeeds mainly when language-independent tokens overlap, such as numbers, units, model names, or product codes.

The poor lexical profile is useful diagnostically. It shows that this split cannot be solved by term frequency unless the query and answer happen to share product identifiers. Cross-lingual semantic matching is required.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run is clearly strongest, with nDCG@10 of 0.3104, hit@10 of 0.5450, and recall@100 of 0.7780. Dense retrieval bridges Spanish questions and English snippets much better than BM25. It can connect Spanish terms like `tamaño`, `modelo`, or `unidades` to English evidence about size, model type, or unit count.

The absolute scores remain moderate because the documents are short and product-specific. A snippet may be a terse title or attribute field with little context. The model must use cross-lingual product semantics and sometimes infer answer polarity from compact evidence.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reports nDCG@10 of 0.1428, hit@10 of 0.2550, and recall@100 of 0.6701. Candidate lists contain 100 to 101 items, and 49 rows use the positive safeguard. Hybrid retrieval improves over BM25 in recall, but it remains far below dense retrieval in top-10 ranking and recall.

The reason is that lexical evidence is mostly unavailable across languages. Adding BM25 candidates can recover some product-code or numeric matches, but it can also introduce distractors. Dense retrieval is the primary first-stage signal for this direction.

### Metric Interpretation for Model Researchers

This split is strongly dense-favorable. BM25 measures only incidental lexical overlap across languages, while dense retrieval measures actual cross-lingual product-question matching. Hybrid retrieval is not enough to overcome the lexical gap.

Because many queries have multiple positives, recall@100 matters for reranking. Dense retrieval's recall advantage means it is much more likely to preserve useful answer snippets for a downstream ranker or generator.

### Query and Relevance Type Tendencies

Representative questions ask whether a three-pack contains different sizes, whether clothing sizes are large or tight, whether a guitar model is acoustic or electro-acoustic, how to choose a size, or whether a pack includes 12 units. Relevant documents are short English snippets with product specifications or customer-reported evidence.

The model must identify concrete product attributes: quantity, size, material, model type, compatibility, or usage. These are small details, and a wrong snippet from the same product category may not answer the question.

### Representative Failure Modes

BM25 fails when Spanish and English have no shared words. Dense retrieval can fail by retrieving a product-related snippet that discusses the same item but not the requested attribute. Hybrid retrieval may add numeric or code-based distractors that share a surface token but do not answer the question.

Another failure mode is polarity loss. Questions often ask yes/no or either/or properties. A relevant snippet must answer the polarity correctly, not merely mention the same product.

### Training Data That May Help

Useful training data includes xPQA train examples, bilingual Spanish-to-English product QA pairs, e-commerce candidate ranking data, and hard negatives from the same product category. Training should exclude xPQA test examples, Nano queries, qrels, and positive product candidates.

Hard negatives should be close product snippets: same item but wrong attribute, same category but different model, or same quantity words with different package meaning. These are more useful than random negatives.

### Model Improvement Notes

Dense models can improve through cross-lingual product-domain supervision, especially for specifications, units, sizes, compatibility, and customer-answer phrasing. Sparse systems have limited value except for product codes and numeric attributes. Hybrid systems may help candidate recall but should not be treated as the final-ranking baseline without a strong reranker.

For evaluation, this split is a clear test of multilingual e-commerce retrieval. A strong model should bridge Spanish user questions to English answer evidence while preserving fine product details.

## Example Data

| Query | Positive document |
| --- | --- |
| el pack de 3 cintas, ¿es una de cada tamaño o las 3 del mismo tamaño? [69 chars] | gm climbing pack of 3 16mm nylon sling runner 120cm / 48inch (gray) [67 chars] |
| que son tallas grandes o justas? [32 chars] | The waist-tightening and slim-fitting design hides your proud flesh at your waist and instead forms a curve there. [114 chars] |
| és el modelo acústico o electro acústico? [41 chars] | martin drs2 dreadnought acoustic-electric guitar [48 chars] |
| como se que tamaño pedir,? [26 chars] | i encourage people to measure your wrist before purchasing; for reference my wrist is 5.5 inches around. [104 chars] |
| si compro un pack vendran 12 unidades? [38 chars] | "unit_count": [{"type": {"value": "count"}, "value": 12}] [57 chars] |

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| xPQA paper | Original cross-lingual product QA dataset and ranking task. |
| MTEB paper | Benchmark context. |
| MTEB task card | Retrieval packaging. |

### Representative Snippets

- A Spanish query asks whether a pack of three straps has one of each size; the relevant English snippet names a three-pack with a specific 120 cm size.
- A query asks whether sizes run large or tight; the relevant snippet describes a slim-fitting design.
- A query asks whether a guitar is acoustic or electro-acoustic; the relevant snippet identifies an acoustic-electric model.
- A query asks how to choose the size; the relevant snippet recommends measuring the wrist.
- A query asks whether a pack contains 12 units; the relevant snippet gives `unit_count` as 12.
