# MNanoBEIR / NanoBEIR-th / NanoDBPedia

## Overview

NanoDBPedia in the Thai NanoBEIR slice is an entity-oriented retrieval task derived from DBpedia Entity Retrieval. The queries are Thai translated entity information needs, and the corpus contains Thai translated DBpedia-style entity descriptions. The task asks a model to rank entities that satisfy short needs involving names, categories, places, works, organizations, or entity classes. It is a compact diagnostic for multilingual entity search, alias handling, and type-aware retrieval in Thai.

## Details

### What the Original Data Measures

DBpedia Entity Retrieval evaluates ranking entities for information needs over an encyclopedic knowledge base. In BEIR-style retrieval, the entity descriptions are treated as documents. Relevance can depend on entity name, alias, type, location, category, relationship, or a combination of these constraints. A relevant result is not merely a document sharing words with the query; it must be the right kind of entity.

The Thai translated version adds difficulty from short Thai queries, translated descriptions, entity names that may remain in English, and tokenization-sensitive matching. A strong model must preserve exact names and categories while also recognizing semantic entity constraints when the query wording differs from the description wording.

### Observed Data Profile

The task contains 50 queries, 6,045 documents, and 1,158 relevance judgments. It is strongly multi-positive, with an average of 23.16 positives per query. The minimum is 1, the median is 18.0, the maximum is 81, and 48 queries are multi-positive, or 96.0% of the query set. This makes the benchmark a broad entity ranking task rather than single-answer lookup.

Queries average 30.92 characters, while documents average 316.44 characters. The queries are short and often keyword-like, while entity descriptions are concise summaries. Since one query can match many entities, the model must recover the relevant set, not just one obvious name match.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.5043, hit@10 of 0.9200, and recall@100 of 0.6520 using the top-500 BM25 candidate subset. This is a strong lexical profile. Entity retrieval often contains names, places, or category terms that transfer directly into descriptions, and BM25 can exploit these anchors effectively.

The recall@100 value shows the remaining challenge. Many queries have broad relevant sets, and exact overlap may miss aliases, translated category labels, or entities that satisfy the intent without repeating the query terms. BM25 is useful for initial entity matching but does not fully cover the relevant set.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.5468, hit@10 of 0.9400, and recall@100 of 0.6675. Dense retrieval improves over BM25 across the main metrics, although the margin is moderate. This indicates that embedding similarity helps identify type and category matches beyond exact lexical overlap.

Dense retrieval is especially useful when the query is short and underspecified. It can connect entity needs to descriptions that use different phrasing, and it can capture broader semantic categories such as films, former republics, architecture, or collections. Remaining errors are likely to involve ambiguous entity types, names that require exact matching, or broad queries with many acceptable results.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.5482, hit@10 of 0.9000, and recall@100 of 0.6986. It uses exactly 100 candidates per query, with no rank-101 safeguard rows. The hybrid profile has the best nDCG@10 and recall@100, while dense retrieval has the best hit@10.

This pattern suggests that combining lexical and dense evidence is useful for ranking the broader entity set. BM25 contributes exact names and type terms, while dense retrieval adds semantic category matching. The small nDCG gain over dense indicates that the two signals are complementary, though the lower hit@10 also shows that hybrid ordering can occasionally displace an early obvious positive.

### Metric Interpretation for Model Researchers

Because almost every query has many positives, hit@10 alone is insufficient. A model can find one relevant entity early and still fail to rank the relevant set well. nDCG@10 measures first-page density and ordering quality, while recall@100 measures whether the candidate set covers enough relevant entities for downstream reranking.

The method comparison shows a balanced task. BM25 is strong because entity names and categories are lexical. Dense retrieval improves semantic type matching. reranking_hybrid gives the best graded top-10 ranking and recall. This makes NanoDBPedia-th useful for testing entity search systems that combine exact name handling with semantic category understanding.

### Query and Relevance Type Tendencies

Queries include entity needs such as Fitzgerald Auto Mall in Chambersburg, a 1994 Alice Munro short-story collection, Roman architecture in Paris, former Yugoslav republics, and films shot in Venice. Relevant documents are DBpedia-style descriptions of entities that satisfy those needs.

The task rewards models that track type constraints and entity attributes. A query may specify a location, work type, author, historical category, or class of films. The right result must satisfy those constraints, not merely mention one of the words.

### Representative Failure Modes

Likely failures include retrieving entities with the wrong type, over-ranking famous entities that share a name fragment, missing aliases or translated category names, and failing to cover many positives for broad entity-class queries. BM25 may be too literal, while dense retrieval may blur neighboring entity types. Hybrid systems need careful ordering to preserve both exact names and type semantics.

### Training Data That May Help

Useful training data includes entity retrieval, Wikipedia or DBpedia search, multilingual entity linking, alias matching, and type-aware ranking. Thai encyclopedic text can help with translated descriptions and segmentation behavior. Hard negatives should share names, locations, categories, or entity types while violating a key constraint.

### Model Improvement Notes

A model targeting this task should combine exact entity-name precision with semantic type awareness. Sparse systems need Thai-aware tokenization and alias normalization. Dense systems should improve constraint tracking for short queries. Hybrid systems are well aligned with the benchmark when the final ranking balances lexical anchors and semantic entity class matching.

## Example Data

### Public Sources

The original task is based on DBpedia Entity Retrieval, with BEIR providing the retrieval benchmark framing and NanoBEIR providing the compact multilingual dataset packaging.

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [DBpedia Entity Retrieval](https://doi.org/10.1145/3077136.3080751) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-th dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |

Representative query and positive entity snippets:

| Query | Positive document snippet |
| --- | --- |
| ฟิตซ์เจอรัลด์ออโต้มอลล์แชมเบอร์สเบิร์กเพนซิลเวเนีย | ฟิตซ์เจอรัลด์ ออโต้ มอลล์ เป็นตัวแทนจำหน่ายรถยนต์ที่เป็นของครอบครัว... |
| การรวบรวมเรื่องสั้นปี 1994 ของอลิส มุนโร เปิดอยู่ | อลิซ แอน มันโร เป็นนักเขียนชาวแคนาดา ผลงานของมันโรถูกอธิบายว่า... |
| สถาปัตยกรรมโรมันในปารีส | ศิลปะในปารีสเป็นบทความเกี่ยวกับวัฒนธรรมและประวัติศาสตร์ศิลปะในปารีส... |
| สาธารณรัฐของยูโกสลาเวียเดิม | รัฐธรรมนูญยูโกสลาเวียปี 1974 เป็นรัฐธรรมนูญฉบับที่สี่... |
| ภาพยนตร์ที่ถ่ายทำในเวนิส | A Little Romance เป็นภาพยนตร์ตลกโรแมนติก Technicolor และ Panavision ของอเมริกา... |
