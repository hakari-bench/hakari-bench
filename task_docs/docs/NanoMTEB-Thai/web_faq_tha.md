# NanoMTEB-Thai / web_faq_tha

## Overview

`NanoMTEB-Thai / web_faq_tha` is a Thai WebFAQ retrieval task. Natural Thai FAQ-style questions must retrieve their corresponding Thai answer passages from a broad web FAQ collection. The original WebFAQ work collects multilingual question-answer pairs from FAQ pages, so this benchmark differs from encyclopedic retrieval: the documents are practical answers about services, products, travel, payments, hotels, promotions, delivery, and support topics. The Nano split contains one relevant answer for each query, making it a direct test of whether a model can match a short user question to the right service-oriented answer in Thai web text.

## Details

### What the Original Data Measures

WebFAQ measures dense retrieval over naturally occurring FAQ question-answer pairs mined from multilingual web pages. The retrieval problem is practical and user-facing: a question should retrieve the answer that a site, product, or service provides. It is less formal than Wikipedia retrieval and often includes brand names, mixed scripts, commercial phrasing, and short direct answers.

For this Thai split, both questions and answers are Thai or Thai-heavy, though some examples contain Latin-script product, hotel, or brand names. This makes the task relevant to real Thai FAQ search and customer-support retrieval.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Each query has exactly one positive answer. Queries average 43.88 characters, while documents average 224.32 characters.

The examples include airport transfer questions, delivery-time questions, location or tracking queries, game-related product FAQs, and hotel amenity questions. Documents are generally shorter than Wikipedia passages and often answer the question directly. Some answers are promotional or operational rather than neutral explanatory prose.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.7607, hit@10 of 0.8500, and recall@100 of 0.9350. This strong result reflects the FAQ setting: questions and answers often repeat service terms, brand names, product names, or operational phrases such as delivery, pool, airport, tracking, or payment.

BM25 is likely to work best when the query contains a distinctive name or short phrase that also appears in the answer. Its main weakness is paraphrase and template confusion. Many FAQ answers from similar service categories can share the same vocabulary, so lexical overlap alone may rank another answer from the same topic above the intended one.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.7822, hit@10 of 0.8650, and recall@100 of 0.9350. Dense retrieval is slightly stronger than BM25 at the top of the ranking while matching BM25 recall@100.

This profile indicates that embedding similarity helps with paraphrased FAQ intent, especially when the answer uses different words from the question. The gain is moderate rather than dramatic because many examples still contain lexical anchors. For model researchers, the split is a good test of whether dense representations improve Thai service-question matching without losing the exact-name behavior that sparse retrieval handles well.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with three queries carrying a rank-101 safeguard positive. It reaches nDCG@10 of 0.7866, hit@10 of 0.8800, and recall@100 of 0.9850. This is the strongest profile across the three candidate types, with the hybrid pool improving both top-rank quality and coverage.

The result suggests that FAQ retrieval benefits from both lexical and semantic evidence. Sparse retrieval captures repeated names and service terms; dense retrieval captures user intent and paraphrase. The hybrid pool is therefore a strong basis for reranking models that must decide among several similar FAQ answers.

### Metric Interpretation for Model Researchers

This task has a clean one-query, one-answer structure, so nDCG@10 and hit@10 are easy to interpret: either the intended answer is near the top, or the system retrieved a different FAQ answer. Recall@100 is also important for reranking, and the hybrid candidate set is close to complete coverage.

Because BM25 and dense retrieval are both strong, improvements should be evaluated against hybrid baselines rather than against BM25 alone. A model that improves paraphrase handling but loses exact brand matching may not improve the overall task.

### Query and Relevance Type Tendencies

Queries are natural Thai support or FAQ questions. Relevant documents are short Thai answer passages, often with concrete operational details: delivery time, location information, amenities, product mechanics, or travel options.

The relevance relation is answer matching. A document is relevant if it is the answer paired with the question, not merely another answer from the same business domain.

### Representative Failure Modes

Common failures include retrieving an answer from the same site category, confusing similar hotel or product names, over-ranking promotional pages with repeated terms, and missing paraphrased policy questions. Mixed Thai and Latin script can also create issues when a model mishandles brand names or transliterations.

### Training Data That May Help

Useful training data includes Thai FAQ retrieval, multilingual WebFAQ examples, customer-support QA, e-commerce FAQ pairs, hotel and travel FAQ pairs, and service-policy question-answer pairs. Hard negatives should come from the same site, product family, or support category.

### Model Improvement Notes

The task rewards balanced retrieval. Sparse term matching should be preserved for names, numbers, and product labels, while dense representations should improve paraphrase and intent matching. Rerankers should be trained on short FAQ answers and same-category negatives, because many wrong answers will look superficially useful.

## Example Data

### Public Sources

- [WebFAQ: A Multilingual Collection of Natural Q&A Datasets for Dense Retrieval](https://arxiv.org/abs/2502.20936), 2025.
- [PaDaS-Lab/webfaq](https://huggingface.co/datasets/PaDaS-Lab/webfaq), source dataset card.
- [mteb/WebFAQRetrieval](https://huggingface.co/datasets/mteb/WebFAQRetrieval), MTEB dataset card.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| WebFAQ: A Multilingual Collection of Natural Q&A Datasets for Dense Retrieval | 2025 | paper | https://arxiv.org/abs/2502.20936 |
| PaDaS-Lab/webfaq |  | dataset card | https://huggingface.co/datasets/PaDaS-Lab/webfaq |
| mteb/WebFAQRetrieval |  | dataset card | https://huggingface.co/datasets/mteb/WebFAQRetrieval |

### Representative Snippets

| Query | Relevant answer excerpt |
| --- | --- |
| จากสนามบินเข้าตัวเมืองอย่างไร? | A Thai answer describing the LAX FlyAway bus as a convenient way to travel from Los Angeles airport to Union Station or Hollywood. |
| ใช้เวลาในการจัดส่งนานเท่าใด? | A short Thai answer stating that current delivery usually takes 1-3 days. |
| ได้รับความนิยม แถวนี้ tracking วัฒนา กรุงเทพมหานคร | A Thai location-style answer pointing to tracking information in Watthana, Bangkok. |
| Dolphins Pearl มีเพย์ไลน์กี่เพย์ไลน์? | A short answer stating that Dolphins Pearl has 10 paylines. |
| Au Grand Hôtel de Sarlat มีสระว่ายน้ำให้บริการไหม | A Thai answer confirming an outdoor pool and children's pool, with access hours. |
