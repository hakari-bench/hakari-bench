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
| Công chúng thờ ơ với cải cách. Liệu cải cách của Thượng viện có nên là ưu tiên hàng đầu trong bối cảnh kinh tế hiện tại hay không là một vấn đề gây tranh cãi, chưa kể đến việc liệu một chính phủ liên minh có thể khởi xướng và thực hiện những biện pháp như vậy hay không. Những nỗ lực cải cách Thượng viện đã bị trì hoãn nhiều lần, cho thấy sự dè dặt của Hạ viện đối với sự thay đổi. [1] Một cảm giác chắc chắn được phản ánh trong ý kiến công chúng Anh – như được thể hiện qua kết quả gần đây của Phiế... [500 / 824 chars] | Chiến dịch AV không thể so sánh với cải cách Thượng viện, hơn nữa không nên nhầm lẫn một công chúng thiếu thông tin do sự xoay chuyển chính trị với sự thờ ơ. Thường thì cử tri bày tỏ rằng họ thờ ơ vì họ cảm thấy rằng họ không thể thay đổi điều gì, rằng lá phiếu của họ sẽ không có giá trị: cải cách đảm bảo rằng những người điều hành đất nước được bầu trực tiếp bởi nhân dân sẽ giúp chống lại những cảm giác này. [412 chars] |
| Sự mở rộng của Heathrow là rất quan trọng cho nền kinh tế Mở rộng Heathrow sẽ đảm bảo nhiều việc làm hiện tại cũng như tạo ra những việc làm mới. Hiện tại, Heathrow hỗ trợ khoảng 250.000 việc làm. [1] Thêm vào đó, hàng trăm ngàn việc làm khác phụ thuộc vào ngành du lịch ở London, điều này dựa vào các liên kết giao thông tốt như Heathrow. Mất đi khả năng cạnh tranh trước các sân bay châu Âu khác không chỉ có thể dẫn đến việc lãng phí khả năng tạo ra việc làm mới, mà còn mất đi một số việc làm hiệ... [500 / 1,000 chars] | Cộng đồng doanh nghiệp còn xa mới thống nhất trong sự ủng hộ được cho là dành cho một đường băng thứ ba. Các cuộc khảo sát cho thấy nhiều doanh nghiệp có ảnh hưởng thực sự không ủng hộ việc mở rộng. Một bức thư bày tỏ lo ngại đã được ký bởi Justin King, Giám đốc điều hành của J Sainsbury và James Murdoch của BskyB. Do đó, việc gộp cộng đồng doanh nghiệp thành một tiếng nói kêu gọi mở rộng là sai lầm. Chúng ta cũng nên nhớ, khi xem xét các lựa chọn thay thế cho đường băng mới của Heathrow như một đường băng mới tại một sân bay khác ở London hoặc một sân bay hoàn toàn mới, rằng những điều này có thể có tác động kinh tế tương tự như việc mở rộng Heathrow. Nếu các kết nối là điều quan trọng để thu hút doanh nghiệp và du khách thì miễn là kết nối đó với London, không quan trọng sân bay nào là nguồn gốc của kết nối. Có thể thậm chí không cần thiết sân bay trở thành sân bay trung tâm nếu chúng ta tập trung vào lợi ích cho London, như Bob Ayling, cựu Giám đốc điều hành của British Airways đã n... [1,000 / 1,180 chars] |
| Con người được đưa ra quá nhiều sự lựa chọn, điều này khiến họ kém hạnh phúc hơn. Quảng cáo dẫn đến việc nhiều người bị choáng ngợp bởi nhu cầu vô tận phải quyết định giữa các yêu cầu cạnh tranh về sự chú ý của họ - điều này được gọi là sự chuyên chế của sự lựa chọn hoặc quá tải lựa chọn. Nghiên cứu gần đây cho thấy rằng trung bình con người kém hạnh phúc hơn so với 30 năm trước - mặc dù họ có cuộc sống tốt hơn và có nhiều sự lựa chọn hơn về những thứ để chi tiêu. Các tuyên bố của quảng cáo dồn... [500 / 952 chars] | Con người không hạnh phúc vì họ không thể có mọi thứ, chứ không phải vì họ được đưa ra quá nhiều sự lựa chọn và cảm thấy căng thẳng. Thực tế, quảng cáo đóng một vai trò quan trọng trong việc đảm bảo rằng số tiền mà mọi người có, họ chi tiêu cho sản phẩm phù hợp nhất với bản thân. Nếu không cho phép quảng cáo, mọi người sẽ lãng phí tiền vào một sản phẩm ban đầu khi, nếu có sự lựa chọn, họ rõ ràng sẽ chọn một sản phẩm khác. Một phân tích tổng hợp kết hợp nghiên cứu từ 50 nghiên cứu độc lập không tìm thấy mối liên hệ có ý nghĩa giữa sự lựa chọn và lo âu, nhưng suy đoán rằng sự biến đổi trong các nghiên cứu để lại khả năng rằng quá tải lựa chọn có thể liên quan đến một số điều kiện tiên quyết rất cụ thể và vẫn chưa được hiểu rõ. [734 chars] |

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
