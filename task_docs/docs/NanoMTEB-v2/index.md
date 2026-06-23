# NanoMTEB-v2

## Overview

NanoMTEB-v2 is the English retrieval group derived from MTEB/BEIR-style
retrieval tasks. It combines ten compact splits covering counterargument
retrieval, claim evidence retrieval, StackExchange duplicate-question
retrieval, financial QA, multi-hop Wikipedia QA, scientific paper relatedness,
controversial-question argument retrieval, and biomedical literature search.
The group is useful because it is not a single English passage-retrieval task:
the relevant item may be a counterargument, evidence passage, duplicate
question, answer passage, related paper, argument, or literature record.

The group contains 1,698 queries, 98,626 task-local documents, and 10,158
positive qrel rows. Most tasks are multi-positive, but the number of positives
varies sharply. `argu_ana` is single-positive, while `treccovid` has 4,584
positives for only 50 queries. Aggregate scores therefore mix exact target
retrieval, many-relevant-document ranking, and relation types that are not
simple semantic similarity.

## What This Group Measures

The benchmark measures whether an English retrieval model can preserve source
task semantics across heterogeneous BEIR-style tasks. `argu_ana` retrieves an
opposing argument, not a supporting or near-duplicate passage. `climate_fever`
and `fever` retrieve Wikipedia evidence for claims. `cqadupstack_gaming` and
`cqadupstack_unix` retrieve duplicate community questions. `fi_qa2018`
retrieves finance answers, `hotpot_qa` retrieves supporting Wikipedia passages,
`scidocs` retrieves related scientific papers, `touche2020_v3` retrieves
arguments for controversial questions, and `treccovid` retrieves COVID-19
literature records for broad information needs.

This group is therefore an English heterogeneity check. It can reveal whether a
model is strong because it matches entities and terms, because it understands
paraphrase and answerability, because it can model scientific relatedness, or
because it retrieves broad biomedical evidence sets.

## Task Families

- **Argument retrieval:** `argu_ana` retrieves counterarguments and
  `touche2020_v3` retrieves argument passages for controversial questions.
- **Claim-evidence retrieval:** `climate_fever` and `fever` retrieve evidence
  passages for factual claims.
- **Community duplicate retrieval:** `cqadupstack_gaming` and
  `cqadupstack_unix` retrieve duplicate StackExchange questions.
- **Question-answer retrieval:** `fi_qa2018` and `hotpot_qa` retrieve answer or
  supporting evidence passages.
- **Scientific and biomedical retrieval:** `scidocs` retrieves related papers,
  and `treccovid` retrieves COVID-19 article records.

## Dataset Shape

The group has ten task pages. Most splits have 200 queries; `argu_ana` has 199,
`touche2020_v3` has 49, and `treccovid` has 50. Candidate pools are usually
10,000 documents, with `argu_ana` using 8,626 documents. The document count is a
sum over task-local pools rather than a deduplicated shared English corpus.

Positive density is central to interpretation. `argu_ana` has exactly one
positive per query. `hotpot_qa` has two positives per query. `touche2020_v3`
averages 34.78 positives per query, and `treccovid` averages 91.68. These broad
relevance sets make recall and early ranking behavior important in ways that
differ from single-positive duplicate or evidence retrieval.

## Retrieval Behavior

### BM25 Profile

BM25 is best for none of the ten tasks in the current Nano data, but it remains
strong where exact entities, claims, or technical terms dominate. `hotpot_qa`
and `fever` are both near 0.89 nDCG@10 with BM25, and `touche2020_v3` reaches
0.8424. These tasks often expose names, dates, entities, or argument terms that
also appear in the relevant documents.

BM25 is weakest on `climate_fever`, `scidocs`, and `treccovid`. Climate evidence
can sit under broader Wikipedia topics that do not repeat the claim wording.
Scientific relatedness can be citation- or topic-based rather than title-token
based. TREC-COVID has many relevant documents per query, and exact term overlap
does not reliably rank the best judged literature records early. The
query-weighted BM25 nDCG@10 is 0.4827.

### Dense Profile

Dense retrieval with `harrier-oss-270m` is the strongest query-weighted profile
at 0.5751 nDCG@10. It is best for seven tasks: `argu_ana`, `climate_fever`,
`cqadupstack_gaming`, `cqadupstack_unix`, `fever`, `fi_qa2018`, and `scidocs`.
This pattern is meaningful. Dense retrieval helps when the relevance relation
depends on paraphrase, evidence semantics, duplicate intent, finance
answerability, or scientific relatedness rather than pure term frequency.

Dense is not best for `hotpot_qa`, `touche2020_v3`, or `treccovid`, where the
reranking hybrid profile performs better. It is also only slightly ahead of
BM25 on `argu_ana`, indicating that counterargument retrieval remains difficult
for both sparse and dense methods. Overall, dense retrieval gives the best
single-profile view of this English heterogeneous group.

### Reranking Hybrid Profile

The reranking hybrid profile is best for `hotpot_qa`, `touche2020_v3`, and
`treccovid`. These are tasks where sparse and dense signals are complementary:
multi-hop QA needs entity anchors and semantic support, controversial-question
argument retrieval benefits from both topic terms and argument meaning, and
COVID literature search needs biomedical terminology plus broader semantic
matching.

Hybrid has the best query-weighted recall@100 at 0.8087, even though its
nDCG@10 is below dense. This suggests that hybrid search is a strong candidate
generation strategy for English BEIR-style tasks, while final top-10 ranking
may still favor a dense profile on duplicate, evidence, finance, and scientific
relatedness tasks.

## Task Summary

| Task | Family | Language | Queries | Docs | Positives | Positives/query | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [argu_ana](argu_ana.md) | Counterargument retrieval | `en` | 199 | 8,626 | 199 | 1.00 | 0.3464 | 0.4092 | 0.3775 | Dense |
| [climate_fever](climate_fever.md) | Claim-evidence retrieval | `en` | 200 | 10,000 | 621 | 3.10 | 0.1719 | 0.3276 | 0.2794 | Dense |
| [cqadupstack_gaming](cqadupstack_gaming.md) | Duplicate-question retrieval | `en` | 200 | 10,000 | 415 | 2.08 | 0.5073 | 0.6375 | 0.5970 | Dense |
| [cqadupstack_unix](cqadupstack_unix.md) | Duplicate-question retrieval | `en` | 200 | 10,000 | 486 | 2.43 | 0.4001 | 0.5095 | 0.4658 | Dense |
| [fever](fever.md) | Claim-evidence retrieval | `en` | 200 | 10,000 | 229 | 1.15 | 0.8893 | 0.9652 | 0.9450 | Dense |
| [fi_qa2018](fi_qa2018.md) | Financial QA retrieval | `en` | 200 | 10,000 | 534 | 2.67 | 0.3799 | 0.5494 | 0.5258 | Dense |
| [hotpot_qa](hotpot_qa.md) | Multi-hop evidence retrieval | `en` | 200 | 10,000 | 400 | 2.00 | 0.8950 | 0.8904 | 0.9156 | Reranking hybrid |
| [scidocs](scidocs.md) | Scientific related-paper retrieval | `en` | 200 | 10,000 | 986 | 4.93 | 0.2067 | 0.2757 | 0.2565 | Dense |
| [touche2020_v3](touche2020_v3.md) | Argument retrieval | `en` | 49 | 10,000 | 1,704 | 34.78 | 0.8424 | 0.8810 | 0.8835 | Reranking hybrid |
| [treccovid](treccovid.md) | Biomedical literature retrieval | `en` | 50 | 10,000 | 4,584 | 91.68 | 0.3893 | 0.4177 | 0.4521 | Reranking hybrid |

## Interpretation Notes for Model Researchers

NanoMTEB-v2 should not be treated as one plain English retrieval score. The
same model behavior can mean different things across tasks: improving FEVER may
reflect entity-evidence matching, improving CQADupStack may reflect duplicate
intent modeling, improving SCIDOCS may reflect scientific representation
quality, and improving TREC-COVID may reflect broad biomedical coverage.

Dense retrieval leads most tasks, but hybrid retrieval is important for
multi-hop, argument, and biomedical settings. BM25 remains a strong sanity
baseline for entity-heavy evidence tasks, yet it does not win any task in this
Nano slice. Per-family analysis is required before using the group score to
make claims about English retrieval quality.

## Training and Leakage Notes

Useful training data should be source-family specific: counterargument pairs,
FEVER-style claim-evidence data, StackExchange duplicate questions, finance QA
pairs, HotpotQA-style supporting evidence, citation-linked scientific papers,
argument retrieval data, and PubMed/TREC-style biomedical search data. For
multi-positive tasks, training should preserve multiple positives instead of
collapsing the relevance set.

Leakage control should exclude Nano evaluation queries, qrels, positive
documents, upstream test examples, and common benchmark package duplicates from
ArguAna, CLIMATE-FEVER, CQADupStack, FEVER, FiQA, HotpotQA, SCIDOCS, Touché,
and TREC-COVID. Synthetic data should preserve relation type: counterargument,
evidence, duplicate question, answer passage, related paper, argument passage,
or biomedical relevance record.

## Public Sources

- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), 2023.
- [Retrieval of the Best Counterargument without Prior Topic Knowledge](https://aclanthology.org/P18-1023/), 2018.
- [CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims](https://arxiv.org/abs/2012.00614), 2020.
- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://eltimster.github.io/www/pubs/adcs2015.pdf), 2015.
- [FEVER: a Large-scale Dataset for Fact Extraction and VERification](https://arxiv.org/abs/1803.05355), 2018.
- [Financial Opinion Mining and Question Answering](https://doi.org/10.1145/3184558.3192301), 2018.
- [HotpotQA](https://arxiv.org/abs/1809.09600), 2018.
- [SPECTER](https://arxiv.org/abs/2004.07180), 2020.
- [Overview of Touché 2020: Argument Retrieval](https://downloads.webis.de/touche/publications/papers/bondarenko_2020d.pdf), 2020.
- [TREC-COVID](https://arxiv.org/abs/2005.04474), 2020.

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |
| Retrieval of the Best Counterargument without Prior Topic Knowledge | 2018 | source task paper | [https://aclanthology.org/P18-1023/](https://aclanthology.org/P18-1023/) |
| CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims | 2020 | source task paper | [https://arxiv.org/abs/2012.00614](https://arxiv.org/abs/2012.00614) |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | source task paper | [https://eltimster.github.io/www/pubs/adcs2015.pdf](https://eltimster.github.io/www/pubs/adcs2015.pdf) |
| FEVER: a Large-scale Dataset for Fact Extraction and VERification | 2018 | source task paper | [https://arxiv.org/abs/1803.05355](https://arxiv.org/abs/1803.05355) |
| Financial Opinion Mining and Question Answering | 2018 | source task paper | [https://doi.org/10.1145/3184558.3192301](https://doi.org/10.1145/3184558.3192301) |
| HotpotQA | 2018 | source task paper | [https://arxiv.org/abs/1809.09600](https://arxiv.org/abs/1809.09600) |
| SPECTER | 2020 | source task paper | [https://arxiv.org/abs/2004.07180](https://arxiv.org/abs/2004.07180) |
| Overview of Touché 2020: Argument Retrieval | 2020 | source task paper | [https://downloads.webis.de/touche/publications/papers/bondarenko_2020d.pdf](https://downloads.webis.de/touche/publications/papers/bondarenko_2020d.pdf) |
| TREC-COVID | 2020 | source task paper | [https://arxiv.org/abs/2005.04474](https://arxiv.org/abs/2005.04474) |
