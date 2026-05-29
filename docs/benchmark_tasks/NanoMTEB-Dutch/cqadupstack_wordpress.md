# NanoMTEB-Dutch / cqadupstack_wordpress

## Overview

`cqadupstack_wordpress` is the Dutch-translated WordPress subforum split of
CQADupStack. Queries are WordPress development and administration questions, and
positive documents are older duplicate questions. The task covers plugins,
themes, hooks, filters, debugging, post metadata, SEO fields, and template logic.

## Details

### What the Original Data Measures

[CQADupStack](https://doi.org/10.1145/2838931.2838934) provides a standard
benchmark for duplicate-question retrieval in community QA, using
StackExchange's manually flagged duplicate links and chronological retrieval
splits. [BEIR](https://arxiv.org/abs/2104.08663) includes CQADupStack as a
heterogeneous zero-shot retrieval task, and [BEIR-NL](https://aclanthology.org/2025.bucc-1.5/)
translates BEIR datasets into Dutch.

This WordPress split is technical and platform-specific. Many identifiers,
function names, hooks, and plugin names remain unchanged after translation,
while the surrounding problem descriptions become Dutch.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrel rows.
Each query has one positive. Queries average 56.55 characters and documents
average 1,183.40 characters. Examples include removing the Yoast SEO metabox,
front-page backgrounds, debugging plugins, term hooks, and passing arguments to
`add_action()`.

The documents are often code-adjacent and contain plugin names, WordPress API
calls, and longer descriptions of attempted implementations. Duplicate retrieval
requires matching intent across different WordPress APIs and wording.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.2608
and hit@10 = 0.3700. Exact plugin and API names help, but short translated
queries and long documents make it easy to retrieve same-plugin but non-duplicate
posts.

### Training Data That May Help

Useful training data includes non-overlapping WordPress Stack Exchange duplicate
pairs, WordPress support forum QA, code-aware duplicate-question data, and
Dutch-translated CMS troubleshooting pairs. Exclude this Nano test split and
positive questions.

### Synthetic Data Guidance

Generate Dutch WordPress troubleshooting questions from non-evaluation posts.
Keep function names, hooks, filters, and plugin names intact. Create duplicate
paraphrases that ask the same implementation problem, with hard negatives from
the same API surface.

## Example Data

| Query | Positive document |
| --- | --- |
| Programmatisch hiërarchische termen invoegen & termen instellen voor berichten veroorzaakt een storing? (103 chars) | Het invoegen van termen in een hiërarchische taxonomie Ik ondervind een paar problemen met het invoegen van termen. Dit is mijn scenario: Ik heb een taxonomie genaamd veda_release_type: //Release Type en Regio $labels = array ... [truncated 225 chars](4702 chars) |
| Hoe de lengte van een excerpt in WordPress te vergroten? (56 chars) | De korte inhoud per karakter **Mogelijk duplicaat:** > fragment in karakters Op sommige van onze sites tonen we fragmenten van berichten (de beheerders voeren geen fragmenten in). We _kunnen_ de functie `the_excerpt` gebruike ... [truncated 225 chars](800 chars) |
| Media bibliotheek pagina supersnel, laad volle kwaliteit afbeeldingen (69 chars) | Wordpress 3.5 Media Manager - Afbeelding Formaat bij Laden Wijzigen De nieuwe media manager laadt afbeeldingen in VOLLE grootte, wat ECHT inefficiënt is voor een thumbnail. Ik wil dit graag vervangen door een ander formaat th ... [truncated 225 chars](352 chars) |
| Voorgedefinieerde categorieën in WordPress via GET-parameters (61 chars) | Hyperlink om nieuw bericht te maken met vooraf gedefinieerde categorie Ik ben een complete WordPress-beginner. Ik heb een site gemaakt voor mijn werk. Items worden gesorteerd op categorie. Op het dashboard (ik heb een aangepa ... [truncated 225 chars](660 chars) |
| Hoe schakel ik reacties uit op een pagina? (42 chars) | Hoe verwijder je de mogelijkheid voor een gebruiker om een reactie te plaatsen of te posten op een pagina? Ik bouw een nieuwe website op WordPress, en al mijn pagina's hebben onderaan het vak om een reactie toe te voegen. Ik ... [truncated 225 chars](518 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Dutch |
| Backing dataset | NanoMTEB-Dutch |
| Task / split | cqadupstack_wordpress |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch) |
| Source dataset | [clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack) |
| Language | nl |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.2608 |
| BM25 hit@10 | 0.3700 |
| BM25 Recall@100 | 0.5950 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3057 |
| Dense hit@10 | 0.4250 |
| Dense Recall@100 | 0.6850 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3371 |
| Reranking hybrid hit@10 | 0.4600 |
| Reranking hybrid Recall@100 | 0.7250 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 55 |
| Query length avg chars | 56.55 |
| Document length avg chars | 1,183.40 |

### Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://doi.org/10.1145/2838931.2838934), 2015.
- [Author-hosted CQADupStack PDF](https://eltimster.github.io/www/pubs/adcs2015.pdf), 2015.
- [BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language](https://aclanthology.org/2025.bucc-1.5/), 2025.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch)
- Source dataset: [clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | proceedings paper | https://doi.org/10.1145/2838931.2838934 |
| BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language | 2025 | proceedings paper | https://aclanthology.org/2025.bucc-1.5/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| clips/beir-nl-cqadupstack |  | dataset card | https://huggingface.co/datasets/clips/beir-nl-cqadupstack |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Dutch
  backing_dataset: NanoMTEB-Dutch
  dataset_id: hakari-bench/NanoMTEB-Dutch
  task_name: cqadupstack_wordpress
  split_name: cqadupstack_wordpress
  language: nl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Dutch/cqadupstack_wordpress.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://doi.org/10.1145/2838931.2838934
    additional_source_urls:
    - https://eltimster.github.io/www/pubs/adcs2015.pdf
    - https://aclanthology.org/2025.bucc-1.5/
    - https://arxiv.org/abs/2104.08663
    - https://huggingface.co/datasets/clips/beir-nl-cqadupstack
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 56.55
    document_mean: 1183.4007
  bm25:
    ndcg_at_10: 0.2607990583308149
    hit_at_10: 0.37
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: CQADupstackWordpress-NL test split from clips/beir-nl-cqadupstack
    train_eval_overlap_audit: not_audited
    leakage_note: Exclude translated CQADupStack WordPress test queries and duplicate
      positives used by this Nano split.
    useful_training_data:
    - non-overlapping WordPress Stack Exchange duplicate-question pairs
    - WordPress support forum QA pairs
    - code-aware CMS duplicate retrieval data
    synthetic_data:
      document_generation: Dutch WordPress support posts with function names and hooks
        preserved.
      question_generation: Paraphrased duplicate WordPress implementation questions.
      answerability: Each query should duplicate one prior WordPress question, with
        same-API hard negatives.
    multi_positive_training: single_positive
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2607990583
      hit_at_10: 0.37
      recall_at_100: 0.595
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.595
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3056615361
      hit_at_10: 0.425
      recall_at_100: 0.685
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.685
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.337105607
      hit_at_10: 0.46
      recall_at_100: 0.725
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.275
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.725
      safeguard_positive_rows: 55
      rows_with_101_candidates: 55
```
