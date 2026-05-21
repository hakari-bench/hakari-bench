# NanoMTEB-Misc

## Overview

NanoMTEB-Misc is a multilingual collection of NanoMTEB-family retrieval tasks
that do not fit cleanly into one official language benchmark family. It combines
four source families: NeuCLIR 2022 Persian/Russian/Chinese news retrieval,
RuSciBench Russian scientific citation and co-citation retrieval, EuroPIRQ
English/Finnish/Portuguese EU legal passage retrieval, and CLSD WMT19/WMT21
German-French cross-lingual sentence discrimination.

The group is useful as a stress test for mixed retrieval behavior. It includes
multi-positive news retrieval, graph-derived scientific citation relevance,
single-positive legal synthetic question retrieval, and cross-lingual
translation-equivalence retrieval. A single group score therefore reflects both
multilingual coverage and very different relevance definitions.

## Details

### What the Original Group Measures

The group does not come from one benchmark paper. NeuCLIR 2022 measures ad hoc
retrieval over Persian, Russian, and Chinese news articles with broad
TREC-style information needs and many relevant documents. RuSciBench measures
Russian scientific document representations using citation-graph relations:
direct citations and co-citations. EuroPIRQ measures synthetic question-to-
passage retrieval over DGT-Acquis European Union legal and administrative text
in English, Finnish, and Portuguese. CLSD measures cross-lingual semantic
discrimination, where a sentence in one language retrieves its true translation
among semantically close distractors.

These differences matter. In the NeuCLIR splits, a query can have up to 100
relevant news articles. In RuSciBench, each query paper has five graph-derived
positive papers. In EuroPIRQ and CLSD, each query has exactly one positive.
The retrieval target ranges from long news articles and Russian abstracts to
formal EU paragraphs and short German-French translated news sentences.

### Subtask Coverage

The twelve subtasks cover four retrieval families:

- **NeuCLIR 2022 news retrieval:** `2022_fa`, `2022_ru`, and `2022_zh` use
  Persian, Russian, and Chinese topic statements to retrieve target-language
  news articles from hard-negative candidate pools.
- **Russian scientific graph retrieval:** `cite_ru` retrieves directly cited
  papers, while `cocite_ru` retrieves co-cited papers from RuSciBench.
- **EuroPIRQ legal passage retrieval:** `en`, `fi`, and `pt` retrieve
  English, Finnish, and Portuguese EU legal or administrative passages from
  synthetic questions.
- **CLSD German-French sentence retrieval:** `wmt19_de_fr`, `wmt19_fr_de`,
  `wmt21_de_fr`, and `wmt21_fr_de` retrieve sentence-level translation
  counterparts across French and German.

This mixture makes the group broad but not homogeneous. It should be read as a
miscellaneous coverage group rather than a single coherent domain benchmark.

### Observed Group Profile

Across the twelve splits, NanoMTEB-Misc contains 1,636 queries, 99,624
split-local candidate documents, and 7,538 positive qrels. Query counts vary:
NeuCLIR has 44 to 47 queries per split, EuroPIRQ has 100 per language, and the
RuSciBench plus CLSD splits have 200 queries each.

The group is strongly affected by multi-positive tasks. The three NeuCLIR splits
and two RuSciBench splits are multi-positive, contributing 530 multi-positive
queries. NeuCLIR has broad relevance pools with up to 100 positives per query,
while RuSciBench fixes five positives per query. EuroPIRQ and CLSD are
single-positive and behave more like exact-pair retrieval.

The text-length profile also varies sharply. RuSciBench queries are long Russian
title-plus-abstract texts; `cite_ru` averages 1,399.06 query characters. NeuCLIR
documents are long news articles, especially Persian and Russian. CLSD documents
are short translated sentences, while EuroPIRQ documents are mid-length legal
paragraphs. These differences make a single truncation or tokenization strategy
risky for the whole group.

### BM25 Difficulty

Query-weighted BM25 nDCG@10 is 0.4315 and query-weighted hit@10 is 0.6229.
The unweighted task means are slightly higher, with nDCG@10 at 0.4608 and
hit@10 at 0.6450. `en` EuroPIRQ is easiest by nDCG@10 at 0.9491, because
synthetic English legal questions often preserve distinctive legal terms,
names, dates, or institutions from the target passage.

The hardest task by nDCG@10 is `wmt19_de_fr` at 0.2053. This is expected:
BM25 has little cross-lingual signal beyond names, numbers, and shared
international terms. `2022_zh` is also difficult at 0.2212 because Chinese news
topics are short and the relevant article pool is broad. In the loaded data,
the first Russian NeuCLIR positive was only at rank 97 and the first Chinese
NeuCLIR positive at rank 93, while EuroPIRQ English had its first positive at
rank 1. The group therefore spans both lexically easy legal retrieval and
semantically difficult multilingual retrieval.

### Training Data That May Help

Training data should be source-family specific. NeuCLIR tasks benefit from
Persian, Russian, and Chinese news retrieval, CLIR-style topic-document pairs,
and same-event hard negatives. RuSciBench benefits from citation-graph
supervision, Russian scientific abstracts, and SPECTER-style citation or
co-citation objectives. EuroPIRQ benefits from EU legal and administrative
passage retrieval and synthetic question-passage data. CLSD benefits from
German-French bitext retrieval, sentence-level contrastive learning, and hard
distractors that preserve entities while changing the meaning.

Training should exclude NanoMTEB-Misc evaluation queries, qrels, and positive
documents. The public benchmark sources should be treated as potential leakage
sources unless overlap has been audited, especially NeuCLIR topic judgments,
RuSciBench citation pairs, EuroPIRQ generated questions, and CLSD WMT sentence
pairs.

### Synthetic Data Guidance

Synthetic data should follow the source relation rather than using one generic
question-answer template. NeuCLIR-style examples should have broad information
needs and multiple relevant news articles. RuSciBench-style examples should use
known or carefully simulated citation/co-citation relations, not arbitrary
same-topic papers. EuroPIRQ-style examples should generate questions from EU
legal paragraphs and include near-duplicate legal boilerplate as negatives.
CLSD-style examples should use true German-French translation pairs with
semantically close distractors that alter actor, number, polarity, or event.

Do not use NanoMTEB-Misc examples as seeds for generation. For all four source
families, hard negatives should be close enough that lexical overlap alone is
not sufficient.

## Task Summary

| Task | Retrieval shape | Queries | Docs | Positives | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars | Source status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [2022_fa](2022_fa.md) | Persian topic to Persian news articles | 45 | 8,882 | 1,131 | 0.2890 | 0.5778 | 83.13 | 2,818.76 | NeuCLIR paper |
| [2022_ru](2022_ru.md) | Russian topic to Russian news articles | 44 | 8,722 | 1,664 | 0.3182 | 0.7273 | 85.57 | 2,448.87 | NeuCLIR paper |
| [2022_zh](2022_zh.md) | Chinese topic to Chinese news articles | 47 | 10,000 | 1,643 | 0.2212 | 0.2553 | 24.00 | 1,107.60 | NeuCLIR paper |
| [cite_ru](cite_ru.md) | Russian paper to directly cited papers | 200 | 10,000 | 1,000 | 0.5081 | 0.8750 | 1,399.06 | 926.86 | RuSciBench paper |
| [cocite_ru](cocite_ru.md) | Russian paper to co-cited papers | 200 | 10,000 | 1,000 | 0.3593 | 0.7150 | 961.80 | 908.88 | RuSciBench paper |
| [en](en.md) | English legal question to EU passage | 100 | 9,422 | 100 | 0.9491 | 0.9700 | 140.43 | 550.09 | EuroPIRQ card |
| [fi](fi.md) | Finnish legal question to EU passage | 100 | 9,422 | 100 | 0.8493 | 0.9200 | 146.53 | 594.55 | EuroPIRQ card |
| [pt](pt.md) | Portuguese legal question to EU passage | 100 | 9,517 | 100 | 0.9189 | 0.9800 | 149.75 | 583.83 | EuroPIRQ card |
| [wmt19_de_fr](wmt19_de_fr.md) | French sentence to German translation | 200 | 7,364 | 200 | 0.2053 | 0.3150 | 159.09 | 147.49 | CLSD paper |
| [wmt19_fr_de](wmt19_fr_de.md) | German sentence to French translation | 200 | 7,365 | 200 | 0.2660 | 0.4200 | 148.98 | 154.22 | CLSD paper |
| [wmt21_de_fr](wmt21_de_fr.md) | French sentence to German translation | 200 | 4,465 | 200 | 0.2167 | 0.3500 | 170.06 | 177.26 | CLSD paper |
| [wmt21_fr_de](wmt21_fr_de.md) | German sentence to French translation | 200 | 4,465 | 200 | 0.4283 | 0.6350 | 174.99 | 174.45 | CLSD paper |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Misc |
| Backing dataset | NanoMTEB-Misc |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Misc](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Misc) |
| Language | multilingual |
| Category | natural_language |
| Subtasks | 12 |
| Total queries | 1,636 |
| Split-local documents | 99,624 |
| Positive qrels | 7,538 |
| Positives per query | avg 4.6076, median varies by source family, max 100 |
| Multi-positive subtasks | 5 of 12 |
| Multi-positive queries | 530 |
| Query-weighted BM25 nDCG@10 | 0.4315 |
| Query-weighted BM25 hit@10 | 0.6229 |
| Mean query length | 400.43 chars, weighted by query count |
| Mean document length | 963.24 chars, weighted by split-local document count |

### Public Sources

- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316); 2023 benchmark context.
- [Overview of the TREC 2022 NeuCLIR Track](https://arxiv.org/abs/2304.12367); NeuCLIR source paper.
- [NeuCLIR official site](https://neuclir.github.io/); project page.
- [RuSciBench: Open Benchmark for Russian and English Scientific Document Representations](https://doi.org/10.1134/S1064562424602191); RuSciBench source paper.
- [EuroPIRQ-retrieval](https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval); dataset card.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); multilingual benchmark context.
- [Cross-Lingual Semantic Discrimination for Building Better Multilingual Embeddings](https://arxiv.org/abs/2502.08638); CLSD source paper.
- [Andrianos/clsd_wmt19_21](https://huggingface.co/datasets/Andrianos/clsd_wmt19_21); CLSD WMT dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Misc](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Misc)
- Source datasets:
  [mteb/NeuCLIR2022RetrievalHardNegatives](https://huggingface.co/datasets/mteb/NeuCLIR2022RetrievalHardNegatives),
  [mlsa-iai-msu-lab/ru_sci_bench_cite_retrieval](https://huggingface.co/datasets/mlsa-iai-msu-lab/ru_sci_bench_cite_retrieval),
  [mlsa-iai-msu-lab/ru_sci_bench_cocite_retrieval](https://huggingface.co/datasets/mlsa-iai-msu-lab/ru_sci_bench_cocite_retrieval),
  [eherra/EuroPIRQ-retrieval](https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval),
  [Andrianos/clsd_wmt19_21](https://huggingface.co/datasets/Andrianos/clsd_wmt19_21).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| Overview of the TREC 2022 NeuCLIR Track | 2023 | source task paper | https://arxiv.org/abs/2304.12367 |
| NeuCLIR official site |  | project page | https://neuclir.github.io/ |
| RuSciBench: Open Benchmark for Russian and English Scientific Document Representations | 2024 | source task paper | https://doi.org/10.1134/S1064562424602191 |
| EuroPIRQ-retrieval | 2025 | dataset card | https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| Cross-Lingual Semantic Discrimination for Building Better Multilingual Embeddings | 2025 | source task paper | https://arxiv.org/abs/2502.08638 |
| Andrianos/clsd_wmt19_21 |  | dataset card | https://huggingface.co/datasets/Andrianos/clsd_wmt19_21 |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoMTEB-Misc
  backing_dataset: NanoMTEB-Misc
  dataset_id: hakari-bench/NanoMTEB-Misc
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Misc/index.md
  source_research:
    primary_source_type: mixed_task_papers_and_dataset_cards
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 12
    queries: 1636
    split_local_documents: 99624
    positive_qrels: 7538
  positives_per_query:
    average: 4.60757946210269
    min: 1
    median: null
    max: 100
    multi_positive_tasks: 5
    multi_positive_queries: 530
  text_stats_chars:
    query_mean_weighted_by_queries: 400.4284413202934
    document_mean_weighted_by_documents: 963.2428978960894
  bm25:
    ndcg_at_10_query_weighted: 0.4314622249388753
    hit_at_10_query_weighted: 0.6228614303178485
    ndcg_at_10_unweighted_task_mean: 0.4607833333333333
    hit_at_10_unweighted_task_mean: 0.6450333333333333
    source: dataset_bm25_column
    easiest_task_by_ndcg_at_10: en
    hardest_task_by_ndcg_at_10: wmt19_de_fr
  tasks:
    - name: 2022_fa
      path: docs/benchmark_tasks/NanoMTEB-Misc/2022_fa.md
      retrieval_shape: persian_topic_to_persian_news_articles
      queries: 45
      documents: 8882
      positive_qrels: 1131
      bm25_ndcg_at_10: 0.289
      bm25_hit_at_10: 0.5778
    - name: 2022_ru
      path: docs/benchmark_tasks/NanoMTEB-Misc/2022_ru.md
      retrieval_shape: russian_topic_to_russian_news_articles
      queries: 44
      documents: 8722
      positive_qrels: 1664
      bm25_ndcg_at_10: 0.3182
      bm25_hit_at_10: 0.7273
    - name: 2022_zh
      path: docs/benchmark_tasks/NanoMTEB-Misc/2022_zh.md
      retrieval_shape: chinese_topic_to_chinese_news_articles
      queries: 47
      documents: 10000
      positive_qrels: 1643
      bm25_ndcg_at_10: 0.2212
      bm25_hit_at_10: 0.2553
    - name: cite_ru
      path: docs/benchmark_tasks/NanoMTEB-Misc/cite_ru.md
      retrieval_shape: russian_paper_to_directly_cited_papers
      queries: 200
      documents: 10000
      positive_qrels: 1000
      bm25_ndcg_at_10: 0.5081
      bm25_hit_at_10: 0.875
    - name: cocite_ru
      path: docs/benchmark_tasks/NanoMTEB-Misc/cocite_ru.md
      retrieval_shape: russian_paper_to_co_cited_papers
      queries: 200
      documents: 10000
      positive_qrels: 1000
      bm25_ndcg_at_10: 0.3593
      bm25_hit_at_10: 0.715
    - name: en
      path: docs/benchmark_tasks/NanoMTEB-Misc/en.md
      retrieval_shape: english_legal_question_to_eu_passage
      queries: 100
      documents: 9422
      positive_qrels: 100
      bm25_ndcg_at_10: 0.9491
      bm25_hit_at_10: 0.97
    - name: fi
      path: docs/benchmark_tasks/NanoMTEB-Misc/fi.md
      retrieval_shape: finnish_legal_question_to_eu_passage
      queries: 100
      documents: 9422
      positive_qrels: 100
      bm25_ndcg_at_10: 0.8493
      bm25_hit_at_10: 0.92
    - name: pt
      path: docs/benchmark_tasks/NanoMTEB-Misc/pt.md
      retrieval_shape: portuguese_legal_question_to_eu_passage
      queries: 100
      documents: 9517
      positive_qrels: 100
      bm25_ndcg_at_10: 0.9189
      bm25_hit_at_10: 0.98
    - name: wmt19_de_fr
      path: docs/benchmark_tasks/NanoMTEB-Misc/wmt19_de_fr.md
      retrieval_shape: french_sentence_to_german_translation
      queries: 200
      documents: 7364
      positive_qrels: 200
      bm25_ndcg_at_10: 0.2053
      bm25_hit_at_10: 0.315
    - name: wmt19_fr_de
      path: docs/benchmark_tasks/NanoMTEB-Misc/wmt19_fr_de.md
      retrieval_shape: german_sentence_to_french_translation
      queries: 200
      documents: 7365
      positive_qrels: 200
      bm25_ndcg_at_10: 0.266
      bm25_hit_at_10: 0.42
    - name: wmt21_de_fr
      path: docs/benchmark_tasks/NanoMTEB-Misc/wmt21_de_fr.md
      retrieval_shape: french_sentence_to_german_translation
      queries: 200
      documents: 4465
      positive_qrels: 200
      bm25_ndcg_at_10: 0.2167
      bm25_hit_at_10: 0.35
    - name: wmt21_fr_de
      path: docs/benchmark_tasks/NanoMTEB-Misc/wmt21_fr_de.md
      retrieval_shape: german_sentence_to_french_translation
      queries: 200
      documents: 4465
      positive_qrels: 200
      bm25_ndcg_at_10: 0.4283
      bm25_hit_at_10: 0.635
  source_links:
    - label: MTEB paper
      url: https://arxiv.org/abs/2210.07316
    - label: NeuCLIR 2022 overview
      url: https://arxiv.org/abs/2304.12367
    - label: NeuCLIR official site
      url: https://neuclir.github.io/
    - label: RuSciBench paper
      url: https://doi.org/10.1134/S1064562424602191
    - label: EuroPIRQ dataset card
      url: https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval
    - label: MMTEB paper
      url: https://arxiv.org/abs/2502.13595
    - label: CLSD paper
      url: https://arxiv.org/abs/2502.08638
    - label: CLSD WMT dataset card
      url: https://huggingface.co/datasets/Andrianos/clsd_wmt19_21
```
