# MNanoBEIR

## Overview

MNanoBEIR is the multilingual NanoBEIR group: a grid of compact BEIR-style
retrieval tasks across Arabic, German, Spanish, French, Italian, Japanese,
Korean, Norwegian, Portuguese, Serbian, Swedish, Thai, and Vietnamese. Each
language variant contains the same thirteen source tasks, so the group separates
two questions that are often mixed together: whether a model understands the
underlying BEIR retrieval relation, and whether that behavior survives in
non-English text.

The source task mix is deliberately heterogeneous. Some tasks retrieve duplicate
questions, some retrieve Wikipedia evidence, some retrieve biomedical or
scientific documents, some retrieve debate arguments, and some retrieve
answer-bearing web passages. A single average score is therefore not enough to
understand the group. The useful reading is by language, task family, and
retrieval profile. BM25 exposes exact-term and named-entity dependence; dense
retrieval exposes semantic transfer and paraphrase handling; `reranking_hybrid`
shows where sparse and dense candidates complement each other.

## What This Group Measures

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663)
introduced a benchmark philosophy based on many retrieval relations rather than
one passage-search task. MNanoBEIR inherits that philosophy from compact
NanoBEIR tasks and applies it to multilingual evaluation. The result is a
regular 13-by-13 grid: thirteen languages and thirteen BEIR-derived source
tasks.

This group measures multilingual robustness under changing relevance semantics.
For example, a relevant Quora document should be a duplicate question, a
relevant FEVER document should support or refute a claim, a relevant ArguAna
document should work as a counterargument, and a relevant SCIDOCS document
should be scientifically related. A retriever that treats all rows as generic
semantic similarity will miss much of what the group tests.

## Task Families

- **Argument retrieval:** `NanoArguAna` and `NanoTouche2020` evaluate
  counterargument and debate-passage retrieval. They often have long text and
  stance-sensitive negatives.
- **Evidence retrieval:** `NanoClimateFEVER`, `NanoFEVER`, and `NanoSciFact`
  evaluate claim-to-evidence retrieval. Exact named entities matter, but the
  target passage must also express the right evidence relation.
- **Open-domain QA retrieval:** `NanoFiQA2018`, `NanoHotpotQA`,
  `NanoMSMARCO`, and `NanoNQ` evaluate answer-bearing retrieval for finance,
  multi-hop QA, web search, and natural questions.
- **Entity and duplicate retrieval:** `NanoDBPedia` and
  `NanoQuoraRetrieval` stress entity-page matching and duplicate-question
  intent matching.
- **Scientific and biomedical retrieval:** `NanoNFCorpus` and `NanoSCIDOCS`
  are domain-specific and multi-positive, with many lexical traps around
  medical terms, paper titles, and related-work language.

## Dataset Shape

MNanoBEIR contains 169 task pages, 8,437 queries, 737,399 split-local documents,
and 61,048 positive qrel rows. Each language has 13 task pages and 649 queries:
most base tasks have 50 queries, while `NanoTouche2020` has 49. The document
count is a sum over task-local pools, not a deduplicated multilingual corpus.

The group is highly multi-positive. `NanoArguAna` and `NanoMSMARCO` are
single-positive in this grid, but `NanoDBPedia`, `NanoNFCorpus`,
`NanoSCIDOCS`, and `NanoTouche2020` contain many positives per query. This
means hit@10 can look good while nDCG@10 or Recall@100 still shows ranking
quality differences. Query and document length also vary by task: ArguAna and
Touche have long argumentative text, Quora has short question text, NFCorpus
has short medical queries and many positives, and FEVER-like tasks depend on
claim-evidence alignment.

## Retrieval Behavior

### BM25 Profile

BM25 is strongest where exact words, named entities, titles, technical terms, or
many acceptable positives dominate. In this group, Quora, FEVER, DBPedia,
HotpotQA, and some Touche splits often give sparse retrieval a clear path.
BM25 is weaker on finance, scientific related-paper retrieval, and some climate
evidence tasks where the relevant document may use different wording from the
query.

Language differences should not be reduced to script alone. Latin-script
European languages can still differ because of translation choices and
morphology; Japanese, Korean, Thai, Arabic, Serbian, and Vietnamese introduce
additional tokenization and segmentation considerations. A BM25-competitive
split is a sign that exact lexical anchoring remains central, not that the task
is easy.

### Dense Profile

Dense retrieval is the leading nDCG@10 profile for many MNanoBEIR tasks. It is
most informative when the target relation depends on paraphrase, answerability,
or relatedness rather than direct term overlap. This is visible in duplicate
question retrieval, NQ-style passage retrieval, FEVER-style evidence selection,
and some finance and scientific tasks.

Dense retrieval can still lose rare exact anchors. Entity-heavy tasks, medical
terms, numeric facts, paper titles, and translated names can be underweighted if
the embedding model smooths them into broader topical similarity. This makes the
BM25-versus-dense comparison useful: it tells whether a task is mainly lexical,
mainly semantic, or dependent on both.

### Reranking Hybrid Profile

`reranking_hybrid` is the practical reranker-candidate view of MNanoBEIR. It
often performs best when BM25 and dense retrieval find different relevant
documents. ClimateFEVER, DBPedia, Touche, SCIDOCS, and several multilingual
open-domain QA splits show this complementarity.

When `reranking_hybrid` is best by nDCG@10, the task is signaling that neither
exact matching nor embedding similarity alone is sufficient. When it is not the
best top-rank sorter but has stronger Recall@100, it is still useful for
reranker experiments because it preserves positives that either first-stage
method would otherwise drop.

## Language Summary

| Language | Tasks | Queries | Docs | Positives | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `ar` | 13 | 649 | 56,723 | 4,696 | 0.4412 | 0.4867 | 0.4919 |
| `de` | 13 | 649 | 56,723 | 4,696 | 0.4476 | 0.5313 | 0.5099 |
| `es` | 13 | 649 | 56,723 | 4,696 | 0.5025 | 0.5309 | 0.5318 |
| `fr` | 13 | 649 | 56,723 | 4,696 | 0.5125 | 0.5565 | 0.5620 |
| `it` | 13 | 649 | 56,723 | 4,696 | 0.4830 | 0.5324 | 0.5304 |
| `ja` | 13 | 649 | 56,723 | 4,696 | 0.4661 | 0.5122 | 0.5061 |
| `ko` | 13 | 649 | 56,723 | 4,696 | 0.4479 | 0.4989 | 0.5023 |
| `no` | 13 | 649 | 56,723 | 4,696 | 0.4197 | 0.5140 | 0.4756 |
| `pt` | 13 | 649 | 56,723 | 4,696 | 0.4816 | 0.5334 | 0.5311 |
| `sr` | 13 | 649 | 56,723 | 4,696 | 0.3944 | 0.5032 | 0.4841 |
| `sv` | 13 | 649 | 56,723 | 4,696 | 0.4184 | 0.5170 | 0.4899 |
| `th` | 13 | 649 | 56,723 | 4,696 | 0.4356 | 0.5081 | 0.4944 |
| `vi` | 13 | 649 | 56,723 | 4,696 | 0.4603 | 0.5336 | 0.5244 |

## Task Navigation

| Base task | Family | Language pages |
| --- | --- | --- |
| NanoArguAna | Argument retrieval | [ar](NanoBEIR-ar__NanoArguAna.md), [de](NanoBEIR-de__NanoArguAna.md), [es](NanoBEIR-es__NanoArguAna.md), [fr](NanoBEIR-fr__NanoArguAna.md), [it](NanoBEIR-it__NanoArguAna.md), [ja](NanoBEIR-ja__NanoArguAna.md), [ko](NanoBEIR-ko__NanoArguAna.md), [no](NanoBEIR-no__NanoArguAna.md), [pt](NanoBEIR-pt__NanoArguAna.md), [sr](NanoBEIR-sr__NanoArguAna.md), [sv](NanoBEIR-sv__NanoArguAna.md), [th](NanoBEIR-th__NanoArguAna.md), [vi](NanoBEIR-vi__NanoArguAna.md) |
| NanoClimateFEVER | Evidence retrieval | [ar](NanoBEIR-ar__NanoClimateFEVER.md), [de](NanoBEIR-de__NanoClimateFEVER.md), [es](NanoBEIR-es__NanoClimateFEVER.md), [fr](NanoBEIR-fr__NanoClimateFEVER.md), [it](NanoBEIR-it__NanoClimateFEVER.md), [ja](NanoBEIR-ja__NanoClimateFEVER.md), [ko](NanoBEIR-ko__NanoClimateFEVER.md), [no](NanoBEIR-no__NanoClimateFEVER.md), [pt](NanoBEIR-pt__NanoClimateFEVER.md), [sr](NanoBEIR-sr__NanoClimateFEVER.md), [sv](NanoBEIR-sv__NanoClimateFEVER.md), [th](NanoBEIR-th__NanoClimateFEVER.md), [vi](NanoBEIR-vi__NanoClimateFEVER.md) |
| NanoDBPedia | Entity retrieval | [ar](NanoBEIR-ar__NanoDBPedia.md), [de](NanoBEIR-de__NanoDBPedia.md), [es](NanoBEIR-es__NanoDBPedia.md), [fr](NanoBEIR-fr__NanoDBPedia.md), [it](NanoBEIR-it__NanoDBPedia.md), [ja](NanoBEIR-ja__NanoDBPedia.md), [ko](NanoBEIR-ko__NanoDBPedia.md), [no](NanoBEIR-no__NanoDBPedia.md), [pt](NanoBEIR-pt__NanoDBPedia.md), [sr](NanoBEIR-sr__NanoDBPedia.md), [sv](NanoBEIR-sv__NanoDBPedia.md), [th](NanoBEIR-th__NanoDBPedia.md), [vi](NanoBEIR-vi__NanoDBPedia.md) |
| NanoFEVER | Evidence retrieval | [ar](NanoBEIR-ar__NanoFEVER.md), [de](NanoBEIR-de__NanoFEVER.md), [es](NanoBEIR-es__NanoFEVER.md), [fr](NanoBEIR-fr__NanoFEVER.md), [it](NanoBEIR-it__NanoFEVER.md), [ja](NanoBEIR-ja__NanoFEVER.md), [ko](NanoBEIR-ko__NanoFEVER.md), [no](NanoBEIR-no__NanoFEVER.md), [pt](NanoBEIR-pt__NanoFEVER.md), [sr](NanoBEIR-sr__NanoFEVER.md), [sv](NanoBEIR-sv__NanoFEVER.md), [th](NanoBEIR-th__NanoFEVER.md), [vi](NanoBEIR-vi__NanoFEVER.md) |
| NanoFiQA2018 | Open-domain QA retrieval | [ar](NanoBEIR-ar__NanoFiQA2018.md), [de](NanoBEIR-de__NanoFiQA2018.md), [es](NanoBEIR-es__NanoFiQA2018.md), [fr](NanoBEIR-fr__NanoFiQA2018.md), [it](NanoBEIR-it__NanoFiQA2018.md), [ja](NanoBEIR-ja__NanoFiQA2018.md), [ko](NanoBEIR-ko__NanoFiQA2018.md), [no](NanoBEIR-no__NanoFiQA2018.md), [pt](NanoBEIR-pt__NanoFiQA2018.md), [sr](NanoBEIR-sr__NanoFiQA2018.md), [sv](NanoBEIR-sv__NanoFiQA2018.md), [th](NanoBEIR-th__NanoFiQA2018.md), [vi](NanoBEIR-vi__NanoFiQA2018.md) |
| NanoHotpotQA | Open-domain QA retrieval | [ar](NanoBEIR-ar__NanoHotpotQA.md), [de](NanoBEIR-de__NanoHotpotQA.md), [es](NanoBEIR-es__NanoHotpotQA.md), [fr](NanoBEIR-fr__NanoHotpotQA.md), [it](NanoBEIR-it__NanoHotpotQA.md), [ja](NanoBEIR-ja__NanoHotpotQA.md), [ko](NanoBEIR-ko__NanoHotpotQA.md), [no](NanoBEIR-no__NanoHotpotQA.md), [pt](NanoBEIR-pt__NanoHotpotQA.md), [sr](NanoBEIR-sr__NanoHotpotQA.md), [sv](NanoBEIR-sv__NanoHotpotQA.md), [th](NanoBEIR-th__NanoHotpotQA.md), [vi](NanoBEIR-vi__NanoHotpotQA.md) |
| NanoMSMARCO | Open-domain QA retrieval | [ar](NanoBEIR-ar__NanoMSMARCO.md), [de](NanoBEIR-de__NanoMSMARCO.md), [es](NanoBEIR-es__NanoMSMARCO.md), [fr](NanoBEIR-fr__NanoMSMARCO.md), [it](NanoBEIR-it__NanoMSMARCO.md), [ja](NanoBEIR-ja__NanoMSMARCO.md), [ko](NanoBEIR-ko__NanoMSMARCO.md), [no](NanoBEIR-no__NanoMSMARCO.md), [pt](NanoBEIR-pt__NanoMSMARCO.md), [sr](NanoBEIR-sr__NanoMSMARCO.md), [sv](NanoBEIR-sv__NanoMSMARCO.md), [th](NanoBEIR-th__NanoMSMARCO.md), [vi](NanoBEIR-vi__NanoMSMARCO.md) |
| NanoNFCorpus | Biomedical retrieval | [ar](NanoBEIR-ar__NanoNFCorpus.md), [de](NanoBEIR-de__NanoNFCorpus.md), [es](NanoBEIR-es__NanoNFCorpus.md), [fr](NanoBEIR-fr__NanoNFCorpus.md), [it](NanoBEIR-it__NanoNFCorpus.md), [ja](NanoBEIR-ja__NanoNFCorpus.md), [ko](NanoBEIR-ko__NanoNFCorpus.md), [no](NanoBEIR-no__NanoNFCorpus.md), [pt](NanoBEIR-pt__NanoNFCorpus.md), [sr](NanoBEIR-sr__NanoNFCorpus.md), [sv](NanoBEIR-sv__NanoNFCorpus.md), [th](NanoBEIR-th__NanoNFCorpus.md), [vi](NanoBEIR-vi__NanoNFCorpus.md) |
| NanoNQ | Open-domain QA retrieval | [ar](NanoBEIR-ar__NanoNQ.md), [de](NanoBEIR-de__NanoNQ.md), [es](NanoBEIR-es__NanoNQ.md), [fr](NanoBEIR-fr__NanoNQ.md), [it](NanoBEIR-it__NanoNQ.md), [ja](NanoBEIR-ja__NanoNQ.md), [ko](NanoBEIR-ko__NanoNQ.md), [no](NanoBEIR-no__NanoNQ.md), [pt](NanoBEIR-pt__NanoNQ.md), [sr](NanoBEIR-sr__NanoNQ.md), [sv](NanoBEIR-sv__NanoNQ.md), [th](NanoBEIR-th__NanoNQ.md), [vi](NanoBEIR-vi__NanoNQ.md) |
| NanoQuoraRetrieval | Duplicate question retrieval | [ar](NanoBEIR-ar__NanoQuoraRetrieval.md), [de](NanoBEIR-de__NanoQuoraRetrieval.md), [es](NanoBEIR-es__NanoQuoraRetrieval.md), [fr](NanoBEIR-fr__NanoQuoraRetrieval.md), [it](NanoBEIR-it__NanoQuoraRetrieval.md), [ja](NanoBEIR-ja__NanoQuoraRetrieval.md), [ko](NanoBEIR-ko__NanoQuoraRetrieval.md), [no](NanoBEIR-no__NanoQuoraRetrieval.md), [pt](NanoBEIR-pt__NanoQuoraRetrieval.md), [sr](NanoBEIR-sr__NanoQuoraRetrieval.md), [sv](NanoBEIR-sv__NanoQuoraRetrieval.md), [th](NanoBEIR-th__NanoQuoraRetrieval.md), [vi](NanoBEIR-vi__NanoQuoraRetrieval.md) |
| NanoSCIDOCS | Scientific related-paper retrieval | [ar](NanoBEIR-ar__NanoSCIDOCS.md), [de](NanoBEIR-de__NanoSCIDOCS.md), [es](NanoBEIR-es__NanoSCIDOCS.md), [fr](NanoBEIR-fr__NanoSCIDOCS.md), [it](NanoBEIR-it__NanoSCIDOCS.md), [ja](NanoBEIR-ja__NanoSCIDOCS.md), [ko](NanoBEIR-ko__NanoSCIDOCS.md), [no](NanoBEIR-no__NanoSCIDOCS.md), [pt](NanoBEIR-pt__NanoSCIDOCS.md), [sr](NanoBEIR-sr__NanoSCIDOCS.md), [sv](NanoBEIR-sv__NanoSCIDOCS.md), [th](NanoBEIR-th__NanoSCIDOCS.md), [vi](NanoBEIR-vi__NanoSCIDOCS.md) |
| NanoSciFact | Evidence retrieval | [ar](NanoBEIR-ar__NanoSciFact.md), [de](NanoBEIR-de__NanoSciFact.md), [es](NanoBEIR-es__NanoSciFact.md), [fr](NanoBEIR-fr__NanoSciFact.md), [it](NanoBEIR-it__NanoSciFact.md), [ja](NanoBEIR-ja__NanoSciFact.md), [ko](NanoBEIR-ko__NanoSciFact.md), [no](NanoBEIR-no__NanoSciFact.md), [pt](NanoBEIR-pt__NanoSciFact.md), [sr](NanoBEIR-sr__NanoSciFact.md), [sv](NanoBEIR-sv__NanoSciFact.md), [th](NanoBEIR-th__NanoSciFact.md), [vi](NanoBEIR-vi__NanoSciFact.md) |
| NanoTouche2020 | Argument retrieval | [ar](NanoBEIR-ar__NanoTouche2020.md), [de](NanoBEIR-de__NanoTouche2020.md), [es](NanoBEIR-es__NanoTouche2020.md), [fr](NanoBEIR-fr__NanoTouche2020.md), [it](NanoBEIR-it__NanoTouche2020.md), [ja](NanoBEIR-ja__NanoTouche2020.md), [ko](NanoBEIR-ko__NanoTouche2020.md), [no](NanoBEIR-no__NanoTouche2020.md), [pt](NanoBEIR-pt__NanoTouche2020.md), [sr](NanoBEIR-sr__NanoTouche2020.md), [sv](NanoBEIR-sv__NanoTouche2020.md), [th](NanoBEIR-th__NanoTouche2020.md), [vi](NanoBEIR-vi__NanoTouche2020.md) |

## Interpretation Notes for Model Researchers

The strongest use of MNanoBEIR is controlled comparison. Because every language
uses the same task grid, score differences can be read as language robustness
only after accounting for the task family. A model may be excellent on
translated Quora duplicates yet weak on translated finance QA or scientific
related-paper retrieval. Family-level breakdowns are therefore more useful than
one global average.

Pay special attention to profile changes. BM25-led rows suggest exact strings,
entities, or many positives. Dense-led rows suggest paraphrase and semantic
answerability. Hybrid-led rows suggest that sparse and dense retrieval recover
different useful candidates. For reranker research, `reranking_hybrid` is often
the most relevant candidate pool even when dense has the best top-rank nDCG.

## Training and Leakage Notes

Useful training data should be both multilingual and task-matched: translated
MS MARCO-style query-passage data for web retrieval, multilingual FEVER-style
claim-evidence pairs for fact checking, duplicate-question pairs for Quora-like
tasks, argument-counterargument pairs for ArguAna, and biomedical or scientific
retrieval data for NFCorpus and SCIDOCS. Mixing all tasks into one generic
similarity objective will blur the distinctions this group is designed to test.

Leakage risk is high because the underlying BEIR tasks are common in retrieval
training mixtures. Exclude exact MNanoBEIR queries, qrels, positives, translated
documents, and direct translations of evaluation text. Audit overlap with MS
MARCO, NQ, FEVER, Quora, NFCorpus, SCIDOCS, SciFact, and Touche-style corpora
before using them for training or synthetic-data seeding.

## Public Sources

- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595), 2025.
- [NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [MTEB benchmark](https://github.com/embeddings-benchmark/mteb).

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR collection |  | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
| MTEB benchmark |  | project | https://github.com/embeddings-benchmark/mteb |
