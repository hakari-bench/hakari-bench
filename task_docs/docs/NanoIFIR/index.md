# NanoIFIR

## Overview

NanoIFIR is the compact Nano subset of IFIR, an instruction-following retrieval
benchmark for expert-domain search. It covers legal retrieval, clinical
decision support, finance QA, medical and nutrition retrieval,
precision-medicine trial matching, and scientific-evidence retrieval. The
queries are often instructions, fact patterns, or case descriptions rather than
plain keyword searches.

The group is useful because a topically related document can still be wrong. A
legal result must satisfy the precedent need, a clinical result must match the
patient or decision context, a precision-medicine result must satisfy trial
eligibility, and a scientific result must provide evidence for the claim.
BM25 exposes when expert terminology is enough; dense retrieval tests semantic
and instruction-following alignment; `reranking_hybrid` shows where exact
domain anchors and semantic constraints recover complementary candidates.

## What This Group Measures

[IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval](https://aclanthology.org/2025.naacl-long.511/)
introduces retrieval tasks where expert-domain instructions matter. NanoIFIR
samples seven task families from that setting: AILA-style legal retrieval,
clinical decision support, FiQA, FIRE legal retrieval, NFCorpus,
precision-medicine patient-to-trial retrieval, and SciFact.

The shared measurement target is instruction-sensitive expert retrieval. The
model must not only identify the topic but also respect the requested evidence
type, domain constraint, patient profile, legal issue, or scientific claim.

## Task Families

- **Legal retrieval:** `NanoIFIRAila` and `NanoIFIRFire` use long fact patterns
  or case summaries and retrieve relevant judgments or precedents.
- **Clinical and biomedical retrieval:** `NanoIFIRCds`, `NanoIFIRNFCorpus`, and
  `NanoIFIRPm` retrieve biomedical evidence, health information, or clinical
  trials.
- **Finance retrieval:** `NanoIFIRFiQA` retrieves personal-finance advice or
  answer passages.
- **Scientific evidence retrieval:** `NanoIFIRScifact` retrieves abstracts that
  support or refute scientific claims.

## Dataset Shape

NanoIFIR contains 7 task pages, 637 queries, 48,246 split-local documents, and
3,872 positive qrel rows. Every task is multi-positive in the current metadata.
Precision medicine has the densest relevance set, averaging more than 20
positive clinical trials per query.

The group mixes very long expert queries with short user-style questions.
`NanoIFIRAila` and `NanoIFIRFire` have legal queries averaging thousands of
characters, while finance, NFCorpus, and SciFact queries are much shorter.
Documents are also long in the legal tasks, especially FIRE, where judgments or
case records can be tens of thousands of characters. This makes NanoIFIR a
joint test of domain expertise, long-text handling, and multi-positive ranking.

## Retrieval Behavior

### BM25 Profile

BM25 is strongest on `NanoIFIRScifact`, where scientific claims and evidence
abstracts often share domain terms. It is also useful on `NanoIFIRPm` and
`NanoIFIRFire`, helped by biomedical or legal vocabulary and multiple
positives. BM25 is weakest on `NanoIFIRAila`, where long legal fact patterns
and judgments require more than term overlap.

Sparse retrieval can find domain-near documents, but instruction satisfaction
is harder. A legal document can share many words and still be the wrong
precedent; a trial can share disease terms and still be ineligible.

### Dense Profile

Dense retrieval is the best profile for most NanoIFIR tasks. It improves
clinical decision support, finance, NFCorpus, and precision medicine by
matching the semantic constraints of the query. It is especially useful when
the answer passage or trial record does not repeat the user's wording.

Dense retrieval is not always enough. Legal retrieval remains hard because long
fact patterns and precedential relevance can be subtle, and SciFact shows that
exact scientific terms can still be decisive.

### Reranking Hybrid Profile

`reranking_hybrid` is strongest on `NanoIFIRFire`, `NanoIFIRPm`, and
`NanoIFIRScifact` in the current metadata. These tasks benefit from both exact
domain anchors and semantic evidence matching. In multi-positive expert
retrieval, the hybrid pool can be valuable even when dense has a slightly
higher nDCG@10, because candidate coverage affects reranker ceiling.

For reranker experiments, NanoIFIR should be evaluated with recall and listwise
ranking in mind. Finding one relevant document is not enough when a query has
many valid cases, papers, or trials.

## Task Summary

| Task | Retrieval focus | Queries | Docs | Positives | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [NanoIFIRAila](NanoIFIRAila.md) | legal fact pattern to prior case | 40 | 2,914 | 119 | 0.0988 | 0.0878 | 0.0798 | BM25 |
| [NanoIFIRCds](NanoIFIRCds.md) | clinical case to biomedical evidence | 42 | 10,000 | 466 | 0.2258 | 0.4073 | 0.3376 | Dense |
| [NanoIFIRFiQA](NanoIFIRFiQA.md) | finance question to advice passage | 200 | 10,000 | 1,010 | 0.3422 | 0.5328 | 0.4678 | Dense |
| [NanoIFIRFire](NanoIFIRFire.md) | legal case summary to precedent | 167 | 1,739 | 563 | 0.3566 | 0.3421 | 0.3996 | Reranking hybrid |
| [NanoIFIRNFCorpus](NanoIFIRNFCorpus.md) | health topic to medical research | 86 | 3,593 | 242 | 0.3338 | 0.4580 | 0.4108 | Dense |
| [NanoIFIRPm](NanoIFIRPm.md) | patient profile to clinical trial | 59 | 10,000 | 1,217 | 0.4232 | 0.5448 | 0.5468 | Reranking hybrid |
| [NanoIFIRScifact](NanoIFIRScifact.md) | scientific claim to evidence abstract | 43 | 10,000 | 255 | 0.8682 | 0.8516 | 0.9055 | Reranking hybrid |

## Interpretation Notes for Model Researchers

NanoIFIR should be read as an expert retrieval and instruction-following
benchmark. The model has to satisfy the retrieval instruction, not merely find
the same topic. This is most visible in legal and clinical tasks, where the
wrong precedent or wrong trial can look lexically similar.

Because every task is multi-positive, nDCG@10 and Recall@100 are more
informative than hit@10 alone. High hit@10 can hide poor ranking of the broader
evidence set. Compare BM25, dense, and hybrid profiles by domain: legal,
clinical, finance, and scientific retrieval have different failure modes.

## Training and Leakage Notes

Useful training data includes IFIR-style instruction-query retrieval pairs,
legal case retrieval, clinical decision support retrieval, FiQA-style finance
QA, NFCorpus-style medical search, precision-medicine patient-to-trial
matching, and SciFact claim-evidence pairs. Training objectives should preserve
multiple relevant documents per query.

Exclude NanoIFIR evaluation queries, positives, qrels, legal cases, clinical
trials, scientific abstracts, and direct synthetic variants. Expert-domain
datasets are often reused across benchmarks, so source split and text-overlap
audits are important before training.

## Public Sources

- [IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval](https://aclanthology.org/2025.naacl-long.511/), 2025.
- [Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance](https://ceur-ws.org/Vol-2517/T1-1.pdf), 2019.

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval | 2025 | paper | https://aclanthology.org/2025.naacl-long.511/ |
| Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance | 2019 | paper | https://ceur-ws.org/Vol-2517/T1-1.pdf |
