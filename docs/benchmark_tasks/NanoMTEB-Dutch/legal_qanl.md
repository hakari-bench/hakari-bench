# NanoMTEB-Dutch / legal_qanl

## Overview

`legal_qanl` is a Dutch legal question-to-law retrieval task from MTEB-NL.
Queries are natural-language legal questions, and documents are Dutch law
article chunks with statute, chapter, and article context. The task tests
whether a retriever can find the legal article that grounds an answer to a Dutch
legal question.

## Details

### What the Original Data Measures

[Retrieval-Augmented Generation for Long-form Question Answering in Dutch](https://aclanthology.org/2024.nllp-1.12/)
introduces a Dutch legal QA dataset built from question-answer pairs with
attributions to Dutch law articles. The paper reports a retrieval-augmented
pipeline for long-form legal answers where answers must be tied back to
verifiable legal sources. For retrieval evaluation, the relevant unit is a law
article or article chunk that supports the answer.

MTEB-NL includes this dataset as LegalQANLRetrieval. This matters because the
task is not general web QA: it is statute retrieval with formal article
structure, legal terminology, and questions that often ask about conditions,
exceptions, authorities, or procedural rights.

### Observed Data Profile

The Nano split has 102 queries, 10,000 documents, and 157 positive qrel rows.
The average positive count is 1.54, 41 queries have multiple positives, and the
maximum is 8. Queries average 104.29 characters and are Dutch legal questions,
usually starting with "Wanneer" or asking which authority may take an action.
Documents average 665.01 characters and begin with law and article metadata
followed by the statutory provision text.

The examples cover primary education funding, electricity regulation, offshore
grid liability, space-activity permits, and guardianship. Some query text in the
sample shows encoding artifacts such as `beÃ«indigd`, while documents use normal
Dutch accents. That increases the need for robust text normalization.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.8143
and hit@10 = 0.9804. The hit rate is very high because many questions contain
distinctive legal nouns that also occur in article headings or article text.

The ranking problem remains non-trivial. Multiple articles can share the same
authority, statute name, or procedure, and the relevant answer may depend on a
specific condition. Dense or hybrid models need to distinguish legal scope,
article hierarchy, and near-duplicate provisions.

### Training Data That May Help

Useful training data includes the official non-overlapping LegalQA-NL training
or development material if available under benchmark rules, Dutch legal QA pairs
with statute attributions, public law article search logs, and synthetic
question-to-article pairs from non-evaluation statutes. The exact Nano queries,
qrels, article chunks, and any upstream test split rows should be excluded from
training.

Because many queries have multiple positives, multi-positive training is useful:
several law articles may jointly ground an answer or provide alternative
article-level evidence.

### Synthetic Data Guidance

For document-to-query generation, select non-evaluation Dutch legal provisions
and generate realistic legal questions about conditions, deadlines, powers,
exceptions, and rights. Questions should be answerable from the provision and
should preserve statute-level terminology.

For joint generation, create short statute-like article chunks with titles,
article numbers, and legal conditions, then generate Dutch legal questions that
map to one or more chunks. Include hard negatives from adjacent articles or
similar powers to teach precise legal retrieval.

## Example Data

| Query | Positive document |
| --- | --- |
| Wanneer wordt een vergunning voor ruimtevaartactiviteiten geweigerd? (68 chars) | Wet ruimtevaartactiviteiten, Hoofdstuk2, Vergunningen, Paragraaf2, Artikel6, Aanvraag vergunning, Artikel 6 een vergunning wordt geweigerd indien: de naleving van een verdrag of een bindend besluit van een volkenrechtelijke o ... [truncated 225 chars](1073 chars) |
| Wanneer kan het bezwaarschrift worden ingediend voor een WOB (wet openbaarheid van bestuur) verzoek? (100 chars) | Wet openbaarheid van bestuur, HoofdstukVI, Overige bepalingen, Artikel15a, Artikel 15a in afwijking van artikel 7:1, eerste lid, onderdeel f, van de algemene wet bestuursrecht kan degene aan wie het recht is toegekend beroep ... [truncated 225 chars](1048 chars) |
| Wanneer kan een ontheffing volgens de opiumwet worden ingetrokken? (66 chars) | Opiumwet, Artikel8e, Artikel 8e een ontheffing kan worden ingetrokken: indien de houder van de ontheffing handelt in strijd met een bij of krachtens deze wet gesteld voorschrift; in het geval en onder de voorwaarden, bedoeld ... [truncated 225 chars](560 chars) |
| Wanneer heeft iemand geen recht op bijstand? (44 chars) | Participatiewet, Hoofdstuk2, Rechten en plichten, Paragraaf2.2, Artikel13, Bijstand, Artikel 13, Uitsluiting van bijstand geen recht op bijstand heeft degene: aan wie rechtens zijn vrijheid is ontnomen; die zich onttrekt aan ... [truncated 225 chars](1099 chars) |
| Wanneer wordt de gemeenschap van rechtswege ontbonden? (54 chars) | Burgerlijk Wetboek Boek 1, Boek1, Titeldeel7, Ontbinding van de gemeenschap, Afdeling3, De wettelijke gemeenschap van goederen, Artikel 99 de gemeenschap wordt van rechtswege ontbonden: in geval van het eindigen van het huwel ... [truncated 225 chars](1154 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Dutch |
| Backing dataset | NanoMTEB-Dutch |
| Task / split | legal_qanl |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch) |
| Source dataset | [clips/mteb-nl-legalqa-pr](https://huggingface.co/datasets/clips/mteb-nl-legalqa-pr) |
| Language | nl |
| Category | natural_language |
| Queries | 102 |
| Documents | 10,000 |
| Positive qrels | 157 |
| Avg positives / query | 1.54 |
| Positives per query (min / median / max) | 1 / 1 / 8 |
| Queries with multiple positives | 41 (40.20%) |
| BM25 nDCG@10 | 0.8143 |
| BM25 hit@10 | 0.9804 |
| BM25 Recall@100 | 0.9618 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8050 |
| Dense hit@10 | 0.9608 |
| Dense Recall@100 | 0.9108 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8455 |
| Reranking hybrid hit@10 | 0.9706 |
| Reranking hybrid Recall@100 | 0.9745 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 104.29 |
| Document length avg chars | 665.01 |

### Public Sources

- [Retrieval-Augmented Generation for Long-form Question Answering in Dutch](https://aclanthology.org/2024.nllp-1.12/), 2024.
- [MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch](https://arxiv.org/abs/2509.12340), 2025.
- [clips/mteb-nl-legalqa-pr](https://huggingface.co/datasets/clips/mteb-nl-legalqa-pr), source dataset card.
- [MTEB project repository](https://github.com/embeddings-benchmark/mteb).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch)
- Source dataset: [clips/mteb-nl-legalqa-pr](https://huggingface.co/datasets/clips/mteb-nl-legalqa-pr)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Retrieval-Augmented Generation for Long-form Question Answering in Dutch | 2024 | ACL paper | https://aclanthology.org/2024.nllp-1.12/ |
| MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch | 2025 | arXiv paper | https://arxiv.org/abs/2509.12340 |
| clips/mteb-nl-legalqa-pr |  | dataset card | https://huggingface.co/datasets/clips/mteb-nl-legalqa-pr |
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
  task_name: legal_qanl
  split_name: legal_qanl
  language: nl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Dutch/legal_qanl.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://aclanthology.org/2024.nllp-1.12/
    additional_source_urls:
    - https://arxiv.org/abs/2509.12340
    - https://huggingface.co/datasets/clips/mteb-nl-legalqa-pr
    - https://github.com/embeddings-benchmark/mteb
    no_paper_note: null
  counts:
    queries: 102
    documents: 10000
    positive_qrels: 157
  positives_per_query:
    average: 1.539215686
    min: 1
    median: 1.0
    max: 8
    multi_positive_queries: 41
    multi_positive_query_percent: 40.196078431
  text_stats_chars:
    query_mean: 104.294117647
    document_mean: 665.007
  bm25:
    ndcg_at_10: 0.814312257246524
    hit_at_10: 0.9803921568627451
    source: dataset_candidate_subset
  learning:
    original_train_split: unknown
    evaluation_split_origin: test split from clips/mteb-nl-legalqa-pr
    train_eval_overlap_audit: not_audited
    leakage_note: Exclude LegalQA-NL evaluation questions, qrels, and law article
      chunks used in this Nano split.
    useful_training_data:
    - non-overlapping Dutch legal QA pairs with statute attributions
    - Dutch law article search or citation data
    - public legal question-answer data with source articles
    - hard negatives from adjacent law articles and similar provisions
    synthetic_data:
      document_generation: Dutch statute-like article chunks with law, chapter, article,
        and condition text.
      question_generation: Dutch legal questions about powers, rights, conditions,
        deadlines, and exceptions.
      answerability: Questions should be answerable from one or more explicit legal
        provisions.
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch
    source_urls:
    - label: LegalQA-NL ACL Anthology
      url: https://aclanthology.org/2024.nllp-1.12/
    - label: MTEB-NL arXiv
      url: https://arxiv.org/abs/2509.12340
    - label: clips/mteb-nl-legalqa-pr
      url: https://huggingface.co/datasets/clips/mteb-nl-legalqa-pr
    - label: MTEB repository
      url: https://github.com/embeddings-benchmark/mteb
    source_notes: []
  references:
  - title: Retrieval-Augmented Generation for Long-form Question Answering in Dutch
    url: https://aclanthology.org/2024.nllp-1.12/
    year: 2024
    doi: 10.18653/v1/2024.nllp-1.12
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch'
    url: https://arxiv.org/abs/2509.12340
    year: 2025
    doi: 10.48550/arXiv.2509.12340
    is_paper: true
    source_confidence: definitive_paper_link
  - title: clips/mteb-nl-legalqa-pr
    url: https://huggingface.co/datasets/clips/mteb-nl-legalqa-pr
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
      ndcg_at_10: 0.8143122572
      hit_at_10: 0.9803921569
      recall_at_100: 0.9617834395
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 102
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9617834395
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8049601356
      hit_at_10: 0.9607843137
      recall_at_100: 0.9108280255
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 102
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9108280255
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8454968273
      hit_at_10: 0.9705882353
      recall_at_100: 0.974522293
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.009804
      query_count: 102
      query_coverage: 1.0
      relevant_coverage_at_100: 0.974522293
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
