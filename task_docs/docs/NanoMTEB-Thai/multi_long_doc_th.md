# NanoMTEB-Thai / multi_long_doc_th

## Overview

`NanoMTEB-Thai / multi_long_doc_th` is the Thai split of MultiLongDocRetrieval. It is a long-document retrieval stress test: generated Thai questions must retrieve the full Thai document that contains the local evidence used to form the question. The task is linked to the MLDR and M3-Embedding line of work, where multilingual retrieval is evaluated across longer and noisier documents than ordinary passage benchmarks. In this Nano split, document length is the defining feature: each query has one positive document, and the average document is roughly 25,993 characters. The task is therefore useful for studying long-context representation, noisy web text, and the limits of embedding models that compress entire documents into a single vector.

## Details

### What the Original Data Measures

MultiLongDocRetrieval evaluates whether a retriever can identify a long source document from a question generated from a smaller part of that document. The retrieval target is not the specific paragraph; it is the entire document. This makes the benchmark different from passage retrieval, where the relevant evidence is already localized.

The Thai split combines Thai queries with very long Thai or Thai-heavy documents. Some documents contain web boilerplate, navigation text, mixed-language fragments, or low-quality generated text. A model must connect the query to the relevant local span while ranking the whole document.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Each query has exactly one positive document. Queries average 107.79 characters, and documents average 25,993.27 characters.

The examples show a noisy long-document environment: chemistry exam pages, phone-number or numerology pages, mixed English/Thai web pages, gambling-like pages, and accommodation-listing pages. Some queries include prefixes such as `คำถาม:` or generated-question phrasing. This is not a clean encyclopedic passage task; it is closer to retrieval over messy long web documents.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.3684, hit@10 of 0.4200, and recall@100 of 0.5600. BM25 is stronger than dense retrieval on this split, which is consistent with the long-document setting. Very long documents contain many lexical hooks, and generated questions often reuse distinctive phrases from the source text.

The same property also causes false positives. Long noisy pages may share repeated terms, boilerplate, or topic vocabulary without being the labeled source document. BM25 succeeds when rare terms or copied phrases identify the document, but it struggles when common web text or repeated templates dominate the scoring signal.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.2125, hit@10 of 0.2950, and recall@100 of 0.5350. Dense retrieval is weaker than BM25 in top-rank quality and slightly weaker in recall@100. This suggests that single-vector dense representations have difficulty preserving the local evidence signal inside very long, noisy documents.

For model researchers, this is an important negative case for ordinary embedding retrieval. A question may correspond to a small paragraph or phrase buried in tens of thousands of characters. If the document embedding is dominated by boilerplate, unrelated sections, or broad topic drift, semantic similarity to the query becomes diluted.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 71 queries carrying a rank-101 safeguard positive. It reaches nDCG@10 of 0.3672, hit@10 of 0.5050, and recall@100 of 0.6450. The hybrid pool has the best hit@10 and recall@100, while BM25 and hybrid are nearly tied on nDCG@10.

This pattern shows that dense retrieval still contributes complementary candidates even though BM25 is the stronger standalone first-stage system. Hybrid retrieval is therefore the most practical candidate-generation strategy for this task. The high number of safeguard rows also shows that many positives are difficult to keep inside a strict top-100 window without explicit coverage protection.

### Metric Interpretation for Model Researchers

This split should be read as a long-document candidate-generation benchmark as much as a ranking benchmark. Recall@100 is especially important because a reranker cannot recover a positive document that the first stage fails to include. nDCG@10 remains important, but the main research signal is whether a retrieval method can keep local evidence visible despite extreme document length.

The single-positive setup makes false positives costly. A long document that is topically similar or shares boilerplate is still wrong unless it is the exact source document.

### Query and Relevance Type Tendencies

Queries are longer than ordinary Thai retrieval questions and often look generated. They may ask about a specific detail, phrase, recommendation, or procedure found inside a long source page. Relevant documents are full long documents, not extracted passages.

The relevance relation is source-document identity. The correct document is the one from which the question's evidence was derived, even if other documents contain similar language.

### Representative Failure Modes

Common failures include matching repeated boilerplate instead of the source page, losing the relevant paragraph inside the document embedding, retrieving another web page with similar template text, and over-weighting common Thai or mixed-language fragments. Dense systems may compress away the relevant detail; sparse systems may be distracted by copied navigation, spam, or repeated keyword blocks.

### Training Data That May Help

Useful data includes Thai long-document retrieval, paragraph-to-document supervision, noisy web document retrieval, and hard negatives sampled from documents with similar boilerplate or topic vocabulary. Training should include long inputs with local answer-bearing spans and should avoid overfitting to clean article structure only.

### Model Improvement Notes

This task favors retrieval architectures that preserve local evidence in long documents: passage aggregation, late interaction, multi-vector document representations, chunk-aware indexing, or reranking over selected spans. Single-vector dense models should be evaluated carefully, because average document semantics may not reflect the small span that generated the query.

## Example Data

| Query | Positive document |
| --- | --- |
| คำถาม: สารละลายที่มีความเข้มข้นเท่ากันทุกสารละลายจะมีค่า pH สูงสุดเมื่อใด? [74 chars] | ข้อเอ็นทรานซ์ เคมี 2537 \| วิชาการ.คอม ข้อเอ็นทรานซ์ เคมี 2537 วิชา : เคมี จำนวน : 88 ข้อ ผู้เข้าชม : 2,262 การประลองฝีมือ : 67 view stats 1 ) กำหนดให้ อุณหภูมิ () น้ำแข็ง 0 น้ำ 0 ไอน้ำ 100 ถ้าน้ำแข็งที่ 0 เปลี่ยนสถานะเป็นไอน้ำที่ 100 ที่ความดัน 1 บรรยากาศ จะต้องใช้พลังงานกี่กิโลจูล a + b + c + d d - c + b - a c + d - a + d คำชี้แจง ใช้ข้อมูลต่อไปนี้ตอบคำถามข้อ 2 และ 3 ระยะทางที่สารเคลื่อนที่ (cm) 2 ) การศึกษาสารต้วอย่าง X , Y และ Z ได้ผลดังนี้ 7.5 , 12.2 7.5 , 9.0 4.0 , 2.2 7.4 , 6.0 4.0 , 6.0 , 2.0 9 , 10.8 , 7.2 ข้อสรุปใดถูกเกี่ยวกับองค์ประกอบของ X , Y , Z 3 ) พิจารณาข้อความต่อไปนี้ ก. Rf ของ A ใน III > Rf ของ A ใน I ข. Rf ของ B ใน I = Rf ของ A ใน III ค. Rf ของ A ใน II > Rf ของ D ใน I ง. Rf ของ B ใน II = Rf ของ D ใน III ข้อใดถูก (ก) และ (ข) (ก) และ (ค) (ข) และ (ง) (ค) และ (ง) 4 ) นำสารละลายชุดหนึ่งซึ่งมีร้อยละของสารองค์ประกอบ A และ B ต่าง ๆ กัน มาทำการทดลองกลั่น เพื่อหาจุดเดือดของสารละลาย ผลการทดลองเป็นดังนี้ ร้อยละของสารองค์ประกอบในสารละลาย A ร้อยละของสารองค์ประกอบในสารละลาย B อุณหภ... [1,000 / 19,534 chars] |
| คำถาม: วิธีเลือกเบอร์โทรศัพท์มงคลเบอร์สวยคืออะไรและทำไมเบอร์ 05-6071-0290 ถือเป็นเบอร์สวย? [90 chars] | 0815529736 ผลรวม 46 ซิมเบอร์สวย เบอร์รายเดือน สี่จี 08-1552-9736 เช็คดวงจากเบอร์มือถือ ศูนย์แปดหนึ่งห้าห้าสองเก้าเจ็ดสามหก 081-5529736, 081-552-9736, 081-5529-736, Zero Eight One Five Five Two Nine Seven Three Six 0531206356 ผลรวม 31 ซิมเบอร์สวย เบอร์สวย ทีโอที ทรีจี 05-3120-6356 เลือกเบอร์ ศูนย์ห้าสามหนึ่งสองศูนย์หกสามห้าหก 053-1206356, 053-120-6356, 053-1206-356, Zero Five Three One Two Zero Six Three Five Six 0604467802 ผลรวม 37 ซิมเบอร์สวย เบอร์เติมเงิน i-mobile 06-0446-7802 ราคาเบอร์สวย ศูนย์หกศูนย์สี่สี่หกเจ็ดแปดศูนย์สอง 060-4467802, 060-446-7802, 060-4467-802, Zero Six Zero Four Four Six Seven Eight Zero Two 0804181885 ผลรวม 43 ซิมเบอร์สวย เบอร์ ทีโอที 08-0418-1885 ซื้อเบอร์สวย ศูนย์แปดศูนย์สี่หนึ่งแปดหนึ่งแปดแปดห้า 080-4181885, 080-418-1885, 080-4181-885, Zero Eight Zero Four One Eight One Eight Eight Five 0726699901 ผลรวม 49 ซิมเบอร์สวย เบอร์สวย imobile 3GX 07-2669-9901 ทำนายเบอร์สวย ศูนย์เจ็ดสองหกหกเก้าเก้าเก้าศูนย์หนึ่ง 072-6699901, 072-669-9901, 072-6699-901, Zero Seven Two... [1,000 / 20,760 chars] |
| s question: How does the code above select all list items on the page and bind a handler function to the click event of each list item using jQuery's? [150 chars] | กันยายน 18, 2019 มกราคม 4, 2020 - by admin My post on worldventures is just a tiny fraction of what this website is about. Archived from the original on 15 july seyedolshohada hospital. Compatible with most leg profiles the versatile and telescopic mini tool bar will rotate independently on a single seat box leg and includes 2 quick release accessory blocks, which can be fitted horizontally or vertically, for securely and quickly attaching keepnets, pole socks and other accessories. It was sunny and warm, but a strong wind had risen and it was blowing clouds over us — they seemed to float like big, ethereal germany american senior singles online dating website tall ships on the top of hour heads. These include: the united states canadian seniors online dating site in sideshow bob he added a category called “revenge manster”. Module 1: the company includes: the role of the company secretary types of companies incorporation stakeholders of a company the board of directors. In fact, your... [1,000 / 27,254 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation | 2024 | paper | [https://arxiv.org/abs/2402.03216](https://arxiv.org/abs/2402.03216) |
| mteb/MultiLongDocRetrieval |  | dataset card | [https://huggingface.co/datasets/mteb/MultiLongDocRetrieval](https://huggingface.co/datasets/mteb/MultiLongDocRetrieval) |
| MTEB: Massive Text Embedding Benchmark | 2022 | paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| คำถาม: สารละลายที่มีความเข้มข้นเท่ากันทุกสารละลายจะมีค่า pH สูงสุดเมื่อใด? | A long Thai chemistry exam page containing many questions, answer choices, and educational-site navigation text. |
| คำถาม: วิธีเลือกเบอร์โทรศัพท์มงคลเบอร์สวยคืออะไรและทำไมเบอร์ 05-6071-0290 ถือเป็นเบอร์สวย? | A long Thai phone-number page with repeated number forms, numerology-style text, and sales-oriented content. |
| s question: How does the code above select all list items on the page and bind a handler function to the click event of each list item using jQuery's? | A noisy mixed-language web document with English fragments, archived-page text, and unrelated sections. |
| สามารถสร้างคำถามที่เจาะจงและมีคุณค่าจากข้อความดังกล่าวได้เป็นดังนี้: | A long Thai gambling or promotion-like page containing repeated promotional and navigation terms. |
| คำถามที่สร้างขึ้น: "Daniela ตอบสนองทันทีเพื่อแก้ไขปัญหา คุณสามารถแนะนำให้พักอยู่กับ Daniela ได้อย่างเต็มใจหรือไม่?" | A long accommodation-listing style page with location filters, host-related text, and review-like content. |
