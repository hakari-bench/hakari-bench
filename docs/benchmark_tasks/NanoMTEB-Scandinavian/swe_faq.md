# NanoMTEB-Scandinavian / swe_faq

## Overview

SuperLim describes SweFAQ as Swedish FAQ data from the websites of public
authorities, and the retrieval adaptation uses user questions to retrieve the
corresponding government answer. This Nano split is practical public-sector
answer retrieval in Swedish, with many questions about parental leave, child
support, disability benefits, administrative eligibility, `Försäkringskassan`,
`underhållsbidrag`, `föräldrapenning`, and `bilstöd`. The task rewards matching
the citizen's situation to the exact policy answer, not just the same benefit
category.

## Details

### What the Original Data Measures

[Superlim: A Swedish Language Understanding Evaluation Benchmark](https://aclanthology.org/2023.emnlp-main.506/)
describes SweFAQ as a Swedish FAQ dataset. The paper states that the dataset
contains answers to frequently asked questions from websites of nine Swedish
authorities, including the Social Insurance Agency and the Swedish Tax Agency.
The MTEB card describes the retrieval adaptation as a Swedish QA dataset derived
from FAQ, with government, non-fiction, written domains.

### Observed Data Profile

The Nano split has 200 Swedish queries, 511 documents, and 200 positive qrels.
Every query has one positive. Queries average 73.33 characters, and documents
average 319.78 characters. Many examples concern parental leave, child support,
disability benefits, and administrative eligibility conditions.

The language is practical public-sector Swedish, with terms such as
`Försäkringskassan`, `underhållsbidrag`, `föräldrapenning`, and `bilstöd`.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.5449 and hit@10 = 0.7500. BM25 ranks 73 positives first. The task is
moderately hard: some question-answer pairs share administrative terminology,
while others require recognizing that an answer resolves the question without
repeating its full wording.

### Training Data That May Help

Useful training data includes non-overlapping Swedish FAQ question-answer pairs,
public-sector help-center retrieval data, and same-benefit hard negatives.
Training should exclude this Nano split and any duplicated SuperLim/SweFAQ test
items.

### Synthetic Data Guidance

Generate Swedish authority-style FAQ questions and concise policy answers.
Include eligibility, timing, application, payment, and exception cases. Hard
negatives should discuss the same benefit but answer a different practical
question.

## Example Data

| Query | Positive document |
| --- | --- |
| Kan Försäkringskassan utreda min arbetsskada så att jag kan få ersättning från AFA Försäkring? (94 chars) | Nej. Det beror på att vi bara får utreda om det är en arbetsskada om du uppfyller villkoren för att ha rätt till ersättning för din arbetsskada från Försäkringskassan. Det står i lagen. (185 chars) |
| Varför behöver mitt vårdbidragsbeslut följas upp? (49 chars) | Ditt beslut om vårdbidrag ska följas upp minst vartannat år, om det inte finns skäl för uppföljning med längre mellanrum. Beslutet ska också följas upp om förhållanden som påverkar behovet av vårdbidrag ändras. (210 chars) |
| Jag arbetar i Sverige men min familj bor i ett annat EU/EES-land. Kan jag få barnbidrag från Sverige? (101 chars) | Ja, om du arbetar i Sverige och har barn som bor i ett annat medlemsland kan du ha rätt till barnbidrag från Sverige. När föräldrarna bor eller arbetar i var sitt medlemsland behöver utbetalningen av barnbidrag samordnas mell ... [truncated 225 chars](314 chars) |
| Jag arbetar i Sverige men den andra föräldern bor i ett annat land inom EU/EES eller Schweiz. Kan hen få föräldrapenning från Sverige? (134 chars) | Ja, men först behöver vi utreda i vilket land du och barnets andra förälder är försäkrade. Om ni är försäkrade i var sitt land kan ni ha rätt till föräldrapenning från båda länderna. Den förälder som vårdar barnet ska i först ... [truncated 225 chars](443 chars) |
| Vad är LSS? (11 chars) | LSS står för lag om stöd och service till vissa funktionshindrade. I lagen står det att personer med funktionsnedsättningar ska kunna få hjälp att leva som andra. (162 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Scandinavian |
| Backing dataset | NanoMTEB-Scandinavian |
| Task / split | swe_faq |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Scandinavian](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Scandinavian) |
| Language | sv |
| Category | natural_language |
| Queries | 200 |
| Documents | 511 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.5449 |
| BM25 hit@10 | 0.7500 |
| Query length avg chars | 73.33 |
| Document length avg chars | 319.78 |

### Public Sources

- [The Scandinavian Embedding Benchmarks](https://arxiv.org/abs/2406.02396); 2024; Kenneth Enevoldsen et al.
- [Superlim: A Swedish Language Understanding Evaluation Benchmark](https://aclanthology.org/2023.emnlp-main.506/); 2023; Aleksandrs Berdicevskis et al.
- [mteb/SweFaqRetrieval dataset card](https://huggingface.co/datasets/mteb/SweFaqRetrieval).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Scandinavian](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Scandinavian)
- Source task: [mteb/SweFaqRetrieval](https://huggingface.co/datasets/mteb/SweFaqRetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| The Scandinavian Embedding Benchmarks | 2024 | arXiv paper | https://arxiv.org/abs/2406.02396 |
| Superlim: A Swedish Language Understanding Evaluation Benchmark | 2023 | ACL Anthology paper | https://aclanthology.org/2023.emnlp-main.506/ |
| mteb/SweFaqRetrieval | 2024 | dataset card | https://huggingface.co/datasets/mteb/SweFaqRetrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Scandinavian
  backing_dataset: NanoMTEB-Scandinavian
  dataset_id: hakari-bench/NanoMTEB-Scandinavian
  task_name: swe_faq
  split_name: swe_faq
  language: sv
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Scandinavian/swe_faq.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 511
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 73.325
    document_mean: 319.7847358121331
  bm25:
    ndcg_at_10: 0.5449484654219235
    hit_at_10: 0.75
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude SweFAQ/SuperLim test examples, Nano qrels, and answer documents in this split
    useful_training_data:
      - non-overlapping Swedish FAQ question-answer pairs
      - Swedish public-sector help-center retrieval
      - same-benefit hard negatives
      - Swedish administrative QA paraphrases
    synthetic_data:
      document_generation: Swedish authority-style FAQ answers covering eligibility, payment, timing, applications, and exceptions
      question_generation: practical Swedish user questions about benefits, taxes, and public services
      answerability: each positive should directly answer the user's administrative question
    multi_positive_training: single_positive_question_answer_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Scandinavian
    source_urls:
      - label: Scandinavian Embedding Benchmarks
        url: https://arxiv.org/abs/2406.02396
      - label: Superlim paper
        url: https://aclanthology.org/2023.emnlp-main.506/
      - label: mteb/SweFaqRetrieval
        url: https://huggingface.co/datasets/mteb/SweFaqRetrieval
    source_notes: []
  references:
    - title: "Superlim: A Swedish Language Understanding Evaluation Benchmark"
      url: https://aclanthology.org/2023.emnlp-main.506/
      year: 2023
      doi: 10.18653/v1/2023.emnlp-main.506
      is_paper: true
      source_confidence: definitive_paper_link
```
