# NanoVNMTEB / argu_ana_vn

## Overview

`argu_ana_vn` is a Vietnamese counterargument retrieval task from NanoVNMTEB. The query is a long translated debate argument, and the relevant document is the best opposing counterargument. Each query has one positive among 8,674 candidate arguments. The task is difficult because the relevant document must be topically related but stance-opposed. Dense retrieval is the strongest top-rank profile, `reranking_hybrid` gives the best recall@100, and BM25 is weaker because lexical overlap tends to retrieve same-topic arguments without checking argumentative stance.

## Details

### What the Original Data Measures

ArguAna was introduced as a counterargument retrieval benchmark: given an argument, a system must retrieve a strong counterargument without prior topic knowledge. The task requires both topic matching and stance opposition.

VN-MTEB translates the source task into Vietnamese. This Nano split is therefore a translated Vietnamese benchmark, not a natively authored Vietnamese debate corpus. It still preserves the core retrieval challenge: same-topic similarity is not enough.

### Observed Data Profile

The Nano split contains 199 queries, 8,674 documents, and 199 positive qrel rows. Every query has exactly one positive. Queries average 1,183.88 characters, while documents average 1,080.34 characters.

Example topics include organ donation, animal testing, airport expansion and pollution, baseball collisions, religious hate speech, BBC funding, blasphemy, hip-hop censorship, and meat eating. The positive document usually shares the topic but presents the opposing position.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.2742, hit@10 of 0.6030, and recall@100 of 0.9548. BM25 can find same-topic arguments because long queries and documents share many content words.

The weakness is stance. A same-topic argument with the wrong argumentative role receives no credit. Term frequency does not know whether a passage supports, refutes, or reframes the query argument.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.3698, hit@10 of 0.7889, and recall@100 of 0.9447. Dense retrieval is the strongest early-ranking profile.

This suggests that embedding similarity captures argument-level semantics better than lexical overlap. It can connect a claim and a rebuttal even when the counterargument uses different wording or focuses on a different premise.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 4 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.3372, hit@10 of 0.7387, and recall@100 of 0.9799. Hybrid retrieval has the best recall@100 but is weaker than dense retrieval at the top ranks.

The pattern is useful for reranking. Sparse matching expands coverage across the same debate topic, while dense retrieval better orders the most relevant counterargument. A stance-aware reranker should benefit from the hybrid pool.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures how early the target counterargument appears, hit@10 measures whether it appears in the first ten candidates, and recall@100 measures reranker availability.

For `argu_ana_vn`, high recall can still include many same-topic wrong-stance candidates. A strong system should model rebuttal relation, not only topical similarity.

### Query and Relevance Type Tendencies

Queries and documents are long Vietnamese argument paragraphs. Relevant documents are counterarguments that oppose or challenge the query's stance. Candidate documents often share the same policy, ethical, or social topic.

Relevance is counterargument fit. A passage that agrees with the query or discusses the topic from a neutral angle is not the positive target.

### Representative Failure Modes

Common failures include retrieving same-stance arguments, matching broad topic terms without rebuttal, overranking arguments with shared examples, and missing translated paraphrases. BM25 is vulnerable to topic-only overlap; dense retrieval can still confuse opposition with relatedness.

### Training Data That May Help

Useful training data includes non-overlapping Vietnamese argument-counterargument pairs, translated ArguAna training material with test overlap removed, Vietnamese debate or stance-labeled forum data, and multilingual argument-mining corpora adapted to Vietnamese. Evaluation queries, positives, and qrels should be excluded.

### Model Improvement Notes

Models should encode stance, claim, premise, and rebuttal relation. Hard negatives should be same-topic arguments with the same or ambiguous stance. Dense retrieval is the best direct ranker, while hybrid retrieval is useful for high-recall reranking.

## Example Data

| Query | Positive document |
| --- | --- |
| Quyền tự quyết cá nhân là quyền con người cơ bản, ngang hàng với quyền sống. Nguyên tắc cơ bản của c... [100 / 1,001 chars] | triết lý y tế đạo đức nhà cho phép quyên góp các cơ quan quan trọng ngay cả chi phí Con người cũng là một sinh vật xã hội. Trong khi chúng ta có quyền đối với cơ thể của mình, chúng ta cũng có nghĩa v... [200 / 818 chars] |
| Động vật thí nghiệm được đối xử tốt Động vật dùng trong nghiên cứu nói chung không bị đau khổ. Mặc d... [100 / 559 chars] | thú vật khoa học khoa học đại chúng thử nghiệm trên động vật Chỉ vì một con vật được đối xử tốt khi nó được nuôi dưỡng không ngăn chặn nỗi đau rất thực tế trong khi thử nghiệm. Quy tắc nghiêm ngặt và... [200 / 353 chars] |
| Việc xây dựng đường băng thứ ba sẽ gây ra vấn đề tiếng ồn và ô nhiễm. Mật độ dân cư cao trong khu vự... [100 / 1,302 chars] | kinh tế môi trường chung khí hậu môi trường chung ô nhiễm nhà ở Việc bổ sung đường băng không nhất thiết dẫn đến sự gia tăng đáng kể về ô nhiễm tiếng ồn, vì điều đó phụ thuộc vào vị trí đặt đường băng... [200 / 1,124 chars] |
| Những va chạm là một phần của trò chơi. Đầu tiên, những va chạm là một phần truyền thống của bóng ch... [100 / 2,102 chars] | đội thể thao tin rằng giải bóng chày nên tiếp tục cho phép va chạm Những va chạm ít xảy ra trong trò chơi hơn những gì mọi người nghĩ. Ý tưởng rằng những va chạm đã tồn tại từ lâu trong trò chơi là mộ... [200 / 1,659 chars] |
| Không có quyền không bị xúc phạm, việc thực thi những gì được cho là chấp nhận được để suy nghĩ hoặc... [100 / 1,230 chars] | Nhà ở khác biệt sống sẽ trừng phạt bài phát biểu thù hận tôn giáo Đây chỉ là một huyền thoại. Xã hội thường thường lập pháp để ngăn ngừa hành vi phạm tội bằng cách hạn chế những gì có thể nói hoặc làm... [200 / 675 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Retrieval of the Best Counterargument without Prior Topic Knowledge | 2018 | ACL paper | [https://aclanthology.org/P18-1023/](https://aclanthology.org/P18-1023/) |
| VN-MTEB: Vietnamese Massive Text Embedding Benchmark | 2026 | ACL paper | [https://aclanthology.org/2026.findings-eacl.86/](https://aclanthology.org/2026.findings-eacl.86/) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| GreenNode/arguana-vn |  | dataset card | [https://huggingface.co/datasets/GreenNode/arguana-vn](https://huggingface.co/datasets/GreenNode/arguana-vn) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| A Vietnamese argument defends personal autonomy in organ donation. | A counterargument emphasizes social obligations and medical ethics. |
| A claim says laboratory animals are generally treated well. | A counterargument says good housing does not remove pain during experiments. |
| A claim argues a third runway would increase noise and pollution. | A counterargument argues added runway capacity need not greatly increase noise pollution. |
| A claim says collisions are a traditional part of baseball. | A counterargument challenges whether collisions are as common or necessary as claimed. |
| A claim opposes restrictions on offensive religious speech. | A counterargument defends limits on harmful or hateful religious speech. |
