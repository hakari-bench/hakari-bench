# NanoDAPFAM / NanoDAPFAMAllTitlAbsToFullText

## Overview

NanoDAPFAMAllTitlAbsToFullText is an English patent-family retrieval task. The query contains only the title and abstract of a source patent family, while the target document contains the full text of a candidate patent family. Relevance comes from DAPFAM family-level citation links under the ALL condition, so positives include both same-domain and cross-domain relations.

This split tests short-summary to long-patent retrieval. The query is much shorter than in claim-rich DAPFAM variants, while the target remains extremely long. A retrieval model must infer the core invention from a title and abstract, then find cited or technically related families inside very long full-text patent records.

## Details

### What the Original Data Measures

DAPFAM is a family-level patent retrieval benchmark built from patent-family records and citation links. It defines IN-domain and OUT-domain relations using IPC3 overlap and also provides ALL splits that keep both relation types. This task uses the ALL relation set.

The source representation is title plus abstract, and the target representation is full text. The task measures whether concise patent summaries can retrieve long target families that are citation-relevant.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 3,989 positive qrels. Every query has multiple positives, averaging 19.95 positives per query, with a minimum of 9 and a maximum of 20. Queries average 775.99 characters, while target full-text documents average 71,113.42 characters.

The query side is compact enough to resemble ordinary patent search input. The target side includes long descriptions, claims, and repeated legal and technical sections, which makes full-document ranking noisy.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3489, hit@10 of 0.8250, and recall@100 of 0.4663 with a top-500 candidate pool. Despite the short query, lexical retrieval remains useful because titles and abstracts contain key invention terms that often reappear in full patent text.

The main limitation is target length. Full-text documents contain many incidental terms, boilerplate, and background discussion. BM25 can find a related area but may over-rank documents that happen to repeat query terms without being citation-relevant.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.4149, hit@10 of 0.8950, and recall@100 of 0.5613. Dense retrieval improves over BM25 by matching technical meaning beyond exact title and abstract terms.

Dense retrieval is useful when a target family describes the same invention space using different words. It still has to compress very long target documents into a ranking signal, so many positives remain unrecovered by rank 100.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset is strongest overall, with nDCG@10 of 0.4175, hit@10 of 0.8950, and recall@100 of 0.5701. It uses top-100 candidates with optional rank-101 safeguards; four rows contain 101 candidates and four safeguard-positive rows are recorded.

The hybrid result indicates that exact title/abstract terms and dense technical similarity are complementary. Dense retrieval is close at the top, but hybrid gives the best recall and slightly higher nDCG.

### Metric Interpretation for Model Researchers

This is a hybrid-favored short-query to long-document patent retrieval task. Hit@10 is high for dense and hybrid, but recall@100 remains modest because each query has many positives. Models should be judged by how much of the citation family set they recover, not only whether they find one positive.

Compared with claim-rich query variants, this split has less query detail. Improving it requires strong semantic expansion from summary-level invention descriptions to full prior-art documents.

### Query and Relevance Type Tendencies

Queries are patent titles and abstracts. Documents are full patent-family texts. Positives include both same-domain and cross-domain citation relations.

The query usually states the problem and invention at summary level, while the target may express relevant evidence in claims, examples, or description sections.

### Representative Failure Modes

BM25 may over-rank full-text documents with repeated query words in background sections. Dense retrieval may retrieve broad technical similarity without exact citation relevance. Hybrid retrieval can still miss positives when the summary query is too sparse or when relevant target evidence is deeply buried.

### Training Data That May Help

Useful training data includes title-abstract patent prior-art retrieval, family-level patent citation retrieval, and long-document patent semantic search. Training should exclude NanoDAPFAM evaluation families and cited positives.

Synthetic data should pair short patent title-abstract queries with long full-text target records. Hard negatives should share technical vocabulary but differ in inventive contribution or cited relationship.

### Model Improvement Notes

Improving this task requires summary-to-full-text matching. Models should identify the invention's central function, materials, components, and technical effect from the abstract, then find long target families with related prior-art value.

Chunking, passage-level aggregation, and late interaction may help because relevant full-text evidence can be localized in a small portion of a very long document.

## Example Data

### Public Sources

NanoDAPFAM is documented through the DAPFAM paper and the public DAPFAM patent dataset card.

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
| A title and abstract for snow-removal equipment. | A full patent-family text about a related snow-clearing apparatus. |
| A title and abstract for a modular transportation system. | A long target family about transportation impact or media sharing. |
| A title and abstract for synthetic hollow microspheres. | A full-text target family about metal-coated hollow microspheres. |
| A title and abstract for low-weight carpet tile. | A long patent record about anti-static mats or carpet materials. |
| A title and abstract for lane-keeping steering. | A full-text target family about driver-assistance steering torque. |
