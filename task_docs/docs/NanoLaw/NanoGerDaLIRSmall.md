# NanoLaw / NanoGerDaLIRSmall

## Overview

`NanoLaw / NanoGerDaLIRSmall` is a German legal information retrieval task based
on GerDaLIR. Queries are German legal passages, and documents are German court
decisions. The retrieval goal is to identify the cited or substantively linked
decision for a legal reasoning passage. The Nano split has 200 queries, 9,969
documents, and 235 positive qrel rows. Most queries have one positive, but 29
queries have multiple positives. Current diagnostics show a strongly lexical
legal retrieval profile: BM25 is the best top-10 ranker, `reranking_hybrid`
improves over dense and slightly improves recall@100 over BM25, while dense
retrieval alone is much weaker.

## Details

### What the Original Data Measures

The GerDaLIR paper introduces a German legal IR dataset built from Open Legal
Data. It constructs query-document relevance from legal passages that cite known
documents in the collection, and it emphasizes passage queries as a realistic
form of legal research. The MTEB GerDaLIRSmall card describes a smaller
evaluation corpus that keeps documents with corresponding queries.

The task measures passage-to-case retrieval. A query is not a short keyword
request; it is a legal reasoning passage that may contain statutes, doctrinal
phrases, anonymized dates, reference markers, and citation-like cues. The target
is a full German court decision, often much longer than the passage.

### Observed Data Profile

The Nano split contains 200 queries, 9,969 documents, and 235 positive qrel
rows. Positives per query average 1.175, with a minimum of 1, a median of 1,
and a maximum of 4. Multi-positive queries account for 14.5 percent of the
task. Query passages average 889.88 characters, while documents average
19,706.82 characters.

Observed texts include German legal reasoning, tenor sections, administrative
and constitutional-law language, tax and labor disputes, asylum-related
decisions, and civil-law passages. The data also contains anonymized placeholders
such as `[DATE]` and `[REF]`. This gives the benchmark a distinctive legal and
documentary texture: formulas, procedural terms, and citation patterns are part
of the retrieval signal.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.5911, hit@10 = 0.7550, and recall@100 = 0.8426. BM25 is
the strongest observed top-10 ranker. This indicates that exact German legal
vocabulary, statutory references, court phrases, and citation-adjacent language
are highly predictive in this task.

BM25's advantage also reflects the construction of GerDaLIR. If a query passage
is linked to a cited decision, surface cues around the citation, legal issue,
or statutory provision can overlap with the target judgment. The challenge is
not absent lexical evidence, but distinguishing the correct decision from other
long judgments that share the same legal domain.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.2405, hit@10 = 0.3850, and recall@100 = 0.6170.
Dense retrieval is much weaker than BM25. The gap suggests that the dense model
does not preserve enough German legal surface detail, citation structure, or
long-document specificity for this benchmark.

Dense similarity may find decisions in the same broad legal area, but that is
not enough. The relevant document is often a particular cited or substantively
linked case, and many decisions share doctrinal vocabulary. A dense retriever
that smooths over statute references, procedural formulas, or court-specific
language will rank related but wrong decisions too high.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 or 101 candidates per
query, with 28 safeguard positive rows and a mean of 100.14 candidates. It
achieves nDCG@10 = 0.4287, hit@10 = 0.6150, and recall@100 = 0.8553. Hybrid
retrieval improves substantially over dense retrieval and gives slightly better
top-100 coverage than BM25, but it does not match BM25's top-10 ranking.

This pattern indicates that dense evidence can broaden candidate coverage, but
exact lexical matching remains the dominant early-ranking signal. For reranking
experiments, the hybrid pool is useful because it preserves more positives, yet
a final model must still learn to respect German legal terms, reference
markers, and citation-like phrasing.

### Metric Interpretation for Model Researchers

This task is mostly single-positive but includes some multi-positive queries.
Hit@10 measures whether at least one relevant decision appears in the first ten
results. nDCG@10 rewards placing relevant decisions high, and recall@100
measures how much of the positive set remains available for reranking.

The metric pattern is clear: BM25 is the best final candidate ordering among
the observed profiles, hybrid is best for top-100 coverage, and dense retrieval
alone is weak. This makes `NanoGerDaLIRSmall` a strong diagnostic for whether a
model preserves legal surface form and citation-oriented evidence in German.

### Query and Relevance Type Tendencies

Queries are medium-length German legal passages, often taken from reasoning
contexts. They contain doctrinal statements, statute references, procedural
language, and anonymized references. Relevant documents are full court
decisions with tenor, facts, and reasons.

The retrieval relation is closer to citation or legal support retrieval than to
general semantic search. The model must find the case document that the passage
points to or substantively depends on. This favors systems that combine exact
legal vocabulary with document-level legal relevance.

### Representative Failure Modes

BM25 can fail when many decisions share the same statutory provisions, court
terms, or procedural formulas. Dense retrieval can fail more broadly by finding
same-domain legal decisions that are semantically related but not the cited or
linked case. Hybrid retrieval can keep both the positive and close negatives,
leaving a hard reranking problem.

Long documents add another difficulty. The relevant cue may correspond to a
small part of a judgment, while the rest of the decision covers broader facts
and reasoning. Single-vector document representations may not capture that
specific link.

### Training Data That May Help

Useful training data includes German legal citation retrieval, passage-to-case
retrieval pairs, German court decision corpora, and hard negatives from cases
sharing the same statute, court, or legal domain. Training should include long
documents and passage-level queries rather than only short legal keywords.

For comparable evaluation, training should exclude NanoGerDaLIRSmall queries,
qrels, and target German case documents. Synthetic data can help when it
generates German legal passages with citation cues and pairs them with full
judgments, while using same-statute cases as hard negatives.

### Model Improvement Notes

Dense retrievers need stronger German legal-domain representations and better
retention of citation-like details, placeholders, statutory references, and
procedural formulas. Sparse systems benefit from careful German legal
tokenization and weighting of section references and legal compounds. Rerankers
should inspect whether the candidate decision is the specific cited or
supporting decision, not just whether it is topically similar.

For hybrid systems, this task argues for keeping BM25 as a primary component.
Dense evidence can improve coverage, but top-rank quality depends heavily on
lexical and citation-oriented signals.

## Example Data

Representative queries include German passages about dispute value setting,
immediate enforceability, notarial estate inventories, salary-law amendments,
and comparable civil-service evaluations. Positive documents are full German
court decisions containing tenor and reasons, often with anonymized dates and
reference markers.

### Public Sources

- [GerDaLIR: A German Dataset for Legal Information Retrieval](https://aclanthology.org/2021.nllp-1.13/),
  2021.
- [GerDaLIR GitHub repository](https://github.com/lavis-nlp/GerDaLIR), source
  repository.
- [mteb/GerDaLIRSmall](https://huggingface.co/datasets/mteb/GerDaLIRSmall),
  MTEB source dataset.
- [hakari-bench/NanoLaw](https://huggingface.co/datasets/hakari-bench/NanoLaw),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| GerDaLIR: A German Dataset for Legal Information Retrieval | 2021 | ACL paper | https://aclanthology.org/2021.nllp-1.13/ |
| GerDaLIR | 2021 | GitHub repository | https://github.com/lavis-nlp/GerDaLIR |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A German passage discussing dispute value setting under procedural cost provisions. | A court decision whose tenor and reasons address the same dispute value issue. |
| A passage about the written justification for immediate enforceability. | An administrative court decision concerning suspensive effect and immediate enforcement. |
| A passage about a notarial estate inventory and an information obligation. | A family or civil-law decision involving the same estate-inventory issue. |
| A passage about salary-law redesign and performance principles. | A long constitutional or administrative decision addressing the salary-law question. |
| A passage about whether evaluations are substantially equal overall. | A decision or order concerning civil-service evaluation and legal value setting. |
