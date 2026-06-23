# NanoVNMTEB / sci_fact_vn

## Overview

`sci_fact_vn` is the Vietnamese NanoVNMTEB version of SciFact scientific claim-evidence retrieval. SciFact was introduced for verifying expert-written scientific claims against scientific abstracts, with evidence abstracts labeled as support or refute and rationale sentences annotated. In this retrieval formulation, translated scientific claims are queries and translated scientific abstracts are documents.

The Nano split contains 134 queries, 5,183 documents, and 155 positive qrels. Queries average 90.641791 characters, and documents average 1,518.840054 characters. Most claims have one positive abstract, so the task is precise evidence retrieval over long scientific text. Dense retrieval is strongest on nDCG@10 and hit@10, while `reranking_hybrid` has the best recall@100. The task tests whether a model can preserve biomedical entities and match the direction of a claimed finding, not merely retrieve abstracts with overlapping terminology.

## Details

### What the Original Data Measures

SciFact measures scientific claim verification. Claims are written against a corpus of abstracts and must be supported or refuted by evidence in those abstracts. The retrieval stage asks whether the system can find the evidence-bearing abstract before classification or rationale extraction.

The Vietnamese version translates claims and abstracts but preserves many scientific terms: gene and protein names, disease names, interventions, measurements, molecular pathways, and experimental vocabulary. Relevance depends on the abstract containing evidence for the claim's relation. An abstract mentioning KRAS or ALDH1 is not necessarily relevant unless it addresses the stated finding.

### Observed Data Profile

There are 155 positives for 134 queries. The average is 1.156716 positives per query, the median is 1, and 13 queries have multiple positives. The maximum positive count is 5. This is mostly a single-evidence retrieval task, with a small number of claims supported or refuted by several abstracts.

Documents are long biomedical or scientific abstracts. Queries are formal claims rather than search questions. The model must map a claim such as an intervention effect, protein recruitment, biomarker association, or disease prognosis relation to the abstract that contains the evidence.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6157620166, hit@10 of 0.7537313433, and recall@100 of 0.8774193548 with a top-500 candidate set. Scientific terms are strong lexical anchors, so sparse retrieval can often find a relevant abstract. Gene symbols, disease names, drug names, and technical phrases are useful exact-match signals.

BM25's limitation is relation sensitivity. Scientific claims often depend on direction, mechanism, population, or experimental context. A same-entity abstract may discuss a different effect, or even a contradictory finding. Lexical overlap finds candidates, but it does not reliably rank the evidence-bearing abstract first.

### Dense Evaluation Profile

Dense retrieval with `harrier-oss-270m` reaches nDCG@10 of 0.6635889042, hit@10 of 0.7835820896, and recall@100 of 0.9096774194. It is strongest on the top-rank metrics. Dense similarity appears to capture more of the claim-to-evidence relation than BM25, especially when evidence wording differs from the claim.

Dense retrieval helps with claims about mechanisms, intervention effects, biomarker prognosis, and cellular processes. Its challenge is that biomedical abstracts with related entities can be semantically close while making different or opposite claims. Domain-specific relation modeling remains important.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reaches nDCG@10 of 0.6485360114, hit@10 of 0.7611940299, and recall@100 of 0.9290322581. The top-100 candidate pool has mean candidate count 100.074627, with 10 safeguard-positive rows and 10 rows containing 101 candidates. Hybrid retrieval improves recall over dense but is slightly worse on top-rank quality.

This shows a familiar scientific-retrieval tradeoff. Sparse evidence rescues exact entities and terms, increasing candidate coverage. Dense retrieval ranks evidence-bearing abstracts better. A final reranker should use hybrid candidates but compare scientific relations and evidence sufficiency rather than only entity overlap.

### Metric Interpretation for Model Researchers

Because most queries have one positive, nDCG@10 is a strong measure of evidence availability for downstream verification. Recall@100 is useful for reranking pipelines, but ranking the evidence abstract high is critical. Dense retrieval currently gives the best immediate top-rank behavior.

The hybrid recall advantage still matters. Scientific evidence retrieval can miss positives when a model ignores rare biomedical tokens. The best pipeline should combine exact biomedical term recall with relation-aware ordering.

### Query and Relevance Type Tendencies

Queries are scientific claims about biomedical mechanisms, interventions, biomarkers, disease associations, cell behavior, and molecular processes. Relevant documents are scientific abstracts that contain evidence for support or refutation. The examples include claims about amyloidosis MRI severity, sildenafil and SSRI-related dysfunction, ethanol stress in bacteria, dendritic cells and intestinal homeostasis, and methionine restriction.

Relevance is evidence-specific. A document can share all major entities and still be irrelevant if it does not address the claimed direction or experimental outcome. This makes the task stricter than topical scientific search.

### Representative Failure Modes

BM25 can over-rank same-entity abstracts with the wrong relation. Dense retrieval can retrieve biologically adjacent abstracts that discuss related pathways but not the claimed finding. Hybrid retrieval can improve candidate coverage while still needing a reranker to reject entity-sharing non-evidence.

Another failure mode is directionality loss. Claims often depend on increases, decreases, recruitment, inhibition, improvement, or association. Models that ignore directional language will confuse support, refutation, and unrelated evidence.

### Training Data That May Help

Useful training data includes official SciFact training claims and abstracts with overlap removed, biomedical claim-evidence retrieval pairs, scientific NLI and fact-verification data, and translated scientific retrieval data. Hard negatives should share entities or interventions while omitting or contradicting the claimed relation.

Synthetic data should generate Vietnamese scientific claims from non-evaluation abstracts while preserving gene names, proteins, diseases, measurements, directions of effect, and experimental context. Claims should be paired with rationale-bearing abstracts and same-entity distractors.

### Model Improvement Notes

The main improvement direction is scientific relation-aware reranking. Sparse retrieval should preserve biomedical nomenclature. Dense retrieval should model the claim relation. Rerankers should compare whether the abstract states evidence for the claim, including direction and experimental condition.

Error analysis should separate entity recall failures, directionality failures, mechanism mismatch, and translation terminology issues. The task is a compact stress test for scientific evidence retrieval in Vietnamese.

## Example Data

| Query | Positive document |
| --- | --- |
| Mức độ nghiêm trọng của bệnh tim liên quan đến amyloidosis có thể được mô tả bằng mức độ xuyên thành của sự tăng cường gadolinium muộn trong MRI. [145 chars] | Giá trị tiên lượng của quá trình tăng cường muộn gadolinium của cộng hưởng từ tim mạch trong bệnh tim amyloidosis BỐN MẠT LÝ NHIỆM: Dự đoán và điều trị 2 loại bệnh Amyloidosis tim chính, chuỗi nhẹ của immunoglobulin (AL) và Amyloidosis transthyretin (ATTR), chịu ảnh hưởng đáng kể bởi sự liên quan đến tim. Chụp cộng hưởng từ tim với tăng cường Gadolinium muộn (LGE) là tiêu chuẩn tham chiếu cho chẩn đoán bệnh amyloidosis tim, nhưng khả năng phân tầng rủi ro của nó chưa được biết đến. PHƯƠNG PHÁP VÀ KẾT QUẢ: Hai trăm năm mươi đối tượng được tuyển chọn, gồm 122 bệnh nhân với bệnh amyloid ATTR, 9 người mang đột biến không triệu chứng, và 119 bệnh nhân với bệnh AL amyloidosis, đã trải qua LGE chụp cộng hưởng từ tim mạch máu. Các đối tượng được theo dõi trong thời gian trung bình 24±13 tháng. LGE được thực hiện với phục hồi nghịch đảo nhạy cảm pha (PSIR) và không có (chỉ độ lớn). Chúng được so sánh với thể tích ngoài tế bào đo bằng bản đồ T1. PSIR vượt trội hơn so với LGE phục hồi nghịch đảo... [1,000 / 2,127 chars] |
| Sildenafil cải thiện chức năng cương dương ở những người đàn ông bị rối loạn cương dương do sử dụng thuốc chống trầm cảm SSRI. [126 chars] | Điều trị rối loạn chức năng tình dục liên quan đến thuốc chống trầm cảm với sildenafil: một thử nghiệm có đối chứng. Bất lực là tác dụng phụ phổ biến của thuốc chống trầm cảm thường gây nên tình trạng không tuân thủ điều trị. MỤC ĐÍCH: Đánh giá hiệu quả của sildenafil citrate trong điều trị rối loạn chức năng sinh dục ở nam giới sử dụng thuốc ức chế tái hấp thu chọn lọc và không chọn lọc serotonin (SSRI). MÔ TẢ PHƯƠNG PHÁP, ĐỊA ĐIỂM VÀ BỆNH NHÂN: Thử nghiệm song song ngẫu nhiên, có nhóm đối chứng giả dược, được tiến hành tại 3 trung tâm y khoa đại học tại Mỹ từ ngày 1/11/2000 đến ngày 1/1/2001 trên 90 bệnh nhân ngoại trú nam giới (tuổi trung bình 45±8 tuổi) mắc chứng trầm cảm nặng đang giảm triệu chứng và rối loạn chức năng sinh dục do dùng SSRI. CÔNG VIỆC: Bệnh nhân được chỉ định ngẫu nhiên dùng sildenafil (n=45) hoặc giả dược (n=45) với liều linh hoạt bắt đầu từ 50 mg tăng lên 100 mg trước khi quan hệ tình dục trong 6 tuần. ĐỐI TƯỢNG ĐÁNH GIÁ CHỦ YẾU: Điểm đánh giá toàn diện lâm sàng... [1,000 / 2,203 chars] |
| Căng thẳng ethanol làm giảm biểu hiện của IBP trong vi khuẩn. [61 chars] | Sự điều chỉnh và chuyển mạch trao hóa trong quá trình tiến hóa trong phòng thí nghiệm của độ dung nạp cồn ở E. coli Hiểu được cơ sở di truyền của sự thích nghi là một vấn đề trung tâm trong sinh học. Tuy nhiên, việc chỉ ra các cơ chế phân tử cơ bản đã gây khó khăn vì những biến đổi về thể chất có thể dẫn đến nhiều đường dẫn, trong đó bất kỳ con đường nào cũng có thể đóng góp tương đối ít. Chúng tôi đã phát triển một khung thực nghiệm/tính toán kết hợp để giải quyết vấn đề này và sử dụng nó để hiểu được cơ sở di truyền của sự dung nạp cồn ở vi khuẩn Escherichia coli. Chúng tôi sử dụng định nghĩa thể chất để đo lường hậu quả của sự rối loạn tại một vị trí duy nhất trong bối cảnh tiếp xúc với cồn. Sau đó, phân tích tính toán ở cấp độ mô-đun được sử dụng để chỉ ra tổ chức của các vị trí góp phần thành các quá trình tế bào và đường dẫn điều hòa (ví dụ như điều hòa nồng độ muối và sinh tổng hợp thành tế bào) mà những biến đổi có tác động đáng kể đến sự dung nạp cồn. Đáng chú ý, chúng tôi phá... [1,000 / 1,545 chars] |

### Source Reference Table

| Source | Role |
|---|---|
| SciFact | Original scientific claim-verification benchmark |
| SciFact GitHub repository | Official dataset repository |
| BEIR | Retrieval benchmark framing |
| VN-MTEB | Vietnamese benchmark collection using translated retrieval tasks |
| GreenNode dataset card | Public dataset entry for this Vietnamese split |

### Representative Snippets

- Query: `Mức độ nghiêm trọng của bệnh tim liên quan đến amyloidosis...`
  Relevant documents discuss gadolinium enhancement in cardiac amyloidosis.
- Query: `Sildenafil cải thiện chức năng cương dương...`
  Relevant documents describe trials of sildenafil for antidepressant-associated sexual dysfunction.
- Query: `Căng thẳng ethanol làm giảm biểu hiện của IBP trong vi khuẩn.`
  Relevant documents concern ethanol tolerance or bacterial stress regulation.
- Query: `Sự giao tiếp giữa tế bào dendritic...`
  Relevant documents discuss dendritic cells, innate lymphoid cells, and intestinal homeostasis.
- Query: `Các tế bào đang trải qua hạn chế methionine có thể kích hoạt miRNAs.`
  Relevant documents discuss microRNAs and stress-response mechanisms.
