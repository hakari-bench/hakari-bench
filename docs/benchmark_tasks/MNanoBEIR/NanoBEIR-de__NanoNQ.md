# MNanoBEIR / NanoBEIR-de / NanoNQ

## Overview

Natural Questions is a Wikipedia question answering benchmark built from real
Google search questions. `NanoBEIR-de__NanoNQ` is the German MNanoBEIR version:
German translated natural questions must retrieve German translated Wikipedia
passages that contain the answer. The task tests open-domain answer evidence
retrieval for naturally phrased questions.

## Details

### What the Original Data Measures

[Natural Questions: a Benchmark for Question Answering
Research](https://aclanthology.org/Q19-1026/) introduces a corpus of real,
anonymized, aggregated Google search queries paired with Wikipedia pages from
the top search results. Annotators identify long answers, usually paragraphs or
HTML regions, and short answers when possible.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes NQ as a
question-answering retrieval task. [MMTEB: Massive Multilingual Text Embedding
Benchmark](https://arxiv.org/abs/2502.13595) provides the multilingual
benchmark context for this German Nano split.

### Observed Data Profile

The sampled German Nano task has 50 queries, 5,035 documents, and 57 positive
qrel rows. Most queries have one positive document, but 7 queries have multiple
positives. The average query length is 55.38 characters, and the average
document length is 588.54 characters.

The inspected queries ask factual questions about films, colleges, terminology,
television locations, and legislature size. Documents are translated
Wikipedia-style answer passages, sometimes short direct answers and sometimes
longer contextual paragraphs.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.3438 and hit@10 = 0.5400. BM25 ranks a positive first for 10 queries, and the
median first-positive rank is 8.

Lexical retrieval helps when the question repeats a distinctive title or entity,
but many queries require matching paraphrased answer contexts. A model must
connect natural German questions to passages that contain the answer even when
the exact question wording is absent from the document.

### Training Data That May Help

Useful training data includes non-overlapping Natural Questions retrieval data,
open-domain QA evidence retrieval pairs, German or multilingual Wikipedia QA
datasets, and question-to-passage supervision with real user questions.

Training should exclude NQ, BEIR, NanoBEIR, or translated Wikipedia QA records
likely to overlap with these evaluation questions or passages.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation German Wikipedia
passages and generate natural search questions whose answers are present in the
passage. Include who, when, where, how many, and title-based questions.

For joint generation, create answer-bearing Wikipedia-style passages and
questions that require retrieving the supporting passage rather than only
recognizing a named entity.

## Example Data

| Query | Positive document |
| --- | --- |
| Wo findet dieses Jahr die Final Four statt? (43 chars) | Das NCAA Division I Men's Basketball Tournament 2018 war ein 68-Team-K.-o.-Turnier, um den nationalen Meister im Basketball der NCAA Division I für die Saison 2017/18 zu ermitteln. Die 80. Auflage des Turniers begann am 13. M ... [truncated 225 chars](307 chars) |
| War "Die Nacht vor Weihnachten" ursprünglich ein Disney-Film? (61 chars) | Die Idee zu "The Nightmare Before Christmas" entstand 1982 in einem Gedicht, das Tim Burton schrieb, während er als Animator bei Walt Disney Feature Animation arbeitete. Nach dem Erfolg von "Vincent" im selben Jahr begann Wal ... [truncated 225 chars](705 chars) |
| Warum steht der Engel des Nordens in Gateshead? (47 chars) | Laut Gormley hatte die Bedeutung des Engels eine dreifache Bedeutung: Erstens, um darauf hinzuweisen, dass unter der Baustelle über zwei Jahrhunderte hinweg Bergleute arbeiteten; zweitens, um den Übergang von der Industrie- z ... [truncated 225 chars](357 chars) |
| Wo wurde der Dreifünftelkompromiss ursprünglich in der Verfassung festgehalten? (79 chars) | Der Dreifünftelkompromiss findet sich in Artikel 1, Abschnitt 2, Satz 3 der Verfassung der Vereinigten Staaten, der lautet: (123 chars) |
| Wer singt "Someone's Watching Me" zusammen mit Michael Jackson? (63 chars) | "Somebody's Watching Me" ist ein Song des amerikanischen Sängers Rockwell von seinem Debütalbum Somebody's Watching Me (1984). Er erschien am 14. Januar 1984 als Rockwells Debütsingle und Lead-Single des Albums bei Motown. De ... [truncated 225 chars](375 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-de |
| Task / split | NanoNQ |
| Hugging Face dataset | [hakari-bench/NanoBEIR-de](https://huggingface.co/datasets/hakari-bench/NanoBEIR-de) |
| Language | de |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,035 |
| Positive qrels | 57 |
| Avg positives / query | 1.14 |
| Positives per query (min / median / max) | 1 / 1.00 / 2 |
| Queries with multiple positives | 7 (14.0%) |
| BM25 nDCG@10 | 0.3438 |
| BM25 hit@10 | 0.5400 |
| Query length avg chars | 55.38 |
| Document length avg chars | 588.54 |

### Public Sources

- [Natural Questions: a Benchmark for Question Answering Research](https://aclanthology.org/Q19-1026/); 2019; Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris Alberti, Danielle Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, Kristina Toutanova, Llion Jones, Matthew Kelcey, Ming-Wei Chang, Andrew M. Dai, Jakob Uszkoreit, Quoc Le, Slav Petrov; DOI: `10.1162/tacl_a_00276`.
- [Natural Questions dataset page](https://ai.google.com/research/NaturalQuestions).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025; Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Marton Kardos, Ashwin Mathur, and others; DOI: `10.48550/arXiv.2502.13595`.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-de](https://huggingface.co/datasets/hakari-bench/NanoBEIR-de)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Natural Questions: a Benchmark for Question Answering Research | 2019 | task paper | https://aclanthology.org/Q19-1026/ |
| Natural Questions dataset page |  | dataset page | https://ai.google.com/research/NaturalQuestions |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: MNanoBEIR
  backing_dataset: NanoBEIR-de
  dataset_id: hakari-bench/NanoBEIR-de
  task_name: NanoNQ
  split_name: NanoNQ
  language: de
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-de__NanoNQ.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 5035
    positive_qrels: 57
  positives_per_query:
    average: 1.14
    min: 1
    median: 1.0
    max: 2
    multi_positive_queries: 7
    multi_positive_query_percent: 14.0
  text_stats_chars:
    query_mean: 55.38
    document_mean: 588.540417
  bm25:
    ndcg_at_10: 0.343849737
    hit_at_10: 0.54
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: MNanoBEIR German NanoBEIR task split from hakari-bench/NanoBEIR-de
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding Natural Questions, BEIR, or NanoBEIR records likely to overlap with these evaluation questions or passages
    useful_training_data:
      - non-overlapping Natural Questions retrieval data
      - open-domain QA evidence retrieval pairs
      - German or multilingual Wikipedia QA datasets
      - question-to-passage supervision with real user questions
    synthetic_data:
      document_generation: German Wikipedia-style answer passages outside the evaluation set
      question_generation: natural German search questions whose answer is present in the passage
      answerability: positives should contain the answer evidence, not merely mention the same entity
    multi_positive_training: useful_but_not_central
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-de
    source_urls:
      - label: Natural Questions paper
        url: https://aclanthology.org/Q19-1026/
      - label: Natural Questions dataset page
        url: https://ai.google.com/research/NaturalQuestions
      - label: BEIR paper
        url: https://arxiv.org/abs/2104.08663
      - label: MMTEB paper
        url: https://arxiv.org/abs/2502.13595
      - label: Zeta Alpha NanoBEIR collection
        url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes:
      - German task is a multilingual NanoBEIR adaptation of the original English BEIR task
  references:
    - title: "Natural Questions: a Benchmark for Question Answering Research"
      url: https://aclanthology.org/Q19-1026/
      year: 2019
      doi: 10.1162/tacl_a_00276
      is_paper: true
      source_confidence: definitive_paper_link
    - title: Natural Questions dataset page
      url: https://ai.google.com/research/NaturalQuestions
      year: null
      doi: null
      is_paper: false
      source_confidence: definitive_dataset_page
    - title: "BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models"
      url: https://arxiv.org/abs/2104.08663
      year: 2021
      doi: 10.48550/arXiv.2104.08663
      is_paper: true
      source_confidence: benchmark_context_paper
    - title: "MMTEB: Massive Multilingual Text Embedding Benchmark"
      url: https://arxiv.org/abs/2502.13595
      year: 2025
      doi: 10.48550/arXiv.2502.13595
      is_paper: true
      source_confidence: benchmark_context_paper
    - title: "NanoBEIR: Smaller BEIR dataset subsets"
      url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
      year: 2024
      doi: null
      is_paper: false
      source_confidence: dataset_collection
```
