# NanoMedical / NanoCMedQAv2reranking

## Overview

`NanoMedical / NanoCMedQAv2reranking` is a Chinese medical answer-selection task derived from CMedQAv2. Queries are informal patient consultation questions, and candidate documents are short Chinese medical answers. The original CMedQAv2 dataset was built for Chinese community medical question answering and answer selection, with anonymized online consultation content and explicit train, development, and test candidate files. This Nano split keeps the reranking-style objective: retrieve an appropriate answer from many plausible short medical replies. It is useful for studying Chinese medical retrieval, symptom paraphrase, answer selection, and the difficulty of ranking short, clinically adjacent responses.

## Details

### What the Original Data Measures

CMedQAv2 measures whether a system can select useful answers for Chinese medical questions. The task is not biomedical literature retrieval and not long-form evidence retrieval. It is closer to patient-facing consultation matching: the question may mention symptoms, duration, medication, pregnancy status, examination results, or treatment concerns, and the correct document is a concise answer that directly addresses the situation.

The official CMedQA2 repository describes a large Chinese medical QA collection for research use. The linked paper introduces attentive interaction models for Chinese medical answer selection.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 377 positive qrel rows. Queries have 1.885 positives on average, with a median of 1 and a maximum of 16. There are 88 multi-positive queries, or 44.0% of the set. Queries average 50.10 Chinese characters, while answers average 100.90 characters.

The examples cover respiratory symptoms, menstrual changes, traumatic injury, accidental ingestion of cleaning fluid, cerebral ischemia, pregnancy, pediatrics, dermatology, digestive symptoms, and cancer-related consultation. Candidate answers are short and often start with advice-like phrases such as considering a cause, recommending an examination, or suggesting hospital care.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.1527, hit@10 of 0.2750, and recall@100 of 0.3263. This is a difficult sparse-retrieval setting. Patient questions and answer replies may discuss the same clinical situation using different wording, and many negatives share high-overlap symptom terms.

BM25 is most useful when distinctive disease names, medication names, or body-part terms repeat. It struggles when the answer requires mapping colloquial symptoms to a clinical recommendation, or when several answers mention the same symptom but apply to different patient context.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.3209, hit@10 of 0.5100, and recall@100 of 0.7003. Dense retrieval is substantially stronger than BM25. The gain is especially large in recall@100, indicating that semantic matching is critical for short Chinese medical answer selection.

The task rewards embeddings that connect symptoms, diagnosis, and recommendation rather than merely matching identical Chinese terms. It also requires sensitivity to patient context such as pregnancy, age, duration, ingestion amount, or prior examination.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 59 queries carrying a rank-101 safeguard positive. It reaches nDCG@10 of 0.2529, hit@10 of 0.4300, and recall@100 of 0.6260. Hybrid retrieval improves substantially over BM25 but remains below dense retrieval on all reported metrics.

This suggests that dense retrieval is the main first-stage signal for this task, while sparse matching adds some complementary exact-term coverage. The large number of safeguard rows shows that many positives are hard to keep inside a strict top-100 candidate window.

### Metric Interpretation for Model Researchers

Scores should be interpreted as answer-selection quality over short, similar medical replies. nDCG@10 measures whether clinically appropriate answers appear early; recall@100 measures whether a reranker can see enough valid answers. The difference between BM25 and dense retrieval shows that lexical symptom overlap alone is not adequate.

Because 44.0% of queries have multiple positives, training and evaluation should support several acceptable answers per question.

### Query and Relevance Type Tendencies

Queries are informal Chinese patient questions, often with repeated descriptions and limited structure. Relevant documents are short consultation answers that provide advice, possible causes, examination suggestions, treatment guidance, or referral recommendations.

The relevance relation is direct answer usefulness. A medically related answer is not sufficient if it addresses a different diagnosis, patient condition, or recommendation.

### Representative Failure Modes

Common failures include retrieving answers that mention the same symptom but a different condition, ignoring pregnancy or pediatric context, over-matching body-part terms, and ranking vague generic advice above a specific answer. Sparse systems are especially vulnerable to same-symptom hard negatives; dense systems may still miss fine-grained contraindication or urgency cues.

### Training Data That May Help

Useful training data includes non-overlapping Chinese medical community QA pairs, Chinese answer-selection data with hard negatives, consultation-style symptom-to-advice retrieval pairs, and short-answer reranking data. Training should exclude CMedQAv2 test candidates and duplicate question-answer rows overlapping this Nano split.

### Model Improvement Notes

Models should focus on Chinese symptom normalization, patient-context handling, and short-answer discrimination. Hard negatives should share symptoms or disease names while differing in diagnosis, patient context, or recommendation. Rerankers should be trained on concise consultation replies rather than only on long biomedical passages.

## Example Data

| Query | Positive document |
| --- | --- |
| 全部症状：近一个月发现，胸闷，气短、咳嗽、低烧治疗情况 [27 chars] | 这样的情况表明癌肿已经侵犯到胸膜，可以说是后期的表现 [26 chars] |
| 全部症状：月经来的天数跟原来的一样，就只是量少了，如果是子宫内膜有异常的话该怎么办发病时间及原因：治疗情况 [53 chars] | 月经量少的原因很多，月经量少一般可能与内分泌失调、妇科炎症等有关，除了可能是黄体机能不足外，甲状腺、泌乳激素功能异常，或是曾做过人工流产手术或是子宫内膜粘连也都是可能的因素之一。子宫内膜有异常的话，要去医院检查，根据情况在医生指导下用药 [118 chars] |
| 主要诊断:右颞叶脑挫裂伤其他诊断:外伤性蛛网膜下腔出血左侧颞骨骨折我想问能不能评上十级伤残主要诊断:右颞叶脑挫裂伤其他诊断:外伤性蛛网膜下腔出血左侧颞骨骨折我想问能不能评上十级伤残？交通事故 [95 chars] | 有可能是由于骨折引起肿胀引起的疼痛这样的话需要应用消肿的药物和止痛的药物一般经过2周的时间就会没事的希望好好的保养不要活动 [61 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Multi-Scale Attentive Interaction Networks for Chinese Medical Question Answer Selection | 2018 | IEEE Access paper | [https://doi.org/10.1109/ACCESS.2018.2883637](https://doi.org/10.1109/ACCESS.2018.2883637) |
| cMedQA2 | 2018 | source repository | [https://github.com/zhangsheng93/cMedQA2](https://github.com/zhangsheng93/cMedQA2) |

### Representative Snippets

| Query | Relevant answer excerpt |
| --- | --- |
| 全部症状：近一个月发现，胸闷，气短、咳嗽、低烧治疗情况 | A short answer indicating that the cancer may have invaded the pleura and that this can be a later-stage sign. |
| 全部症状：月经来的天数跟原来的一样，就只是量少了，如果是子宫内膜有异常的话该怎么办发病时间及原因：治疗情况 | An answer explaining possible causes of low menstrual volume and recommending hospital examination and medication guidance. |
| 主要诊断:右颞叶脑挫裂伤其他诊断:外伤性蛛网膜下腔出血左侧颞骨骨折我想问能不能评上十级伤残主要诊断:右颞叶脑挫裂伤其他诊断:外伤性蛛网膜下腔出血左侧颞骨骨折我想问能不能评上十级伤残？交通事故 | A short answer discussing pain and swelling after fracture and suggesting anti-swelling and pain-relief treatment. |
| 我宝宝误喝了一爵臣牌清洗剂有事吗用去医院洗胃吗 | An answer saying that if the amount was large, hospital gastric lavage should be considered. |
| 我母亲半月前出现过几次突然眼前发黑、头很晕、无力，开始血压很高，到医院诊断是脑动脉缺血，医生解释说是脑梗塞前期，我想请问一下怎么治疗？能否治好？在饮食方面具体吃那些东西？药物方面该用什么药？在医院住过一周我想请问一下怎么治疗？能否治好？在饮食方面具体吃那些东西？药物方面该用什么药？ | An answer connecting dizziness to insufficient cerebral blood supply and suggesting relaxation, Chinese medicine, acupuncture, and physical therapy. |
