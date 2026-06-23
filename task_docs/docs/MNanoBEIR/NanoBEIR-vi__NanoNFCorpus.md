# MNanoBEIR / NanoBEIR-vi / NanoNFCorpus

## Overview

NanoNFCorpus in the Vietnamese NanoBEIR slice is a biomedical and nutrition retrieval task derived from NFCorpus. The queries are Vietnamese translated health information needs, and the corpus contains Vietnamese translated scientific or medical passages. The retrieval goal is to find passages that are medically relevant to a short health query, often across a broad set of related studies. This makes the task useful for evaluating Vietnamese domain retrieval, multi-positive ranking, and biomedical terminology handling.

## Details

### What the Original Data Measures

NFCorpus was built for medical information retrieval with relevance judgments over health-related documents. In retrieval form, a model receives a compact query about a disease, food, nutrient, intervention, or medical concept and must retrieve passages that are relevant to that information need. Relevance is often broad: many documents can discuss the same condition, dietary factor, or clinical outcome.

The Vietnamese translated version adds multilingual domain difficulty. Biomedical vocabulary, study terminology, abbreviations, and food or disease names may be translated unevenly or remain close to English. A strong model must handle both exact medical terms and broader conceptual relevance.

### Observed Data Profile

The task contains 50 queries, 2,953 documents, and 1,651 relevance judgments. It is highly multi-positive, with an average of 33.02 positives per query. The minimum is 1, the median is 23.5, the maximum is 100, and 47 queries are multi-positive, or 94.0% of the query set.

Queries average 25.30 characters, while documents average 1,565.89 characters. This is a short-query, long-document domain retrieval task. The model must map a small number of health terms to long passages that may contain study designs, background statements, methods, outcomes, and caveats.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2313, hit@10 of 0.6000, and recall@100 of 0.1369 using the top-500 BM25 candidate subset. Lexical matching helps when the query contains explicit biomedical terms such as foods, nutrients, or conditions, but it covers only a small fraction of the broad positive set.

The low recall@100 should be interpreted in light of the many positives per query. BM25 can surface at least one relevant passage for many queries, but it is not broad enough to recover the full range of relevant biomedical evidence. It is especially vulnerable when relevant passages use related clinical terminology rather than the exact query wording.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.2445, hit@10 of 0.5800, and recall@100 of 0.1781. Dense retrieval improves nDCG@10 and recall@100 over BM25, but its hit@10 is slightly lower. This suggests that embedding similarity expands the relevant evidence pool but does not consistently place at least one relevant passage in the top 10 for every query.

The dense profile is consistent with a biomedical domain task where semantic similarity helps with related concepts, yet specialized terminology still limits a general multilingual embedding model. It can retrieve passages that are conceptually connected to the query, but fine distinctions between conditions, interventions, and outcomes remain difficult.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.2638, hit@10 of 0.6400, and recall@100 of 0.1781. It uses a top-100 candidate range with an optional rank-101 safeguard; this slice has 4 safeguard rows, candidate counts from 100 to 101, and a mean of 100.08 candidates. This is the strongest profile for top-10 ranking, while recall@100 matches dense retrieval.

The result indicates that Vietnamese NFCorpus benefits from combining exact medical term matching with dense concept matching. BM25 contributes precise disease, nutrient, or food anchors, while dense retrieval contributes semantically related evidence. The hybrid pool gives the best first-page relevance even though the overall relevant set remains hard to cover.

### Metric Interpretation for Model Researchers

Because most queries have many positives, nDCG@10 measures whether the top results contain highly useful biomedical evidence, while recall@100 measures only a small slice of the available relevant set. A low recall@100 is not necessarily a failure to find any evidence; it reflects the difficulty of covering dozens of positives from long scientific text.

The comparison shows that BM25 is useful for exact terminology, dense retrieval improves broader semantic coverage, and reranking_hybrid gives the best top-10 behavior. This task is a good diagnostic for whether a retrieval system can combine sparse medical vocabulary with dense biomedical relatedness.

### Query and Relevance Type Tendencies

Queries include health and nutrition topics such as health benefits of nuts, medical ethics, fava beans, what is really in chicken nuggets, and saturated fat. Relevant documents are often scientific or clinical passages with abstracts, objectives, methods, or findings. The same query may have many relevant passages because multiple studies can address the same health concept.

The task rewards domain vocabulary, synonym handling, and broad topical relevance. Unlike single-answer QA, the model is not looking for one exact answer. It must rank a useful set of medical evidence passages above unrelated or weakly related scientific text.

### Representative Failure Modes

Likely failures include over-ranking passages that share a food or disease term but discuss a different outcome, missing relevant studies that use technical synonyms, retrieving background medical text without direct relevance, and under-covering the large positive set. BM25 may be too literal, while dense retrieval may be too broad without biomedical specialization.

### Training Data That May Help

Useful training data includes Vietnamese biomedical retrieval, medical QA, scientific abstract ranking, nutrition evidence retrieval, and multi-positive supervision. Hard negatives should share the same disease, food, or intervention but differ in outcome, population, or clinical question.

### Model Improvement Notes

A model targeting this task should improve both terminology normalization and biomedical semantic matching. Sparse systems need robust medical tokenization and synonym expansion. Dense systems need domain adaptation on clinical and scientific text. Hybrid systems are promising because the strongest observed profile comes from combining exact terms with embedding-based relatedness.

## Example Data

| Query | Positive document |
| --- | --- |
| Lợi ích sức khỏe của các loại hạt [33 chars] | Mục tiêu Nghiên cứu mối quan hệ giữa việc tiêu thụ anh đào và nguy cơ tái phát cơn gout ở những người mắc bệnh gout. Phương pháp Chúng tôi đã tiến hành một nghiên cứu trường hợp chéo để xem xét mối liên hệ của một tập hợp các yếu tố nguy cơ giả định với các cơn gout tái phát. Những người mắc bệnh gout đã được tuyển chọn theo cách tiềm năng và theo dõi trực tuyến trong một năm. Người tham gia được hỏi về các thông tin sau khi trải qua một cơn gout: ngày bắt đầu của cơn gout, triệu chứng và dấu hiệu, thuốc (bao gồm cả thuốc chống gout), và các yếu tố nguy cơ tiềm năng (bao gồm lượng tiêu thụ anh đào hàng ngày và chiết xuất anh đào) trong khoảng thời gian 2 ngày trước cơn gout. Chúng tôi đã đánh giá thông tin phơi nhiễm tương tự trong các khoảng thời gian kiểm soát 2 ngày. Chúng tôi ước tính nguy cơ tái phát cơn gout liên quan đến việc tiêu thụ anh đào bằng cách sử dụng hồi quy logistic có điều kiện. Kết quả Nghiên cứu của chúng tôi bao gồm 633 cá nhân mắc bệnh gout. Việc tiêu thụ anh đào... [1,000 / 1,732 chars] |
| đạo đức y tế [12 chars] | BỐI CẢNH: Một trong những vấn đề chính trong việc kiểm soát cholesterol huyết thanh thông qua can thiệp chế độ ăn uống dường như là cần cải thiện sự tuân thủ của bệnh nhân. MỤC TIÊU: Khám phá nhiều câu hỏi liên quan đến các rào cản và động lực cho việc tuân thủ chế độ ăn uống giảm cholesterol. PHƯƠNG PHÁP: Chúng tôi đã khảo sát thực hành dinh dưỡng của các bác sĩ đa khoa Pháp đối với bệnh nhân bị tăng cholesterol máu, và xem xét thái độ của bệnh nhân đối với cách tiếp cận này. KẾT QUẢ: Chúng tôi đã phân tích 234 bảng câu hỏi cá nhân của bác sĩ và 356 bảng câu hỏi tự khảo sát của bệnh nhân. Lý do của bệnh nhân không tuân thủ chế độ ăn uống được chỉ định bao gồm: 'đã có thói quen ăn uống hài lòng' (34.7%), 'không muốn chịu đựng sự thiếu thốn dinh dưỡng' (33.3%), 'khó khăn trong việc hòa hợp chế độ ăn với cuộc sống gia đình' (27.8%) và 'đang dùng thuốc giảm cholesterol' (22.2%). Mặc dù bệnh nhân hiểu biết chung về khuyến nghị của bác sĩ là tốt, nhưng một số sự khác biệt đã được thấy giữa... [1,000 / 1,913 chars] |
| đậu fava [8 chars] | Trong 20 năm qua, sự quan tâm ngày càng tăng đối với sinh hóa, dinh dưỡng và dược lý của L-arginine đã dẫn đến nhiều nghiên cứu sâu rộng để khám phá vai trò dinh dưỡng và điều trị của nó trong việc điều trị và ngăn ngừa các rối loạn chuyển hóa ở người. Bằng chứng mới nổi cho thấy việc bổ sung L-arginine qua chế độ ăn uống giảm mỡ ở chuột béo phì di truyền, chuột béo phì do chế độ ăn, lợn nuôi đến tuổi xuất chuồng và các đối tượng người béo phì mắc bệnh tiểu đường loại 2. Các cơ chế chịu trách nhiệm cho những tác động có lợi của L-arginine có thể phức tạp, nhưng cuối cùng liên quan đến việc thay đổi cân bằng giữa năng lượng nạp vào và tiêu thụ theo hướng giảm mỡ hoặc giảm sự phát triển của mô mỡ trắng. Các nghiên cứu gần đây chỉ ra rằng việc bổ sung L-arginine kích thích sinh tổng hợp ty thể và phát triển mô mỡ nâu có thể thông qua việc tăng cường tổng hợp các phân tử tín hiệu tế bào (ví dụ: nitric oxide, carbon monoxide, polyamines, cGMP và cAMP) cũng như tăng cường biểu hiện của các g... [1,000 / 1,275 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [NFCorpus](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-vi dataset | [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi) |

Representative query and positive passage snippets:

| Query | Positive document snippet |
| --- | --- |
| Loi ich suc khoe cua cac loai hat | Muc tieu nghien cuu moi quan he giua viec tieu thu anh dao va nguy co tai phat con gout... |
| dao duc y te | Mot trong nhung van de chinh trong viec kiem soat cholesterol huyet thanh... |
| dau fava | Trong 20 nam qua, su quan tam ngay cang tang doi voi sinh hoa va dinh duong cua L-arginine... |
| Thuc su co gi trong mon ga vien? | De xac dinh thanh phan cua thit ga vien tu 2 chuoi thuc pham quoc gia... |
| chat beo bao hoa | Nghien cuu tiem nang hien tai xem xet moi lien he giua viec me tieu thu chat beo... |
