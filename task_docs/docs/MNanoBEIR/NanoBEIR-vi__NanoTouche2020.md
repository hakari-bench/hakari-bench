# MNanoBEIR / NanoBEIR-vi / NanoTouche2020

## Overview

NanoTouche2020 in the Vietnamese NanoBEIR slice is an argument retrieval task derived from Touche 2020. The queries are Vietnamese translated controversial questions, and the corpus contains Vietnamese translated argument passages. The retrieval goal is to find passages that argue about the requested issue, often from either the pro or con side. This makes the task useful for evaluating Vietnamese debate retrieval, stance-adjacent relevance, and ranking over long argumentative text.

## Details

### What the Original Data Measures

Touche 2020 evaluates retrieval for controversial information needs. In this setting, a model receives a debate-style question and must retrieve passages that contain useful arguments about that issue. Relevance is broader than fact lookup: passages can be relevant because they present reasons, examples, policy claims, or normative arguments connected to the question.

The Vietnamese translated version preserves the controversial-question style while adding multilingual argumentation challenges. The model must match short questions to long passages that may use rhetorical framing, examples, and stance-specific vocabulary. A strong retriever should find arguments that address the question, not just any text mentioning the topic.

### Observed Data Profile

The task contains 49 queries, 5,745 documents, and 932 relevance judgments. Every query is multi-positive, with an average of 19.02 positives per query. The minimum is 6, the median is 19.0, the maximum is 32, and all 49 queries are multi-positive.

Queries average 52.86 characters, while documents average 1,712.75 characters. The query is usually a concise debate question, while the relevant passages are long argument texts. This makes the benchmark sensitive to both broad topical coverage and fine matching to the debated aspect.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.5444, hit@10 of 0.9796, and recall@100 of 0.7725 using the top-500 BM25 candidate subset. This is a strong lexical profile. Controversial questions often include distinctive topic terms such as homework, prescription drugs, vaccines, abortion, or standardized tests, and those terms appear repeatedly in relevant arguments.

BM25 is especially good at finding at least one argument near the top. The challenge is not simply locating the topic; it is ranking many relevant arguments and covering different formulations. Lexical matching can over-rank passages that mention the debate topic without addressing the precise question or useful argument dimension.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.4636, hit@10 of 0.9592, and recall@100 of 0.7446. Dense retrieval remains strong in absolute terms, but it is weaker than BM25 on this task. This suggests that general embedding similarity captures broad debate topicality but does not outperform repeated lexical anchors in the long argument passages.

The dense weakness is important for model researchers. Argument retrieval often contains long texts with many semantically related claims, and dense similarity can retrieve passages that feel topically close but are less directly relevant to the exact debate question. Domain-specific argument training may be needed to improve this behavior.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.5368, hit@10 of 1.0000, and recall@100 of 0.7811. It uses exactly 100 candidates per query, with no safeguard rows. The hybrid profile has the best hit@10 and recall@100, while BM25 has a slightly higher nDCG@10.

This shows that hybrid search is the best candidate pool for this task. BM25 supplies strong topic-term matching, and dense retrieval adds coverage for arguments expressed with different wording. The result is not a clean dense win: the task remains highly lexical, but hybrid retrieval improves visibility and candidate completeness.

### Metric Interpretation for Model Researchers

Because every query has many positives, hit@10 is an easy metric compared with nDCG@10 and recall@100. A system can find one argument quickly while still ranking the broader relevant set poorly. nDCG@10 measures whether the first page contains stronger relevant arguments, and recall@100 measures whether downstream reranking can access enough of the argument pool.

The comparison shows that BM25 is very competitive for top ranking, dense retrieval is weaker for these long translated arguments, and reranking_hybrid offers the best coverage. This task is useful for evaluating whether a model can go beyond topic detection toward argument-aware ranking.

### Query and Relevance Type Tendencies

Queries include debate prompts such as whether homework is beneficial, whether prescription drugs should be advertised directly to consumers, whether vaccines should be required for children, whether abortion should be legal, and whether standardized tests improve education. Relevant documents are long passages presenting reasons, examples, policy arguments, or counterarguments.

The task rewards matching the debated issue and the argumentative aspect. A relevant passage may be pro or con, but it must address the question. Passages that merely discuss the topic in passing may be weaker than passages with explicit reasoning.

### Representative Failure Modes

Likely failures include retrieving topic mentions without substantive argument, missing arguments that use indirect phrasing, over-ranking long passages with repeated debate keywords, and failing to distinguish the specific policy question from adjacent moral or factual discussions. BM25 may overvalue repeated terms, while dense retrieval may blur distinct argumentative aspects.

### Training Data That May Help

Useful training data includes Vietnamese debate retrieval, argument mining, stance-aware ranking, controversial-question retrieval, and hard negatives that discuss the same topic but do not answer the specific debate prompt. Multi-positive supervision is important because each query has many relevant arguments.

### Model Improvement Notes

A model targeting this task should preserve strong topic recall while improving argument quality ranking. Sparse systems need good handling of long argumentative passages and repeated topic terms. Dense systems need argument-specific training to avoid broad topical overgeneralization. Hybrid systems are promising as reranking inputs because the observed profile has the best candidate coverage.

## Example Data

| Query | Positive document |
| --- | --- |
| Bài tập về nhà có lợi không? [28 chars] | Đầu tiên, có ba lý do tại sao bài tập về nhà là tuyệt vời và nên tiếp tục trong các trường học hiện đại. 1. Bài tập về nhà hỗ trợ những người học thực hành. Người ta thường chấp nhận rằng có ba loại n... [200 / 3,948 chars] |
| Có nên quảng cáo thuốc theo toa trực tiếp đến người tiêu dùng không? [68 chars] | Nhiều quảng cáo không cung cấp đủ thông tin về hiệu quả của thuốc. Ví dụ, Lunesta được quảng cáo bằng hình ảnh một con bướm bay qua cửa sổ phòng ngủ, trên một người đang ngủ say. Thực tế, Lunesta giúp... [200 / 1,324 chars] |
| Có cần yêu cầu tiêm vắc xin nào cho trẻ em không? [49 chars] | Chưa phải là một trường hợp đầy đủ... Chỉ là một số điểm nhỏ mà tôi đã tổng hợp... Chính phủ không nên có quyền can thiệp vào các quyết định về sức khỏe mà cha mẹ đưa ra cho con cái của họ. 31% cha mẹ... [200 / 3,913 chars] |
| Phá thai có nên hợp pháp không? [31 chars] | Nạo phá thai nên hợp pháp vì nhân cách bắt đầu khi thai nhi trở nên khả thi hoặc sau khi sinh, chứ không phải tại thời điểm thụ thai. Theo Tòa án Tối cao Hoa Kỳ, một người được tính tuổi khi họ ra khỏ... [200 / 284 chars] |
| Các bài kiểm tra chuẩn hóa có cải thiện giáo dục không? [55 chars] | Đã giải quyết: SAT, ACT và các bài kiểm tra tiêu chuẩn khác cung cấp nhiều thông tin hơn về sự chuẩn bị của học sinh trung học cho giáo dục tại các trường cao đẳng và đại học elite hơn là GPA trung họ... [200 / 4,046 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [Touche 2020](https://doi.org/10.1007/978-3-030-58219-7_26) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-vi dataset | [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi) |

Representative query and positive argument snippets:

| Query | Positive document snippet |
| --- | --- |
| Bai tap ve nha co loi khong? | Co ba ly do tai sao bai tap ve nha la tuyet voi va nen tiep tuc trong cac truong hoc... |
| Co nen quang cao thuoc theo toa truc tiep den nguoi tieu dung khong? | Nhieu quang cao khong cung cap du thong tin ve hieu qua cua thuoc... |
| Co can yeu cau tiem vac xin nao cho tre em khong? | Chinh phu khong nen co quyen can thiep vao cac quyet dinh ve suc khoe ma cha me dua ra... |
| Pha thai co nen hop phap khong? | Nao pha thai nen hop phap vi nhan cach bat dau khi thai nhi tro nen kha thi... |
| Cac bai kiem tra chuan hoa co cai thien giao duc khong? | SAT, ACT va cac bai kiem tra tieu chuan khac cung cap nhieu thong tin hon... |
