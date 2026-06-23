# NanoMTEB-Misc

## Overview

NanoMTEB-Misc is a mixed multilingual retrieval group for NanoMTEB-family tasks
that do not belong cleanly to one language-specific benchmark set. It combines
NeuCLIR 2022 Persian, Russian, and Chinese news retrieval; RuSciBench Russian
scientific citation and co-citation retrieval; EuroPIRQ English, Finnish, and
Portuguese legal passage retrieval; and German-French CLSD translation-pair
retrieval from WMT19 and WMT21.

The group contains 1,636 queries, 99,624 task-local documents, and 7,538
positive qrel rows. It should be read as a stress test for mixed relevance
definitions rather than as one coherent domain benchmark. Some tasks have broad
multi-positive news or citation relevance, while others are single-positive
legal question retrieval or cross-lingual translation-equivalence retrieval.

## What This Group Measures

The group measures robustness across source families. The NeuCLIR tasks ask a
model to retrieve many relevant target-language news articles from Persian,
Russian, or Chinese topic statements. RuSciBench tasks use Russian scientific
paper relations derived from citation graphs. EuroPIRQ tasks retrieve EU legal
or administrative passages from synthetic questions in English, Finnish, and
Portuguese. CLSD tasks retrieve the true German-French or French-German
translation counterpart among close distractors.

Because the relevance relation changes from task to task, aggregate scores are
only a starting point. A model can look strong by excelling at cross-lingual
sentence retrieval while still struggling with broad news relevance or citation
graph retrieval. Conversely, a sparse system can be competitive on legal
passages while failing on translation-pair retrieval where exact word overlap is
mostly unavailable.

## Task Families

- **NeuCLIR 2022 news retrieval:** `2022_fa`, `2022_ru`, and `2022_zh` retrieve
  Persian, Russian, and Chinese news articles from TREC-style information
  needs.
- **Russian scientific graph retrieval:** `cite_ru` retrieves directly cited
  papers; `cocite_ru` retrieves co-cited papers.
- **EuroPIRQ legal passage retrieval:** `en`, `fi`, and `pt` retrieve English,
  Finnish, and Portuguese EU legal or administrative passages.
- **CLSD translation retrieval:** `wmt19_de_fr`, `wmt19_fr_de`,
  `wmt21_de_fr`, and `wmt21_fr_de` retrieve German-French translation pairs.

## Dataset Shape

The group has twelve task pages. The NeuCLIR and RuSciBench tasks are
multi-positive: NeuCLIR topics can have dozens of relevant news articles, and
RuSciBench tasks use five positive papers per query. EuroPIRQ and CLSD are
single-positive, so a query is expected to retrieve one target passage or
translation counterpart.

Text length and corpus shape vary sharply. RuSciBench queries are long
title-plus-abstract scientific texts. NeuCLIR documents are long news articles.
EuroPIRQ documents are formal legal paragraphs. CLSD documents are short
translated sentences. This variation makes NanoMTEB-Misc especially sensitive
to tokenization, truncation, multilingual representation quality, and whether a
model was trained on sentence-pair or document-retrieval supervision.

## Retrieval Behavior

### BM25 Profile

BM25 is strongest on the EuroPIRQ legal tasks. It is the best profile for
`fi`, and it remains very close to the best profile for `en` and `pt`. The legal
questions often preserve distinctive terms, institutions, dates, or entities
from the target passage, which gives sparse retrieval a clear lexical signal.
BM25 also remains useful for RuSciBench, where Russian title and abstract terms
overlap with related scientific papers.

BM25 is weak on the CLSD translation tasks, especially compared with dense
retrieval. This is expected because cross-lingual sentence retrieval gives BM25
few shared tokens beyond names, numbers, and international terms. It is also
limited on NeuCLIR Chinese and Persian, where broad topic relevance and long
news articles do not reduce to direct token overlap. The query-weighted BM25
nDCG@10 is 0.4700, making it a useful baseline but not the dominant retrieval
profile for this group.

### Dense Profile

Dense retrieval with `harrier-oss-270m` is the strongest query-weighted profile:
0.7842 nDCG@10 and 0.9273 hit@10. Its advantage is most visible on the CLSD
tasks. The four German-French translation retrieval tasks score between 0.8954
and 0.9574 nDCG@10 with dense retrieval, while BM25 stays much lower. This
suggests that the dense model captures cross-lingual semantic equivalence much
better than lexical overlap can.

Dense is also best on all three NeuCLIR tasks and on `cite_ru`. For NeuCLIR,
embedding similarity helps connect information needs with relevant news
articles even when vocabulary differs. For citation retrieval, dense similarity
captures topic and abstract-level relatedness. Dense is weaker than BM25 on
`fi` and slightly weaker than hybrid on `en`, but its overall dominance makes
NanoMTEB-Misc a strong multilingual semantic retrieval diagnostic.

### Reranking Hybrid Profile

The reranking hybrid profile has the best query-weighted recall@100 at 0.9019,
but it is not the best nDCG@10 profile overall. It is best on `2022_ru`, `en`,
and `cocite_ru`, where sparse and dense retrieval appear to recover
complementary candidates. The Russian NeuCLIR and co-citation tasks are good
examples of hybrid search helping when exact terms and semantic relatedness both
matter.

Hybrid underperforms dense on the CLSD tasks because dense retrieval already
captures the translation relation very strongly, while sparse evidence is weak.
It also trails dense on Persian and Chinese NeuCLIR. The pattern is therefore
not "hybrid always wins"; rather, hybrid is useful for candidate coverage and
mixed evidence retrieval, while dense ranking is often better for cross-lingual
semantic equivalence.

## Task Summary

| Task | Family | Language | Queries | Docs | Positives | Positives/query | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [2022_fa](2022_fa.md) | NeuCLIR news retrieval | `fa` | 45 | 8,882 | 1,131 | 25.13 | 0.2600 | 0.4915 | 0.4138 | Dense |
| [2022_ru](2022_ru.md) | NeuCLIR news retrieval | `ru` | 44 | 8,722 | 1,664 | 37.82 | 0.3490 | 0.5807 | 0.6011 | Reranking hybrid |
| [2022_zh](2022_zh.md) | NeuCLIR news retrieval | `zh` | 47 | 10,000 | 1,643 | 34.96 | 0.2931 | 0.5101 | 0.4072 | Dense |
| [cite_ru](cite_ru.md) | Scientific citation retrieval | `ru` | 200 | 10,000 | 1,000 | 5.00 | 0.5566 | 0.6182 | 0.6134 | Dense |
| [cocite_ru](cocite_ru.md) | Scientific co-citation retrieval | `ru` | 200 | 10,000 | 1,000 | 5.00 | 0.3920 | 0.4249 | 0.4346 | Reranking hybrid |
| [en](en.md) | EU legal passage retrieval | `en` | 100 | 9,422 | 100 | 1.00 | 0.9414 | 0.9255 | 0.9438 | Reranking hybrid |
| [fi](fi.md) | EU legal passage retrieval | `fi` | 100 | 9,422 | 100 | 1.00 | 0.9092 | 0.8542 | 0.8813 | BM25 |
| [pt](pt.md) | EU legal passage retrieval | `pt` | 100 | 9,517 | 100 | 1.00 | 0.9186 | 0.8623 | 0.8901 | BM25 |
| [wmt19_de_fr](wmt19_de_fr.md) | Translation retrieval | `multilingual` | 200 | 7,364 | 200 | 1.00 | 0.2204 | 0.9151 | 0.5447 | Dense |
| [wmt19_fr_de](wmt19_fr_de.md) | Translation retrieval | `multilingual` | 200 | 7,365 | 200 | 1.00 | 0.3078 | 0.9574 | 0.6054 | Dense |
| [wmt21_de_fr](wmt21_de_fr.md) | Translation retrieval | `multilingual` | 200 | 4,465 | 200 | 1.00 | 0.3127 | 0.9249 | 0.5988 | Dense |
| [wmt21_fr_de](wmt21_fr_de.md) | Translation retrieval | `multilingual` | 200 | 4,465 | 200 | 1.00 | 0.4658 | 0.8954 | 0.6999 | Dense |

## Interpretation Notes for Model Researchers

NanoMTEB-Misc is a good place to look for failure modes hidden by average
scores. Dense models that handle German-French sentence equivalence well can
score very highly on the CLSD block, but that does not imply strong NeuCLIR
news retrieval or Russian citation retrieval. Sparse systems can look strong on
EuroPIRQ legal passages while failing cross-lingual translation retrieval.

The group also highlights different uses of many positives. NeuCLIR evaluates
broad ad hoc relevance with dozens of positives per topic, while RuSciBench
uses graph-derived scientific relations. These are not the same retrieval
problem. Researchers should inspect task-family means and not rely solely on
the overall NanoMTEB-Misc score.

## Training and Leakage Notes

Training should be source-family specific. NeuCLIR benefits from multilingual
news retrieval and same-event hard negatives. RuSciBench benefits from
citation, co-citation, and scientific abstract representation learning.
EuroPIRQ benefits from EU legal question-passage pairs and legal boilerplate
negatives. CLSD benefits from German-French bitext retrieval and semantically
close translation distractors.

Leakage control should exclude Nano queries, qrels, and positive documents from
NeuCLIR, RuSciBench, EuroPIRQ, and CLSD/WMT-derived sources. Synthetic data
should preserve the original relevance relation: broad news topics with many
articles, citation-graph relations, legal question-to-passage mapping, and true
translation equivalence with close cross-lingual negatives.

## Public Sources

- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), 2023.
- [Overview of the TREC 2022 NeuCLIR Track](https://arxiv.org/abs/2304.12367), 2023.
- [NeuCLIR official site](https://neuclir.github.io/).
- [RuSciBench: Open Benchmark for Russian and English Scientific Document Representations](https://doi.org/10.1134/S1064562424602191), 2024.
- [EuroPIRQ-retrieval](https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval), 2025.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595), 2025.
- [Cross-Lingual Semantic Discrimination for Building Better Multilingual Embeddings](https://arxiv.org/abs/2502.08638), 2025.
- [Andrianos/clsd_wmt19_21](https://huggingface.co/datasets/Andrianos/clsd_wmt19_21).
- [mteb/NeuCLIR2022RetrievalHardNegatives](https://huggingface.co/datasets/mteb/NeuCLIR2022RetrievalHardNegatives).
- [mlsa-iai-msu-lab/ru_sci_bench_cite_retrieval](https://huggingface.co/datasets/mlsa-iai-msu-lab/ru_sci_bench_cite_retrieval).
- [mlsa-iai-msu-lab/ru_sci_bench_cocite_retrieval](https://huggingface.co/datasets/mlsa-iai-msu-lab/ru_sci_bench_cocite_retrieval).

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |
| Overview of the TREC 2022 NeuCLIR Track | 2023 | source task paper | [https://arxiv.org/abs/2304.12367](https://arxiv.org/abs/2304.12367) |
| NeuCLIR official site |  | project page | [https://neuclir.github.io/](https://neuclir.github.io/) |
| RuSciBench: Open Benchmark for Russian and English Scientific Document Representations | 2024 | source task paper | [https://doi.org/10.1134/S1064562424602191](https://doi.org/10.1134/S1064562424602191) |
| EuroPIRQ-retrieval | 2025 | dataset card | [https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval](https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| Cross-Lingual Semantic Discrimination for Building Better Multilingual Embeddings | 2025 | source task paper | [https://arxiv.org/abs/2502.08638](https://arxiv.org/abs/2502.08638) |
| Andrianos/clsd_wmt19_21 |  | dataset card | [https://huggingface.co/datasets/Andrianos/clsd_wmt19_21](https://huggingface.co/datasets/Andrianos/clsd_wmt19_21) |
| mteb/NeuCLIR2022RetrievalHardNegatives |  | dataset card | [https://huggingface.co/datasets/mteb/NeuCLIR2022RetrievalHardNegatives](https://huggingface.co/datasets/mteb/NeuCLIR2022RetrievalHardNegatives) |
| mlsa-iai-msu-lab/ru_sci_bench_cite_retrieval |  | dataset card | [https://huggingface.co/datasets/mlsa-iai-msu-lab/ru_sci_bench_cite_retrieval](https://huggingface.co/datasets/mlsa-iai-msu-lab/ru_sci_bench_cite_retrieval) |
| mlsa-iai-msu-lab/ru_sci_bench_cocite_retrieval |  | dataset card | [https://huggingface.co/datasets/mlsa-iai-msu-lab/ru_sci_bench_cocite_retrieval](https://huggingface.co/datasets/mlsa-iai-msu-lab/ru_sci_bench_cocite_retrieval) |
