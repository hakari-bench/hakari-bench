# NanoMuPLeR

## Overview

NanoMuPLeR is the Nano task group for MuPLeR-retrieval, a multilingual parallel
legal retrieval benchmark derived from European Union legal text. It covers 14
European languages: Greek, English, Spanish, Finnish, French, Italian,
Lithuanian, Latvian, Dutch, Polish, Portuguese, Slovak, Slovenian, and Swedish.
Each split contains synthetic legal queries and DGT-Acquis-derived legal
passages in the same language.

The group measures focused legal passage retrieval under a parallel multilingual
setup. The same underlying legal questions and passages are represented across
languages, so the group is useful for comparing whether a retriever preserves
legal-retrieval strength across morphology, script, and translation variation,
not just across unrelated monolingual datasets.

## Details

### What the Original Group Measures

The [MuPLeR-retrieval dataset card](https://huggingface.co/datasets/mteb/MuPLeR-retrieval)
describes MuPLeR as a multilingual, parallel legal dataset for retrieval and
cross-lingual retrieval evaluation. It contains 10,000 human-translated parallel
passages derived from the European Union's DGT-Acquis corpus and 200 synthetic
parallel queries across 14 European languages. The card notes that the technical
paper is still in progress, so the dataset card and source-corpus references are
the most direct task-level sources currently available.

The source corpus is DGT-Acquis. The European Commission's
[DGT-Acquis page](https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en)
describes it as multilingual parallel corpora extracted from the Official Journal
of the European Union, covering documents from mid-2004 to the end of 2011 in up
to 23 languages. The cited source article,
[An overview of the European Union's highly multilingual parallel corpora](https://link.springer.com/article/10.1007/s10579-014-9277-0),
serves as a reference publication for DGT-Acquis and related EU language
resources.

### Subtask Coverage

All current NanoMuPLeR subtasks are same-language legal retrieval splits. Queries
ask about legal conditions, treaty interpretations, state aid, procurement,
import duties, nuclear policy, pre-accession rules, and EU institutional
procedures. Documents are medium-length legal passages rather than full acts.
The source dataset card states that the passages were chunked into short legal
contexts of roughly 60 to 150 words, with language validation, deduplication,
parallel alignment checks, and synthetic query generation.

Although the splits are monolingual at evaluation time, their parallel
construction matters. A strong model should retrieve the corresponding passage
for each language without over-relying on English-centric legal phrasing. The
observed examples show many shared legal anchors across translations: directive
numbers, dates, percentages, treaty articles, state names, EU institutions, and
terms such as state aid, procurement criteria, and pre-accession provisions.

### Observed Group Profile

Across the 14 splits, NanoMuPLeR contains 2,800 queries, 2,800 positive qrels,
and 140,000 split-local documents. Every split has exactly 200 queries, 10,000
documents, and 200 positive qrels. All observed qrels are single-positive.

The query-weighted mean query length is 141.44 characters, and the
document-count-weighted mean document length is 679.65 characters. Finnish has
the longest average queries at 160.16 characters, while English has the shortest
average queries at 134.87 characters among the observed splits. Document lengths
are relatively compact compared with long-document benchmarks, but the passages
are dense legal text, so retrieval depends on matching the precise legal
condition rather than broad topical similarity.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, query-weighted BM25 nDCG@10 is
0.7787 and query-weighted hit@10 is 0.8561. Because every split has exactly 200
queries, the unweighted task means are the same values.

BM25 is a strong baseline for this group. Dutch is the easiest observed split,
with nDCG@10 = 0.8909 and hit@10 = 0.9400. Swedish, Polish, Latvian,
Portuguese, and Lithuanian are also high. English is the hardest split by
nDCG@10 at 0.5994, followed by Finnish at 0.6706. The first English sampled
query has its positive at BM25 rank 100, showing that even in a lexically rich
legal dataset, paraphrased synthetic queries can outrun exact term overlap.

The main difficulty is legal specificity. Many wrong passages share EU-law
vocabulary, dates, institutions, and regulatory style. Models need to distinguish
the exact legal condition, actor, threshold, or procedural rule rather than only
matching the domain.

### Training Data That May Help

Useful training data includes non-overlapping EUR-Lex and DGT-Acquis retrieval
pairs, multilingual legal QA, legal passage reranking data, and parallel legal
bitext with hard negatives from nearby EU provisions. Synthetic legal queries
can help if they preserve the exact legal condition and avoid turning the task
into vague topical retrieval.

Training should exclude MuPLeR evaluation queries, positives, and exact parallel
equivalents. Because the same underlying passages are aligned across languages,
an overlap audit should consider translated duplicates, not only same-language
string matches.

### Synthetic Data Guidance

Synthetic data should generate language-specific legal questions from
non-evaluation EU legal passages. The generated query should mention the legal
actor, condition, date, percentage, article, directive, or procedural constraint
that makes one passage answerable. Near negatives should come from adjacent legal
topics with overlapping terms but a different legal conclusion.

For multilingual training, synthetic queries should be generated or validated in
each target language rather than translated blindly from English. This matters
for morphology-rich languages such as Finnish, Polish, Slovak, Slovenian, and
Lithuanian, and for preserving Greek script and EU legal terminology.

## Task Summary

| Task | Retrieval shape | Queries | Docs | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars | Source status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [el](el.md) | Greek legal question to Greek EU passage | 200 | 10,000 | 0.7749 | 0.8600 | 141.28 | 744.82 | MuPLeR dataset card + DGT-Acquis source reference |
| [en](en.md) | English legal question to English EU passage | 200 | 10,000 | 0.5994 | 0.7100 | 134.87 | 650.58 | MuPLeR dataset card + DGT-Acquis source reference |
| [es](es.md) | Spanish legal question to Spanish EU passage | 200 | 10,000 | 0.7792 | 0.8600 | 134.67 | 734.58 | MuPLeR dataset card + DGT-Acquis source reference |
| [fi](fi.md) | Finnish legal question to Finnish EU passage | 200 | 10,000 | 0.6706 | 0.7400 | 160.16 | 683.64 | MuPLeR dataset card + DGT-Acquis source reference |
| [fr](fr.md) | French legal question to French EU passage | 200 | 10,000 | 0.7773 | 0.8850 | 141.22 | 746.43 | MuPLeR dataset card + DGT-Acquis source reference |
| [it](it.md) | Italian legal question to Italian EU passage | 200 | 10,000 | 0.7920 | 0.8750 | 140.77 | 726.14 | MuPLeR dataset card + DGT-Acquis source reference |
| [lt](lt.md) | Lithuanian legal question to Lithuanian EU passage | 200 | 10,000 | 0.8115 | 0.8750 | 143.04 | 621.81 | MuPLeR dataset card + DGT-Acquis source reference |
| [lv](lv.md) | Latvian legal question to Latvian EU passage | 200 | 10,000 | 0.8376 | 0.8900 | 140.47 | 608.95 | MuPLeR dataset card + DGT-Acquis source reference |
| [nl](nl.md) | Dutch legal question to Dutch EU passage | 200 | 10,000 | 0.8909 | 0.9400 | 147.87 | 716.33 | MuPLeR dataset card + DGT-Acquis source reference |
| [pl](pl.md) | Polish legal question to Polish EU passage | 200 | 10,000 | 0.8400 | 0.9050 | 143.97 | 686.12 | MuPLeR dataset card + DGT-Acquis source reference |
| [pt](pt.md) | Portuguese legal question to Portuguese EU passage | 200 | 10,000 | 0.8222 | 0.8950 | 135.46 | 702.90 | MuPLeR dataset card + DGT-Acquis source reference |
| [sk](sk.md) | Slovak legal question to Slovak EU passage | 200 | 10,000 | 0.7041 | 0.7850 | 136.25 | 628.24 | MuPLeR dataset card + DGT-Acquis source reference |
| [sl](sl.md) | Slovenian legal question to Slovenian EU passage | 200 | 10,000 | 0.7455 | 0.8350 | 136.35 | 607.82 | MuPLeR dataset card + DGT-Acquis source reference |
| [sv](sv.md) | Swedish legal question to Swedish EU passage | 200 | 10,000 | 0.8563 | 0.9300 | 143.74 | 656.78 | MuPLeR dataset card + DGT-Acquis source reference |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMuPLeR |
| Backing dataset | NanoMuPLeR |
| Hugging Face dataset | [hakari-bench/NanoMuPLeR](https://huggingface.co/datasets/hakari-bench/NanoMuPLeR) |
| Source dataset | [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval) |
| Language | multilingual: el, en, es, fi, fr, it, lt, lv, nl, pl, pt, sk, sl, sv |
| Category | natural_language |
| Domain | legal |
| Subtasks | 14 |
| Total queries | 2,800 |
| Split-local documents | 140,000 |
| Positive qrels | 2,800 |
| Positives per query | exactly 1.00 for every subtask |
| Query-weighted BM25 nDCG@10 | 0.7787 |
| Query-weighted BM25 hit@10 | 0.8561 |
| Mean query length | 141.44 chars, weighted by query count |
| Mean document length | 679.65 chars, weighted by split-local document count |

### Public Sources

- [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval), source dataset card.
- [DGT-Acquis](https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en), European Commission source-corpus page.
- [An overview of the European Union's highly multilingual parallel corpora](https://link.springer.com/article/10.1007/s10579-014-9277-0); 2014; Ralf Steinberger et al.; DOI: `10.1007/s10579-014-9277-0`.
- [Massive Text Embedding Benchmark](https://github.com/embeddings-benchmark/mteb), benchmark integration reference.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMuPLeR](https://huggingface.co/datasets/hakari-bench/NanoMuPLeR)
- Source task dataset: [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MuPLeR: Multilingual Parallel Legal Retrieval | 2026 | dataset card | https://huggingface.co/datasets/mteb/MuPLeR-retrieval |
| DGT-Acquis | 2026 | source corpus page | https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en |
| An overview of the European Union's highly multilingual parallel corpora | 2014 | source reference paper | https://link.springer.com/article/10.1007/s10579-014-9277-0 |
| Massive Text Embedding Benchmark | 2026 | benchmark repository | https://github.com/embeddings-benchmark/mteb |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoMuPLeR
  backing_dataset: NanoMuPLeR
  dataset_id: hakari-bench/NanoMuPLeR
  source_dataset_id: mteb/MuPLeR-retrieval
  language: multilingual
  category: natural_language
  domain: legal
  document_path: docs/benchmark_tasks/NanoMuPLeR/index.md
  source_research:
    primary_source_type: dataset_card_and_source_corpus_page
    paper_pdf_or_html_checked: false
    no_paper_note: MuPLeR dataset card says the technical paper is in progress; DGT-Acquis source article landing page and European Commission corpus page were checked.
  counts:
    tasks: 14
    queries: 2800
    split_local_documents: 140000
    positive_qrels: 2800
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_tasks: 0
    multi_positive_queries: 0
  text_stats_chars:
    query_mean_weighted_by_queries: 141.43714285714285
    document_mean_weighted_by_documents: 679.6528571428571
  bm25:
    ndcg_at_10_query_weighted: 0.7786785714285714
    hit_at_10_query_weighted: 0.8560714285714286
    ndcg_at_10_unweighted_task_mean: 0.7786785714285714
    hit_at_10_unweighted_task_mean: 0.8560714285714285
    source: dataset_bm25_column
    easiest_task_by_ndcg_at_10: nl
    hardest_task_by_ndcg_at_10: en
  tasks:
    - name: el
      path: docs/benchmark_tasks/NanoMuPLeR/el.md
      retrieval_shape: greek_legal_question_to_greek_eu_passage
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.7749
      bm25_hit_at_10: 0.86
    - name: en
      path: docs/benchmark_tasks/NanoMuPLeR/en.md
      retrieval_shape: english_legal_question_to_english_eu_passage
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.5994
      bm25_hit_at_10: 0.71
    - name: es
      path: docs/benchmark_tasks/NanoMuPLeR/es.md
      retrieval_shape: spanish_legal_question_to_spanish_eu_passage
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.7792
      bm25_hit_at_10: 0.86
    - name: fi
      path: docs/benchmark_tasks/NanoMuPLeR/fi.md
      retrieval_shape: finnish_legal_question_to_finnish_eu_passage
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.6706
      bm25_hit_at_10: 0.74
    - name: fr
      path: docs/benchmark_tasks/NanoMuPLeR/fr.md
      retrieval_shape: french_legal_question_to_french_eu_passage
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.7773
      bm25_hit_at_10: 0.885
    - name: it
      path: docs/benchmark_tasks/NanoMuPLeR/it.md
      retrieval_shape: italian_legal_question_to_italian_eu_passage
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.792
      bm25_hit_at_10: 0.875
    - name: lt
      path: docs/benchmark_tasks/NanoMuPLeR/lt.md
      retrieval_shape: lithuanian_legal_question_to_lithuanian_eu_passage
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.8115
      bm25_hit_at_10: 0.875
    - name: lv
      path: docs/benchmark_tasks/NanoMuPLeR/lv.md
      retrieval_shape: latvian_legal_question_to_latvian_eu_passage
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.8376
      bm25_hit_at_10: 0.89
    - name: nl
      path: docs/benchmark_tasks/NanoMuPLeR/nl.md
      retrieval_shape: dutch_legal_question_to_dutch_eu_passage
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.8909
      bm25_hit_at_10: 0.94
    - name: pl
      path: docs/benchmark_tasks/NanoMuPLeR/pl.md
      retrieval_shape: polish_legal_question_to_polish_eu_passage
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.84
      bm25_hit_at_10: 0.905
    - name: pt
      path: docs/benchmark_tasks/NanoMuPLeR/pt.md
      retrieval_shape: portuguese_legal_question_to_portuguese_eu_passage
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.8222
      bm25_hit_at_10: 0.895
    - name: sk
      path: docs/benchmark_tasks/NanoMuPLeR/sk.md
      retrieval_shape: slovak_legal_question_to_slovak_eu_passage
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.7041
      bm25_hit_at_10: 0.785
    - name: sl
      path: docs/benchmark_tasks/NanoMuPLeR/sl.md
      retrieval_shape: slovenian_legal_question_to_slovenian_eu_passage
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.7455
      bm25_hit_at_10: 0.835
    - name: sv
      path: docs/benchmark_tasks/NanoMuPLeR/sv.md
      retrieval_shape: swedish_legal_question_to_swedish_eu_passage
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.8563
      bm25_hit_at_10: 0.93
  learning:
    leakage_note: exclude NanoMuPLeR evaluation queries, qrels, positive passages, and exact parallel equivalents across all 14 languages
    useful_training_data:
      - non-overlapping EUR-Lex and DGT-Acquis legal retrieval pairs
      - multilingual legal QA and legal passage reranking data
      - parallel legal bitext with language-specific hard negatives
      - EU legal passages with synthetic questions grounded in specific legal conditions
    synthetic_data:
      document_generation: medium-length EU legal passages preserving article references, dates, percentages, institutions, and procedural conditions
      question_generation: language-specific legal questions grounded in one passage, validated in the target language
      answerability: the positive passage must answer the exact legal condition or procedural rule in the query
    multi_positive_training: single_positive_parallel_legal_retrieval
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMuPLeR
    source_urls:
      - label: mteb/MuPLeR-retrieval
        url: https://huggingface.co/datasets/mteb/MuPLeR-retrieval
      - label: DGT-Acquis
        url: https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en
      - label: DGT-Acquis source reference article
        url: https://link.springer.com/article/10.1007/s10579-014-9277-0
      - label: MTEB
        url: https://github.com/embeddings-benchmark/mteb
    source_notes:
      - MuPLeR dataset card states that the technical paper is in progress.
  references:
    - title: "MuPLeR: Multilingual Parallel Legal Retrieval"
      url: https://huggingface.co/datasets/mteb/MuPLeR-retrieval
      year: 2026
      is_paper: false
      source_confidence: official_dataset_card
    - title: DGT-Acquis
      url: https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en
      year: 2026
      is_paper: false
      source_confidence: official_source_corpus_page
    - title: "An overview of the European Union's highly multilingual parallel corpora"
      url: https://link.springer.com/article/10.1007/s10579-014-9277-0
      year: 2014
      doi: 10.1007/s10579-014-9277-0
      is_paper: true
      source_confidence: source_reference_paper_landing_page
```
