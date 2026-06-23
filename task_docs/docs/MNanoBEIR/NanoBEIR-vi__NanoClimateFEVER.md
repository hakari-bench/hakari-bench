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
| Từ năm 1970 đến năm 1998 đã có một giai đoạn ấm lên làm tăng nhiệt độ khoảng 0,7 độ F, điều này đã g... [100 / 159 chars] | Thế Paleocen ( -LSB- pronˈpæliəˌsiːn , _ ˈpæ - , _ - lioʊ - -RSB- ) hay Palaeocene, được gọi là "cũ gần đây", là một kỷ địa chất kéo dài từ khoảng thời gian nào đó. Đây là kỷ đầu tiên của Thế Paleogen... [200 / 1,144 chars] |
| Trên thực tế, xu hướng, mặc dù không có ý nghĩa thống kê, đang giảm. [68 chars] | Chu kỳ mặt trời hoặc chu kỳ hoạt động từ tính của mặt trời là sự thay đổi gần như định kỳ 11 năm trong hoạt động của Mặt Trời (bao gồm sự thay đổi trong mức độ bức xạ mặt trời và sự phun trào vật chất... [200 / 696 chars] |
| Mực nước biển địa phương và khu vực tiếp tục thể hiện sự biến đổi tự nhiên điển hình - ở một số nơi... [100 / 140 chars] | Mực nước biển trung bình (MSL) (viết tắt đơn giản là mực nước biển) là mức trung bình của bề mặt một hoặc nhiều đại dương của Trái Đất từ đó có thể đo được độ cao như độ cao địa hình. MSL là một loại... [200 / 1,089 chars] |
| [Các nhà khoa học khí hậu] nói rằng các khía cạnh của trường hợp bão Harvey cho thấy sự nóng lên toà... [100 / 136 chars] | Các tác động của sự nóng lên toàn cầu là những thay đổi môi trường và xã hội do (trực tiếp hoặc gián tiếp) khí thải khí nhà kính của con người gây ra. Có sự đồng thuận khoa học rằng biến đổi khí hậu đ... [200 / 1,376 chars] |
| Thí nghiệm CLOUD của CERN chỉ kiểm tra một phần ba của một trong bốn yêu cầu cần thiết để đổ lỗi cho... [100 / 187 chars] | Việc quy kết biến đổi khí hậu gần đây là nỗ lực xác định một cách khoa học các cơ chế chịu trách nhiệm cho những biến đổi khí hậu gần đây trên Trái Đất, thường được gọi là "nóng lên toàn cầu". Nỗ lực... [200 / 2,045 chars] |

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
