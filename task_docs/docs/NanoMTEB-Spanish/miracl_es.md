# NanoMTEB-Spanish / miracl_es

## Overview

`miracl_es` is the Spanish NanoMTEB split of MIRACL, a multilingual ad hoc retrieval benchmark over Wikipedia. MIRACL was built for monolingual retrieval across many languages, including Spanish, with native-language queries and passage-level relevance judgments. In this task, Spanish information needs retrieve Spanish Wikipedia passages. Unlike single-answer QA retrieval, many queries have several relevant passages.

The Nano split contains 200 queries, 10,000 documents, and 934 positive relevance judgments. Queries average about 48 characters, while documents average about 555 characters. The average number of positives per query is 4.67, the median is 4, and 86.0% of queries have multiple positives. This makes the split a multi-positive passage retrieval task where systems should retrieve several answer-bearing or relevant passages, not just the first matching passage.

## Details

### What the Original Data Measures

MIRACL measures multilingual ad hoc retrieval over Wikipedia. Queries are written in the target language, and documents are passages from that language's Wikipedia. Relevance judgments are passage-level and can include multiple positives per query. The Spanish split therefore tests native Spanish search over Spanish encyclopedia text.

The MTEB hard-negative packaging builds candidate pools from BM25 and dense retrievers, but the underlying retrieval objective remains the same: rank relevant Spanish passages for Spanish queries. A relevant passage should contain evidence or information that satisfies the information need.

### Observed Data Profile

The documents are Wikipedia-style passages, often beginning with a title or entity name. The query set covers architecture, religious terms, criminal history, political systems, Roman military institutions, sports, Paraguayan music, ancient Greek philosophy, agriculture, and PlayStation. Many positives may come from the same article or related articles.

The multi-positive structure changes evaluation. A system that finds one relevant passage quickly can have high hit@10, but nDCG@10 rewards ranking several relevant passages well. Recall@100 matters because rerankers need enough positives in the candidate set.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.5620, hit@10 of 0.9400, and recall@100 of 0.9743. This is a strong lexical profile. Spanish Wikipedia queries often share key entity names, terms, or definitions with relevant passages. BM25 is especially good at ensuring that at least one relevant passage appears in the top 10 and that most positives survive into the top 100.

The limitation is ordering all relevant passages. BM25 can retrieve the obvious title or entity match but may not rank multiple supporting passages in ideal order. It can also over-rank passages that share a key term but do not answer the query as directly.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run has the best nDCG@10, with 0.7481, while hit@10 is 0.9250 and recall@100 is 0.9122. Dense retrieval is better at top-rank relevance quality: it places highly relevant Spanish passages earlier, even when wording differs from the query.

The tradeoff is lower recall@100 than BM25. Dense retrieval may focus strongly on the most semantically aligned passages but miss some additional positives that share lexical evidence. For direct search results, dense retrieval is the strongest ranking signal; for broad candidate coverage, it is not the strongest source alone.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reports nDCG@10 of 0.7042, hit@10 of 0.9900, and recall@100 of 0.9989. Candidate lists contain exactly 100 items with no safeguard rows. Hybrid retrieval combines BM25's broad lexical coverage with dense semantic ranking, yielding nearly complete top-100 relevant coverage and the best hit@10.

Hybrid does not exceed dense nDCG@10, so its top ordering is not the best. But it is the best candidate-generation profile. For reranking pipelines, this is the most useful first-stage pool because it preserves nearly every relevant passage while still ranking many positives near the top.

### Metric Interpretation for Model Researchers

This split shows a clear division: dense retrieval is strongest for nDCG@10, while hybrid retrieval is strongest for hit@10 and recall@100. BM25 is also strong, especially in recall, because Spanish Wikipedia passages preserve many exact terms. The task is therefore useful for separating ranking quality from candidate coverage.

Researchers should not judge this task by hit@10 alone. With 86.0% multi-positive queries, finding one relevant passage is much easier than ordering several. nDCG@10 better reflects whether the model ranks the set of relevant passages well.

### Query and Relevance Type Tendencies

Representative queries ask about the architecture of the Orbelian caravanserai, what Jews call the Pentateuch, when Daniel Harold Rolling received lethal injection, how to define parliamentarism, and what the mission of the Praetorian Guard was. These are encyclopedia information needs with direct evidence in Wikipedia-style passages.

Relevant documents often include titles and explanatory text. Some queries require definitions; others ask for dates, roles, missions, or terminology. A good model should retrieve all passages that satisfy the information need, not only the title-bearing passage.

### Representative Failure Modes

BM25 may over-rank passages that contain the same entity name but do not answer the specific question. Dense retrieval may rank a semantically related explanatory passage highly while missing additional relevant passages that use different wording. Hybrid retrieval can include nearly all positives but may still order lexical matches above the most directly useful passages.

Another failure mode is confusing related entities in Wikipedia. Articles about adjacent historical terms, religious concepts, or political systems can share many words. Models must distinguish the exact information need.

### Training Data That May Help

Useful training data includes non-overlapping MIRACL Spanish training data, Spanish Wikipedia question-passage retrieval pairs, native Spanish retrieval data, and hard negatives from related Wikipedia entities. Multi-positive objectives or listwise distillation are useful because many queries have several relevant passages.

Hard negatives should come from the same topic area, article neighborhood, or entity family. Random negatives are too easy for this task. The best training examples teach the model to rank directly answer-bearing passages above related encyclopedia text.

### Model Improvement Notes

Dense models can improve by preserving both semantic answer relevance and broader candidate coverage. Sparse systems are strong and should not be ignored; Spanish lexical matching remains highly effective. Hybrid systems are particularly useful for reranking pipelines because they preserve almost all positives at top 100.

For evaluation, nDCG@10 should be used to judge direct ranking, while recall@100 should be used to judge first-stage retrieval for reranking. This split makes that distinction explicit.

## Example Data

### Public Sources

- MIRACL paper: https://arxiv.org/abs/2210.09984
- MTEB benchmark paper: https://arxiv.org/abs/2210.07316
- Source task dataset card: https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| MIRACL paper | Original multilingual retrieval benchmark description. |
| MTEB paper | Retrieval benchmark context. |
| MTEB task card | Hard-negative retrieval packaging. |

### Representative Snippets

- A query asks about the architecture of the Orbelian caravanserai; relevant passages describe its basalt-block construction.
- A query asks what Jews call the Pentateuch; relevant passages connect it with the Torah.
- A query asks when Daniel Harold Rolling received lethal injection; relevant passages state the execution date.
- A query asks how to define parliamentarism; relevant passages define the parliamentary system of government.
- A query asks what the Praetorian Guard's mission was; relevant passages describe its role protecting Roman emperors.
