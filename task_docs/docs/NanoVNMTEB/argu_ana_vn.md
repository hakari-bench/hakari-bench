# NanoVNMTEB / argu_ana_vn

## Overview

`argu_ana_vn` is a Vietnamese counterargument retrieval task from NanoVNMTEB. The query is a long translated debate argument, and the relevant document is the best opposing counterargument. Each query has one positive among 8,674 candidate arguments. The task is difficult because the relevant document must be topically related but stance-opposed. Dense retrieval is the strongest top-rank profile, `reranking_hybrid` gives the best recall@100, and BM25 is weaker because lexical overlap tends to retrieve same-topic arguments without checking argumentative stance.

## Details

### What the Original Data Measures

ArguAna was introduced as a counterargument retrieval benchmark: given an argument, a system must retrieve a strong counterargument without prior topic knowledge. The task requires both topic matching and stance opposition.

VN-MTEB translates the source task into Vietnamese. This Nano split is therefore a translated Vietnamese benchmark, not a natively authored Vietnamese debate corpus. It still preserves the core retrieval challenge: same-topic similarity is not enough.

### Observed Data Profile

The Nano split contains 199 queries, 8,674 documents, and 199 positive qrel rows. Every query has exactly one positive. Queries average 1,183.88 characters, while documents average 1,080.34 characters.

Example topics include organ donation, animal testing, airport expansion and pollution, baseball collisions, religious hate speech, BBC funding, blasphemy, hip-hop censorship, and meat eating. The positive document usually shares the topic but presents the opposing position.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.2742, hit@10 of 0.6030, and recall@100 of 0.9548. BM25 can find same-topic arguments because long queries and documents share many content words.

The weakness is stance. A same-topic argument with the wrong argumentative role receives no credit. Term frequency does not know whether a passage supports, refutes, or reframes the query argument.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.3698, hit@10 of 0.7889, and recall@100 of 0.9447. Dense retrieval is the strongest early-ranking profile.

This suggests that embedding similarity captures argument-level semantics better than lexical overlap. It can connect a claim and a rebuttal even when the counterargument uses different wording or focuses on a different premise.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 4 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.3372, hit@10 of 0.7387, and recall@100 of 0.9799. Hybrid retrieval has the best recall@100 but is weaker than dense retrieval at the top ranks.

The pattern is useful for reranking. Sparse matching expands coverage across the same debate topic, while dense retrieval better orders the most relevant counterargument. A stance-aware reranker should benefit from the hybrid pool.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures how early the target counterargument appears, hit@10 measures whether it appears in the first ten candidates, and recall@100 measures reranker availability.

For `argu_ana_vn`, high recall can still include many same-topic wrong-stance candidates. A strong system should model rebuttal relation, not only topical similarity.

### Query and Relevance Type Tendencies

Queries and documents are long Vietnamese argument paragraphs. Relevant documents are counterarguments that oppose or challenge the query's stance. Candidate documents often share the same policy, ethical, or social topic.

Relevance is counterargument fit. A passage that agrees with the query or discusses the topic from a neutral angle is not the positive target.

### Representative Failure Modes

Common failures include retrieving same-stance arguments, matching broad topic terms without rebuttal, overranking arguments with shared examples, and missing translated paraphrases. BM25 is vulnerable to topic-only overlap; dense retrieval can still confuse opposition with relatedness.

### Training Data That May Help

Useful training data includes non-overlapping Vietnamese argument-counterargument pairs, translated ArguAna training material with test overlap removed, Vietnamese debate or stance-labeled forum data, and multilingual argument-mining corpora adapted to Vietnamese. Evaluation queries, positives, and qrels should be excluded.

### Model Improvement Notes

Models should encode stance, claim, premise, and rebuttal relation. Hard negatives should be same-topic arguments with the same or ambiguous stance. Dense retrieval is the best direct ranker, while hybrid retrieval is useful for high-recall reranking.

## Example Data

### Public Sources

- [Retrieval of the Best Counterargument without Prior Topic Knowledge](https://aclanthology.org/P18-1023/), task paper.
- [VN-MTEB: Vietnamese Massive Text Embedding Benchmark](https://aclanthology.org/2026.findings-eacl.86/), VN-MTEB paper.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), benchmark paper.
- [GreenNode/arguana-vn](https://huggingface.co/datasets/GreenNode/arguana-vn), source dataset card.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Retrieval of the Best Counterargument without Prior Topic Knowledge | 2018 | ACL paper | https://aclanthology.org/P18-1023/ |
| VN-MTEB: Vietnamese Massive Text Embedding Benchmark | 2026 | ACL paper | https://aclanthology.org/2026.findings-eacl.86/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| GreenNode/arguana-vn |  | dataset card | https://huggingface.co/datasets/GreenNode/arguana-vn |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| A Vietnamese argument defends personal autonomy in organ donation. | A counterargument emphasizes social obligations and medical ethics. |
| A claim says laboratory animals are generally treated well. | A counterargument says good housing does not remove pain during experiments. |
| A claim argues a third runway would increase noise and pollution. | A counterargument argues added runway capacity need not greatly increase noise pollution. |
| A claim says collisions are a traditional part of baseball. | A counterargument challenges whether collisions are as common or necessary as claimed. |
| A claim opposes restrictions on offensive religious speech. | A counterargument defends limits on harmful or hateful religious speech. |
