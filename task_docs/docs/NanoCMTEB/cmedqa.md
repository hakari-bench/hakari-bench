# NanoCMTEB / cmedqa

## Overview

NanoCMTEB `cmedqa` is a Chinese medical consultation retrieval task derived from the CMedQA-style retrieval setting in C-MTEB. Queries are patient questions or short case descriptions, and documents are concise doctor-style answers. The task measures whether a retriever can connect symptoms, patient context, and medical concerns to answer passages that address the specific condition.

## Details

### What the Original Data Measures

C-MTEB, described in the C-Pack benchmark paper, evaluates Chinese embedding models across retrieval and related tasks. The Cmedqa retrieval source is based on online Chinese medical consultation text. The query side resembles a patient asking about symptoms, pregnancy, pain, infection, examination results, or treatment options, while the document side resembles short clinician advice.

The task is not simple keyword lookup. Patients often describe symptoms in everyday language, while answers may use clinical phrasing, recommended examinations, treatment advice, or differential possibilities. Relevance depends on whether the answer addresses the patient's specific presentation and constraints.

### Observed Data Profile

The task contains 200 queries, 10,000 documents, and 324 relevance judgments. It is partly multi-positive: there are 1.62 positives per query on average, a minimum of 1, a median of 1.0, a maximum of 9, and 70 multi-positive queries, or 35.00% of the set.

Queries average 52.00 Chinese characters, and documents average 157.57 characters. Queries can be brief direct questions or longer symptom narratives. Documents are typically compact advice passages, which may recommend examination, rest, medication, surgery, or follow-up.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.1667, hit@10 of 0.2700, and recall@100 of 0.3735 using the top-500 BM25 candidate subset. This is a weak lexical profile. BM25 can work when the disease name, symptom, or body part is repeated in both query and answer, but many relevant answers use different wording.

The main limitation is patient-to-clinician vocabulary mismatch. A query may describe pain location and history, while the answer recommends imaging, blood tests, anti-inflammatory treatment, or hospital consultation without repeating all patient terms. Chinese word segmentation and short medical phrases also make pure term frequency fragile.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.3322, hit@10 of 0.5150, and recall@100 of 0.7222. Dense retrieval is the strongest profile across the reported metrics. It nearly doubles BM25 nDCG@10 and greatly improves recall@100.

This indicates that embedding similarity is important for Chinese medical QA retrieval. Dense retrieval can connect symptom descriptions to medically appropriate answers even when the exact disease or treatment words do not match. It is especially useful for paraphrases, implied diagnoses, and advice passages that summarize next steps.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.2595, hit@10 of 0.4200, and recall@100 of 0.6698. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 56 safeguard rows, candidate counts from 100 to 101, and a mean of 100.28 candidates.

Hybrid retrieval improves over BM25 but remains below dense retrieval. Sparse signals add value for exact disease names and body parts, but the fused ordering does not match dense's ability to rank semantically appropriate answers. For this task, dense retrieval is the best observed first-stage method.

### Metric Interpretation for Model Researchers

This task is a dense-favorable Chinese medical retrieval benchmark. BM25's low hit@10 and recall@100 show that exact term matching misses many valid doctor answers. Dense retrieval provides much better top-10 ranking and candidate coverage. Reranking_hybrid is useful but does not surpass dense.

Researchers should evaluate whether a model retrieves answers that are clinically responsive to the query, not merely answers mentioning the same symptom. Because some queries have multiple valid answers, nDCG@10 and recall@100 are both important for downstream medical QA systems.

### Query and Relevance Type Tendencies

Queries include hemorrhoid-like symptoms, radiating hip and leg pain, fever concerns, cervical cerclage discomfort, pregnancy questions, hepatitis antibody results, psychiatric symptoms, and gynecological or digestive complaints. Positive documents often provide concise medical advice, examination suggestions, and treatment or triage recommendations.

The relevance relation is answer appropriateness. A positive answer should address the patient's specific condition, risk, or next action. Answers from the same specialty can be hard negatives if they discuss the wrong symptom pattern or patient context.

### Representative Failure Modes

Likely failures include retrieving answers with the same body part but wrong disease, matching a medication name without matching the condition, missing answers that recommend tests rather than repeat symptoms, and confusing pregnancy-related risk contexts.

BM25 is vulnerable to Chinese tokenization and lexical mismatch. Dense retrieval can still over-match broad symptom similarity without enough clinical specificity. Hybrid retrieval helps when disease names are explicit but does not solve the patient-answer semantic gap.

### Training Data That May Help

Useful training data includes non-overlapping Chinese medical QA pairs, consultation question-answer retrieval pairs, disease and symptom paraphrase pairs, and same-specialty hard negatives.

Synthetic data should generate realistic patient consultation questions with symptoms, duration, pregnancy or age context, and constraints. Positive answers should directly address diagnosis, treatment, triage, or follow-up. Hard negatives should share symptoms or disease names but recommend a different action or describe a different patient context.

### Model Improvement Notes

Strong systems should model Chinese patient language, clinical terminology, and answer intent. Dense retrieval is the strongest observed baseline, but domain-specific medical contrastive training and hard negatives from similar specialties should improve ranking quality. Sparse terms remain useful for exact disease names, lab markers, and medications.

The task is suitable for evaluating medical QA retrieval, but retrieved results should be treated as benchmark relevance, not medical advice.

## Example Data

| Query | Positive document |
| --- | --- |
| 我于五天前感觉会阴部位轻微疼痛，照镜子发现是会阴边沿有米粒大小红肿。就自行涂抹马应龙痔疮膏，口服消痣胶囊，每天酒精局部消毒，顿时感觉一阵刺痛。会阴口已经有一粒花生米大小的红肿，并且已经破溃。但是白天不擦洗时并无明显不适。患处总不见好，是不是痔疮，为什么长在会阴处？我该怎么办？ [138 chars] | 根据你的情况一般的还是有用炎症的刺激造成的建议你要注意休息避免劳累及上火同时饮食清淡为主及时的进行手术的治疗 [54 chars] |
| 右臀部疼痛，疼痛的大概位置坐下的部位也能感觉到疼痛，右臀部腰也能感觉到疼痛。大腿的后外侧也能感觉到疼，小腿肚子也感觉到疼。以上症状在坐下的时候感觉厉害，站起来的瞬间疼痛加剧，站起来后疼痛减轻，不影响走路。坐着时低头有时也会引起臀部的疼痛，洗澡后感觉疼痛减轻。我这是什么病？应该怎么治疗？谢谢大夫了， [149 chars] | 因不能面诊。建议你到医院做腰椎核磁共振。骨盆拍片。血液生化全套。血常规。血沉。类风湿因子。抗O。血清尿酸等检查确诊后再治疗。 [62 chars] |
| 痔疮（外痔、内痔、）会不会引起低烧？ [18 chars] | 痔疮是人体直肠末端粘膜下和肛管皮肤下静脉丛发生扩张和屈曲所形成的柔软静脉团，多见于经常站立者和久坐者。痔疮的治疗首先要保持大便通畅，进食易消化、少含渣滓的食物。饮食应粗细搭配，少饮浓茶、咖啡、酒类及少进辛辣食物，以减少对肛管的刺激。便后要温水坐浴，局部应用痔疮栓或痔疮膏。根据病情的不同，可以采取注射治疗、冷冻治疗及物理治疗。严重者可手术治疗，包括结扎法、胶圈套扎法、痔切除等。痔疮（外痔、内痔）不会引起低烧的症状出现的 [210 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Benchmark paper | [C-Pack: Packed Resources For General Chinese Embeddings](https://arxiv.org/abs/2309.07597) |
| DOI record | [C-Pack DOI](https://doi.org/10.1145/3626772.3657878) |
| Source dataset | [mteb/CmedqaRetrieval](https://huggingface.co/datasets/mteb/CmedqaRetrieval) |
| NanoCMTEB dataset | [hakari-bench/NanoCMTEB](https://huggingface.co/datasets/hakari-bench/NanoCMTEB) |

Representative query and positive source snippets:

| Query | Positive document snippet |
| --- | --- |
| A patient describes perineal swelling, rupture, and concern about hemorrhoids. | A doctor-style answer suggests inflammation, rest, diet control, and possible surgical treatment. |
| A patient has right hip, waist, thigh, and calf pain that worsens when sitting. | An answer recommends lumbar MRI, pelvic imaging, and blood tests before treatment. |
| Can internal or external hemorrhoids cause low fever? | An answer explains hemorrhoids and states that they do not usually cause low fever. |
| Abdominal needle-like pain after cervical cerclage during pregnancy. | An answer recommends hospital examination, ruling out infection, rest, and avoiding exertion. |
| What causes velamentous placenta? | An answer explains cord attachment to membranes and fetal risk. |
