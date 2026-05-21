# NanoRTEB / NanoAILACasedocs

## Overview

`NanoRTEB / NanoAILACasedocs` is the AILA precedent retrieval task in RTEB.
Long Indian legal situation descriptions retrieve relevant Supreme Court of
India case documents.

## Details

### What the Original Data Measures

[Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal
Assistance](https://ceur-ws.org/Vol-2517/T1-1.pdf) describes a legal
assistance benchmark where systems retrieve prior cases and statutes for a
given legal situation. The case-law subtask asks a system to identify precedent
documents that are relevant to the facts and legal issues in a query.

[Introducing RTEB: A New Standard for Retrieval Evaluation](https://huggingface.co/blog/rteb)
includes AILA case documents as an open English legal dataset because the
queries are non-synthetic and the documents are challenging. This Nano task
keeps that retrieval-first framing: the query is a full legal situation, not a
short keyword query.

### Observed Data Profile

The split has 50 queries, 186 documents, and 195 positive qrel rows. Queries
average 3,038.42 characters; documents average 26,947.34 characters and can
exceed 220k characters. Most queries have multiple precedents, with an average
of 3.90 positives per query and a maximum of 22.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2932 and hit@10 = 0.6400. It ranks 17 queries at rank 1 and finds a positive
in the top 10 for 32 of 50 queries.

BM25 helps when the situation and precedent share distinctive statutory or
procedural terms, but long case facts often contain many generic legal phrases.
The task rewards legal issue matching, not only surface overlap.

### Training Data That May Help

Useful training data includes legal precedent retrieval, Indian case-law
citations, legal entailment and issue matching, and hard negatives from cases
with similar facts but different legal holdings.

### Synthetic Data Guidance

Generate long fact patterns from non-evaluation case documents and pair them
with cited or legally analogous precedents. Hard negatives should share parties,
procedural posture, or statute names while differing in the controlling issue.
Avoid making positives only from exact quotation overlap.

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
| Nano set | NanoRTEB |
| Backing dataset | NanoRTEB |
| Task / split | NanoAILACasedocs |
| Hugging Face dataset | [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB) |
| Source dataset | [mteb/AILA_casedocs](https://huggingface.co/datasets/mteb/AILA_casedocs) |
| Language | en |
| Category | natural_language |
| Queries | 50 |
| Documents | 186 |
| Positive qrels | 195 |
| Positives per query | avg 3.90 / min 1 / median 3 / max 22 |
| Multi-positive queries | 40 |
| BM25 nDCG@10 | 0.2932 |
| BM25 hit@10 | 0.6400 |
| Query length avg chars | 3,038.42 |
| Document length avg chars | 26,947.34 |

### Public Sources

- [Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance](https://ceur-ws.org/Vol-2517/T1-1.pdf), task paper.
- [AILA 2019 Precedent & Statute Retrieval Task](https://doi.org/10.5281/zenodo.4063986), dataset record.
- [Introducing RTEB: A New Standard for Retrieval Evaluation](https://huggingface.co/blog/rteb), RTEB benchmark announcement.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB)
- Source task dataset: [mteb/AILA_casedocs](https://huggingface.co/datasets/mteb/AILA_casedocs)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance | 2019 | task paper | https://ceur-ws.org/Vol-2517/T1-1.pdf |
| AILA 2019 Precedent & Statute Retrieval Task | 2020 | dataset record | https://doi.org/10.5281/zenodo.4063986 |
| Introducing RTEB: A New Standard for Retrieval Evaluation | 2025 | benchmark article | https://huggingface.co/blog/rteb |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoRTEB
  backing_dataset: NanoRTEB
  dataset_id: hakari-bench/NanoRTEB
  task_name: NanoAILACasedocs
  split_name: NanoAILACasedocs
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRTEB/NanoAILACasedocs.md
  source_research:
    primary_source_type: task_paper
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
    document_mean: 26947.34
  bm25:
    ndcg_at_10: 0.2932
    hit_at_10: 0.64
    source: dataset_bm25_column
  example_count: 5
```
