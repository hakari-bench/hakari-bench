# NanoMTEB-Dutch / open_tender

## Overview

`open_tender` is a Dutch public-procurement retrieval task from MTEB-NL. Queries
are tender titles or short procurement descriptions, and documents are tender
call descriptions from Belgian and Dutch public procurement records. The task
tests retrieval over administrative, contractual, and domain-specific Dutch.

## Details

### What the Original Data Measures

[MTEB-NL and E5-NL](https://arxiv.org/abs/2509.12340) includes
OpenTenderRetrieval as a Dutch retrieval task based on Belgian and Dutch tender
calls from OpenTender. The appendix describes the retrieval framing as matching
tender titles to tender descriptions. This adds a procurement domain that differs
from encyclopedic QA, news, and fact verification.

No standalone paper for this exact retrieval dataset was confirmed. The public
interpretation here relies on the MTEB-NL paper, the Hugging Face source dataset
card, MTEB metadata, and observed Nano examples.

### Observed Data Profile

The Nano split has 199 queries, 10,000 documents, and 199 positive qrel rows.
Every query has exactly one positive. Queries average 62.19 characters and are
often formal procurement titles. Documents average 442.03 characters and range
from very short title-like descriptions to longer notices about procedures,
contract scope, suppliers, and transparency announcements.

The sample includes coaching procurement, parking-garage construction, printing
and copying services, asylum-center redevelopment, and digital-service
procurement. Several positives are extremely short, while others contain legal
or procedural language. This creates a mix of title matching and semantic
description matching.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.6712
and hit@10 = 0.7136. Lexical overlap is helpful because tender titles often
share nouns with descriptions, but the baseline is far below the news and FEVER
tasks.

The hard cases are procurement-specific paraphrases, abbreviations, and very
short descriptions. A query such as a redevelopment or service title may need to
match a document that describes the contract scope in different administrative
terms.

### Training Data That May Help

Useful training data includes non-overlapping Dutch tender title-description
pairs, procurement search logs, public contract notices with CPV-like category
metadata, and same-category hard negatives. Training data should exclude the
OpenTender evaluation titles, descriptions, and qrels used by this Nano split.

Because each query has one positive, strong hard-negative mining is important:
documents from the same municipality, category, or procurement procedure can be
lexically close but non-relevant.

### Synthetic Data Guidance

For document-to-query generation, use non-evaluation procurement notices and
generate concise Dutch tender titles or search queries that preserve the
contract subject. Keep administrative vocabulary such as aanbesteding,
raamovereenkomst, onderhoud, levering, and inhuur.

For joint generation, create realistic tender descriptions with buyer,
procedure, contract scope, and service category, then generate title-like
queries. Include hard negatives from the same sector or procedure type.

## Example Data

| Query | Positive document |
| --- | --- |
| Warmtebeeldcamera's (19 chars) | Warmtebeeldcamera TSWarmtebeeldcamera OvDten behoeve van de veiligheidsregio's Noord- en Oost Gelderland, IJsselland en Twente. (127 chars) |
| Nieuwbouw van een vrijstaand gebouw voor dienstverlenende en adminstratieve functies. (85 chars) | Lot 4: Liften voor bouwen van een nieuwbouw voor dienstverlening van geestelijke gezondheid en bijhorende administratie. (120 chars) |
| Toegangscontrolesysteem (23 chars) | Het leveren en installeren van online draadloos toegangscontrolesystemen. (73 chars) |
| 57/52/3/18/032 - Area North-West - Omvorming van spoorinfrastructuur - Raamovereenkomst (87 chars) | De opdracht bestaat hoofdzakelijk uit:Hoofdzaak:— De opbraak en aanleg (vernieuwen) van spoortoestellen in hoofd- en bijspoor,— De opbraak en aanleg (vernieuwen) van spoorstaven, dwarsliggers en ballast in hoofd- en bijspoor. (225 chars) |
| Europese aanbesteding brandverzekering Veiligheidsregio Zeeland (63 chars) | Het doel van deze openbare Europese aanbesteding is het op transparante wijze sluiten van een of meer brandverzekeringsovereenkomsten tussen Aanbestedende dienst, in hoedanigheid van Veiligheidsregio Zeeland in de ruimste zin ... [truncated 225 chars](884 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Dutch |
| Backing dataset | NanoMTEB-Dutch |
| Task / split | open_tender |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch) |
| Source dataset | [clips/mteb-nl-opentender-ret](https://huggingface.co/datasets/clips/mteb-nl-opentender-ret) |
| Language | nl |
| Category | natural_language |
| Queries | 199 |
| Documents | 10,000 |
| Positive qrels | 199 |
| BM25 nDCG@10 | 0.6712 |
| BM25 hit@10 | 0.7136 |
| BM25 Recall@100 | 0.8090 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.6044 |
| Dense hit@10 | 0.6734 |
| Dense Recall@100 | 0.8090 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6556 |
| Reranking hybrid hit@10 | 0.7286 |
| Reranking hybrid Recall@100 | 0.8543 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 29 |
| Query length avg chars | 62.19 |
| Document length avg chars | 442.03 |

### Public Sources

- [MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch](https://arxiv.org/abs/2509.12340), 2025.
- [clips/mteb-nl-opentender-ret](https://huggingface.co/datasets/clips/mteb-nl-opentender-ret), source dataset card.
- [MTEB project repository](https://github.com/embeddings-benchmark/mteb).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch)
- Source dataset: [clips/mteb-nl-opentender-ret](https://huggingface.co/datasets/clips/mteb-nl-opentender-ret)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch | 2025 | arXiv paper | https://arxiv.org/abs/2509.12340 |
| clips/mteb-nl-opentender-ret |  | dataset card | https://huggingface.co/datasets/clips/mteb-nl-opentender-ret |
| MTEB project repository |  | repository | https://github.com/embeddings-benchmark/mteb |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Dutch
  backing_dataset: NanoMTEB-Dutch
  dataset_id: hakari-bench/NanoMTEB-Dutch
  task_name: open_tender
  split_name: open_tender
  language: nl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Dutch/open_tender.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2509.12340
    additional_source_urls:
    - https://huggingface.co/datasets/clips/mteb-nl-opentender-ret
    - https://github.com/embeddings-benchmark/mteb
    no_paper_note: No standalone OpenTender retrieval paper was confirmed; MTEB-NL
      and the source dataset card were used.
  counts:
    queries: 199
    documents: 10000
    positive_qrels: 199
  positives_per_query:
    average: 1.0
    min: 1
    median: 1
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 62.185929648
    document_mean: 442.0317
  bm25:
    ndcg_at_10: 0.6711732173395353
    hit_at_10: 0.7135678391959799
    source: dataset_candidate_subset
  learning:
    original_train_split: unknown
    evaluation_split_origin: test split from clips/mteb-nl-opentender-ret
    train_eval_overlap_audit: not_audited
    leakage_note: Exclude overlapping OpenTender titles, descriptions, qrels, and
      evaluation rows.
    useful_training_data:
    - non-overlapping Dutch tender title-description pairs
    - public procurement notices with category metadata
    - procurement search logs and clicked tender records
    - same-category hard negatives from tender corpora
    synthetic_data:
      document_generation: Dutch procurement notices with buyer, scope, procedure,
        and contract details.
      question_generation: Concise tender titles or procurement search queries.
      answerability: Each query should map to one procurement notice, with same-sector
        hard negatives.
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch
    source_urls:
    - label: MTEB-NL arXiv
      url: https://arxiv.org/abs/2509.12340
    - label: clips/mteb-nl-opentender-ret
      url: https://huggingface.co/datasets/clips/mteb-nl-opentender-ret
    - label: MTEB repository
      url: https://github.com/embeddings-benchmark/mteb
    source_notes: []
  references:
  - title: 'MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch'
    url: https://arxiv.org/abs/2509.12340
    year: 2025
    doi: 10.48550/arXiv.2509.12340
    is_paper: true
    source_confidence: definitive_paper_link
  - title: clips/mteb-nl-opentender-ret
    url: https://huggingface.co/datasets/clips/mteb-nl-opentender-ret
    year: null
    doi: null
    is_paper: false
    source_confidence: probably_correct
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6711732173
      hit_at_10: 0.7135678392
      recall_at_100: 0.8090452261
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 199
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8090452261
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6044057976
      hit_at_10: 0.6733668342
      recall_at_100: 0.8090452261
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 199
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8090452261
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.6555984882
      hit_at_10: 0.7286432161
      recall_at_100: 0.8542713568
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.145729
      query_count: 199
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8542713568
      safeguard_positive_rows: 29
      rows_with_101_candidates: 29
```
