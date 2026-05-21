# NanoMTEB-German / gov_service

## Overview

`gov_service` is the German government-service QA retrieval split in
`NanoMTEB-German`. Queries are German citizen questions about Munich municipal
services, and documents are service descriptions from the City of Munich
administration. The retriever must find the service page that contains the
answer or required procedure.

## Details

### What the Original Data Measures

No standalone task paper was confirmed for this dataset. The interpretation is
based on the official [it-at-m/LHM-Dienstleistungen-QA](https://huggingface.co/datasets/it-at-m/LHM-Dienstleistungen-QA)
dataset card, MTEB metadata, and observed Nano samples. The dataset card states
that the data was created from Munich city administration service data, with
texts taken from the `Dienstleistungsfinder` service pages as of November 2022,
and that the format is inspired by GermanQuAD.

The task measures practical public-service retrieval: questions ask what a
citizen must do, which documents are required, whether a procedure is allowed,
or when a step takes place. The positive document is a municipal service text,
not an encyclopedic passage.

### Observed Data Profile

The Nano split has 200 queries, 105 documents, and 200 positive qrels. Every
query has one positive. Queries average 63.88 characters and are direct German
questions such as "Darf man..." or "Was muss man...". Documents average
1,244.25 characters and contain titles, prerequisites, required documents,
timing, fees, and procedural notes.

The sampled positives cover Heilpraktiker permits, taxi or rental-car business
transfer, passport applications for minors, oral exam timing, and passport fees.
The domain is narrow but operationally sensitive: near-duplicate service pages
can share terms while requiring different forms or conditions.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.5875 and hit@10 = 0.8000. The small corpus helps lexical retrieval, and BM25
ranks 78 positives first. Still, the correct service often appears below the
top result because many service descriptions reuse words such as `Antrag`,
`Unterlagen`, `Reisepass`, `Erlaubnis`, and `Termin`.

Strong models should distinguish procedural intent: whether the user asks about
eligibility, required documents, costs, transfer of a business license, or exam
scheduling. This is more like FAQ-to-service matching than open-domain fact QA.

### Training Data That May Help

The source dataset includes train and test splits, but training should avoid the
test split and any examples overlapping the Nano evaluation rows. Useful data
includes non-overlapping LHM-Dienstleistungen-QA train questions, German public
administration FAQ pairs, municipal service descriptions, and citizen
question-to-service mappings from other German cities.

Training should retain procedural language, formal document names, fees,
deadlines, and authority names. Generic paraphrase data helps less than
domain-specific public-service retrieval pairs.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation municipal service pages
and generate German citizen questions about requirements, documents, fees,
appointments, deadlines, and eligibility. For joint generation, create service
descriptions with realistic headings and then ask grounded questions answerable
from one service page.

Synthetic negatives should include related services with overlapping terms, such
as different passport, permit, or vehicle-registration procedures. Do not seed
generation with Nano evaluation questions or positive service texts.

## Example Data

| Query | Positive document |
| --- | --- |
| Was bietet die Abteilung Ferienangebote/Familienpass für die Betreuer:innen an? (79 chars) | Betreuer-innen für Ferienangebote Betreuer*innen für Ferienangebote Du hast Freude im Umgang mit Kindern und Jugendlichen, bist mindestens 18 Jahre alt und suchst einen sinnvollen Ferienjob? Dann melde dich bei uns! Wir, der ... [truncated 225 chars](1283 chars) |
| Was kostet die Heilpraktikerprüfung? (36 chars) | Allgemeine Heilpraktikererlaubnis kertätigkeit in München: Wenn Ihr amtlicher Wohnsitz nicht im Stadtgebiet München liegt, legen Sie Ihren Mietvertrag, Anstellungsvertrag oder andere Dokumente bei, die Ihre heilkundliche Täti ... [truncated 225 chars](1243 chars) |
| Wo muss ich anrufen, wenn ich Fragen zum Thema Ferienangebote habe? (67 chars) | Betreuer-innen für Ferienangebote leitungen und Fachkräfte - eine faire Aufwandsentschädigung, sowie freie Unterkunft und Verpflegung - Tätigkeitsnachweis über dein ehrenamtliches Engagement Benötigte Unterlagen Hast Du Inter ... [truncated 225 chars](1108 chars) |
| Wo bekomme ich einen Antrag auf Wohngeld? (41 chars) | Wohngeld – Mietzuschuss für Mietwohnungen Nachweis Kontoauszüge vorlegen, dürfen Sie Verwendungszweck bzw. Empfänger einer Überweisung – nicht aber deren Höhe - schwärzen, wenn es sich um besondere Kategorien personenbezogene ... [truncated 225 chars](1262 chars) |
| Woher weiß ich als Mieter wie meine Rauchmelder funktionieren? (62 chars) | Rauchmelder werden? Die Rauchwarnmelder müssen so eingebaut oderangebracht und betrieben werden, dass Brandrauchfrühzeitig erkannt und gemeldet wird. Genaue Angabenzur Standortwahl, Montage und Wartung sind in denHerstelleran ... [truncated 225 chars](1174 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-German |
| Backing dataset | NanoMTEB-German |
| Task / split | gov_service |
| Hugging Face dataset | [hakari-bench/NanoMTEB-German](https://huggingface.co/datasets/hakari-bench/NanoMTEB-German) |
| Language | de |
| Category | natural_language |
| Queries | 200 |
| Documents | 105 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.5875 |
| BM25 hit@10 | 0.8000 |
| Query length avg chars | 63.88 |
| Document length avg chars | 1,244.25 |

### Public Sources

- [it-at-m/LHM-Dienstleistungen-QA dataset card](https://huggingface.co/datasets/it-at-m/LHM-Dienstleistungen-QA).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316); 2023.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-German](https://huggingface.co/datasets/hakari-bench/NanoMTEB-German)
- Source dataset: [it-at-m/LHM-Dienstleistungen-QA](https://huggingface.co/datasets/it-at-m/LHM-Dienstleistungen-QA)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| it-at-m/LHM-Dienstleistungen-QA | 2022 | dataset card | https://huggingface.co/datasets/it-at-m/LHM-Dienstleistungen-QA |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-German
  backing_dataset: NanoMTEB-German
  dataset_id: hakari-bench/NanoMTEB-German
  task_name: gov_service
  split_name: gov_service
  language: de
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-German/gov_service.md
  source_research:
    primary_source_type: dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: No standalone task paper was confirmed; interpretation is based on the official dataset card, MTEB metadata, and observed Nano data.
    paper_url: https://arxiv.org/abs/2210.07316
    additional_source_urls:
      - https://arxiv.org/abs/2502.13595
      - https://huggingface.co/datasets/it-at-m/LHM-Dienstleistungen-QA
  counts:
    queries: 200
    documents: 105
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 63.875
    document_mean: 1244.247619
  bm25:
    ndcg_at_10: 0.5875118162
    hit_at_10: 0.8
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude LHM-Dienstleistungen-QA test data, Nano queries, qrels, and positive service texts likely to overlap with the evaluation split
    useful_training_data:
      - non-overlapping LHM-Dienstleistungen-QA train questions
      - German municipal FAQ and service-description retrieval pairs
      - citizen question to public-service page mappings
      - hard negatives from related administrative services
    synthetic_data:
      document_generation: German municipal service pages with requirements, forms, deadlines, fees, appointments, and responsible offices
      question_generation: German citizen questions about eligibility, documents, costs, deadlines, procedures, and appointments
      answerability: the selected service text should directly answer the procedural question
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-German
    source_urls:
      - label: it-at-m/LHM-Dienstleistungen-QA
        url: https://huggingface.co/datasets/it-at-m/LHM-Dienstleistungen-QA
      - label: MTEB arXiv
        url: https://arxiv.org/abs/2210.07316
      - label: MMTEB arXiv
        url: https://arxiv.org/abs/2502.13595
    source_notes: []
  references:
    - title: "it-at-m/LHM-Dienstleistungen-QA"
      url: https://huggingface.co/datasets/it-at-m/LHM-Dienstleistungen-QA
      year: 2022
      doi: null
      is_paper: false
      source_confidence: definitive_dataset_link
    - title: "MTEB: Massive Text Embedding Benchmark"
      url: https://arxiv.org/abs/2210.07316
      year: 2023
      doi: 10.48550/arXiv.2210.07316
      is_paper: true
      source_confidence: definitive_paper_link
```

