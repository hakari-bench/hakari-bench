# NanoRTEB

## Overview

NanoRTEB is the Nano task group for the open English portion of RTEB, the
Retrieval Embedding Benchmark. It covers 14 retrieval tasks across legal,
finance, code, healthcare, and technical-document settings. The group is
intentionally heterogeneous: some tasks retrieve statutes or case law from long
legal fact patterns, some retrieve financial filing evidence, some retrieve code
or SQL from programming questions, and some retrieve medical or developer
support answers.

The group contains 2,390 queries, 33,864 task-local documents, and 9,150
positive qrel rows. It evaluates retrieval-first behavior across practical
domains rather than one academic task family. Models must handle long queries,
short queries, long documents, code snippets, SQL strings, tables, multi-positive
medical evidence, and enterprise-style technical search.

## What This Group Measures

RTEB focuses on realistic retrieval evaluation across law, healthcare, code, and
finance. NanoRTEB preserves that practical-domain mixture. Legal tasks retrieve
case law, statutes, and legal clauses. Finance tasks retrieve filing evidence,
financial answer passages, or table-backed numerical evidence. Code tasks
retrieve Python solutions, data-science code, or SQL queries. Healthcare tasks
retrieve patient responses or clinical evidence. FreshStack retrieves technical
documentation for developer questions.

Several tasks are repurposed from generation or QA datasets, so relevance is not
always ordinary passage similarity. A programming problem may retrieve an
implementation; a table question may retrieve SQL; a legal summary may retrieve
a clause; a clinical question may retrieve multiple biomedical passages. This
is the main value of the group for retrieval-model research.

## Task Families

- **Legal retrieval:** `NanoAILACasedocs`, `NanoAILAStatutes`, and
  `NanoLegalSummarization`.
- **Finance retrieval:** `NanoFinanceBench`, `NanoHC3Finance`, and
  `NanoFinQA`.
- **Code and structured-query retrieval:** `NanoApps`, `NanoDS1000`,
  `NanoHumanEval`, `NanoMBPP`, and `NanoWikiSQL`.
- **Healthcare retrieval:** `NanoChatDoctor` and `NanoCUREv1`.
- **Technical-document retrieval:** `NanoFreshStack`.

## Dataset Shape

All tasks are English. Query and document length vary substantially. AILA legal
queries are long fact patterns, while HC3Finance, MBPP, FinQA, and legal
summarization use much shorter queries. Code and WikiSQL tasks often have long
problem statements but short target code or SQL. AILA case documents are very
long; WikiSQL target documents are short SQL strings.

Positive density also varies. `NanoCUREv1` dominates the qrel count with 5,163
positives and 28.37 positives per query. `NanoFreshStack`, AILA, and legal
summarization are also multi-positive. Most code and finance splits are
single-positive, so exact top-rank retrieval matters more there.

## Retrieval Behavior

### BM25 Profile

BM25 is best only for `NanoFinQA`. That task often shares company names, years,
financial metrics, and table labels between the query and evidence, giving
sparse retrieval strong anchors. BM25 is also reasonable for `NanoCUREv1`,
`NanoLegalSummarization`, and `NanoWikiSQL`, where terminology or schema terms
often overlap with the target.

BM25 fails badly on code-generation-style retrieval. `NanoApps` has 0.0084
nDCG@10, and `NanoMBPP` has 0.0875, because problem statements and correct
implementations share little surface text. Long legal and technical-document
tasks also show that finding one overlapping term is not enough; ranking the
right precedent, provision, or document requires more than token frequency.

### Dense Profile

Dense retrieval with `harrier-oss-270m` is the strongest group-level profile at
0.5764 nDCG@10. It is best for most single-answer semantic or code tasks,
including `NanoApps`, `NanoChatDoctor`, `NanoDS1000`, `NanoFinanceBench`,
`NanoHC3Finance`, `NanoMBPP`, and `NanoWikiSQL`. The gains on code and SQL are
large, especially for MBPP and WikiSQL, where dense similarity can connect a
natural-language task to an implementation or query.

Dense is not uniformly best. It trails BM25 on `NanoFinQA`, where exact
financial evidence terms are highly useful, and trails hybrid on several
multi-positive or evidence-heavy tasks. Still, dense retrieval is the best
single profile for the group because many NanoRTEB tasks require semantic
matching beyond exact lexical overlap.

### Reranking Hybrid Profile

The reranking hybrid profile is best for `NanoCUREv1`, `NanoFreshStack`,
`NanoHumanEval`, and `NanoLegalSummarization`, and it has the best group-level
recall@100. These tasks benefit from combining exact anchors with semantic
matching: biomedical terms plus clinical meaning, documentation terms plus
developer intent, function identifiers plus code behavior, and legal vocabulary
plus clause meaning.

Hybrid is less effective than dense on APPS, MBPP, WikiSQL, and FinanceBench,
where sparse evidence can add noise to a strong semantic or structured-code
signal. The group therefore supports task-aware retrieval design: dense is a
strong default, hybrid is useful for evidence-rich and multi-positive tasks,
and BM25 remains important for highly lexical financial evidence.

## Task Summary

| Task | Family | Language | Queries | Docs | Positives | Positives/query | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [NanoAILACasedocs](NanoAILACasedocs.md) | Legal precedent retrieval | `en` | 50 | 186 | 195 | 3.90 | 0.2805 | 0.4003 | 0.3667 | Dense |
| [NanoAILAStatutes](NanoAILAStatutes.md) | Statute retrieval | `en` | 50 | 82 | 217 | 4.34 | 0.2070 | 0.2711 | 0.2564 | Dense |
| [NanoApps](NanoApps.md) | Code retrieval | `en` | 200 | 8,754 | 200 | 1.00 | 0.0084 | 0.2528 | 0.1655 | Dense |
| [NanoCUREv1](NanoCUREv1.md) | Clinical evidence retrieval | `en` | 182 | 10,000 | 5,163 | 28.37 | 0.5102 | 0.5479 | 0.5688 | Reranking hybrid |
| [NanoChatDoctor](NanoChatDoctor.md) | Medical answer retrieval | `en` | 200 | 5,545 | 200 | 1.00 | 0.2952 | 0.5533 | 0.4671 | Dense |
| [NanoDS1000](NanoDS1000.md) | Data-science code retrieval | `en` | 200 | 997 | 200 | 1.00 | 0.4424 | 0.6835 | 0.6053 | Dense |
| [NanoFinQA](NanoFinQA.md) | Financial evidence retrieval | `en` | 200 | 380 | 200 | 1.00 | 0.7330 | 0.6051 | 0.7309 | BM25 |
| [NanoFinanceBench](NanoFinanceBench.md) | Filing evidence retrieval | `en` | 150 | 145 | 150 | 1.00 | 0.4267 | 0.7694 | 0.6613 | Dense |
| [NanoFreshStack](NanoFreshStack.md) | Technical-document retrieval | `en` | 200 | 3,770 | 1,522 | 7.61 | 0.2768 | 0.3396 | 0.3482 | Reranking hybrid |
| [NanoHC3Finance](NanoHC3Finance.md) | Finance answer retrieval | `en` | 200 | 415 | 200 | 1.00 | 0.3079 | 0.4654 | 0.4177 | Dense |
| [NanoHumanEval](NanoHumanEval.md) | Code retrieval | `en` | 158 | 158 | 158 | 1.00 | 0.3405 | 0.5666 | 0.5770 | Reranking hybrid |
| [NanoLegalSummarization](NanoLegalSummarization.md) | Legal clause retrieval | `en` | 200 | 438 | 345 | 1.72 | 0.5678 | 0.5861 | 0.6085 | Reranking hybrid |
| [NanoMBPP](NanoMBPP.md) | Code retrieval | `en` | 200 | 972 | 200 | 1.00 | 0.0875 | 0.7599 | 0.2305 | Dense |
| [NanoWikiSQL](NanoWikiSQL.md) | Text-to-SQL retrieval | `en` | 200 | 2,022 | 200 | 1.00 | 0.4898 | 0.9507 | 0.7763 | Dense |

## Interpretation Notes for Model Researchers

NanoRTEB is best interpreted by domain and target type. Code and SQL tasks
strongly favor dense retrieval. Multi-positive clinical, legal, and technical
documentation tasks often benefit from hybrid candidate generation. Finance
evidence can remain highly lexical. A single aggregate score can hide whether a
model is improving code retrieval, financial filing retrieval, legal search, or
healthcare evidence retrieval.

The group is also sensitive to memorization. Several code datasets have exact
solutions; legal and finance tasks have small document pools; CURE and
FreshStack include many positives. Per-task inspection and leakage audits matter
when using NanoRTEB for model comparison.

## Training and Leakage Notes

Useful training data includes legal precedent and statute retrieval, contract
clause retrieval, SEC filing evidence retrieval, table QA retrieval,
problem-to-code and docstring-to-code pairs, text-to-SQL examples, clinical
evidence retrieval, patient-question-to-answer ranking, and developer
documentation retrieval. Multi-positive tasks should retain multiple support
documents when possible.

Leakage control should exclude NanoRTEB evaluation queries, qrels, positive
documents, exact code solutions, SQL targets, legal clauses, financial tables,
and near-duplicate source records. For code tasks, exact solution memorization
is a serious risk; for legal, finance, and healthcare tasks, passage overlap can
inflate scores without improving retrieval generalization.

## Public Sources

- [Introducing RTEB: A New Standard for Retrieval Evaluation](https://huggingface.co/blog/rteb), 2025.
- [Overview of the FIRE 2019 AILA Track](https://ceur-ws.org/Vol-2517/T1-1.pdf), 2019.
- [Plain English Summarization of Contracts](https://aclanthology.org/W19-2201/), 2019.
- [FinanceBench](https://arxiv.org/abs/2311.11944), 2023.

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| Introducing RTEB: A New Standard for Retrieval Evaluation | 2025 | benchmark page | https://huggingface.co/blog/rteb |
| Overview of the FIRE 2019 AILA Track | 2019 | source task paper | https://ceur-ws.org/Vol-2517/T1-1.pdf |
| Plain English Summarization of Contracts | 2019 | source task paper | https://aclanthology.org/W19-2201/ |
| FinanceBench | 2023 | source task paper | https://arxiv.org/abs/2311.11944 |
