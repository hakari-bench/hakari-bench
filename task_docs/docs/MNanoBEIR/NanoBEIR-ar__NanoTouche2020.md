# MNanoBEIR / NanoBEIR-ar / NanoTouche2020

## Overview

NanoBEIR-ar / NanoTouche2020 is the Arabic NanoBEIR version of Touché 2020
argument retrieval. Touché 2020, described in
[Overview of Touché 2020: Argument
Retrieval](https://doi.org/10.1007/978-3-030-58219-7_26), asks systems to
retrieve relevant arguments for controversial topics from debate-style
documents. This Nano task contains 49 Arabic translated controversial
questions, 5,745 Arabic translated argument documents, and 932 positive qrels.
Every query is multi-positive, with an average of 19.02 relevant arguments. The
task is therefore about debate-topic coverage and useful argument ranking, not
finding a single answer. BM25 and `reranking_hybrid` are strongest near the
top, while hybrid has the best hit@10 and Recall@100.

## Details

### What the Original Data Measures

Touché 2020 focuses on argument retrieval: given a socially important
controversial question, retrieve arguments that are relevant and useful for
debate. The corpus is based on debate-portal material, so documents often
contain claims, premises, evidence, rebuttals, citations, and informal
argumentation. Relevance is broader than answerability. A positive document is
a substantive argument that addresses the topic.

The Arabic NanoBEIR version keeps this task shape through translation. Unlike
ArguAna, it does not ask for one best counterargument to a query argument.
Instead, a short controversial question can have many relevant pro and con
arguments. The retriever should surface a useful set of arguments.

### Observed Data Profile

The metadata records 49 queries, 5,745 documents, and 932 positive qrels. Every
query has multiple positives. The average is 19.02 positives per query, the
median is 19, and the range is 6 to 32. Queries average 40.73 characters, while
documents are long, averaging 1,803.56 characters. Examples include homework,
direct-to-consumer prescription drug advertising, childhood vaccination,
abortion legality, standardized testing, minimum wage, the penny, corporate
taxes, golf, and net neutrality.

This shape means that a high hit@10 is not enough. Many systems can find at
least one relevant argument, but the harder objective is to rank a diverse and
substantive set of arguments near the top.

### BM25 Evaluation Profile

The BM25 candidate subset reaches nDCG@10 = 0.5263, hit@10 = 0.9388, and
Recall@100 = 0.7232. BM25 is strong because controversial questions contain
visible topic words that recur in debate documents: homework, vaccination,
abortion, drug advertising, standardized tests, taxes, or net neutrality.
Sparse overlap is often enough to find the debate neighborhood.

BM25's limitation is argument quality and coverage. Long debate documents may
repeat the topic without providing a strong argument, or may address only one
side of a multi-sided issue. Sparse retrieval can over-rank documents that
share obvious topic terms while missing more substantive arguments with
different phrasing.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` reaches nDCG@10 =
0.4155, hit@10 = 0.9388, and Recall@100 = 0.7253. Dense retrieval ties BM25 on
hit@10 and slightly improves Recall@100, but it is weaker on nDCG@10. This
suggests that dense semantic similarity can find additional topic-relevant
arguments, but the top ordering is less aligned with the judged argument
quality or relevance than BM25 in this Arabic translated sample.

Dense retrieval may also blur stance and argument role. A semantically related
document may discuss the same controversy but not present a useful argument for
the query. For debate retrieval, broad semantic relatedness is insufficient.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset reaches nDCG@10 = 0.5262, hit@10 =
0.9796, and Recall@100 = 0.7758. It nearly matches BM25's nDCG@10 while
improving hit@10 and Recall@100. The candidate count is exactly 100 per query,
with no rank-101 safeguard rows, so the coverage gain comes from the hybrid
candidate composition rather than extra positive insertion.

For reranker experiments, hybrid is the best candidate pool. It preserves
BM25's topic anchors and adds dense candidates that may capture arguments using
different wording. The reranker can then focus on argument usefulness,
specificity, and stance diversity.

### Metric Interpretation for Model Researchers

NanoTouche2020-ar is highly multi-positive. hit@10 is easy to satisfy compared
with single-positive tasks because every topic has many relevant arguments.
nDCG@10 and Recall@100 are more informative: they show whether a model ranks
strong arguments early and covers a broad argument set. BM25 is a strong sparse
baseline for top ordering, dense contributes slightly to coverage, and hybrid
is the best candidate source overall.

Researchers should inspect whether models return diverse arguments or simply
many near-duplicates from the same stance. In argument retrieval, breadth and
substantive relevance matter.

### Query and Relevance Type Tendencies

Queries are short Arabic controversial questions. Relevant documents are long
arguments, often pro or con, with premises, examples, citations, or rebuttal
structure. A positive document should address the controversy with a substantive
argument, not merely mention the topic.

Lexical-heavy cases include topics with clear nouns and policy terms. Dense
cases include arguments that use different framing, such as harms, rights,
costs, incentives, or social consequences. Hybrid retrieval is useful when a
topic term anchors the search but useful arguments are phrased in varied ways.

### Representative Failure Modes

BM25 can retrieve long documents that repeat the topic but contain weak or
off-target argumentation. Dense retrieval can retrieve broadly related debate
text that does not answer the particular controversial question. Both can
over-concentrate on one stance and miss relevant arguments from the other side.
Multi-positive failures often appear as poor diversity: a model finds several
similar arguments but misses other judged positives.

Good hard negatives include same-topic low-quality debate text, arguments about
a nearby controversy, and documents that share policy vocabulary but do not
address the query.

### Arabic-Specific Notes

Arabic argument retrieval must handle translated debate style, long documents,
informal phrasing, lists, citations, stance markers, and policy vocabulary.
Sparse retrieval benefits from preserving topic terms. Dense retrieval needs to
recognize argument framing and stance while avoiding overly broad topical
matching. Long-document handling matters because the useful argument may be
inside a large translated passage.

### Training and Leakage Notes

Training should exclude Touché, args.me, BEIR, or NanoBEIR records likely to
overlap with these evaluation topics or debate documents. Useful
non-overlapping data includes debate-portal argument relevance data, Arabic or
multilingual query-to-argument supervision, stance-labeled arguments, and
multi-positive argument retrieval judgments.

### Model Improvement Hints

The main improvement target is multi-positive argument ranking. First-stage
retrievers should recover the debate neighborhood while avoiding weak
topic-only matches. Rerankers should learn argument relevance, stance, and
substantive usefulness. Listwise or diversity-aware training can help because
each topic has many positives.

### Training Data That May Help

Useful training data includes non-overlapping debate-portal arguments,
query-to-argument relevance labels, stance classification data, argument
quality annotations, pro/con argument pairs, and synthetic controversial-topic
clusters with several relevant arguments.

### Synthetic Data Guidance

Generate Arabic debate arguments with claims, premises, evidence, rebuttals,
and informal style. Then generate short controversial questions that those
arguments address. Include multiple pro and con positives per topic, plus
same-topic weak or off-target negatives. Positives should be substantive
arguments relevant to the topic, not merely long documents sharing keywords.

## Example Data

| Query | Positive document |
| --- | --- |
| هل الواجبات المدرسية مفيدة؟ (27 chars) | أولاً، هناك ثلاثة حجج تدعم أهمية الواجبات المنزلية في المدارس الحديثة. 1. الواجبات المنزلية تساعد المتعلمين الذين يتعلمون من خلال الفعل. هناك ثلاثة أنواع من المتعلمين: الذين يتعلمون من خلال السمع، والذين يتعلمون من خلال الرؤي ... [truncated 225 chars](3157 chars) |
| هل يجب أن تُعلن الأدوية الموصوفة مباشرة للأفراد؟ (48 chars) | كثير من الإعلانات لا تحتوي على معلومات كافية حول فعالية الأدوية. على سبيل المثال، يتم الإعلان عن الدواء "لونستا" عبر فراشة تطير عبر نافذة غرفة نوم فوق شخص نائم بسلام. في الواقع، يساعد "لونستا" المرضى على النوم 15 دقيقة أسرع ب ... [truncated 225 chars](1033 chars) |
| هل يجب تطعيم الأطفال؟ (21 chars) | ليس هناك قضية كاملة بعد... مجرد بعض النقاط التي جمعتها... لا يجب أن يكون للحكومة الحق في التدخل في قرارات الصحة التي يتخذها الآباء لأطفالهم. وفقًا لاستطلاع أجرته جامعة ميشيغان في عام 2010، يعتقد 31% من الآباء أنهم يجب أن يكون ... [truncated 225 chars](3842 chars) |
| هل يجب أن تكون الإجهاض قانونيًا؟ (32 chars) | يجب أن تكون الإجهاض قانونيًا، حيث تبدأ الشخصية بعد أن يصبح الجنين قادرًا على الحياة أو بعد الولادة، وليس عند الحمل. وفقًا لمحكمة العدل العليا الأمريكية، يبدأ الشخص في الحصول على عمره بعد الولادة عندما يبدأ في التنفس، بدءًا من ... [truncated 225 chars](261 chars) |
| هل اختبارات القياس الموحد تحسن من جودة التعليم؟ (47 chars) | القرار: اختبارات SAT وACT وغيرها من الاختبارات المعيارية توفر رؤى أكبر حول استعداد طالب المدرسة الثانوية للتعليم في الكليات والجامعات النخبة مقارنة بمعدل التخرج من المدرسة الثانوية، وبالتالي يجب أن تلعب دورًا أكبر في عملية ال ... [truncated 225 chars](3549 chars) |

### Public Sources

- [Overview of Touché 2020: Argument Retrieval](https://doi.org/10.1007/978-3-030-58219-7_26), 2020.
- [Open PDF: Overview of Touché 2020: Argument Retrieval](https://downloads.webis.de/touche/publications/papers/bondarenko_2020d.pdf).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595), 2025.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of Touché 2020: Argument Retrieval | 2020 | task paper | https://doi.org/10.1007/978-3-030-58219-7_26 |
| Open PDF: Overview of Touché 2020: Argument Retrieval | 2020 | paper PDF | https://downloads.webis.de/touche/publications/papers/bondarenko_2020d.pdf |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
