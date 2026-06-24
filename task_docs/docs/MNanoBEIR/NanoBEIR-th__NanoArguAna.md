# MNanoBEIR / NanoBEIR-th / NanoArguAna

## Overview

NanoArguAna in the Thai NanoBEIR slice is an argument-counterargument retrieval task derived from ArguAna. The queries and documents are Thai translated argumentative passages, and each query has one paired relevant response passage. The benchmark measures whether a retriever can identify argumentative relation, stance contrast, and response fit between long texts. It is a compact but demanding diagnostic for multilingual retrieval where topical similarity alone is not sufficient.

## Details

### What the Original Data Measures

ArguAna is used in BEIR as an argument retrieval task where relevance depends on the relation between an argument and a counterargument. The relevant passage may challenge a premise, present a different stance, or respond to the specific reasoning in the query. A same-topic passage is not automatically relevant if it does not answer the argumentative move.

The Thai translated version adds difficulty from long translated passages and Thai word segmentation. Both query and document are substantial argumentative texts, so the model must compare claims, reasons, and stance across a full discourse unit. Lexical overlap helps identify the debate topic, but the relevant response may not be the passage with the most repeated words.

### Observed Data Profile

The task contains 50 queries, 3,635 documents, and 50 relevance judgments. Every query has exactly one positive passage: the average, minimum, median, and maximum positives per query are all 1.0, and there are no multi-positive queries. This makes the benchmark a precise single-target retrieval task.

Queries average 820.62 characters, and documents average 860.05 characters. Both sides are long compared with ordinary web-search tasks. The length means that simple keyword overlap can find same-topic passages, but ranking the exact paired response requires understanding the argumentative relation across many sentences.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4051, hit@10 of 0.7200, and recall@100 of 0.9400 using the top-500 BM25 candidate subset. This is a strong lexical candidate-generation profile. Long argumentative passages repeat topic words, entities, and policy terms, which gives BM25 useful anchors.

The gap between recall@100 and nDCG@10 is the main signal. BM25 usually gets the correct response into the first 100 ranks, but it often cannot place it in the top 10. That is consistent with ArguAna: many distractors discuss the same topic, while only one passage responds to the query's stance and premise.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.3721, hit@10 of 0.7000, and recall@100 of 0.9000. Dense retrieval is slightly weaker than BM25 on this Thai slice. This suggests that the dense model captures broad argumentative or topical similarity, but exact lexical anchors and long-passage overlap remain especially important for finding the paired response.

The dense weakness does not mean semantics are irrelevant. Rather, it indicates that general embedding similarity may blur stance and response relation in long Thai argumentative text. A dense model can retrieve passages about the same debate while still missing the exact counterargument pair.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.4349, hit@10 of 0.7200, and recall@100 of 0.9200. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 4 safeguard rows and a mean of 100.08 candidates. This is the strongest top-10 ranking profile among the three modes.

The hybrid result shows that Thai ArguAna benefits from combining lexical topic anchors with dense semantic signals. BM25 alone has the best recall@100, but hybrid improves nDCG@10 by better ordering the high-confusion same-topic candidate set. For direct top-rank retrieval, the hybrid profile is the most aligned with the task.

### Metric Interpretation for Model Researchers

Because every query has one positive, nDCG@10 and hit@10 directly measure whether the paired response is visible near the top. recall@100 measures whether a later reranker has a chance to recover it. The task is useful for separating candidate recall from stance-aware ordering: BM25 finds candidates, but hybrid ranks the top list better.

The comparison also warns that dense retrieval alone may not be enough for long Thai argument matching. A model may need language-aware tokenization, Thai discourse coverage, and hard negatives that share topic vocabulary but differ in stance or response target.

### Query and Relevance Type Tendencies

Queries are long argumentative passages about issues such as public indifference to reform, Heathrow expansion, choice overload, cyberattacks by non-state actors, and the relation between religion, hate speech, and free expression. Positives are paired response passages, often counterarguments or passages that qualify the original reasoning.

The task rewards models that understand the target of an argument. A relevant document should respond to the claim being made, not just mention the same policy area. This makes stance, premise, and argumentative role central to relevance.

### Representative Failure Modes

Likely failures include retrieving same-topic passages that do not respond to the query, confusing support and counterargument roles, over-ranking long passages with repeated topic words, and missing the paired response when Thai translation changes wording. Dense models may retrieve semantically related but stance-mismatched passages, while BM25 may overvalue surface overlap.

### Training Data That May Help

Useful training data includes Thai debate retrieval, argument-counterargument pairs, stance-aware ranking, multilingual argument mining, and hard negatives from the same topic but different stance or premise. Thai segmentation-aware preprocessing may help sparse systems. For rerankers, same-topic non-response passages are the most important negative examples.

### Model Improvement Notes

A model targeting this task should improve response-relation modeling for long Thai argumentative passages. Sparse systems should preserve strong lexical candidate recall while reducing same-topic distractors. Dense systems need hard-negative training on stance and counterargument relation. Hybrid systems are promising because they combine topic anchoring with semantic response cues.

## Example Data

| Query | Positive document |
| --- | --- |
| สาธารณชนไม่สนใจการปฏิรูป ไม่ว่าจะเป็นการปฏิรูปสภาขุนนางควรเป็นลำดับความสำคัญสูงสุดในสภาพเศรษฐกิจปัจจุบันหรือไม่เป็นเรื่องที่ถกเถียงกันได้ ยิ่งไปกว่านั้นรัฐบาลผสมจะสามารถเริ่มต้นและผลักดันมาตรการดังกล่าวได้หรือไม่ ความพยายามในการปฏิรูปสภาขุนนางถูกเลื่อนออกไปซ้ำแล้วซ้ำเล่า แสดงให้เห็นถึงความกังวลของสภาสามัญเกี่ยวกับการเปลี่ยนแปลง ความรู้สึกนี้ไม่มีข้อสงสัยสะท้อนอยู่ในความคิดเห็นของประชาชนชาวอังกฤษ – ดังที่แสดงให้เห็นจากผลการลงคะแนนเสียงทางเลือกเมื่อเร็ว ๆ นี้ – สาธารณชนมีความรู้สึกต่อต้านแนวคิดการ... [500 / 528 chars] | แคมเปญ AV ไม่สามารถเปรียบเทียบกับการปฏิรูปสภาขุนนางได้ นอกจากนี้ ไม่ควรเข้าใจผิดว่าประชาชนที่มีข้อมูลผิดพลาดจากการเมืองเป็นความเฉยเมย บ่อยครั้งที่ผู้มีสิทธิเลือกตั้งแสดงออกว่าพวกเขาเฉยเมยเพราะรู้สึกว่าพวกเขาไม่สามารถเปลี่ยนแปลงอะไรได้ และเสียงของพวกเขาจะไม่มีความหมาย: การปฏิรูปที่ทำให้ผู้ที่บริหารประเทศได้รับการเลือกตั้งโดยตรงจากประชาชนจะช่วยแก้ไขความรู้สึกเหล่านี้ได้ [370 chars] |
| การขยายสนามบินฮีทโธรว์มีความสำคัญต่อเศรษฐกิจ การขยายสนามบินฮีทโธรว์จะทำให้มั่นใจได้ว่ามีงานปัจจุบันจำนวนมากและสร้างงานใหม่ด้วย ขณะนี้สนามบินฮีทโธรว์สนับสนุนงานประมาณ 250,000 ตำแหน่ง [1] นอกจากนี้ยังมีคนอีกหลายแสนคนที่พึ่งพาการค้าท่องเที่ยวในลอนดอนซึ่งขึ้นอยู่กับการเชื่อมต่อการขนส่งที่ดีเช่นสนามบินฮีทโธรว์ การสูญเสียความสามารถในการแข่งขันเมื่อเปรียบเทียบกับสนามบินอื่นในยุโรปไม่เพียงแต่จะหมายถึงการสูญเสียโอกาสในการสร้างงานใหม่ แต่ยังสูญเสียงานบางส่วนที่มีอยู่แล้ว การขยายสนามบินฮีทโธรว์ยังจะเป็นการ... [500 / 911 chars] | ชุมชนธุรกิจยังห่างไกลจากการเป็นเอกภาพในความสนับสนุนที่กล่าวอ้างต่อการสร้างรันเวย์ที่สาม การสำรวจแสดงให้เห็นว่าหลายธุรกิจที่มีอิทธิพลจริง ๆ แล้วไม่สนับสนุนการขยายตัว จดหมายที่แสดงความกังวลได้รับการลงนามโดยจัสติน คิง ประธานเจ้าหน้าที่บริหารของ J Sainsbury และเจมส์ เมอร์ด็อก จาก BskyB ดังนั้นการรวมชุมชนธุรกิจเป็นเสียงเดียวที่เรียกร้องให้มีการขยายตัวจึงเป็นการเข้าใจผิด เราควรจำไว้ด้วยว่าเมื่อพิจารณาทางเลือกอื่น ๆ ต่อรันเวย์ใหม่ของฮีทโธรว์ เช่น รันเวย์ใหม่ที่สนามบินลอนดอนอื่นหรือสนามบินใหม่ทั้งหมด สิ่งเหล่านี้อาจมีผลกระทบทางเศรษฐกิจที่คล้ายคลึงกับการขยายตัวของฮีทโธรว์ หากการเชื่อมต่อเป็นสิ่งสำคัญในการดึงดูดธุรกิจและนักท่องเที่ยว ตราบใดที่การเชื่อมต่อนั้นอยู่กับลอนดอนก็ไม่สำคัญว่าการเชื่อมต่อนั้นมาจากสนามบินไหน อาจจะไม่มีความจำเป็นที่สนามบินจะต้องเป็นสนามบินศูนย์กลางหากเรามุ่งเน้นไปที่ผลประโยชน์ต่อกรุงลอนดอน ตามที่บ็อบ เออิง อดีตประธานเจ้าหน้าที่บริหารของบริติชแอร์เวย์สกล่าวว่า ฮีทโธรว์ควรมุ่งเน้นไปที่ผู้โดยสารที่ต้องการมาที่ลอนดอน ไม่ใช่เพียงแค่เป็นจุดเปลี่ยน เขากล่าวว่ารันเวย์ที่สามอาจเป็น... [1,000 / 1,032 chars] |
| ผู้คนได้รับทางเลือกมากเกินไป ซึ่งทำให้พวกเขาน้อยใจมากขึ้น การโฆษณานำไปสู่หลายคนที่รู้สึกท่วมท้นจากความต้องการที่ไม่มีที่สิ้นสุดในการตัดสินใจระหว่างความต้องการที่แข่งขันกันสำหรับความสนใจของพวกเขา – สิ่งนี้เรียกว่าการปกครองของทางเลือกหรือความท่วมท้นของทางเลือก งานวิจัยล่าสุดแนะนำว่าผู้คนโดยเฉลี่ยมีความสุขน้อยกว่าที่เคยเป็นเมื่อ 30 ปีก่อน - แม้ว่าจะอยู่ในสภาพที่ดีขึ้นและมีทางเลือกมากขึ้นในการใช้จ่ายเงินของพวกเขา การอ้างสิทธิ์ของโฆษณาเข้ามารบกวนผู้คน ทำให้คาดหวังเกี่ยวกับผลิตภัณฑ์และนำไปสู่ความผิดหว... [500 / 797 chars] | ผู้คนไม่พอใจเพราะพวกเขาไม่สามารถมีทุกอย่างได้ ไม่ใช่เพราะพวกเขาได้รับทางเลือกมากเกินไปและรู้สึกเครียด ในความเป็นจริง โฆษณามีบทบาทสำคัญในการทำให้แน่ใจว่าผู้คนใช้เงินที่มีอยู่ไปกับผลิตภัณฑ์ที่เหมาะสมที่สุดสำหรับตัวเอง หากไม่มีการอนุญาตให้โฆษณา ผู้คนจะใช้เงินไปกับผลิตภัณฑ์แรกเมื่อเมื่อมีทางเลือก พวกเขาจะเลือกผลิตภัณฑ์อื่นอย่างชัดเจน การวิเคราะห์เมตาที่รวมการวิจัยจากการศึกษาอิสระ 50 ชิ้นพบว่าไม่มีความเชื่อมโยงที่มีความหมายระหว่างทางเลือกและความวิตกกังวล แต่คาดการณ์ว่าความแปรผันในงานวิจัยทำให้มีความเป็นไปได้ว่าการมีทางเลือกมากเกินไปอาจเกี่ยวข้องกับเงื่อนไขเบื้องต้นที่เฉพาะเจาะจงและยังเข้าใจไม่ดี1. 1 ^ Scheibehenne, Benjamin; Greifeneder, R. & Todd, P. M. (2010). "Can There Ever be Too Many Options? A Meta-Analytic Review of Choice Overload". Journal of Consumer Research 37: 409-425. [788 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [ArguAna](https://aclanthology.org/P18-1023/) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-th dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |

Representative query and positive response snippets:

| Query | Positive document snippet |
| --- | --- |
| สาธารณชนไม่สนใจการปฏิรูป ไม่ว่าจะเป็นการปฏิรูปสภาขุนนางควรเป็นลำดับความสำคัญสูงสุด... | แคมเปญ AV ไม่สามารถเปรียบเทียบกับการปฏิรูปสภาขุนนางได้... |
| การขยายสนามบินฮีทโธรว์มีความสำคัญต่อเศรษฐกิจ... | ชุมชนธุรกิจยังห่างไกลจากการเป็นเอกภาพในความสนับสนุนที่กล่าวอ้าง... |
| ผู้คนได้รับทางเลือกมากเกินไป ซึ่งทำให้พวกเขาน้อยใจมากขึ้น... | ผู้คนไม่พอใจเพราะพวกเขาไม่สามารถมีทุกอย่างได้... |
| การโจมตีทางไซเบอร์มักเกิดขึ้นโดยผู้ที่ไม่ใช่รัฐ... | ในกรณีที่มีการโจมตีจากผู้ไม่ใช่รัฐ ผู้เชี่ยวชาญหลายคนในกฎหมายระหว่างประเทศเห็นพ้องกัน... |
| เนื่องจากศาสนาส่งเสริมความแน่นอนของความเชื่อ... | ไม่มีใครถูกบังคับให้กระทำการใช้ความรุนแรงโดยคำพูดของผู้อื่น... |
