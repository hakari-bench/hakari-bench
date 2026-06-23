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
| Quyền tự quyết cá nhân là quyền con người cơ bản, ngang hàng với quyền sống. Nguyên tắc cơ bản của con người là mỗi người sinh ra đều có tính chủ thể. Vì vậy chúng tôi tin rằng mọi người đều có quyền đối với cơ thể của mình và do đó có quyền ra quyết định về nó. Điều này là bởi vì chúng tôi nhận thức rằng bất kể những quyết định nào mà chúng tôi đưa ra về cơ thể của mình xuất phát từ kiến thức mà chúng tôi nắm giữ về sở thích của chính mình. Không ai có thể nói cho chúng tôi biết cách đánh giá c... [500 / 1,001 chars] | triết lý y tế đạo đức nhà cho phép quyên góp các cơ quan quan trọng ngay cả chi phí Con người cũng là một sinh vật xã hội. Trong khi chúng ta có quyền đối với cơ thể của mình, chúng ta cũng có nghĩa vụ đối với những người xung quanh. Nếu chúng ta chọn chấm dứt cuộc sống của mình, chúng ta phải cân nhắc hậu quả đối với những người phụ thuộc vào chúng ta về thể xác hay tinh thần. Chúng ta có thực sự có thể đánh giá liệu cuộc sống của chính mình có ít ý nghĩa hơn so với người nhận không? Con người cũng thường đưa ra quyết định mà không có tất cả thông tin liên quan. Quyết định mà chúng ta đưa ra có thể hoàn toàn thiếu hiểu biết ngay cả khi chúng ta tin rằng mình đã có đầy đủ thông tin. Một phần vấn đề ở đây là tất cả các hậu quả của quyết định của chúng ta không bao giờ có thể được hiểu hay dự đoán toàn diện. [818 chars] |
| Động vật thí nghiệm được đối xử tốt Động vật dùng trong nghiên cứu nói chung không bị đau khổ. Mặc dù chúng có thể bị đau, nhưng nói chung chúng được cho thuốc giảm đau, và khi chúng bị hạ sát thì việc này được thực hiện một cách nhân đạo. [16] Chúng được chăm sóc, bởi vì những con vật khỏe mạnh có kết quả thí nghiệm tốt hơn. Những con vật này sống tốt hơn so với cuộc sống hoang dã của chúng. Miễn là động vật được đối xử tốt, không nên có sự phản đối về mặt đạo lý đối với nghiên cứu trên động vậ... [500 / 559 chars] | thú vật khoa học khoa học đại chúng thử nghiệm trên động vật Chỉ vì một con vật được đối xử tốt khi nó được nuôi dưỡng không ngăn chặn nỗi đau rất thực tế trong khi thử nghiệm. Quy tắc nghiêm ngặt và thuốc giảm đau không giúp ích gì vì sự thiếu đau đớn không thể đảm bảo – nếu chúng tôi biết những gì sẽ xảy ra, chúng tôi sẽ không thực hiện thí nghiệm. [353 chars] |
| Việc xây dựng đường băng thứ ba sẽ gây ra vấn đề tiếng ồn và ô nhiễm. Mật độ dân cư cao trong khu vực xung quanh sân bay Heathrow cho thấy đây không phải là địa điểm lý tưởng để xây dựng một sân bay lớn hơn. Việc tăng sức chứa ở một khu vực có mật độ dân cư thấp thay vì cố gắng làm điều đó trong khu vực bị giới hạn bởi các khu vực đô thị liền kề là một ý tưởng hợp lý hơn. Việc mở rộng sân bay Heathrow sẽ khiến cho khoảng 700.000 người sống dưới đường bay phải đối mặt với nhiều tiếng ồn hơn. Theo... [500 / 1,302 chars] | kinh tế môi trường chung khí hậu môi trường chung ô nhiễm nhà ở Việc bổ sung đường băng không nhất thiết dẫn đến sự gia tăng đáng kể về ô nhiễm tiếng ồn, vì điều đó phụ thuộc vào vị trí đặt đường băng. Nếu đường băng được xây dựng ở phía Tây của vị trí hiện tại thì những chiếc máy bay sẽ bay qua các khu vực không có dân cư bởi vì chúng sẽ bay trên M25, Khu công nghiệp Poyle, Hồ chứa nước Wraysbury và một phần của Stanwell Moor. Mặt khác tất cả các đường băng có thể được di chuyển sang phía bên kia của M25 và bố trí gần nhau, giảm tiếng ồn xuống mức thấp hơn so với mức hiện tại ngay cả khi có ba hoặc bốn đường băng. [1] Do đó, lập luận về khiếu nại tiếng ồn là không đúng. Không có sân bay nào lại im lặng hoàn toàn nhưng với đề xuất tăng số lượng Airbus A380, chỉ tạo ra một nửa tiếng ồn khi cất cánh và chỉ tạo ra một phần tư tiếng ồn khi hạ cánh so với Boeing 747, lập luận về tiếng ồn thực sự mất đi rất nhiều điểm. [2] Chúng ta cũng nên nhớ rằng việc xây dựng thêm đường băng thứ ba sẽ gi... [1,000 / 1,124 chars] |

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
