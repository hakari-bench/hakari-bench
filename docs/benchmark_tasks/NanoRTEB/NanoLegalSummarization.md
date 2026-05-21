# NanoRTEB / NanoLegalSummarization

## Overview

`NanoRTEB / NanoLegalSummarization` retrieves source legal text passages for
plain-English contract or terms-of-service summaries.

## Details

### What the Original Data Measures

[Plain English Summarization of Contracts](https://aclanthology.org/W19-2201/)
introduces a corpus of contract clauses paired with plain-English
summaries, targeting legal text simplification and summarization. RTEB
repurposes this alignment as retrieval: the simplified summary acts as the
query and the corresponding legal text excerpt is the relevant document.

[Introducing RTEB: A New Standard for Retrieval Evaluation](https://huggingface.co/blog/rteb)
lists LegalSummarization as an open English legal dataset and notes that the
summaries were manually reviewed for quality. This retrieval form tests whether
a model can connect informal legal explanations with the formal clause text.

### Observed Data Profile

The split has 200 queries, 438 documents, and 345 positive qrel rows. Queries
are short summaries averaging 103.06 characters, while documents average 606.16
characters. Most queries have one positive, but 56 queries have multiple
matching excerpts and the maximum is 11.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.5374 and hit@10 = 0.7400. It ranks 89 queries at rank 1 and 148 within the
top 10.

BM25 benefits from repeated legal terms and product names, but the task often
requires matching a simplified phrase such as "don't die or hurt others" to a
formal liability or safe-use clause.

### Training Data That May Help

Useful training data includes legal simplification, clause-summary pairs,
contract passage retrieval, and hard negatives from the same terms-of-service
document. Models should learn both legal terminology and lay paraphrases.

### Synthetic Data Guidance

Generate plain-English summaries from non-evaluation contract clauses and pair
them with the original clause. Include paraphrases with informal language,
negative obligations, liability limits, and user-rights language. Hard negatives
should be nearby clauses from the same contract.

## Example Data

| Query | Positive document |
| --- | --- |
| this service may collect use and share location data. (53 chars) | apple and our partners and licensees may collect use and share precise location data including the real time geographic location of your apple computer or device. where available location based services may use gps bluetooth ... [truncated 225 chars](740 chars) |
| you may mod the game but don t distribute hacked clients. (57 chars) | if you ve bought the game you may play around with it and modify it. we d appreciate it if you didn t use this for griefing though and remember not to distribute the changed versions of our software. basically mods or plugins ... [truncated 225 chars](349 chars) |
| if you haven t played for a year you mess up or we mess up we can delete all of your virtual goods. we don t have to give them back. we might even discontinue some virtual goods entirely but we ll give you 60 days advance not ... [truncated 225 chars](245 chars) | we may cancel suspend or terminate your account and your access to your trading items virtual money virtual goods the content or the services in our sole discretion and without prior notice including if a your account is inac ... [truncated 225 chars](1441 chars) |
| the service makes critical changes to its terms without user involvement. (73 chars) | gitlab reserves the right at its sole discretion to modify or replace any part of this agreement. it is your responsibility to check this agreement periodically for changes. your continued use of or access to the website foll ... [truncated 225 chars](624 chars) |
| dropbox along with their third parties are allowed to access scan store and duplicate content that you put on the service. (122 chars) | when you use our services you provide us with things like your files content email messages contacts and so on your stuff. your stuff is yours. these terms don t give us any rights to your stuff except for the limited rights ... [truncated 225 chars](714 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRTEB |
| Backing dataset | NanoRTEB |
| Task / split | NanoLegalSummarization |
| Hugging Face dataset | [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB) |
| Source dataset | [mteb/legal_summarization](https://huggingface.co/datasets/mteb/legal_summarization) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 438 |
| Positive qrels | 345 |
| Positives per query | avg 1.73 / min 1 / median 1 / max 11 |
| Multi-positive queries | 56 |
| BM25 nDCG@10 | 0.5374 |
| BM25 hit@10 | 0.7400 |
| Query length avg chars | 103.06 |
| Document length avg chars | 606.16 |

### Public Sources

- [Plain English Summarization of Contracts](https://aclanthology.org/W19-2201/), task paper.
- [mteb/legal_summarization](https://huggingface.co/datasets/mteb/legal_summarization), source retrieval dataset card.
- [Introducing RTEB: A New Standard for Retrieval Evaluation](https://huggingface.co/blog/rteb), RTEB benchmark announcement.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB)
- Source task dataset: [mteb/legal_summarization](https://huggingface.co/datasets/mteb/legal_summarization)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Plain English Summarization of Contracts | 2019 | task paper | https://aclanthology.org/W19-2201/ |
| mteb/legal_summarization |  | dataset card | https://huggingface.co/datasets/mteb/legal_summarization |
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
  task_name: NanoLegalSummarization
  split_name: NanoLegalSummarization
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRTEB/NanoLegalSummarization.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 438
    positive_qrels: 345
  positives_per_query:
    average: 1.725
    min: 1
    median: 1.0
    max: 11
    multi_positive_queries: 56
    multi_positive_query_percent: 28.0
  text_stats_chars:
    query_mean: 103.06
    document_mean: 606.16
  bm25:
    ndcg_at_10: 0.5374
    hit_at_10: 0.74
    source: dataset_bm25_column
  example_count: 5
```
