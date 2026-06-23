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
| Ở Alaska, gấu nâu đang thay đổi thói quen ăn uống của chúng để ăn quả mâm xôi chín sớm hơn. [91 chars] | Gấu nâu Gấu nâu (Ursus arctos) là một loài gấu lớn với sự phân bố rộng nhất trong số các loài gấu còn sinh tồn. Loài này được tìm thấy ở hầu hết các vùng phía bắc của châu Âu và Bắc Mỹ. Đây là một trong hai loài ăn thịt lớn nhất trên mặt đất, chỉ có thể sánh ngang về kích thước với họ hàng gần gũi của nó, gấu Bắc Cực (Ursus maritimus), nhưng do có kích thước biến đổi ít hơn nên chúng trung bình lại lớn hơn. Có nhiều phân loại được công nhận nằm trong nhóm gấu nâu, khá nổi tiếng tại những nơi mà chúng sinh sống bản địa. Phạm vi chính của loài này bao gồm những phần thuộc Nga, Trung Á, Trung Quốc, Canada, Hoa Kỳ (chủ yếu Alaska), Scandinavia và vùng Carpathian (đặc biệt Romania), Anatolia và Kavkaz. Gấu nâu được công nhận là quốc thú ở vài nước châu Âu khác nhau . Mặc dù phạm vi sống bị thu hẹp lại và phải đối mặt với việc tuyệt chủng cục bộ nhưng theo Liên minh Bảo tồn Thiên nhiên Quốc tế IUCN thì vẫn xếp lớp nguy cấp thấp cho loài này với tổng số lượng cá thể khoảng 200 nghìn con vào n... [1,000 / 1,643 chars] |
| Chúng ta sẽ phải đối mặt với nhiệt độ cực cao, nhưng ở mức độ dễ chịu hơn rất nhiều so với nếu chúng ta không làm gì để ngăn chặn biến đổi khí hậu. [147 chars] | Thay đổi khí hậu và giới tính Thay đổi khí hậu và giới tính liên quan đến sự khác biệt về giới trong bối cảnh thay đổi khí hậu và các mối quan hệ quyền lực phức tạp, đan xen phát sinh từ đó. Bằng cách thay đổi hệ sinh thái của hành tinh, biến đổi khí hậu, đặc biệt là hiện tượng ấm lên toàn cầu tác động trực tiếp đến loài người. Những ảnh hưởng này khác nhau đối với các phân đoạn dân cư khác nhau, cụ thể là đối với những người thuộc hai giới tính khác nhau. Trong nhiều trường hợp, phụ nữ dễ bị tổn thương hơn trước những tác động tiêu cực của biến đổi khí hậu do vị thế xã hội thấp ở hầu hết các nước trên thế giới . Nhiều phụ nữ nghèo khổ , đặc biệt là ở khu vực đang phát triển , làm nghề nông nghiệp và sống dựa vào môi trường tự nhiên để kiếm ăn và thu nhập . Do hạn chế thêm nữa khả năng tiếp cận vật chất , xã hội , chính trị và nguồn tài chính vốn đã bị thắt chặt trước đây của họ , biến đổi khí hậu thường gánh nặng lên vai phụ nữ hơn nam giới . Cả tại địa phương cũng như toàn cầu cả chí... [1,000 / 1,439 chars] |
| Họ nói với chúng ta rằng chúng ta là những lực lượng chính điều khiển nhiệt độ trên Trái Đất bằng cách đốt cháy nhiên liệu hóa thạch và giải phóng khí carbon dioxide ra môi trường. [180 chars] | Khí cacbonic Khí cacbonic ( công thức hóa học: CO2) là một khí vô màu với mật độ cao hơn khoảng 60% so với không khí (1,225 g/L), ở nồng độ thông thường nó không có mùi. Khí cacbonic bao gồm một nguyên tử cacbon liên kết đôi với hai nguyên tử oxy. Nó xuất hiện tự nhiên trong bầu khí quyển của Trái Đất như một loại khí vi lượng ở nồng độ khoảng 0,04 phần trăm (400 ppm) về thể tích. Nguồn gốc tự nhiên bao gồm núi lửa, suối nước nóng và mạch nước phun hơi nước; nó được giải phóng từ đá vôi bằng cách hòa tan trong nước và axit. Bởi vì khí cacbonic tan trong nước nên nó xuất hiện tự nhiên trong tầng ngầm, sông ngòi và hồ ao, băng hà vĩnh cửu, sông băng và biển mặn. Nó còn tồn tại trong các trầm tích dầu mỏ và ga thiên nhiên . Là nguồn cung cấp carbon sẵn có trong chu trình Carbon , Khí cacbonic trên bầu trời là nguồn bổ sung Carbon chính cho sự sống trên Trái đất cũng như nồng độ của nó đã được điều tiết bởi sinh vật quang hợp cùng những hiện tượng địa chất kể từ thời kỳ tiền Cambri vào cuố... [1,000 / 1,882 chars] |

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
