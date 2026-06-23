# NanoDAPFAM / NanoDAPFAMInTitlAbsClmToFullText

## Overview

NanoDAPFAMInTitlAbsClmToFullText is an English patent-family retrieval task. The query contains a source patent family's title, abstract, and claims, while the target document contains the full text of a candidate patent family. Relevance comes from the DAPFAM IN-domain condition, meaning positive families are citation-related and share an IPC3 technical class with the query family.

This split tests in-domain prior-art retrieval with long patent text on both sides. The query is claim-rich, and the target is full-text, so lexical overlap is available. The challenge is to rank truly cited same-domain families above many patents that share technical class vocabulary and legal phrasing.

## Details

### What the Original Data Measures

DAPFAM is a domain-aware patent retrieval benchmark built at family level. It uses patent-family citations as qrels and defines IN-domain relations when query and target families share at least one IPC code at the first-three-character level.

This split focuses on the IN-domain subset. It measures whether a claim-rich source patent can retrieve same-domain cited patent families represented by full text. Because all positives are in-domain, the task emphasizes fine-grained prior-art discrimination inside related technical areas.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 3,069 positive qrels. Most queries are multi-positive: 194 of 200 queries have more than one positive. The average positives per query is 15.35, with a minimum of 1, median of 18.0, and maximum of 20. Queries average 8,405.46 characters, while full-text documents average 68,906.02 characters.

The data is long and patent-specific. Query claims supply detailed components and constraints, while target full texts include descriptions, claims, and background sections from same-domain patent families.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3505, hit@10 of 0.8150, and recall@100 of 0.5673 with a top-500 candidate pool. Exact technical terms, component names, materials, and claim phrases help lexical retrieval. In-domain filtering also means many relevant documents share vocabulary with the source.

The remaining difficulty is that same-domain negatives also share much of that vocabulary. BM25 can find patents in the right technical area but may not distinguish citation-relevant families from merely similar families. Full-text length further increases incidental term overlap.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is strongest by top-rank metrics, with nDCG@10 of 0.4484, hit@10 of 0.8950, and recall@100 of 0.7025. Dense retrieval improves over BM25 by capturing technical relatedness beyond exact claim wording.

Dense retrieval is especially useful when cited families describe the same invention space with different claim structures. The higher recall relative to BM25 indicates that semantic similarity is important even inside a shared IPC3 domain.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.4375, hit@10 of 0.8850, and recall@100 of 0.7032. It uses top-100 candidates with optional rank-101 safeguards; seven rows contain 101 candidates and seven safeguard-positive rows are recorded. Hybrid retrieval has the best recall@100 by a small margin, while dense retrieval has the best nDCG@10.

This indicates complementary signals. BM25 captures exact claim terms, while dense retrieval captures paraphrased technical similarity. The hybrid pool is useful for broad positive coverage, but dense ranking is slightly cleaner at the top.

### Metric Interpretation for Model Researchers

This is an in-domain, multi-positive patent retrieval task. Hit@10 shows whether a model finds at least one same-domain cited family, while recall@100 shows how much of the citation set it covers. Dense and hybrid recall are both much higher than BM25 recall, making this split a good test of semantic prior-art retrieval inside one technical domain.

Because target documents are full text, single-vector models may dilute relevant evidence. The best systems should combine long-document handling with claim-aware matching.

### Query and Relevance Type Tendencies

Queries include title, abstract, and claims. Documents are full patent-family texts. Positives share IPC3 domain with the query and are citation-related. This creates many same-field distractors that are lexically close but not qrel-positive.

### Representative Failure Modes

BM25 may rank same-domain patents with overlapping claim language but no citation relationship. Dense retrieval may find broad technical similarity but miss specific cited families. Hybrid retrieval improves coverage but can still rank long full-text distractors highly when they contain both exact and semantic overlap.

### Training Data That May Help

Useful training data includes same-IPC patent citation retrieval, in-domain prior-art search, and claim-aware patent-family retrieval. Training should exclude NanoDAPFAM evaluation families, positives, qrels, and same-family duplicates.

Synthetic data should use same-domain patent full-text records with shared IPC-style terminology, and positives should be cited same-domain patent families rather than merely topic-similar examples.

### Model Improvement Notes

Improving this task requires fine-grained in-domain discrimination. Models should preserve claim elements, component relationships, and technical effects while discounting boilerplate and broad class vocabulary.

Chunk-level retrieval or late interaction may help because relevant full-text evidence can be localized inside a very long patent record.

## Example Data

| Query | Positive document |
| --- | --- |
| snow removal equipment with automatic walking function the invention relates to snow removal equipme... [100 / 6,075 chars] | multifunctional device for clearing snow an apparatus and method for clearing an accumulation of matter from a surface that includes a blade configured to collect matter upon movement of the apparatus... [200 / 59,310 chars] |
| apparatus for indication of at least one subsurface barrier characteristic and methods of use a cont... [100 / 11,428 chars] | method of confirming position of drain material left and apparatus for confirming same in drain engineering method a method and apparatus is provided to embed paper drain material in water-laden soil... [200 / 23,599 chars] |
| an article including identification for use in an electrically heated smoking system. there is provi... [100 / 5,076 chars] | apparatus for generating aerosol from an aerosolisable medium, an article of aerosolisable medium and a method of determining a parameter of an article to provide an apparatus that heats an aerosoliza... [200 / 52,756 chars] |
| low weight carpet and carpet tile and methods of manufacture low weight and non-square carpet tile s... [100 / 3,799 chars] | anti-static mats and carpets a novel carpet material or mat which is characterized by an extraordinary ability to quickly and comfortably discharge any build-up of a static electricity charge on a per... [200 / 17,195 chars] |
| organosilicon precursors for interlayer dielectric films with low dielectric constants a method of f... [100 / 11,588 chars] | radiation shield a radiation shield and an assembly and a reactor including the radiation shield are disclosed. the radiation shield can be used to control heat flux from a susceptor heater assembly a... [200 / 48,536 chars] |

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
| A claim-rich patent family in a specific technical class. | A long full-text patent family that is cited and shares the same IPC3 domain. |
| A source family with detailed apparatus components. | A target full-text family with related components and same-domain prior-art relation. |
| A source process patent with numbered claim steps. | A cited target family whose full description expands a related process. |
| A source material or device patent with technical constraints. | A full-text same-domain family sharing the technical field and citation relation. |
| A source vehicle or machinery system patent. | A full-text target family in the same technical domain with related control or apparatus claims. |
