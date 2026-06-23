# NanoBEIR-en / NanoDBPedia

## Overview

NanoDBPedia is the compact English NanoBEIR version of DBpedia-Entity, an entity search task over DBpedia-style entity descriptions. Queries are short entity-oriented information needs, ranging from keyword strings to factual questions and list requests. The retrieval goal is to return the DBpedia entities that satisfy the query, not merely documents that share surface words. This makes the task useful for evaluating entity retrieval, alias handling, entity typing, relation matching, and multi-positive ranking.

## Details

### What the Original Data Measures

DBpedia-Entity v2 was built as a test collection for entity search over the DBpedia knowledge base. The original benchmark targets free-text queries whose desired outputs are ranked DBpedia entity URIs. Its query sources include named-entity search, keyword queries, list search, and natural-language questions answerable by entities.

The BEIR version treats DBpedia entity descriptions as retrieval documents, and the NanoBEIR version keeps a compact English sample. Relevance can be single-entity lookup, but it can also be a broad entity set: places, people, products, historical entities, occupations, works, or entities satisfying an attribute relation.

### Observed Data Profile

The task contains 50 queries, 6,045 documents, and 1,158 relevance judgments. It is strongly multi-positive, with an average of 23.16 positives per query. The minimum is 1, the median is 18.0, the maximum is 81, and 48 queries are multi-positive, or 96.0% of the set.

Queries are short, averaging 33.10 characters, while documents average 336.31 characters. The documents are compact entity descriptions that often begin with a title and a short encyclopedic summary. The benchmark therefore mixes direct title matching with set retrieval and relation-aware entity search.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6374, hit@10 of 0.9400, and recall@100 of 0.7168 using the top-500 BM25 candidate subset. This is a strong lexical baseline. Short entity queries often contain names, aliases, types, or rare phrases that appear in the relevant entity descriptions.

However, hit@10 is not enough for this task because most queries have many positives. BM25 may find one entity quickly but fail to cover enough of the relevant entity set. It can also over-rank entities that share names or broad types while missing entities that satisfy an attribute constraint, relation, or list intent.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.6243, hit@10 of 0.9600, and recall@100 of 0.7599. Dense retrieval improves hit@10 and recall@100 over BM25 but is slightly weaker on nDCG@10. This suggests that embedding similarity broadens the candidate pool but may not always put the most directly relevant entities at the top.

Dense retrieval is useful for relation and type matching, especially when the query is not an exact entity name. It can connect natural-language questions to descriptions that express the answer indirectly. The tradeoff is that entity search often rewards exact aliases, titles, and identifiers, where sparse matching remains highly competitive.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.6564, hit@10 of 0.9200, and recall@100 of 0.7746. It uses exactly 100 candidates per query, with no safeguard rows. The hybrid profile has the best nDCG@10 and recall@100, though dense has the highest hit@10.

This indicates that entity retrieval benefits from combining sparse and dense signals. BM25 contributes exact names and aliases, while dense retrieval contributes type and relation similarity. The hybrid candidate pool is especially appropriate when a downstream model must rank many relevant entities rather than just find one.

### Metric Interpretation for Model Researchers

Because the task is highly multi-positive, nDCG@10 and recall@100 are more informative than hit@10. A system can have a high hit@10 by finding one relevant entity while still missing most of the intended entity set. recall@100 measures whether a reranker can access enough candidates for list and class queries.

The comparison shows that BM25 is strong for surface entity matching, dense retrieval increases coverage, and reranking_hybrid gives the best balance for ranking and candidate completeness. This task is useful for testing whether retrieval models can handle entity sets, not only single-page lookup.

### Query and Relevance Type Tendencies

Queries include direct strings such as Fitzgerald Auto Mall in Chambersburg, a short story collection by Alice Munro, Gallo-Roman architecture in Paris, republics of the former Yugoslavia, and films shot in Venice. Other queries can ask natural-language entity questions or list constraints. Relevant documents are DBpedia-style entity descriptions.

The task rewards alias matching, entity type recognition, and relation interpretation. A positive can be a direct entity page, a member of a requested class, or an entity satisfying a factual relation. Same-name and same-type distractors are common sources of error.

### Representative Failure Modes

Likely failures include retrieving entities with overlapping names but wrong types, finding one correct entity while missing many other positives, confusing list intent with direct lookup, and over-ranking descriptions that mention the query terms without satisfying the relation. BM25 may be too literal, while dense retrieval may be too broad for precise entity identity.

### Training Data That May Help

Useful training data includes non-overlapping DBpedia or Wikidata entity-search pairs, Wikipedia title and abstract retrieval, knowledge-base QA with entity answers, entity linking data, and list-completion or entity-set retrieval data. Multi-positive supervision is especially valuable because many queries have large relevant sets.

### Model Improvement Notes

A model targeting this task should preserve exact entity and alias recall while improving type and relation matching. Sparse systems need title, alias, and field-aware indexing. Dense systems need entity-centric contrastive training with same-type hard negatives. Hybrid systems are promising because the best observed profile combines entity-name precision with broader semantic coverage.

## Example Data

| Query | Positive document |
| --- | --- |
| fitzgerald auto mall chambersburg pa [36 chars] | Fitzgerald Auto Malls is a family owned and operated auto dealership that was founded in 1966, with its first location opening in Bethesda, Maryland. As of 2014, Fitzgerald Auto Malls ranked number 59... [200 / 429 chars] |
| 1994 short story collection Alice Munro is Open [47 chars] | Alice Ann Munro (/ˈælɨs ˌæn mʌnˈroʊ/, née Laidlaw /ˈleɪdlɔː/; born 10 July 1931) is a Canadian author. Munro's work has been described as having revolutionized the architecture of short stories, espec... [200 / 499 chars] |
| gallo roman architecture in paris [33 chars] | Art in Paris is an article on the art culture and history in Paris, the capital of France. For centuries, Paris has attracted artists from around the world, arriving in the city to educate themselves... [200 / 333 chars] |
| republics of the former Yugoslavia [34 chars] | The 1974 Yugoslav Constitution was the fourth and final constitution of the Socialist Federal Republic of Yugoslavia. It came into effect on February 21.With 406 original articles, the 1974 constituti... [200 / 436 chars] |
| films shot in Venice [20 chars] | A Little Romance is a 1979 American Technicolor and Panavision romantic comedy film directed by George Roy Hill and starring Laurence Olivier, Thelonious Bernard, and Diane Lane in her film debut. The... [200 / 371 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset paper | [DBpedia-Entity v2](https://doi.org/10.1145/3077136.3080751) |
| Project page | [DBpedia-Entity official project page](https://iai-group.github.io/DBpedia-Entity/) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-en dataset | [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en) |

Representative query and positive entity snippets:

| Query | Positive document snippet |
| --- | --- |
| fitzgerald auto mall chambersburg pa | Fitzgerald Auto Malls is a family owned and operated auto dealership founded in 1966. |
| 1994 short story collection Alice Munro is Open | Alice Ann Munro is a Canadian author known for short stories. |
| gallo roman architecture in paris | Art in Paris is an article on art culture and history in the capital of France. |
| republics of the former Yugoslavia | The 1974 Yugoslav Constitution was the final constitution of the Socialist Federal Republic of Yugoslavia. |
| films shot in Venice | A Little Romance is a 1979 romantic comedy film directed by George Roy Hill. |
