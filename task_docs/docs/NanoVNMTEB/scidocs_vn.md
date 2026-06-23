# NanoVNMTEB / scidocs_vn

## Overview

`scidocs_vn` is the Vietnamese NanoVNMTEB version of SciDocs retrieval. SciDocs was introduced with SPECTER as a scientific document-level benchmark using citation, co-citation, recommendation, and related-paper signals. In this VN-MTEB split, translated paper titles or short scientific descriptions are used as queries, and translated scientific abstracts are candidate documents.

The Nano split contains 200 queries, 10,000 documents, and 988 positive qrels. Every query has multiple positives: the average is 4.94, the median is 5, and each query has between 3 and 5 positives. Queries average 73.355 characters, while documents average 1,226.7277 characters. This is one of the hardest NanoVNMTEB retrieval tasks: absolute scores are low, and `reranking_hybrid` is only slightly ahead of dense on nDCG@10 and recall@100. The task measures related-paper retrieval, not answer lookup.

## Details

### What the Original Data Measures

SciDocs evaluates scientific document representations across document-level tasks. Citation and co-citation signals are used as proxies for relatedness, and the benchmark includes recommendation-style matching. Unlike QA retrieval, relevance is often based on scientific relationship: similar method, dataset, application, citation context, or topic.

The Vietnamese version translates scientific titles and abstracts. Technical terms, datasets, algorithms, software names, and domain phrases often remain partly unchanged. A relevant document may not share many exact words with the query, because citation-relatedness can reflect methodology or research context rather than direct wording.

### Observed Data Profile

The task has 988 positive qrels across 200 queries. Every query is multi-positive, with a minimum of 3 and maximum of 5 positives. This fixed small positive set makes the benchmark a related-paper ranking task: the system should retrieve several relevant scientific documents for each query.

Documents are long abstracts. Queries are short paper titles or short scientific descriptions. Examples include Android malware behavior analysis, semantic dictionary linkage to WordNet, cloud hardware reliability, daily activity recognition, and virtual learning environments. These topics span computing, language resources, systems, vision, education technology, and other scientific areas.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.1613400598, hit@10 of 0.5200, and recall@100 of 0.3805668016 with a top-500 candidate set. The low nDCG indicates that exact lexical matching is a weak signal for this task. Scientific abstracts can share terms without being citation-related, and related papers may use different terminology.

BM25 still provides some useful anchors, especially for rare technical terms, datasets, algorithms, and system names. However, it often retrieves same-field but non-relevant papers. Citation-style relevance requires matching research intent and context, not only keywords.

### Dense Evaluation Profile

Dense retrieval with `harrier-oss-270m` reaches nDCG@10 of 0.2028299676, hit@10 of 0.5800, and recall@100 of 0.4564777328. It improves over BM25, showing that semantic representations help with related-paper retrieval. The improvement is meaningful but still leaves low absolute performance.

Dense retrieval can connect papers with similar methods or application domains even when terms differ. Its limitation is that generic semantic similarity does not fully capture citation intent. Papers may be topically similar but not part of the same research context, or citation-related despite limited surface similarity.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reaches nDCG@10 of 0.2038882997, hit@10 of 0.5650, and recall@100 of 0.4676113360. The top-100 candidate pool has mean candidate count 100.13, with 26 safeguard-positive rows and 26 rows containing 101 candidates. Hybrid retrieval is slightly best on nDCG@10 and recall@100, while dense has the best hit@10.

The small differences show that neither lexical nor general dense retrieval solves the task. Sparse evidence helps with technical anchors, and dense retrieval helps with semantic relatedness, but citation-style relevance likely requires domain-specific scientific document training. Hybrid search improves coverage a little, but the top ranks remain difficult.

### Metric Interpretation for Model Researchers

This task should be read as a low-score, high-difficulty related-paper benchmark. Every query has several positives, so recall@100 matters. However, because there are only 3 to 5 positives, nDCG@10 also reflects whether the model can place the most related papers near the top.

The relative ordering is modest: dense improves over BM25; hybrid barely improves over dense on nDCG and recall. Model researchers should not overinterpret small score gaps. The more important signal is that general retrieval methods struggle with citation and recommendation-style relevance.

### Query and Relevance Type Tendencies

Queries are scientific titles or concise research descriptions. Relevant documents are related scientific abstracts, often linked by method, task, domain, or citation context. Examples include malware analysis, Semantic Web vocabularies, cloud reliability, activity recognition, and virtual learning environments.

Relevance is not answerability or duplicate status. A relevant document may be a related work, a cited method, a paper in the same research cluster, or a paper useful for recommendation. This makes the task closer to scientific literature discovery than question answering.

### Representative Failure Modes

BM25 can retrieve papers sharing a keyword but unrelated in citation context. Dense retrieval can retrieve semantically similar abstracts that are not actually relevant by SciDocs signals. Hybrid retrieval can still fail when technical keywords and broad semantics point to same-field distractors.

Another failure mode is missing methodology. Two papers may be related because they share an evaluation setting, algorithmic approach, dataset, or citation neighborhood, even if abstracts use different surface vocabulary. General-purpose embeddings may not encode this structure.

### Training Data That May Help

Useful training data includes non-overlapping SciDocs signals, scientific citation pairs, co-citation pairs, paper recommendation logs, and translated scientific abstract retrieval data. Multi-positive training is appropriate because every query has multiple related documents.

Synthetic data should create related-paper queries from scientific abstracts, but it should include same-field hard negatives. Generated labels should reflect shared methods, datasets, applications, or citation rationale rather than only topical similarity.

### Model Improvement Notes

The main improvement direction is scientific document representation learning. Citation-informed or co-citation-informed training is likely more useful than generic QA data. Sparse features should preserve technical names, while dense representations should encode method, task, domain, and research context.

Error analysis should group failures by same-keyword distractors, same-domain but unrelated papers, missed method links, and translation of technical terms. This task is a strong diagnostic for research-paper recommendation quality.

## Example Data

| Query | Positive document |
| --- | --- |
| Phân tích hành vi của mã độc Android [36 chars] | Về chứng nhận ứng dụng điện thoại di động nhẹ Người dùng đã bắt đầu tải về một số lượng ngày càng lớn các ứng dụng cho điện thoại di động để đáp ứng với sự tiến bộ trong các thiết bị cầm tay và mạng không dây. Số lượng ứng dụng tăng lên làm tăng thêm khả năng cài đặt các chương trình độc hại và virus máy tính tương tự. Trong bài báo này, chúng tôi đề xuất dịch vụ bảo mật Kirin cho Android, thực hiện chứng nhận nhẹ của các ứng dụng để giảm thiểu phần mềm độc hại tại thời điểm cài đặt. Chứng nhận Kirin sử dụng các quy tắc bảo mật, đó là các mẫu được thiết kế để khớp bảo thủ các thuộc tính không mong muốn trong cấu hình bảo mật được đóng gói với các ứng dụng. Chúng tôi sử dụng một biến thể của kỹ thuật kỹ thuật yêu cầu bảo mật để thực hiện phân tích bảo mật sâu rộng của Android để tạo ra một tập hợp các quy tắc phù hợp với đặc điểm của phần mềm độc hại. Trong một mẫu 311 các ứng dụng phổ biến nhất được tải xuống từ Chợ chính thức của Android, Kirin và các quy tắc của chúng tôi tìm thấy 5... [1,000 / 1,361 chars] |
| Liên kết một từ điển ngữ nghĩa với Wordnet và chuyển đổi sang Wordnet-LMF [73 chars] | Học cách bản đồ giữa các từ vựng trên Web ngữ nghĩa Các ngữ nghĩa học đóng một vai trò nổi bật trong Semantic Web. Chúng cho phép xuất bản dữ liệu có thể hiểu được bởi máy tính, mở ra nhiều cơ hội để xử lý thông tin tự động. Tuy nhiên, do tính phân tán của Semantic Web, dữ liệu trên nó sẽ xuất phát từ nhiều nguồn khác nhau. Xử lý thông tin giữa các ngữ nghĩa học không có khả năng mà không biết được các bản đồ ngữ nghĩa giữa các thành phần của chúng. Việc tìm kiếm thủ công các bản đồ này là mệt mỏi, dễ sai và rõ ràng không khả thi ở quy mô web. Do đó, việc phát triển các công cụ hỗ trợ quá trình bản đồ ngữ nghĩa là rất quan trọng đối với sự thành công của Semantic Web.Chúng tôi mô tả một hệ thống gọi là "keo", sử dụng các kỹ thuật học máy để tìm ra các bản đồ như vậy. Cho hai ngữ nghĩa học, đối với mỗi khái niệm trong một ngữ nghĩa học, keo tìm ra khái niệm tương tự nhất trong ngữ nghĩa học còn lại. Chúng tôi đưa ra các định nghĩa xác suất hợp lý cho nhiều phép đo độ tương tự thực tế, v... [1,000 / 2,024 chars] |
| Mô tả tính độ tin cậy của phần cứng điện toán đám mây [53 chars] | Xu hướng thất bại trong một quần thể ổ đĩa lớn Được ước tính rằng trên 90% thông tin mới được sản xuất ra trên thế giới đang lưu trữ trên các phương tiện từ tính, hầu hết là trên ổ cứng. Mặc dù sự quan trọng của họ, có tương đối ít công trình đã được xuất bản về các mô hình hỏng hóc của ổ đĩa và các yếu tố chủ chốt ảnh hưởng đến tuổi thọ của chúng. Hầu hết dữ liệu có sẵn hoặc dựa trên việc suy diễn từ các thí nghiệm lão hóa tăng tốc hoặc từ các nghiên cứu thực địa quy mô tương đối khiêm tốn. Hơn nữa, các nghiên cứu quy mô lớn hiếm khi có cơ sở hạ tầng để thu thập các tín hiệu y tế từ các thành phần đang hoạt động, điều đó là thông tin quan trọng cho phân tích lỗi chi tiết. Chúng tôi trình bày dữ liệu thu thập được từ quan sát chi tiết một dân số ổ đĩa lớn trong triển khai dịch vụ Internet sản xuất. Dân số quan sát lớn nhiều lần so với các nghiên cứu trước đây. Ngoài việc trình bày thống kê hư hỏng, chúng tôi phân tích sự tương quan giữa các lỗi và một số tham số được tin tưởng nói chun... [1,000 / 1,462 chars] |

### Source Reference Table

| Source | Role |
|---|---|
| SPECTER / SciDocs | Original scientific document representation and evaluation benchmark |
| SciDocs dataset page | Official dataset context |
| BEIR | Retrieval benchmark framing |
| VN-MTEB | Vietnamese benchmark collection using translated retrieval tasks |
| GreenNode dataset card | Public dataset entry for this Vietnamese split |

### Representative Snippets

- Query: `Phân tích hành vi của mã độc Android`
  Relevant documents include related mobile security or malware-analysis papers.
- Query: `Liên kết một từ điển ngữ nghĩa với Wordnet và chuyển đổi sang Wordnet-LMF`
  Relevant documents concern semantic resources, WordNet, or vocabulary mapping.
- Query: `Mô tả tính độ tin cậy của phần cứng điện toán đám mây`
  Relevant documents discuss reliability and failure trends in computing hardware.
- Query: `Nhận diện thói quen hàng ngày qua các hoạt động`
  Relevant documents include activity recognition or detection methods.
- Query: `VELNET (Môi trường ảo cho học tập mạng)`
  Relevant documents concern virtual learning environments or educational technology.
