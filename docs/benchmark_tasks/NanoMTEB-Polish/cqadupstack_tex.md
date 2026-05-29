# NanoMTEB-Polish / cqadupstack_tex

## Overview

`cqadupstack_tex` is a Polish duplicate-question retrieval task from the TeX
split of CQADupStack. Queries ask about LaTeX or TeX formatting, packages,
macros, links, table-of-contents behavior, and document layout. Relevant
documents are duplicate or equivalent TeX Stack Exchange posts.

## Details

### What the Original Data Measures

[CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://ir.webis.de/anthology/2015.adcs_conference-2015.3/)
defines the source family as duplicate community-question retrieval. The
[MTEB paper](https://arxiv.org/abs/2210.07316) includes CQADupStack in its
retrieval benchmark suite. The exact Polish TeX split is specified by the
MTEB/CLARIN dataset cards.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 843 positive qrels. Queries
average 50.30 characters and documents average 1,106.13 characters. The examples
show section-title hyphenation, paragraph spacing, `\include` and table of
contents behavior, clickable PDF links, and blank lines in alignment
environments. Multi-positive clusters are common, with 94 queries having more
than one positive.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.2615 and hit@10 = 0.4350, with 51 positives at rank 1
and 87 in the top 10. Package names and commands provide lexical anchors, but
duplicate questions can share only the intended formatting effect rather than
the same macro names.

### Training Data That May Help

Useful data includes non-overlapping TeX Stack Exchange duplicate pairs,
Polish LaTeX help questions, documentation retrieval pairs, and hard negatives
with the same command or package but a different rendering issue. Exclude
evaluation queries and positive posts.

### Synthetic Data Guidance

Generate Polish LaTeX troubleshooting posts with realistic preambles, commands,
packages, and output symptoms. Synthetic duplicates should preserve the same
layout or compilation problem while changing document class, package stack, or
minimal example wording.

## Example Data

| Query | Positive document |
| --- | --- |
| BibLaTeX: bibliografia główna i drugorzędna (43 chars) | biblatex: drukowanie oddzielnych bibliografii Używam `biblatex` i mam to ustawione tak: W moim pliku bib mam 3 rodzaje wpisów, online, broszura i książka. A w mojej pracy dyplomowej chcę je wydrukować osobno w następujący spo ... [truncated 225 chars](797 chars) |
| Jak mogę przyspieszyć kompilację dokumentu z wieloma obrazami? (62 chars) | Pomiń przetwarzanie wszystkich obrazów Próbuję zrobić szkic, zmuszając LaTeX do ignorowania wszystkich obrazów. Jak mam powiedzieć LaTeX, aby pominął wszystkie nazwy plików obrazów (w poleceniu `\includegraphics`) i po prostu ... [truncated 225 chars](398 chars) |
| Puste linie w wyrównanym środowisku (35 chars) | Błąd w wyrównaniu środowiska - niekontrolowany argument? > **Possible Duplicate:** > Puste linie w środowisku wyrównania \documentclass[12pt,a4paper]{article} \usepackage[wersja=3]{mhchem} \usepackage{siunitx} \begin{document ... [truncated 225 chars](488 chars) |
| alternatywa slashbox (20 chars) | Tworzenie tabeli, jak pokazano na rysunku Chcę utworzyć tabelę w LaTeX, która zaczyna się tak, jak pokazano na poniższym rysunku. Jak to zrobić, korzystając z pakietu tabel/tabel? Zrobiłem to za pomocą TikZ, ale jestem pewien ... [truncated 225 chars](295 chars) |
| Umieszczanie innego obrazu w każdym rogu strony (47 chars) | flipbook w pracy magisterskiej Właśnie piszę pracę magisterską z informatyki na temat wizualizacji. Ponieważ sednem mojej pracy magisterskiej jest złożona wizualizacja 3D, która wysyła wiadomość tylko poprzez interakcję z uży ... [truncated 225 chars](2698 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Polish |
| Backing dataset | NanoMTEB-Polish |
| Task / split | cqadupstack_tex |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish) |
| Source dataset | [mteb/CQADupstack-Tex-PL](https://huggingface.co/datasets/mteb/CQADupstack-Tex-PL) |
| Language | pl |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 843 |
| Avg positives / query | 4.215 |
| Positives per query (min / median / max) | 1 / 1.0 / 100 |
| Queries with multiple positives | 94 (47.0%) |
| BM25 nDCG@10 | 0.2555 |
| BM25 hit@10 | 0.4300 |
| BM25 Recall@100 | 0.3405 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2805 |
| Dense hit@10 | 0.4800 |
| Dense Recall@100 | 0.4033 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3147 |
| Reranking hybrid hit@10 | 0.5450 |
| Reranking hybrid Recall@100 | 0.4282 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 50 |
| Query length avg chars | 50.30 |
| Document length avg chars | 1,106.13 |

### Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://ir.webis.de/anthology/2015.adcs_conference-2015.3/), original benchmark paper record.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), benchmark paper covering CQADupStack retrieval tasks.
- [CLARIN-KNEXT cqadupstack-tex-pl](https://huggingface.co/datasets/clarin-knext/cqadupstack-tex-pl), Polish source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish)
- Source task dataset: [mteb/CQADupstack-Tex-PL](https://huggingface.co/datasets/mteb/CQADupstack-Tex-PL)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | task paper | https://ir.webis.de/anthology/2015.adcs_conference-2015.3/ |
| MTEB: Massive Text Embedding Benchmark | 2022 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| CLARIN-KNEXT cqadupstack-tex-pl |  | dataset card | https://huggingface.co/datasets/clarin-knext/cqadupstack-tex-pl |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Polish
  backing_dataset: NanoMTEB-Polish
  dataset_id: hakari-bench/NanoMTEB-Polish
  task_name: cqadupstack_tex
  split_name: cqadupstack_tex
  language: pl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Polish/cqadupstack_tex.md
  source_research:
    primary_source_type: dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone paper for this Polish translated split was confirmed
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 843
  positives_per_query:
    average: 4.215
    min: 1
    median: 1.0
    max: 100
    multi_positive_queries: 94
    multi_positive_query_percent: 47.0
  text_stats_chars:
    query_mean: 50.3
    document_mean: 1106.1253
  bm25:
    ndcg_at_10: 0.2554989437084018
    hit_at_10: 0.43
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2554989437
      hit_at_10: 0.43
      recall_at_100: 0.3404507711
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.3404507711
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2805258472
      hit_at_10: 0.48
      recall_at_100: 0.4033214709
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4033214709
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3147204035
      hit_at_10: 0.545
      recall_at_100: 0.428232503
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.25
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.428232503
      safeguard_positive_rows: 50
      rows_with_101_candidates: 50
```
