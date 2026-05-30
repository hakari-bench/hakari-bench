# NanoCMTEB / covid

## Overview

NanoCMTEB `covid` is a Chinese COVID-19 news and public-policy retrieval task. Queries are short fact-seeking questions about pandemic measures, dates, benefits, procedures, agencies, or local support policies. Documents are Chinese news or government-policy passages. The task measures whether a retriever can locate the passage containing the requested policy detail in a COVID-related information environment.

## Details

### What the Original Data Measures

The task belongs to the Chinese retrieval resources used in C-MTEB and is related to the Multi-CPR family of domain-specific Chinese passage retrieval datasets. The source setting is COVID-19 news and policy retrieval, where a user asks a concise question and the relevant passage contains the answer.

This differs from open-ended medical advice. The queries usually seek a specific administrative fact, such as how many measures were issued, when a medical team departed, what an agency required, or what a public-service notice instructs. Relevance depends on finding the passage with the exact policy or news detail.

### Observed Data Profile

The task contains 200 queries, 10,000 documents, and 204 relevance judgments. It is almost entirely single-positive: there are 1.02 positives per query on average, a minimum of 1, a median of 1.0, a maximum of 4, and only 2 multi-positive queries, or 1.00% of the set.

Queries average 25.73 Chinese characters. Documents average 409.35 characters and are often longer news or notice passages. Many contain local government names, dates, institutions, and procedural details.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.7888, hit@10 of 0.8750, and recall@100 of 0.9608 using the top-500 BM25 candidate subset. This is a strong lexical profile. COVID policy questions often repeat exact location names, agency names, dates, and policy terms that also appear in relevant passages.

BM25 can still fail when the query paraphrases the requested detail, when the answer is embedded in a long notice, or when several documents share similar pandemic vocabulary. But compared with medical consultation retrieval, exact term matching is highly effective here.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.7518, hit@10 of 0.8550, and recall@100 of 0.9314. Dense retrieval is strong but trails BM25 across all reported metrics. This suggests that exact lexical signals are especially important for short COVID policy questions.

Dense retrieval remains useful for paraphrased requests and semantically similar notices, but it can underweight exact administrative terms that uniquely identify the relevant passage. The task is therefore not purely semantic.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.7834, hit@10 of 0.8850, and recall@100 of 0.9902. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 2 safeguard rows, candidate counts from 100 to 101, and a mean of 100.01 candidates.

Hybrid retrieval has the best hit@10 and recall@100, while BM25 is slightly best for nDCG@10. The practical interpretation is that sparse matching provides the strongest ordering signal, and hybrid search broadens coverage enough to expose nearly all positives in the top 100.

### Metric Interpretation for Model Researchers

This task is BM25-favorable and hybrid-friendly. Exact Chinese terms, places, organizations, and dates carry much of the relevance signal. Dense retrieval is competitive but weaker than BM25 in top-rank ordering. Reranking_hybrid is the best candidate pool when recall@100 matters.

Researchers should treat this as short-query factual policy retrieval. A model should preserve entity and date precision, not only semantic similarity. High hit@10 is expected; small nDCG differences matter because most queries have only one positive.

### Query and Relevance Type Tendencies

Queries ask about Beijing measures for small businesses, Jiangsu medical teams aiding Hubei, Wuzhou online teaching arrangements, guidance for older adults and chronic disease patients, and accountability rules from transportation authorities. Positive documents are news reports, public notices, and policy summaries.

The relevance relation is answer containment. A positive passage should contain the exact requested policy detail, date, number, procedure, or administrative instruction.

### Representative Failure Modes

Likely failures include retrieving a notice from the same agency but the wrong date, matching a city name without answering the requested action, over-ranking broad COVID policy passages, and confusing similar local support policies.

BM25 is vulnerable to near-duplicate administrative wording. Dense retrieval can blur exact dates and organizations. Hybrid retrieval helps coverage but still requires precise entity and fact matching.

### Training Data That May Help

Useful training data includes Chinese COVID policy QA, Chinese news retrieval pairs, public-service FAQ retrieval data, and hard negatives from the same agency, same city, or same policy topic.

Synthetic data should generate factual Chinese questions over long policy or news passages. Questions should target dates, eligibility, administrative actions, benefits, or procedures. Hard negatives should mention the same pandemic context but not contain the answer.

### Model Improvement Notes

Strong systems should combine Chinese entity matching, date and number precision, and semantic handling of policy phrasing. BM25 is already strong, so model improvements should focus on reranking near-duplicate policy passages and preserving exact answer-bearing facts.

The benchmark is useful for evaluating public-information retrieval under short Chinese factual queries, where sparse term matching is an important baseline that dense systems must beat carefully.

## Example Data

### Public Sources

The task is part of the C-MTEB/C-Pack Chinese retrieval benchmark family and is related to COVID-focused Chinese passage retrieval resources.

### Source Reference Table

| Item | Reference |
| --- | --- |
| Task-family paper | [Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval](https://arxiv.org/abs/2203.03367) |
| Benchmark paper | [C-Pack: Packed Resources For General Chinese Embeddings](https://arxiv.org/abs/2309.07597) |
| Source dataset | [mteb/CovidRetrieval](https://huggingface.co/datasets/mteb/CovidRetrieval) |
| NanoCMTEB dataset | [hakari-bench/NanoCMTEB](https://huggingface.co/datasets/hakari-bench/NanoCMTEB) |

Representative query and positive source snippets:

| Query | Positive document snippet |
| --- | --- |
| 北京市出台多少条措施帮助中小微企业应对疫情影响？ | A news passage states that Beijing issued 16 measures and describes rent reductions. |
| 江苏援湖北第一批医疗队是什么时间？ | A report describes Jiangsu medical teams departing for Hubei during late January and February. |
| 梧州市教育局开展的线上教学活动是怎么执行的？ | A local notice describes delayed school opening and online teaching arrangements. |
| 老年人和慢性病患者出现发热咳嗽等症状时应该怎么做？ | A health-service notice provides guidance for older adults and chronic disease patients. |
| 交通运输部规定对哪类人进行问责和严肃处理？ | A transportation ministry notice describes supervision and accountability during epidemic control. |
