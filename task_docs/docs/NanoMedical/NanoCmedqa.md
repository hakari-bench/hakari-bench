# NanoMedical / NanoCmedqa

## Overview

`NanoMedical / NanoCmedqa` is a Chinese medical QA retrieval task connected to the cMedQA out-of-domain setting used in DuReader-Retrieval. Queries are patient-style Chinese medical questions, and candidate documents are short consultation answers. Unlike the tighter CMedQAv2 reranking split, this task is framed as larger-pool retrieval over answer passages, testing whether a model can retrieve medically useful replies from a broader Chinese medical QA corpus. The task is useful for studying domain transfer, colloquial patient wording, symptom-to-advice matching, and the gap between lexical overlap and clinically appropriate answer retrieval.

## Details

### What the Original Data Measures

DuReader-Retrieval uses cMedQA as an out-of-domain Chinese medical retrieval test, while the underlying medical QA data traces to Chinese community medical question answering resources such as CMedQAv2. The central problem is matching a messy patient question to answer text that directly addresses the concern.

This is not encyclopedic disease retrieval. The positive answer may include a recommendation, a possible diagnosis, a test interpretation, or practical medical advice. The question often contains informal patient history rather than clean medical terminology.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 324 positive qrel rows. Queries have 1.62 positives on average, with a median of 1 and a maximum of 9. There are 70 multi-positive queries, or 35.0% of the set. Queries average 52.00 Chinese characters, while documents average 157.57 characters.

Observed questions cover menstruation, pregnancy checks, pediatric fever, gynecological symptoms, fractures, semen analysis, emotional episodes, balanitis, hemorrhoids, and post-surgical concerns. Documents are usually short medical-advice answers, though the broader retrieval pool can include noisy or only loosely related passages.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.1669, hit@10 of 0.2700, and recall@100 of 0.3735. This is a hard lexical baseline. Many queries and answers share symptoms or disease names, but the correct answer often depends on the recommendation, examination, or patient context.

BM25 is strongest when exact disease names, examination names, or rare phrases repeat. It fails when a wrong answer shares the same symptom category but gives advice for another case, or when a noisy passage happens to contain overlapping terms.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.3380, hit@10 of 0.5250, and recall@100 of 0.7191. Dense retrieval is much stronger than BM25 across all metrics. The large recall gap indicates that semantic matching is essential for mapping colloquial Chinese patient descriptions to useful medical advice.

The dense profile also shows that the task rewards domain-aware paraphrase, symptom normalization, and answer-intent matching rather than exact term matching alone.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 57 queries carrying a rank-101 safeguard positive. It reaches nDCG@10 of 0.2591, hit@10 of 0.4250, and recall@100 of 0.6667. Hybrid retrieval improves substantially over BM25 but remains below dense retrieval.

This suggests that sparse retrieval contributes some exact-term medical anchors, but dense retrieval is the stronger first-stage method for this split. The many safeguard rows show that keeping positives in a strict top-100 candidate set is difficult.

### Metric Interpretation for Model Researchers

nDCG@10 and hit@10 measure whether a useful consultation answer appears early. Recall@100 is important for reranking because many positives are missed by sparse retrieval. The dense-over-BM25 gap is a clear signal that this is a semantic medical answer-selection problem, not merely Chinese word matching.

The task has a meaningful multi-positive component, so models should support multiple acceptable answers while rejecting same-topic but clinically mismatched replies.

### Query and Relevance Type Tendencies

Queries are colloquial Chinese patient histories with symptoms, timing, examination results, treatment history, and concern. Relevant documents are short medical advice passages or answer texts.

The relevance relation is answer usefulness for the patient concern. Same-disease topicality is not enough if the advice or clinical context does not match.

### Representative Failure Modes

Common failures include retrieving a same-symptom answer for a different patient situation, missing pregnancy or pediatric constraints, over-ranking generic advice, and being distracted by noisy passages. Sparse systems struggle with medical paraphrase; dense systems may still miss fine-grained test interpretation or urgency cues.

### Training Data That May Help

Useful training data includes non-overlapping Chinese medical QA retrieval pairs, doctor-patient consultation corpora with answer relevance labels, Chinese answer-selection data with hard negatives, and symptom normalization or medical-intent matching data. CMedQA and CMedQAv2 rows overlapping this split should be excluded.

### Model Improvement Notes

Models should learn Chinese medical intent, not only symptom vocabulary. Hard negatives should share disease or symptom terms but differ in recommendation, test interpretation, timing, or patient context. Reranking models should be trained on short answer candidates and noisy same-topic negatives.

## Example Data

### Public Sources

- [DuReader-Retrieval: A Large-scale Chinese Benchmark for Passage Retrieval from Web Search Engine](https://arxiv.org/abs/2203.10232), 2022.
- [DuReader-Retrieval ACL Anthology record](https://aclanthology.org/2022.emnlp-main.357/).
- [Multi-Scale Attentive Interaction Networks for Chinese Medical Question Answer Selection](https://doi.org/10.1109/ACCESS.2018.2883637), 2018.
- [cMedQA2 repository](https://github.com/zhangsheng93/cMedQA2), official dataset repository.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| DuReader-Retrieval: A Large-scale Chinese Benchmark for Passage Retrieval from Web Search Engine | 2022 | arXiv paper | https://arxiv.org/abs/2203.10232 |
| DuReader-Retrieval: A Large-scale Chinese Benchmark for Passage Retrieval from Web Search Engine | 2022 | ACL Anthology paper | https://aclanthology.org/2022.emnlp-main.357/ |
| Multi-Scale Attentive Interaction Networks for Chinese Medical Question Answer Selection | 2018 | IEEE Access paper | https://doi.org/10.1109/ACCESS.2018.2883637 |
| cMedQA2 | 2018 | source repository | https://github.com/zhangsheng93/cMedQA2 |

### Representative Snippets

| Query | Relevant answer excerpt |
| --- | --- |
| 我于五天前感觉会阴部位轻微疼痛，照镜子发现是会阴边沿有米粒大小红肿... | An answer suggesting inflammation, rest, avoiding fatigue and irritation, a light diet, and timely treatment. |
| 右臀部疼痛，疼痛的大概位置坐下的部位也能感觉到疼痛... | An answer recommending hospital imaging and blood tests before diagnosis and treatment. |
| 痔疮（外痔、内痔、）会不会引起低烧？ | An answer explaining hemorrhoids and stating that internal or external hemorrhoids do not cause low fever. |
| 宫颈环扎后腹部有时会有像针扎一样是什么原因... | An answer recommending prompt hospital examination to rule out local infection and advising bed rest. |
| 帆状胎盘是什么原因引起的 | An answer defining velamentous cord insertion and noting that its main risk is to the fetus. |
