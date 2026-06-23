# NanoMTEB-Thai / xqu_ad_th

## Overview

`NanoMTEB-Thai / xqu_ad_th` is the Thai XQuAD retrieval split. Thai questions must retrieve the translated Thai context paragraph that contains the answer. XQuAD was created as a cross-lingual question-answering benchmark from SQuAD-style data translated into multiple languages; in the retrieval conversion, the question becomes the query and the context paragraph becomes the document. This Nano task is small, with only 240 documents, but it is useful for understanding question-to-context retrieval in Thai because many questions are clustered around the same source articles and paragraphs.

## Details

### What the Original Data Measures

XQuAD measures cross-lingual QA transfer using translated question-answer examples. The retrieval version changes the target from answer extraction to paragraph retrieval: a model must find the Thai paragraph that contains enough context to answer the Thai question.

In this split, both query and document text are Thai. The challenge is not cross-lingual transfer at retrieval time, but distinguishing the correct translated context among a small set of related paragraphs.

### Observed Data Profile

The Nano split contains 200 queries, 240 documents, and 200 positive qrel rows. Each query has exactly one positive paragraph. Queries average 54.18 characters, while documents average 736.76 characters.

Several examples come from shared article contexts, including American football and historical or cultural topics. Multiple questions can point to nearby or repeated context, so a retriever must handle clustered questions and avoid ranking another paragraph from the same topic above the labeled one.

### BM25 Evaluation Profile

The BM25 candidate subset covers all 240 documents and reaches nDCG@10 of 0.9835, hit@10 of 1.0000, and recall@100 of 1.0000. This is an extremely strong sparse profile. The corpus is small, questions and contexts are in the same language, and many questions share key terms with their answer-bearing paragraphs.

BM25 is therefore the strongest standalone candidate source for this split. Its rare ranking errors are likely to occur among closely related paragraphs from the same source article, where a nearby paragraph shares many terms but is not the labeled context.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` also covers all 240 documents and reaches nDCG@10 of 0.9459, hit@10 of 0.9800, and recall@100 of 0.9950. Dense retrieval is very strong, but slightly weaker than BM25. This suggests that semantic similarity is effective for Thai question-to-paragraph retrieval, while exact lexical overlap is especially reliable in this small translated corpus.

The dense profile is still valuable for studying failures where the model ranks a semantically related paragraph above the exact context. Such errors can reveal whether an embedding model captures answer-bearing specificity or only broad topic similarity.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates with no safeguard positives. It reaches nDCG@10 of 0.9674, hit@10 of 0.9900, and recall@100 of 1.0000. The hybrid pool restores full recall like BM25 and improves over dense retrieval, but it does not surpass BM25's top-rank quality.

This is a case where hybrid retrieval is useful for coverage but not necessary for first-stage success. Since BM25 already covers the task almost perfectly, the main value of a hybrid or reranker setup is to test robustness on clustered context paragraphs rather than to rescue missing positives.

### Metric Interpretation for Model Researchers

Scores are near ceiling, so this task should be treated as an easy or sanity-check retrieval split rather than a high-difficulty benchmark. It is still useful because it exposes whether a model can handle Thai translated QA contexts and whether it fails on clustered paragraphs.

For this split, small nDCG differences can correspond to only a few queries. Researchers should inspect errors directly before drawing broad conclusions about Thai retrieval quality.

### Query and Relevance Type Tendencies

Queries are Thai QA questions asking for named entities, numbers, events, dates, roles, or details from a paragraph. Relevant documents are medium-length translated context paragraphs, often drawn from SQuAD-style articles.

The relevance relation is answer-bearing context. The correct paragraph should contain the information required to answer the question, even if neighboring paragraphs are topically similar.

### Representative Failure Modes

Failures include retrieving an adjacent paragraph from the same article, matching a shared entity but not the answer sentence, and confusing repeated sports or historical details. Dense systems may prefer a semantically broad paragraph; sparse systems may prefer a paragraph with more repeated query terms.

### Training Data That May Help

Useful training data includes Thai SQuAD-style QA retrieval, translated XQuAD examples, TyDi-style question-to-context pairs, and hard negatives from adjacent paragraphs in the same article. Because the corpus is small and easy, training value is highest when negatives are closely related.

### Model Improvement Notes

This task is best used to verify Thai QA-context retrieval behavior and error modes. Strong models should reach near-ceiling performance. To make additional progress, focus on paragraph-level reranking among clustered contexts and on preserving exact answer constraints such as numbers, dates, and named entities.

## Example Data

| Query | Positive document |
| --- | --- |
| ศิลปินท่านใดที่ทำงานแกะสลักไม้ให้กับไบเบิลของลูเทอร์? [53 chars] | ถูกเผยแพร่ในเวลาที่มีความต้องการเพิ่มมากขึ้นสำหรับ สิ่งพิมพ์ภาษาเยอรมัน งานแปล คัมภีร์ไบเบิล เวอร์ชั่นของลูเทอร์กลายเป็นที่นิยมและมีอิทธิพลอย่างรวดเร็ว เช่นนั้น งานชิ้นนี้เป็นส่วนช่วยสำคัญแก่ วิวัฒนาการของภาษาและวรรณกรรมเยอรมัน ตกแต่งด้วยบันทึกและบทนำโดยลูเทอร์ และด้วยไม้แกะสลักโดย ลูคัส ครานัค ที่มีภาพต่อต้านสมเด็จพระสันตะปาปา หนังสือนี้มีบทบาทสำคัญในการเผยแพร่คำสอนของลูเทอร์ทั่วทั้งเยอรมนี หนังสือ Luther Bible มีอิทธิพลต่องานแปลอื่น เช่นไบเบิลภาษาอังกฤษของ วิลเลียม ทนเดล (1525 ถัดมา) คัมภีร์ก่อนหน้า King James Bible [523 chars] |
| ระหว่างการแข่งขันเพลย์ออฟ ใครไม่ได้ขว้างลูกบอลเลย [49 chars] | ทีมบรอนคอส เอาชนะทีม พิตต์สเบิร์ก สตีลเลอร์ส ในรอบดิวิชั่น 23–16 ด้วยการทำ 11 คะแนนในสามนาทีสุดท้ายของเกม จากนั้นพวกเขาก็เอาชนะทีมรับของ นิวอิงแลนด์แพทริออตส์ ซึ่งเป็นแชมป์ซูเปอร์โบว์ลครั้งที่ 49 ในการแข่งขันแชมป์ชิงเอเอฟซี 20–18 ด้วยการอินเตอร์เซปการขว้างลูกของนิวอิงแลนด์ที่พยายามทำ 2 คะแนนหลังทัชดาวน์ โดยมีเวลาเหลือ 17 วินาที ถึงแม้ แมนนิง จะมีปัญหากับการอินเตอร์เซปในฤดูกาลนี้ แต่เขาก็ไม่ได้ขว้างลูกบอลเลยในการแข่งขันเพลย์ออฟทั้งสองครั้งของพวกเขา [453 chars] |
| ทีมบรอนคอสทำคะแนนได้เท่าไรในสามนาทีสุดท้ายของการแข่งขันกับทีมพิตต์สเบิร์ก [73 chars] | ทีมบรอนคอส เอาชนะทีม พิตต์สเบิร์ก สตีลเลอร์ส ในรอบดิวิชั่น 23–16 ด้วยการทำ 11 คะแนนในสามนาทีสุดท้ายของเกม จากนั้นพวกเขาก็เอาชนะทีมรับของ นิวอิงแลนด์แพทริออตส์ ซึ่งเป็นแชมป์ซูเปอร์โบว์ลครั้งที่ 49 ในการแข่งขันแชมป์ชิงเอเอฟซี 20–18 ด้วยการอินเตอร์เซปการขว้างลูกของนิวอิงแลนด์ที่พยายามทำ 2 คะแนนหลังทัชดาวน์ โดยมีเวลาเหลือ 17 วินาที ถึงแม้ แมนนิง จะมีปัญหากับการอินเตอร์เซปในฤดูกาลนี้ แต่เขาก็ไม่ได้ขว้างลูกบอลเลยในการแข่งขันเพลย์ออฟทั้งสองครั้งของพวกเขา [453 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| On the Cross-lingual Transferability of Monolingual Representations | 2019 | paper | [https://arxiv.org/abs/1910.11856](https://arxiv.org/abs/1910.11856) |
| google-deepmind/xquad |  | repository | [https://github.com/google-deepmind/xquad](https://github.com/google-deepmind/xquad) |
| google/xquad |  | dataset card | [https://huggingface.co/datasets/google/xquad](https://huggingface.co/datasets/google/xquad) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| ศิลปินท่านใดที่ทำงานแกะสลักไม้ให้กับไบเบิลของลูเทอร์? | A Thai translated context about Luther's Bible, German-language print demand, and the cultural influence of the translation. |
| ระหว่างการแข่งขันเพลย์ออฟ ใครไม่ได้ขว้างลูกบอลเลย | A Thai context about the Broncos' playoff wins and defensive performance. |
| ทีมบรอนคอสทำคะแนนได้เท่าไรในสามนาทีสุดท้ายของการแข่งขันกับทีมพิตต์สเบิร์ก | A Thai paragraph stating that the Broncos scored 11 points in the final three minutes against Pittsburgh. |
| ตลาดหลักทรัพย์วอร์ซอว์ตั้งอยู่ในอดีตสำนักงานใหญ่ของใครจนกระทั่งปี 2000 | A Thai context about the Warsaw Stock Exchange, its history, and its former headquarters. |
| เดนเวอร์ถูกกันให้อยู่นอกเอนด์โซนกี่เกม หลังจากแย่งลูกบอลไปจากนิวตัน | A Thai football context describing a late play involving Miller forcing a fumble from Newton. |
