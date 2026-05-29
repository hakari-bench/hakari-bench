# NanoMTEB-Dutch / cqadupstack_android

## Overview

`cqadupstack_android` is the Dutch-translated Android subforum split of
CQADupStack. Queries are translated Android Stack Exchange questions and
positive documents are earlier translated questions marked as duplicates. The
task measures duplicate-question retrieval for Android devices, Google Play,
hardware behavior, and mobile troubleshooting.

## Details

### What the Original Data Measures

[CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://doi.org/10.1145/2838931.2838934)
introduces CQADupStack as a benchmark built from twelve StackExchange
subforums, annotated with duplicate-question links and released with predefined
retrieval and classification splits. The paper explains that the retrieval setup
models the real-world task of finding previously asked duplicate questions, with
chronological constraints so that query questions are matched against older
indexed questions.

[BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language](https://aclanthology.org/2025.bucc-1.5/)
extends BEIR to Dutch by automatically translating public BEIR datasets. This
split is therefore not native Dutch forum data; it is a Dutch translation of the
BEIR CQADupStack Android retrieval task, preserving the duplicate-question
structure while changing the language surface.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrel rows.
Each query has one positive. Queries average 59.10 characters and are short
Android help questions. Documents average 638.08 characters and often include a
question title, duplicate marker, and a body with device names, app-store terms,
or troubleshooting details.

The sample includes ad-hoc hotspots, paid app reuse, device naming, gallery
thumbnails, and battery conditioning. Some rows are almost exact duplicate
titles, while others need matching an abbreviated question to a longer translated
forum post.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.2944
and hit@10 = 0.4250. Exact technical names such as Android, Google Play, ICS,
or Gallery help sparse retrieval, but translation variation and long forum bodies
make duplicate matching harder than keyword search.

### Training Data That May Help

Useful training data includes non-overlapping CQADupStack Android duplicate
pairs, Dutch or translated mobile-support question pairs, and multilingual
duplicate-question retrieval data. Training should exclude the translated test
queries, qrels, and positive duplicate questions used by this Nano split.

### Synthetic Data Guidance

Generate Dutch Android troubleshooting questions from non-evaluation support
posts, then create paraphrased duplicate titles and bodies with the same device,
OS version, or app-store issue. Add hard negatives from the same Android topic
that solve a different problem.

## Example Data

| Query | Positive document |
| --- | --- |
| Waarom is een Android ROM apparaatspecifiek? (44 chars) | Pure Android Download **Mogelijk duplicaat:** Waarom kan Android nog steeds niet als regulier besturingssysteem worden geïnstalleerd? Ik heb rondgekeken en vroeg me af of het niet mogelijk is om Android 4.2 kant-en-klaar (nie ... [truncated 225 chars](453 chars) |
| Hoe kan ik een bestand opslaan in plaats van het te openen? (59 chars) | Hoe download ik een audiobestand van een website? Is er een manier om een audiobestand, zoals een mp3-bestand, van de Android-browser naar het apparaat te downloaden zodat ik er later offline naar kan luisteren? Is er een man ... [truncated 225 chars](339 chars) |
| Hoe kan ik een video stream van het scherm van mijn Android telefoon vastleggen en deze op mijn laptop weergeven? (113 chars) | Hoe stream ik mijn Android-scherm naar mijn Mac? **Mogelijk duplicaat:** > Hoe projecteer ik het scherm van mijn Android-telefoon voor een presentatie? Ik wil mijn Android-telefoon livestreamen terwijl ik een game speel. Tot ... [truncated 225 chars](741 chars) |
| “Niet compatibel met andere applicatie(s) die dezelfde gedeelde gebruikers-ID gebruiken” bij het installeren van Google Play-services? (134 chars) | Kan Google Play-services niet installeren: Niet compatibel met andere applicatie(s) die dezelfde gedeelde gebruikers-ID gebruiken Ik kan Google Play-services niet installeren. Er staat: "Niet compatibel met andere applicatie( ... [truncated 225 chars](304 chars) |
| Hoe kan ik zowel het volume als het overslaan van nummers op mijn Android-apparaat bedienen met mijn hoofdtelefoon? (115 chars) | Koptelefoonbediening op SGS-III **Mogelijk duplicaat:** > Hoe kan ik zowel het volume als het wisselen van tracks op mijn Android-apparaat bedienen met mijn > koptelefoon? Ik heb onlangs de SIII gekregen en de iPhone 4s laten ... [truncated 225 chars](712 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Dutch |
| Backing dataset | NanoMTEB-Dutch |
| Task / split | cqadupstack_android |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch) |
| Source dataset | [clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack) |
| Language | nl |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.2944 |
| BM25 hit@10 | 0.4250 |
| BM25 Recall@100 | 0.6300 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3862 |
| Dense hit@10 | 0.5450 |
| Dense Recall@100 | 0.7750 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3836 |
| Reranking hybrid hit@10 | 0.5400 |
| Reranking hybrid Recall@100 | 0.7800 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 44 |
| Query length avg chars | 59.10 |
| Document length avg chars | 638.08 |

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
  task_name: cqadupstack_android
  split_name: cqadupstack_android
  language: nl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Dutch/cqadupstack_android.md
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
    query_mean: 59.105
    document_mean: 638.0803
  bm25:
    ndcg_at_10: 0.294388324280885
    hit_at_10: 0.425
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: CQADupstackAndroid-NL test split from clips/beir-nl-cqadupstack
    train_eval_overlap_audit: not_audited
    leakage_note: Exclude translated CQADupStack Android test queries and duplicate
      positives used by this Nano split.
    useful_training_data:
    - non-overlapping CQADupStack Android duplicate-question pairs
    - Dutch or translated mobile-support duplicate questions
    - multilingual technical support duplicate retrieval data
    synthetic_data:
      document_generation: Dutch Android support questions and answers outside the
        evaluation set.
      question_generation: Paraphrased duplicate Android troubleshooting questions
        with shared intent.
      answerability: Each synthetic query should duplicate one prior Android question,
        with same-topic hard negatives.
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch
    source_urls:
    - label: CQADupStack DOI
      url: https://doi.org/10.1145/2838931.2838934
    - label: BEIR-NL ACL Anthology
      url: https://aclanthology.org/2025.bucc-1.5/
    - label: BEIR arXiv
      url: https://arxiv.org/abs/2104.08663
    - label: clips/beir-nl-cqadupstack
      url: https://huggingface.co/datasets/clips/beir-nl-cqadupstack
    source_notes: []
  references:
  - title: 'CQADupStack: A Benchmark Data Set for Community Question-Answering Research'
    url: https://doi.org/10.1145/2838931.2838934
    year: 2015
    doi: 10.1145/2838931.2838934
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language'
    url: https://aclanthology.org/2025.bucc-1.5/
    year: 2025
    is_paper: true
    source_confidence: definitive_paper_link
  - title: clips/beir-nl-cqadupstack
    url: https://huggingface.co/datasets/clips/beir-nl-cqadupstack
    year: null
    is_paper: false
    source_confidence: probably_correct
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2943883243
      hit_at_10: 0.425
      recall_at_100: 0.63
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.63
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3861798904
      hit_at_10: 0.545
      recall_at_100: 0.775
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.775
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3836426023
      hit_at_10: 0.54
      recall_at_100: 0.78
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.22
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.78
      safeguard_positive_rows: 44
      rows_with_101_candidates: 44
```
