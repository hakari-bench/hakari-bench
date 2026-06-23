# NanoMTEB-German

## Overview

NanoMTEB-German is a compact German retrieval group covering five tasks from the
MTEB and multilingual MTEB ecosystem. It brings together legal retrieval,
open-domain question answering, reading-comprehension context retrieval,
municipal service search, and e-commerce product retrieval. The group is useful
because it does not describe one single German retrieval problem: it tests
whether a model can move between formal legal prose, encyclopedic passages,
citizen-facing administrative language, and short marketplace labels.

The benchmark contains 982 queries, 23,455 task-local documents, and 4,959
positive qrel rows. Most tasks are single-positive retrieval tasks, but
`xmarket_de` is heavily multi-positive, with category queries linked to many
acceptable product records. This mixture makes the group a good diagnostic for
German retrieval systems that need both precise answer-bearing passage retrieval
and broader many-relevant-item ranking.

## What This Group Measures

The central question is whether a model can retrieve German documents under
different relevance relations. `ger_da_lir` asks the model to find legal
decisions from legal passages, where exact legal terminology and citation-like
phrasing are important. `german_dpr` and `german_qu_ad` use German Wikipedia
question-answering data, but they behave differently: one rewards semantic
answerability more strongly, while the other is almost solved by strong lexical
and context overlap. `gov_service` maps natural user questions to Munich service
pages, testing intent matching in administrative German. `xmarket_de` maps
category-like German queries to product metadata, testing high-recall ranking
with many relevant items.

For researchers, the value of the group is the contrast among retrieval
signals. Some tasks are dominated by sparse lexical matching, some by dense
semantic matching, and none in the current Nano slice is best served by the
reranking hybrid profile at nDCG@10. That does not make hybrid unimportant:
hybrid still improves top-100 coverage and hit@10 at group level, but it is not
the leading nDCG@10 profile for any individual task in this group.

## Task Families

- **Legal retrieval:** `ger_da_lir` retrieves German legal decisions from legal
  passages. It is long-document retrieval with strong terminology and citation
  signals.
- **German QA passage retrieval:** `german_dpr` retrieves answer-bearing German
  Wikipedia passages for open-domain questions.
- **German reading-comprehension retrieval:** `german_qu_ad` retrieves the
  GermanQuAD context passage for each question, with very high scores across all
  retrieval profiles.
- **Public service retrieval:** `gov_service` retrieves Munich municipal service
  pages from citizen questions.
- **Marketplace retrieval:** `xmarket_de` retrieves product records from German
  category labels and short product-oriented queries.

## Dataset Shape

The group has five task pages. Four tasks are marked as German (`de`), while
`xmarket_de` is marked multilingual because product names, brand strings, and
category labels often mix German with international terms. The group-level
document count is the sum of task-local pools, not a deduplicated shared corpus.

Three tasks are strictly single-positive: `german_dpr`, `german_qu_ad`, and
`gov_service`. `ger_da_lir` is nearly single-positive with 235 positives for 200
queries. `xmarket_de` is the outlier: 182 queries have 4,124 positives, or about
22.66 positives per query. This difference matters when interpreting recall and
nDCG. A single missed positive can define failure in the QA tasks, while
marketplace ranking is more about placing many acceptable products early.

## Retrieval Behavior

### BM25 Profile

BM25 is the best nDCG@10 profile for `ger_da_lir` and `german_qu_ad`. This is
consistent with tasks where query wording, entities, legal terms, and passage
phrases carry direct relevance evidence. In `german_qu_ad`, BM25 reaches
0.9458 nDCG@10, essentially matching dense and hybrid. In `ger_da_lir`, BM25
scores 0.5360 while dense falls to 0.2920, showing that the legal task in this
Nano slice strongly rewards exact German legal vocabulary and surface-form
anchors.

BM25 is weaker on `german_dpr`, `gov_service`, and `xmarket_de`. Those tasks
require more paraphrase, intent matching, or category-product association than
literal token overlap alone can provide. At group level, BM25 remains a strong
baseline because the legal and GermanQuAD tasks are sizeable and lexically
friendly, but it should not be treated as a universal German retrieval solution.

### Dense Profile

Dense retrieval with `harrier-oss-270m` is the best profile for `german_dpr`,
`gov_service`, and `xmarket_de`. The GermanDPR result is the clearest case:
dense reaches 0.7837 nDCG@10 against BM25 at 0.4647, which indicates that the
task depends on semantic answerability and paraphrase between question and
passage. `gov_service` behaves similarly, with dense at 0.7903 against BM25 at
0.6132, because citizen questions and official service descriptions often use
different wording for the same intent.

Dense is only slightly ahead on `xmarket_de`, where all profiles are low:
0.2268 for dense, 0.2210 for hybrid, and 0.2012 for BM25. This suggests that
embedding similarity helps with category-product relatedness, but the task
remains difficult because relevance is broad, product metadata is short, and
many positives compete within the top ranks.

### Reranking Hybrid Profile

The reranking hybrid column combines sparse and dense evidence to emulate a
hybrid-search candidate set. In this group it is not the best nDCG@10 profile
for any individual task, but it is still informative. It improves group-level
hit@10 and recall@100 relative to dense alone, and it stays close to the best
profile on `german_qu_ad` and `xmarket_de`. That pattern indicates that hybrid
retrieval is recovering complementary candidates even when the final top-10
ordering is not the strongest.

The main caution is visible in `german_dpr` and `gov_service`: hybrid trails
dense by a noticeable margin at nDCG@10. For these semantic-answerability tasks,
adding sparse evidence can dilute dense ranking in the top positions. For German
systems, this group therefore argues for tuning hybrid fusion per task family
rather than assuming that combined retrieval always dominates both components.

## Task Summary

| Task | Family | Language | Queries | Docs | Positives | Positives/query | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [ger_da_lir](ger_da_lir.md) | Legal retrieval | `de` | 200 | 10,000 | 235 | 1.18 | 0.5360 | 0.2920 | 0.4461 | BM25 |
| [german_dpr](german_dpr.md) | QA passage retrieval | `de` | 200 | 2,876 | 200 | 1.00 | 0.4647 | 0.7837 | 0.6120 | Dense |
| [german_qu_ad](german_qu_ad.md) | Reading-comprehension retrieval | `de` | 200 | 474 | 200 | 1.00 | 0.9458 | 0.9321 | 0.9427 | BM25 |
| [gov_service](gov_service.md) | Public service retrieval | `de` | 200 | 105 | 200 | 1.00 | 0.6132 | 0.7903 | 0.6959 | Dense |
| [xmarket_de](xmarket_de.md) | Marketplace retrieval | `multilingual` | 182 | 10,000 | 4,124 | 22.66 | 0.2012 | 0.2268 | 0.2210 | Dense |

## Interpretation Notes for Model Researchers

NanoMTEB-German should be read as a diagnostic group, not as a single aggregate
German score. BM25-led performance on `ger_da_lir` and `german_qu_ad` suggests
that exact lexical evidence remains critical for legal and context-overlap
retrieval. Dense-led performance on `german_dpr`, `gov_service`, and
`xmarket_de` suggests that German semantic retrieval quality matters for
question answering, public-service intent matching, and category-product
association.

The group also separates single-positive evaluation from many-positive
evaluation. Improvements on `xmarket_de` may reflect better category coverage
and product clustering, while improvements on `german_dpr` or `gov_service`
usually mean better ranking of one target passage or page. When comparing
models, inspect per-task nDCG@10 and recall@100 before interpreting the group
mean.

## Training and Leakage Notes

Training data for this group should be separated by retrieval family. German
Wikipedia QA pairs, GermanQuAD-style context retrieval pairs, German municipal
FAQ and service descriptions, German legal case retrieval pairs, and e-commerce
category-product pairs are all useful, but they exercise different relevance
relations. Mixing them without labels can hide whether gains come from legal
lexical matching, semantic QA retrieval, public-service intent matching, or
marketplace categorization.

Leakage control should exclude evaluation queries, qrels, and positive
documents from GerDaLIR, GermanDPR, GermanQuAD, LHM-Dienstleistungen-QA, and
XMarket-derived data. Synthetic augmentation should preserve named entities,
legal terms, service names, product names, numbers, and category labels. Hard
negatives are especially useful when they share surface terms but differ in the
actual legal issue, answer, service, or product category.

## Public Sources

- [GerDaLIR: A German Dataset for Legal Information Retrieval](https://aclanthology.org/2021.nllp-1.13/), 2021.
- [GermanQuAD and GermanDPR: Improving Non-English Question Answering and Passage Retrieval](https://arxiv.org/abs/2104.12741), 2021.
- [Cross-Market Product Recommendation](https://arxiv.org/abs/2109.05929), 2021.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), 2023.
- [MMTEB arXiv](https://arxiv.org/abs/2502.13595).
- [GerDaLIR GitHub](https://github.com/lavis-nlp/GerDaLIR).
- [mteb/GerDaLIR](https://huggingface.co/datasets/mteb/GerDaLIR).
- [mteb/GermanDPR](https://huggingface.co/datasets/mteb/GermanDPR).
- [deepset/germandpr](https://huggingface.co/datasets/deepset/germandpr).
- [deepset/germanquad](https://huggingface.co/datasets/deepset/germanquad).
- [it-at-m/LHM-Dienstleistungen-QA](https://huggingface.co/datasets/it-at-m/LHM-Dienstleistungen-QA), 2022.

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| GerDaLIR: A German Dataset for Legal Information Retrieval | 2021 | paper | [https://aclanthology.org/2021.nllp-1.13/](https://aclanthology.org/2021.nllp-1.13/) |
| GermanQuAD and GermanDPR: Improving Non-English Question Answering and Passage Retrieval | 2021 | paper | [https://arxiv.org/abs/2104.12741](https://arxiv.org/abs/2104.12741) |
| Cross-Market Product Recommendation | 2021 | paper | [https://arxiv.org/abs/2109.05929](https://arxiv.org/abs/2109.05929) |
| MTEB: Massive Text Embedding Benchmark | 2023 | paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |
| MMTEB arXiv |  | paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| GerDaLIR GitHub |  | dataset or project page | [https://github.com/lavis-nlp/GerDaLIR](https://github.com/lavis-nlp/GerDaLIR) |
| mteb/GerDaLIR |  | dataset or project page | [https://huggingface.co/datasets/mteb/GerDaLIR](https://huggingface.co/datasets/mteb/GerDaLIR) |
| mteb/GermanDPR |  | dataset or project page | [https://huggingface.co/datasets/mteb/GermanDPR](https://huggingface.co/datasets/mteb/GermanDPR) |
| deepset/germandpr |  | dataset or project page | [https://huggingface.co/datasets/deepset/germandpr](https://huggingface.co/datasets/deepset/germandpr) |
| deepset/germanquad |  | dataset or project page | [https://huggingface.co/datasets/deepset/germanquad](https://huggingface.co/datasets/deepset/germanquad) |
| it-at-m/LHM-Dienstleistungen-QA | 2022 | dataset or project page | [https://huggingface.co/datasets/it-at-m/LHM-Dienstleistungen-QA](https://huggingface.co/datasets/it-at-m/LHM-Dienstleistungen-QA) |
