# NanoRARb / NanoTempReasonL3Context

## Overview

`NanoTempReasonL3Context` is an English temporal reasoning retrieval task from NanoRARb. The query contains a harder temporal question plus a very long context of dated facts, and the relevant document is the correct short answer. Each query has one positive. L3 questions often require before/after ordering over temporal states rather than only matching a date to an interval. Dense retrieval is the strongest profile, `reranking_hybrid` is close, and BM25 is weaker because lexical overlap alone cannot determine the correct temporal predecessor or successor.

## Details

### What the Original Data Measures

RAR-b reformulates TempReason temporal reasoning problems as retrieval. The underlying TempReason benchmark tests whether models can reason over time, including temporal ordering, duration, and entity-state changes.

The L3 context variant combines harder temporal relations with long supplied evidence. The query may ask for the holder of a role before or after another holder, or for the next entity in a dated sequence. The retriever must identify the relevant chain in a large context and retrieve the correct answer string.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Every query has one positive. Queries average 31,804.13 characters, while answer documents average 19.88 characters.

Examples ask who chaired Technical University of Munich before Wolfgang A. Herrmann, who led Romania before Alexandru G. Golescu, which parliamentary position Lord Douglas Gordon-Hallyburton held before a later Parliament, which employer Eduard Winkelmann joined after the Imperial University of Dorpat, and who led Romania after Adrian Nastase.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.0945, hit@10 of 0.1550, and recall@100 of 0.3600. BM25 benefits from repeated entity and role names in the long context, but its coverage and top-rank quality remain limited.

The difficulty is that the correct answer is not simply the fact with the highest word overlap. A predecessor or successor relation may be expressed through dates and sequence position, while many distractor facts share the same country, institution, person, or office vocabulary.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.1926, hit@10 of 0.3200, and recall@100 of 0.7600. Dense retrieval is the strongest standalone profile.

This result suggests that embedding similarity is better at connecting the question, relation, and relevant temporal context. The remaining gap is substantial: retrieving a semantically related answer is easier than determining the exact before-or-after state among nearby alternatives.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 54 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.1668, hit@10 of 0.3100, and recall@100 of 0.7300. Hybrid retrieval is close to dense retrieval but slightly lower on all reported metrics.

This indicates that sparse evidence helps anchor entities and relation terms, but it also brings in lexical distractors from the large context. Dense retrieval remains the better first-stage signal for this split, while hybrid retrieval is still a useful reranking pool.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures early ranking of the exact answer, hit@10 measures whether the answer is in the first ten candidates, and recall@100 measures whether a reranker can access the answer.

For this split, recall@100 is especially important because the correct answer is often near other temporally related entities. A strong reranker must inspect ordering relations, not only semantic similarity.

### Query and Relevance Type Tendencies

Queries combine a temporal question with a very long context of dated facts. Relevant documents are short answer strings, usually names, offices, institutions, or roles. The key signal is often a before/after relation within a timeline.

Relevance depends on temporal ordering. An entity from the same timeline is incorrect if it is not the immediate or specified predecessor or successor required by the question.

### Representative Failure Modes

Common failures include retrieving the anchor entity instead of the requested neighbor, choosing a non-adjacent holder from the same timeline, ranking a fact with stronger name overlap above the ordered answer, and losing the relevant chain inside the long context. BM25 is exposed to repeated terms; dense retrieval can still blur adjacent temporal states.

### Training Data That May Help

Useful training data includes timeline ordering QA, before/after retrieval pairs, long-context temporal reasoning, entity succession tasks, and hard negatives drawn from adjacent timeline entries. Evaluation facts, questions, answers, and qrels should be excluded.

### Model Improvement Notes

Models should learn to represent temporal order explicitly and distinguish anchor entities from requested answers. Hard negatives should use the same timeline and relation with wrong neighboring positions. Long-context compression and interval-aware ranking are both important for this task.

## Example Data

| Query | Positive document |
| --- | --- |
| Question: Who was the chair of Technical University of Munich before Wolfgang A. Herrmann? Facts: Otto Meitinger is the chair of Technical University of Munich from Jan, 1987 to Jan, 1995. Herbert Kupfer is the chair of Technical University of Munich from Jan, 1986 to Jan, 1987. Thomas F. Hofmann is the chair of Technical University of Munich from Sep, 2019 to Dec, 2022. Wolfgang A. Herrmann is the chair of Technical University of Munich from Jan, 1995 to Sep, 2019. Context: Technical University... [500 / 13,613 chars] | Otto Meitinger [14 chars] |
| Question: Who was the head of Romania before Alexandru G. Golescu? Facts: Gheorghe Tătărescu is the head of the government of Romania from Jan, 1934 to Dec, 1937. Adrian Năstase is the head of the government of Romania from Dec, 2000 to Dec, 2004. Manea Mănescu is the head of the government of Romania from Feb, 1974 to Mar, 1979. Petre S. Aurelian is the head of the government of Romania from Dec, 1896 to Apr, 1897. Ion Gheorghe Maurer is the head of the government of Romania from Mar, 1961 to F... [500 / 75,383 chars] | Dimitrie Ghica [14 chars] |
| Question: Which position did Lord Douglas Gordon-Hallyburton hold before Member of the 13th Parliament of the United Kingdom? Facts: Lord Douglas Gordon-Hallyburton holds the position of Member of the 11th Parliament of the United Kingdom from Dec, 1832 to Dec, 1834. Lord Douglas Gordon-Hallyburton holds the position of Member of the 13th Parliament of the United Kingdom from Jul, 1837 to Jun, 1841. Lord Douglas Gordon-Hallyburton holds the position of Member of the 10th Parliament of the United... [500 / 3,024 chars] | Member of the 12th Parliament of the United Kingdom [51 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | [https://arxiv.org/abs/2404.06347](https://arxiv.org/abs/2404.06347) |
| Towards Benchmarking and Improving the Temporal Reasoning Capability of Large Language Models | 2023 | arXiv paper | [https://arxiv.org/abs/2306.08952](https://arxiv.org/abs/2306.08952) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Who was the chair of Technical University of Munich before Wolfgang A. Herrmann? | Otto Meitinger. |
| Who was the head of Romania before Alexandru G. Golescu? | Dimitrie Ghica. |
| Which position did Lord Douglas Gordon-Hallyburton hold before Member of the 13th Parliament of the United Kingdom? | Member of the 12th Parliament of the United Kingdom. |
| Which employer did Eduard Winkelmann work for after Imperial University of Dorpat? | University of Bern. |
| Who was the head of Romania after Adrian Nastase? | Calin Popescu-Tariceanu. |
