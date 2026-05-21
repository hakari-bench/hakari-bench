# NanoMMTEB-v2 / mlqa

## Overview

`mlqa` is a multilingual QA retrieval task derived from MLQA. Queries are
questions in Arabic, German, Spanish, Hindi, Vietnamese, Chinese, and English,
and documents are Wikipedia-style context passages. The task tests cross-lingual
and multilingual passage retrieval for extractive QA.

## Details

### What the Original Data Measures

[MLQA: Evaluating Cross-lingual Extractive Question Answering](https://arxiv.org/abs/1910.07475)
introduces a multi-way aligned extractive QA benchmark in seven languages. The
paper describes Wikipedia contexts and questions designed so many QA instances
are parallel across languages. The retrieval version uses questions as queries
and their answer-bearing contexts as positive documents.

### Observed Data Profile

The split has 196 queries, 10,000 documents, and 196 positive qrels. Each query
has one positive. Queries average 47.38 characters and documents average 731.33
characters. The examples show cross-lingual behavior: some Arabic or Spanish
queries retrieve passages in Spanish, Arabic, Hindi, or English.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.0503
and hit@10 = 0.0816. Lexical matching is very weak when query and positive
passage languages differ, and even monolingual pairs often require answer-span
semantics rather than exact token overlap.

### Training Data That May Help

Useful data includes MLQA train-compatible resources such as SQuAD-style QA,
cross-lingual QA retrieval, multilingual Wikipedia passage retrieval, and
parallel question-context pairs outside the evaluation split. Overlap with MLQA
validation/test examples should be excluded.

### Synthetic Data Guidance

Generate questions from non-evaluation Wikipedia passages in each target
language, and include cross-lingual variants where the query and context are in
different MLQA languages. Positives must contain the answer span or an explicit
answer-bearing sentence; hard negatives should share the article topic without
answering the question.

## Example Data

| Query | Positive document |
| --- | --- |
| Phiên dịch được sử dụng cho ngôn ngữ nào? (41 chars) | Nói chung, tất cả mọi người trong nước đều hiểu và nói tiếng Nga, ngoại trừ tại một số vùng xa xôi hẻo lánh. Tiếng Nga là tiếng mẹ đẻ của đa số dân cư Bishkek, và hầu hết các giao dịch thương mại cũng như chính trị đều được t ... [truncated 225 chars](539 chars) |
| ما هي التقنيات الحديثة المستخدمة للوصول إلى الإنترنت عبر الهاتف المحمول؟ (72 chars) | Reichweite und Bandbreite: Mobiler Internetzugriff ist generell langsamer als direkte Kabelverbindungen. Verwendete Technologien sind hier GPRS, oder EDGE, aktuell auch HSDPA und HSUPA, 3G und 4G Netzwerke, sowie das neue 5G ... [truncated 225 chars](435 chars) |
| Was wurde in den 1990er Jahren eingeführt? (42 chars) | أما القديس فالنتين الذي كان يعيش في تورني فقد أصبح أسقفًا لمدينة انترامنا (الاسم الحديث لمدينة تورني) تقريبًا في عام 197 بعد الميلاد، ويُقال إنه قد قُتل فترة الاضطهاد التي تعرض له المسيحيون أثناء عهد الإمبراطور أوريليان. وجرى ... [truncated 225 chars](407 chars) |
| TB-3 là loại phương tiện vận tải gì? (36 chars) | 图波列夫TB-3（俄语：Тяжёлый Бомбардировщик，转写：Tyazholy Bombardirovschik，意为重型轰炸机；民用型则称为ANT-6）是西元1930年代苏联空军列装的重型轰炸机，并被使用于第二次世界大战。它是世界上第一个悬翼四引擎的重型轰炸机。 西元1939年，TB-3因过时而正式退役，但TB-3仍在整个二次世界大战进行轰炸和运输工作。 TB-3也以Zveno计划战斗机母机和轻型战车运输机的角色参加战斗。 (221 chars) |
| बाह्यत्वचा की कोशिकाएं क्या कर सकती हैं? (40 chars) | The plant epidermis is specialised tissue, composed of parenchyma cells, that covers the external surfaces of leaves, stems and roots. Several cell types may be present in the epidermis. Notable among these are the stomatal g ... [truncated 225 chars](1229 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMMTEB-v2 |
| Backing dataset | NanoMMTEB-v2 |
| Task / split | mlqa |
| Hugging Face dataset | [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2) |
| Source dataset | [mteb/MLQARetrieval](https://huggingface.co/datasets/mteb/MLQARetrieval) |
| Language | multilingual |
| Category | natural_language |
| Queries | 196 |
| Documents | 10000 |
| Positive qrels | 196 |
| BM25 nDCG@10 | 0.0503 |
| BM25 hit@10 | 0.0816 |
| Query length avg chars | 47.38 |
| Document length avg chars | 731.33 |

### Public Sources

- [MLQA: Evaluating Cross-lingual Extractive Question Answering](https://arxiv.org/abs/1910.07475).
- [MLQA dataset](https://huggingface.co/datasets/mlqa).
- [mteb/MLQARetrieval](https://huggingface.co/datasets/mteb/MLQARetrieval).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2)
- Source dataset: [mteb/MLQARetrieval](https://huggingface.co/datasets/mteb/MLQARetrieval)
- Upstream dataset: [mlqa](https://huggingface.co/datasets/mlqa)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MLQA: Evaluating Cross-lingual Extractive Question Answering | 2019 | task paper | https://arxiv.org/abs/1910.07475 |
| MLQA dataset | 2019 | dataset card | https://huggingface.co/datasets/mlqa |
| mteb/MLQARetrieval | 2024 | dataset card | https://huggingface.co/datasets/mteb/MLQARetrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMMTEB-v2
  backing_dataset: NanoMMTEB-v2
  dataset_id: hakari-bench/NanoMMTEB-v2
  task_name: mlqa
  split_name: mlqa
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMMTEB-v2/mlqa.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 196
    documents: 10000
    positive_qrels: 196
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 47.38265306122449
    document_mean: 731.3334
  bm25:
    ndcg_at_10: 0.050320808056020766
    hit_at_10: 0.08163265306122448
    source: dataset_bm25_column
  learning:
    original_train_split: not_found
    evaluation_split_origin: validation
    train_eval_overlap_audit: not_audited
    leakage_note: do not train on overlapping MLQA validation/test questions, contexts, or positives
    useful_training_data:
      - SQuAD-style QA retrieval
      - multilingual Wikipedia passage retrieval
      - cross-lingual question-context pairs
      - non-overlapping MLQA-style parallel QA data
    synthetic_data:
      document_generation: Wikipedia-style contexts in MLQA languages
      question_generation: native-language and cross-lingual questions targeting explicit answer spans
      answerability: positive passage should contain the answer span or a direct answer-bearing sentence
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2
    source_urls:
      - label: MLQA arXiv
        url: https://arxiv.org/abs/1910.07475
      - label: MLQA dataset
        url: https://huggingface.co/datasets/mlqa
      - label: mteb/MLQARetrieval
        url: https://huggingface.co/datasets/mteb/MLQARetrieval
    source_notes: []
  references:
    - title: "MLQA: Evaluating Cross-lingual Extractive Question Answering"
      url: https://arxiv.org/abs/1910.07475
      year: 2019
      is_paper: true
      source_confidence: definitive_paper_link
```
