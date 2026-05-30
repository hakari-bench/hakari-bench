# NanoMMTEB-v2 / ailastatutes

## Overview

`NanoMMTEB-v2 / ailastatutes` is an English legal statute-retrieval task from
AILA 2019. Each query is a long Indian legal fact pattern, and the retriever
must return the statutory provisions that apply to the situation. The Nano split
has 50 queries, 82 statute documents, and 217 positive qrel rows. Every query
has multiple positives, averaging 4.34 applicable statutes. Current diagnostics
show dense retrieval as the strongest top-rank profile, `reranking_hybrid` close
behind, and BM25 weaker because legal relevance is often implied by facts,
procedure, and legal effect rather than repeated statute wording.

## Details

### What the Original Data Measures

The FIRE 2019 AILA track introduced Artificial Intelligence for Legal
Assistance tasks for Indian legal materials. The statute retrieval task gives
systems factual legal scenarios and asks them to identify relevant statutory
provisions from a pool of frequently cited provisions. The Zenodo release and
the MTEB dataset packaging expose this as a retrieval benchmark for embedding
evaluation.

This task measures legal issue spotting and fact-to-statute retrieval. A model
must connect facts such as conviction, appeal, dowry death, conspiracy,
registration, public servant status, or evidence rules to the statute text that
governs the legal issue.

### Observed Data Profile

The Nano split contains 50 long scenario queries, 82 statute documents, and 217
positive qrel rows. Every query has multiple positives: the average is 4.34
positives per query, with a minimum of 2, median of 4.5, and maximum of 5.
Queries average 3,038.42 characters, while statute documents average 1,972.63
characters.

The queries are legal narratives or case summaries, often much longer than the
documents. The documents usually contain a statute title and provision text.
Examples include attempt to murder, dowry death, criminal conspiracy,
compulsory registration of documents, and legal exceptions or procedural
provisions.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains all 82 documents per query
and achieves nDCG@10 = 0.2070, hit@10 = 0.6600, and recall@100 = 1.0000. Since
the corpus has only 82 documents, recall@100 is saturated by every candidate
subset and should not be read as evidence of strong ranking quality.

BM25 is the weakest top-rank profile. Long fact patterns contain many narrative
terms, party names, dates, procedural history, and case-specific facts that do
not necessarily appear in the statute text. Relevant provisions may be implied
by legal effect rather than direct word overlap.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains all 82 documents per
query and achieves nDCG@10 = 0.2725, hit@10 = 0.7600, and recall@100 = 1.0000.
Dense retrieval is the strongest observed top-rank profile for this task.

This pattern fits the benchmark: the model benefits from semantic similarity
between legal facts and statute concepts. A scenario about death soon after
marriage, a criminal appeal, public-servant sanction, or property registration
may not repeat exact section language, but it is semantically tied to the
applicable provision.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset also contains all 82 documents per
query and achieves nDCG@10 = 0.2557, hit@10 = 0.7400, and recall@100 = 1.0000.
It is stronger than BM25 but slightly below dense retrieval.

Because every profile sees the entire statute pool, `reranking_hybrid` should
be interpreted as a ranking diagnostic rather than a candidate-coverage test.
The hybrid signal helps over pure lexical matching, but dense semantic matching
appears to better capture the scenario-to-statute relationship in this small
legal corpus.

### Metric Interpretation for Model Researchers

This is a multi-positive task. Each fact pattern can require several statutory
provisions, and nDCG@10 rewards ordering many positives high in the result list.
Hit@10 only indicates whether at least one relevant statute is retrieved near
the top, so it is less informative than nDCG@10 for complete legal coverage.

Recall@100 is saturated because the corpus has only 82 documents. For this
task, ranking quality within the full candidate set is the meaningful signal.
Researchers should look for models that rank all applicable provisions above
adjacent but legally inapplicable sections.

### Query and Relevance Type Tendencies

Queries are long English legal fact patterns from Indian case contexts. They
often describe appeals, convictions, evidentiary questions, marriage-related
death, public office, conspiracy, registration, partnership dissolution, or
procedural requirements. The wording is narrative and case-specific.

Relevant documents are statute provisions. They are shorter than the queries
and use formal legal language. Applicability depends on matching legal
conditions, roles, procedures, remedies, or elements of an offense rather than
matching only surface terms.

### Representative Failure Modes

BM25 can over-rank statutes sharing broad legal words such as offence,
punishment, evidence, appeal, property, or registration while missing the
specific legal element. Dense retrieval can retrieve a semantically related
statute that fails on a condition such as timing, jurisdiction, public-servant
status, intent, or remedy.

Hybrid retrieval can inherit both problems: lexical overlap may pull in adjacent
sections, while semantic similarity may blur closely related legal doctrines.
Rerankers should compare the fact pattern against clause-level statutory
conditions.

### Training Data That May Help

Useful training data includes fact-to-statute retrieval pairs, statutory legal
entailment data, legal issue spotting examples, and adjacent statute hard
negatives. Training should preserve the multi-positive structure because
several provisions can apply to one scenario.

Synthetic data can generate realistic legal fact patterns and match them to
several statute-like provisions. Negatives should share legal vocabulary but
fail on a material element such as jurisdiction, procedure, remedy, detention
status, mental state, or evidentiary rule. Evaluation scenarios and positive
statutes from this Nano split should be excluded from training.

### Model Improvement Notes

Dense retrievers should be trained for legal entailment and issue spotting, not
only generic semantic similarity. Sparse systems may improve by emphasizing
statute titles, legal terms of art, and clause-level concepts while reducing
noise from long narrative facts. Rerankers should parse the scenario into legal
issues and compare those issues against statute conditions.

For hybrid systems, `NanoMMTEB-v2 / ailastatutes` is a small-corpus ranking
test. Candidate coverage is trivial, so improvements must come from ranking
multiple applicable provisions above near-miss legal sections.

## Example Data

Representative queries describe criminal appeals, dowry death convictions,
questions about the effect of another Act, sanction for criminal proceedings,
and whether distribution of partnership assets requires registration. Positive
documents are statute provisions such as attempt to murder, dowry death,
criminal conspiracy, compulsory registration, or other applicable legal rules.

### Public Sources

- [Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance](https://ceur-ws.org/Vol-2517/T1-1.pdf),
  2019.
- [AILA 2019 Precedent & Statute Retrieval Task](https://zenodo.org/records/4063986).
- [mteb/AILA_statutes](https://huggingface.co/datasets/mteb/AILA_statutes).
- [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance | 2019 | task paper | https://ceur-ws.org/Vol-2517/T1-1.pdf |
| AILA 2019 Precedent & Statute Retrieval Task | 2020 | dataset release | https://zenodo.org/records/4063986 |
| mteb/AILA_statutes | 2024 | dataset card | https://huggingface.co/datasets/mteb/AILA_statutes |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A long appeal scenario involving conviction and life imprisonment. | A statute provision titled "Attempt to murder." |
| A scenario about death of a woman after marriage and criminal conviction. | A statute provision titled "Dowry death." |
| A scenario about whether another Act affects punishment provisions. | A statute provision preserving certain laws from being affected. |
| A scenario about sanction before criminal proceedings. | A statute provision about punishment of criminal conspiracy or related procedure. |
| A scenario about partnership assets and compulsory registration. | A statute provision on documents requiring registration. |
