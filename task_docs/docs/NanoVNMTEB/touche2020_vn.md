# NanoVNMTEB / touche2020_vn

## Overview

`touche2020_vn` is the Vietnamese NanoVNMTEB version of the Touché 2020 argument-retrieval task. Touché 2020 Task 1 asks systems to retrieve relevant arguments for controversial questions from debate-style sources. VN-MTEB translates the topics and passages into Vietnamese, preserving the argument-retrieval setting rather than turning it into ordinary topical search.

The Nano split contains 25 queries, 10,000 candidate documents, and 481 positive qrels. Queries average 52.2 characters, while documents average 1,939.6177 characters. Every query has multiple positives, with an average of 19.24 positives per query. All three retrieval conditions achieve hit@10 of 1.0, so the meaningful difference is ranking quality and recall over many arguments. `reranking_hybrid` is strongest on nDCG@10, dense retrieval is strongest on recall@100, and BM25 is competitive because controversial topics have strong lexical anchors.

## Details

### What the Original Data Measures

Touché 2020 evaluates argument retrieval: given a controversial question, the system should retrieve passages that contain relevant arguments. Relevance is not just about mentioning the topic. A good result should present useful pro or con reasoning, with claims and premises that address the question.

The Vietnamese version translates debate topics and long argumentative passages. Topics include voting age, prescription-drug advertising, renewable energy, voting rights for former offenders, gun control, minimum wage, obesity as disease, universal basic income, and capital punishment. The model must retrieve passages that argue about the question, not merely passages that contain topical words.

### Observed Data Profile

The task has only 25 queries but 481 positives. Every query is multi-positive, with a minimum of 6, a median of 19, and a maximum of 32 positives. This makes it a small-topic, many-answer benchmark. Each topic can have several relevant arguments, often representing different stance, quality, and detail.

Documents are long debate passages, and some are very long. A relevant passage may include concessions, rebuttals, policy details, examples, and stance-specific reasoning. Query-document matching therefore involves both topic identification and argument usefulness.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6841345409, hit@10 of 1.0, and recall@100 of 0.8212058212 with a top-500 candidate set. The perfect hit@10 is not surprising: controversial questions contain distinctive topic words, and every query has many positives.

BM25's weakness is not first positive retrieval but ordering. Topic words such as gun control, minimum wage, prescription drugs, voting age, or renewable energy occur in many debate passages. Sparse retrieval can find on-topic text but may not rank the best arguments, stance-balanced material, or most directly responsive passages highest.

### Dense Evaluation Profile

Dense retrieval with `harrier-oss-270m` reaches nDCG@10 of 0.6869062421, hit@10 of 1.0, and recall@100 of 0.9043659044. It is very close to BM25 on nDCG@10 but substantially better on recall@100. Dense retrieval appears to broaden candidate coverage by recognizing arguments that use different wording for the same issue.

Dense retrieval is useful when the passage discusses the policy implication or premise without repeating the exact topic phrase. It can connect paraphrased arguments about public health, social policy, criminal justice, or energy systems. Its top-rank advantage is small because many documents are topically similar and long, making fine-grained argument quality difficult.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reaches nDCG@10 of 0.7280316314, hit@10 of 1.0, and recall@100 of 0.8960498960. The top-100 candidate pool has exactly 100 candidates per query and no safeguard-expanded rows. Hybrid retrieval gives the best nDCG@10 while slightly trailing dense on recall@100.

This is a useful argument-retrieval pattern. Sparse evidence anchors the topic, while dense evidence expands to paraphrased reasoning. Hybrid ranking can place stronger arguments higher in the first ten results, even if dense retrieves a slightly broader set by rank 100. Since every system already hits at least one positive, the hybrid benefit is mainly better top-rank argument ordering.

### Metric Interpretation for Model Researchers

Hit@10 is saturated and should not drive interpretation. nDCG@10 and recall@100 are the meaningful metrics. nDCG@10 reflects whether the model ranks useful arguments near the top; recall@100 reflects whether it covers many arguments for each controversial question.

This task is not a single-answer benchmark. It rewards retrieving multiple relevant arguments, potentially across stances. Researchers should inspect whether a model retrieves diverse pro and con reasoning or just many passages from one lexical cluster.

### Query and Relevance Type Tendencies

Queries are controversial questions. Relevant documents are argumentative passages with claims, premises, rebuttals, examples, or policy reasoning. They may support or oppose the proposition, and both can be relevant if they address the topic.

Relevance is argument relevance. A passage about gun ownership is not necessarily relevant to a gun-control topic unless it argues for or against the policy question. A passage about renewable energy is not necessarily relevant unless it addresses replacement of fossil fuels or a related debate claim.

### Representative Failure Modes

BM25 can retrieve long topical passages with weak argument content. Dense retrieval can retrieve broad opinion text that is semantically adjacent but not directly responsive. Hybrid retrieval can improve top ranks but still over-represent one stance or one argument style.

Another failure mode is ignoring stance and premise. A useful argument retrieval system should distinguish a factual background paragraph from an actual argument, and it should recognize whether the passage addresses the controversial question directly.

### Training Data That May Help

Useful training data includes non-overlapping Touché argument-retrieval data, Vietnamese debate and opinion QA, argument-mining corpora, stance-labeled argument data, and translated argument retrieval with overlap removed. Multi-positive training is essential because each topic has many relevant passages.

Synthetic data should generate controversial Vietnamese questions and multiple pro and con arguments. Hard negatives should share the topic but be off-stance, low-quality, or not actually argumentative.

### Model Improvement Notes

The main improvement direction is argument-aware reranking. Candidate generation is already strong enough to hit positives, so ranking should focus on directness, stance, premise quality, and diversity. Sparse signals can anchor the topic, while dense signals can capture paraphrased reasoning.

Error analysis should check stance balance, argument directness, and whether top-ranked passages are actually argumentative. A model that only retrieves topic mentions will look acceptable on hit@10 but weak for real argument search.

## Example Data

| Query | Positive document |
| --- | --- |
| Tuổi bỏ phiếu có nên được giảm xuống? [37 chars] | Pro không đưa ra bất kỳ một lý do hợp lý nào để giảm độ tuổi bầu cử. Tuy nhiên có khá nhiều lý do tại sao độ tuổi bầu cử của Anh Quốc không nên được giảm xuống. 1) Những người trẻ tuổi không quan tâm... [200 / 2,112 chars] |
| Thuốc kê đơn có nên quảng cáo trực tiếp cho người tiêu dùng không? [66 chars] | Nhiều quảng cáo không cung cấp đủ thông tin về mức độ hiệu quả của thuốc. Ví dụ, Lunesta được quảng cáo bởi một con tằm bay qua cửa sổ phòng ngủ trên một người đang ngủ yên bình. Thực tế, Lunesta giúp... [200 / 1,804 chars] |
| Liệu năng lượng tái tạo có thể thay thế nhiên liệu hóa thạch một cách hiệu quả? [79 chars] | Trong mỗi lập luận tôi chỉ định đăng một điểm. Bây giờ để bác bỏ ý tưởng của đối thủ rằng thủy điện kết hợp với năng lượng gió và mặt trời có thể trong lý thuyết cung cấp năng lượng cho Hoa Kỳ, tôi mu... [200 / 4,070 chars] |
| Những người phạm tội đã mãn hạn tù có được phép bỏ phiếu không? [63 chars] | Mặc dù hồ sơ của đối thủ tranh luận rằng ông ta sống ở Ấn Độ, cuộc tranh luận này là về tội phạm và quyền bầu cử trong một xã hội dân chủ. Tôi không quen với luật pháp và mong đợi của xã hội Ấn Độ cũn... [200 / 6,356 chars] |
| Có nên ban hành thêm các luật kiểm soát súng? [45 chars] | Ngay cả trước khi bắt đầu tấn công với vụ án của đối thủ, tôi muốn giải thích rằng đối thủ của tôi đã bỏ lỡ bản chất cơ bản của cuộc tranh luận. Trong cuộc tranh luận này, "Những vụ nổ súng gần đây và... [200 / 7,757 chars] |

### Source Reference Table

| Source | Role |
|---|---|
| Touché 2020 overview | Original argument-retrieval shared task description |
| Touché 2020 Task 1 page | Official task page |
| BEIR | Retrieval benchmark framing |
| VN-MTEB | Vietnamese benchmark collection using translated retrieval tasks |
| GreenNode dataset card | Public dataset entry for this Vietnamese split |

### Representative Snippets

- Query: `Tuổi bỏ phiếu có nên được giảm xuống?`
  Relevant documents argue for or against lowering the voting age.
- Query: `Thuốc kê đơn có nên quảng cáo trực tiếp cho người tiêu dùng không?`
  Relevant documents discuss arguments about prescription-drug advertising.
- Query: `Liệu năng lượng tái tạo có thể thay thế nhiên liệu hóa thạch một cách hiệu quả?`
  Relevant documents provide debate passages about renewable energy replacing fossil fuels.
- Query: `Những người phạm tội đã mãn hạn tù có được phép bỏ phiếu không?`
  Relevant documents argue about voting rights after imprisonment.
- Query: `Có nên ban hành thêm các luật kiểm soát súng?`
  Relevant documents discuss arguments for or against additional gun-control laws.
