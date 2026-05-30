# NanoMTEB-Dutch

## Overview

NanoMTEB-Dutch is a compact Dutch retrieval group covering translated BEIR-NL
tasks, native Dutch MTEB tasks, cross-lingual Belebele retrieval, legal and
medical retrieval, scientific evidence retrieval, news and tender retrieval,
web FAQ retrieval, and Dutch Wikipedia retrieval. Ten of the twenty-seven tasks
are Dutch CQADupStack duplicate-question splits, but the group is broader than
duplicate QA.

The group should be read as both a Dutch-language benchmark and a translation
robustness benchmark. Some tasks are native Dutch resources, such as legal,
news, tender, FAQ, or bibliography retrieval. Others carry BEIR-style relevance
relations into Dutch. BM25 exposes exact Dutch terms and named entities; dense
retrieval tests paraphrase, translation, and cross-lingual matching;
`reranking_hybrid` is useful when sparse and dense candidates recover different
positives.

## What This Group Measures

NanoMTEB-Dutch follows Dutch retrieval coverage assembled for MTEB-NL and
BEIR-NL. It includes translated BEIR-style datasets, cross-lingual Belebele
directions, Dutch legal resources, Dutch news, public procurement, Flemish
academic bibliography, FAQ retrieval, and Wikipedia retrieval.

The group measures Dutch retrieval across task semantics. A relevant document
may be a duplicate question, a statute article, a FAQ answer, a news article,
a procurement notice, a scientific paper, a medical abstract, or a Wikipedia
passage. A model must preserve both Dutch lexical details and the original
task relation after translation or cross-lingual mapping.

## Task Families

- **Duplicate and argument retrieval:** `argu_ana_nl`, the ten
  `cqadupstack_*` tasks, and `quora`.
- **Cross-lingual and monolingual reading comprehension:** the three Belebele
  directions.
- **Legal retrieval:** `b_bsardnl` and `legal_qanl`.
- **Open-domain and encyclopedic retrieval:** `nq`, `fever`, and
  `wikipedia_multilingual_nl`.
- **Scientific and medical retrieval:** `nfcorpus_nl`, `sci_fact_nl`, and
  `scidocs_nl`.
- **News, procurement, bibliography, and FAQ retrieval:** `dutch_news_articles`,
  `open_tender`, `vabb`, and `web_faq_nld`.

## Dataset Shape

NanoMTEB-Dutch contains 27 task pages, 5,299 queries, 227,987 split-local
documents, and 13,018 positive qrel rows. Most tasks have 200 queries. The
group has a mix of single-positive and multi-positive tasks; NFCorpus, SCIDOCS,
Quora, LegalQA-NL, bBSARD, FEVER, and NQ require multi-positive interpretation.

Text lengths and formats are diverse. Argument queries are long, FAQ and web
queries are short, legal tasks contain formal statute language, CQADupStack
contains technical forum text, and scientific tasks contain paper or abstract
language. This makes task-family breakdown more useful than one aggregate
Dutch score.

## Retrieval Behavior

### BM25 Profile

BM25 is strongest on tasks with direct named entities, titles, article terms, or
Dutch surface overlap. FEVER, Dutch news, Wikipedia, Quora, LegalQA-NL, WebFAQ,
OpenTender, and VABB all show substantial sparse signal. BM25 is also useful on
same-language Belebele where question and passage share Dutch answer context.

BM25 is weaker on cross-lingual Belebele, bBSARD, SCIDOCS, and many
CQADupStack technical duplicate tasks. These require language alignment,
paraphrase, legal concept mapping, scientific relatedness, or duplicate intent
beyond exact word overlap.

### Dense Profile

Dense retrieval is the best profile for many Dutch tasks, especially
cross-lingual Belebele, Quora, WebFAQ, Wikipedia, VABB, NQ, SciFact, and several
CQADupStack splits. It helps when the Dutch query and document express the same
intent with different words, or when translated benchmark artifacts weaken
literal matching.

Dense retrieval still needs exact anchors. Legal articles, procurement notices,
scientific terms, and technical forum posts can depend on specific names,
codes, product terms, or statute phrases. Dense gains should be checked against
candidate recall for those anchors.

### Reranking Hybrid Profile

`reranking_hybrid` is strongest on same-language Belebele, LegalQA-NL, and
several CQADupStack tasks. It is most useful where exact Dutch terms and dense
paraphrase matching are both needed. For FAQ, Quora, and Wikipedia-style tasks,
hybrid remains competitive even when dense has the best nDCG@10.

For reranker experiments, multi-positive tasks such as NFCorpus, SCIDOCS,
Quora, and legal retrieval should be read with recall and candidate diversity
in mind, not only first-hit success.

## Task Summary

| Task | Family | Queries | Docs | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [argu_ana_nl](argu_ana_nl.md) | argument retrieval | 199 | 8,624 | 0.2970 | 0.3723 | 0.3529 | Dense |
| [b_bsardnl](b_bsardnl.md) | legal retrieval | 200 | 10,000 | 0.1249 | 0.2749 | 0.2234 | Dense |
| [belebele_eng_latn_nld_latn](belebele_eng_latn_nld_latn.md) | cross-lingual QA | 200 | 488 | 0.4738 | 0.8918 | 0.6283 | Dense |
| [belebele_nld_latn_eng_latn](belebele_nld_latn_eng_latn.md) | cross-lingual QA | 200 | 488 | 0.3288 | 0.9306 | 0.4456 | Dense |
| [belebele_nld_latn_nld_latn](belebele_nld_latn_nld_latn.md) | Dutch QA | 200 | 488 | 0.8364 | 0.8899 | 0.8999 | Reranking hybrid |
| [cqadupstack_android](cqadupstack_android.md) | duplicate question | 200 | 10,000 | 0.2944 | 0.3862 | 0.3836 | Dense |
| [cqadupstack_english](cqadupstack_english.md) | duplicate question | 200 | 10,000 | 0.2769 | 0.3587 | 0.3248 | Dense |
| [cqadupstack_gis](cqadupstack_gis.md) | duplicate question | 200 | 10,000 | 0.2790 | 0.3202 | 0.3272 | Reranking hybrid |
| [cqadupstack_mathematica](cqadupstack_mathematica.md) | duplicate question | 200 | 10,000 | 0.1826 | 0.1992 | 0.2181 | Reranking hybrid |
| [cqadupstack_physics](cqadupstack_physics.md) | duplicate question | 200 | 10,000 | 0.3269 | 0.4020 | 0.3756 | Dense |
| [cqadupstack_programmers](cqadupstack_programmers.md) | duplicate question | 200 | 10,000 | 0.2991 | 0.3906 | 0.3638 | Dense |
| [cqadupstack_stats](cqadupstack_stats.md) | duplicate question | 200 | 10,000 | 0.2827 | 0.3224 | 0.3337 | Reranking hybrid |
| [cqadupstack_tex](cqadupstack_tex.md) | duplicate question | 200 | 10,000 | 0.2106 | 0.2611 | 0.2926 | Reranking hybrid |
| [cqadupstack_webmasters](cqadupstack_webmasters.md) | duplicate question | 200 | 10,000 | 0.2307 | 0.2947 | 0.2968 | Reranking hybrid |
| [cqadupstack_wordpress](cqadupstack_wordpress.md) | duplicate question | 200 | 10,000 | 0.2608 | 0.3057 | 0.3371 | Reranking hybrid |
| [dutch_news_articles](dutch_news_articles.md) | news retrieval | 200 | 10,000 | 0.8868 | 0.8996 | 0.8954 | Dense |
| [fever](fever.md) | evidence retrieval | 200 | 10,000 | 0.9221 | 0.9207 | 0.9215 | BM25 |
| [legal_qanl](legal_qanl.md) | legal QA retrieval | 102 | 10,000 | 0.8143 | 0.8050 | 0.8455 | Reranking hybrid |
| [nfcorpus_nl](nfcorpus_nl.md) | biomedical retrieval | 199 | 3,593 | 0.2683 | 0.2590 | 0.2656 | BM25 |
| [nq](nq.md) | open-domain QA | 200 | 10,000 | 0.4505 | 0.6335 | 0.5473 | Dense |
| [open_tender](open_tender.md) | tender retrieval | 199 | 10,000 | 0.6712 | 0.6044 | 0.6556 | BM25 |
| [quora](quora.md) | duplicate question | 200 | 10,000 | 0.8391 | 0.9289 | 0.8772 | Dense |
| [sci_fact_nl](sci_fact_nl.md) | scientific evidence | 200 | 5,183 | 0.6160 | 0.6758 | 0.6709 | Dense |
| [scidocs_nl](scidocs_nl.md) | related scientific documents | 200 | 10,000 | 0.1335 | 0.2264 | 0.1835 | Dense |
| [vabb](vabb.md) | bibliography retrieval | 200 | 9,123 | 0.6952 | 0.7804 | 0.7540 | Dense |
| [web_faq_nld](web_faq_nld.md) | FAQ retrieval | 200 | 10,000 | 0.7698 | 0.8776 | 0.8442 | Dense |
| [wikipedia_multilingual_nl](wikipedia_multilingual_nl.md) | Wikipedia QA retrieval | 200 | 10,000 | 0.8444 | 0.8948 | 0.8840 | Dense |

## Interpretation Notes for Model Researchers

NanoMTEB-Dutch should be interpreted by source type. Translated BEIR tasks
stress whether the original relevance relation survives in Dutch. Native Dutch
legal, FAQ, news, tender, and bibliography tasks stress domain vocabulary and
local data conventions. Cross-lingual Belebele should be read separately from
same-language Dutch retrieval.

The BM25/dense profile is a useful diagnostic. BM25-led tasks show direct Dutch
surface anchors. Dense-led tasks show paraphrase, translation, or semantic
intent matching. Hybrid-led tasks show that both exact terms and semantic
alignment are needed for candidate generation.

## Training and Leakage Notes

Useful training data includes Dutch search logs, legal question-article pairs,
FAQ retrieval, translated BEIR-NL training data, duplicate-question pairs,
scientific and biomedical retrieval, and cross-lingual QA pairs. Hard negatives
should be drawn from same legal article families, same technical forums, same
scientific topic, or same answer-bearing article.

Exclude NanoMTEB-Dutch evaluation queries, positives, qrels, duplicate clusters,
translated test examples, statute articles, and source rows. Cross-lingual
tasks should avoid direct translations of evaluation queries as synthetic
training seeds.

## Public Sources

- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), 2022.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [Belebele: a Parallel Reading Comprehension Dataset in 122 Language Variants](https://arxiv.org/abs/2308.16884), 2023.

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| MTEB: Massive Text Embedding Benchmark | 2022 | paper | https://arxiv.org/abs/2210.07316 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | paper | https://arxiv.org/abs/2104.08663 |
| Belebele: a Parallel Reading Comprehension Dataset in 122 Language Variants | 2023 | paper | https://arxiv.org/abs/2308.16884 |
