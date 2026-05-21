# NanoMTEB-German / german_dpr

## Overview

`german_dpr` is the GermanDPR retrieval split in `NanoMTEB-German`. Queries are
German open-domain fact questions, and documents are German Wikipedia passages.
The retriever must find the passage that contains the answer, making this a
German passage-retrieval analogue of DPR-style open-domain QA.

## Details

### What the Original Data Measures

[GermanQuAD and GermanDPR: Improving Non-English Question Answering and Passage Retrieval](https://arxiv.org/abs/2104.12741)
introduces GermanQuAD and then adapts it into GermanDPR, a dataset for dense
passage retrieval. The paper explains that GermanDPR is created by adding hard
negative passages from the full German Wikipedia to GermanQuAD question-answer
pairs. It also reports that the authors train and evaluate one of the first
non-English DPR models.

The source paper is explicit about why the task matters: non-English QA lacks
annotated resources, and machine-translated English QA data does not fully
replace hand-annotated target-language data. In the MTEB version, GermanDPR is
presented as an open-domain QA retrieval task where each question is associated
with a textual context containing the answer.

### Observed Data Profile

The Nano split has 200 queries, 2,876 documents, and 200 positive qrels. Every
query has exactly one positive. Queries average 63.71 characters and are mostly
short German fact questions beginning with forms such as `Welche`, `Wie`, `Was`,
and `Wann`. Documents average 1,288.60 characters and are German Wikipedia
passages, often with the page title repeated at the beginning.

The sampled positives cover entities, dates, locations, transport institutions,
religious demographics, dinosaurs, and cosmology. The task rewards exact
evidence retrieval, but the evidence passage can be semantically close without
sharing all query words.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.4230 and hit@10 = 0.7900. This means lexical retrieval often finds the answer
passage somewhere in the first page of results, but it ranks the correct passage
first for only 32 of 200 queries.

The observed BM25 ranks show the issue: fact questions such as "Wann sind die
Dinosaurier ausgestorben?" find the right passage at rank 7, while other
questions land at ranks 4 or 6. German morphology and paraphrase matter, but so
does entity grounding; the best model needs to connect a concise question to the
passage containing the answer, not just match surface words.

### Training Data That May Help

The original GermanDPR train split is relevant training data if benchmark rules
allow it, but upstream test examples and the Nano split should be excluded from
training. Useful non-overlapping data includes GermanDPR training pairs,
GermanQuAD train contexts reformatted for retrieval, German Wikipedia
question-passage pairs, and hard negatives retrieved from German Wikipedia.

Training should preserve answer-bearing passage supervision and should avoid
turning the task into answer classification. The model must learn to rank the
supporting context, not only predict the answer string.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation German Wikipedia
passages and generate self-contained German fact questions whose answers are
explicitly contained in the passage. For joint generation, create short
encyclopedic passages with titles plus German questions over entities, dates,
counts, and definitions.

Synthetic negatives should be topically close but answer a different question.
Do not seed generation with Nano evaluation questions or positive passages.

## Example Data

| Query | Positive document |
| --- | --- |
| Seit wann gibt es in Iowa keine Todesstrafe mehr? (49 chars) | Todesstrafe_in_den_Vereinigten_Staaten In der Geschichte Iowas gab es 46 Hinrichtungen, davon 43 wegen Mord und drei wegen Vergewaltigung. Alle Getöteten waren Männer. 1872 wurde die Todesstrafe erstmals abgeschafft, aber ber ... [truncated 225 chars](538 chars) |
| Welche Personen sitzen im akademischen Senat? (45 chars) | Universität An der Spitze einer Universität steht ein Rektor oder Präsident, der in der Regel selbst ein Universitätsprofessor ist. Er wird üblicherweise unterstützt von mehreren Prorektoren beziehungsweise Vizepräsidenten, m ... [truncated 225 chars](1042 chars) |
| Für welche Geräte konnte USB 1.0 auch als Stromzufuhr eingesetzt werden? (73 chars) | Universal_Serial_Bus Schon mit USB 1.0 war eine Stromversorgung angeschlossener Geräte über die USB-Kabelverbindungen möglich. Allerdings war die maximale Leistung nur für Geräte mit geringem Strombedarf (wie Maus oder Tastat ... [truncated 225 chars](896 chars) |
| Welche Institution organisiert den öffentlichen Verkehr in London? (66 chars) | London London ist Dreh- und Angelpunkt des Straßen-, Schienen- und Luftverkehrs im Vereinigten Königreich. Das Verkehrswesen fällt in die direkte Zuständigkeit des Mayor of London, des Oberbürgermeisters, der die betriebliche ... [truncated 225 chars](617 chars) |
| Was war der Grund für den Absturz der Boeing 747-300 über Guam 1997? (68 chars) | Guam Am 6. August 1997 wurde eine Boeing 747-300 der Korean Airlines auf dem Korean-Air-Flug 801 von Seoul nach Agana (Guam) bei heftigem Regen gegen einen Hügel 5 km vor dem Flughafen Hagåtña geflogen. Das Flugzeug brach aus ... [truncated 225 chars](1542 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-German |
| Backing dataset | NanoMTEB-German |
| Task / split | german_dpr |
| Hugging Face dataset | [hakari-bench/NanoMTEB-German](https://huggingface.co/datasets/hakari-bench/NanoMTEB-German) |
| Language | de |
| Category | natural_language |
| Queries | 200 |
| Documents | 2,876 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.4230 |
| BM25 hit@10 | 0.7900 |
| Query length avg chars | 63.71 |
| Document length avg chars | 1,288.60 |

### Public Sources

- [GermanQuAD and GermanDPR: Improving Non-English Question Answering and Passage Retrieval](https://arxiv.org/abs/2104.12741); 2021; Timo Möller, Julian Risch, and Malte Pietsch; DOI: `10.48550/arXiv.2104.12741`.
- [ACL Anthology record for GermanQuAD and GermanDPR](https://aclanthology.org/2021.mrqa-1.4/); DOI: `10.18653/v1/2021.mrqa-1.4`.
- [mteb/GermanDPR dataset card](https://huggingface.co/datasets/mteb/GermanDPR).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-German](https://huggingface.co/datasets/hakari-bench/NanoMTEB-German)
- Source dataset: [mteb/GermanDPR](https://huggingface.co/datasets/mteb/GermanDPR)
- Original source dataset: [deepset/germandpr](https://huggingface.co/datasets/deepset/germandpr)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| GermanQuAD and GermanDPR: Improving Non-English Question Answering and Passage Retrieval | 2021 | arXiv paper | https://arxiv.org/abs/2104.12741 |
| GermanQuAD and GermanDPR: Improving Non-English Question Answering and Passage Retrieval | 2021 | proceedings paper | https://aclanthology.org/2021.mrqa-1.4/ |
| mteb/GermanDPR | 2025 | dataset card | https://huggingface.co/datasets/mteb/GermanDPR |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-German
  backing_dataset: NanoMTEB-German
  dataset_id: hakari-bench/NanoMTEB-German
  task_name: german_dpr
  split_name: german_dpr
  language: de
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-German/german_dpr.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2104.12741
    additional_source_urls:
      - https://aclanthology.org/2021.mrqa-1.4/
      - https://huggingface.co/datasets/mteb/GermanDPR
      - https://huggingface.co/datasets/deepset/germandpr
  counts:
    queries: 200
    documents: 2876
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 63.71
    document_mean: 1288.599444
  bm25:
    ndcg_at_10: 0.4230457645
    hit_at_10: 0.79
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude GermanDPR test data, Nano queries, qrels, and positive passages likely to overlap with the evaluation split
    useful_training_data:
      - non-overlapping GermanDPR train pairs
      - GermanQuAD train contexts reformatted for retrieval
      - German Wikipedia question-to-passage pairs
      - German Wikipedia hard negatives selected by BM25 or dense retrieval
    synthetic_data:
      document_generation: German Wikipedia-style passages with titles and explicit answer evidence
      question_generation: self-contained German fact questions over entities, dates, counts, definitions, and locations
      answerability: the positive passage should contain the answer text or enough context to support it
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-German
    source_urls:
      - label: GermanQuAD/GermanDPR arXiv
        url: https://arxiv.org/abs/2104.12741
      - label: ACL Anthology record
        url: https://aclanthology.org/2021.mrqa-1.4/
      - label: mteb/GermanDPR
        url: https://huggingface.co/datasets/mteb/GermanDPR
      - label: deepset/germandpr
        url: https://huggingface.co/datasets/deepset/germandpr
    source_notes: []
  references:
    - title: "GermanQuAD and GermanDPR: Improving Non-English Question Answering and Passage Retrieval"
      url: https://arxiv.org/abs/2104.12741
      year: 2021
      doi: 10.48550/arXiv.2104.12741
      is_paper: true
      source_confidence: definitive_paper_link
```

