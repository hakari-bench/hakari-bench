# NanoMedical / NanoCMedQAv2reranking

## Overview

CMedQAv2 was introduced for Chinese medical question-answer selection, using
online consultation questions and candidate answers from community medical QA.
This NanoMedical reranking-style split keeps that answer-selection objective:
patient questions with symptoms, pregnancy context, test results, medication
history, or treatment concerns must retrieve medically appropriate short answer
candidates. The difficulty is not broad document search but distinguishing
plausible Chinese consultation replies that share symptoms or body parts while
giving different advice.

## Details

### What the Original Data Measures

[Multi-Scale Attentive Interaction Networks for Chinese Medical Question Answer Selection](https://doi.org/10.1109/ACCESS.2018.2883637)
introduced CMedQAv2 as an expanded Chinese medical question-answer selection
dataset. The official [cMedQA2 repository](https://github.com/zhangsheng93/cMedQA2)
describes it as an updated dataset for Chinese community medical question
answering, available for non-commercial research, anonymized to protect privacy,
and split into train, development, and test candidate files. The repository
reports 108,000 questions and 203,569 answers in total, with average character
lengths of about 49 for questions and 101 for answers.

This task measures answer selection, not full-document medical literature
retrieval. The user question can be informal, redundant, and symptom-heavy, while
the positive answer is usually a concise consultation response: a likely cause,
a recommended examination, a caution during pregnancy, a dietary or medication
suggestion, or a referral to a hospital department. The relevant answer may not
share all symptoms verbatim; it often has to infer the consultation target from
messy phrasing.

### Observed Data Profile

The Nano split has 200 queries, 10,000 candidate-answer documents, and 377
positive qrel rows. The average query has 1.89 positives, but the distribution
is uneven: 112 queries have only one positive, while one query has 16 positives.
Queries average 50.10 characters and documents average 100.90 characters, close
to the official CMedQAv2 repository statistics.

The sampled questions cover pregnancy, gynecology, pediatrics, respiratory
disease, chronic pain, oncology, orthopedics, dermatology, digestion, and general
symptom triage. Many queries include repeated phrasing and patient-history
fragments, for example current symptoms, duration, previous examinations, and
past medication effects. Candidate answers frequently begin with advice markers
such as `考虑`, `一般`, `建议`, `根据`, or `如果`, making many documents look
superficially similar even when they answer different clinical situations.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.1500
and hit@10 = 0.2750. It ranks 25 positives first and 63 of 377 positives inside
the top 10. This is a hard sparse-retrieval setting: even though question and
answer are both short Chinese medical consultation text, the correct answer can
use different wording from the patient question, and many negatives contain the
same disease, symptom, pregnancy, or body-part terms.

Observed BM25 failures are mostly fine-grained answer-selection errors. For a
question about pediatric hyperactivity, BM25 ranks a general "what are you
asking" reply first and places a correct ADHD-treatment answer outside the top
10. For a right-hand weakness question, it retrieves other right/left-hand or
injury passages before the answer about cervical disease, cerebral vascular
disease, or peripheral neuritis. For waterpox transmission, it retrieves related
immunity and vaccine passages before the longer answer explaining lifetime
immunity and transmission. These failures show that lexical overlap alone is not
enough; the model must match symptoms, context, and clinical recommendation.

### Training Data That May Help

Useful training data includes non-overlapping Chinese medical community QA
pairs, Chinese answer-selection datasets with positive and hard-negative
candidate answers, consultation-style symptom-to-advice pairs, and supervised
reranking data where answers are short and medically adjacent negatives are
present. Chinese medical terminology, colloquial patient wording, pregnancy and
pediatric phrasing, and symptom normalization are all important.

Because CMedQAv2 is public and the official split files are explicit, training
for clean evaluation should exclude the CMedQAv2 test candidates and any
duplicate question-answer rows that overlap this Nano split. Closely related
datasets scraped from the same Chinese medical consultation sources should be
deduplicated before use.

### Synthetic Data Guidance

For document-to-question generation, start from non-evaluation Chinese medical
consultation answers and generate patient questions that contain symptoms,
duration, age or pregnancy status, and a concrete concern. The answer should
remain a short consultation reply, not a long encyclopedia article.

For joint document-and-question generation, create Chinese patient questions and
several candidate answers per question: one or more correct answers plus hard
negatives that share symptoms or disease names but give a different diagnosis,
patient context, or recommendation. Synthetic data should include noisy,
informal, repeated patient phrasing, but should not copy CMedQAv2 evaluation
queries or answers.

## Example Data

| Query | Positive document |
| --- | --- |
| 全部症状：近一个月发现，胸闷，气短、咳嗽、低烧治疗情况 (27 chars) | 这样的情况表明癌肿已经侵犯到胸膜，可以说是后期的表现 (26 chars) |
| 全部症状：月经来的天数跟原来的一样，就只是量少了，如果是子宫内膜有异常的话该怎么办发病时间及原因：治疗情况 (53 chars) | 月经量少的原因很多，月经量少一般可能与内分泌失调、妇科炎症等有关，除了可能是黄体机能不足外，甲状腺、泌乳激素功能异常，或是曾做过人工流产手术或是子宫内膜粘连也都是可能的因素之一。子宫内膜有异常的话，要去医院检查，根据情况在医生指导下用药 (118 chars) |
| 主要诊断:右颞叶脑挫裂伤其他诊断:外伤性蛛网膜下腔出血左侧颞骨骨折我想问能不能评上十级伤残主要诊断:右颞叶脑挫裂伤其他诊断:外伤性蛛网膜下腔出血左侧颞骨骨折我想问能不能评上十级伤残？交通事故 (95 chars) | 有可能是由于骨折引起肿胀引起的疼痛这样的话需要应用消肿的药物和止痛的药物一般经过2周的时间就会没事的希望好好的保养不要活动 (61 chars) |
| 我宝宝误喝了一爵臣牌清洗剂有事吗用去医院洗胃吗 (23 chars) | 你的情况要考虑这个如果量比较多的话还是要到医院进行洗胃治疗的。 (31 chars) |
| 我母亲半月前出现过几次突然眼前发黑、头很晕、无力，开始血压很高，到医院诊断是脑动脉缺血，医生解释说是脑梗塞前期，我想请问一下怎么治疗？能否治好？在饮食方面具体吃那些东西？药物方面该用什么药？在医院住过一周我想请问一下怎么治疗？能否治好？在饮食方面具体吃那些东西？药物方面该用什么药？ (141 chars) | 你头晕或眩晕是脑供血不足引起的，可能有脑血管痉挛，由于紧张压力等因素造成的，需要放松训练，、最好采用中医中药治疗，中药方剂有效，结合针灸理疗效果好，特别是头针治疗有特效 (84 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMedical |
| Backing dataset | NanoMedical |
| Task / split | NanoCMedQAv2reranking |
| Hugging Face dataset | [hakari-bench/NanoMedical](https://huggingface.co/datasets/hakari-bench/NanoMedical) |
| Language | zh |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 377 |
| Positives per query | avg 1.89; min 1; median 1; max 16 |
| Multi-positive queries | 88 / 200 (44.00%) |
| BM25 nDCG@10 | 0.1500 |
| BM25 hit@10 | 0.2750 |
| Query length avg chars | 50.10 |
| Document length avg chars | 100.90 |

### Public Sources

- [Multi-Scale Attentive Interaction Networks for Chinese Medical Question Answer Selection](https://doi.org/10.1109/ACCESS.2018.2883637); 2018; Sheng Zhang, Xin Zhang, Hui Wang, Liang Guo, and Shanshan Liu.
- [cMedQA2 repository](https://github.com/zhangsheng93/cMedQA2), the official dataset repository.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMedical](https://huggingface.co/datasets/hakari-bench/NanoMedical)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Multi-Scale Attentive Interaction Networks for Chinese Medical Question Answer Selection | 2018 | IEEE Access paper | https://doi.org/10.1109/ACCESS.2018.2883637 |
| cMedQA2 | 2018 | source repository | https://github.com/zhangsheng93/cMedQA2 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMedical
  backing_dataset: NanoMedical
  dataset_id: hakari-bench/NanoMedical
  task_name: NanoCMedQAv2reranking
  split_name: NanoCMedQAv2reranking
  language: zh
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMedical/NanoCMedQAv2reranking.md
  source_research:
    primary_source_type: task_paper_and_repository
    paper_pdf_or_html_checked: false
    no_fulltext_note: IEEE full text was not accessible from the local environment; official DOI metadata, the cMedQA2 repository, and observed Nano samples were checked
    paper_url: https://doi.org/10.1109/ACCESS.2018.2883637
    additional_source_urls:
      - https://github.com/zhangsheng93/cMedQA2
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 377
  positives_per_query:
    average: 1.885
    min: 1
    median: 1.0
    max: 16
    multi_positive_queries: 88
    multi_positive_query_percent: 44.0
  text_stats_chars:
    query_mean: 50.105
    document_mean: 100.8981
  bm25:
    ndcg_at_10: 0.1500390078
    hit_at_10: 0.275
    source: dataset_bm25_column
  learning:
    original_train_split: available_in_cMedQAv2
    evaluation_split_origin: CMedQAv2 answer-selection candidate split sampled into NanoMedical
    train_eval_overlap_audit: not_audited
    leakage_note: exclude CMedQAv2 test candidates and duplicate question-answer rows overlapping this Nano split
    useful_training_data:
      - non-overlapping Chinese medical community QA pairs
      - Chinese medical answer-selection data with hard negatives
      - consultation-style symptom-to-advice retrieval pairs
    synthetic_data:
      document_generation: short Chinese consultation answers with diagnosis, examination, treatment, or referral advice
      question_generation: informal Chinese patient questions with symptoms, duration, and context
      hard_negatives: same-symptom answers with different diagnosis, patient context, or recommendation
      answerability: correct answers should directly address the patient question without requiring external context
    multi_positive_training: support multiple acceptable answers per question and short hard-negative answers
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMedical
    source_urls:
      - label: CMedQAv2 paper DOI
        url: https://doi.org/10.1109/ACCESS.2018.2883637
      - label: cMedQA2 repository
        url: https://github.com/zhangsheng93/cMedQA2
```
