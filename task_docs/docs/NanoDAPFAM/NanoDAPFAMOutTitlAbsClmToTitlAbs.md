# NanoDAPFAM / NanoDAPFAMOutTitlAbsClmToTitlAbs

## Overview

NanoDAPFAMOutTitlAbsClmToTitlAbs is an English patent-family retrieval task. The query contains title, abstract, and claims from a source family, while target documents contain only title and abstract. Positives are DAPFAM OUT-domain citation relations, so query and target families do not share IPC3 domain.

This is a hard long-query to short-target cross-domain patent retrieval task. The target abstracts are concise and may not expose the detailed reasoning behind a cross-domain citation. The model must connect source claims to short summaries from different technical classes.

## Details

### What the Original Data Measures

DAPFAM uses citation links as relevance judgments and IPC3 overlap to define domain relations. OUT-domain positives are cited families outside the query's IPC3 domain. This split uses a claim-rich source representation and a short title-abstract target representation.

The task measures cross-domain prior-art retrieval when the target exposes only summary-level evidence.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 1,257 positive qrels. There are 159 multi-positive queries. Positives per query average 6.29, with a minimum of 1, median of 4.0, and maximum of 20. Queries average 9,315.66 characters, while target documents average 777.94 characters.

The mismatch is severe: detailed source claims must retrieve compact summaries from other technical classes.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.0439, hit@10 of 0.1600, and recall@100 of 0.1225 with a top-500 candidate pool. Exact word matching is especially weak because targets are short and cross-domain.

BM25 can only help when distinctive terminology survives across domains. Otherwise, it tends to retrieve same-topic or superficially similar summaries rather than cited OUT-domain families.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is strongest, with nDCG@10 of 0.0872, hit@10 of 0.2900, and recall@100 of 0.2235. Dense retrieval nearly doubles BM25 recall, showing that semantic matching is crucial.

The absolute score remains low because short target abstracts omit many details needed to explain cross-domain relevance. Dense models must infer analogy or technical dependency from limited text.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.0714, hit@10 of 0.2500, and recall@100 of 0.2220. It uses top-100 candidates with optional rank-101 safeguards; 77 rows contain 101 candidates and 77 safeguard-positive rows are recorded. Dense retrieval is slightly stronger across all major top metrics.

The many safeguard rows indicate that positives often do not appear naturally in the top-100 hybrid pool. This split is a difficult candidate-generation problem.

### Metric Interpretation for Model Researchers

This split is a stress test for cross-domain patent retrieval from claim-rich queries to short summaries. BM25 is not sufficient, and dense retrieval is only moderately successful. It reveals whether a model can identify technology-transfer style relevance from compact target records.

Because each query has fewer positives than IN variants, missing a relevant family has a larger effect on recall. Evaluation should focus on both top-rank quality and candidate coverage.

### Query and Relevance Type Tendencies

Queries contain title, abstract, and claims. Documents contain title and abstract only. Positives are citation-related but outside the source IPC3 domain.

Relevance often depends on functional analogy, shared technical effect, or transferred mechanism rather than exact field vocabulary.

### Representative Failure Modes

BM25 misses positives due to vocabulary shift and short target text. Dense retrieval may retrieve semantically broad but non-cited summaries. Hybrid retrieval can introduce lexical distractors without improving top ranking.

### Training Data That May Help

Useful training data includes cross-IPC patent citation retrieval, cross-domain prior-art search with short targets, and patent analogy retrieval. Training should exclude NanoDAPFAM evaluation families and qrels.

Synthetic data should generate long source records and short target title-abstract records from different technical classes, with positives based on cross-domain citation relevance.

### Model Improvement Notes

Improving this task requires better cross-domain abstraction from claims to short summaries. Models should learn to recognize shared functions and technical effects even when domain vocabulary differs.

For reranking, external signals such as citation graph structure, IPC-aware negative sampling, and technology analogy modeling may help.

## Example Data

| Query | Positive document |
| --- | --- |
| bicycle handlebar grip a bicycle handlebar grip contains a plastic inner shell having a tubular shap... [100 / 2,588 chars] | durable flexible membrane and method of making same a flexible membrane having a valuable combination of desirable properties is composed of a generally heavy, dense supporting and reinforcing reticul... [200 / 1,921 chars] |
| method for improving belt press dewatering a method for increasing the removal of a higher fraction... [100 / 4,605 chars] | artificial human anti-factor b antibody problem to be solved: to provide novel engineered forms of a monoclonal antibody and antigen-binding fragments thereof that bind complement protein factor b and... [200 / 533 chars] |
| stitch distribution control system for tufting machines a stitch distribution control system for a t... [100 / 5,968 chars] | method and apparatus for measuring direction or position of weft yarn of fabric the measurement of the pick or stitches course position in continuously moved fabrics involves examining at least one ga... [200 / 789 chars] |
| low weight carpet and carpet tile and methods of manufacture low weight and non-square carpet tile s... [100 / 3,799 chars] | modular floor covering units with built-in lighting an apparatus for guiding the occupants of a structure along a path of travel within the structure is provided. the apparatus is comprised of modular... [200 / 785 chars] |
| method and apparatus for the zonal transmission of data using building lighting fixtures this invent... [100 / 7,344 chars] | shelf tag with ambient light detector the present invention relates to an electronic shelf display device which includes an optical device and an ambient light detector circuitry. the electronic shelf... [200 / 1,213 chars] |

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
| A claim-rich source patent from one field. | A short title-abstract target from another field with a citation relation. |
| A detailed mechanical apparatus query. | A cross-domain abstract expressing a related functional mechanism. |
| A process claim query. | A target summary in another class with related process behavior. |
| A material or composition query. | A target abstract from another domain with a related material effect. |
| A control-system query. | A cross-domain target summary with analogous control logic. |
