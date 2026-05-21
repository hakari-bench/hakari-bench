# NanoLaw / NanoLegalQuAD

## Overview

`NanoLegalQuAD` is a German legal QA retrieval task. Queries are German legal
questions, and documents are German legal decisions that contain the answer or
the relevant legal discussion.

## Details

### What the Original Data Measures

The task metadata cites [Towards Intelligent Legal Advisors for Document Retrieval and Question-Answering in German Legal Documents](https://doi.org/10.1109/AIKE52691.2021.00011).
The public DOI and MTEB card identify it as a German legal document retrieval
and question-answering dataset. The [MTEB LegalQuAD card](https://huggingface.co/datasets/mteb/LegalQuAD)
states that the dataset consists of German questions and legal documents, with
200 queries, 200 documents, and one relevant document per query in the test
split.

No freely accessible full paper text was confirmed beyond bibliographic and
dataset-card information during this pass, so the interpretation here relies on
the official dataset card, repository metadata, and observed Nano examples.

### Observed Data Profile

The Nano split has 200 queries, 200 documents, and 200 positive qrels. Each
query has exactly one positive document. Queries are concise German legal
questions averaging 71.94 characters, while documents are long court decisions
averaging 19,481.02 characters.

The observed questions ask about issues such as voluntary health-insurance
contribution income, interim legal protection, advertising claims, detention
grounds, and statutory default interest.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.6765 and hit@10 = 0.7950. It ranks a positive first for 112 queries. Lexical
matching is useful for specific terms like "Verzugszinsen" or "Haftgründe", but
the positive document is often long, so relevant answer evidence can be buried
inside broad factual and procedural text.

### Training Data That May Help

Useful training data includes German legal QA, question-to-judgment retrieval,
long-document German legal search, and hard negatives from judgments sharing the
same statute or legal domain but not answering the question.

### Synthetic Data Guidance

Generate concise German legal questions and pair them with full judicial
decisions that contain the answer. Hard negatives should include similar legal
terminology but answer a different procedural or substantive issue.

## Example Data

| Query | Positive document |
| --- | --- |
| Wie ist das rechtliche Gehör nach Art. 103 Abs. 1 GG definiert? (64 chars) | TenorDer Antrag auf Zulassung der Berufung wird abgelehnt.Der Kläger trägt die Kosten des Zulassungsverfahrens; Gerichtskosten werden nicht erhoben.1G r ü n d e2Der Antrag auf Zulassung der Berufung hat keinen Erfolg. Die ... [truncated 225 chars](13780 chars) |
| Welchen Wert hat das Beschwerdeverfahren? (41 chars) | TenorDie Beschwerde des Beschwerdeführers vom 27.04.2018 gegen den Beschluss des Amtsgerichts – Familiengericht – Bochum vom 21.03.2018 (57 F 17/18) in Verbindung mit dem Beschluss vom 03.04.2018 wird zurückgewiesen.Die Kos ... [truncated 225 chars](11601 chars) |
| Muss der Beauftragte dem Auftraggeber erhaltene Gegenstände zur Ausführung des Auftrages zurückgeben? (101 chars) | Tenor1E n t s c h e i d u n g s g r ü n d e :2##blob##nbsp;3##blob##nbsp;4Die in förmlicher Hinsicht unbedenkliche Berufung hat nach demErgebnis der zweitinstanzlichen Beweisaufnahme keinen Erfolg.5Das Landgericht hat die B ... [truncated 225 chars](13258 chars) |
| Mit wem wurde der Baubeginn abgestimmt? (39 chars) | Tenor1.Die Anträge vom 25.04.2012 auf Erlass einer einstweiligen Verfügung werden zurückgewiesen.2.Die Verfügungsklägerin trägt die Kosten des Verfahrens.3.Das Urteil ist vorläufig vollstreckbar. Die Verfügungskläger ... [truncated 225 chars](13416 chars) |
| Können Gesellschafter zur Erhöhung von Beiträgen verpflichtet werden? (69 chars) | Auf die Berufung des Beklagten wird das Urteil der 9. Zivilkammer des Landgerichts Koblenz vom 15. Juli 2004 abgeändert und die Klage abgewiesen.Die Kläger tragen die Kosten des Rechtsstreits einschließlich der Kosten, die ... [truncated 225 chars](13468 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoLaw |
| Backing dataset | NanoLaw |
| Task / split | NanoLegalQuAD |
| Hugging Face dataset | [hakari-bench/NanoLaw](https://huggingface.co/datasets/hakari-bench/NanoLaw) |
| Language | de |
| Category | natural_language |
| Queries | 200 |
| Documents | 200 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.6765 |
| BM25 hit@10 | 0.7950 |
| Query length avg chars | 71.94 |
| Document length avg chars | 19481.02 |

### Public Sources

- [Towards Intelligent Legal Advisors for Document Retrieval and Question-Answering in German Legal Documents](https://doi.org/10.1109/AIKE52691.2021.00011); 2021; Christoph Hoppe et al.
- [mteb/LegalQuAD dataset card](https://huggingface.co/datasets/mteb/LegalQuAD).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoLaw](https://huggingface.co/datasets/hakari-bench/NanoLaw)
- Source dataset: [mteb/LegalQuAD](https://huggingface.co/datasets/mteb/LegalQuAD)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Towards Intelligent Legal Advisors for Document Retrieval and Question-Answering in German Legal Documents | 2021 | IEEE DOI record | https://doi.org/10.1109/AIKE52691.2021.00011 |
| LegalQuAD | 2025 | Hugging Face dataset card | https://huggingface.co/datasets/mteb/LegalQuAD |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoLaw
  backing_dataset: NanoLaw
  dataset_id: hakari-bench/NanoLaw
  task_name: NanoLegalQuAD
  split_name: NanoLegalQuAD
  language: de
  category: natural_language
  document_path: docs/benchmark_tasks/NanoLaw/NanoLegalQuAD.md
  source_research:
    primary_source_type: task_doi_and_dataset_card
    paper_pdf_or_html_checked: false
    no_paper_note: no_freely_accessible_full_text_confirmed
  counts:
    queries: 200
    documents: 200
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 71.94
    document_mean: 19481.02
  bm25:
    ndcg_at_10: 0.6765084712604355
    hit_at_10: 0.795
    source: dataset_bm25_column
  learning:
    original_train_split: unknown
    evaluation_split_origin: legalquad_test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoLegalQuAD questions, qrels, and positive German legal documents
    useful_training_data:
      - German legal QA
      - question-to-judgment retrieval
      - long-document German legal search
      - same-statute German legal hard negatives
    synthetic_data:
      document_generation: German court decisions containing answer-bearing passages
      question_generation: concise German legal questions
      answerability: positives should contain the legal discussion needed to answer the question
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoLaw
    source_urls:
      - label: LegalQuAD DOI
        url: https://doi.org/10.1109/AIKE52691.2021.00011
      - label: MTEB LegalQuAD
        url: https://huggingface.co/datasets/mteb/LegalQuAD
    source_notes:
      - full paper text not confirmed as freely accessible during first pass
  references:
    - title: "Towards Intelligent Legal Advisors for Document Retrieval and Question-Answering in German Legal Documents"
      url: https://doi.org/10.1109/AIKE52691.2021.00011
      year: 2021
      doi: 10.1109/AIKE52691.2021.00011
      is_paper: true
      source_confidence: definitive_paper_link
```
