# NanoMTEB-v2 / fever

## Overview

`NanoMTEB-v2 / fever` is a claim-to-evidence retrieval task derived from FEVER. Queries are short factual claims, and relevant documents are Wikipedia passages that provide evidence for or against those claims. The original FEVER benchmark was introduced for fact extraction and verification: a system must retrieve evidence and then decide whether a claim is supported, refuted, or unverifiable. This Nano retrieval split focuses on the evidence-retrieval step using 200 claims over 10,000 candidate passages. It is a comparatively lexical, entity-centered fact-checking task where claims often contain named entities that also appear in the correct evidence passage.

## Details

### What the Original Data Measures

FEVER measures whether systems can retrieve and reason over Wikipedia evidence for factual claims. In the retrieval conversion, the model is not asked to output the final verification label; it must find the passages that contain the relevant evidence. A relevant passage may support or refute the claim, but it must be evidentially connected to the specific entity and relation in the query.

The MTEB hard-negative source makes the task more useful for retrieval evaluation by including plausible Wikipedia passages, not only random negatives.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 229 positive qrel rows. Each query has 1.145 positives on average, with a median of 1 and a maximum of 4. There are 25 multi-positive queries, or 12.5% of the query set. Queries average 50.56 characters, while documents average 565.98 characters.

The examples include claims about films, locations, companies, actors, and historical figures. Documents usually begin with a Wikipedia title followed by a passage, so entity names and aliases are strong retrieval anchors.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.8893, hit@10 of 0.9950, and recall@100 of 0.9869. This is a very strong sparse profile. The claims often include distinctive named entities, and the evidence passages repeat those entities in titles or opening sentences.

BM25's remaining difficulty is exact evidence selection. A passage about the correct entity may not contain the specific fact needed for the claim, and a claim can be false while still sharing many words with a related article. Even so, sparse lexical retrieval is already near ceiling as a candidate generator on this Nano split.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.9652, hit@10 of 0.9800, and recall@100 of 0.9738. Dense retrieval has the best nDCG@10, although its hit@10 and recall@100 are slightly below BM25. This indicates that dense representations rank the correct evidence passage more cleanly when it is retrieved, but BM25 has slightly broader coverage.

The dense advantage at the top rank likely comes from modeling claim semantics beyond entity names. It can prefer passages that match the relation or role in the claim rather than passages that only repeat the entity.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates with no safeguard positives. It reaches nDCG@10 of 0.9450, hit@10 of 0.9950, and recall@100 of 0.9869. The hybrid pool matches BM25 coverage while improving top-rank quality over BM25, though dense retrieval remains strongest by nDCG@10.

This pattern is useful for reranking: BM25 supplies excellent entity coverage, dense retrieval improves semantic ordering, and their hybrid gives a reliable candidate set for a reranker that can judge evidential relevance.

### Metric Interpretation for Model Researchers

Scores are high, so this task is partly a sanity check for English Wikipedia evidence retrieval. A weak model may fail to connect claims and titles, but strong systems should approach ceiling. Small differences in nDCG@10 still matter because they show whether a model ranks the exact evidence passage first rather than merely retrieving it somewhere in the candidate list.

The low multi-positive rate means most claims are effectively single-evidence retrieval cases. Exact top-rank placement is therefore important.

### Query and Relevance Type Tendencies

Queries are short declarative factual claims. Relevant documents are Wikipedia passages about the claim's entities, works, places, or historical figures. Many queries require matching a named entity and a specific predicate such as award count, location, occupation, company type, or cause of death.

The relevance relation is evidential, not just topical. A page about the entity may still be wrong if it lacks evidence for the claim.

### Representative Failure Modes

Common failures include retrieving the correct entity page but the wrong passage, matching an entity without matching the predicate, confusing related works or people, and ignoring negation or numeric constraints. Dense models may occasionally prefer semantically broad passages, while sparse systems may over-rank pages with heavy entity-term overlap.

### Training Data That May Help

Useful training data includes FEVER claim-evidence pairs, Wikipedia entity retrieval data, fact-checking evidence datasets, and hard negatives with the same named entities but different predicates. Training examples from this evaluation split should be excluded.

### Model Improvement Notes

The most important improvements are exact evidence discrimination and relation-aware ranking. Candidate generation is already strong, so rerankers should focus on whether the passage actually supports or refutes the claim. Hard negatives should share the same entity while changing relation, date, role, award, location, or membership facts.

## Example Data

| Query | Positive document |
| --- | --- |
| One Flew Over the Cuckoo's Nest only won one Academy Award. [59 chars] | One Flew Over the Cuckoo's Nest (film) One Flew Over the Cuckoo 's Nest is a 1975 American comedy-drama film directed by Miloš Forman , based on the 1962 novel One Flew Over the Cuckoo 's Nest by Ken... [200 / 1,023 chars] |
| Salt River Valley is on the Mississippi River. [46 chars] | Salt River Valley The Salt River Valley is an extensive valley on the Salt River in central Arizona , which contains the Phoenix Metropolitan Area . Although this geographic term still identifies the... [200 / 525 chars] |
| Sky UK is a British telecommunications company. [47 chars] | United Kingdom The United Kingdom of Great Britain and Northern Ireland , commonly known as the United Kingdom ( UK ) or Britain , is a sovereign country in western Europe . Lying off the north-wester... [200 / 5,000 chars] |
| Kaya Scodelario is a director. [30 chars] | Kaya Scodelario Kaya Scodelario-Davis ( born Kaya Rose Humphrey ; March 13 , 1992 ) is an English actress . She made her acting debut as Effy Stonem on the E4 teen drama Skins ( 2007-2010 ) , for whic... [200 / 1,626 chars] |
| A fellow Protestant murdered King Henry III of France. [54 chars] | Henry III of France Henry III ( 19 September 1551 -- 2 August 1589 ; born Alexandre Édouard de France , Henryk Walezy , Henrikas Valua ) was a monarch of the House of Valois who was elected the monarc... [200 / 2,522 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FEVER: a Large-scale Dataset for Fact Extraction and VERification | 2018 | source task paper | [https://arxiv.org/abs/1803.05355](https://arxiv.org/abs/1803.05355) |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |
| mteb/FEVER_test_top_250_only_w_correct-v2 |  | dataset card | [https://huggingface.co/datasets/mteb/FEVER_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/mteb/FEVER_test_top_250_only_w_correct-v2) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| One Flew Over the Cuckoo's Nest only won one Academy Award. | A Wikipedia passage about the 1975 film, its director, source novel, cast, and awards context. |
| Salt River Valley is on the Mississippi River. | A passage explaining that the Salt River Valley is on the Salt River in central Arizona. |
| Sky UK is a British telecommunications company. | A passage about the United Kingdom, used in the evidence pool for the claim. |
| Kaya Scodelario is a director. | A biographical passage identifying Kaya Scodelario as an English actress. |
| A fellow Protestant murdered King Henry III of France. | A passage about Henry III of France, his reign, and historical background. |
