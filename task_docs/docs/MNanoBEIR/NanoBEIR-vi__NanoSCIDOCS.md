# MNanoBEIR / NanoBEIR-vi / NanoSCIDOCS

## Overview

NanoSCIDOCS in the Vietnamese NanoBEIR slice is a scientific document retrieval task derived from SCIDOCS and the SPECTER evaluation setting. The queries are Vietnamese translated paper-title style texts, and the corpus contains Vietnamese translated scientific abstracts or abstract-like passages. The retrieval goal is to find papers related to the query paper. This makes the task useful for evaluating Vietnamese academic search, citation-style related-document retrieval, and scientific topic matching.

## Details

### What the Original Data Measures

SCIDOCS evaluates scientific document representations over tasks such as citation prediction, co-viewing, co-reading, and recommendation. In BEIR-style retrieval, the task becomes scientific related-document search: a query paper title should retrieve related scientific documents. Relevance is not simply answer containment; it reflects topical, methodological, or citation-neighborhood relatedness.

The Vietnamese translated version adds multilingual scientific terminology challenges. Technical terms may be translated, borrowed, abbreviated, or left partly in English. A strong retriever must match research topics and methods across title-like queries and longer abstract text.

### Observed Data Profile

The task contains 50 queries, 2,210 documents, and 244 relevance judgments. Every query is multi-positive, with an average of 4.88 positives per query. The minimum is 3, the median is 5.0, the maximum is 5, and all 50 queries are multi-positive.

Queries average 76.14 characters, while documents average 952.55 characters. The query side is similar to a paper title, and the document side is much longer. The model must connect a compact research topic to abstracts that may describe methods, results, and applications in different wording.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2839, hit@10 of 0.8000, and recall@100 of 0.6311 using the top-500 BM25 candidate subset. Scientific titles often contain strong technical terms, so lexical matching can find at least one related document for many queries. The hit@10 value is therefore competitive.

However, BM25's nDCG@10 remains modest because related scientific documents do not always share the same exact terminology. A title and an abstract can describe the same method family or research area using different phrases. BM25 is useful for precise term anchoring but can miss broader scientific relatedness.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.3201, hit@10 of 0.7200, and recall@100 of 0.5779. Dense retrieval improves nDCG@10 over BM25 but has lower hit@10 and recall@100. This suggests that embedding similarity improves ranking quality when it finds related documents, but it misses some exact technical-term matches that BM25 captures.

The result is plausible for scientific retrieval with translated technical vocabulary. General dense embeddings can connect related methods and topics, but specialized scientific terminology, abbreviations, and formula-like phrases may require domain adaptation.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.3202, hit@10 of 0.8000, and recall@100 of 0.6639. It uses exactly 100 candidates per query, with no safeguard rows. This is the strongest overall profile: it matches BM25 hit@10, slightly exceeds dense nDCG@10, and has the best recall@100.

The hybrid result shows that scientific retrieval benefits from combining exact terminology and semantic relatedness. BM25 contributes technical phrase matching, while dense retrieval contributes conceptual similarity across titles and abstracts. For a reranker, the hybrid pool is the most attractive starting point because it preserves the best candidate coverage.

### Metric Interpretation for Model Researchers

Because every query has multiple positives, nDCG@10 measures whether several related documents are placed early, while hit@10 can be satisfied by only one related paper. recall@100 is important for reranking and recommendation-style use cases because the relevant set usually contains several documents.

The comparison shows that BM25 remains useful in scientific text, dense retrieval improves semantic ordering, and reranking_hybrid is best when both top-rank quality and candidate coverage matter. This task is a good diagnostic for whether a model handles translated scientific terminology without losing broader topic matching.

### Query and Relevance Type Tendencies

Queries include paper-title-like topics such as a new multilevel DC-DC boost converter, fast learning of sparse Gaussian Markov random fields, texture synthesis with convolutional neural networks, circularly polarized RFID antennas, and an advanced digital heart-rate monitor. Relevant documents are scientific abstracts or translated abstract fragments related by topic, method, or application.

The task rewards technical vocabulary handling and conceptual relatedness. A relevant document may not repeat the exact title words, but it should occupy a nearby research area. Conversely, a document can share a common technical term while addressing a different contribution.

### Representative Failure Modes

Likely failures include over-ranking abstracts that share a technical phrase but solve a different problem, missing related work expressed with alternative terminology, failing on partially translated or malformed scientific text, and confusing broad fields with specific methods. BM25 may be too narrow, while dense retrieval may be too broad without scientific specialization.

### Training Data That May Help

Useful training data includes scientific document retrieval, citation ranking, paper recommendation, Vietnamese academic abstracts, and multilingual scientific title-abstract pairs. Hard negatives should come from the same field but differ in method, contribution, or application.

### Model Improvement Notes

A model targeting this task should combine scientific terminology precision with document-level semantic relatedness. Sparse systems need normalization for translated technical terms and abbreviations. Dense systems need domain adaptation on scientific corpora. Hybrid systems are especially suitable because the observed profile shows the best balance of nDCG@10, hit@10, and recall@100.

## Example Data

| Query | Positive document |
| --- | --- |
| Bộ chuyển đổi tăng áp đa mức DC-DC mới [38 chars] | Tóm tắt: Các bộ chuyển đổi nguồn điện đa mức đang nổi lên như một loại tùy chọn bộ chuyển đổi năng lượng mới cho các ứng dụng công suất cao. Các bộ chuyển đổi nguồn điện đa mức thường tổng hợp sóng đi... [200 / 920 chars] |
| Học Lĩnh Vực Ngẫu Nhiên Markov Gauss Thưa Nhanh Dựa Trên Phân Tích Cholesky [75 chars] | Văn bản đã được dịch: [21 chars] |
| Tổng hợp kết cấu sử dụng mạng nơ-ron tích chập [46 chars] | Trong công trình này, chúng tôi nghiên cứu ảnh hưởng của độ sâu của mạng nơ-ron tích chập đến độ chính xác của nó trong bối cảnh nhận diện hình ảnh quy mô lớn. Đóng góp chính của chúng tôi là một đánh... [200 / 908 chars] |
| Antenna vòng tròn băng thông phẳng với phân cực tròn cho hệ thống RFID [70 chars] | Trong bài báo này, một kỹ thuật cấp nguồn dải uốn ngang (HMS) được đề xuất để đạt được sự khớp trở tốt và các mô hình bức xạ đối xứng cho một ăng-ten patch xếp chồng phân cực tròn băng thông rộng được... [200 / 1,256 chars] |
| Thiết kế máy theo dõi nhịp tim kỹ thuật số tiên tiến sử dụng các linh kiện điện tử cơ bản [89 chars] | Trong bài báo này, chúng tôi trình bày thiết kế và phát triển một thiết bị tích hợp mới để đo nhịp tim bằng đầu ngón tay nhằm cải thiện việc ước lượng nhịp tim. Khi các bệnh liên quan đến tim mạch ngà... [200 / 1,160 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original evaluation context | [SPECTER](https://arxiv.org/abs/2004.07180) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-vi dataset | [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi) |

Representative query and positive abstract snippets:

| Query | Positive document snippet |
| --- | --- |
| Bo chuyen doi tang ap da muc DC-DC moi | Cac bo chuyen doi nguon dien da muc dang noi len nhu mot tuy chon nang luong moi... |
| Hoc Linh Vuc Ngau Nhien Markov Gauss Thua Nhanh Dua Tren Phan Tich Cholesky | Van ban da duoc dich... |
| Tong hop ket cau su dung mang no-ron tich chap | Chung toi nghien cuu anh huong cua do sau mang no-ron tich chap den do chinh xac... |
| Antenna vong tron bang thong phang voi phan cuc tron cho he thong RFID | Mot ky thuat cap nguon dai uon ngang duoc de xuat cho ang-ten patch... |
| Thiet ke may theo doi nhip tim ky thuat so tien tien | Chung toi trinh bay thiet ke va phat trien mot thiet bi tich hop moi de do nhip tim... |
