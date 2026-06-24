# MNanoBEIR / NanoBEIR-vi / NanoSciFact

## Overview

NanoSciFact in the Vietnamese NanoBEIR slice is a scientific claim evidence retrieval task derived from SciFact. The queries are Vietnamese translated scientific claims, and the corpus contains Vietnamese translated abstract evidence. The retrieval goal is to find abstracts that support or refute a scientific claim. This makes the task useful for evaluating Vietnamese scientific evidence retrieval, biomedical terminology matching, and claim-to-abstract ranking.

## Details

### What the Original Data Measures

SciFact was created for scientific claim verification using abstracts from biomedical and scientific literature. In retrieval form, a model receives a claim and must retrieve the abstract that contains evidence relevant to verifying it. The task is evidence-oriented: a passage is relevant because it addresses the claim, not because it merely shares a topic.

The Vietnamese translated version keeps the scientific evidence structure while introducing multilingual terminology variation. Gene names, disease names, methods, abbreviations, and protein identifiers often remain close to English, while surrounding claim and abstract text is Vietnamese. A strong model must combine exact scientific anchors with evidence-relation matching.

### Observed Data Profile

The task contains 50 queries, 2,919 documents, and 56 relevance judgments. Most queries have one positive abstract, with an average of 1.12 positives per query. The minimum is 1, the median is 1.0, the maximum is 4, and 4 queries are multi-positive, or 8.0% of the set.

Queries average 100.06 characters, while documents average 1,489.56 characters. The claims are longer and more technical than ordinary web questions, and the documents are long scientific abstracts. The model must align a precise claim with abstract-level evidence.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.7134, hit@10 of 0.8600, and recall@100 of 0.9107 using the top-500 BM25 candidate subset. This is a strong lexical profile. Scientific claims often contain distinctive terms such as gene symbols, diseases, assays, interventions, or molecular pathways, and these terms provide reliable anchors for BM25.

The high score also shows that term frequency can be very effective in scientific evidence retrieval when the claim and abstract share specialized vocabulary. However, BM25 can still over-rank abstracts that mention the right entity without addressing the exact claim, especially when several papers discuss the same method or biological process.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.6644, hit@10 of 0.7800, and recall@100 of 0.9107. Dense retrieval matches BM25's recall@100 but is weaker in top-10 ranking. This suggests that general embedding similarity recovers the same broad evidence pool, but it is less precise than lexical matching for ordering technical scientific abstracts.

The result is plausible for SciFact-style data. Scientific claims include exact terms that are highly informative, and a dense model not specialized for biomedical evidence may blur distinctions between related mechanisms, outcomes, or study contexts. Dense retrieval still has value for paraphrased claims, but it is not the strongest direct ranker here.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.7632, hit@10 of 0.8600, and recall@100 of 0.9107. It uses a top-100 candidate range with an optional rank-101 safeguard; this slice has 5 safeguard rows, candidate counts from 100 to 101, and a mean of 100.10 candidates. It is the strongest profile by nDCG@10 while matching BM25 on hit@10 and recall@100.

This indicates that combining exact scientific term matching with dense semantic similarity improves the top ordering of evidence abstracts. BM25 supplies precise biomedical anchors, while dense retrieval helps when the claim and abstract express the same finding with different wording. The hybrid profile is the most attractive first-stage candidate set for evidence-aware reranking.

### Metric Interpretation for Model Researchers

Because most queries have one positive, hit@10 directly measures whether the evidence abstract is visible to a verifier or RAG system, and nDCG@10 measures how early it appears. recall@100 indicates whether a downstream reranker can access the evidence. In this task, BM25 and dense have the same recall@100, but reranking_hybrid improves top-rank quality.

The comparison shows that scientific term overlap is unusually strong, dense retrieval alone is not enough for the best top ranks, and hybrid retrieval provides the best direct nDCG@10. This task is useful for checking whether a model preserves exact biomedical anchors while still benefiting from semantic evidence matching.

### Query and Relevance Type Tendencies

Queries include claims about Ly49Q regulation of raft membrane function, antiretroviral therapy and tuberculosis rates, interferon-stimulated genes and West Nile virus, HPV detection for cervical cancer screening, and TDP-43 interactions with respiratory complex proteins. Relevant documents are long scientific abstracts that describe experiments, populations, findings, or mechanisms.

The task rewards precise biomedical evidence matching. A relevant abstract must address the claim's scientific relation, not simply mention the same gene, disease, or assay. This makes same-entity scientific negatives especially challenging.

### Representative Failure Modes

Likely failures include retrieving abstracts that share a gene or disease name but test a different hypothesis, confusing support with broad topical similarity, missing evidence when terminology is paraphrased, and over-ranking background abstracts. BM25 may be too term-driven, while dense retrieval may underweight exact biomedical identifiers.

### Training Data That May Help

Useful training data includes Vietnamese scientific claim verification, biomedical abstract retrieval, multilingual evidence retrieval, and hard negatives that share entities or methods but do not support the claim. Training should preserve exact identifiers and include claim-evidence relation supervision.

### Model Improvement Notes

A model targeting this task should keep scientific identifier precision while improving evidence-relation ranking. Sparse systems need strong biomedical tokenization and acronym handling. Dense systems need domain adaptation on biomedical claim-abstract pairs. Hybrid systems are well suited here because the best observed top-rank behavior comes from combining both signals.

## Example Data

| Query | Positive document |
| --- | --- |
| Quy định của Ly49Q về chức năng của màng raft trong sự di chuyển của bạch cầu trung tính đến các vị trí viêm. [109 chars] | Các bạch cầu trung tính nhanh chóng trải qua quá trình phân cực và di chuyển theo hướng để xâm nhập vào các vị trí nhiễm trùng và viêm. Ở đây, chúng tôi cho thấy rằng một thụ thể MHC I ức chế, Ly49Q, là rất quan trọng cho sự phân cực nhanh chóng và xâm nhập mô của các bạch cầu trung tính. Trong trạng thái ổn định, Ly49Q ức chế sự bám dính của bạch cầu trung tính bằng cách ngăn chặn sự hình thành phức hợp điểm, có thể bằng cách ức chế Src và PI3 kinase. Tuy nhiên, trong sự hiện diện của các tác nhân viêm, Ly49Q đã trung gian cho sự phân cực nhanh chóng và xâm nhập mô của bạch cầu trung tính theo cách phụ thuộc vào miền ITIM. Các chức năng đối lập này dường như được trung gian bởi việc sử dụng khác nhau của phosphatase hiệu ứng SHP-1 và SHP-2. Sự phân cực và di chuyển phụ thuộc vào Ly49Q bị ảnh hưởng bởi sự điều chỉnh của Ly49Q đối với chức năng của bè màng. Chúng tôi đề xuất rằng Ly49Q là yếu tố then chốt trong việc chuyển đổi bạch cầu trung tính sang hình thái phân cực và di chuyển nha... [1,000 / 1,134 chars] |
| Liệu pháp kháng retrovirus và tác động của nó đến việc giảm tỷ lệ bệnh lao trên một loạt các mức CD4. [101 chars] | NỀN TẢNG Nhiễm virus suy giảm miễn dịch ở người (HIV) là yếu tố nguy cơ mạnh nhất dẫn đến bệnh lao và đã thúc đẩy sự tái phát của nó, đặc biệt là ở khu vực hạ Sahara châu Phi. Năm 2010, ước tính có 1,1 triệu trường hợp lao mới trong số 34 triệu người sống với HIV trên toàn thế giới. Liệu pháp kháng retrovirus có tiềm năng lớn trong việc ngăn ngừa bệnh lao liên quan đến HIV. Chúng tôi đã tiến hành một đánh giá hệ thống về các nghiên cứu phân tích tác động của liệu pháp kháng retrovirus đối với tỷ lệ mắc bệnh lao ở người lớn nhiễm HIV. PHƯƠNG PHÁP VÀ KẾT QUẢ PubMed, Embase, African Index Medicus, LILACS và các cơ sở dữ liệu thử nghiệm lâm sàng đã được tìm kiếm một cách hệ thống. Các thử nghiệm ngẫu nhiên có đối chứng, nghiên cứu đoàn hệ tiến cứu và nghiên cứu đoàn hệ hồi cứu được đưa vào nếu chúng so sánh tỷ lệ mắc bệnh lao theo tình trạng liệu pháp kháng retrovirus ở người lớn nhiễm HIV trong thời gian trung bình trên 6 tháng ở các nước đang phát triển. Đối với các phân tích tổng hợp, c... [1,000 / 2,179 chars] |
| Sự điều chỉnh tăng nhanh và biểu hiện cơ bản cao hơn của các gen được kích thích bởi interferon có làm giảm sự sống sót của các nơ-ron tế bào hạt bị nhiễm virus West Nile không? [177 chars] | Mặc dù độ nhạy cảm của các tế bào thần kinh trong não đối với nhiễm trùng vi sinh vật là một yếu tố quyết định chính trong kết quả lâm sàng, nhưng rất ít điều được biết về các yếu tố phân tử điều chỉnh độ nhạy cảm này. Ở đây, chúng tôi cho thấy rằng hai loại tế bào thần kinh từ các vùng não khác nhau có sự cho phép khác nhau đối với sự sao chép của một số virus RNA dương. Tế bào thần kinh hạt của tiểu não và tế bào thần kinh vỏ não từ vỏ não có các chương trình miễn dịch bẩm sinh độc đáo, điều này mang lại độ nhạy cảm khác nhau đối với nhiễm virus ex vivo và in vivo. Bằng cách chuyển gen vào tế bào thần kinh vỏ não mà được biểu hiện cao hơn trong tế bào thần kinh hạt, chúng tôi đã xác định được ba gen kích thích interferon (ISGs; Ifi27, Irg1 và Rsad2 (còn được biết đến là Viperin)) có tác dụng kháng virus đối với các virus thần kinh khác nhau. Hơn nữa, chúng tôi phát hiện rằng trạng thái di truyền và sự điều chỉnh của microRNA (miRNA) đối với ISGs có tương quan với phản ứng kháng virus... [1,000 / 1,233 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [SciFact](https://arxiv.org/abs/2004.14974) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-vi dataset | [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi) |

Representative query and positive evidence snippets:

| Query | Positive document snippet |
| --- | --- |
| Quy dinh cua Ly49Q ve chuc nang cua mang raft trong su di chuyen cua bach cau trung tinh den cac vi tri viem. | Cac bach cau trung tinh nhanh chong trai qua qua trinh phan cuc va di chuyen... |
| Lieu phap khang retrovirus va tac dong cua no den viec giam ty le benh lao tren mot loat cac muc CD4. | Nhiem virus suy giam mien dich o nguoi la yeu to nguy co manh nhat dan den benh lao... |
| Su dieu chinh tang nhanh va bieu hien co ban cao hon cua cac gen duoc kich thich boi interferon co lam giam su song sot cua cac no-ron bi nhiem virus West Nile khong? | Rat it dieu duoc biet ve cac yeu to phan tu dieu chinh do nhay cam nay... |
| Sang loc ung thu co tu cung nguyen phat voi phat hien HPV co do nhay doc cao hon so voi te bao hoc thong thuong? | Sang loc ung thu co tu cung dua tren viec xet nghiem virus papilloma o nguoi... |
| Chan tuong tac giua TDP-43 va protein phuc hop ho hap I ND3 va ND6 dan den tang cuong mat neuron do TDP-43 gay ra. | Cac dot bien gen trong protein lien ket DNA TAR gay ra benh xo cung teo co mot ben... |
