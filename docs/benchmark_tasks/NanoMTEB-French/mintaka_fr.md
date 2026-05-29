# NanoMTEB-French / mintaka_fr

## Overview

`mintaka_fr` is the French Mintaka retrieval split. Queries are French complex
QA questions, and documents are short answer strings or entity names. The
retriever must connect a French question to the correct answer entity, often
with little lexical overlap.

## Details

### What the Original Data Measures

[Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering](https://arxiv.org/abs/2210.01613)
introduces 20,000 English question-answer pairs annotated with Wikidata
entities and professionally translated into eight languages, including French.
The paper targets complex naturally elicited questions such as count,
comparison, superlative, intersection, and multi-hop questions.

The retrieval packaging treats answer strings as documents. This turns a QA
benchmark into a short-answer retrieval task.

### Observed Data Profile

The Nano split has 200 French queries, 1,714 documents, and 200 positive
qrels. Every query has one positive. Queries average 71.61 characters, and
documents average 14.41 characters. Sampled positives include `Toy Story`, `Le
Seigneur des anneaux : La Communauté de l'anneau`, `Matrix Reloaded`, `Clint
Eastwood`, and `Mick Jagger`.

Many answer documents are named entities, titles, or short values. Some are in
English and some are in French, making this a multilingual entity-linking style
retrieval task.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.3000 and hit@10 = 0.4000. The median best rank is 100. Short answer strings
give BM25 very little to match unless the answer name appears in the query.

### Training Data That May Help

Useful training data includes non-overlapping Mintaka train examples, French
Wikidata QA, multilingual entity linking, and complex-question paraphrases.
Training should avoid Mintaka test examples, Nano queries, qrels, and answer
strings likely to overlap with this evaluation.

### Synthetic Data Guidance

Generate French questions over entity attributes and comparisons, with short
canonical answer documents. Include film, music, geography, sports, and
history questions. Do not use Nano evaluation questions or answer strings as
seeds.

## Example Data

| Query | Positive document |
| --- | --- |
| Quel film du début des année 1970 est-il celui pour lequel Bruce Lee est le plus connu ? (88 chars) | Opération Dragon (16 chars) |
| Quel acteur a joué Hans Solo et Indiana Jones ? (47 chars) | Harrison Ford (13 chars) |
| Quel est le nom du tout premier film du réalisateur Kevin Smith ? (65 chars) | Clerks : Les Employés modèles (29 chars) |
| Quel film de Star Trek a le moins rapporté ? (44 chars) | Star Trek : Nemesis (19 chars) |
| Dans quel film de Major League ne figurait pas Charlie Sheen ? (62 chars) | Les Indians 3 (13 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-French |
| Backing dataset | NanoMTEB-French |
| Task / split | mintaka_fr |
| Hugging Face dataset | [hakari-bench/NanoMTEB-French](https://huggingface.co/datasets/hakari-bench/NanoMTEB-French) |
| Language | fr, en |
| Category | natural_language |
| Queries | 200 |
| Documents | 1714 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.2995 |
| BM25 hit@10 | 0.3900 |
| BM25 Recall@100 | 0.4750 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3676 |
| Dense hit@10 | 0.5300 |
| Dense Recall@100 | 0.7650 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3400 |
| Reranking hybrid hit@10 | 0.4500 |
| Reranking hybrid Recall@100 | 0.6550 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 69 |
| Query length avg chars | 71.61 |
| Document length avg chars | 14.41 |

### Public Sources

- [Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering](https://arxiv.org/abs/2210.01613); 2022; Priyanka Sen, Alham Fikri Aji, Amir Saffari.
- [mteb/MintakaRetrieval dataset card](https://huggingface.co/datasets/mteb/MintakaRetrieval).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316); 2023; Niklas Muennighoff et al.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-French](https://huggingface.co/datasets/hakari-bench/NanoMTEB-French)
- Source dataset: [mteb/MintakaRetrieval](https://huggingface.co/datasets/mteb/MintakaRetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering | 2022 | arXiv paper | https://arxiv.org/abs/2210.01613 |
| MTEB: Massive Text Embedding Benchmark | 2023 | arXiv paper | https://arxiv.org/abs/2210.07316 |
| mteb/MintakaRetrieval | 2025 | dataset card | https://huggingface.co/datasets/mteb/MintakaRetrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-French
  backing_dataset: NanoMTEB-French
  dataset_id: hakari-bench/NanoMTEB-French
  task_name: mintaka_fr
  split_name: mintaka_fr
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-French/mintaka_fr.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1714
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 71.61
    document_mean: 14.407234539089849
  bm25:
    ndcg_at_10: 0.2994941321826419
    hit_at_10: 0.39
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude Mintaka test examples, Nano queries, qrels, and answer strings
      likely to overlap with this evaluation
    useful_training_data:
    - non-overlapping Mintaka train examples
    - French Wikidata QA pairs
    - multilingual entity-linking supervision
    - complex-question paraphrases
    synthetic_data:
      document_generation: short canonical answer strings and entity names
      question_generation: French complex QA questions over films, music, geography,
        sports, history, and Wikidata-style relations
      answerability: each answer string should be the canonical entity or value implied
        by the question
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-French
    source_urls:
    - label: Mintaka arXiv
      url: https://arxiv.org/abs/2210.01613
    - label: mteb/MintakaRetrieval
      url: https://huggingface.co/datasets/mteb/MintakaRetrieval
    - label: MTEB arXiv
      url: https://arxiv.org/abs/2210.07316
    source_notes: []
  references:
  - title: 'Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question
      Answering'
    url: https://arxiv.org/abs/2210.01613
    year: 2022
    doi: 10.48550/arXiv.2210.01613
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2994941322
      hit_at_10: 0.39
      recall_at_100: 0.475
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.475
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.367640436
      hit_at_10: 0.53
      recall_at_100: 0.765
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.765
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3400057846
      hit_at_10: 0.45
      recall_at_100: 0.655
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.345
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.655
      safeguard_positive_rows: 69
      rows_with_101_candidates: 69
```
