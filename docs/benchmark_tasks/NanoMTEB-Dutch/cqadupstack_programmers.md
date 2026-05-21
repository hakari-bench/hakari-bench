# NanoMTEB-Dutch / cqadupstack_programmers

## Overview

`cqadupstack_programmers` is the Dutch-translated Programmers subforum split of
CQADupStack. Queries are software-engineering questions and positives are older
duplicate forum questions. The task focuses on conceptual programming practice:
design tradeoffs, debugging habits, interfaces, refactoring, and methodology.

## Details

### What the Original Data Measures

[CQADupStack](https://doi.org/10.1145/2838931.2838934) frames duplicate
question retrieval as finding previously answered questions in community QA
archives. The dataset uses StackExchange duplicate labels and predefined splits
for reproducible retrieval experiments. [BEIR](https://arxiv.org/abs/2104.08663)
includes CQADupStack as a diverse zero-shot retrieval dataset, and
[BEIR-NL](https://aclanthology.org/2025.bucc-1.5/) translates BEIR datasets into
Dutch.

This split is less code-snippet oriented than the Mathematica split. It is about
software engineering intent and opinion-like conceptual duplicates, which can be
lexically broad.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrel rows.
Each query has one positive. Queries average 61.25 characters and documents
average 1,142.35 characters. Examples include God classes, recovering from
mistakes, quick fixes versus good solutions, interfaces for every class, and
avoiding typos.

Many positive documents are long discussion-style posts. They may share few
surface terms with the query while still asking the same design or work-practice
question.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.2991
and hit@10 = 0.4150. Keywords like interface, class, Agile, or refactoring help,
but the duplicate relation often depends on broader software-engineering
semantics and stance.

### Training Data That May Help

Useful training data includes non-overlapping Programmers or Software
Engineering Stack Exchange duplicate pairs, Dutch-translated developer QA, and
technical discussion pairs with conceptual duplicate labels. Exclude this Nano
test split and positives.

### Synthetic Data Guidance

Generate Dutch software-engineering questions from non-evaluation discussion
posts. Create duplicate paraphrases with different framing, such as practical
experience, design principle, or team-process wording. Use hard negatives from
the same topic that ask a different tradeoff.

## Example Data

| Query | Positive document |
| --- | --- |
| Moet ik blijven investeren in datastructuren en algoritmes? (59 chars) | Hoe belangrijk is het leren van algoritmes voor programmeurs van hogere programmeertalen? **Mogelijk duplicaat:** > Hoe belangrijk is het bestuderen van algoritmes en theorie om een geweldige > programmeur te worden? Vandaag ... [truncated 225 chars](632 chars) |
| Django leren aan de hand van voorbeelden (40 chars) | Hoe begrijp ik het Django framework goed? Ik heb redelijke kennis van PHP, d.w.z. ik kan een framework pakken, de code lezen en als de documentatie adequaat is, begrijpen wat het doet. De belangrijkste reden hiervoor is dat P ... [truncated 225 chars](786 chars) |
| Licentieverificatie en contact opnemen met de thuisserver (57 chars) | Softwarelicentie veilig valideren Ik ontwikkel momenteel een product (in C#) dat gratis te downloaden is, maar een maandelijks abonnement vereist om na een specifieke proefperiode te kunnen gebruiken. Mijn bedoeling is dat de ... [truncated 225 chars](1674 chars) |
| Als ik .NET Framework gebruik voor mijn applicatie, moet ik dan iets aan Microsoft betalen? (91 chars) | Ik wil mijn software verkopen [C# desktop applicatie], maar zit vast met licenties **Mogelijk duplicaat:** > Als ik .NET Framework gebruik voor mijn applicatie, moet ik dan iets aan > Microsoft betalen? Ik heb een desktop app ... [truncated 225 chars](1229 chars) |
| Wat is een goede uitleg voor pointers? (38 chars) | Wat is de definitie van een pointer? Conceptueel is een "pointer" gewoon iets dat naar iets anders "wijst"; Is deze definitie voldoende om precies te zeggen wat een pointer is in programmeertalen? Moet het nog andere kenmerke ... [truncated 225 chars](860 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Dutch |
| Backing dataset | NanoMTEB-Dutch |
| Task / split | cqadupstack_programmers |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch) |
| Source dataset | [clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack) |
| Language | nl |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.2991 |
| BM25 hit@10 | 0.4150 |
| Query length avg chars | 61.25 |
| Document length avg chars | 1,142.35 |

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
  task_name: cqadupstack_programmers
  split_name: cqadupstack_programmers
  language: nl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Dutch/cqadupstack_programmers.md
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
    query_mean: 61.25
    document_mean: 1142.3499
  bm25:
    ndcg_at_10: 0.2990881643
    hit_at_10: 0.415
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: "CQADupstackProgrammers-NL test split from clips/beir-nl-cqadupstack"
    train_eval_overlap_audit: not_audited
    leakage_note: "Exclude translated CQADupStack Programmers test queries and duplicate positives used by this Nano split."
    useful_training_data:
      - non-overlapping Software Engineering Stack Exchange duplicate-question pairs
      - Dutch-translated developer discussion QA
      - conceptual programming duplicate-question data with overlap removed
    synthetic_data:
      document_generation: "Dutch software-engineering discussion questions outside the evaluation set."
      question_generation: "Paraphrased duplicate questions about the same design or process tradeoff."
      answerability: "Each query should duplicate one prior programming-practice question, with same-topic hard negatives."
    multi_positive_training: single_positive
  example_count: 5
```
