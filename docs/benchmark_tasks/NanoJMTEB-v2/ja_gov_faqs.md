# NanoJMTEB-v2 / ja_gov_faqs

## Overview

`NanoJMTEB-v2 / ja_gov_faqs` is the Nano split for JaGovFaqs-22k. Japanese FAQ
questions from government and bureau websites must retrieve their corresponding
answers. The task is a question-to-answer retrieval benchmark for formal public
administration language.

## Details

### What the Original Data Measures

The JMTEB card describes JaGovFaqs-22k as FAQs manually extracted from Japanese
bureau websites. The query side contains the FAQ questions and the corpus side
contains shuffled FAQ answers; the retrieval goal is to match each question to
its answer. Unlike web search, the positive document is an answer passage rather
than the page that originally caused a generated question.

This makes the task a test of Japanese administrative language, policy terms,
forms, dates, procedures, and legal or procurement terminology. Many questions
are long and precise, while some answers are short and depend on bureaucratic
context.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrel rows.
Every query has one positive answer. Queries average 59.97 characters and often
contain formal Japanese punctuation, numbered FAQ references, document names, or
application schedules. Documents average 193.38 characters, ranging from very
short direct answers to multi-sentence procedural explanations.

The examples show several answer styles: direct yes/no responses, references to
external schedules, legal-category explanations, and compact statements that only
make sense when paired with the original FAQ question. This makes the benchmark
hard for models that rely only on high lexical overlap.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.1586
and hit@10 = 0.1650. It places only 31 of 200 positives at rank 1 and 33 in the
top 10, although all positives appear somewhere within the top 100.

The low top-10 score reflects answer-side wording mismatch. Questions can name a
public program, deadline, or regulation, while the answer may be a terse phrase
such as "there is no current plan" or a procedural URL. A strong model needs to
connect official question phrasing to the corresponding answer intent, not just
match rare legal tokens.

### Training Data That May Help

Useful training data includes Japanese FAQ question-answer pairs, government
support-center retrieval data, administrative procedure QA, and legal/policy
question-answer matching. Data should preserve formal wording and answer brevity.
Training should exclude the same upstream FAQ pairs used in this evaluation.

### Synthetic Data Guidance

Synthetic data should generate realistic Japanese administrative questions and
matching answers over permits, procurement, applications, schedules, laws, and
public-service procedures. Include short answers, answer-only references to
previous FAQ numbers, dates, and URLs. Avoid making every answer restate the full
question, because the real task often requires bridging question context to a
short answer.

## Example Data

| Query | Positive document |
| --- | --- |
| 入学後に家計が苦しくなった場合、後から申し込むことは可能ですか。 (32 chars) | 入学後に申し込むことも可能です。災害や生計維持者（父母等）の死亡などの予期できない事情があって家計が急変した場合には、特例的に、随時申込みを受け付け、急変後の所得に基づいて要件を満たすかどうかを判定し、支援対象とします。（資料７参照）（大学等の事務担当者におかれては、「授業料等減免事務処理要領」及びJASSOからの案内を御確認 の上、学生等の相談に応じていただけるよう、お願いします。） (194 chars) |
| 公的研究機関の場合、「事情」欄はどのように記載すればよいですか。 (32 chars) | 出願人が研究所の場合は、「出願人○○は公的研究機関である」と記載してください。なお、出願人が都道府県名等であって、当該研究所名と異なる場合は、ガイドラインのII. 5.（1）②の記載を参考にしてください。 (102 chars) |
| どのような手数料が必要ですか。 (15 chars) | 法人文書の開示にあたっては、情報公開法の規定による「開示請求手数料」および「開示実施手数料」の納付が必要です。開示請求手数料は、法人文書1件について300円の納付が必要です。開示実施手数料は、文書の種類、開示の実施方法、開示文書の量等により計算した額から開示請求の際に納付された300円を減額した額が納付する額となります。納付する開示実施手数料の額は、開示決定通知書に記載しお知らせします。 (195 chars) |
| 申請用総合ソフトのインストール先のドライブを変更することはできますか。 (35 chars) | 利用するＰＣの既定のシステムドライブに自動的にインストールされるため，保存先ドライブを変更することはできません。 (56 chars) |
| 最近の実際の放射性検査の結果を知りたい。 (20 chars) | 世界で最も厳しいレベルの基準値を超える品目は、近年ほとんどありません。 (35 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoJMTEB-v2 |
| Backing dataset | NanoJMTEB-v2 |
| Task / split | ja_gov_faqs |
| Hugging Face dataset | [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2) |
| Language | ja |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.1586 |
| BM25 hit@10 | 0.1650 |
| Query length avg chars | 59.97 |
| Document length avg chars | 193.38 |

### Public Sources

- [sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB), source card describing JaGovFaqs-22k.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), 2022.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2)
- Source task dataset: [mteb/JaGovFaqsRetrieval](https://huggingface.co/datasets/mteb/JaGovFaqsRetrieval)
- JMTEB source dataset: [sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| sbintuitions/JMTEB | 2024 | dataset card | https://huggingface.co/datasets/sbintuitions/JMTEB |
| MTEB: Massive Text Embedding Benchmark | 2022 | paper | https://arxiv.org/abs/2210.07316 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoJMTEB-v2
  backing_dataset: NanoJMTEB-v2
  dataset_id: hakari-bench/NanoJMTEB-v2
  task_name: ja_gov_faqs
  split_name: ja_gov_faqs
  language: ja
  category: natural_language
  document_path: docs/benchmark_tasks/NanoJMTEB-v2/ja_gov_faqs.md
  source_research:
    primary_source_type: dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: "No standalone JaGovFaqs paper was confirmed; JMTEB dataset card was checked."
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
    query_mean: 59.97
    document_mean: 193.3841
  bm25:
    ndcg_at_10: 0.1586009307
    hit_at_10: 0.165
    source: dataset_bm25_column
  example_count: 5
```
