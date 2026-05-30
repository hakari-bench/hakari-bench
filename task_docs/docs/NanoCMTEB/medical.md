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

### Public Sources

The task is based on the medical retrieval domain from the Multi-CPR and C-MTEB Chinese retrieval benchmark families.

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
