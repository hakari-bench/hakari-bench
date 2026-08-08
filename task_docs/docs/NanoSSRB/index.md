# NanoSSRB

## Overview

NanoSSRB is HAKARI-Bench's compact evaluation of natural-language retrieval
over semi-structured JSON records. It derives from SSRB, the Semi-Structured
Retrieval Benchmark introduced at NeurIPS 2025. The source benchmark contains
about 14 million objects from 99 schemas across six domains and 8,485 test
queries. NanoSSRB preserves those six domains as separate 200-query tasks with
10,000 documents each. Queries mix exact constraints—names, dates, numeric
ranges, categories, and required fields—with fuzzy requirements such as
quality, suitability, risk, or expertise. A model must retrieve an entire JSON
object that satisfies the combined request rather than merely find a passage
about the same topic.

## What This Group Measures

The [SSRB paper](https://papers.neurips.cc/paper_files/paper/2025/hash/631bbd89466337712564872840a401be-Abstract-Datasets_and_Benchmarks_Track.html)
frames neural retrieval as a unified interface to heterogeneous semi-structured
collections. NanoSSRB tests whether a retriever can preserve field-value
relationships, compare numbers and dates, follow conjunctions and exclusions,
and still understand semantic conditions expressed without exact field values.
It differs from ordinary passage retrieval because topical similarity is not
enough: a near-match that violates one required constraint is a hard negative.

## Task Families

- [Academic](Academic.md): grants, researchers, publications, collaborations,
  events, and other academic records.
- [FinanceAndEconomics](FinanceAndEconomics.md): transactions, banking, markets,
  insurance, risk, budgets, and economic indicators.
- [HumanResources](HumanResources.md): employees, roles, payroll, benefits,
  feedback, policies, and workplace activity.
- [LLMAgentAndTool](LLMAgentAndTool.md): agents, tools, API requests, model runs,
  sessions, security events, and capability records.
- [ProductSearch](ProductSearch.md): products and services selected through
  attributes, price, availability, ratings, and semantic preferences.
- [ResumeSearch](ResumeSearch.md): candidates selected through experience,
  skills, education, certifications, availability, and role requirements.

## Dataset Shape

| Task | Queries | Documents | Positive qrels | Main retrieval challenge |
| --- | ---: | ---: | ---: | --- |
| Academic | 200 | 10,000 | 600 | entities, dates, funding, research fields |
| FinanceAndEconomics | 200 | 10,000 | 601 | numeric thresholds, currency, time, risk |
| HumanResources | 200 | 10,000 | 578 | policy and employee constraints across nested fields |
| LLMAgentAndTool | 200 | 10,000 | 600 | tool capability, runtime, endpoint, and security filters |
| ProductSearch | 200 | 10,000 | 600 | attribute conjunctions plus subjective suitability |
| ResumeSearch | 200 | 10,000 | 647 | evidence distributed across long candidate records |

## Retrieval Behavior

BM25 is useful when queries repeat brands, identifiers, endpoints, skills, or
field values, but its candidate recall is weakest on finance and HR. The
Harrier dense candidate set improves nDCG@10 in five of six domains and gives
the strongest top-ten profile for Academic and ProductSearch. Reranking hybrid
has the best candidate recall on HR, ProductSearch, and ResumeSearch and the
best nDCG@10 on HR, LLM Agent and Tool, and ResumeSearch. These patterns make
NanoSSRB useful for diagnosing whether a model understands constraints, not
only whether it embeds a domain topic correctly.

## Interpretation Notes for Model Researchers

Read nDCG@10 as top-rank constraint satisfaction and Recall@100 as first-stage
coverage. A high semantic score with low exact-filter accuracy suggests that a
model retrieves plausible domain neighbors but ignores a date, numeric bound,
negation, or required nested value. Because each query usually has about three
positives, a useful candidate list may still miss some valid objects. Compare
the six domains separately: schema vocabulary, record length, and the balance
between exact and fuzzy conditions differ substantially.

## Training and Leakage Notes

SSRB is synthetically constructed with LLM generation and LLM-assisted
relevance judging, with human evaluation used to validate the judgments.
Training pipelines must exclude NanoSSRB evaluation queries, qrels, positive
objects, and transformed copies of the same source records. Report exposure to
`vec-ai/struct-ir`, SSRB training data, or synthetic data seeded from SSRB test
objects. Safer training data can be generated from independent schemas and
objects while preserving explicit field grounding and difficult
constraint-violating negatives.

## Public Sources

- [SSRB: Direct Natural Language Querying to Massive Heterogeneous Semi-Structured Data](https://papers.neurips.cc/paper_files/paper/2025/hash/631bbd89466337712564872840a401be-Abstract-Datasets_and_Benchmarks_Track.html), NeurIPS 2025 Datasets and Benchmarks Track.
- [vec-ai/struct-ir source dataset](https://huggingface.co/datasets/vec-ai/struct-ir).
- [hakari-bench/NanoSSRB](https://huggingface.co/datasets/hakari-bench/NanoSSRB).
