# MNanoBEIR / NanoBEIR-th / NanoMSMARCO

## Overview

NanoMSMARCO in the Thai NanoBEIR slice is a web passage retrieval task derived from MS MARCO. The queries are Thai translated search questions, and the corpus contains Thai translated answer-bearing passages. The task measures whether a retriever can connect short user questions to passages that answer them. It is a compact diagnostic for practical QA-style retrieval in Thai, where queries are brief, answer passages are short-to-medium length, and exact term overlap is often not enough.

## Details

### What the Original Data Measures

MS MARCO was built from real web-search questions and answer passages. In retrieval form, a model receives a user query and must retrieve the passage containing the answer. The relevant passage may define a term, identify a person, describe a role, locate a place, or explain a phrase. Relevance depends on answer-bearing content, not just topical match.

The Thai translated version adds challenges from Thai word segmentation, translated question wording, and mixed-script entities such as song titles or show names. A strong retriever must preserve exact anchors while also understanding the expected answer type. A passage that mentions the query topic but does not answer the question should not be ranked highly.

### Observed Data Profile

The task contains 50 queries, 5,043 documents, and 50 relevance judgments. Every query has exactly one positive passage, with no multi-positive queries. This makes the benchmark a strict single-answer retrieval task.

Queries average 32.14 characters, while documents average 293.94 characters. The queries are very short, often definition or fact-seeking questions, and the passages are concise answer-bearing texts. Because the query provides little context, a model must infer intent from a few Thai words and any embedded named entities.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2907, hit@10 of 0.4600, and recall@100 of 0.8000 using the top-500 BM25 candidate subset. This profile shows that lexical matching can often find the answer candidate somewhere in the first 100 ranks, but it is much weaker at placing it in the top 10.

The gap between recall@100 and nDCG@10 is important. BM25 can use visible terms such as a disease name, song title, actor name, or geographic phrase, but answer passages may use different wording or contain the answer in a surrounding explanation. Thai segmentation and translated phrasing make pure lexical ranking more brittle.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.4265, hit@10 of 0.6200, and recall@100 of 0.9200. Dense retrieval improves strongly over BM25 across all metrics. This indicates that embedding similarity is much better aligned with Thai question-to-answer passage matching than exact term overlap alone.

The dense advantage is typical for MS MARCO-style retrieval. Short queries often need semantic answer matching, and relevant passages may explain the answer without repeating the query text exactly. Remaining errors likely involve ambiguous short questions, mixed-script names, or cases where the answer is only a small part of a passage.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.3653, hit@10 of 0.5400, and recall@100 of 0.9400. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 3 safeguard rows and a mean of 100.06 candidates. The hybrid profile has the strongest recall@100, while dense retrieval has the strongest top-10 ranking and hit rate.

This means hybrid search broadens candidate coverage by adding lexical matches to the dense pool, but its first-stage ordering is less aligned with answer usefulness. For Thai NanoMSMARCO, reranking_hybrid is useful when a later reranker can exploit the high-recall pool. For direct search results, dense retrieval is the stronger baseline.

### Metric Interpretation for Model Researchers

Because every query has one positive, nDCG@10 and hit@10 directly measure whether the answer passage appears in a usable position. recall@100 measures whether a later reranker has access to the answer. BM25's high recall but weak top-10 score shows that candidate discovery and final ranking are separate problems here.

The method comparison is clear: BM25 finds some lexical candidates but ranks too many distractors above the answer, dense retrieval improves semantic answer matching, and reranking_hybrid improves coverage while needing better ordering. This task is useful for testing Thai short-query intent modeling and answer-bearing passage discrimination.

### Query and Relevance Type Tendencies

Queries include definition questions, song questions, actor-role questions, geography questions, and phrase-meaning questions, such as what rumination syndrome is, who sang "Here I Go Again," who Cameron Boyce played in Liv and Maddie, where the largest deserts occur, and what a term means for police. Positive passages usually contain direct answers or concise explanations.

The task rewards recognizing answer type. "Who" queries need people, "where" queries need locations, and "what is" queries need definitions. Topic similarity without the requested answer type is a common source of false positives.

### Representative Failure Modes

Likely failures include retrieving passages that mention the query term without answering it, confusing similarly named songs or shows, missing answers because Thai wording differs from the passage, and over-ranking broad background passages. BM25 is vulnerable to tokenization and vocabulary mismatch, while dense retrieval may retrieve semantically related non-answers.

### Training Data That May Help

Useful training data includes Thai web QA, multilingual passage retrieval, short-query answer retrieval, search-log style data, and hard negatives that share query terms but do not answer the question. For rerankers, answer-type negatives are valuable because the main distinction is often whether the passage actually answers the query.

### Model Improvement Notes

A model targeting this task should improve short Thai query understanding and answer-bearing passage ranking. Sparse systems need Thai-aware tokenization and query expansion. Dense systems are the strongest direct baseline and should be refined with topical non-answer hard negatives. Hybrid systems should preserve their recall advantage while using reranking to suppress lexical distractors.

## Example Data

| Query | Positive document |
| --- | --- |
| โรคการคิดซ้ำคืออะไร [19 chars] | โรคการย้อนกลับอาหาร โรคการย้อนกลับอาหาร ซึ่งเรียกว่า Merycism เป็นประเภทของความผิดปกติในการกินที่ไม่ได้ระบุไว้ในประเภทอื่น ซึ่งทำให้เกิดการย้อนกลับของอาหาร แม้ว่าจะไม่ได้ถูกระบุว่าเป็นความผิดปกติในการ... [200 / 283 chars] |
| ใครร้องเพลง Here I Go Again [27 chars] | สำหรับการใช้งานอื่น ๆ ดูที่ Here I Go Again (การชี้แจงความหมาย) Here I Go Again เป็นเพลงของวงร็อคอังกฤษ Whitesnake เปิดตัวครั้งแรกในอัลบั้ม Saints & Sinners ปี 1982 เพลงนี้ถูกบันทึกเสียงใหม่สำหรับอัลบ... [200 / 298 chars] |
| คาเมรอน บอยซ์ แสดงเป็นใครในลิฟและแมดดี้ [39 chars] | เตรียมตัวให้พร้อมสำหรับเสียงหัวเราะที่จริงจังนะทุกคน ในการชมพิเศษก่อนออกอากาศตอนวันที่ 19 เม.ย. ของ Liv & Maddie ที่ชื่อว่า “Prom-A-Rooney” แน่นอน ในคลิปที่ตลกขบขันนี้ เราเห็นเจสซี่ที่แสดงโดยแคเมอรอน... [200 / 306 chars] |
| ทะเลทรายขนาดใหญ่ส่วนใหญ่ของโลกเกิดขึ้นที่ไหน [44 chars] | ทะเลทรายที่เหลือของโลกอยู่ภายนอกพื้นที่ขั้วโลก ทะเลทรายที่ใหญ่ที่สุดคือทะเลทรายซาฮารา ซึ่งเป็นทะเลทรายเขตร้อนชื้นในแอฟริกาเหนือ [127 chars] |
| ความหมายของทองแดงสำหรับตำรวจ [28 chars] | จากการค้นพบในปัจจุบัน ดูเหมือนว่า "copper" (ตำรวจ, แปลตรงตัวว่า 'ผู้ที่จับกุม') จะมีมาก่อน "cop" (ไม่ว่าจะใช้ในรูปแบบคำกริยาหมายถึงการจับกุม หรือในรูปแบบคำนามหมายถึงตำรวจ) อาจเป็นไปได้ว่าเหรียญตรา "co... [200 / 322 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [MS MARCO](https://arxiv.org/abs/1611.09268) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-th dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |

Representative query and positive passage snippets:

| Query | Positive document snippet |
| --- | --- |
| โรคการคิดซ้ำคืออะไร | โรคการย้อนกลับอาหาร ซึ่งเรียกว่า Merycism เป็นประเภทของความผิดปกติในการกิน... |
| ใครร้องเพลง Here I Go Again | Here I Go Again เป็นเพลงของวงร็อคอังกฤษ Whitesnake... |
| คาเมรอน บอยซ์ แสดงเป็นใครในลิฟและแมดดี้ | ในการชมพิเศษก่อนออกอากาศตอนวันที่ 19 เม.ย. ของ Liv & Maddie... |
| ทะเลทรายขนาดใหญ่ส่วนใหญ่ของโลกเกิดขึ้นที่ไหน | ทะเลทรายที่เหลือของโลกอยู่ภายนอกพื้นที่ขั้วโลก ทะเลทรายที่ใหญ่ที่สุดคือทะเลทรายซาฮารา... |
| ความหมายของทองแดงสำหรับตำรวจ | จากการค้นพบในปัจจุบัน ดูเหมือนว่า "copper" จะมีมาก่อน "cop"... |
