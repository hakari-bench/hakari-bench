# NanoVNMTEB / climate_fever_vn

## Overview

`climate_fever_vn` is a Vietnamese climate claim evidence retrieval task from NanoVNMTEB. The query is a translated real-world climate claim, and relevant documents are translated Wikipedia-style evidence passages that support, refute, or otherwise inform the claim. Most queries have multiple positives. Dense retrieval is the strongest top-rank profile, while `reranking_hybrid` gives the best recall@100. BM25 is weaker because climate evidence often uses different phrasing or related scientific context rather than repeating the claim.

## Details

### What the Original Data Measures

CLIMATE-FEVER adapts FEVER-style fact verification to real-world climate claims. The original task emphasizes evidence retrieval for subtle climate claims, including claims that require scientific context rather than simple entity lookup.

VN-MTEB translates and filters the benchmark into Vietnamese. The Nano split evaluates Vietnamese claim-to-evidence retrieval, where each claim may have several relevant evidence passages.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 635 positive qrel rows. Queries average 129.97 characters, while documents average 407.08 characters. Positives per query average 3.17, with a minimum of 1, a median of 3, and a maximum of 5. There are 186 multi-positive queries, 93.0% of the split.

Example claims discuss brown bears in Alaska changing feeding habits, extreme temperature outcomes under climate action, fossil fuels and carbon dioxide, cattle emissions, and whether climate models ignore benefits from atmospheric CO2.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.2447, hit@10 of 0.6350, and recall@100 of 0.7339. BM25 can find evidence when the claim names a distinctive climate term or entity.

The limitation is evidence framing. Relevant passages may discuss background science, related entities, or causal mechanisms without repeating the exact claim wording. Translation can also reduce exact lexical overlap.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.3713, hit@10 of 0.7950, and recall@100 of 0.8063. Dense retrieval is the strongest top-rank profile.

This indicates that embedding similarity is useful for connecting climate claims to scientific evidence passages, especially when the evidence is paraphrased or indirect.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 8 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.3245, hit@10 of 0.7700, and recall@100 of 0.8126. Hybrid retrieval has the best recall@100 but lower early ranking than dense retrieval.

This suggests that sparse climate terms help widen the evidence pool, while dense retrieval better orders the strongest evidence. Hybrid is useful when a reranker can evaluate claim-evidence relation explicitly.

### Metric Interpretation for Model Researchers

Because most queries have multiple positives, nDCG@10 measures whether relevant evidence appears early, hit@10 measures whether at least one relevant passage appears in the first ten, and recall@100 measures evidence coverage for reranking.

For `climate_fever_vn`, hit@10 alone is not enough. A fact-checking retriever should return multiple evidence passages that cover the scientific context behind the claim.

### Query and Relevance Type Tendencies

Queries are Vietnamese translated climate claims. Relevant documents are evidence passages about climate science, environmental effects, greenhouse gases, models, sea level, weather, and related entities.

Relevance is evidence usefulness for verification. A passage can be climate-related but non-relevant if it does not support, refute, or contextualize the specific claim.

### Representative Failure Modes

Common failures include retrieving broad climate pages without the needed evidence, missing paraphrased scientific relations, confusing related entities, and overmatching climate keywords. BM25 is term-driven; dense retrieval can still retrieve topically related but evidentially weak passages.

### Training Data That May Help

Useful training data includes Climate-FEVER data with overlap removed, FEVER-style claim-evidence retrieval pairs, Vietnamese climate or science fact-checking data, and multilingual climate evidence retrieval pairs. Evaluation claims, evidence passages, and qrels should be excluded.

### Model Improvement Notes

Models should encode claim-evidence entailment, climate terminology, numbers, causal relations, and uncertainty. Hard negatives should share climate vocabulary but fail to verify the claim. Dense retrieval is the strongest first-stage ranker, while hybrid retrieval is useful for recall-oriented reranking.

## Example Data

| Query | Positive document |
| --- | --- |
| Ở Alaska, gấu nâu đang thay đổi thói quen ăn uống của chúng để ăn quả mâm xôi chín sớm hơn. [91 chars] | Gấu nâu Gấu nâu (Ursus arctos) là một loài gấu lớn với sự phân bố rộng nhất trong số các loài gấu còn sinh tồn. Loài này được tìm thấy ở hầu hết các vùng phía bắc của châu Âu và Bắc Mỹ. Đây là một tro... [200 / 1,643 chars] |
| Chúng ta sẽ phải đối mặt với nhiệt độ cực cao, nhưng ở mức độ dễ chịu hơn rất nhiều so với nếu chúng... [100 / 147 chars] | Thay đổi khí hậu và giới tính Thay đổi khí hậu và giới tính liên quan đến sự khác biệt về giới trong bối cảnh thay đổi khí hậu và các mối quan hệ quyền lực phức tạp, đan xen phát sinh từ đó. Bằng cách... [200 / 1,439 chars] |
| Họ nói với chúng ta rằng chúng ta là những lực lượng chính điều khiển nhiệt độ trên Trái Đất bằng cá... [100 / 180 chars] | Khí cacbonic Khí cacbonic ( công thức hóa học: CO2) là một khí vô màu với mật độ cao hơn khoảng 60% so với không khí (1,225 g/L), ở nồng độ thông thường nó không có mùi. Khí cacbonic bao gồm một nguyê... [200 / 1,882 chars] |
| Nhai nhổ bọt của bò gây tác hại đến khí hậu hơn tất cả những chiếc xe hơi trên hành tinh này. [93 chars] | Trái Đất Trái Đất ( từ Eorðe -LSB- Γαῖα , Gaia -RSB- Terra ) , còn được gọi là Thế giới hay Trái cầu, là hành tinh thứ ba tính từ Mặt Trời và là vật thể duy nhất trong vũ trụ được biết đến có sự sống.... [200 / 978 chars] |
| Ngoài ra [mô hình khí hậu] bỏ qua thực tế là việc làm giàu khí quyển với CO2 có lợi. [84 chars] | Giảm nhẹ biến đổi khí hậu Giảm nhẹ biến đổi khí hậu bao gồm các hành động nhằm hạn chế mức độ hoặc tốc độ của biến đổi khí hậu trong dài hạn. Giảm nhẹ biến đổi khí hậu nói chung liên quan đến việc giả... [200 / 2,205 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims | 2020 | arXiv paper | [https://arxiv.org/abs/2012.00614](https://arxiv.org/abs/2012.00614) |
| VN-MTEB: Vietnamese Massive Text Embedding Benchmark | 2026 | ACL paper | [https://aclanthology.org/2026.findings-eacl.86/](https://aclanthology.org/2026.findings-eacl.86/) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| GreenNode/climate-fever-vn |  | dataset card | [https://huggingface.co/datasets/GreenNode/climate-fever-vn](https://huggingface.co/datasets/GreenNode/climate-fever-vn) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| A claim says brown bears in Alaska are changing feeding habits because berries ripen earlier. | Evidence passage about brown bears and their distribution. |
| A claim says climate action will still leave extreme temperatures but less severe than no action. | Evidence passage about climate change impacts and social context. |
| A claim says humans drive Earth's temperature by burning fossil fuels and emitting CO2. | Evidence passage about carbon dioxide properties and atmospheric role. |
| A claim compares cattle emissions with emissions from all cars. | Evidence passage about Earth and environmental context. |
| A claim says climate models ignore benefits of atmospheric CO2 enrichment. | Evidence passage about climate change mitigation and greenhouse gases. |
