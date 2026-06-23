# MNanoBEIR / NanoBEIR-vi / NanoClimateFEVER

## Overview

NanoClimateFEVER in the Vietnamese NanoBEIR slice is a climate claim evidence retrieval task derived from CLIMATE-FEVER. The queries are Vietnamese translated climate-related claims, and the corpus contains Vietnamese translated evidence passages. The retrieval goal is to find passages that help verify, contextualize, or assess claims about climate science, warming trends, sea level, storms, solar activity, and attribution. It is a compact diagnostic for multilingual scientific evidence retrieval in Vietnamese.

## Details

### What the Original Data Measures

CLIMATE-FEVER evaluates evidence retrieval for real-world climate claims. A relevant passage must bear on the specific claim, not merely mention the same climate topic. The claim may involve a time period, trend direction, statistical qualifier, causal mechanism, or scientific attribution. Retrieval therefore requires claim-specific evidence matching.

The Vietnamese translated version adds multilingual pressure around scientific phrasing, long claims, and long evidence passages. Climate vocabulary can provide useful anchors, but relevant evidence may be expressed through broader explanatory context. A model must preserve exact scientific details while recognizing when a passage actually verifies the claim.

### Observed Data Profile

The task contains 50 queries, 3,408 documents, and 148 relevance judgments. It is mostly multi-positive, with an average of 2.96 positives per query. The minimum is 1, the median is 3.0, the maximum is 5, and 44 queries are multi-positive, or 88.0% of the query set. This makes the task a multi-evidence retrieval benchmark.

Queries average 133.76 characters, while documents average 1,589.80 characters. The claims are long factual assertions, and the evidence documents are substantially longer. The relevant signal may be only one portion of the document, so broad topic matching is insufficient for strong ranking.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2668, hit@10 of 0.6000, and recall@100 of 0.6284 using the top-500 BM25 candidate subset. This is a moderate lexical profile. Vietnamese climate claims contain important terms, but exact overlap alone does not reliably surface all evidence passages or rank them well.

The BM25 result suggests that term matching can identify some climate-topic evidence, but struggles with paraphrase and claim specificity. Passages about global warming, sea level, or solar cycles may share words with the query without verifying the exact assertion. This makes lexical retrieval a useful baseline but not a complete solution.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.3539, hit@10 of 0.7800, and recall@100 of 0.6554. Dense retrieval improves substantially over BM25 in top-10 quality and hit rate, with a smaller recall gain. This indicates that embedding similarity captures claim-evidence semantics beyond exact climate terminology.

Dense retrieval is especially useful when the evidence passage uses explanatory wording rather than repeating the claim. It can connect a claim about a trend, attribution, or event to a passage that describes the underlying mechanism. Remaining errors likely involve passages that are topically close but do not verify the precise claim.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.3558, hit@10 of 0.7800, and recall@100 of 0.6824. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 3 safeguard rows and a mean of 100.06 candidates. The hybrid profile is slightly strongest overall, especially in recall@100.

This suggests that combining lexical climate anchors with dense semantic similarity improves candidate coverage and marginally improves graded top-10 ranking. The gain over dense is small, so the main value of hybrid search is broader evidence access. A stronger reranker could use that candidate pool to better distinguish verifying passages from same-topic distractors.

### Metric Interpretation for Model Researchers

nDCG@10 measures whether useful evidence appears in the first page. hit@10 indicates whether at least one evidence passage is visible, and recall@100 measures whether a later reranker has access to the evidence set. Because most queries have multiple positives, recall@100 matters for evidence completeness.

The method comparison shows that BM25 is limited by exact wording, dense retrieval is much better for semantic evidence matching, and reranking_hybrid gives the broadest candidate pool. NanoClimateFEVER-vi is therefore useful for evaluating claim-specific evidence ranking rather than broad climate-topic retrieval.

### Query and Relevance Type Tendencies

Queries are full climate claims about warming periods, statistical trends, sea-level variation, Hurricane Harvey, global warming attribution, and cosmic rays. Relevant documents are evidence-bearing passages that may explain scientific phenomena, measurement baselines, or attribution mechanisms.

The task rewards models that preserve qualifiers. Words about trend direction, statistical significance, locality, causation, or attribution can determine relevance. A passage on the same climate topic is not enough if it does not address those claim-specific qualifiers.

### Representative Failure Modes

Likely failures include retrieving broad climate passages that do not verify the claim, missing evidence because the passage phrases the issue differently, ignoring statistical or causal qualifiers, and over-ranking background explanations. BM25 is vulnerable to vocabulary mismatch, while dense retrieval can overgeneralize from topic similarity.

### Training Data That May Help

Useful training data includes Vietnamese climate fact-checking, scientific evidence retrieval, multilingual claim-evidence data, and hard negatives that reuse climate terms without verifying the claim. For rerankers, near-topic non-evidence passages are especially useful because they match the benchmark's main ambiguity.

### Model Improvement Notes

A model targeting this task should improve claim-specific evidence discrimination. Sparse systems need terminology normalization and query expansion without losing scientific specificity. Dense systems need better handling of numerical, causal, and negation-like qualifiers. Hybrid systems are promising as high-recall candidate generators, but should be paired with evidence-aware reranking.

## Example Data

| Query | Positive document |
| --- | --- |
| Từ năm 1970 đến năm 1998 đã có một giai đoạn ấm lên làm tăng nhiệt độ khoảng 0,7 độ F, điều này đã giúp khởi xướng phong trào báo động về sự nóng lên toàn cầu. [159 chars] | Thế Paleocen ( -LSB- pronˈpæliəˌsiːn , _ ˈpæ - , _ - lioʊ - -RSB- ) hay Palaeocene, được gọi là "cũ gần đây", là một kỷ địa chất kéo dài từ khoảng thời gian nào đó. Đây là kỷ đầu tiên của Thế Paleogene trong Kỷ Đệ Tứ hiện đại. Giống như nhiều kỷ địa chất khác, các lớp đất xác định sự bắt đầu và kết thúc của kỷ này được xác định rõ ràng, nhưng độ tuổi chính xác vẫn chưa chắc chắn. Kỷ Paleocen bao gồm hai sự kiện lớn trong lịch sử Trái Đất. Nó bắt đầu với sự kiện tuyệt chủng hàng loạt vào cuối kỷ Phấn Trắng, được gọi là ranh giới Kỷ Phấn Trắng - Paleogene (K - Pg). Đây là thời kỳ đánh dấu sự diệt vong của các loài khủng long không bay, các loài bò sát biển khổng lồ và nhiều động thực vật khác. Sự tuyệt chủng của khủng long để lại những ngách sinh thái chưa được lấp đầy trên toàn cầu. Kỷ Paleocen kết thúc với sự kiện Tối đa Nhiệt độ Paleocen - Eocen, một khoảng thời gian địa chất ngắn (khoảng 0.2 triệu năm) đặc trưng bởi những thay đổi cực đoan trong khí hậu và chu trình carbon. Tên gọi "... [1,000 / 1,144 chars] |
| Trên thực tế, xu hướng, mặc dù không có ý nghĩa thống kê, đang giảm. [68 chars] | Chu kỳ mặt trời hoặc chu kỳ hoạt động từ tính của mặt trời là sự thay đổi gần như định kỳ 11 năm trong hoạt động của Mặt Trời (bao gồm sự thay đổi trong mức độ bức xạ mặt trời và sự phun trào vật chất từ mặt trời) và hình thức (thay đổi trong số lượng và kích thước của các đốm mặt trời, các cơn bùng phát và các biểu hiện khác). Chúng đã được quan sát (qua sự thay đổi trong hình thức của mặt trời và qua những thay đổi thấy trên Trái Đất, chẳng hạn như cực quang) trong nhiều thế kỷ. Những thay đổi trên mặt trời gây ra các tác động trong không gian, trong bầu khí quyển và trên bề mặt Trái Đất. Trong khi nó là biến số chi phối trong hoạt động mặt trời, các dao động không định kỳ cũng xảy ra. [696 chars] |
| Mực nước biển địa phương và khu vực tiếp tục thể hiện sự biến đổi tự nhiên điển hình - ở một số nơi tăng lên và ở những nơi khác giảm xuống. [140 chars] | Mực nước biển trung bình (MSL) (viết tắt đơn giản là mực nước biển) là mức trung bình của bề mặt một hoặc nhiều đại dương của Trái Đất từ đó có thể đo được độ cao như độ cao địa hình. MSL là một loại dữ liệu thẳng đứng, một điểm tham chiếu địa chất được chuẩn hóa, được sử dụng, chẳng hạn, làm dữ liệu bản đồ trong bản đồ học và điều hướng hàng hải, hoặc, trong hàng không, là mực nước biển chuẩn mà tại đó áp suất khí quyển được đo để hiệu chỉnh độ cao và, do đó, các mức bay của máy bay. Một tiêu chuẩn mực nước biển trung bình phổ biến và tương đối đơn giản là điểm giữa giữa mực nước thấp trung bình và mực nước cao trung bình tại một vị trí cụ thể. Mực nước biển có thể bị ảnh hưởng bởi nhiều yếu tố và được biết là đã thay đổi rất nhiều qua các thang thời gian địa chất. Việc đo lường cẩn thận các biến đổi trong MSL có thể cung cấp những hiểu biết về sự thay đổi khí hậu đang diễn ra, và sự gia tăng mực nước biển đã được trích dẫn rộng rãi như là bằng chứng của sự nóng lên toàn cầu đang diễn... [1,000 / 1,089 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [CLIMATE-FEVER](https://arxiv.org/abs/2012.00614) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-vi dataset | [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi) |

Representative query and positive evidence snippets:

| Query | Positive document snippet |
| --- | --- |
| Từ năm 1970 đến năm 1998 đã có một giai đoạn ấm lên làm tăng nhiệt độ khoảng 0,7 độ F... | Thế Paleocen hay Palaeocene, được gọi là "cũ gần đây", là một kỷ địa chất... |
| Trên thực tế, xu hướng, mặc dù không có ý nghĩa thống kê, đang giảm. | Chu kỳ mặt trời hoặc chu kỳ hoạt động từ tính của mặt trời là sự thay đổi gần như định kỳ 11 năm... |
| Mực nước biển địa phương và khu vực tiếp tục thể hiện sự biến đổi tự nhiên điển hình... | Mực nước biển trung bình (MSL) là mức trung bình của bề mặt một hoặc nhiều đại dương... |
| Các nhà khoa học khí hậu nói rằng các khía cạnh của trường hợp bão Harvey cho thấy sự nóng lên toàn cầu đang làm tình hình tồi tệ hơn. | Các tác động của sự nóng lên toàn cầu là những thay đổi môi trường và xã hội do khí thải khí nhà kính của con người gây ra... |
| Thí nghiệm CLOUD của CERN chỉ kiểm tra một phần ba của một trong bốn yêu cầu cần thiết để đổ lỗi cho sự nóng lên toàn cầu vào các tia vũ trụ... | Việc quy kết biến đổi khí hậu gần đây là nỗ lực xác định một cách khoa học các cơ chế chịu trách nhiệm... |
