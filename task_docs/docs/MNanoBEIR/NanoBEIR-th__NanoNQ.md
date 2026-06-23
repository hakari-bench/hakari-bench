# MNanoBEIR / NanoBEIR-th / NanoNQ

## Overview

NanoNQ in the Thai NanoBEIR slice is an open-domain question answering retrieval task derived from Natural Questions. The queries are Thai translated search questions, and the corpus contains Thai translated answer passages. The retrieval goal is to find passages that contain or support the answer to each question, not merely passages about the same entity. This makes the task a compact diagnostic for Thai question-to-passage retrieval, entity grounding, and answer-bearing passage ranking.

## Details

### What the Original Data Measures

Natural Questions was built from real search questions with Wikipedia evidence. In retrieval form, the system receives a natural question and must retrieve the passage that answers it. The relevant passage may contain the answer directly, or it may provide enough context to establish the requested fact, location, reason, or entity relation.

The Thai translated version adds challenges from Thai wording, word segmentation, and mixed-script entity names. Some names, songs, films, or events remain in English or transliterated form, while the surrounding question and passage text are Thai. A strong retriever must use exact anchors when they are available while also recognizing answer semantics beyond surface overlap.

### Observed Data Profile

The task contains 50 queries, 5,035 documents, and 57 relevance judgments. Most queries have one positive passage, with an average of 1.14 positives per query. The minimum is 1, the median is 1.0, the maximum is 2, and 7 queries have multiple positives, or 14.0% of the query set. This is therefore mostly a single-answer retrieval task.

Queries average 40.82 characters, while documents average 473.63 characters. The queries are short natural-language questions, and the passages are longer Wikipedia-style answer contexts. This structure makes the task sensitive to whether a model can map question intent to the passage that actually answers it.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3191, hit@10 of 0.5600, and recall@100 of 0.8421 using the top-500 BM25 candidate subset. This profile shows that lexical matching recovers many answer passages by rank 100, but is much weaker at placing them in the top 10. In other words, BM25 is more useful as a candidate generator than as a final ranker.

The result is consistent with open-domain QA. Questions often contain entities or distinctive terms that help BM25 find the right neighborhood, but the true answer passage may not have the strongest surface overlap. Thai segmentation and translated wording can also make exact matching less reliable.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.5367, hit@10 of 0.7400, and recall@100 of 0.9123. Dense retrieval is clearly stronger than BM25 across all three metrics. This indicates that embedding similarity captures question-answer semantics and passage context beyond exact token overlap.

The dense advantage is important for questions where the passage answers through explanation or paraphrase. It can better connect "why," "where," and "who" questions to answer-bearing passages, even when Thai wording differs from the passage text. Remaining errors likely involve ambiguous entities, mixed-script names, or passages that are topically related but do not contain the requested fact.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.4246, hit@10 of 0.6400, and recall@100 of 0.9298. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 3 safeguard rows and a mean of 100.06 candidates. The hybrid profile has the best recall@100, while dense retrieval has the strongest top-10 ranking.

This means hybrid search broadens the candidate pool by combining lexical and dense evidence, but its first-stage ordering is weaker than dense retrieval alone. For Thai NanoNQ, reranking_hybrid is valuable when a later reranker can exploit the high-recall pool. For direct retrieval output, dense similarity is the more aligned ranking signal.

### Metric Interpretation for Model Researchers

nDCG@10 is the most practical metric for a QA or RAG pipeline because only the top few passages are usually consumed. hit@10 measures whether at least one answer-bearing passage is visible, and recall@100 measures whether a reranker has access to the answer. The task shows a clear difference between answer-candidate coverage and answer ranking.

BM25's recall is relatively high but its top-10 ranking is weak. Dense retrieval provides the best first-page quality. reranking_hybrid gives the most complete candidate pool but needs stronger reranking. Researchers can use this task to test whether gains come from semantic answer matching or simply from broader candidate coverage.

### Query and Relevance Type Tendencies

Queries ask factual questions such as where the Final Four is held, whether Nightmare Before Christmas was originally a Disney film, why the Angel of the North is there, where the three-fifths compromise appears in the Constitution, and who sings "Somebody's Watching Me" with Michael Jackson. Relevant passages are answer-bearing encyclopedia-style texts.

The task rewards precise handling of question type. "Where" questions need locations, "why" questions need explanations, and "who" questions need people. A passage about the same title or event is not enough unless it answers the requested relation.

### Representative Failure Modes

Likely failures include retrieving a passage about the same entity but not the requested fact, confusing similar works or names, missing answer passages because Thai translation changes the wording, and over-ranking broad background text. BM25 may overvalue repeated names, while dense retrieval may retrieve semantically related passages that lack the exact answer.

### Training Data That May Help

Useful training data includes Thai open-domain QA, Wikipedia passage retrieval, multilingual question-passage pairs, and hard negatives that share entities but do not answer the question. Thai question rewriting and translated QA data can help if evaluation overlap is avoided. For rerankers, same-entity non-answer passages are especially valuable.

### Model Improvement Notes

A model targeting this task should improve answer-bearing passage discrimination. Dense retrieval is the strongest direct baseline and should be refined with question-answer hard negatives. Sparse systems need Thai-aware tokenization and entity normalization. Hybrid systems should use their high recall with a reranker that explicitly detects whether the passage answers the question.

## Example Data

| Query | Positive document |
| --- | --- |
| ปีนี้รอบสุดท้ายจะจัดที่ไหน [26 chars] | การแข่งขันบาสเกตบอลชาย NCAA Division I ปี 2018 เป็นการแข่งขันแบบน็อกเอาต์ 68 ทีมเพื่อกำหนดแชมป์ระดับชาติของสมาคมกรีฑาวิทยาลัยแห่งชาติ (NCAA) Division I สำหรับฤดูกาล 2017–18 รุ่นที่ 80 ของการแข่งขันเริ... [200 / 323 chars] |
| หนัง Nightmare Before Christmas เป็นภาพยนตร์ของดิสนีย์ตั้งแต่แรกหรือไม่ [71 chars] | นิทานก่อนวันคริสต์มาสเริ่มต้นจากบทกวีที่เขียนโดยทีม เบอร์ตันในปี 1982 ขณะที่เขาทำงานเป็นนักสร้างอนิเมชั่นที่วอลท์ ดิสนีย์ ฟีเจอร์ แอนิเมชั่น ด้วยความสำเร็จของวินเซนต์ในปีเดียวกัน สตูดิโอวอลท์ ดิสนีย์เ... [200 / 557 chars] |
| ทำไมเทวดาแห่งเหนือถึงอยู่ที่นั่น [32 chars] | ตามที่กอร์มลีย์กล่าว ความสำคัญของเทวดามีสามประการ: ประการแรก เพื่อบ่งชี้ว่าภายใต้สถานที่ก่อสร้างนั้น คนงานเหมืองถ่านหินทำงานมาเป็นเวลาสองศตวรรษ; ประการที่สอง เพื่อเข้าใจการเปลี่ยนผ่านจากยุคอุตสาหกรรมส... [200 / 307 chars] |
| ที่ไหนที่การประนีประนอม 3/5 ถูกกล่าวถึงในรัฐธรรมนูญ [51 chars] | การประนีประนอมสามในห้าพบได้ในมาตรา 1, หมวด 2, ข้อ 3 ของรัฐธรรมนูญสหรัฐอเมริกา ซึ่งระบุว่า: [90 chars] |
| ใครร้องเพลง somebody's watching me ร่วมกับไมเคิล แจ็คสัน [56 chars] | "Somebody's Watching Me" เป็นเพลงของนักร้องชาวอเมริกัน Rockwell จากอัลบั้มสตูดิโอเดบิวต์ของเขา Somebody's Watching Me (1984) ซึ่งถูกปล่อยออกมาเป็นซิงเกิลเดบิวต์ของ Rockwell และซิงเกิลหลักจากอัลบั้มเมื... [200 / 350 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [Natural Questions](https://aclanthology.org/Q19-1026/) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-th dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |

Representative query and positive passage snippets:

| Query | Positive document snippet |
| --- | --- |
| ปีนี้รอบสุดท้ายจะจัดที่ไหน | การแข่งขันบาสเกตบอลชาย NCAA Division I ปี 2018 เป็นการแข่งขันแบบน็อกเอาต์ 68 ทีม... |
| หนัง Nightmare Before Christmas เป็นภาพยนตร์ของดิสนีย์ตั้งแต่แรกหรือไม่ | นิทานก่อนวันคริสต์มาสเริ่มต้นจากบทกวีที่เขียนโดยทีม เบอร์ตันในปี 1982... |
| ทำไมเทวดาแห่งเหนือถึงอยู่ที่นั่น | ตามที่กอร์มลีย์กล่าว ความสำคัญของเทวดามีสามประการ... |
| ที่ไหนที่การประนีประนอม 3/5 ถูกกล่าวถึงในรัฐธรรมนูญ | การประนีประนอมสามในห้าพบได้ในมาตรา 1, หมวด 2, ข้อ 3... |
| ใครร้องเพลง somebody's watching me ร่วมกับไมเคิล แจ็คสัน | "Somebody's Watching Me" เป็นเพลงของนักร้องชาวอเมริกัน Rockwell... |
