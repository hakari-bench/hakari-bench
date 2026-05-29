# NanoLaw / NanoAILACasedocs

## Overview

`NanoAILACasedocs` is an English legal precedent-retrieval task. Each query is a
long factual case scenario from Indian law, and the retriever must find prior
case documents that are relevant as precedents.

## Details

### What the Original Data Measures

[Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance](https://ceur-ws.org/Vol-2517/T1-1.pdf)
defines two legal assistance retrieval tasks: finding relevant prior cases and
finding relevant statutes for a natural-language legal situation. For precedent
retrieval, the paper says participants were given 50 factual scenarios in
English and asked to identify relevant prior cases from Indian Supreme Court
case documents. The same source explains that the gold standard was based on
cases cited by lawyers in the original documents, with the caveat that a fuller
expert-curated gold standard was planned for future work.

The MTEB dataset card for [AILA_casedocs](https://huggingface.co/datasets/mteb/AILA_casedocs)
describes the task as retrieving the case document most closely matching or most
relevant to the query scenario, and points to the AILA 2019 Zenodo release.

### Observed Data Profile

The Nano split has 50 queries, 186 documents, and 195 positive qrels. Queries
are long case narratives averaging 3,038.42 characters; documents are full or
near-full case judgments averaging 26,947.34 characters. Positive labels are
multi-valued for 40 of 50 queries, with an average of 3.90 positives per query
and a maximum of 22.

The sampled data is dominated by criminal, constitutional, land, procedural, and
public-law fact patterns. Query and document text both contain legal citations,
party roles, procedural posture, and anonymized placeholders.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2921 and hit@10 = 0.6000. It ranks a positive first for 17 queries. Lexical
matching helps when the same statute names, procedural terms, or charge labels
appear in both texts, but the task often asks for analogical legal relevance
across long judgments rather than passage-level keyword overlap.

### Training Data That May Help

Useful training data includes non-overlapping legal precedent retrieval pairs,
case-citation prediction, Indian legal case retrieval, and hard negatives from
cases sharing charges or statutes but not legal reasoning. Training should keep
the long-query setting intact instead of reducing the task to short keyword
queries.

### Synthetic Data Guidance

Synthetic examples should pair a full factual/legal scenario with prior cases
that share legally material facts, procedural issues, or statutory reasoning.
Hard negatives should share surface charges or named statutes while differing
in the decisive legal issue.

## Example Data

| Query | Positive document |
| --- | --- |
| Appellant calls in question legality of the judgment rendered by High Court confirming his conviction for offence and sentence of imprisonment for life as awarded by the learned Sessions Judge. Background facts as unfolded du ... [truncated 225 chars](3569 chars) | Kalarimadathil Unni v State of Kerala Supreme Court of India 22 April 1966 Criminal Appeals Nos. 102 & 103 of 1965 The Judgment was delivered by : M. Hidayatullah, J. 1. This judgment will also govern the disposal of Criminal ... [truncated 225 chars](18777 chars) |
| This appeal, by special leave, has been preferred against the judgment and order dated 23 February 2005 of the High Court (Aurangabad Bench), by which the appeal preferred by the appellants was dismissed and their conviction ... [truncated 225 chars](3266 chars) | State of Andhra Pradesh v Thadi Narayana Supreme Court of India 24 July 1961 Criminal Appeal No. 222 of 1959. Appeal by special leave from the judgment and order dated February 24, 1959, of the Andhra Pradesh High Court, Hyde ... [truncated 225 chars](30909 chars) |
| The appellant before us was examined as prime witness in the trial of T.R. on the file of the Special Judge against the first respondent. The trial ended in conviction against the first respondent and when the appeal filed by ... [truncated 225 chars](2857 chars) | R. K. Lakshmanan v A. K. Srinivasan and Another Supreme Court of India 1 August 1975 CRIMINAL APPELLATE JURISDICTION : Criminal Appeal No. 1 30 of 1975. Appeal by Special Leave from the Judgment and Order dated the 13th March ... [truncated 225 chars](15791 chars) |
| Whether sanction is required to initiate criminal proceedings in respect of offences is the question arising for consideration in these cases. The District Registrar lodged a complaint with the Inspector of Police, CBCID on 0 ... [truncated 225 chars](1664 chars) | Shambhoo Nath Misra v State of U. P. Supreme Court of India 14 March 1997 Appeal (Cr.) 318 of 1997 The Order of the Court was as follows : Leave granted. We have heard learned counsel on both sides. 1. This appeal by special ... [truncated 225 chars](5678 chars) |
| These appeals involve a pure question of law as to whether an award by which residue assets of a partnership firm are distributed amongst the partners on dissolution of the partnership firm requires registration. Briefly the ... [truncated 225 chars](1668 chars) | S. V. Chandra Pandian and Others v S. V. Sivalinga Nadar and Others Supreme Court of India 11 January 1993 C.As. Nos. 17491752 of 1992 The Judgment was delivered by : Hon'ble Justice A. M. Ahmadi 1. The four appellants and re ... [truncated 225 chars](45869 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoLaw |
| Backing dataset | NanoLaw |
| Task / split | NanoAILACasedocs |
| Hugging Face dataset | [hakari-bench/NanoLaw](https://huggingface.co/datasets/hakari-bench/NanoLaw) |
| Language | en |
| Category | natural_language |
| Queries | 50 |
| Documents | 186 |
| Positive qrels | 195 |
| Positives per query | avg 3.90 / min 1 / median 3.0 / max 22 |
| Multi-positive queries | 40 (80.00%) |
| BM25 nDCG@10 | 0.2805 |
| BM25 hit@10 | 0.6200 |
| BM25 Recall@100 | 0.9128 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4003 |
| Dense hit@10 | 0.6800 |
| Dense Recall@100 | 0.9026 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3667 |
| Reranking hybrid hit@10 | 0.7000 |
| Reranking hybrid Recall@100 | 0.9436 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 2 |
| Query length avg chars | 3038.42 |
| Document length avg chars | 26947.34 |

### Public Sources

- [Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance](https://ceur-ws.org/Vol-2517/T1-1.pdf); 2019; Paheli Bhattacharya et al.
- [AILA 2019 Precedent & Statute Retrieval Task](https://doi.org/10.5281/zenodo.4063986); 2020; Zenodo dataset release.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoLaw](https://huggingface.co/datasets/hakari-bench/NanoLaw)
- Source dataset: [mteb/AILA_casedocs](https://huggingface.co/datasets/mteb/AILA_casedocs)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance | 2019 | CEUR paper | https://ceur-ws.org/Vol-2517/T1-1.pdf |
| AILA 2019 Precedent & Statute Retrieval Task | 2020 | Zenodo dataset | https://doi.org/10.5281/zenodo.4063986 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoLaw
  backing_dataset: NanoLaw
  dataset_id: hakari-bench/NanoLaw
  task_name: NanoAILACasedocs
  split_name: NanoAILACasedocs
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoLaw/NanoAILACasedocs.md
  source_research:
    primary_source_type: task_paper_and_dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 186
    positive_qrels: 195
  positives_per_query:
    average: 3.9
    min: 1
    median: 3.0
    max: 22
    multi_positive_queries: 40
    multi_positive_query_percent: 80.0
  text_stats_chars:
    query_mean: 3038.42
    document_mean: 26947.344086021505
  bm25:
    ndcg_at_10: 0.28050774745000373
    hit_at_10: 0.62
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: aila_2019_precedent_retrieval
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoAILACasedocs queries, qrels, and cited precedent documents
    useful_training_data:
    - non-overlapping legal precedent retrieval pairs
    - case citation prediction data
    - Indian legal case retrieval corpora
    - same-charge legal hard negatives
    synthetic_data:
      document_generation: full legal judgments with procedural posture and legal
        reasoning
      question_generation: long factual scenarios describing a possible lawsuit or
        appeal
      answerability: positives should be legally analogous prior cases, not merely
        topically similar cases
    multi_positive_training: preserve_multiple_precedents_per_scenario
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoLaw
    source_urls:
    - label: AILA 2019 paper
      url: https://ceur-ws.org/Vol-2517/T1-1.pdf
    - label: AILA Zenodo dataset
      url: https://doi.org/10.5281/zenodo.4063986
    - label: MTEB AILA_casedocs
      url: https://huggingface.co/datasets/mteb/AILA_casedocs
    source_notes: []
  references:
  - title: 'Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal
      Assistance'
    url: https://ceur-ws.org/Vol-2517/T1-1.pdf
    year: 2019
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2805077475
      hit_at_10: 0.62
      recall_at_100: 0.9128205128
      candidate_count_min: 186
      candidate_count_max: 186
      candidate_count_mean: 186.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9128205128
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4003439103
      hit_at_10: 0.68
      recall_at_100: 0.9025641026
      candidate_count_min: 186
      candidate_count_max: 186
      candidate_count_mean: 186.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9025641026
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3667246366
      hit_at_10: 0.7
      recall_at_100: 0.9435897436
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.04
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9435897436
      safeguard_positive_rows: 2
      rows_with_101_candidates: 2
```
