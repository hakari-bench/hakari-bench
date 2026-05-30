# MNanoBEIR / NanoBEIR-ar / NanoClimateFEVER

## Overview

NanoBEIR-ar / NanoClimateFEVER is the Arabic NanoBEIR version of
Climate-FEVER, a climate claim verification retrieval task introduced by
[CLIMATE-FEVER: A Dataset for Verification of Real-World Climate
Claims](https://arxiv.org/abs/2012.00614). Each query is an Arabic translated
climate-related claim, and the retrieval target is an Arabic translated
evidence passage that supports, refutes, or otherwise directly addresses the
claim. The Nano task contains 50 claims, 3,408 evidence candidates, and 148
positive qrels. Unlike single-answer entity retrieval, this task is strongly
multi-positive: most claims have several relevant evidence passages. The main
challenge is to retrieve evidence that addresses the specific climate claim,
including its quantities, time span, causal wording, or skeptical framing, not
merely passages that mention climate change in general.

## Details

### What the Original Data Measures

Climate-FEVER adapts FEVER-style claim verification to real-world climate
claims. The original dataset collects climate-related claims from public web
sources and annotates evidence passages as supporting, refuting, or not
providing enough information. This matters for retrieval because the query is a
declarative claim, not a keyword query. A relevant passage must help verify the
claim, and relevance may depend on numerical interpretation, temporal scope,
partial support, qualification, or contradiction.

The Arabic NanoBEIR version should be read as a compact translated
claim-to-evidence retrieval task. It does not ask the model to classify the
claim label directly. It asks whether the model can retrieve the evidence
needed by a downstream verifier. This is especially useful for testing whether
retrievers preserve scientific details while still matching paraphrased climate
claims across translation.

### Observed Data Profile

The metadata records 50 queries, 3,408 documents, and 148 positive qrels.
Queries average 2.96 positives, the median is 3, and 44 of 50 queries are
multi-positive. Query text averages 116.76 characters, while evidence documents
average 1,342.96 characters. The examples include claims about warming trends,
sea-level variation, Hurricane Harvey, solar cycles, CERN CLOUD, carbon
dioxide, Holocene warmth, and climate attribution.

This is a different retrieval shape from ArguAna. The query is shorter, but the
evidence document is much longer, and there are usually several acceptable
positive passages. A useful system should retrieve multiple evidence paths for
the same claim rather than only one topical hit. Long documents also mean that
matching one phrase is not enough; the relevant part may be embedded inside a
larger explanatory passage.

### BM25 Evaluation Profile

The BM25 candidate subset reaches nDCG@10 = 0.2400, hit@10 = 0.5800, and
Recall@100 = 0.5676. BM25 captures visible claim terms such as carbon dioxide,
solar cycles, sea level, hurricane names, greenhouse gases, temperature trends,
and named scientific projects. This lexical signal is important because many
climate claims contain exact entities, quantities, or technical phrases that
should not be smoothed away.

The sparse baseline is limited by evidence indirection. A claim can be answered
by a passage that does not repeat the claim wording, and a document can share
many climate terms without actually supporting or refuting the claim. BM25 also
struggles when translated Arabic terminology varies across the claim and the
evidence passage. It is a useful anchor for climate vocabulary, but it misses a
large fraction of judged positives by top 100.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` reaches nDCG@10 =
0.2899, hit@10 = 0.6600, and Recall@100 = 0.5946. Dense retrieval improves over
BM25 across the visible metrics, which suggests that embedding similarity helps
connect Arabic claim wording to evidence passages that use different
scientific or encyclopedic phrasing. This is expected for claim verification:
the evidence often explains a phenomenon rather than repeating the claim.

Dense retrieval still leaves substantial room for improvement. Climate claims
are detail-sensitive, and embedding similarity can retrieve a passage about the
same broad topic while missing the specific quantity, time frame, causal
relation, or attribution statement. Dense models can also over-rank generic
climate-change passages when the claim requires evidence about a narrower
scientific mechanism or named event.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset reaches nDCG@10 = 0.2948, hit@10 =
0.7200, and Recall@100 = 0.6486. It is the strongest of the three candidate
views on all visible aggregate metrics. The hybrid pool combines BM25's exact
climate terminology with dense retrieval's ability to match paraphrased or
indirect evidence. The metadata records 3 rows with the optional rank-101
safeguard, showing that a few positives still needed explicit preservation near
the candidate boundary.

For reranker evaluation, this is the most informative pool. It contains
lexical hits, semantically related passages, and climate-domain distractors.
The reranker must decide which candidates actually address the claim, rather
than merely share the same climate topic.

### Metric Interpretation for Model Researchers

This task shows a clear hybrid-search pattern. BM25 is useful but weakest
overall. Dense retrieval improves top-10 quality and top-100 coverage, showing
that semantic matching is important for translated claim evidence. Hybrid
retrieval improves again, which indicates that lexical and dense systems find
partly complementary positives. Because the task is multi-positive, Recall@100
should be read as evidence-pool coverage: a higher value means more judged
supporting/refuting evidence is available to a downstream verifier or reranker.

A first-stage retriever that improves only nDCG@10 may surface one good
evidence passage but still miss alternative evidence. A retriever that improves
Recall@100 is valuable for fact-checking pipelines because it gives the
verifier more ways to assess the claim. The strongest system should preserve
scientific terms and numbers while also matching paraphrased evidence.

### Query and Relevance Type Tendencies

Queries are Arabic declarative claims, often written in misinformation-like or
skeptical framing. They can mention time ranges, measurements, trends, named
institutions, weather events, greenhouse gases, solar activity, or climate
attribution. Relevant passages are long evidence documents that may support,
refute, or qualify the claim. They are not necessarily written as direct answers
to the claim.

Lexical-heavy cases involve named phenomena or exact scientific terms. Dense
retrieval is more important when the evidence uses explanatory language, when
the claim is indirectly addressed, or when translation changes the surface
form. Hybrid retrieval is strongest when both conditions hold: the system must
keep exact climate terms but still find evidence expressed in different words.

### Representative Failure Modes

BM25 can over-rank passages that mention the same climate entity but do not
verify the claim. For example, a passage about sea level may not address the
claim's local/regional variation, and a passage about greenhouse gases may not
settle the specific causal or temporal statement. Dense retrieval can over-rank
general climate passages that are semantically close but lack the exact
measurement, event, or causal relation. In both cases, the common failure is
topical relevance without verification relevance.

Hard negatives should therefore include same-topic climate passages that omit
the needed quantity, use a different time period, discuss a different
mechanism, or support a different claim about the same phenomenon.

### Arabic-Specific Notes

Arabic claim retrieval depends on scientific terminology, translated
encyclopedic style, number and unit handling, and normalization of names and
technical phrases. Sparse retrieval needs tokenization that preserves climate
terms and named projects while handling Arabic morphology and attached
particles. Dense retrieval needs enough Arabic scientific coverage to connect
claim-like wording with evidence-like explanation. Models should be careful not
to collapse distinct quantities, dates, or causal markers, because those small
details often determine whether a passage verifies the claim.

### Training and Leakage Notes

Training should exclude upstream Climate-FEVER development/test examples, BEIR
or NanoBEIR records that overlap with these claims or evidence passages, and
synthetic data generated from the evaluation evidence. Useful non-overlapping
data includes Climate-FEVER-style claim/evidence pairs, FEVER evidence
retrieval data, Arabic or multilingual scientific claim verification, and
climate-domain evidence retrieval. Reports should disclose whether the model
saw Climate-FEVER or related fact-checking datasets.

### Model Improvement Hints

The main improvement target is claim-sensitive evidence retrieval. First-stage
retrievers should preserve exact climate entities, numbers, and technical terms
while using dense similarity to find explanatory evidence. Rerankers should be
trained to distinguish passages that verify the specific claim from passages
that merely discuss the same climate topic. Multi-positive training is useful
because most queries have several relevant passages.

### Training Data That May Help

Useful training data includes non-overlapping Climate-FEVER claim-evidence
pairs, FEVER-style evidence retrieval, Arabic or multilingual scientific claim
verification data, climate-domain claim-to-evidence pairs, and hard negatives
from the same climate topic but different claim relation.

### Synthetic Data Guidance

Generate Arabic declarative climate claims from non-evaluation evidence
passages. Include quantities, time spans, causal statements, named institutions,
weather events, greenhouse gases, ice sheets, sea level, solar cycles, and
climate attribution. Positives should contain evidence addressing the claim;
hard negatives should share the climate topic but fail to support, refute, or
qualify the specific statement.

## Example Data

| Query | Positive document |
| --- | --- |
| من عام 1970 حتى عام 1998، كان هناك فترة تدفئة رفعت درجات الحرارة بمقدار 0.39 درجة مئوية، وأدت إلى نشأة حركة التحرش بشأن الاحتباس الحراري العالمي. (145 chars) | البياليوسيني (pronˈpæliəˌsiːn , _ ˈpæ - , _ - lioʊ - ) أو الباليوسيني، وهو ما يعني "الحديث القديم"، هو عصر جيولوجي استمر من حوالي 66 إلى 56 مليون سنة مضت. وهو أول عصر في فترة الباليوجيني في العصر الحديث السيني. كما هو الحال م ... [truncated 225 chars](1012 chars) |
| في الواقع، الاتجاه، رغم عدم أهميته الإحصائية، هو هابط. (54 chars) | الدورة الشمسية أو دورة النشاط الشمسي المغناطيسي هي التغير شبه الدوري كل 11 عامًا في نشاط الشمس (بما في ذلك التغيرات في مستويات الإشعاع الشمسي وإطلاق المواد الشمسية) والمظهر (التغيرات في عدد وحجم البقع الشمسية والاشعاعات والظو ... [truncated 225 chars](504 chars) |
| مستويات سطح البحر المحلية والإقليمية تستمر في إظهار التغير الطبيعي المعتاد، حيث ترتفع في بعض المناطق وتنخفض في البعض الآخر. (123 chars) | المستوى المتوسط للمحيطات (MSL) (يُختصر إلى مستوى سطح البحر) هو مستوى متوسط لسطح أحد أو أكثر من محيطات الأرض، ويتم استخدامه لقياس الارتفاعات مثل الارتفاعات. MSL هو نوع من المعايير المرجعية الجغرافية العمودية، ويتم استخدامه، عل ... [truncated 225 chars](878 chars) |
| يقول العلماء المناخيون أن جوانب إعصار هارفي تشير إلى أن التغير المناخي العالمي يجعل الوضع أسوأ. (95 chars) | تأثيرات تغير المناخ هي التغيرات البيئية والاجتماعية التي تسببها (بشكل مباشر أو غير مباشر) انبعاثات الغازات الدفيئة البشرية. هناك اتفاق علمي على أن تغير المناخ يحدث، وأن الأنشطة البشرية هي العامل الرئيسي. تم ملاحظة العديد من ت ... [truncated 225 chars](1120 chars) |
| تجربة CLOUD في سيرن لم تستطع اختبار جزء من أحد أربعة متطلبات ضرورية لتوجيه اللوم إلى الأشعة الكونية في ظاهرة الاحتباس الحراري، وفشلت بالفعل متطلبات أخرى اثنتان. (160 chars) | التعيين المسؤول عن التغيرات المناخية الحديثة هو الجهود العلمية لتحديد الآليات المسؤولة عن التغيرات المناخية الحديثة على الأرض، المعروفة عمومًا باسم "التسخين العالمي". وقد ركزت هذه الجهود على التغيرات الملاحظة خلال فترة سجلات ... [truncated 225 chars](1645 chars) |

### Public Sources

- [CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims](https://arxiv.org/abs/2012.00614), 2020.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595), 2025.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims | 2020 | task paper | https://arxiv.org/abs/2012.00614 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
