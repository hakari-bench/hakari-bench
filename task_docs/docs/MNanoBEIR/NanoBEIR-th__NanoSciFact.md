# MNanoBEIR / NanoBEIR-th / NanoSciFact

## Overview

NanoSciFact in the Thai NanoBEIR slice is a scientific evidence retrieval task derived from SciFact. The queries are Thai translated scientific claims, and the corpus contains Thai translated scientific abstracts. The retrieval goal is to find abstracts that provide evidence for each claim, not merely papers in the same broad topic area. This makes the task a compact benchmark for Thai scientific claim retrieval, biomedical evidence matching, and fact-checking-oriented search.

## Details

### What the Original Data Measures

SciFact evaluates scientific claim verification using research abstracts. In retrieval form, a model receives a claim and must retrieve an abstract containing evidence needed to assess it. The relevant abstract may discuss a specific biological mechanism, clinical result, intervention, gene, disease, or experimental finding.

The Thai translated version adds multilingual and domain-specific pressure. Claims are long and technical, and abstracts contain dense biomedical language. A strong retriever must preserve exact scientific terms such as gene names or diseases while also recognizing the evidence relation when the abstract phrases it differently.

### Observed Data Profile

The task contains 50 queries, 2,919 documents, and 56 relevance judgments. Most queries have one positive abstract, with an average of 1.12 positives per query. The minimum is 1, the median is 1.0, the maximum is 4, and 4 queries are multi-positive, or 8.0% of the query set. This is mostly a single-evidence retrieval task.

Queries average 92.74 characters, while documents average 1,328.85 characters. The claims are already fairly long, but the abstracts are much longer and may include background, method, result, and conclusion text. The model must identify the abstract that evidences the claim, not only the abstract that shares the most terminology.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6334, hit@10 of 0.7800, and recall@100 of 0.8571 using the top-500 BM25 candidate subset. This is a strong lexical baseline. Scientific claims often contain distinctive biomedical terms, and exact matching can identify many candidate abstracts.

The result still leaves room for evidence-sensitive ranking. A same-entity abstract may not support the claim, and a relevant abstract may express the same finding through different wording. BM25 can locate the right scientific neighborhood, but it does not fully model the claim-evidence relation.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.5713, hit@10 of 0.7200, and recall@100 of 0.8571. Dense retrieval matches BM25 recall@100 but is weaker on top-rank metrics. This suggests that exact scientific terminology is especially important in this Thai SciFact slice, and the dense model may over-rank semantically related but non-evidential abstracts.

The dense profile remains useful as a semantic complement, but it does not outperform lexical matching directly. Scientific evidence retrieval requires precise relation matching, not only broad semantic relatedness. General embeddings can blur abstracts that discuss the same disease, gene, or method while differing in the claim outcome.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.6206, hit@10 of 0.7400, and recall@100 of 0.9286. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 4 safeguard rows and a mean of 100.08 candidates. The hybrid profile has the best recall@100, while BM25 has the strongest nDCG@10 and hit@10.

This indicates that hybrid search improves evidence candidate coverage but does not fully improve first-page ordering. Combining lexical and dense candidates helps recover more positives by rank 100, but the top ranks still depend heavily on precise biomedical term matching. A downstream reranker could benefit from the hybrid pool if it can judge the claim-abstract evidence relation.

### Metric Interpretation for Model Researchers

nDCG@10 is the key direct ranking metric because scientific evidence should appear in the first page for a verifier or reader. hit@10 measures whether at least one evidence abstract is visible, while recall@100 measures whether a reranker has access to the evidence. Since most queries have one positive, top-rank ordering is especially important.

The method comparison shows that Thai SciFact is lexically anchored. BM25 performs best at the top, dense retrieval does not improve ordering, and reranking_hybrid improves recall. This is useful for diagnosing whether a model can handle precise scientific terminology and whether hybrid search provides candidate coverage without degrading top-rank evidence quality.

### Query and Relevance Type Tendencies

Queries are long scientific claims, often biomedical. Examples involve Ly49Q and neutrophil migration, antiretroviral therapy and tuberculosis, interferon-induced genes and West Nile virus, HPV detection for cervical cancer screening, and TDP-43 interactions in neuronal loss. Relevant documents are abstracts containing experimental or clinical evidence.

The task rewards models that preserve technical detail. Small changes in genes, proteins, diseases, treatments, or causal relations can change relevance. A broadly related biomedical abstract is not enough if it does not provide the evidence needed for the claim.

### Representative Failure Modes

Likely failures include retrieving abstracts that mention the same entity but not the claim outcome, confusing support evidence with background, missing evidence because Thai translation changes terminology, and over-ranking abstracts with similar biomedical vocabulary. Dense models may retrieve same-topic non-evidence, while BM25 may miss paraphrased evidence.

### Training Data That May Help

Useful training data includes scientific claim verification, biomedical abstract retrieval, Thai scientific QA, multilingual evidence retrieval, and hard negatives that share entities or methods but do not support the claim. Thai biomedical terminology resources and segmentation-aware preprocessing can help. For rerankers, close non-evidence abstracts are especially valuable.

### Model Improvement Notes

A model targeting this task should combine biomedical term precision with evidence-aware reasoning. Sparse systems should maintain strong exact matching for scientific names. Dense systems need domain-specific hard-negative training to distinguish evidence from topical relatedness. Hybrid systems should exploit their stronger recall with a reranker that compares the claim and abstract in detail.

## Example Data

| Query | Positive document |
| --- | --- |
| การควบคุมฟังก์ชันของเมมเบรนราฟต์ของ Ly49Q ในการเคลื่อนที่ของนิวโทรฟิลไปยังจุดอักเสบ [83 chars] | นิวโทรฟิลจะเกิดการพอระเบียบและเคลื่อนที่ในทิศทางอย่างรวดเร็วเพื่อแทรกซึมเข้าสู่จุดติดเชื้อและการอักเสบ ที่นี่เราจะแสดงให้เห็นว่า ตัวรับ MHC I ที่มีฤทธิ์ยับยั้ง Ly49Q มีความสำคัญต่อการพอระเบียบอย่างรวดเร็วและการแทรกซึมของนิวโทรฟิลในเนื้อเยื่อ ในสภาวะปกติ Ly49Q จะยับยั้งการยึดเกาะของนิวโทรฟิลโดยการป้องกันการ形成ของโฟกัลคอมเพล็กซ์ ซึ่งน่าจะเกิดจากการยับยั้ง Src และ PI3 kinase อย่างไรก็ตาม ในการมีอยู่ของสิ่งกระตุ้นการอักเสบ Ly49Q จะทำหน้าที่ในการพอระเบียบและการแทรกซึมของนิวโทรฟิลอย่างรวดเร็วในลักษณะที่ขึ้นอยู่กับโดเมน ITIM ฟังก์ชันที่ตรงกันข้ามเหล่านี้ดูเหมือนจะถูกควบคุมโดยการใช้ฟอสฟาเทส SHP-1 และ SHP-2 ที่แตกต่างกัน การพอระเบียบและการเคลื่อนที่ที่ขึ้นอยู่กับ Ly49Q ได้รับผลกระทบจากการควบคุมฟังก์ชันของเมมเบรนแรฟท์โดย Ly49Q เราขอเสนอว่า Ly49Q มีบทบาทสำคัญในการเปลี่ยนแปลงนิวโทรฟิลให้มีรูปร่างที่พอระเบียบและการเคลื่อนที่อย่างรวดเร็วเมื่อเกิดการอักเสบ ผ่านการควบคุมเชิงพื้นที่และเวลาเกี่ยวกับเมมเบรนแรฟท์และโมเลกุลสัญญาณที่เกี่ยวข้องกับแรฟท์ [942 chars] |
| การบำบัดด้วยยาต้านไวรัสและผลกระทบต่อการลดอัตราการติดเชื้อวัณโรคในกลุ่ม CD4 ที่หลากหลาย [86 chars] | พื้นหลัง การติดเชื้อไวรัสภูมิคุ้มกันบกพร่องของมนุษย์ (HIV) เป็นปัจจัยเสี่ยงที่สำคัญที่สุดในการพัฒนาวัณโรคและได้กระตุ้นให้เกิดการกลับมาของโรคนี้ โดยเฉพาะในแอฟริกาตอนใต้ของซาฮารา ในปี 2010 มีการประมาณว่ามีผู้ป่วยวัณโรคใหม่ประมาณ 1.1 ล้านรายในกลุ่มคน 34 ล้านคนที่มีชีวิตอยู่กับ HIV ทั่วโลก การบำบัดด้วยยาต้านไวรัสมีศักยภาพอย่างมากในการป้องกันวัณโรคที่เกี่ยวข้องกับ HIV เราได้ทำการทบทวนอย่างเป็นระบบเกี่ยวกับการศึกษาที่วิเคราะห์ผลกระทบของการบำบัดด้วยยาต้านไวรัสต่ออุบัติการณ์ของวัณโรคในผู้ใหญ่ที่ติดเชื้อ HIV วิธีการและผลการศึกษา ได้มีการค้นหาอย่างเป็นระบบใน PubMed, Embase, African Index Medicus, LILACS และทะเบียนการทดลองทางคลินิก การทดลองแบบสุ่มควบคุม, การศึกษาแบบกลุ่มตาม prospective และการศึกษาแบบกลุ่มตาม retrospective ถูกนำมารวมไว้หากเปรียบเทียบอุบัติการณ์ของวัณโรคตามสถานะการบำบัดด้วยยาต้านไวรัสในผู้ใหญ่ที่ติดเชื้อ HIV เป็นระยะเวลามากกว่า 6 เดือนในประเทศที่กำลังพัฒนา สำหรับการวิเคราะห์เมตา มีการจัดกลุ่มเป็นสี่ประเภทตามจำนวน CD4 ณ จุดเริ่มต้นการบำบัดด้วยยาต้านไวรัส: (1) น้อยกว่า 200 เซลล์/µl,... [1,000 / 1,895 chars] |
| การเพิ่มการแสดงออกอย่างรวดเร็วและการแสดงออกพื้นฐานที่สูงขึ้นของยีนที่กระตุ้นโดยอินเตอร์เฟอรอนลดการอยู่รอดของเซลล์ประสาทเกรนูลที่ติดเชื้อไวรัสเวสต์ไนล์หรือไม่? [158 chars] | แม้ว่าความไวของเซลล์ประสาทในสมองต่อการติดเชื้อจุลินทรีย์จะเป็นปัจจัยหลักที่กำหนดผลลัพธ์ทางคลินิก แต่ข้อมูลเกี่ยวกับปัจจัยโมเลกุลที่ควบคุมความเปราะบางนี้ยังมีน้อย ที่นี่เราจะแสดงให้เห็นว่าเซลล์ประสาทสองประเภทจากภูมิภาคสมองที่แตกต่างกันมีความสามารถในการอนุญาตต่อการจำลองของไวรัส RNA เชิงบวกหลายชนิดแตกต่างกัน เซลล์ประสาทเกรนูลในสมองน้อยและเซลล์ประสาทในเปลือกสมองมีโปรแกรมภูมิคุ้มกันที่เป็นเอกลักษณ์ซึ่งทำให้เกิดความไวที่แตกต่างต่อการติดเชื้อไวรัสทั้งในสภาพ ex vivo และ in vivo โดยการถ่ายทอดเซลล์ประสาทในเปลือกสมองด้วยยีนที่แสดงออกสูงกว่าในเซลล์ประสาทเกรนูล เราได้ระบุยีนที่กระตุ้นโดยอินเตอร์เฟอรอนสามตัว (ISGs; Ifi27, Irg1 และ Rsad2 (ที่รู้จักกันในชื่อ Viperin)) ที่ช่วยในการต่อต้านไวรัสต่อไวรัสที่มีผลต่อระบบประสาทที่แตกต่างกัน นอกจากนี้ เรายังพบว่าสถานะเอพิเจเนติกและการควบคุมของ ISGs โดยไมโครRNA (miRNA) มีความสัมพันธ์กับการตอบสนองต่อไวรัสที่เพิ่มขึ้นในเซลล์ประสาทเกรนูล ดังนั้น เซลล์ประสาทจากภูมิภาคสมองที่มีวิวัฒนาการแตกต่างกันจึงมีลายเซ็นภูมิคุ้มกันที่เป็นเอกลักษณ์ ซึ่งอาจมีส่วนช่วยในการอนุญาตต่... [1,000 / 1,021 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [SciFact](https://arxiv.org/abs/2004.14974) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-th dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |

Representative query and positive abstract snippets:

| Query | Positive document snippet |
| --- | --- |
| การควบคุมฟังก์ชันของเมมเบรนราฟต์ของ Ly49Q ในการเคลื่อนที่ของนิวโทรฟิลไปยังจุดอักเสบ | นิวโทรฟิลจะเกิดการพอระเบียบและเคลื่อนที่ในทิศทางอย่างรวดเร็วเพื่อแทรกซึมเข้าสู่จุดติดเชื้อ... |
| การบำบัดด้วยยาต้านไวรัสและผลกระทบต่อการลดอัตราการติดเชื้อวัณโรคในกลุ่ม CD4 ที่หลากหลาย | พื้นหลัง การติดเชื้อไวรัสภูมิคุ้มกันบกพร่องของมนุษย์ (HIV)... |
| การเพิ่มการแสดงออกอย่างรวดเร็วและการแสดงออกพื้นฐานที่สูงขึ้นของยีนที่กระตุ้นโดยอินเตอร์เฟอรอนลดการอยู่รอดของเซลล์ประสาทเกรนูลที่ติดเชื้อไวรัสเวสต์ไนล์หรือไม่? | แม้ว่าความไวของเซลล์ประสาทในสมองต่อการติดเชื้อจุลินทรีย์จะเป็นปัจจัยหลัก... |
| การตรวจคัดกรองมะเร็งปากมดลูกขั้นต้นด้วยการตรวจหา HPV มีความไวเชิงยาวที่สูงกว่าซิโทโลยีแบบดั้งเดิมในการตรวจหานีโอพลาสเซียในปากมดลูกเกรด 2 หรือไม่? | ภูมิหลัง การคัดกรองมะเร็งปากมดลูกโดยอิงจากการตรวจหาเชื้อไวรัส HPV... |
| การบล็อกการมีปฏิสัมพันธ์ระหว่าง TDP-43 กับโปรตีนที่เกี่ยวข้องกับระบบหายใจซับซ้อน I ND3 และ ND6 ส่งผลให้เกิดการสูญเสียเซลล์ประสาทที่เกิดจาก TDP-43 เพิ่มขึ้น | การกลายพันธุ์ทางพันธุกรรมในโปรตีนที่จับกับดีเอ็นเอ TAR... |
