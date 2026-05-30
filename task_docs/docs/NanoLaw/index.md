# NanoLaw

## Overview

NanoLaw is a compact legal retrieval group spanning English, German, and
Chinese legal data. It includes Indian precedent and statute retrieval, German
legal passage and QA retrieval, Chinese criminal-case retrieval,
LegalBench-derived consumer-contract and corporate-lobbying retrieval, and
plain-English contract-summary retrieval.

The group is useful because legal retrieval is not one search pattern. Some
tasks map long fact scenarios to cases or statutes. Others match contract
questions to clauses, bill descriptions to summaries, German questions to
judgments, or Chinese criminal cases to related cases. A model can be topically
close and still be wrong if it misses jurisdiction, legal role, statutory
function, contract obligation, procedural posture, or case analogy. BM25, dense
retrieval, and `reranking_hybrid` expose different legal matching behaviors.

## What This Group Measures

NanoLaw draws from several legal NLP resources rather than a single benchmark.
AILA-style tasks measure Indian legal assistance retrieval. GerDaLIR and
LegalQuAD measure German legal information access. LeCaRDv2 measures Chinese
legal case retrieval. LegalBench contributes consumer-contract and corporate
lobbying tasks, and LegalSummarization turns contract simplification into
summary-to-clause retrieval.

The shared measurement target is legal relevance. The positive document must
support the requested legal relation, not merely share broad topic terms. That
relation can be precedent analogy, statutory applicability, contractual right,
legislative policy match, or related-case reasoning.

## Task Families

- **Scenario to law:** `NanoAILACasedocs` and `NanoAILAStatutes` map long
  Indian legal fact patterns to cases or statutory provisions.
- **Long legal document retrieval:** `NanoGerDaLIRSmall`, `NanoLegalQuAD`, and
  `NanoLeCaRDv2` retrieve German or Chinese legal decisions and related cases.
- **Contract retrieval:** `NanoLegalBenchConsumerContractsQA` and
  `NanoLegalSummarization` retrieve clauses or snippets for consumer questions
  and simplified contract summaries.
- **Legislative retrieval:** `NanoLegalBenchCorporateLobbying` retrieves bill
  titles or summaries from policy descriptions.

## Dataset Shape

NanoLaw contains 8 task pages, 1,259 queries, 15,142 split-local documents, and
5,488 positive qrel rows. Relevance density varies sharply. AILA, LeCaRDv2, and
LegalSummarization are multi-positive, while the LegalBench and LegalQuAD tasks
are single-positive. `NanoLeCaRDv2` dominates the qrel count with many related
cases per query.

The text profile is broad. AILA and LeCaRDv2 queries are long legal narratives.
German legal documents can average around 19,000 characters. Contract and
legislative tasks are shorter but require precise clause or bill matching.
This makes NanoLaw both a legal reasoning benchmark and a long-document
retrieval benchmark.

## Retrieval Behavior

### BM25 Profile

BM25 is strongest when legal formulas, bill phrases, German legal terms, or
contract keywords repeat directly. It leads on `NanoGerDaLIRSmall` and
`NanoLegalQuAD`, and is very strong on corporate lobbying. This reflects the
importance of exact legal vocabulary, citations, and statutory phrasing.

BM25 is weaker on AILA scenario-to-law tasks because long fact patterns imply
statutory or precedent relevance without necessarily repeating the authority's
language. It can also over-rank contract or case documents that share topic
words but miss the decisive legal relation.

### Dense Profile

Dense retrieval helps with legal paraphrase and fact-to-authority mapping. It
improves both AILA tasks, consumer-contract QA, corporate lobbying, and
LegalSummarization. Dense retrieval is especially useful when the query is in
plain English or factual narrative form and the target is written in legal or
contractual language.

Dense retrieval is not always enough. German long-document tasks show that
exact legal terminology can outperform broad semantic matching. Legal retrieval
often requires preserving precise words, names, sections, and citations.

### Reranking Hybrid Profile

`reranking_hybrid` is best on `NanoLeCaRDv2`,
`NanoLegalBenchConsumerContractsQA`, and `NanoLegalSummarization`. These tasks
benefit from combining exact legal terms with semantic or analogical matching.
Hybrid is also useful where a reranker needs candidate diversity from both
sparse and dense retrieval.

For reranking, multi-positive legal tasks should be read with Recall@100 in
mind. A system that retrieves one plausible case or clause may still miss other
valid authorities.

## Task Summary

| Task | Retrieval focus | Lang | Queries | Docs | Positives | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [NanoAILACasedocs](NanoAILACasedocs.md) | legal fact pattern to precedent case | `en` | 50 | 186 | 195 | 0.2805 | 0.4003 | 0.3667 | Dense |
| [NanoAILAStatutes](NanoAILAStatutes.md) | legal fact pattern to statute | `en` | 50 | 82 | 217 | 0.2070 | 0.2711 | 0.2564 | Dense |
| [NanoGerDaLIRSmall](NanoGerDaLIRSmall.md) | German legal passage to judgment | `de` | 200 | 9,969 | 235 | 0.5911 | 0.2405 | 0.4287 | BM25 |
| [NanoLeCaRDv2](NanoLeCaRDv2.md) | Chinese criminal case to related cases | `zh` | 159 | 3,795 | 3,896 | 0.6528 | 0.6940 | 0.7225 | Reranking hybrid |
| [NanoLegalBenchConsumerContractsQA](NanoLegalBenchConsumerContractsQA.md) | contract question to clause | `en` | 200 | 153 | 200 | 0.7556 | 0.7785 | 0.8054 | Reranking hybrid |
| [NanoLegalBenchCorporateLobbying](NanoLegalBenchCorporateLobbying.md) | policy description to bill summary | `en` | 200 | 319 | 200 | 0.8955 | 0.9108 | 0.9068 | Dense |
| [NanoLegalQuAD](NanoLegalQuAD.md) | German legal question to judgment | `de` | 200 | 200 | 200 | 0.7420 | 0.5819 | 0.7043 | BM25 |
| [NanoLegalSummarization](NanoLegalSummarization.md) | plain-English summary to contract snippet | `en` | 200 | 438 | 345 | 0.5678 | 0.5861 | 0.6085 | Reranking hybrid |

## Interpretation Notes for Model Researchers

NanoLaw should be interpreted by jurisdiction and legal relation. English
contract retrieval, Indian scenario-to-law retrieval, German legal judgment
retrieval, and Chinese related-case retrieval have different relevance rules.
One overall score can hide whether a model is learning legal vocabulary,
jurisdiction-specific structure, or broader semantic analogy.

The BM25/dense split is instructive. BM25-led German tasks show the value of
exact legal terminology. Dense-led AILA tasks show fact-to-authority semantic
matching. Hybrid-led Chinese and contract tasks show that both exact legal
anchors and semantic relevance are needed for candidate generation.

## Training and Leakage Notes

Useful training data includes jurisdiction-specific case retrieval,
fact-to-statute retrieval, citation prediction, German legal QA, Chinese
related-case retrieval, consumer-contract QA, contract clause retrieval, and
legislative search. Hard negatives should share statutes, charges, agencies,
contract topics, or legal vocabulary while failing the decisive legal relation.

Exclude NanoLaw evaluation queries, positives, qrels, legal cases, statutes,
contract clauses, bill summaries, and direct synthetic variants. Legal datasets
often reuse public benchmark splits, so source and text-overlap audits are
necessary before training.

## Public Sources

- [Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance](https://ceur-ws.org/Vol-2517/T1-1.pdf), 2019.
- [LeCaRDv2: A Large-Scale Chinese Legal Case Retrieval Dataset](https://arxiv.org/abs/2310.17609), 2023.
- [LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models](https://arxiv.org/abs/2308.11462), 2023.

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance | 2019 | paper | https://ceur-ws.org/Vol-2517/T1-1.pdf |
| LeCaRDv2: A Large-Scale Chinese Legal Case Retrieval Dataset | 2023 | paper | https://arxiv.org/abs/2310.17609 |
| LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models | 2023 | paper | https://arxiv.org/abs/2308.11462 |
