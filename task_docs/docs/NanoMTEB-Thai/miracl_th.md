# NanoMTEB-Thai / miracl_th

## Overview

`NanoMTEB-Thai / miracl_th` is the Thai split of MIRACL-style hard-negative passage retrieval. It asks Thai questions against a Thai Wikipedia-derived candidate pool, so the central problem is not cross-lingual matching but ranking the right evidence passage among many closely related Thai passages. The original MIRACL benchmark was designed as a multilingual information retrieval benchmark with native-speaker judgments over Wikipedia passages; this Nano task keeps that passage-level search setting while reducing the corpus to 10,000 documents and 200 queries. The split is useful for studying Thai tokenization, named-entity matching, factual question answering, and the difference between sparse lexical retrieval and semantic dense retrieval on a non-Latin script.

## Details

### What the Original Data Measures

MIRACL measures multilingual ad hoc retrieval over Wikipedia passages. In this Thai task, each query is written in Thai and the relevant documents are Thai passages that can answer or support the query. The task inherits MIRACL's emphasis on passage-level evidence rather than page-level topicality: a model should prefer the passage that contains the answer-bearing context, not merely a page about a related entity.

The hard-negative version used by MTEB makes the task more diagnostic by including candidates surfaced by retrieval systems. That means many negatives are topically plausible and may share names, dates, or surrounding concepts with the positive passage.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 343 positive qrel rows. Each query has 1.715 positives on average, with a median of 1 and a maximum of 7. There are 86 multi-positive queries, or 43.0% of the query set. Queries average 43.59 characters, while documents average 471.83 characters.

The examples cover definitions, national symbols, nutrition facts, Thai historical sites, and public works. Many positive passages begin with an entity title and then provide compact factual context. This shape favors models that can connect a concise Thai question to an answer-bearing passage while resisting nearby entity confusions.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.5999, hit@10 of 0.8800, and recall@100 of 0.9621. This is a strong sparse baseline for a hard-negative passage task. Thai entity names, dates, and key nouns often appear in both the query and the relevant passage, so exact or near-exact term evidence remains highly informative.

BM25 is therefore most competitive on queries that quote the target entity or contain distinctive factual words. Its weaknesses are the usual sparse-retrieval weaknesses: it can over-rank passages that share an entity family, title fragment, or topical vocabulary but do not contain the answer-bearing statement. For Thai retrieval research, this task is a useful reminder that a strong tokenizer and robust lexical matching are still major components of factual search quality.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.8076, hit@10 of 0.9500, and recall@100 of 0.9563. Dense retrieval is clearly stronger in the top ranks, even though its recall@100 is slightly below BM25. This indicates that semantic similarity is especially helpful once plausible candidates are available: the dense model more often places the answer-bearing passage near the top of the list.

This profile is consistent with queries whose wording is not a simple title lookup, or where answer context matters more than surface overlap alone. For model researchers, the task rewards Thai sentence and passage representations that preserve factual relations, temporal cues, and named-entity context.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with one query carrying a rank-101 safeguard positive. It reaches nDCG@10 of 0.7250, hit@10 of 0.9350, and recall@100 of 0.9971. The hybrid result has the best recall profile, recovering almost all judged positives within the reranking window, while dense retrieval remains stronger at nDCG@10.

This split therefore separates candidate coverage from final rank quality. A reranker trained on this task should benefit from the hybrid pool because it contains the complementary strengths of sparse term matching and dense semantic matching. However, the high recall also means that final effectiveness depends heavily on the reranker's ability to distinguish precise evidence passages from related Thai negatives.

### Metric Interpretation for Model Researchers

BM25 is already a high bar in recall and hit rate, so improvements that only recover more candidates may be less visible unless they also improve top-rank ordering. Dense retrieval's advantage in nDCG@10 suggests that semantic Thai passage representations are central to this split. The hybrid pool shows that a combined retrieval stack can expose nearly all positives to a reranker, making cross-encoder or late-interaction evaluation especially meaningful.

Because 43.0% of queries have multiple positives, nDCG should be read as ranking quality over a small set of acceptable evidence passages, not as a single-answer exact-match score.

### Query and Relevance Type Tendencies

Queries are short Thai factual questions. They often ask "what is", "when was", or "how much" style questions, and many contain a named entity. Relevant documents are medium-length Thai passages, usually with enough context to answer the question directly.

The relevance relation is evidence-oriented: a document is useful if it contains the needed factual statement or explanation. Pure topical relatedness is not enough.

### Representative Failure Modes

Common failures include ranking a passage about a neighboring entity, retrieving a broader article section that lacks the answer, confusing similar Thai historical or administrative names, and favoring passages with repeated query terms over passages that state the answer more directly. Dense systems may also miss exact date or number constraints when the semantic topic is otherwise correct.

### Training Data That May Help

Useful training data includes Thai MIRACL training examples, Thai Wikipedia question-passage pairs, Thai open-domain QA retrieval data, and hard negatives from the same article, entity family, or time period. Training examples should preserve Thai script, punctuation, date variants, and title-like entity mentions.

### Model Improvement Notes

The most promising improvements are Thai-aware tokenization for sparse systems, stronger Thai entity representations for dense systems, and rerankers trained to identify answer-bearing passages rather than merely topic-matching passages. Hybrid retrieval should be evaluated with both recall@100 and nDCG@10, because the best candidate pool is not necessarily the best first-stage ranker.

## Example Data

### Public Sources

- [Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages](https://arxiv.org/abs/2210.09984), 2022.
- [MIRACL project page](http://miracl.ai/).
- [mteb/MIRACLRetrievalHardNegatives](https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives), source task dataset card.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2022 | paper | https://arxiv.org/abs/2210.09984 |
| MIRACL project page |  | project page | http://miracl.ai/ |
| mteb/MIRACLRetrievalHardNegatives |  | dataset card | https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| ชาวนอร์มันหมายถึงอะไร? | A Thai passage defining the Normans as the people associated with Normandy in northern France, descended from Vikings and earlier Frankish and Gallo-Roman settlers. |
| สัตว์ประจำชาติสหรัฐอเมริกาคืออะไร? | A Thai passage about the United States and its ecology, including national wildlife context. |
| สไปรูไลนามีโปรตีนอยู่ราวเท่าไหร่? | A Thai passage explaining that spirulina contains roughly 60% protein and discussing its amino-acid composition. |
| พระราชวังบวรสถานมงคล ถูกสร้างขึ้นเมื่อไหร่? | A Thai historical passage about Phra Ratchawang Bowon Sathan Mongkhon and its royal context in Bangkok. |
| คลองรังสิต สร้างขึ้นเมื่อใด ? | A Thai passage about the Rangsit canal project, including the construction period and its role in Thai irrigation development. |
