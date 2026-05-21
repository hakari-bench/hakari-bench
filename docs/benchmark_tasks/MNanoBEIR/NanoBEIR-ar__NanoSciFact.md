# MNanoBEIR / NanoBEIR-ar / NanoSciFact

## Overview

SciFact is a scientific claim verification dataset where systems retrieve
research abstracts containing evidence for or against a scientific claim.
`NanoBEIR-ar__NanoSciFact` is the Arabic MNanoBEIR version: each query is an
Arabic translated scientific claim, and relevant documents are Arabic
translated scientific abstracts. The task tests evidence retrieval over
specialized scientific and biomedical language.

## Details

### What the Original Data Measures

[Fact or Fiction: Verifying Scientific
Claims](https://arxiv.org/abs/2004.14974) introduces SciFact as a task for
selecting research abstracts that support or refute scientific claims and
identifying rationale sentences. The paper reports 1.4K expert-written claims
paired with evidence-containing abstracts, labels, and rationales. Claims are
atomic scientific statements derived from citation sentences, so verification
requires scientific context and directionality.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes SciFact in its
fact-checking group. [MMTEB: Massive Multilingual Text Embedding
Benchmark](https://arxiv.org/abs/2502.13595) provides the multilingual
evaluation context for this Arabic Nano split. In this retrieval benchmark,
support and refute labels are collapsed into evidence relevance: the first goal
is to find the abstract that can verify the claim.

### Observed Data Profile

The sampled Arabic Nano task has 50 queries, 2,919 documents, and 56 positive
qrel rows. Most queries have one positive; 4 of 50 have multiple positives, and
the maximum is 4. The average query length is 88.96 characters, and the average
document length is 1,316.81 characters.

The inspected claims cover developmental biology, breast cancer risk,
teaching-hospital outcomes, glycolysis and axonal transport, and ivermectin for
lymphatic filariasis. Positive documents are translated scientific abstracts
with methods, results, and biomedical terminology. A retriever must match the
claim to evidence-bearing abstracts, not merely to documents that share one
scientific term.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.5794 and hit@10 = 0.7800. BM25 ranks a positive first for 21 of 50 queries,
and the median first-positive rank is 2. Every query has a positive within the
top 100.

BM25 is helped by distinctive scientific terms such as named genes, diseases,
interventions, and biological processes. The harder cases require understanding
the evidence relation: a claim about glycolysis retrieves an abstract about ATP
for axonal transport, while a claim about cancer risk and placental weight
needs a specific epidemiological abstract. Strong retrievers should preserve
scientific entities, outcome direction, population, and intervention context.

### Training Data That May Help

Useful training data includes the non-overlapping SciFact train split,
scientific claim-evidence pairs, PubMed abstract retrieval data, biomedical
entailment or scientific NLI data, and citation-sentence to cited-abstract
supervision. Training should include hard negatives that share terminology but
do not verify the claim.

Training should exclude SciFact dev/test, BEIR, NanoBEIR, or translated records
likely to overlap with these evaluation claims or evidence abstracts.

### Synthetic Data Guidance

For document-to-query generation, use non-evaluation biomedical abstracts and
generate Arabic atomic scientific claims supported or refuted by the abstract.
Claims should include interventions, populations, outcomes, quantities,
biological mechanisms, and direction of effect.

For joint generation, create Arabic scientific abstracts with explicit methods
and results, then generate claims and evidence labels. Positives should contain
enough evidence to verify the claim; related-topic abstracts should be used as
hard negatives, not positives.

## Example Data

| Query | Positive document |
| --- | --- |
| Ly49Q يدير تنظيم هجرة الخلايا المتعادلة إلى مواقع الالتهاب من خلال تنظيم وظائف الأجزاء الغشائية. (96 chars) | تتحرك الخلايا المتعادلة بسرعة وتتقطب نحو مواقع العدوى والالتهاب. هنا، نوضح أن مستقبل MHC I المثبط، Ly49Q، كان حاسمًا في التقطيب السريع وتغزو الأنسجة للخلايا المتعادلة. خلال الحالة الطبيعية، يمنع Ly49Q التصاق الخلايا المتعادلة ... [truncated 225 chars](776 chars) |
| العلاج المضاد للفيروسات الراجعة يقلل من معدلات السل على نطاق واسع من مستويات CD4 (80 chars) | **الخلفية:** فيروس نقص المناعة البشرية (HIV) هو أقوى عامل خطر لتطور السل، وقد ساهم في إعادة ظهوره، وخاصة في أفريقيا جنوب الصحراء. في عام 2010، كان هناك حوالي 1.1 مليون حالة جديدة من السل بين 34 مليون شخص يعيشون مع فيروس نقص ا ... [truncated 225 chars](1950 chars) |
| زيادة سريعة في تنظيم الجينات المستحثة بالإنترفيرون وتعبيرها الأساسي الأعلى تقلل من بقاء عصبونات الخلايا الحبيبية المصابة بفيروس النيل الغربي. (141 chars) | على الرغم من أن عرض الخلايا العصبية في الدماغ للإصابة بالعدوى الميكروبية هو عامل رئيسي في تحديد النتائج السريرية، إلا أن القليل ما يُعرف عن العوامل الجزيئية التي تحكم هذه الحساسية. في هذا البحث، نظهر أن نوعين من الخلايا العصب ... [truncated 225 chars](1084 chars) |
| الفحص الأولي لسرطان عنق الرحم باستخدام كشف فيروس الورم الحليمي البشري يوفر حساسية أعلى على المدى الطويل من الفحص الخلوي التقليدي لكشف عن التغيرات الخلوية السابقة للسرطانية من الدرجة الثانية. (190 chars) | الخلفية: فحص سرطان عنق الرحم بناءً على اختبار فيروس الورم الحليمي البشري (HPV) يزيد من حساسية الكشف عن الأورام داخل الرحم السليفية من الدرجة العالية (الدرجة 2 أو 3)، ولكن ما إذا كان هذا الزيادة يمثل تشخيصًا زائدًا أو حماية ضد ... [truncated 225 chars](2088 chars) |
| منع التفاعل بين بروتين TDP-43 ومجموعة البروتينات التنفسية الأولى ND3 وND6 يؤدي إلى زيادة فقدان العصبونات الناتج عن TDP-43. (122 chars) | تسبب الطفرات الوراثية في بروتين ربط الحمض النووي TAR 43 (TARDBP، المعروف أيضًا باسم TDP-43) مرض التصلب الجانبي الأميوتروفي (ALS)، وزيادة وجود TDP-43 (المشفر بواسطة TARDBP) في السيتوبلازم هي سمة بارزة في علم الأمراض النسيجي لل ... [truncated 225 chars](1116 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-ar |
| Task / split | NanoSciFact |
| Hugging Face dataset | [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar) |
| Language | ar |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,919 |
| Positive qrels | 56 |
| Avg positives / query | 1.12 |
| Positives per query (min / median / max) | 1 / 1.00 / 4 |
| Queries with multiple positives | 4 (8.0%) |
| BM25 nDCG@10 | 0.5794 |
| BM25 hit@10 | 0.7800 |
| Query length avg chars | 88.96 |
| Document length avg chars | 1,316.81 |

### Public Sources

- [Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974); 2020; David Wadden, Shanchuan Lin, Kyle Lo, Lucy Lu Wang, Madeleine van Zuylen, Arman Cohan, Hannaneh Hajishirzi; DOI: `10.48550/arXiv.2004.14974`.
- [SciFact GitHub repository](https://github.com/allenai/scifact).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025; Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Marton Kardos, Ashwin Mathur, and others; DOI: `10.48550/arXiv.2502.13595`.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Fact or Fiction: Verifying Scientific Claims | 2020 | task paper | https://arxiv.org/abs/2004.14974 |
| SciFact GitHub repository |  | project repository | https://github.com/allenai/scifact |
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
  backing_dataset: NanoBEIR-ar
  dataset_id: hakari-bench/NanoBEIR-ar
  task_name: NanoSciFact
  split_name: NanoSciFact
  language: ar
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ar__NanoSciFact.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 2919
    positive_qrels: 56
  positives_per_query:
    average: 1.12
    min: 1
    median: 1.0
    max: 4
    multi_positive_queries: 4
    multi_positive_query_percent: 8.0
  text_stats_chars:
    query_mean: 88.96
    document_mean: 1316.81295
  bm25:
    ndcg_at_10: 0.5793704005
    hit_at_10: 0.78
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: MNanoBEIR Arabic NanoBEIR task split from hakari-bench/NanoBEIR-ar
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding SciFact, BEIR, or NanoBEIR records likely to overlap with these evaluation claims or evidence abstracts
    useful_training_data:
      - non-overlapping SciFact train split
      - Arabic or multilingual scientific claim-evidence pairs
      - biomedical abstract retrieval data
      - citation-sentence to cited-abstract supervision
    synthetic_data:
      document_generation: Arabic scientific abstracts with methods, results, quantities, and outcomes
      question_generation: Arabic atomic scientific claims supported or refuted by one abstract
      answerability: positives should contain evidence needed to verify the claim, not just share terminology
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar
    source_urls:
      - label: SciFact paper
        url: https://arxiv.org/abs/2004.14974
      - label: SciFact GitHub repository
        url: https://github.com/allenai/scifact
      - label: BEIR paper
        url: https://arxiv.org/abs/2104.08663
      - label: MMTEB paper
        url: https://arxiv.org/abs/2502.13595
      - label: Zeta Alpha NanoBEIR collection
        url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes:
      - Arabic task is a multilingual NanoBEIR adaptation of the original English BEIR task
  references:
    - title: "Fact or Fiction: Verifying Scientific Claims"
      url: https://arxiv.org/abs/2004.14974
      year: 2020
      doi: 10.48550/arXiv.2004.14974
      is_paper: true
      source_confidence: definitive_paper_link
    - title: SciFact GitHub repository
      url: https://github.com/allenai/scifact
      year: null
      doi: null
      is_paper: false
      source_confidence: definitive_project_page
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
