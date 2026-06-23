# MNanoBEIR / NanoBEIR-ar / NanoSciFact

## Overview

NanoBEIR-ar / NanoSciFact is the Arabic NanoBEIR version of SciFact, the
scientific claim verification dataset introduced in
[Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974).
Each query is an Arabic translated atomic scientific claim, and the retrieval
target is an Arabic translated scientific abstract containing evidence that can
support or refute the claim. The Nano task contains 50 claims, 2,919 abstracts,
and 56 positive qrels. Most claims have one positive abstract, with only a small
multi-positive tail. The task tests claim-sensitive scientific evidence
retrieval: a relevant abstract must verify the claim, not simply share a gene,
disease, intervention, or biological-process term.

## Details

### What the Original Data Measures

SciFact was built to verify expert-written scientific claims against research
abstracts. The original task includes claim labels and rationale sentences, but
in retrieval evaluation the first requirement is to find the evidence abstract.
This makes the task different from SCIDOCS: SCIDOCS asks for related papers,
while SciFact asks for an abstract that can verify a specific claim.

The Arabic NanoBEIR version keeps this claim-to-evidence retrieval objective in
translated form. The retriever must preserve scientific terminology while also
matching the direction and content of the claim: population, intervention,
mechanism, outcome, quantity, or biological relation.

### Observed Data Profile

The metadata records 50 queries, 2,919 documents, and 56 positive qrels.
Queries average 1.12 positives; only 4 queries have more than one positive.
Query text averages 88.96 characters, while documents average 1,316.81
characters. Examples include claims about Ly49Q and neutrophil migration,
antiretroviral therapy and tuberculosis, interferon-induced genes and West Nile
virus, HPV screening sensitivity, and TDP-43 interactions with mitochondrial
complex proteins.

The documents are long scientific abstracts with methods, results, biomedical
entities, and measured outcomes. This means a model must retrieve an evidence
document that addresses the claim's specific scientific assertion, not merely a
document in the same biomedical area.

### BM25 Evaluation Profile

The BM25 candidate subset reaches nDCG@10 = 0.5755, hit@10 = 0.7600, and
Recall@100 = 0.9464. BM25 is strong because scientific claims often include
distinctive terms: genes, diseases, interventions, cell types, proteins,
biological mechanisms, and measurement phrases. Exact terminology is crucial in
this task and often recovers the right evidence neighborhood.

BM25's limitation is claim verification. A document can contain the same gene
or disease term but not the claim's direction, outcome, population, or causal
relation. Sparse matching can therefore retrieve scientific neighbors that are
not evidence for the claim. It is a strong first-stage anchor but still needs
semantic evidence matching.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` reaches nDCG@10 =
0.5807, hit@10 = 0.7200, and Recall@100 = 0.8571. Dense retrieval slightly
improves nDCG@10 over BM25 but loses hit@10 and Recall@100. This suggests that
embedding similarity can help order some evidence abstracts but can also lose
rare scientific anchors.

Dense retrieval is useful when the abstract phrases the claim differently, but
it must not smooth away names of genes, proteins, interventions, or outcomes.
Scientific claim retrieval is detail-sensitive: a semantically close abstract
can still be wrong if it studies a different mechanism or direction of effect.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset reaches nDCG@10 = 0.6340, hit@10 =
0.8000, and Recall@100 = 0.9643. It is the strongest candidate view on all
visible aggregate metrics. The metadata records 2 rows with the optional
rank-101 safeguard, indicating that a small number of positives needed explicit
preservation near the candidate boundary.

For reranker experiments, hybrid is the best pool because it combines BM25's
scientific term preservation with dense retrieval's claim-to-evidence semantic
matching. The reranker can then distinguish true verifying evidence from
same-topic scientific distractors.

### Metric Interpretation for Model Researchers

NanoSciFact-ar shows why scientific retrieval needs both lexical precision and
semantic relation matching. BM25 has strong coverage because exact terms are
important. Dense can improve local ordering but loses some coverage. Hybrid
improves nDCG@10, hit@10, and Recall@100, showing that the two retrieval
families recover complementary evidence.

Because most queries have one positive, top-rank mistakes matter. Researchers
should inspect whether failures are caused by missing a rare entity, confusing
direction of effect, retrieving a related but non-verifying abstract, or
ranking a review-like neighbor above the evidence abstract.

### Query and Relevance Type Tendencies

Queries are Arabic scientific claims, often biomedical. They include genes,
proteins, diseases, interventions, populations, mechanisms, outcomes, and
comparative or causal statements. Relevant documents are abstracts that contain
the evidence needed to support or refute the claim.

Lexical-heavy cases involve rare biomedical entities and exact intervention
names. Dense-heavy cases involve claims whose evidence is phrased through
methods, results, or experimental descriptions rather than the same surface
sentence. Hybrid retrieval is strongest when both exact terminology and
relation semantics matter.

### Representative Failure Modes

BM25 can retrieve abstracts that mention the same scientific term but study a
different outcome, mechanism, or population. Dense retrieval can retrieve a
biomedically related abstract while missing the exact gene, protein, or
intervention. Both can fail on directionality: an abstract may support the
opposite claim or contain a related negative result. Good hard negatives share
scientific vocabulary but do not verify the claim.

### Arabic-Specific Notes

Arabic SciFact retrieval mixes translated scientific prose, biomedical terms,
Latin gene/protein symbols, disease names, quantitative expressions, and
abstract structure. Sparse retrieval needs to preserve technical symbols and
names. Dense retrieval needs scientific Arabic or multilingual biomedical
coverage. Translation artifacts can affect terminology, especially for cell
types, interventions, protein names, and methodological phrases.

### Training and Leakage Notes

Training should exclude SciFact, BEIR, or NanoBEIR records likely to overlap
with these evaluation claims or evidence abstracts. Useful non-overlapping data
includes SciFact train examples, Arabic or multilingual scientific
claim-evidence pairs, biomedical abstract retrieval, citation-sentence to
cited-abstract supervision, and scientific NLI or entailment-style data.

### Model Improvement Hints

The main improvement target is evidence-aware scientific matching. First-stage
retrievers should preserve exact scientific entities while using semantic
matching to identify abstracts that verify the claim. Rerankers should compare
same-term abstracts with different outcomes or directions of effect. Training
should emphasize hard negatives that share terminology but lack verification
evidence.

### Training Data That May Help

Useful training data includes non-overlapping SciFact claims, biomedical
claim-evidence pairs, PubMed abstract retrieval, citation-sentence retrieval,
scientific entailment data, and multilingual biomedical QA evidence pairs.

### Synthetic Data Guidance

Generate Arabic scientific abstracts with explicit methods, results,
quantities, interventions, populations, mechanisms, and outcomes. Then generate
atomic scientific claims supported or refuted by those abstracts. Positives
should contain evidence needed to verify the claim; related-topic abstracts
should be used as hard negatives, not positives.

## Example Data

| Query | Positive document |
| --- | --- |
| Ly49Q يدير تنظيم هجرة الخلايا المتعادلة إلى مواقع الالتهاب من خلال تنظيم وظائف الأجزاء الغشائية. [96 chars] | تتحرك الخلايا المتعادلة بسرعة وتتقطب نحو مواقع العدوى والالتهاب. هنا، نوضح أن مستقبل MHC I المثبط، Ly49Q، كان حاسمًا في التقطيب السريع وتغزو الأنسجة للخلايا المتعادلة. خلال الحالة الطبيعية، يمنع Ly49Q التصاق الخلايا المتعادلة من خلال منع تكوين مركبات التركيز، ومن المحتمل أن يكون ذلك من خلال تثبيط كينازات Src وPI3. ومع ذلك، في وجود محفزات الالتهاب، وسّط Ly49Q التقطيب السريع وتغزو الأنسجة للخلايا المتعادلة بطريقة تعتمد على مجال ITIM. تظهر هذه الوظائف المعاكسة أنها وسّطت بواسطة استخدام مميز للفوسفاتاز الفعال SHP-1 وSHP-2. تأثرت التقطيب والهجرة التي تعتمد على Ly49Q بتحكم Ly49Q في وظائف الجزر الغشائية. نقدم أن Ly49Q هو حاسم في تحويل الخلايا المتعادلة إلى شكلها المتقطب والهجرة السريعة عند الالتهاب، من خلال تنظيمه المكاني-الزمني للجزر الغشائية وجزيئات الإشارة المرتبطة بها. [776 chars] |
| العلاج المضاد للفيروسات الراجعة يقلل من معدلات السل على نطاق واسع من مستويات CD4 [80 chars] | **الخلفية:** فيروس نقص المناعة البشرية (HIV) هو أقوى عامل خطر لتطور السل، وقد ساهم في إعادة ظهوره، وخاصة في أفريقيا جنوب الصحراء. في عام 2010، كان هناك حوالي 1.1 مليون حالة جديدة من السل بين 34 مليون شخص يعيشون مع فيروس نقص المناعة البشرية في جميع أنحاء العالم. العلاج المضاد للفيروسات الراجعة له القدرة الكبيرة على منع السل المرتبط بفيروس نقص المناعة البشرية. أجرينا مراجعة منهجية للدراسات التي تحليلت تأثير العلاج المضاد للفيروسات الراجعة على انتشار السل لدى البالغين المصابين بفيروس نقص المناعة البشرية. **الطرق والأبحاث:** تم البحث في PubMed، Embase، African Index Medicus، LILACS، وسجلات التجارب السريرية بشكل منهجي. تم تضمين التجارب السريرية العشوائية، الدراسات التسلسلية المستقبلية، والدراسات التسلسلية التاريخية إذا قارنت انتشار السل حسب حالة العلاج المضاد للفيروسات الراجعة لدى البالغين المصابين بفيروس نقص المناعة البشرية لمدة متوسطة تزيد عن 6 أشهر في الدول النامية. تم تقسيم التحليلات الإحصائية إلى أربع فئات بناءً على عدد خلايا CD4 عند بدء العلاج المضاد للفيروسات الراجعة: (1) أقل من 200... [1,000 / 1,950 chars] |
| زيادة سريعة في تنظيم الجينات المستحثة بالإنترفيرون وتعبيرها الأساسي الأعلى تقلل من بقاء عصبونات الخلايا الحبيبية المصابة بفيروس النيل الغربي. [141 chars] | على الرغم من أن عرض الخلايا العصبية في الدماغ للإصابة بالعدوى الميكروبية هو عامل رئيسي في تحديد النتائج السريرية، إلا أن القليل ما يُعرف عن العوامل الجزيئية التي تحكم هذه الحساسية. في هذا البحث، نظهر أن نوعين من الخلايا العصبية من مناطق مختلفة في الدماغ أظهرت اختلافًا في السماح بتكاثر عدة فيروسات إيجابية السلسلة من الرنا. الخلايا العصبية الحبيبية في الدماغ الصغير والخلايا العصبية القشرية في القشرة الدماغية تمتلك برامج مناعية فطرية فريدة تمنحها حساسية متفاوتة للإصابة الفيروسية خارج الجسم وفي الجسم الحي. من خلال إدخال الجينات التي تم تعبيرها بشكل أعلى في الخلايا العصبية الحبيبية إلى الخلايا العصبية القشرية، تم تحديد ثلاثة جينات محفزة بالإنترفيرون (ISGs؛ Ifi27، Irg1 وRsad2 (المعروفة أيضًا باسم Viperin)) التي وسعت التأثيرات المضادة للفيروسات ضد مختلف الفيروسات العصبية. بالإضافة إلى ذلك، وجدنا أن الحالة الجينية والميكرو رنا (miRNA)-المتوسطة لتنظيم ISGs تتوافق مع الاستجابة المضادة للفيروسات المحسنة في الخلايا العصبية الحبيبية. لذا، الخلايا العصبية من مناطق الدماغ المختلفة من الناحية التطورية... [1,000 / 1,084 chars] |

### Public Sources

- [Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974), 2020.
- [SciFact GitHub repository](https://github.com/allenai/scifact).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595), 2025.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Fact or Fiction: Verifying Scientific Claims | 2020 | task paper | [https://arxiv.org/abs/2004.14974](https://arxiv.org/abs/2004.14974) |
| SciFact GitHub repository |  | project repository | [https://github.com/allenai/scifact](https://github.com/allenai/scifact) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
