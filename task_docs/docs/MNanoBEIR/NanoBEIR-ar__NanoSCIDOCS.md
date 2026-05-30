# MNanoBEIR / NanoBEIR-ar / NanoSCIDOCS

## Overview

NanoBEIR-ar / NanoSCIDOCS is the Arabic NanoBEIR version of SCIDOCS, the
scientific document evaluation suite introduced with
[SPECTER: Document-level Representation Learning using Citation-informed
Transformers](https://arxiv.org/abs/2004.07180). Each query is an Arabic
translated scientific paper title, and the retrieval target is a set of Arabic
translated related scientific documents. The Nano task contains 50 queries,
2,210 documents, and 244 positive qrels. Every query is multi-positive, with
roughly five related papers per query. This is not answer-passage retrieval:
the task measures scholarly relatedness, citation-like neighborhood, method
similarity, and related-paper recommendation. Dense retrieval and
`reranking_hybrid` both outperform BM25, reflecting the importance of semantic
scientific similarity beyond keyword overlap.

## Details

### What the Original Data Measures

SCIDOCS evaluates scientific document representations using signals such as
citation relationships, co-citation, recommendation, and classification. In
the BEIR retrieval framing, a query paper should retrieve related scientific
papers. Relevance is therefore document-level scholarly relatedness, not a
short factual answer and not duplicate-title matching.

The Arabic NanoBEIR version keeps this objective in translated form. A query
title may name a method, task, dataset, device, or research problem, and
positives may be related through methodology, application area, citation
context, or scientific contribution. This makes the task useful for evaluating
retrievers on research-paper similarity.

### Observed Data Profile

The metadata records 50 queries, 2,210 documents, and 244 positive qrels. Every
query has multiple positives: the average is 4.88, the median is 5, and the
range is 3 to 5. Query titles average 64.96 characters, while document records
average 823.44 characters. Examples include titles about DC-DC converters,
Gaussian Markov random fields, neural texture generation, RFID receivers, and
heart-rate monitoring devices.

The retrieval unit is usually a title or title-plus-abstract-like scientific
record. A positive paper may not repeat the exact query title terms, but it
should belong to the same research neighborhood. This differs sharply from
MS MARCO or NQ, where relevance is answerability.

### BM25 Evaluation Profile

The BM25 candidate subset reaches nDCG@10 = 0.2488, hit@10 = 0.6800, and
Recall@100 = 0.5574. BM25 can recover related papers when a query title
contains distinctive method names, devices, datasets, technical acronyms, or
domain terms that also appear in related abstracts. It is a useful anchor for
technical vocabulary.

BM25's limitation is that scientific relatedness often crosses surface wording.
Two papers may be related by method, task, citation context, or application
area without sharing many exact terms. Sparse retrieval can also over-rank
papers that share technical words but differ in contribution. This explains the
relatively low nDCG@10 and moderate Recall@100.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` reaches nDCG@10 =
0.2996, hit@10 = 0.7600, and Recall@100 = 0.6107. Dense retrieval improves over
BM25 on all visible metrics, which is expected for scientific related-paper
retrieval. Embedding similarity can connect method-level, task-level, and
topic-level relationships even when title terms do not exactly match.

Dense retrieval's risk is broad topical drift. It may retrieve papers in the
same field that are not close enough as related work, or papers that share a
method family but address a different problem. Scientific retrieval requires
semantic similarity that is fine-grained enough to respect contribution and
context.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset reaches nDCG@10 = 0.2939, hit@10 =
0.8000, and Recall@100 = 0.6393. Hybrid has the best hit@10 and Recall@100,
while dense has slightly higher nDCG@10. The metadata records one row with the
optional rank-101 safeguard. The pattern suggests that dense retrieval is a
strong top sorter, while hybrid is a safer candidate source for covering more
related papers.

For reranker experiments, hybrid is useful because it includes exact technical
term matches and semantic related-work candidates. The reranker can then judge
which papers are truly related, rather than merely sharing vocabulary.

### Metric Interpretation for Model Researchers

SCIDOCS-ar should be interpreted as multi-positive scientific relatedness
retrieval. Hit@10 indicates whether at least one related paper appears near the
top, but it does not measure whether the related-paper set is well covered.
Recall@100 is important because each query has several positives. Dense
retrieval improves top-rank quality, and hybrid improves coverage. A strong
scientific retriever should do both: rank close related work high and recover
the broader neighborhood.

Models trained only on QA or duplicate-question data may underperform because
SCIDOCS relevance is not answer equivalence. It is scholarly relatedness.

### Query and Relevance Type Tendencies

Queries are Arabic translated scientific titles. They often mention methods,
devices, datasets, models, domains, or applications. Relevant documents are
scientific abstracts or title-abstract records related by citation-like
context, shared contribution, method, domain, or recommendation signal.

Lexical-heavy cases include distinctive acronyms and method names. Dense-heavy
cases include related papers that use different terminology for the same
scientific problem. Hybrid retrieval is strongest when exact technical terms
and broader method similarity both matter.

### Representative Failure Modes

BM25 can retrieve papers that share a technical phrase but are not truly
related in contribution or citation context. Dense retrieval can retrieve papers
from the same broad field while missing the specific method, dataset, or
application focus. Multi-positive failures occur when the model finds one
related paper but misses the rest of the related-work cluster.

Good hard negatives are papers from the same field with different methods,
papers sharing acronyms but not contribution, and nearby abstracts that are
topically similar but not recommendation-equivalent.

### Arabic-Specific Notes

The metadata language is marked multilingual, and the task is the Arabic
MNanoBEIR adaptation. The text can include Arabic translated scientific
phrasing, English acronyms, method names, dataset names, and technical symbols.
Sparse retrieval needs to preserve acronyms and technical terms. Dense
retrieval needs scientific-domain representations that understand title and
abstract semantics across translation. Translation artifacts can be especially
harmful for method names and domain-specific phrases.

### Training and Leakage Notes

Training should exclude SCIDOCS, BEIR, or NanoBEIR records likely to overlap
with these evaluation papers or related-paper labels. Useful non-overlapping
data includes scientific citation pairs, co-citation and related-paper
recommendation data, scientific title/abstract retrieval triples, and
multilingual scientific document retrieval pairs. Multi-positive training is
appropriate because every query has several related papers.

### Model Improvement Hints

The main improvement target is fine-grained scientific relatedness. First-stage
retrievers should preserve technical vocabulary while using dense similarity to
recover method and contribution neighbors. Rerankers should compare papers that
share a topic but differ in method, dataset, or scientific contribution. Models
should be evaluated for related-set coverage, not just the first positive.

### Training Data That May Help

Useful training data includes non-overlapping citation pairs, co-citation
graphs, related-paper recommendation logs, Semantic Scholar-style title/abstract
triples, multilingual scientific abstracts, and hard negatives from the same
research field.

### Synthetic Data Guidance

Generate Arabic scientific abstracts with method, task, dataset, contribution,
application, and result details. Create clusters of related paper titles and
abstracts around the same scientific problem. Positives should be scholarly
related papers; hard negatives should share keywords but differ in contribution
or citation context.

## Example Data

| Query | Positive document |
| --- | --- |
| محول رفع الجهد متعدد المستويات DC إلى DC جديد (45 chars) | محولات مصدر الجهد المتعددة المستويات تظهر كخيار جديد من محولات الطاقة لتطبيقات الطاقة العالية. تولد محولات مصدر الجهد المتعددة المستويات عادةً موجة جهد الدرجات من عدة مستويات من جهد مكثفات التيار المستمر. واحدة من أكبر القيود ... [truncated 225 chars](794 chars) |
| تعلم الحقول العشوائية الغاوسية الماركوفية النادرة بسرعة بناءً على تحليل تشولسكي (79 chars) | Sure, please provide the English document that you need translated into Arabic. (79 chars) |
| توليد النسيج باستخدام الشبكات العصبية التقويمية (47 chars) | في هذا العمل، ندرس تأثير عمق الشبكات التلافيفية على دقتها في التعرف على الصور على نطاق واسع. المساهمة الرئيسية لدينا هي تقييم شامل لشبكات ذات عمق متزايد، والذي يظهر أن تحسينًا كبيرًا على التكوينات السابقة يمكن تحقيقه من خلال ... [truncated 225 chars](644 chars) |
| مستقبِل دائري دائري عريض النطاق مسطح بقطبية دائرية لنظام RFID (61 chars) | في هذا البحث، يتم اقتراح تقنية تغذية شريط متعرج أفقيًا (HMS) لتحقيق مطابقة مقاومة جيدة وأنماط إشعاع جانبي متماثل لمستقبلات رقمية دائرية الطور ذات طبقة مزدوجة، وهي مناسبة لتطبيقات التعرف على الراديو الترددي (RFID) في نطاق التر ... [truncated 225 chars](1081 chars) |
| تطوير جهاز مراقبة نبضات القلب الرقمي المتقدم من خلال استخدام مكونات إلكترونية أساسية (84 chars) | في هذا الورقة، قدمنا تصميم وتطوير جهاز متكامل جديد لقياس معدل ضربات القلب باستخدام الإصبع لتحسين تقدير معدل ضربات القلب. مع زيادة الأمراض المتعلقة بالقلب يوميًا، أصبح هناك حاجة ملحة إلى جهاز قياس معدل ضربات القلب دقيق وميسور ... [truncated 225 chars](855 chars) |

### Public Sources

- [SPECTER: Document-level Representation Learning using Citation-informed Transformers](https://arxiv.org/abs/2004.07180), 2020.
- [SCIDOCS GitHub repository](https://github.com/allenai/scidocs).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595), 2025.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SPECTER: Document-level Representation Learning using Citation-informed Transformers | 2020 | task paper | https://arxiv.org/abs/2004.07180 |
| SCIDOCS GitHub repository |  | project repository | https://github.com/allenai/scidocs |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
