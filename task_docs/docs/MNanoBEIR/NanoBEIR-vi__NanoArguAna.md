# MNanoBEIR / NanoBEIR-vi / NanoArguAna

## Overview

NanoArguAna in the Vietnamese NanoBEIR slice is an argument-counterargument retrieval task derived from ArguAna. The queries and documents are Vietnamese translated argumentative passages, and each query has one paired relevant response passage. The benchmark measures whether a retriever can identify argumentative relation and response fit between long texts, rather than only retrieving a same-topic passage. It is a compact diagnostic for stance-aware multilingual retrieval in Vietnamese.

## Details

### What the Original Data Measures

ArguAna is used in BEIR as an argument retrieval benchmark where relevance depends on the relationship between an argument and a counterargument. The relevant document often challenges a premise, qualifies a claim, or answers a specific argumentative move. A same-topic passage may be a distractor if it does not respond to the query's stance or reasoning.

The Vietnamese translated version presents long argumentative passages on both sides. The model must compare claims, premises, stance, and discourse relation across substantial text. Lexical overlap can locate the debate topic, but the correct paired response may not be the passage with the most repeated words.

### Observed Data Profile

The task contains 50 queries, 3,635 documents, and 50 relevance judgments. Every query has exactly one positive passage: the average, minimum, median, and maximum positives per query are all 1.0, and there are no multi-positive queries. This makes the benchmark a precise single-target retrieval task.

Queries average 979.28 characters, and documents average 998.38 characters. Both sides are long, which makes the task different from short-query passage retrieval. Ranking quality depends on understanding the whole argument, not only isolated keywords.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4275, hit@10 of 0.7400, and recall@100 of 0.9200 using the top-500 BM25 candidate subset. This is a strong lexical candidate-generation profile. Long passages share topic words, entities, and policy terms, so BM25 often finds the correct response somewhere in the first 100 ranks.

The weaker top-10 ordering shows the main difficulty. Many passages may discuss the same issue, but only one is the paired response. BM25 can over-rank same-topic distractors because it does not directly model stance, rebuttal structure, or response target.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.4529, hit@10 of 0.8400, and recall@100 of 0.9400. Dense retrieval improves over BM25 across all three metrics. This indicates that embedding similarity better captures argumentative relatedness and response fit than exact overlap alone.

The dense gain is particularly visible in hit@10. Vietnamese argument passages can share topic vocabulary while differing in stance; dense retrieval appears better at placing the true paired response near the top. Remaining errors likely involve stance mismatch, broad same-topic similarity, or long passages where only part of the text responds to the query.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.4701, hit@10 of 0.7800, and recall@100 of 1.0000. It uses exactly 100 candidates per query, with no rank-101 safeguard rows. The hybrid profile has the best nDCG@10 and complete recall@100, while dense retrieval has the highest hit@10.

This pattern shows that hybrid search is an excellent candidate source for Vietnamese ArguAna. Combining lexical and dense evidence ensures that every positive is present by rank 100 and slightly improves graded top-10 ranking. However, the lower hit@10 than dense retrieval suggests that the final ordering can still place same-topic distractors above the true response for some queries.

### Metric Interpretation for Model Researchers

Because there is exactly one positive per query, hit@10 and nDCG@10 directly measure whether the paired response is usable in the first page. recall@100 measures whether a later reranker has access to the correct response. The complete hybrid recall is valuable, but top-rank ordering still needs discourse-aware modeling.

The method comparison shows a progression from lexical topic matching to semantic response matching and then to hybrid coverage. Dense retrieval is strong for immediate top-10 access, while reranking_hybrid is strongest as a candidate pool. This task is useful for testing whether rerankers can exploit high recall to identify stance and counterargument relation.

### Query and Relevance Type Tendencies

Queries are long arguments about issues such as public indifference to reform, Heathrow expansion, choice overload, cyberattacks by non-state actors, and religion, hate speech, and free expression. Positive documents are response passages that often challenge, qualify, or counter the query's reasoning.

The task rewards models that understand the argument target. The relevant passage should respond to the query's premise or stance, not merely discuss the same policy area. This makes argument relation more important than broad topical similarity.

### Representative Failure Modes

Likely failures include retrieving same-topic passages that do not respond to the query, confusing supportive and counterargument roles, over-ranking long passages with repeated policy vocabulary, and missing the paired response when Vietnamese translation changes phrasing. Dense models can retrieve stance-mismatched passages, while BM25 can rank lexical distractors too high.

### Training Data That May Help

Useful training data includes Vietnamese debate retrieval, argument-counterargument pairs, stance-aware ranking, multilingual argument mining, and hard negatives that share topic vocabulary but answer a different premise. For rerankers, same-topic non-response passages are especially valuable because they mirror the task's main failure mode.

### Model Improvement Notes

A model targeting this task should improve long-text response-relation modeling. Sparse systems should preserve strong candidate recall while reducing same-topic distractors. Dense systems need hard-negative training for stance and premise matching. Hybrid systems are promising because they provide complete recall, but they need a reranker that compares claims, stance, and counterargument structure.

## Example Data

| Query | Positive document |
| --- | --- |
| Công chúng thờ ơ với cải cách. Liệu cải cách của Thượng viện có nên là ưu tiên hàng đầu trong bối cả... [100 / 824 chars] | Chiến dịch AV không thể so sánh với cải cách Thượng viện, hơn nữa không nên nhầm lẫn một công chúng thiếu thông tin do sự xoay chuyển chính trị với sự thờ ơ. Thường thì cử tri bày tỏ rằng họ thờ ơ vì... [200 / 412 chars] |
| Sự mở rộng của Heathrow là rất quan trọng cho nền kinh tế Mở rộng Heathrow sẽ đảm bảo nhiều việc làm... [100 / 1,000 chars] | Cộng đồng doanh nghiệp còn xa mới thống nhất trong sự ủng hộ được cho là dành cho một đường băng thứ ba. Các cuộc khảo sát cho thấy nhiều doanh nghiệp có ảnh hưởng thực sự không ủng hộ việc mở rộng. M... [200 / 1,180 chars] |
| Con người được đưa ra quá nhiều sự lựa chọn, điều này khiến họ kém hạnh phúc hơn. Quảng cáo dẫn đến... [100 / 952 chars] | Con người không hạnh phúc vì họ không thể có mọi thứ, chứ không phải vì họ được đưa ra quá nhiều sự lựa chọn và cảm thấy căng thẳng. Thực tế, quảng cáo đóng một vai trò quan trọng trong việc đảm bảo r... [200 / 734 chars] |
| Các cuộc tấn công mạng thường được thực hiện bởi các tác nhân phi nhà nước Các cuộc tấn công mạng th... [100 / 1,143 chars] | Trong trường hợp các tác nhân phi nhà nước tấn công, nhiều chuyên gia trong lĩnh vực luật quốc tế đồng ý rằng nhà nước vẫn có thể trả đũa để tự vệ nếu một nhà nước khác "không sẵn sàng hoặc không có k... [200 / 592 chars] |
| Bởi vì tôn giáo thúc đẩy sự chắc chắn trong niềm tin, sự thù hận được thần thánh hóa dễ dàng được sử... [100 / 1,172 chars] | Không ai bị buộc phải thực hiện các hành vi bạo lực bởi lời nói của người khác; đó là sự lựa chọn của họ. Tương tự, có rất nhiều người có quan điểm có thể được coi là kỳ thị đồng tính nhưng lại cảm th... [200 / 657 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [ArguAna](https://aclanthology.org/P18-1023/) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-vi dataset | [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi) |

Representative query and positive response snippets:

| Query | Positive document snippet |
| --- | --- |
| Công chúng thờ ơ với cải cách. Liệu cải cách của Thượng viện có nên là ưu tiên hàng đầu... | Chiến dịch AV không thể so sánh với cải cách Thượng viện, hơn nữa không nên nhầm lẫn... |
| Sự mở rộng của Heathrow là rất quan trọng cho nền kinh tế... | Cộng đồng doanh nghiệp còn xa mới thống nhất trong sự ủng hộ được cho là dành cho một đường băng thứ ba... |
| Con người được đưa ra quá nhiều sự lựa chọn, điều này khiến họ kém hạnh phúc hơn... | Con người không hạnh phúc vì họ không thể có mọi thứ... |
| Các cuộc tấn công mạng thường được thực hiện bởi các tác nhân phi nhà nước... | Trong trường hợp các tác nhân phi nhà nước tấn công, nhiều chuyên gia trong lĩnh vực luật quốc tế đồng ý... |
| Bởi vì tôn giáo thúc đẩy sự chắc chắn trong niềm tin... | Không ai bị buộc phải thực hiện các hành vi bạo lực bởi lời nói của người khác... |
