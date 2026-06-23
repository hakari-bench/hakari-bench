# NanoCMTEB / medical

## Overview

NanoCMTEB `medical` is a Chinese medical passage retrieval task from the Multi-CPR and C-MTEB retrieval families. Queries are short consumer-style health questions, and documents are concise medical answer passages. The task measures whether a retriever can connect informal symptom descriptions and patient concerns to the answer that addresses the exact medical scenario.

## Details

### What the Original Data Measures

Multi-CPR introduced domain-specific Chinese passage retrieval datasets, including a medical search domain, and C-MTEB includes the corresponding MedicalRetrieval task. The source setting is specialized medical retrieval rather than broad web search.

The task is similar in spirit to medical consultation QA but shorter and single-positive in the Nano labels. A query may use informal wording, shorthand, or a symptom phrase, while the answer may use clinical explanation, treatment advice, or a likely diagnosis.

### Observed Data Profile

The task contains 200 queries, 10,000 documents, and 200 relevance judgments. Every query has exactly one positive in the Nano labels, so the positives per query average, minimum, median, and maximum are all 1.0, with 0 multi-positive queries.

Queries average 18.12 Chinese characters, and documents average 119.70 characters. The examples include pediatric reflux, gynecological inflammation, viral skin conditions, swelling, musculoskeletal symptoms, and cardiac marker questions.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3582, hit@10 of 0.4400, and recall@100 of 0.5600 using the top-500 BM25 candidate subset. Lexical retrieval works when the symptom, condition, or treatment name appears in both query and answer.

BM25 is limited by informal medical wording. Patients may use colloquial symptom descriptions or non-standard spelling, while answers may use clinical terms, diagnostic explanations, or treatment categories. Same-symptom passages can also be wrong if they address a different patient context.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.5691, hit@10 of 0.6750, and recall@100 of 0.8400. Dense retrieval is the strongest profile across the reported metrics. It improves substantially over BM25 in both top-10 ranking and recall.

This indicates that semantic matching is important for Chinese medical search. Dense retrieval can connect informal patient questions to clinically phrased answers, even when the exact symptom or disease name differs.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.4699, hit@10 of 0.5700, and recall@100 of 0.8250. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 35 safeguard rows, candidate counts from 100 to 101, and a mean of 100.18 candidates.

Hybrid retrieval improves over BM25 but remains below dense retrieval. Sparse signals help when disease names or treatment terms are explicit, but the fused ordering does not match dense's ability to rank clinically responsive passages.

### Metric Interpretation for Model Researchers

This is a dense-favorable single-positive medical retrieval task. Because each query has one positive, hit@10 directly reflects whether the intended answer appears near the top. Dense retrieval is the best first-stage profile, while reranking_hybrid is useful but not superior.

Researchers should distinguish symptom overlap from answer appropriateness. A passage can mention the same organ or condition but still fail to answer the specific question. Medical-domain hard negatives are essential for meaningful improvements.

### Query and Relevance Type Tendencies

Queries include infant reflux, vulvar redness, common warts, muscle swelling, myocardial infarction markers, surgical timing, gynecological symptoms, and pediatric complaints. Positive documents are short medical answers with explanation, treatment advice, or suggested next steps.

The relevance relation is direct medical answer matching. The positive should address the patient's condition, not merely mention a related disease or body part.

### Representative Failure Modes

Likely failures include retrieving same-symptom answers for the wrong age or condition, matching treatment terms without matching diagnosis, missing colloquial-to-clinical paraphrases, and confusing related gynecological or dermatological issues.

BM25 is vulnerable to vocabulary mismatch. Dense retrieval can over-match broad symptom semantics. Hybrid retrieval helps when exact condition names are present but still needs clinical specificity.

### Training Data That May Help

Useful training data includes Chinese medical consultation QA pairs, symptom-diagnosis paraphrase data, patient question-answer retrieval pairs, and same-symptom medical hard negatives.

Synthetic data should pair brief patient questions with concise Chinese medical answer passages. Hard negatives should share symptoms, age group, or treatment terms but answer a different diagnosis or clinical scenario.

### Model Improvement Notes

Strong systems should learn Chinese medical paraphrase, symptom-to-diagnosis relations, and patient-context constraints. Dense retrieval is the best observed baseline, and domain-specific contrastive training should focus on clinically close negatives.

The task should be used for retrieval evaluation only; retrieved passages are benchmark answers, not medical advice.

## Example Data

| Query | Positive document |
| --- | --- |
| 孩子刚满月，老是反酸看着他都难受，想问一下专家该怎么办才好呢？ [31 chars] | 病情分析：这属于正常现象，妈妈不用太担心。这是因为新生儿胃的位置呈水平位，贲门括约肌也较松弛，一旦摄入奶量稍多，即可发生溢奶现象。随着孩子年龄的增长，胃的位置逐渐变垂直，贲门括约肌肌力加强，溢奶次数就会逐渐减少，七八个月时停止。意见建议：预防宝宝溢奶或吐奶有赖于家长的正确喂养，如哺乳时应将宝宝斜着抱起，不要躺着喂哺；如果是用奶瓶喂奶时，奶头孔要大小适当，奶不可太烫或太冷，更忌吸入空气；喂奶之后不要... [200 / 231 chars] |
| 小阴纯红奌用保妇康疑胶 [11 chars] | 你好,考虑是外阴炎引起的,外阴炎就是外阴的皮肤或粘膜所发生的炎症病变,如红、肿、痛、痒、糜烂等,外阴会因各种细菌感染而产生多种疾病,如外阴白斑、外阴瘙痒,一般治疗可以选择用清热解毒、除湿止痒的中草 药煎水坐浴,可以明显缓解外阴的痒痛不适,您还可以口服消炎药如环丙沙星,再配 合使用妇炎洁 或洁尔阴洗液清洗外阴综合治疗, [159 chars] |
| 寻常疣也可以用鸦胆子治疗吗 [13 chars] | 鸦胆子是可以治寻常疣，烂肉（疣）也抗病毒，但有复发的可能，最好加服阿昔洛韦片二周治疗。效果最好。这些局部用药虽可造成局部坏死而治疗寻常疣,但说到底只是一个&quot;烂&quot;字而已,有时候反而刺激寻常疣而长大,激光治疗和这些方法类似,只是将烂的时间变短,其实作为病毒感染的寻常疣一般两年左右会自愈. [152 chars] |
| 大鱼际肌肉肿胀是怎么了 [11 chars] | 你好，有可能是局部损伤，导致肿胀，可以做做冷敷，超过24小时，可以热敷，也有可能是被蚊虫叮咬了，观察一下，如果是涂抹点碘伏，很快就会好了。 [69 chars] |
| 心肌梗死血清肌凝蛋白轻链和重链变化是怎样 [20 chars] | 病情分析： 朋友你好根据您所说的情况分析这些指标主要就是分析心肌细胞受损程度的。 指导意见： 根据您所说的情况建议你想知道这么具体的区别一般是没有太特殊的意义的，主要看一下心肌损伤标志物就可以了。 [98 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Task paper | [Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval](https://arxiv.org/abs/2203.03367) |
| Benchmark paper | [C-Pack: Packed Resources For General Chinese Embeddings](https://arxiv.org/abs/2309.07597) |
| Source dataset | [mteb/MedicalRetrieval](https://huggingface.co/datasets/mteb/MedicalRetrieval) |
| NanoCMTEB dataset | [hakari-bench/NanoCMTEB](https://huggingface.co/datasets/hakari-bench/NanoCMTEB) |

Representative query and positive source snippets:

| Query | Positive document snippet |
| --- | --- |
| 孩子刚满月，老是反酸怎么办？ | An answer explains infant reflux and feeding practices to reduce spitting up. |
| 小阴唇红点能用保妇康凝胶吗？ | An answer discusses possible vulvar inflammation and cleaning or anti-inflammatory treatment. |
| 寻常疣也可以用鸦胆子治疗吗？ | An answer discusses wart treatment, recurrence, and antiviral therapy. |
| 大鱼际肌肉肿胀是怎么了？ | An answer suggests local injury or insect bite and cold or warm compresses. |
| 心肌梗死血清肌凝蛋白轻链和重链变化是怎样？ | An answer explains that such markers reflect myocardial cell injury. |
