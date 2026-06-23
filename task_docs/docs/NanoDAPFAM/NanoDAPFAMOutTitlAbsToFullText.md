# NanoDAPFAM / NanoDAPFAMOutTitlAbsToFullText

## Overview

NanoDAPFAMOutTitlAbsToFullText is an English patent-family retrieval task. The query contains only the title and abstract of a source patent family, while target documents contain full patent-family text. Positives are DAPFAM OUT-domain citation relations, meaning relevant target families do not share IPC3 domain with the source.

This split tests compact-query cross-domain prior-art retrieval over very long target documents. The model must infer a cross-domain technical relationship from a short patent summary and find it inside full-text records from different fields.

## Details

### What the Original Data Measures

DAPFAM benchmarks family-level patent retrieval using citation links and IPC3 domain labels. OUT-domain positives are citation-related families outside the source domain. This split uses title-abstract queries and full-text targets.

It measures cross-domain retrieval with minimal query context and maximal target length. This is one of the more realistic settings for difficult prior-art discovery from a compact patent summary.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 1,259 positive qrels. There are 159 multi-positive queries. Positives per query average 6.30, with a minimum of 1, median of 4.0, and maximum of 20. Queries average 786.61 characters, while target documents average 71,902.31 characters.

The short query and very long target create both semantic and length challenges. Relevant cross-domain evidence may be sparse inside the target full text.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.0638, hit@10 of 0.2100, and recall@100 of 0.1875 with a top-500 candidate pool. Exact title and abstract terms are not reliable enough for cross-domain search, and full-text targets introduce many incidental matches.

BM25 can help when a cross-domain target uses shared mechanism or material names, but most OUT-domain positives require more abstract matching than term frequency provides.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is strongest by nDCG@10 and hit@10, with nDCG@10 of 0.0952, hit@10 of 0.3350, and recall@100 of 0.2518. Dense retrieval improves over BM25 by matching technical similarity beyond shared terms.

The absolute scores remain low because the query is compact and the relevant target is cross-domain and very long. Dense retrieval must represent analogy or technical transfer, not just topical similarity.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.0858, hit@10 of 0.3050, and recall@100 of 0.2653. It uses top-100 candidates with optional rank-101 safeguards; 74 rows contain 101 candidates and 74 safeguard-positive rows are recorded. Hybrid provides the best recall@100, while dense has better top-rank ordering.

This suggests that lexical evidence adds some additional positives but also introduces noise. A downstream reranker would need to identify the cross-domain relationship among many weakly related candidates.

### Metric Interpretation for Model Researchers

This is a difficult short-query, long-target, cross-domain patent retrieval task. The gap between BM25 and dense shows that semantic retrieval is necessary, but the low absolute recall shows that current dense candidates still miss many positives.

The task is useful for testing cross-domain prior-art discovery and long-document retrieval, especially under limited query context.

### Query and Relevance Type Tendencies

Queries are title-abstract summaries. Documents are full patent texts. Positives are citation-related families outside the query's IPC3 class.

The relevant relationship may involve analogous functions, mechanisms, control methods, materials, or processes that are described differently across domains.

### Representative Failure Modes

BM25 retrieves long documents with incidental term overlap. Dense retrieval retrieves broadly related technology but misses citation relevance. Hybrid retrieval can recover more positives by rank 100 but may rank lexical distractors above them.

### Training Data That May Help

Useful training data includes cross-domain title-abstract patent retrieval, cross-IPC patent citation pairs, and long-target prior-art search. Training should exclude NanoDAPFAM evaluation family IDs, positives, and qrels.

Synthetic data should pair compact source patent summaries with long full-text patent records from different technical classes.

### Model Improvement Notes

Improving this task requires cross-domain semantic expansion from short summaries and evidence extraction from long targets. Models should learn functional analogy and technical effect matching across IPC classes.

Passage-level target representations are likely important because a full-text patent may contain the relevant cross-domain evidence only in a small section.

## Example Data

| Query | Positive document |
| --- | --- |
| bicycle handlebar grip a bicycle handlebar grip contains a plastic inner shell having a tubular shap... [100 / 821 chars] | durable flexible membrane and method of making same a flexible membrane having a valuable combination of desirable properties is composed of a generally heavy, dense supporting and reinforcing reticul... [200 / 28,042 chars] |
| method for improving belt press dewatering a method for increasing the removal of a higher fraction... [100 / 620 chars] | artificial human anti-factor b antibody problem to be solved: to provide novel engineered forms of a monoclonal antibody and antigen-binding fragments thereof that bind complement protein factor b and... [200 / 108,109 chars] |
| stitch distribution control system for tufting machines a stitch distribution control system for a t... [100 / 647 chars] | method and apparatus for measuring direction or position of weft yarn of fabric the measurement of the pick or stitches course position in continuously moved fabrics involves examining at least one ga... [200 / 24,253 chars] |
| low weight carpet and carpet tile and methods of manufacture low weight and non-square carpet tile s... [100 / 565 chars] | modular floor covering units with built-in lighting an apparatus for guiding the occupants of a structure along a path of travel within the structure is provided. the apparatus is comprised of modular... [200 / 35,319 chars] |
| method and apparatus for the zonal transmission of data using building lighting fixtures this invent... [100 / 969 chars] | shelf tag with ambient light detector the present invention relates to an electronic shelf display device which includes an optical device and an ambient light detector circuitry. the electronic shelf... [200 / 54,320 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [DAPFAM: A Domain-Aware Family-level Dataset to benchmark cross domain patent retrieval](https://arxiv.org/abs/2506.22141) | Source benchmark paper for family-level patent retrieval. |
| [DAPFAM DOI record](https://doi.org/10.1016/j.array.2026.100720) | DOI record for the DAPFAM paper. |
| [datalyes/DAPFAM_patent](https://huggingface.co/datasets/datalyes/DAPFAM_patent) | Public source dataset card. |
| [hakari-bench/NanoDAPFAM](https://huggingface.co/datasets/hakari-bench/NanoDAPFAM) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A compact title-abstract source summary. | A full-text target family in a different IPC3 domain with citation relevance. |
| A short apparatus abstract. | A long cross-domain target with analogous apparatus behavior. |
| A short process abstract. | A full-text target from another class with related process logic. |
| A compact material or composition summary. | A cross-domain full-text target with related material effects. |
| A control-system abstract. | A long target in another field with analogous control principles. |
