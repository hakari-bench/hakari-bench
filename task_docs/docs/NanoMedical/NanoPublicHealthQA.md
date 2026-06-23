# NanoMedical / NanoPublicHealthQA

## Overview

`NanoMedical / NanoPublicHealthQA` is an Arabic public-health FAQ retrieval task. Queries are public-facing health questions, and the relevant documents are longer official-guidance answer passages sourced from public-health Q&A or FAQ material. No standalone task paper was confirmed; the task interpretation is based on the publichealth-qa dataset card, repository metadata, and observed Nano sample data. The split is small, with 86 questions and 86 documents, but it tests an important retrieval pattern: Arabic user questions about COVID-19, infection prevention, pregnancy, breastfeeding, malaria, influenza, or healthcare procedures must retrieve the precise guidance answer rather than a generally related pandemic passage.

## Details

### What the Original Data Measures

The publichealth-qa dataset card describes question-answer pairs sourced from CDC and WHO Q&A pages and FAQs, originally connected to a multilingual COVID-QA collection. This task uses the Arabic portion as a direct question-to-answer retrieval benchmark.

The target documents are not research abstracts. They are public-health communication passages with recommendations, cautions, procedures, and conditions. Relevance depends on finding the answer to the specific action or safety question.

### Observed Data Profile

The Nano split contains 86 queries, 86 documents, and 86 positive qrel rows. Each query has exactly one positive. Queries average 79.85 characters, while documents average 828.15 characters.

The examples ask about breastfeeding while ill, ineffective COVID-19 measures, antibiotics, disinfectants for healthcare or home settings, and whether suspected or confirmed patients can share rooms. Documents often begin with a direct answer and then provide conditions, explanations, or action steps.

### BM25 Evaluation Profile

The BM25 candidate subset covers all 86 documents and reaches nDCG@10 of 0.7379, hit@10 of 0.9419, and recall@100 of 1.0000. BM25 is strong because many questions and answers share Arabic health terms, including COVID-19, infection, antibiotics, breastfeeding, disinfectants, malaria, and influenza.

The remaining difficulty is intent discrimination. Many documents share pandemic vocabulary, so sparse matching can retrieve a topically related answer that addresses the wrong action, population, or recommendation.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` covers all 86 documents and reaches nDCG@10 of 0.8176, hit@10 of 0.9767, and recall@100 of 1.0000. Dense retrieval is the strongest standalone method. This suggests that embedding similarity helps connect Arabic question intent to the correct guidance passage.

The dense advantage is especially relevant for procedural questions, where the answer may share disease terms with many other passages but is distinguished by an action such as isolation, cleaning, breastfeeding, referral, or medication.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset also covers all 86 documents and reaches nDCG@10 of 0.7847, hit@10 of 0.9535, and recall@100 of 1.0000. Hybrid retrieval improves over BM25 but remains below dense retrieval in top-rank quality.

Because the corpus contains only 86 documents, all methods have complete recall. The meaningful comparison is top-rank ordering, where dense retrieval best distinguishes the correct FAQ answer among similar public-health passages.

### Metric Interpretation for Model Researchers

Recall@100 is saturated and not informative in this small corpus. nDCG@10 and hit@10 are the useful metrics. The task should be read as Arabic FAQ answer ranking rather than candidate-generation stress testing.

Since every query has one positive, ranking the exact guidance answer above related but wrong answers is central.

### Query and Relevance Type Tendencies

Queries are Arabic public-health questions, often asking whether an action is safe, what should be avoided, how to clean or isolate, or what care procedure should be followed. Relevant documents are official-guidance style answer passages.

The relevance relation is exact FAQ answer matching. A passage about COVID-19 in general is not enough if it does not answer the specific question.

### Representative Failure Modes

Common failures include retrieving another COVID-19 guidance passage with shared vocabulary, confusing pregnancy guidance with delivery guidance, missing medication or disinfectant specificity, and ranking general prevention answers above procedural answers. Sparse systems are particularly vulnerable when disease terms dominate both query and document.

### Training Data That May Help

Useful training data includes non-overlapping Arabic public-health FAQ retrieval pairs, WHO or CDC style guidance data, Arabic medical FAQ data, and healthcare guidance question-answer pairs. Publichealth-qa examples, COVID-QA multilingual examples, and regenerated copies likely to overlap this split should be excluded for clean evaluation.

### Model Improvement Notes

Models should focus on Arabic public-health intent and action matching. Hard negatives should share disease terms while differing in recommendation, population, or procedure. Dense retrieval already performs well, but rerankers can improve exact answer selection by modeling whether a passage directly answers the question.

## Example Data

| Query | Positive document |
| --- | --- |
| أنا مصابة بمرض كوفيد-19 وأشعر بتوعك شديد لا يسمح لي بإرضاع طفلي مباشرة. ماذا أفعل؟ [82 chars] | إذا كنت تشعرين بتوعك شديد يمنعك من إرضاع طفلك مباشرة سواء بسبب مرض كوفيد-19 أو غيره من المضاعفات، فينبغي أن تلتمسي الدعم لتوفير حليبك لطفلك على نحو مأمون وبطريقة مناسبة ومتاحة ومقبولة لك. ويمكن أن يشمل ذلك ما يلي:استخراج الحليب من الثدي؛استدرار الحليب بعد انقطاعه؛الحصول على حليب أم متبرعة. [291 chars] |
| هل هناك أمور ينبغي أن أتجنبها؟ [30 chars] | التدابير التالية غير فعّالة في مواجهة مرض كوفيد-19 بل قد تكون ضارة: التدخيناستخدام كمامات متعددة تعاطي المضادات الحيوية (أنظر هل توجد أي أدوية أو علاجات يمكنها الوقاية من مرض كوفيد-19 أو علاجه؟) في جميع الأحوال، إذا كنت مصاباً بالحمى والسعال وصعوبة التنفس، التمس الرعاية الطبية مبكراً من أجل الحد من مخاطر الإصابة بعدوى أشد وطأة، وتأكد من إطلاع مقدم الرعاية الصحية على أي أماكن سافرت إليها في الآونة الأخيرة. [408 chars] |
| هل المضادات الحيوية فعّالة في الوقاية من مرض كوفيد-2019 أو علاجه؟ [65 chars] | لا. لا تقضي المضادات الحيوية على الفيروسات، فهي لا تقضي إلا على العدوى الجرثومية. وبما أن مرض كوفيد-19 سببه فيروس، فإن المضادات الحيوية لا تقضي عليه. فلا ينبغي استعمال المضادات الحيوية كوسيلة للوقاية من مرض كوفيد-19 أو علاجه. ولا ينبغي استعمالها إلا وفقاًلتعليمات الطبيب لعلاج حالات العدوى الجرثومية. [300 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| publichealth-qa | 2024 | dataset card | [https://huggingface.co/datasets/xhluca/publichealth-qa](https://huggingface.co/datasets/xhluca/publichealth-qa) |
| publichealth-qa repository |  | source repository | [https://github.com/xhluca/publichealth-qa](https://github.com/xhluca/publichealth-qa) |
| COVID-QA dataset |  | source dataset | [https://www.kaggle.com/datasets/xhlulu/covidqa](https://www.kaggle.com/datasets/xhlulu/covidqa) |

### Representative Snippets

| Query | Relevant answer excerpt |
| --- | --- |
| أنا مصابة بمرض كوفيد-19 وأشعر بتوعك شديد لا يسمح لي بإرضاع طفلي مباشرة. ماذا أفعل؟ | An Arabic guidance passage advising support for safely providing breast milk when direct breastfeeding is not possible. |
| هل هناك أمور ينبغي أن أتجنبها؟ | A passage listing ineffective or potentially harmful measures against COVID-19, such as smoking, multiple masks, and antibiotics. |
| هل المضادات الحيوية فعّالة في الوقاية من مرض كوفيد-2019 أو علاجه؟ | A passage explaining that antibiotics do not work against viruses and should not be used to prevent or treat COVID-19. |
| ما هي المطهرات الموصى باستخدامها لتنظيف البيئة في مرافق الرعاية الصحية أو المنازل التي يوجد فيها المرضى الذين يُشتبه في إصابتهم بعدوى فيروس كورونا المستجد أو الذين تأكّدت إصابتهم بها؟ | A passage recommending disinfectants effective against enveloped viruses for healthcare or home environments with suspected or confirmed cases. |
| هل يمكن جمع المرضى الذين يُشتبه في إصابتهم بعدوى فيروس كورونا المستجد أو الذين تأكّدت إصابتهم بها في نفس الغرفة؟ | A passage explaining that single rooms are preferred but cohorting suspected or confirmed patients can be an option when individual rooms are limited. |
