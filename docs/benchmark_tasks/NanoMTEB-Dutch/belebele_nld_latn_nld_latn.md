# NanoMTEB-Dutch / belebele_nld_latn_nld_latn

## Overview

`belebele_nld_latn_nld_latn` is the same-language Dutch Belebele retrieval
split. Dutch reading-comprehension questions retrieve Dutch passages. It tests
short-form Dutch passage retrieval where the relevant evidence is a translated
Belebele passage rather than a web search document.

## Details

### What the Original Data Measures

[The Belebele Benchmark](https://arxiv.org/abs/2308.16884) introduces Belebele
as a parallel reading-comprehension dataset in 122 language variants. The paper
reports that the passages come from FLORES-200 and that the questions are
designed to be answerable from the passage while avoiding overly easy lexical
shortcuts. This makes the retrieval conversion a passage-selection test built
from comprehension questions.

[MTEB-NL and E5-NL](https://arxiv.org/abs/2509.12340) includes BelebeleRetrieval
as one of the Dutch retrieval tasks and notes that the Dutch portion of
Belebele was used without additional preprocessing. This same-language split
therefore measures Dutch semantic retrieval over parallel translated passages.

### Observed Data Profile

The Nano split has 200 queries, 488 documents, and 200 positive qrel rows. Each
query has one positive. Queries average 69.39 characters, and Dutch documents
average 529.14 characters. The examples mirror the English-passage direction:
constitutional amendments, President Arias, a gas leak, an Afghan election
runoff, and an internet radio show.

The task is compact but not trivial. Queries often ask "which reason", "where",
or "who", while the answer-bearing passage may include several nearby facts.
The correct document is a passage-level match, not necessarily a single lexical
span.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.8364
and hit@10 = 0.9150. This is a strong lexical baseline: both sides are Dutch,
the corpus has only 488 documents, and many queries contain distinctive words
that also appear in the passage.

The remaining errors matter for dense-model evaluation. BM25 can still confuse
nearby passages when the question is abstract, asks for an exclusion, or uses
paraphrases. A dense model should improve mostly on those semantic cases rather
than on straightforward entity overlap.

### Training Data That May Help

Useful training data includes Dutch reading-comprehension retrieval pairs,
Dutch QA-to-passage retrieval, non-overlapping Belebele-style translated data,
and Dutch passage ranking data with hard negatives. Training should exclude the
Belebele test questions and Dutch passages used by this Nano split.

Because this is single-positive passage retrieval with a small candidate pool,
training can use standard contrastive objectives, but hard negatives should be
semantically close Dutch passages rather than random unrelated documents.

### Synthetic Data Guidance

For document-to-query generation, use short Dutch passages outside the
evaluation set and generate Dutch comprehension questions that target a fact,
cause, location, person, date, or exception in the passage. Avoid copying long
phrases from the source document into the query.

For joint generation, create Dutch news or encyclopedic passages plus a single
answerable Dutch question. Include hard negatives that share topics or entities
but do not answer the exact question.

## Example Data

| Query | Positive document |
| --- | --- |
| Welke uitspraak over het evenement waar de schietpartij plaatsvond, is juist? (77 chars) | Er waren op zijn minst 100 mensen op het feest aanwezig die de eerste huwelijksdag vierden van een koppel dat vorig jaar trouwde. Er stond een formeel verjaardagsevenement gepland voor een latere datum, volgens de ambtenaren. ... [truncated 225 chars](469 chars) |
| Wat moeten arrestanten volgens het tijdelijke contactverbod dat in de tekst wordt genoemd, krijgen om langer dan 24 uur te mogen worden vastgehouden? (149 chars) | In de afgelopen 3 maanden zijn er meer dan 80 arrestanten uit de Central Booking-inrichting vrijgelaten zonder dat ze officieel zijn aangeklaagd. In april van dit jaar heeft rechter Glynn een tijdelijk contactverbod tegen de ... [truncated 225 chars](748 chars) |
| Welke uitspraak over de maansonde van de Chandrayaan-1 is niet waar? (68 chars) | De onbemande ruimtesonde Chandrayaan-1 wierp zijn Moon Impact Probe (MIP) uit, die vervolgens met 1,5 kilometer per seconde (3000 mijl per uur) over de oppervlakte van de maan werd geslingerd en met succes in de buurt van de ... [truncated 225 chars](409 chars) |
| Wie stelde voor om de 'Clean Air Act' te herschrijven? (54 chars) | Premier Stephen Harper is akkoord gegaan om de 'Clean Air Act' van de overheid naar een commissie voor alle partijen te sturen voor herziening, voorafgaand aan de tweede lezing, na de 25 minuten durende vergadering met NDP-le ... [truncated 225 chars](1010 chars) |
| Welke van de volgende heeft de NBA besloten op te schorten? (59 chars) | Als gevolg van COVID-19 werd door de National Basketball Association (NBA) van de Verenigde Staten afgelopen woensdag het professionele basketbalseizoen opgeschort. De beslissing van de NBA werd genomen nadat een speler van U ... [truncated 225 chars](274 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Dutch |
| Backing dataset | NanoMTEB-Dutch |
| Task / split | belebele_nld_latn_nld_latn |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch) |
| Source dataset | [mteb/belebele](https://huggingface.co/datasets/mteb/belebele) |
| Language | nl |
| Category | natural_language |
| Queries | 200 |
| Documents | 488 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.8364 |
| BM25 hit@10 | 0.9150 |
| BM25 Recall@100 | 0.9700 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8899 |
| Dense hit@10 | 0.9600 |
| Dense Recall@100 | 0.9650 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8999 |
| Reranking hybrid hit@10 | 0.9500 |
| Reranking hybrid Recall@100 | 0.9900 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 2 |
| Query length avg chars | 69.39 |
| Document length avg chars | 529.14 |

### Public Sources

- [The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122 Language Variants](https://arxiv.org/abs/2308.16884), 2023.
- [facebookresearch/belebele](https://github.com/facebookresearch/belebele), source repository.
- [mteb/belebele](https://huggingface.co/datasets/mteb/belebele), MTEB dataset card.
- [MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch](https://arxiv.org/abs/2509.12340), 2025.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch)
- Source dataset: [mteb/belebele](https://huggingface.co/datasets/mteb/belebele)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122 Language Variants | 2023 | arXiv paper | https://arxiv.org/abs/2308.16884 |
| facebookresearch/belebele | 2023 | repository | https://github.com/facebookresearch/belebele |
| mteb/belebele |  | dataset card | https://huggingface.co/datasets/mteb/belebele |
| MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch | 2025 | arXiv paper | https://arxiv.org/abs/2509.12340 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Dutch
  backing_dataset: NanoMTEB-Dutch
  dataset_id: hakari-bench/NanoMTEB-Dutch
  task_name: belebele_nld_latn_nld_latn
  split_name: belebele_nld_latn_nld_latn
  language: nl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Dutch/belebele_nld_latn_nld_latn.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2308.16884
    additional_source_urls:
    - https://github.com/facebookresearch/belebele
    - https://huggingface.co/datasets/mteb/belebele
    - https://arxiv.org/abs/2509.12340
  counts:
    queries: 200
    documents: 488
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 69.39
    document_mean: 529.143443
  bm25:
    ndcg_at_10: 0.8364152115644063
    hit_at_10: 0.915
    source: dataset_candidate_subset
  learning:
    original_train_split: unknown
    evaluation_split_origin: mteb/belebele nld_Latn-nld_Latn test split
    train_eval_overlap_audit: not_audited
    leakage_note: Exclude Belebele test questions and passages used by this Nano split.
    useful_training_data:
    - Dutch reading-comprehension retrieval pairs
    - Dutch QA-to-passage retrieval data
    - non-overlapping Belebele-style translated data
    - Dutch hard-negative passage ranking data
    synthetic_data:
      document_generation: Short Dutch news or encyclopedic passages outside the evaluation
        set.
      question_generation: Dutch comprehension questions answerable from one selected
        passage.
      answerability: The positive passage should explicitly contain the answer, with
        same-topic Dutch hard negatives.
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch
    source_urls:
    - label: Belebele arXiv
      url: https://arxiv.org/abs/2308.16884
    - label: Belebele repository
      url: https://github.com/facebookresearch/belebele
    - label: mteb/belebele
      url: https://huggingface.co/datasets/mteb/belebele
    - label: MTEB-NL arXiv
      url: https://arxiv.org/abs/2509.12340
    source_notes: []
  references:
  - title: 'The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122
      Language Variants'
    url: https://arxiv.org/abs/2308.16884
    year: 2023
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch'
    url: https://arxiv.org/abs/2509.12340
    year: 2025
    doi: 10.48550/arXiv.2509.12340
    is_paper: true
    source_confidence: definitive_paper_link
  - title: mteb/belebele
    url: https://huggingface.co/datasets/mteb/belebele
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
      ndcg_at_10: 0.8364152116
      hit_at_10: 0.915
      recall_at_100: 0.97
      candidate_count_min: 488
      candidate_count_max: 488
      candidate_count_mean: 488.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.97
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8899230055
      hit_at_10: 0.96
      recall_at_100: 0.965
      candidate_count_min: 488
      candidate_count_max: 488
      candidate_count_mean: 488.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.965
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8999042286
      hit_at_10: 0.95
      recall_at_100: 0.99
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.01
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.99
      safeguard_positive_rows: 2
      rows_with_101_candidates: 2
```
