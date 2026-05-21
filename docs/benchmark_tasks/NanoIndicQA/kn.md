# NanoIndicQA / kn

## Overview

`NanoIndicQA / kn` is the Kannada split of IndicQA retrieval. Kannada questions
retrieve Kannada evidence paragraphs.

## Details

### What the Original Data Measures

IndicQA, described in [Towards Leaving No Indic Language Behind](https://arxiv.org/abs/2212.05409),
is a manually curated cloze-style reading-comprehension task. The retrieval
conversion asks models to retrieve the context paragraph for each question.

### Observed Data Profile

The Nano split has 200 queries, 257 documents, and 200 positive qrel rows. Each
query has one positive. Queries average 53.27 characters and documents average
882.74 characters. The examples show several questions about Nepal mapped to the
same context.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.4730
and hit@10 = 0.6000. It ranks 70 positives at rank 1 and 120 in the top 10.
All positives are within the top 100.

### Training Data That May Help

Kannada QA, Kannada Wikipedia passage retrieval, and Indic multilingual
retrieval training should help. Topic-neighbor negatives are important because
multiple history/geography contexts share terms.

### Synthetic Data Guidance

Generate Kannada questions from context paragraphs, with multiple questions per
paragraph. Preserve full context positives and include nearby history/geography
paragraphs as negatives.

## Example Data

| Query | Positive document |
| --- | --- |
| ಮುಸ್ಲಿಂ-ಬಹುಸಂಖ್ಯಾತ ಪ್ರದೇಶ ಯಾವುದು? (33 chars) | 1947ರಲ್ಲಿ, ಕಾಶ್ಮೀರದ ಜನಸಂಖ್ಯೆಯ "ಶೇಕಡಾ 77ರಷ್ಟು ಭಾಗವು ಮುಸ್ಲಿಮರಿಂದ ಕೂಡಿತ್ತು ಮತ್ತು ತನ್ನೊಂದು ಗಡಿಯನ್ನು ಅದು ಪಾಕಿಸ್ತಾನದೊಂದಿಗೆ ಹಂಚಿಕೊಂಡಿತ್ತು. ಆದ್ದರಿಂದ, ಬ್ರಿಟಿಷ್‌ ಸಾರ್ವಭೌಮತೆಯು ಆಗಸ್ಟ್‌ನ 14-15ರಂದು ಕೊನೆಗೊಂಡಾಗ, ಮಹಾರಾಜನು ಪಾಕಿಸ್ತಾನವನ್ನು ಅಂಗೀಕ ... [truncated 225 chars](1598 chars) |
| ಚೆನ್ನೈ ಪದದ ಅರ್ಥವೇನು? (20 chars) | 'ಮದ್ರಾಸು' ಎಂಬ ಹೆಸರು 'ಮದ್ರಾಸುಪಟ್ನಂ' ಪದದಿಂದ ಬಂದಿದೆ, ಈ ಜಾಗವನ್ನು ಬ್ರಿಟೀಷ್ ಈಸ್ಟ್ ಇಂಡಿಯಾ ಕಂಪನಿ ಖಾಯಂ ನೆಲೆಗಾಗಿ 1639 ರಲ್ಲಿ ಆಯ್ಕೆ ಮಾಡಿಕೊಂಡಿತು. https://www. mapsofindia. com/on-this-day/22nd-august-1639-madras-now-chennai-is-founded-by- ... [truncated 225 chars](599 chars) |
| ಕಾರು ಪ್ರಿಯರು ಯಾವ ವಿವಿಧ ಮಾದರಿಯ ಕಾರು ಗಳನ್ನು ನೋಡಬಹುದು ? (53 chars) | ಅರಮನೆಗಳು ಮತ್ತು ಕೋಟೆಗಳ ಹೊರತಾಗಿ ಜೈಪುರದಲ್ಲಿನ ಹಬ್ಬಗಳು ಮತ್ತು ಮೇಳಗಳೂ ತುಂಬಾ ಜನಪ್ರಿಯವಾಗಿದೆ. ಇಲ್ಲಿನ ಮೇಳಗಳಲ್ಲಿ ಒಂದೆಂದರೆ ಜೈಪುರ ವಿಂಟೇಜ್ ಕಾರ್ ರ್ಯಾಲಿ. ಇದನ್ನು ಜನವರಿಯಲ್ಲಿ ನಡೆಸಲಾಗುತ್ತದೆ. ಇತ್ತೀಚೆಗೆ ಈ ಮೇಳವು ತುಂಬಾ ಜನಪ್ರಿಯವಾಗುತ್ತಿದೆ. ಕಾರು ಪ್ರಿಯರು ... [truncated 225 chars](978 chars) |
| ಬ್ರಿಟಿಶ್ ಈಸ್ಟ್ ಇಂಡಿಯಾ ಕಂಪನಿಯನ್ನು ಯಾವ ನದಿಯ ಪ್ರದೇಶದಲ್ಲಿ ಸ್ಥಾಪಿಸಲಾಯಿತು? (68 chars) | 19ನೇ ಶತಮಾನದಿಂದ ಈ ಪ್ರದೇಶದ ಕುರಿತು ಹಲವು ಬೇರೆಬೇರೆ ತರಹದ ವಿವರಣೆಗಳಿವೆ, ಮತ್ತು ಮೊದಲು ಹೆಸರುಗಳಿವೆ ಹಾಗು ರಾಜ್ಯದ ಸರಹದ್ದುಗಳಿವೆ, ಅಂದರೆ, ಬ್ರಿಟೀಷ್ ಈಸ್ಟ್ ಇಂಡಿಯಾ ಕಂಪನಿಯು ತನ್ನ ಪ್ರಾಬಲ್ಯದ ಅಡಿಯಲ್ಲಿ ಗಂಗಾ ನದಿಯ ಸಮತಲದಲ್ಲಿ ಸ್ಥಾಪಿತಗೊಳಿಸಿದ ನಂತರ. 1833 ರಲ್ಲಿ ... [truncated 225 chars](1101 chars) |
| ಅಲಿಘಢ್‍ಗೆ ಭೇಟಿ ನೀಡಲು ಉತ್ತಮ ಸಮಯ ಯಾವುದು? (39 chars) | ಅಲಿಘಢ್‍ನಲ್ಲಿ ಮಾನ್ಸೂನ್ ಪ್ರಭಾವಿತ ಹವಾಮಾನವಿದೆ. ಉತ್ತರ-ಕೇಂದ್ರ ಭಾಗದಲ್ಲಿರುವ ಸಮಶೀತೋಷ್ಣ ಆರ್ದ್ರತೆಯುಳ್ಳ ವಾತಾವರಣ ಕಾಣುತ್ತದೆ. ಏಪ್ರಿಲ್‍ನಲ್ಲಿ ಆರಂಭವಾಗುವ ಬೇಸಿಗೆಯು ಮೇ ತಿಂಗಳಲ್ಲಿ ಅಧಿಕ ಉಷ್ಣತೆ ಹೊಂದಿರುತ್ತದೆ. ಸರಾಸರಿ ಉಷ್ಣತೆಯು 28–33 °C (82–91 °F)ರ ನಡುವೆ ... [truncated 225 chars](618 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoIndicQA |
| Backing dataset | NanoIndicQA |
| Task / split | kn |
| Hugging Face dataset | [hakari-bench/NanoIndicQA](https://huggingface.co/datasets/hakari-bench/NanoIndicQA) |
| Language | kn |
| Category | natural_language |
| Queries | 200 |
| Documents | 257 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.4730 |
| BM25 hit@10 | 0.6000 |
| Query length avg chars | 53.27 |
| Document length avg chars | 882.74 |

### Public Sources

- [Towards Leaving No Indic Language Behind](https://arxiv.org/abs/2212.05409), ACL 2023.
- [mteb/IndicQARetrieval](https://huggingface.co/datasets/mteb/IndicQARetrieval).
- [ai4bharat/IndicQA](https://huggingface.co/datasets/ai4bharat/IndicQA).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoIndicQA](https://huggingface.co/datasets/hakari-bench/NanoIndicQA)
- Source task dataset: [mteb/IndicQARetrieval](https://huggingface.co/datasets/mteb/IndicQARetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Towards Leaving No Indic Language Behind | 2023 | paper | https://arxiv.org/abs/2212.05409 |
| mteb/IndicQARetrieval |  | dataset card | https://huggingface.co/datasets/mteb/IndicQARetrieval |
| ai4bharat/IndicQA |  | dataset card | https://huggingface.co/datasets/ai4bharat/IndicQA |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoIndicQA
  backing_dataset: NanoIndicQA
  dataset_id: hakari-bench/NanoIndicQA
  task_name: kn
  split_name: kn
  language: kn
  category: natural_language
  document_path: docs/benchmark_tasks/NanoIndicQA/kn.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 257
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 53.265
    document_mean: 882.735409
  bm25:
    ndcg_at_10: 0.4730209757
    hit_at_10: 0.6
    source: dataset_bm25_column
  example_count: 5
```
