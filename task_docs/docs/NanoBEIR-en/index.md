# NanoBEIR-en

## Overview

NanoBEIR-en is the English compact BEIR group. It preserves BEIR's main
evaluation idea, heterogeneous zero-shot retrieval, while making each source
task small enough for fast iteration and manual inspection. The group contains
thirteen English retrieval tasks covering counterargument retrieval,
fact-checking evidence, entity search, financial QA, multi-hop Wikipedia QA,
web passage retrieval, biomedical evidence, duplicate-question matching,
scientific document relatedness, and debate argument retrieval.

This group should not be interpreted as one generic English search task. Each
subtask defines relevance differently. DBPedia rewards entity disambiguation,
Quora rewards duplicate-question intent, FEVER and SciFact reward evidence,
ArguAna rewards counterarguments, and NFCorpus rewards biomedical relevance.
BM25 identifies tasks with strong surface anchors, dense retrieval identifies
semantic or paraphrase-heavy tasks, and `reranking_hybrid` highlights cases
where exact and semantic retrieval produce complementary candidate sets.

## What This Group Measures

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663)
introduced BEIR as a benchmark for retrieval transfer across domains and task
definitions. [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)
keeps the BEIR task diversity but uses compact subsets. NanoBEIR-en is the
English anchor group for comparing these task families without multilingual
translation effects.

The group measures whether a retriever understands the relevance relation of
each task. A model that works well on MS MARCO-style web questions may still
fail on SCIDOCS related-paper retrieval or ArguAna counterargument retrieval.
That is the point of this group: it exposes whether retrieval quality transfers
across English tasks whose queries and documents look superficially similar but
require different matching behavior.

## Task Families

- **Argument retrieval:** `NanoArguAna` and `NanoTouche2020` use long,
  stance-sensitive argument text. Topical similarity alone can be misleading.
- **Evidence retrieval:** `NanoClimateFEVER`, `NanoFEVER`, and `NanoSciFact`
  retrieve evidence for claims. Exact entities help, but the evidence relation
  must also be correct.
- **Open-domain QA retrieval:** `NanoFiQA2018`, `NanoHotpotQA`,
  `NanoMSMARCO`, and `NanoNQ` retrieve answer-bearing passages for finance,
  multi-hop questions, web search, and natural questions.
- **Entity and duplicate retrieval:** `NanoDBPedia` retrieves entity pages,
  while `NanoQuoraRetrieval` retrieves semantically duplicate questions.
- **Scientific and biomedical retrieval:** `NanoNFCorpus` and `NanoSCIDOCS`
  emphasize technical terms, abstracts, paper titles, and broad multi-positive
  relevance.

## Dataset Shape

NanoBEIR-en contains 13 task pages, 649 queries, 56,723 split-local documents,
and 4,696 positive qrel rows. Most tasks have 50 queries; `NanoTouche2020` has
49. The group has 343 multi-positive queries, and the average positives per
query is about 7.24, driven mainly by `NanoDBPedia`, `NanoNFCorpus`,
`NanoSCIDOCS`, and `NanoTouche2020`.

Length differs more by task than by retrieval method. `NanoArguAna` has very
long argument queries, `NanoTouche2020` has long argument passages,
`NanoQuoraRetrieval` has very short question documents, and `NanoNFCorpus` has
short medical queries with many relevant documents. Because of this variation,
global averages are less useful than family-level interpretation.

## Retrieval Behavior

### BM25 Profile

BM25 is strong where exact surface evidence is informative. `NanoHotpotQA`,
`NanoFEVER`, `NanoQuoraRetrieval`, `NanoSciFact`, and `NanoTouche2020` all have
substantial sparse signal in the current metadata. These tasks contain named
entities, claims, question wording, or many acceptable positives that BM25 can
recover.

BM25 is weaker on tasks where relevant documents use different vocabulary from
the query. `NanoNFCorpus`, `NanoClimateFEVER`, and `NanoSCIDOCS` are especially
useful for seeing that limitation. They require biomedical terminology,
scientific relatedness, or evidence wording that is not always captured by raw
term overlap.

### Dense Profile

Dense retrieval improves many English BEIR tasks because it can connect
paraphrases, answer-bearing passages, duplicate intent, and semantic relatedness
without exact word repetition. It is particularly informative for
`NanoArguAna`, `NanoMSMARCO`, `NanoNQ`, `NanoQuoraRetrieval`, and several
evidence tasks.

Dense retrieval is still not a universal substitute for lexical matching. It
can underweight rare entities, numbers, citations, and technical terms. The best
research use of NanoBEIR-en is to compare dense improvements against BM25: a
dense-led task indicates semantic transfer, while a BM25-competitive task shows
where exact evidence remains hard to replace.

### Reranking Hybrid Profile

`reranking_hybrid` is strongest on tasks where sparse and dense retrieval find
different useful positives. It is the best nDCG@10 profile for tasks such as
`NanoClimateFEVER`, `NanoDBPedia`, `NanoFiQA2018`, `NanoHotpotQA`, and
`NanoQuoraRetrieval` in the current metadata. These are good candidates for
reranker experiments because first-stage candidate diversity matters.

When hybrid is not the best top-rank profile, it can still be the safer
candidate pool if it improves Recall@100. For reranking research, this means the
hybrid column should be read as a candidate-generation diagnostic, not simply as
another ranker score.

## Task Summary

| Task | Retrieval focus | Queries | Docs | Positives | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [NanoArguAna](NanoArguAna.md) | counterargument retrieval | 50 | 3,635 | 50 | 0.4650 | 0.5787 | 0.5422 | Dense |
| [NanoClimateFEVER](NanoClimateFEVER.md) | climate claim evidence | 50 | 3,408 | 148 | 0.3266 | 0.2811 | 0.3419 | Reranking hybrid |
| [NanoDBPedia](NanoDBPedia.md) | entity retrieval | 50 | 6,045 | 1,158 | 0.6374 | 0.6243 | 0.6564 | Reranking hybrid |
| [NanoFEVER](NanoFEVER.md) | factual claim evidence | 50 | 4,996 | 57 | 0.8143 | 0.8816 | 0.8521 | Dense |
| [NanoFiQA2018](NanoFiQA2018.md) | finance QA passage retrieval | 50 | 4,598 | 123 | 0.4211 | 0.5011 | 0.5150 | Reranking hybrid |
| [NanoHotpotQA](NanoHotpotQA.md) | multi-hop QA evidence | 50 | 5,090 | 100 | 0.8270 | 0.8043 | 0.8325 | Reranking hybrid |
| [NanoMSMARCO](NanoMSMARCO.md) | web passage retrieval | 50 | 5,043 | 50 | 0.5217 | 0.6188 | 0.6170 | Dense |
| [NanoNFCorpus](NanoNFCorpus.md) | biomedical evidence retrieval | 50 | 2,953 | 1,651 | 0.3060 | 0.3135 | 0.3178 | Reranking hybrid |
| [NanoNQ](NanoNQ.md) | natural question evidence | 50 | 5,035 | 57 | 0.5140 | 0.6726 | 0.6584 | Dense |
| [NanoQuoraRetrieval](NanoQuoraRetrieval.md) | duplicate question retrieval | 50 | 5,046 | 70 | 0.8745 | 0.8888 | 0.9105 | Reranking hybrid |
| [NanoSCIDOCS](NanoSCIDOCS.md) | related scientific documents | 50 | 2,210 | 244 | 0.3294 | 0.4392 | 0.3962 | Dense |
| [NanoSciFact](NanoSciFact.md) | scientific claim evidence | 50 | 2,919 | 56 | 0.7282 | 0.7679 | 0.7397 | Dense |
| [NanoTouche2020](NanoTouche2020.md) | debate argument retrieval | 49 | 5,745 | 932 | 0.6648 | 0.5407 | 0.6184 | BM25 |

## Interpretation Notes for Model Researchers

NanoBEIR-en is the best baseline group for understanding the task-family effects
that also appear in multilingual NanoBEIR variants. If a model is weak on
English `NanoNFCorpus` or `NanoSCIDOCS`, a multilingual failure on the same
source task is probably not only a language issue. If it is strong on English
but weak in another language, the gap is more likely tied to translation,
tokenization, or multilingual representation.

The group is also useful for diagnosing ranking depth. In multi-positive tasks,
hit@10 can saturate while nDCG@10 and Recall@100 still separate models. For
single-positive tasks, top-rank ordering and candidate coverage are easier to
interpret directly. Always compare the score profile with the task's relevance
definition before drawing conclusions about model quality.

## Training and Leakage Notes

Useful training data should be task-specific: MS MARCO-style passage pairs for
web retrieval, FEVER and SciFact claim-evidence data for fact verification,
duplicate-question pairs for Quora, biomedical or medical search data for
NFCorpus, citation and paper-title retrieval for SCIDOCS, and argument-mining
data for ArguAna and Touche. Multi-positive objectives are important for entity,
biomedical, scientific, and debate retrieval tasks.

Leakage risk is substantial because BEIR source datasets are widely used in
retrieval training mixtures. Exclude NanoBEIR-en evaluation queries, positives,
qrels, and direct synthetic variants of them. Audit overlap before using MS
MARCO, NQ, HotpotQA, FEVER, Quora, NFCorpus, SCIDOCS, SciFact, DBPedia, or
Touche-style data.

## Public Sources

- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [MTEB benchmark](https://github.com/embeddings-benchmark/mteb).

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| NanoBEIR collection |  | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| MTEB benchmark |  | project | [https://github.com/embeddings-benchmark/mteb](https://github.com/embeddings-benchmark/mteb) |
