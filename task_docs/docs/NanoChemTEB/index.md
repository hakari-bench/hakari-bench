# NanoChemTEB

## Overview

NanoChemTEB is the compact chemistry-domain retrieval group. It combines two
chemistry-filtered QA retrieval tasks, `NanoChemHotpotQA` and `NanoChemNQ`,
with `NanoChemRxiv`, a chemical-literature retrieval task over ChemRxiv-style
paragraphs. The shared challenge is not English retrieval in general, but
retrieval under chemical names, compounds, reactions, materials, methods, and
scientific passage style.

The group contrasts Wikipedia-derived QA evidence with chemistry literature
retrieval. The QA tasks ask familiar question-to-passage retrieval questions in
a chemistry-heavy subset. The ChemRxiv task is closer to scientific literature
search, where exact chemical terminology can be very informative but the
passage may be longer and more technical. BM25, dense retrieval, and
`reranking_hybrid` are all strong on this group, so the interesting signal is
which task benefits from exact chemical terms, semantic answerability, or a
combined candidate pool.

## What This Group Measures

[ChemTEB: Chemical Text Embedding Benchmark](https://proceedings.mlr.press/v262/shiraee-kasmaee24a.html)
evaluates embedding models on chemical-domain tasks, including retrieval.
[ChEmbed: Enhancing Chemical Literature Search Through Domain-Specific Text Embeddings](https://arxiv.org/abs/2508.01643)
extends the domain-specific literature search setting. NanoChemTEB packages
three compact retrieval splits from that chemistry-focused evaluation surface.

The group measures whether a retriever can connect chemistry questions to
evidence passages. In the QA tasks, the model must retrieve a passage that
answers the chemistry-focused question. In ChemRxiv, it must retrieve a
scientific paragraph whose domain terminology, method, compound, or result
matches the information need.

## Task Families

- **Chemistry QA evidence retrieval:** `NanoChemHotpotQA` and `NanoChemNQ`
  retrieve Wikipedia-derived evidence passages for chemistry-focused questions.
- **Chemical literature retrieval:** `NanoChemRxiv` retrieves ChemRxiv-style
  scientific paragraphs.
- **Term-heavy scientific matching:** all tasks contain chemical entities,
  methods, compounds, or materials where exact wording and semantic context both
  matter.

## Dataset Shape

NanoChemTEB contains 3 task pages, 245 queries, 30,000 split-local documents,
and 253 positive qrel rows. `NanoChemRxiv` dominates the group by query count
with 200 queries, while the QA tasks are much smaller. Most queries are
single-positive; `NanoChemNQ` has a small number of multi-positive queries.

Documents differ by source. ChemRxiv paragraphs average more than 1,000
characters, while the HotpotQA and NQ chemistry passages are shorter
Wikipedia-style evidence. This means the group mixes answer-passage retrieval
with scientific paragraph retrieval, and those should be interpreted separately.

## Retrieval Behavior

### BM25 Profile

BM25 is very strong on `NanoChemRxiv`, where chemical names, materials, methods,
and scientific phrases often repeat between query and paragraph. It is also
competitive on `NanoChemHotpotQA`. `NanoChemNQ` is harder because shorter
questions can phrase the information need differently from the evidence passage.

This group shows the positive side of lexical retrieval in domain science:
exact chemical terms are often meaningful, not noise. A model that loses those
terms may underperform even if it has good general semantic similarity.

### Dense Profile

Dense retrieval helps most when the chemistry question and passage express the
same answer relation with different wording. It improves over BM25 on
`NanoChemNQ` and `NanoChemHotpotQA`, where question wording can be less
terminology-aligned than literature search. Dense retrieval is slightly behind
BM25 on ChemRxiv in the current metadata, which suggests exact scientific terms
remain important.

Dense scores should be read as domain semantic matching, not generic English
similarity. The model must preserve chemical entities and methods while also
connecting paraphrased evidence.

### Reranking Hybrid Profile

`reranking_hybrid` is the best profile for `NanoChemHotpotQA` and
`NanoChemRxiv`, and it remains competitive on `NanoChemNQ`. That pattern fits
the domain: sparse retrieval preserves chemical terminology, while dense
retrieval can connect broader answerability or scientific context.

For reranker experiments, the hybrid pool is likely the safest starting point
because candidate loss can happen when either exact terms or semantic relations
are missing.

## Task Summary

| Task | Retrieval focus | Queries | Docs | Positives | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [NanoChemHotpotQA](NanoChemHotpotQA.md) | chemistry multi-hop QA evidence | 18 | 10,000 | 18 | 0.7178 | 0.7748 | 0.7923 | Reranking hybrid |
| [NanoChemNQ](NanoChemNQ.md) | chemistry Natural Questions evidence | 27 | 10,000 | 35 | 0.4446 | 0.6184 | 0.5526 | Dense |
| [NanoChemRxiv](NanoChemRxiv.md) | chemistry query to ChemRxiv paragraph | 200 | 10,000 | 200 | 0.9411 | 0.9000 | 0.9419 | Reranking hybrid |

## Interpretation Notes for Model Researchers

NanoChemTEB is a domain-specific retrieval check. Strong results imply that a
model handles chemistry terminology and scientific evidence, not just English
questions. Compare QA and ChemRxiv separately: QA rewards answerability, while
ChemRxiv rewards literature-style paragraph matching with exact domain terms.

The BM25/dense comparison is especially useful. If BM25 is strong, exact
chemical phrases are carrying the task. If dense improves, the model is bridging
question wording and evidence. If hybrid improves, both are needed for reliable
candidate generation.

## Training and Leakage Notes

Useful training data includes non-overlapping ChemTEB retrieval pairs,
chemistry-focused QA evidence pairs, scientific abstract or paragraph retrieval,
ChemRxiv or PubMed-style literature search, and hard negatives that share
compounds, methods, or materials but answer a different question.

Exclude NanoChemTEB evaluation queries, positives, qrels, and positive
paragraphs. If ChemRxiv, ChemTEB, HotpotQA, or Natural Questions source data are
used, audit the chemistry-filtered examples for overlap before training.

## Public Sources

- [ChemTEB: Chemical Text Embedding Benchmark](https://proceedings.mlr.press/v262/shiraee-kasmaee24a.html), 2024.
- [ChEmbed: Enhancing Chemical Literature Search Through Domain-Specific Text Embeddings](https://arxiv.org/abs/2508.01643), 2025.
- [HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://aclanthology.org/D18-1259/), 2018.
- [Natural Questions: A Benchmark for Question Answering Research](https://aclanthology.org/Q19-1026/), 2019.

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| ChemTEB: Chemical Text Embedding Benchmark | 2024 | paper | [https://proceedings.mlr.press/v262/shiraee-kasmaee24a.html](https://proceedings.mlr.press/v262/shiraee-kasmaee24a.html) |
| ChEmbed: Enhancing Chemical Literature Search Through Domain-Specific Text Embeddings | 2025 | paper | [https://arxiv.org/abs/2508.01643](https://arxiv.org/abs/2508.01643) |
| HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering | 2018 | paper | [https://aclanthology.org/D18-1259/](https://aclanthology.org/D18-1259/) |
| Natural Questions: A Benchmark for Question Answering Research | 2019 | paper | [https://aclanthology.org/Q19-1026/](https://aclanthology.org/Q19-1026/) |
