# MNanoBEIR / NanoBEIR-th / NanoTouche2020

## Overview

NanoTouche2020 in the Thai NanoBEIR slice is an argument retrieval task derived from the Touché 2020 shared task. The queries are Thai translated controversial questions, and the corpus contains Thai translated argument passages. The retrieval goal is to find passages that provide relevant arguments for the debate topic, often across several sides and sub-aspects. This makes the task a compact benchmark for Thai argumentative search, stance-aware retrieval, and multi-positive ranking.

## Details

### What the Original Data Measures

Touché 2020 evaluates argument retrieval for controversial information needs. A relevant passage should contribute an argument, reason, example, or perspective that helps address the debate question. Relevance is broader than ordinary topicality: a passage may mention the same issue but still be weak if it does not answer the specific argumentative need.

The Thai translated version tests this behavior with short debate questions and long argument passages. The model must connect a concise Thai question to passages that may express only one side or one aspect of the issue. Topic matching is useful, but stance, argumentative role, and aspect coverage are the deeper retrieval signals.

### Observed Data Profile

The task contains 49 queries, 5,745 documents, and 932 relevance judgments. Every query is multi-positive, with an average of 19.02 positives per query. The minimum is 6, the median is 19.0, and the maximum is 32. This is a broad relevant-set task where finding one argument is not enough.

Queries average 46.29 characters, while documents average 1,438.05 characters. The short-query and long-document contrast is important: a brief question about homework, vaccines, abortion, or standardized testing can map to many long passages with claims, examples, and justifications. The model must rank many relevant arguments, not just the most literal match.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.5108, hit@10 of 0.9796, and recall@100 of 0.7489 using the top-500 BM25 candidate subset. This is a strong lexical baseline. Debate questions contain salient topic words, and long argument passages often repeat those terms, so BM25 almost always finds at least one relevant argument in the top 10.

The remaining challenge is broad ranking. Every query has many positives, and arguments may use different phrasing or focus on different aspects of the debate. BM25 can find the obvious topical candidates, but it may miss or under-rank relevant arguments that express the issue indirectly or from another stance.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.4534, hit@10 of 0.9184, and recall@100 of 0.7521. Dense retrieval has slightly higher recall@100 than BM25, but weaker top-rank quality. This suggests that embedding similarity broadens the candidate set but can also retrieve broadly related passages that are less directly useful as arguments.

For Thai argument retrieval, dense matching captures semantic relatedness and varied wording, but it may blur stance or aspect. A passage can be semantically related to a controversial topic while failing to answer the particular question. This explains why dense retrieval is useful for coverage but not the strongest first-page ranker here.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.5380, hit@10 of 0.9796, and recall@100 of 0.7951. It uses exactly 100 candidates per query, with no rank-101 safeguard rows. This is the strongest profile among the three modes, improving both graded top-10 ranking and recall.

The hybrid result shows that Thai Touché retrieval benefits from combining lexical topic anchors with dense semantic coverage. BM25 keeps the query topic precise, while dense retrieval brings in relevant arguments that do not match the wording exactly. The hybrid ordering is therefore better aligned with the task's multi-positive argument search objective.

### Metric Interpretation for Model Researchers

Because every query has many positives, hit@10 is not sufficient. A model can show a high hit rate while retrieving only one obvious argument and missing much of the debate landscape. nDCG@10 measures whether the first page contains a dense set of relevant arguments, while recall@100 measures whether downstream reranking has access to a broad candidate set.

The method comparison is instructive. BM25 is strong for obvious topical matches. Dense retrieval broadens coverage but weakens first-page ordering. reranking_hybrid combines both advantages and is the best profile for this slice. This makes the task useful for studying hybrid search and stance-aware reranking for Thai argument retrieval.

### Query and Relevance Type Tendencies

Queries ask controversial questions such as whether homework is useful, whether prescription drugs should be advertised directly to consumers, whether some vaccines should be required for children, whether abortion should be legal, and whether standardized tests improve education. Relevant passages are long arguments with claims, evidence, and reasoning.

The task rewards models that understand issue, stance, and aspect. Different positives may argue for or against the same proposition, or discuss a particular sub-issue. A same-topic document is not automatically relevant if it does not contribute an argument to the question.

### Representative Failure Modes

Likely failures include retrieving generic informational passages instead of arguments, over-ranking passages that repeat the topic but lack a clear reason, missing counterarguments with different wording, and failing to cover multiple aspects of a debate. BM25 can be too literal, while dense retrieval can be too broad. Hybrid systems help when their ordering preserves both topic precision and argumentative usefulness.

### Training Data That May Help

Useful training data includes Thai debate retrieval, argument passage ranking, stance-aware retrieval, controversial question answering, and hard negatives that share the same topic but do not answer the requested aspect. For rerankers, same-topic weak arguments and stance-mismatched passages are particularly valuable.

### Model Improvement Notes

A model targeting this task should optimize for both first-page argument quality and broad positive-set coverage. Sparse systems need lexical precision plus expansion for paraphrased arguments. Dense systems need better stance and aspect sensitivity. Hybrid systems are the strongest baseline here, especially when paired with a reranker that can judge whether a passage functions as an argument for the query.

## Example Data

| Query | Positive document |
| --- | --- |
| การบ้านมีประโยชน์หรือไม่? [25 chars] | ก่อนอื่นมีสามเหตุผลว่าทำไมการบ้านจึงยอดเยี่ยมและควรดำเนินต่อไปในโรงเรียนสมัยใหม่ 1. การบ้านช่วยผู้เรียนที่ลงมือทำ โดยทั่วไปแล้วถือว่ามีผู้เรียนสามประเภท: ผู้ที่เรียนรู้จากการฟัง, ผู้ที่เรียนรู้จากการมองเห็น, และผู้ที่เรียนรู้จากการลงมือทำ ในขณะที่หลายคนพอใจกับการฟังหรือเห็นการสอนในหัวข้อที่กำหนด บางคนต้องการที่จะลงมือทำจริงๆ ดังนั้นการบ้านจึงเป็นประโยชน์สำหรับกลุ่มหลังนี้เพราะการสอนนั้นเรียนรู้ผ่านการกระทำ 2. การบ้านเสริมสร้างการสอน แม้ว่าหลายคนอาจจะดีใจที่ไม่มีการบ้าน แต่คุณภาพของการศึกษาที่ได้รับจะต้องได้รับผลกระทบแน่นอนหากมันถูกยกเลิก ไม่ว่าจะเป็นการบ้านที่เป็นการอ่าน, เอกสารรายงาน, เป็นต้น ทั้งหมดนี้ถูกออกแบบมาเพื่อเสริมสร้างการสอนในความคิดของนักเรียน หลังจากทั้งหมด ผู้ที่ทำการบ้านจะประสบความสำเร็จทางวิชาการมากกว่าผู้ที่ไม่ทำ ฉันรู้สึกว่านี่เป็นความจริงที่ชัดเจน แต่ฉันจะปล่อยให้ Pro ชี้แจงให้คุณฟัง 3. การบ้านสะท้อนความต้องการในชีวิตจริง หลังจากจบมัธยมปลาย จะมีเส้นทางหลักสองเส้นทางสำหรับผู้สำเร็จการศึกษา: มหาวิทยาลัยหรือทำงาน สำหรับทั้งสองเส้นทางนี้ จะมีการมอบหมายงานและอาจารย์/เจ้าน... [1,000 / 3,199 chars] |
| ควรโฆษณายาใบสั่งโดยตรงถึงผู้บริโภคหรือไม่? [42 chars] | โฆษณาหลายรายการไม่รวมข้อมูลเพียงพอเกี่ยวกับประสิทธิภาพของยา ตัวอย่างเช่น Lunesta ถูกโฆษณาผ่านผีเสื้อที่ลอยผ่านหน้าต่างห้องนอนเหนือคนที่นอนหลับอย่างสงบ จริงๆ แล้ว Lunesta ช่วยให้ผู้ป่วยนอนหลับเร็วขึ้น 15 นาทีหลังจากการรักษาเป็นเวลา 6 เดือนและให้เวลานอนเพิ่มขึ้นอีก 37 นาทีต่อคืน โฆษณาส่วนใหญ่มีพื้นฐานจากการดึงดูดทางอารมณ์ แต่มีเพียงไม่กี่รายการที่รวมสาเหตุของโรค ปัจจัยเสี่ยง หรือการเปลี่ยนแปลงวิถีชีวิตที่สำคัญ ในการศึกษาที่เกี่ยวกับโฆษณายา 38 รายการ นักวิจัยพบว่า 82 เปอร์เซ็นต์มีการกล่าวอ้างที่เป็นข้อเท็จจริงและ 86 เปอร์เซ็นต์มีการนำเสนอเหตุผลที่มีเหตุผลสำหรับการใช้ผลิตภัณฑ์ มีเพียง 26 เปอร์เซ็นต์ที่อธิบายถึงสาเหตุของโรค ปัจจัยเสี่ยง หรือความชvalนของโรค ดังนั้นจึงไม่ให้ข้อมูลที่สมดุลแก่ผู้ป่วยที่ทำให้พวกเขาตระหนักว่าการทานยาเม็ดหนึ่งไม่ใช่ทางออกวิเศษสำหรับปัญหาของพวกเขา จริงๆ แล้ว ตามการศึกษาที่ดำเนินการในสหรัฐอเมริกาและนิวซีแลนด์ ผู้ป่วยขอใบสั่งยาใน 12% ของการเยี่ยมชมที่สำรวจ ในการขอเหล่านี้ 42% เป็นผลิตภัณฑ์ที่โฆษณาต่อผู้บริโภคและผู้บริโภคไม่สามารถจำผลิตภัณฑ์ยาได้มากกว่า 4 รายการ นี่พิ... [1,000 / 1,096 chars] |
| ควรมีวัคซีนใด ๆ ที่จำเป็นสำหรับเด็กหรือไม่? [43 chars] | ยังไม่ใช่กรณีที่เต็มรูปแบบ.. แค่จุดเล็กๆ ที่ฉันรวบรวมไว้... รัฐบาลไม่ควรมีสิทธิ์แทรกแซงในเรื่องการตัดสินใจด้านสุขภาพที่พ่อแม่ทำเพื่อบุตรหลานของตน ตามการสำรวจในปี 2010 โดยมหาวิทยาลัยมิชิแกน พบว่า 31% ของพ่อแม่เชื่อว่าพวกเขาควรมีสิทธิ์ปฏิเสธการฉีดวัคซีนที่กำหนดสำหรับการเข้าศึกษาในโรงเรียนให้กับบุตรหลานของตน พ่อแม่หลายคนมีความเชื่อทางศาสนาที่ต่อต้านการฉีดวัคซีน การบังคับให้พ่อแม่เหล่านี้ฉีดวัคซีนให้กับบุตรหลานจะเป็นการละเมิดการแก้ไขเพิ่มเติมครั้งที่ 1 ซึ่งรับรองสิทธิของพลเมืองในการปฏิบัติศาสนาของตนอย่างเสรี วัคซีนมักไม่จำเป็นในหลายกรณีที่ความเสี่ยงจากการเสียชีวิตจากโรคมีน้อย ในช่วงต้นศตวรรษที่ 19 อัตราการเสียชีวิตจากโรคในเด็ก เช่น ไอกรน หัด และไข้แดง ลดลงอย่างมากก่อนที่การฉีดวัคซีนจะมีให้บริการ อัตราการเสียชีวิตที่ลดลงนี้ได้รับการอธิบายว่าเกิดจากการปรับปรุงสุขอนามัยส่วนบุคคล การบำบัดน้ำ การกำจัดน้ำเสียอย่างมีประสิทธิภาพ และสุขอนามัยและโภชนาการอาหารที่ดีขึ้น วัคซีนขัดขวางกฎธรรมชาติและแผนของพระเจ้าสำหรับมนุษย์ โรคเป็นเหตุการณ์ตามธรรมชาติ และมนุษย์ไม่ควรแทรกแซงในเส้นทางของมัน วัคซีนทั่วไปในเ... [1,000 / 3,513 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original task | [Touché 2020](https://doi.org/10.1007/978-3-030-58219-7_26) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-th dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |

Representative query and positive argument snippets:

| Query | Positive document snippet |
| --- | --- |
| การบ้านมีประโยชน์หรือไม่? | ก่อนอื่นมีสามเหตุผลว่าทำไมการบ้านจึงยอดเยี่ยมและควรดำเนินต่อไปในโรงเรียนสมัยใหม่... |
| ควรโฆษณายาใบสั่งโดยตรงถึงผู้บริโภคหรือไม่? | โฆษณาหลายรายการไม่รวมข้อมูลเพียงพอเกี่ยวกับประสิทธิภาพของยา... |
| ควรมีวัคซีนใด ๆ ที่จำเป็นสำหรับเด็กหรือไม่? | ยังไม่ใช่กรณีที่เต็มรูปแบบ.. รัฐบาลไม่ควรมีสิทธิ์แทรกแซง... |
| การทำแท้งควรเป็นเรื่องถูกกฎหมายหรือไม่? | การทำแท้งควรถูกกฎหมายเนื่องจากสถานะบุคคลเริ่มต้นหลังจากที่ทารกในครรภ์... |
| การทดสอบมาตรฐานช่วยพัฒนาการศึกษาไหม? | ข้อสรุป: SAT, ACT และการทดสอบมาตรฐานอื่น ๆ ให้ข้อมูลเชิงลึก... |
