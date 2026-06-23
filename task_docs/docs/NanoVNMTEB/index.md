# NanoVNMTEB

## Overview

NanoVNMTEB is the Nano task group for VN-MTEB retrieval. It contains Vietnamese
retrieval versions of widely used MTEB and BEIR-style tasks, including
duplicate question retrieval, fact-checking evidence retrieval, web search,
natural question answering, finance QA, argument retrieval, biomedical
retrieval, and scientific-paper retrieval. The group evaluates Vietnamese
retrieval quality and robustness to translated benchmark artifacts.

The group contains 4,768 queries, 247,475 task-local documents, and 24,671
positive qrel rows across 26 tasks. Most tasks are Vietnamese, while
`nfcorpus_vn` is marked multilingual because biomedical terminology and
translation artifacts cross language boundaries. The group is large enough that
aggregate scores can hide very different retrieval relations.

## What This Group Measures

VN-MTEB translates and filters English MTEB datasets into Vietnamese while
preserving named entities, numbers, links, special characters, fluency, and
meaning. NanoVNMTEB focuses on the retrieval family from that benchmark. A high
score means that a model can preserve the original retrieval relation after
Vietnamese translation, whether the relation is duplicate intent, evidence
support, web answerability, scientific relatedness, argument stance, or
biomedical relevance.

The group should not be read as one native Vietnamese corpus. Many tasks inherit
their semantics from English benchmark sources. This makes it valuable for
testing multilingual and translation-robust retrievers, but it also means that
source-task shape matters as much as Vietnamese language quality.

## Task Families

- **Duplicate and paraphrase retrieval:** ten CQADupStack splits plus
  `quora_vn` retrieve duplicate or equivalent questions.
- **Fact-checking and evidence retrieval:** `fever_vn`, `nano_fever`,
  `climate_fever_vn`, and `sci_fact_vn` retrieve evidence for claims.
- **Open-domain and web QA retrieval:** `msmarco_vn`, `nq_vn`, `nano_nq`, and
  `hotpot_qa_vn` retrieve answer-bearing passages.
- **Argument retrieval:** `argu_ana_vn` retrieves counterarguments and
  `touche2020_vn` retrieves argumentative passages.
- **Domain retrieval:** `fi_qa2018_vn`, `nfcorpus_vn`, and `treccovid_vn` cover
  finance, biomedical literature, and COVID-19 evidence.
- **Entity and scholarly retrieval:** `dbpedia_vn` retrieves entity articles,
  and `scidocs_vn` retrieves related scientific papers.

## Dataset Shape

Most splits have 200 queries and 10,000 candidate documents. Smaller exceptions
include `sci_fact_vn`, `nfcorpus_vn`, `touche2020_vn`, and `treccovid_vn`.
Positive density varies sharply. ArguAna is single-positive. Many FEVER, NQ,
and MS MARCO-style tasks are close to single-positive. DBpedia, NFCorpus,
Touché, TREC-COVID, and several duplicate-question tasks are strongly
multi-positive.

The group average is 5.17 positives per query, but that average is driven by
large relevance sets in DBpedia, NFCorpus, Touché, and TREC-COVID. The median
task behavior is closer to one or two positives per query. Query length also
varies: `argu_ana_vn` uses long translated debate arguments, while MS MARCO,
NQ, and many CQADupStack queries are short search or question strings.

## Retrieval Behavior

### BM25 Profile

BM25 is best for `quora_vn` and remains strong on entity-heavy and fact-like
tasks. `fever_vn`, `nano_fever`, `hotpot_qa_vn`, `msmarco_vn`, and `quora_vn`
all score high because translated named entities, titles, and short duplicate
phrases often preserve lexical overlap. BM25 also works reasonably on many
CQADupStack domains when technical terms, code fragments, product names, or
StackExchange terminology survive translation.

BM25 is weak on tasks where the source relevance relation is not lexical.
`scidocs_vn` has low nDCG@10 because related scientific papers may not share
title words. `climate_fever_vn`, `argu_ana_vn`, and several CQADupStack domains
also require evidence, stance, or duplicate intent beyond topical overlap.
`treccovid_vn` has many positives, but BM25 nDCG@10 is modest because broad
COVID terminology does not rank the best judged literature records early.

### Dense Profile

Dense retrieval with `harrier-oss-270m` is the strongest group-level profile.
It is best for most tasks, including argument retrieval, climate evidence,
DBpedia, FEVER, MS MARCO, NQ, SciFact, and many duplicate-question domains. The
large gains on `msmarco_vn`, `nano_nq`, `nq_vn`, and `fever_vn` show that
Vietnamese embedding similarity helps connect translated questions and claims
to answer-bearing or evidence passages.

Dense is not always best. `quora_vn` slightly favors hybrid, and some technical
duplicate tasks favor hybrid because exact tokens and semantic intent are both
important. Still, dense retrieval is the main profile for VN-MTEB-style
Vietnamese translation robustness.

### Reranking Hybrid Profile

The reranking hybrid profile is best for several tasks where exact tokens and
semantic relatedness both matter: `cqadupstack_mathematica_vn`,
`cqadupstack_stats_vn`, `cqadupstack_tex_vn`, `cqadupstack_wordpress_vn`,
`fi_qa2018_vn`, `nfcorpus_vn`, `quora_vn`, `scidocs_vn`, and `touche2020_vn`.
These tasks often contain technical terms, formulas, biomedical terminology,
argument terms, or duplicate clusters where sparse and dense signals recover
complementary candidates.

Hybrid has the best group-level recall@100, which is important for
multi-positive tasks. It is not the best nDCG@10 profile overall because dense
ranking is stronger on many translated QA and evidence tasks. For Vietnamese
retrieval systems, this suggests a practical split: dense is a strong default,
while hybrid is valuable for technical duplicates, biomedical retrieval,
argument retrieval, and candidate generation.

## Task Summary

| Task | Family | Language | Queries | Docs | Positives | Positives/query | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [argu_ana_vn](argu_ana_vn.md) | Argument retrieval | `vi` | 199 | 8,674 | 199 | 1.00 | 0.2742 | 0.3698 | 0.3372 | Dense |
| [climate_fever_vn](climate_fever_vn.md) | Claim-evidence retrieval | `vi` | 200 | 10,000 | 635 | 3.17 | 0.2447 | 0.3713 | 0.3245 | Dense |
| [cqadupstack_android_vn](cqadupstack_android_vn.md) | Duplicate-question retrieval | `vi` | 200 | 10,000 | 811 | 4.05 | 0.3774 | 0.4991 | 0.4629 | Dense |
| [cqadupstack_gis_vn](cqadupstack_gis_vn.md) | Duplicate-question retrieval | `vi` | 200 | 10,000 | 299 | 1.50 | 0.3038 | 0.3481 | 0.3420 | Dense |
| [cqadupstack_mathematica_vn](cqadupstack_mathematica_vn.md) | Duplicate-question retrieval | `vi` | 200 | 10,000 | 424 | 2.12 | 0.2157 | 0.1975 | 0.2367 | Reranking hybrid |
| [cqadupstack_physics_vn](cqadupstack_physics_vn.md) | Duplicate-question retrieval | `vi` | 200 | 10,000 | 592 | 2.96 | 0.4127 | 0.4991 | 0.4696 | Dense |
| [cqadupstack_programmers_vn](cqadupstack_programmers_vn.md) | Duplicate-question retrieval | `vi` | 200 | 10,000 | 490 | 2.45 | 0.3568 | 0.4294 | 0.4229 | Dense |
| [cqadupstack_stats_vn](cqadupstack_stats_vn.md) | Duplicate-question retrieval | `vi` | 200 | 10,000 | 310 | 1.55 | 0.3205 | 0.3695 | 0.3796 | Reranking hybrid |
| [cqadupstack_tex_vn](cqadupstack_tex_vn.md) | Duplicate-question retrieval | `vi` | 200 | 10,000 | 743 | 3.71 | 0.2843 | 0.2927 | 0.3163 | Reranking hybrid |
| [cqadupstack_unix_vn](cqadupstack_unix_vn.md) | Duplicate-question retrieval | `vi` | 200 | 10,000 | 434 | 2.17 | 0.3822 | 0.4486 | 0.4455 | Dense |
| [cqadupstack_webmasters_vn](cqadupstack_webmasters_vn.md) | Duplicate-question retrieval | `vi` | 200 | 10,000 | 825 | 4.12 | 0.2517 | 0.3498 | 0.3236 | Dense |
| [cqadupstack_wordpress_vn](cqadupstack_wordpress_vn.md) | Duplicate-question retrieval | `vi` | 200 | 10,000 | 337 | 1.69 | 0.3214 | 0.3105 | 0.3672 | Reranking hybrid |
| [dbpedia_vn](dbpedia_vn.md) | Entity retrieval | `vi` | 200 | 10,000 | 5,754 | 28.77 | 0.6137 | 0.7640 | 0.7247 | Dense |
| [fever_vn](fever_vn.md) | Claim-evidence retrieval | `vi` | 200 | 10,000 | 232 | 1.16 | 0.8013 | 0.9520 | 0.8904 | Dense |
| [fi_qa2018_vn](fi_qa2018_vn.md) | Finance QA retrieval | `vi` | 200 | 10,000 | 549 | 2.75 | 0.3388 | 0.4057 | 0.4118 | Reranking hybrid |
| [hotpot_qa_vn](hotpot_qa_vn.md) | Multi-hop evidence retrieval | `vi` | 200 | 10,000 | 400 | 2.00 | 0.8001 | 0.8773 | 0.8649 | Dense |
| [msmarco_vn](msmarco_vn.md) | Web passage retrieval | `vi` | 200 | 10,000 | 214 | 1.07 | 0.7579 | 0.9259 | 0.8285 | Dense |
| [nano_fever](nano_fever.md) | Claim-evidence retrieval | `vi` | 200 | 10,000 | 232 | 1.16 | 0.7967 | 0.9409 | 0.8680 | Dense |
| [nano_nq](nano_nq.md) | Open-domain QA retrieval | `vi` | 200 | 10,000 | 234 | 1.17 | 0.6095 | 0.8495 | 0.7234 | Dense |
| [nfcorpus_vn](nfcorpus_vn.md) | Biomedical retrieval | `multilingual` | 166 | 3,618 | 4,571 | 27.54 | 0.2552 | 0.2827 | 0.2902 | Reranking hybrid |
| [nq_vn](nq_vn.md) | Open-domain QA retrieval | `vi` | 200 | 10,000 | 234 | 1.17 | 0.5882 | 0.7981 | 0.6826 | Dense |
| [quora_vn](quora_vn.md) | Duplicate-question retrieval | `vi` | 200 | 10,000 | 452 | 2.26 | 0.8345 | 0.8259 | 0.8510 | Reranking hybrid |
| [sci_fact_vn](sci_fact_vn.md) | Scientific evidence retrieval | `vi` | 134 | 5,183 | 155 | 1.16 | 0.6158 | 0.6636 | 0.6485 | Dense |
| [scidocs_vn](scidocs_vn.md) | Scholarly related-paper retrieval | `vi` | 200 | 10,000 | 988 | 4.94 | 0.1613 | 0.2028 | 0.2039 | Reranking hybrid |
| [touche2020_vn](touche2020_vn.md) | Argument retrieval | `vi` | 25 | 10,000 | 481 | 19.24 | 0.6841 | 0.6869 | 0.7280 | Reranking hybrid |
| [treccovid_vn](treccovid_vn.md) | COVID literature retrieval | `vi` | 44 | 10,000 | 4,076 | 92.64 | 0.2811 | 0.3750 | 0.3551 | Dense |

## Interpretation Notes for Model Researchers

NanoVNMTEB is a translation-robustness and task-shape benchmark. Dense retrieval
dominates many translated QA and evidence tasks, suggesting that Vietnamese
semantic matching is critical. Hybrid retrieval is valuable for technical
duplicate clusters, biomedical and scholarly retrieval, finance QA, and
argument retrieval, where exact terms and semantic relatedness both matter.

The group should be analyzed by source family. Improvements on FEVER, MS MARCO,
or NQ do not necessarily imply improvements on CQADupStack, SciDocs, NFCorpus,
or Touché. Multi-positive tasks such as DBpedia, NFCorpus, Touché, and
TREC-COVID should be inspected with recall and ranking behavior, not only one
top-hit metric.

## Training and Leakage Notes

Useful training data includes Vietnamese duplicate-question pairs, Vietnamese
Wikipedia QA, translated or native claim-evidence pairs, finance QA, argument
retrieval, biomedical retrieval, scientific related-paper retrieval, and
Vietnamese web passage retrieval. Technical tasks should preserve code snippets,
math or TeX fragments, URLs, product names, and domain-specific terminology.

Leakage control should exclude NanoVNMTEB evaluation queries, qrels, positive
documents, duplicate clusters, and translated variants of common benchmark test
examples. Overlap audits are especially important for MS MARCO, FEVER, NQ,
Quora, CQADupStack, TREC-COVID, and SciDocs because these sources often appear
in multilingual or synthetic training mixtures.

## Public Sources

- [VN-MTEB: Vietnamese Massive Text Embedding Benchmark](https://aclanthology.org/2026.findings-eacl.86/), 2026.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), 2023.
- [BEIR](https://arxiv.org/abs/2104.08663), 2021.
- [CQADupStack](https://doi.org/10.1145/2838931.2838934), 2015.
- [FEVER](https://arxiv.org/abs/1803.05355), 2018.
- [Natural Questions](https://aclanthology.org/Q19-1026/), 2019.
- [MS MARCO](https://arxiv.org/abs/1611.09268), 2016.
- [TREC-COVID](https://arxiv.org/abs/2005.04474), 2020.
- [GreenNode datasets](https://huggingface.co/GreenNode).

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| VN-MTEB: Vietnamese Massive Text Embedding Benchmark | 2026 | benchmark paper | [https://aclanthology.org/2026.findings-eacl.86/](https://aclanthology.org/2026.findings-eacl.86/) |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |
| BEIR | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| CQADupStack | 2015 | source task paper | [https://doi.org/10.1145/2838931.2838934](https://doi.org/10.1145/2838931.2838934) |
| FEVER | 2018 | source task paper | [https://arxiv.org/abs/1803.05355](https://arxiv.org/abs/1803.05355) |
| Natural Questions | 2019 | source task paper | [https://aclanthology.org/Q19-1026/](https://aclanthology.org/Q19-1026/) |
| MS MARCO | 2016 | source task paper | [https://arxiv.org/abs/1611.09268](https://arxiv.org/abs/1611.09268) |
| TREC-COVID | 2020 | source task paper | [https://arxiv.org/abs/2005.04474](https://arxiv.org/abs/2005.04474) |
| GreenNode datasets |  | dataset organization | [https://huggingface.co/GreenNode](https://huggingface.co/GreenNode) |
