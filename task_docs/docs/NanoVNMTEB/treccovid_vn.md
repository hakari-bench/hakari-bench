# NanoVNMTEB / treccovid_vn

## Overview

`treccovid_vn` is the Vietnamese NanoVNMTEB version of TREC-COVID, a pandemic-era biomedical information retrieval benchmark built over the rapidly growing CORD-19 literature collection. VN-MTEB translates COVID-19 topics and scientific documents into Vietnamese. Queries are biomedical information needs about SARS-CoV-2, COVID-19 treatments, transmission, immunity, diagnostics, mechanisms, and clinical or public-health guidance.

The Nano split contains 44 queries, 10,000 candidate documents, and 4,076 positive qrels. Every query has many positives: the average is 92.636364, the median is 100, and the maximum is 100. Queries average 70.545455 characters, while documents average 1,315.6452 characters. Dense retrieval is strongest on nDCG@10 and hit@10, while `reranking_hybrid` has the best recall@100. Absolute recall remains low because each topic has a very large relevant set, making broad biomedical coverage difficult.

## Details

### What the Original Data Measures

TREC-COVID was constructed to support information retrieval over COVID-19 scientific literature during the early pandemic. The collection used CORD-19 documents and evolving topic sets with relevance judgments across multiple rounds. The task reflects real biomedical search needs under rapidly changing evidence.

The Vietnamese version translates topics and documents but preserves biomedical terminology, virus names, treatment names, study populations, outcomes, and uncertainty language. Relevance is broad: many papers can be relevant to one topic, and usefulness may depend on treatment evidence, mechanism, public-health implication, or clinical guidance.

### Observed Data Profile

The split has 44 queries and 4,076 positives. Every query is multi-positive, with at least 28 positives and usually 100 positives. This is an extreme many-positive scientific retrieval task. Retrieving one relevant paper is easy compared with covering the relevant literature.

Documents are scientific abstracts or article summaries. They may discuss mechanisms, interventions, epidemiology, diagnostics, modeling, vaccines, masks, social distancing, asymptomatic infection, or drug repurposing. The model must retrieve useful biomedical evidence across a large and diverse relevant set.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2810932253, hit@10 of 0.7727272727, and recall@100 of 0.2058390579 with a top-500 candidate set. Sparse retrieval can use exact terms such as SARS-CoV-2, COVID-19, remdesivir, mRNA, cytokine storm, masks, or social distancing, but the scores show that lexical matching alone is weak for ranking broad biomedical evidence.

The low recall@100 is especially important. Since each query has many positives, BM25 may retrieve some obvious exact-term documents while missing much of the relevant literature that uses different terminology, broader coronavirus language, or related clinical concepts.

### Dense Evaluation Profile

Dense retrieval with `harrier-oss-270m` reaches nDCG@10 of 0.3750221655, hit@10 of 0.9772727273, and recall@100 of 0.2463199215. It is strongest on top-rank metrics and substantially improves hit@10 over BM25. Dense retrieval is better at connecting topic descriptions to biomedical abstracts that express the same need without exact wording.

Dense retrieval helps for questions about immunity, transmission, interventions, mechanisms, and clinical guidance. Its recall@100 is still low relative to the number of positives, which suggests that general embeddings struggle to cover broad biomedical topics with many relevant documents. Domain adaptation and literature-search training would likely help.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reaches nDCG@10 of 0.3550643016, hit@10 of 0.8863636364, and recall@100 of 0.2588321884. The top-100 candidate pool has exactly 100 candidates per query and no safeguard-expanded rows. Hybrid retrieval has the best recall@100, but dense retrieval has better top-rank quality.

This pattern shows that sparse evidence contributes coverage for exact biomedical terms, while dense retrieval gives better ranking near the top. Hybrid retrieval recovers a slightly larger fraction of the relevant literature, but it can rank exact-term distractors above stronger evidence. A biomedical reranker would need to combine both channels while scoring evidence usefulness.

### Metric Interpretation for Model Researchers

Hit@10 can be misleading because every topic has many positives. Dense retrieval nearly saturates hit@10, but recall@100 remains under 0.25. The key challenge is not just finding one relevant paper; it is covering a broad evidence set and ranking useful documents high.

The metric ordering shows dense retrieval as the best user-facing first-page ranker and hybrid retrieval as the best candidate-coverage condition. Researchers should treat this as a many-positive biomedical literature search benchmark and evaluate both top evidence quality and coverage.

### Query and Relevance Type Tendencies

Queries ask about vaccines, masks, social distancing, drug repurposing, asymptomatic infection, cytokine storms, weather effects, immunity, diagnostics, and clinical guidance. Relevant documents can be original studies, reviews, modeling papers, or clinical summaries. Many positives are related at the topic level rather than as a single answer sentence.

Relevance is scientific usefulness for the topic. A paper can be relevant if it provides evidence, background, mechanism, or guidance related to the information need. This makes the task broader than fact verification and harder than single-answer QA.

### Representative Failure Modes

BM25 can over-rank documents that repeat COVID-19 terms but do not address the specific information need. Dense retrieval can over-rank broad pandemic summaries over targeted studies. Hybrid retrieval can improve coverage but still suffer when exact terms dominate biomedical usefulness.

Another failure mode is missing uncertainty and study type. Pandemic literature includes preliminary findings, reviews, clinical trials, modeling studies, and public-health guidance. A strong retriever should distinguish these contexts when ranking evidence.

### Training Data That May Help

Useful training data includes non-overlapping TREC-COVID rounds and judgments, CORD-19 biomedical retrieval pairs, COVID-19 literature search data, biomedical QA, and translated scientific retrieval with overlap removed. Multi-positive training is essential because each topic has many relevant papers.

Synthetic data should generate Vietnamese biomedical information needs from non-evaluation COVID-19 abstracts. Hard negatives should share disease or treatment terms but differ in outcome, population, or evidence type.

### Model Improvement Notes

The main improvement direction is biomedical literature retrieval with high-coverage ranking. Sparse retrieval should preserve exact virus, drug, intervention, and outcome terms. Dense retrieval should model broader biomedical intent. Rerankers should score evidence usefulness, study type, and topic specificity.

Error analysis should separate exact-term misses, broad-topic false positives, outcome mismatch, intervention mismatch, and evidence-type mismatch. Because TREC-COVID reflects rapidly evolving medical literature, benchmark relevance should not be treated as current clinical advice.

## Example Data

| Query | Positive document |
| --- | --- |
| Chúng ta biết gì về vắc xin mRNA cho vi-rút SARS-CoV-2? [55 chars] | Chống dịch COVID-19: Đánh giá nhanh chẩn đoán, liệu pháp và vắc xin Đại dịch COVID-19 do một chủng virus corona mới, SARS-CoV-2, đã lây nhiễm hơn 4.9 triệu người và gây ra trên 300.000 ca tử vong trên toàn cầu. Sự lan truyền nhanh chóng của virus và sự gia tăng đột biến số ca bệnh đòi hỏi phải phát triển khẩn cấp các phương pháp chẩn đoán chính xác, các phương pháp điều trị hiệu quả và các loại vắc xin. Ở đây, chúng tôi tổng quan tiến bộ trong việc phát triển các phương pháp chẩn đoán, liệu pháp và vắc xin cho SARS-CoV-2 tập trung vào các thử nghiệm lâm sàng hiện tại và những thách thức của chúng. Đối với chẩn đoán, xét nghiệm khuếch đại axit nucleic vẫn là phương pháp chẩn đoán chính xác nhất để xác nhận phòng thí nghiệm nhiễm SARS-CoV-2, trong khi xét nghiệm kháng thể huyết thanh được sử dụng để hỗ trợ truy tìm tiếp xúc, nghiên cứu dịch tễ học và đánh giá vắc xin. Cách ly virus không được khuyến nghị cho các thủ tục chẩn đoán thông thường do lo ngại về an toàn. Hiện tại, không có thu... [1,000 / 2,093 chars] |
| Những chiếc mặt nạ nào là tốt nhất để phòng ngừa nhiễm Covid-19? [64 chars] | Đại dịch SARS, MERS và virus corona chủng mới (COVID-19), các mối đe dọa sức khỏe toàn cầu mới nhất và lớn nhất: chúng ta đã học được gì? MỤC ĐÍCH: Cung cấp tổng quan về ba loại virus corona gây chết người và xác định các lĩnh vực cần cải thiện trong kế hoạch chuẩn bị cho tương lai, cũng như cung cấp đánh giá quan trọng về các yếu tố nguy cơ và các biện pháp có thể thực hiện để ngăn chặn sự lây lan của chúng, sử dụng bài học rút ra từ hai đợt bùng phát virus corona trước đó, cũng như báo cáo ban đầu từ dịch bệnh virus corona mới (COVID-19) hiện tại ở Vũ Hán, Trung Quốc. PHƯƠNG PHÁP: Sử dụng trang web của Trung tâm Kiểm soát và Phòng ngừa Dịch bệnh (CDC, Hoa Kỳ) và một đánh giá toàn diện các tài liệu trên PubMed, chúng tôi thu thập được thông tin về các dấu hiệu và triệu chứng lâm sàng, điều trị và chẩn đoán, phương thức truyền nhiễm, phương pháp phòng ngừa và các yếu tố nguy cơ đối với Hội chứng Hô hấp Trung Đông (MERS), Hội chứng Hô hấp Sâu sắc (SARS) và COVID-19. Các so sánh giữa các... [1,000 / 2,092 chars] |
| có phải giãn cách xã hội đã ảnh hưởng đến việc làm chậm sự lây lan của COVID-19 không? [86 chars] | Tăng cường phát hiện kết hợp với giãn cách xã hội và quy hoạch năng lực y tế giảm gánh nặng các trường hợp và tử vong do COVID-19: Nghiên cứu khái niệm bằng mô hình mô phỏng tính toán ngẫu nhiên Mục tiêu: Trong bối cảnh không có vắc-xin, đại dịch COVID-19 đang được kiểm soát thông qua các biện pháp phi dược phẩm được gọi là giãn cách xã hội (SC). Tuy nhiên, liệu SC có đủ để làm giảm độ dốc của đường cong dịch bệnh hay không vẫn còn là vấn đề gây tranh cãi. Bằng cách sử dụng Mô hình Mô phỏng Tính toán Khác ngẫu nhiên, chúng tôi đã nghiên cứu tác động của việc tăng cường SD, giường bệnh viện và tỷ lệ phát hiện COVID-19 trong việc ngăn ngừa các trường hợp và tử vong do COVID-19. Thiết kế và phương pháp nghiên cứu: Mô hình Mô phỏng Khác ngẫu nhiên được xây dựng bằng gói EpiModel trong R. Là một nghiên cứu khái niệm, chúng tôi đã thực hiện mô phỏng trên Kasaragod, quận bị ảnh hưởng nhiều nhất ở Kerala. Chúng tôi đã thêm 3 khoang vào mô hình SEIR để có được mô hình SEIQHRF (Dễ bị nhiễm - Tiế... [1,000 / 1,616 chars] |

### Source Reference Table

| Source | Role |
|---|---|
| TREC-COVID | Original pandemic information retrieval test collection |
| TREC-COVID challenge page | Official challenge context |
| BEIR | Retrieval benchmark framing |
| VN-MTEB | Vietnamese benchmark collection using translated retrieval tasks |
| GreenNode dataset card | Public dataset entry for this Vietnamese split |

### Representative Snippets

- Query: `Chúng ta biết gì về vắc xin mRNA cho vi-rút SARS-CoV-2?`
  Relevant documents discuss diagnostics, therapies, vaccines, or SARS-CoV-2 vaccine development.
- Query: `Những chiếc mặt nạ nào là tốt nhất để phòng ngừa nhiễm Covid-19?`
  Relevant documents include evidence about masks or prevention of coronavirus infection.
- Query: `có phải giãn cách xã hội đã ảnh hưởng đến việc làm chậm sự lây lan của COVID-19 không?`
  Relevant documents discuss social distancing, case burden, and transmission reduction.
- Query: `Protein SARS-CoV-2 có tương tác với protein của con người...`
  Relevant documents discuss viral proteins, host interactions, and drug repurposing.
- Query: `Những gì chúng ta biết về những người bị nhiễm Covid-19 nhưng không có triệu chứng?`
  Relevant documents discuss asymptomatic infection, transmission, or observed outbreaks.
