# NanoMTEB-Polish / cqadupstack_physics

## Overview

CQADupStack uses duplicate links in community QA as relevance judgments; the
Polish Physics split brings that retrieval objective to translated physics
forum posts. Queries are short conceptual or calculation-oriented physics
questions, and relevant documents are equivalent posts that may express the same
phenomenon with different formality or equations. The observed clusters cover
cosmology, gravity, superconductivity, inertial frames, and heat transfer, with
large duplicate groups in some cases, so retrieval requires matching physical
meaning across varied explanations.

## Details

### What the Original Data Measures

[CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://ir.webis.de/anthology/2015.adcs_conference-2015.3/)
introduced the source benchmark for community QA duplicate retrieval. The
[MTEB paper](https://arxiv.org/abs/2210.07316) includes CQADupStack in its
retrieval suite, while the Polish Physics split is exposed by the MTEB/CLARIN
dataset cards.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 621 positive qrels. Queries
average 58.80 characters and documents average 814.74 characters. Examples span
cosmology, gravity, superconductivity, inertial frames, and heat transfer. The
qrels are often multi-positive: 83 queries have more than one positive and the
largest duplicate cluster has 72 positives.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3359 and hit@10 = 0.5450, with 65 positives at rank 1
and 109 in the top 10. Lexical terms such as "Hubble", "grawitacyjne", or
"nadprzewodnictwo" help, but semantic matching is needed when a colloquial
question maps to a formal physics concept.

### Training Data That May Help

Useful data includes non-overlapping Physics Stack Exchange duplicates, Polish
science QA, translated physics explanations, and hard negatives sharing formulas
or entities but asking about different principles. Do not train on the upstream
test duplicate clusters or positive posts.

### Synthetic Data Guidance

Generate Polish physics questions paired with source-style explanations that
contain the relevant principle, variables, and physical setting. Synthetic
duplicates should vary intuition, examples, and terminology while preserving the
same answerable physics problem.

## Example Data

| Query | Positive document |
| --- | --- |
| Jak równanie Schroedingera jest równaniem falowym? (50 chars) | związek między równaniem Schrodingera a równaniem falowym Zawsze byłem zdezorientowany związkiem między równaniem Schrödingera a równaniem falowym. $$ i\hbar \frac{\partial \psi}{\partial t} = - \frac{\hbar^2}{2m} \nabla^2+ U ... [truncated 225 chars](1059 chars) |
| Pomiary technologii aktywnej redukcji szumów (44 chars) | Maksymalne opóźnienie efektywnej aktywnej redukcji szumów? Aktywna redukcja szumów redukuje niechciany dźwięk, wysyłając odwróconą fazę oryginalnej fazy: ![Aktywna redukcja szumów](http://i.stack.imgur.com/0jSp8.png) (Źródło: ... [truncated 225 chars](913 chars) |
| Czy ciągłe modele matematyczne dyskretnych zjawisk fizycznych są bałaganiarskie z powodu rozłączenia między „ciągłym” i „nieciągłym”? (133 chars) | Jaki jest „dyskretny” odpowiednik mechaniki „ciągłej”? Gdybym chciał zbadać podejście matematyki dyskretnej do mechaniki kontinuum, do jakich podręczników powinienem się zajrzeć? Przypuszczam, że gotową odpowiedzią na to pyta ... [truncated 225 chars](536 chars) |
| Grawitacja z energii (20 chars) | Czy energia niemasowa generuje pole grawitacyjne? Na bardzo podstawowym poziomie wiem, że grawitacja nie jest generowana przez masę, ale raczej przez tensor naprężenia-energii i kiedy często macham rękami, wydaje się, że ozna ... [truncated 225 chars](1451 chars) |
| Dlaczego (relatywistyczna) masa obiektu wzrasta, gdy jego prędkość zbliża się do prędkości światła? (99 chars) | Relatywistyczny pęd i masa Czy istnieje w ogóle relatywistyczna masa czy po prostu relatywistyczny pęd? Jaki jest powód, aby preferować jeden nad drugim? Jaki jest problem ze stwierdzeniem, że gorący gaz będzie miał większą m ... [truncated 225 chars](241 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Polish |
| Backing dataset | NanoMTEB-Polish |
| Task / split | cqadupstack_physics |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish) |
| Source dataset | [mteb/CQADupstack-Physics-PL](https://huggingface.co/datasets/mteb/CQADupstack-Physics-PL) |
| Language | pl |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 621 |
| Avg positives / query | 3.105 |
| Positives per query (min / median / max) | 1 / 1.0 / 72 |
| Queries with multiple positives | 83 (41.5%) |
| BM25 nDCG@10 | 0.3359 |
| BM25 hit@10 | 0.5450 |
| BM25 Recall@100 | 0.4364 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4306 |
| Dense hit@10 | 0.6750 |
| Dense Recall@100 | 0.5475 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4024 |
| Reranking hybrid hit@10 | 0.6100 |
| Reranking hybrid Recall@100 | 0.5491 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 27 |
| Query length avg chars | 58.80 |
| Document length avg chars | 814.74 |

### Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://ir.webis.de/anthology/2015.adcs_conference-2015.3/), original benchmark paper record.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), benchmark paper covering CQADupStack retrieval tasks.
- [CLARIN-KNEXT cqadupstack-physics-pl](https://huggingface.co/datasets/clarin-knext/cqadupstack-physics-pl), Polish source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish)
- Source task dataset: [mteb/CQADupstack-Physics-PL](https://huggingface.co/datasets/mteb/CQADupstack-Physics-PL)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | task paper | https://ir.webis.de/anthology/2015.adcs_conference-2015.3/ |
| MTEB: Massive Text Embedding Benchmark | 2022 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| CLARIN-KNEXT cqadupstack-physics-pl |  | dataset card | https://huggingface.co/datasets/clarin-knext/cqadupstack-physics-pl |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Polish
  backing_dataset: NanoMTEB-Polish
  dataset_id: hakari-bench/NanoMTEB-Polish
  task_name: cqadupstack_physics
  split_name: cqadupstack_physics
  language: pl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Polish/cqadupstack_physics.md
  source_research:
    primary_source_type: dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone paper for this Polish translated split was confirmed
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 621
  positives_per_query:
    average: 3.105
    min: 1
    median: 1.0
    max: 72
    multi_positive_queries: 83
    multi_positive_query_percent: 41.5
  text_stats_chars:
    query_mean: 58.795
    document_mean: 814.7388
  bm25:
    ndcg_at_10: 0.33587022323429133
    hit_at_10: 0.545
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3358702232
      hit_at_10: 0.545
      recall_at_100: 0.4363929147
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4363929147
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4306202603
      hit_at_10: 0.675
      recall_at_100: 0.5475040258
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5475040258
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4023854084
      hit_at_10: 0.61
      recall_at_100: 0.5491143317
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.135
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5491143317
      safeguard_positive_rows: 27
      rows_with_101_candidates: 27
```
