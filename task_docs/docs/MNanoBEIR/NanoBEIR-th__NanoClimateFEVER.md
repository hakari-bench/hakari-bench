# MNanoBEIR / NanoBEIR-th / NanoClimateFEVER

## Overview

NanoClimateFEVER in the Thai NanoBEIR slice is a climate claim evidence retrieval task derived from CLIMATE-FEVER. The queries are Thai translated climate-related claims, and the corpus contains Thai translated evidence passages. The retrieval goal is to find passages that help verify or contextualize claims about climate science, global warming, sea level, storms, solar activity, or attribution. It is a compact diagnostic for multilingual scientific fact-checking retrieval in Thai.

## Details

### What the Original Data Measures

CLIMATE-FEVER evaluates evidence retrieval for real-world climate claims. A relevant passage must bear on the specific claim, not merely discuss the same climate topic. The claim may involve a time span, trend, scientific attribution, statistical qualifier, or causal explanation, so the retrieval model must preserve both content and factual relation.

The Thai translated version adds challenges from long claims, long evidence passages, and Thai text segmentation. Climate terminology can be shared across query and evidence, but relevant passages may express the verifying information through broader scientific context or paraphrase. A strong model needs both exact scientific anchors and semantic evidence matching.

### Observed Data Profile

The task contains 50 queries, 3,408 documents, and 148 relevance judgments. Most queries are multi-positive, with an average of 2.96 positives per query. The minimum is 1, the median is 3.0, the maximum is 5, and 44 queries are multi-positive, or 88.0% of the query set. This makes the benchmark a multi-evidence retrieval task.

Queries average 118.64 characters, while documents average 1,395.41 characters. The claims are full factual assertions, and the evidence passages are much longer explanatory texts. The relevant evidence may be a small part of the document, so broad topical matching is not enough.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2368, hit@10 of 0.5400, and recall@100 of 0.5270 using the top-500 BM25 candidate subset. This is a limited lexical profile. Climate terms can help candidate discovery, but exact overlap alone often fails to rank or recover the full evidence set.

The weakness is especially visible in hit@10 and recall@100. Many claims contain qualifiers such as time range, trend direction, statistical significance, or attribution. BM25 may retrieve passages that share climate vocabulary but do not verify the claim. Thai segmentation and translated wording can further reduce exact lexical alignment.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.3444, hit@10 of 0.7400, and recall@100 of 0.6419. Dense retrieval improves substantially over BM25 across all metrics. This indicates that embedding similarity captures claim-evidence semantic relationships that lexical matching misses.

The dense advantage is important for climate fact-checking because evidence often appears as explanatory context rather than a sentence with the same words as the claim. Still, the task remains difficult: a dense model can retrieve passages about the same climate phenomenon without necessarily retrieving the passage that verifies the exact claim.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.3015, hit@10 of 0.7600, and recall@100 of 0.6622. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 2 safeguard rows and a mean of 100.04 candidates. The hybrid profile has the best hit@10 and recall@100, while dense retrieval has the best nDCG@10.

This pattern suggests that hybrid search broadens candidate coverage and increases the chance of at least one evidence passage appearing near the top. However, dense retrieval orders the top-10 set better overall. For Thai Climate-FEVER, reranking_hybrid is a strong candidate source, but a better evidence-aware reranker is needed to turn its coverage into the best graded ranking.

### Metric Interpretation for Model Researchers

nDCG@10 measures whether evidence passages are ranked highly enough for a fact-checking or RAG system to use. hit@10 indicates whether at least one evidence passage is visible, while recall@100 measures whether a later reranker can access the evidence set. Because most queries have multiple positives, recall matters more than it would in a single-answer task.

The comparison shows that BM25 is too dependent on exact climate wording, dense retrieval is the strongest top-rank semantic matcher, and reranking_hybrid gives the broadest candidate access. This task is useful for evaluating whether a model improves claim-specific evidence ranking or only retrieves broad climate-topic passages.

### Query and Relevance Type Tendencies

Queries are full climate claims, often about warming periods, statistical trends, local and regional sea level, Hurricane Harvey, global warming attribution, or cosmic rays. Relevant passages are explanatory evidence passages that may define a phenomenon, describe a scientific mechanism, or summarize attribution evidence.

The task rewards models that preserve qualifiers and causal relations. A passage about sea level is not enough if the claim concerns local variation; a passage about global warming is not enough if the claim concerns a specific attribution mechanism. This evidence specificity is the core challenge.

### Representative Failure Modes

Likely failures include retrieving same-topic climate passages that do not verify the claim, missing evidence because the Thai translation uses different wording, ignoring statistical or causal qualifiers, and over-ranking broad climate explanations. BM25 is vulnerable to vocabulary mismatch, while dense retrieval can overgeneralize from topic similarity.

### Training Data That May Help

Useful training data includes climate claim verification, Thai or multilingual fact-checking, scientific evidence retrieval, and hard negatives that share climate terms but fail to verify the claim. Thai scientific and public-policy text can help with language coverage. For rerankers, near-topic non-evidence passages are especially important.

### Model Improvement Notes

A model targeting this task should improve claim-specific evidence matching. Sparse systems need Thai-aware tokenization and scientific term normalization. Dense systems need better handling of numerical, causal, and negation-like qualifiers. Hybrid systems should use their coverage advantage with a reranker that reads the claim-passage relation more explicitly.

## Example Data

| Query | Positive document |
| --- | --- |
| ตั้งแต่ปี 1970 จนถึงปี 1998 มีช่วงเวลาที่อุณหภูมิสูงขึ้นประมาณ 0.7 ฟาเรนไฮต์ ซึ่งช่วยกระตุ้นการเคลื่อนไหวของผู้ที่เตือนเกี่ยวกับภาวะโลกร้อน [139 chars] | ยุคพาเลโอซีน ( -LSB- pronˈpæliəˌsiːn , _ ˈpæ - , _ - lioʊ - -RSB- ) หรือ พาเลโอซีน ซึ่งหมายถึง "เก่าใหม่" เป็นยุคทางธรณีวิทยาที่มีระยะเวลาประมาณ . มันเป็นยุคแรกของยุคพาเลโอโจเนในยุคเซโนโซอิกสมัยใหม่ เช่นเดียวกับยุคทางธรณีวิทยาหลายยุค ชั้นหินที่กำหนดจุดเริ่มต้นและสิ้นสุดของยุคนี้ได้รับการระบุอย่างชัดเจน แต่ช่วงอายุที่แน่นอนยังคงไม่แน่นอน ยุคพาเลโอซีนเป็นกรอบระยะเวลาสำคัญสองเหตุการณ์ในประวัติศาสตร์โลก มันเริ่มต้นด้วยเหตุการณ์การสูญพันธุ์ครั้งใหญ่ที่สิ้นสุดยุคครีเทเชียส ซึ่งรู้จักกันในชื่อขอบเขตครีเทเชียส-พาเลโอโจเน (K-Pg) นี่เป็นช่วงเวลาที่มีการสูญพันธุ์ของไดโนเสาร์ที่ไม่ใช่นก สัตว์เลื้อยคลานขนาดยักษ์ในทะเล และสัตว์พืชอื่นๆ อีกมากมาย การสูญพันธุ์ของไดโนเสาร์ทำให้เกิดช่องทางนิเวศวิทยาที่ว่างเปล่าทั่วโลก ยุคพาเลโอซีนสิ้นสุดลงด้วยจุดสูงสุดทางความร้อนของพาเลโอซีน-อีโอซีน ซึ่งเป็นช่วงเวลาทางธรณีวิทยาที่สั้น ( ~ 0.2 ล้านปี ) ที่มีลักษณะโดยการเปลี่ยนแปลงที่รุนแรงในสภาพอากาศและการหมุนเวียนของคาร์บอน ชื่อ "พาเลโอซีน" มาจากภาษากรีกโบราณและหมายถึง "เก่า (กว่า)" (παλαιός, palaios) "ใหม่" (καινός, ka... [1,000 / 1,033 chars] |
| ในความเป็นจริง แนวโน้ม แม้จะไม่สำคัญทางสถิติ แต่ก็มีแนวโน้มลดลง [63 chars] | วงจรสุริยะหรือวงจรกิจกรรมแม่เหล็กสุริยะคือการเปลี่ยนแปลงที่เกิดขึ้นเป็นระยะเวลาเกือบ 11 ปีในกิจกรรมของดวงอาทิตย์ (รวมถึงการเปลี่ยนแปลงในระดับการแผ่รังสีจากดวงอาทิตย์และการปล่อยวัสดุจากดวงอาทิตย์) และลักษณะ (การเปลี่ยนแปลงในจำนวนและขนาดของจุดด่างบนดวงอาทิตย์ การระเบิด และการแสดงออกอื่น ๆ) ซึ่งได้ถูกสังเกต (จากการเปลี่ยนแปลงในลักษณะของดวงอาทิตย์และจากการเปลี่ยนแปลงที่เห็นบนโลก เช่น แสงเหนือ) มานานหลายศตวรรษ การเปลี่ยนแปลงบนดวงอาทิตย์ทำให้เกิดผลกระทบในอวกาศ ในชั้นบรรยากาศ และบนพื้นผิวของโลก ในขณะที่มันเป็นตัวแปรที่มีอิทธิพลหลักในกิจกรรมของดวงอาทิตย์ การเปลี่ยนแปลงที่ไม่เป็นระยะก็เกิดขึ้นเช่นกัน [598 chars] |
| ระดับน้ำทะเลในท้องถิ่นและระดับภูมิภาคยังคงแสดงความแปรปรวนตามธรรมชาติที่เป็นปกติ—ในบางสถานที่สูงขึ้นและในบางสถานที่ต่ำลง。 [120 chars] | ระดับน้ำทะเลเฉลี่ย (MSL) (ย่อว่า ระดับน้ำทะเล) คือระดับเฉลี่ยของผิวของมหาสมุทรหนึ่งหรือมากกว่าของโลก ซึ่งใช้วัดความสูงเช่นระดับความสูง MSL เป็นประเภทของข้อมูลแนวดิ่งที่เป็นจุดอ้างอิงทางเรขาคณิตที่ได้มาตรฐาน ซึ่งใช้เป็นตัวอย่าง เช่น เป็นข้อมูลแผนที่ในงานแผนที่และการนำทางทางทะเล หรือในอากาศยาน เป็นระดับน้ำทะเลมาตรฐานที่ใช้วัดความดันบรรยากาศเพื่อปรับระดับความสูงและระดับการบินของเครื่องบิน ระดับน้ำทะเลเฉลี่ยที่เป็นที่รู้จักและค่อนข้างตรงไปตรงมาคือจุดกึ่งกลางระหว่างน้ำขึ้นเฉลี่ยต่ำและน้ำขึ้นเฉลี่ยสูงที่สถานที่เฉพาะ ระดับน้ำทะเลสามารถได้รับผลกระทบจากปัจจัยหลายประการและเป็นที่รู้กันว่ามีการเปลี่ยนแปลงอย่างมากในช่วงเวลาทางธรณีวิทยา การวัดความแปรปรวนใน MSL อย่างระมัดระวังสามารถให้ข้อมูลเชิงลึกเกี่ยวกับการเปลี่ยนแปลงสภาพภูมิอากาศที่กำลังดำเนินอยู่ และการเพิ่มขึ้นของระดับน้ำทะเลถูกอ้างถึงอย่างกว้างขวางว่าเป็นหลักฐานของการอบอุ่นของโลกที่กำลังดำเนินอยู่ คำว่า "เหนือระดับน้ำทะเล" โดยทั่วไปหมายถึงเหนือระดับน้ำทะเลเฉลี่ย (AMSL) [925 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [CLIMATE-FEVER](https://arxiv.org/abs/2012.00614) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-th dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |

Representative query and positive evidence snippets:

| Query | Positive document snippet |
| --- | --- |
| ตั้งแต่ปี 1970 จนถึงปี 1998 มีช่วงเวลาที่อุณหภูมิสูงขึ้นประมาณ 0.7 ฟาเรนไฮต์... | ยุคพาเลโอซีน หรือ พาเลโอซีน ซึ่งหมายถึง "เก่าใหม่" เป็นยุคทางธรณีวิทยา... |
| ในความเป็นจริง แนวโน้ม แม้จะไม่สำคัญทางสถิติ แต่ก็มีแนวโน้มลดลง | วงจรสุริยะหรือวงจรกิจกรรมแม่เหล็กสุริยะคือการเปลี่ยนแปลงที่เกิดขึ้นเป็นระยะเวลาเกือบ 11 ปี... |
| ระดับน้ำทะเลในท้องถิ่นและระดับภูมิภาคยังคงแสดงความแปรปรวนตามธรรมชาติ... | ระดับน้ำทะเลเฉลี่ย (MSL) คือระดับเฉลี่ยของผิวของมหาสมุทรหนึ่งหรือมากกว่าของโลก... |
| นักวิทยาศาสตร์ด้านสภาพอากาศกล่าวว่าปัจจัยบางประการในกรณีของพายุเฮอริเคนฮาร์วีย์... | ผลกระทบจากภาวะโลกร้อนคือการเปลี่ยนแปลงทางสิ่งแวดล้อมและสังคมที่เกิดขึ้น... |
| การทดลอง CERN CLOUD ทดสอบเพียงหนึ่งในสามของหนึ่งในสี่ข้อกำหนด... | การระบุสาเหตุของการเปลี่ยนแปลงสภาพภูมิอากาศในช่วงล่าสุดคือความพยายามในการตรวจสอบกลไก... |
