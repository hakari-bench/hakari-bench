# NanoIFIR / NanoIFIRAila

## Overview

`NanoIFIRAila` is an English legal instruction-following retrieval task in NanoIFIR. The queries are long legal fact patterns adapted from AILA-style Indian Supreme Court case scenarios, and the documents are full prior case judgments.

This task evaluates whether a retriever can find legally relevant precedents under a detailed information need. The relevant relation is not simple topical overlap: positives are prior cases that match the legal issue, factual posture, precedent value, or reasoning constraints implied by the query.

## Details

### What the Original Data Measures

IFIR introduces expert-domain instruction-following information retrieval across finance, law, healthcare, and scientific literature. It augments established expert-domain retrieval benchmarks with detailed instructions and domain-specific retrieval demands.

The legal source context is AILA, a FIRE legal assistance track over Indian Supreme Court material. AILA precedent retrieval gives a factual situation and asks systems to retrieve similar or relevant prior case documents. In `NanoIFIRAila`, this becomes a compact Nano split for testing long-query legal precedent retrieval.

### Observed Data Profile

This Nano split contains 40 queries, 2,914 documents, and 119 positive qrels. Queries have 2.98 positives on average, with a minimum of 1, a median of 2.0, and a maximum of 10. There are 30 multi-positive queries, or 75.0% of the split. Queries average 2,890.05 characters, and documents average 19,998.06 characters.

Observed queries are long legal narratives about appeals, detention, criminal proceedings, partnership dissolution, customs or export issues, arbitration, land acquisition, trial evidence, and procedural questions. Documents are long Indian Supreme Court judgments with citations, party names, procedural history, legal analysis, and holdings.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.0988, hit@10 of 0.2000, and recall@100 of 0.3361 with a top-500 candidate pool. Lexical retrieval is weak because both queries and documents are very long, and many legal terms recur across unrelated cases.

BM25 can help when a query and precedent share distinctive statute names, procedural phrases, or unusual facts. It struggles when the relevant connection is legal analogy, reasoning pattern, or precedent value rather than direct word repetition.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.0878, hit@10 of 0.2750, and recall@100 of 0.3950. Dense retrieval improves hit rate and recall over BM25, but its nDCG@10 is lower.

This suggests that dense retrieval finds more relevant prior cases somewhere in the candidate set, but does not reliably rank the best precedents at the top. Long legal documents and long fact-pattern queries may exceed the granularity that a general embedding model can represent cleanly.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.0798, hit@10 of 0.2000, and recall@100 of 0.4034. It uses 100 candidates per query, with 21 rank-101 safeguard positives.

Hybrid retrieval gives the highest recall@100 but the weakest top-10 ordering. This makes it more useful as a candidate pool than as a direct ranker. The large safeguard count shows that many positives are near the edge of the hybrid pool, so reranking depends heavily on candidate construction quality.

### Metric Interpretation for Model Researchers

`NanoIFIRAila` is a hard legal retrieval task. All top-10 scores are low, which indicates that generic lexical and dense retrieval signals do not capture the legal matching function well enough. Recall@100 is more encouraging than nDCG@10, especially for dense and hybrid profiles, but reranking remains essential.

Researchers should interpret this task as a test of legal analogy and long-context retrieval. A model that improves nDCG@10 here likely understands legal issue structure, material facts, procedural posture, and precedent similarity beyond surface terms.

### Query and Relevance Type Tendencies

Queries are long English legal fact patterns, often written like case summaries or retrieval instructions. Documents are full prior judgments from Indian Supreme Court material.

The relevance relation is precedent relevance. Positives may share a statute, issue, factual pattern, or legal principle with the query, but they are not necessarily lexically similar. Multiple prior cases may be relevant for a single query.

### Representative Failure Modes

BM25 may retrieve cases with overlapping legal vocabulary but different holdings or facts. Dense retrieval may retrieve broadly similar disputes while missing the controlling legal issue. Hybrid retrieval can improve coverage but still fails to rank the best precedents near the top.

Long document length creates another failure mode: a judgment may contain many unrelated procedural and factual sections, so a whole-document representation can dilute the relevant passage or legal principle.

### Training Data That May Help

Useful training data includes non-overlapping AILA precedent retrieval pairs, Indian Supreme Court citation graphs, legal case similarity datasets, same-statute hard negatives, and judgments labeled for issue-level or precedent-level similarity.

Training should exclude `NanoIFIRAila` queries, qrels, and positive prior-case documents.

### Model Improvement Notes

Improving this task likely requires legal-domain retrieval training and long-document handling. Models should represent legal issues, procedural posture, facts, statutes, and holdings separately rather than treating each judgment as a flat bag of text.

For reranking, a strong model should compare the query's legal issue and material facts against the precedent's reasoning and holding. Citation-aware training or issue-segment retrieval may help more than generic sentence similarity.

## Example Data

### Public Sources

This task is documented through the IFIR paper and the FIRE 2019 AILA track overview. The Nano split is published in `hakari-bench/NanoIFIR`.

### Source Reference Table

| Source | Role |
| --- | --- |
| [IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval](https://arxiv.org/abs/2503.04644) | Expert-domain instruction-following IR benchmark paper. |
| [Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance](https://ceur-ws.org/Vol-2517/T1-1.pdf) | Original AILA legal assistance track overview. |
| [hakari-bench/NanoIFIR](https://huggingface.co/datasets/hakari-bench/NanoIFIR) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A long appeal narrative asking whether distribution of partnership residue assets on dissolution requires registration. | A Supreme Court judgment about partnership dissolution, residue assets, and registration requirements. |
| A detention fact pattern involving a foreign airport manager, customs movement, and preventive detention. | A prior judgment about detention, procedural safeguards, and related constitutional review. |
| A criminal proceeding involving witness examination, conviction, and appeal-stage issues. | A judgment addressing criminal appellate procedure and evidentiary or witness-related questions. |
| A fact pattern about export licensing, company management, and detention or enforcement action. | A prior case involving industrial export activity, enforcement, and detention review. |
| An arbitration dispute involving objections to an award by a former judge appointed as sole arbitrator. | A judgment discussing arbitration award objections, misconduct, or review of arbitral reasoning. |
