# MNanoBEIR / NanoBEIR-th / NanoFEVER

## Overview

NanoFEVER in the Thai NanoBEIR slice is a Wikipedia evidence retrieval task derived from FEVER. The queries are Thai translated factual claims, and the corpus contains Thai translated evidence passages. The retrieval goal is to find passages that can verify the claim, not just passages that mention the same entity or topic. This compact task is useful for evaluating entity grounding, claim-to-evidence matching, and factual retrieval behavior in Thai.

## Details

### What the Original Data Measures

FEVER was created for fact extraction and verification over Wikipedia. In retrieval form, a claim must be matched to evidence passages that contain enough information to assess it. The relevant passage often centers on a named entity, work, person, location, or event, but relevance depends on the specific factual relation in the claim.

The Thai translated version tests whether a model can handle factual claims with Thai wording and mixed entity forms. Some names, media titles, or organizations remain in English or transliterated forms, while surrounding text is Thai. A strong retriever must preserve those exact anchors while also ranking the passage that actually verifies the claim.

### Observed Data Profile

The task contains 50 queries, 4,996 documents, and 57 relevance judgments. Most queries have one positive passage, with an average of 1.14 positives per query. The minimum is 1, the median is 1.0, the maximum is 3, and 6 queries are multi-positive, or 12.0% of the query set. This is therefore mostly a single-evidence retrieval benchmark.

Queries average 46.88 characters, while documents average 1,084.74 characters. The claims are short, but the evidence passages are longer Wikipedia-style texts. The model must identify the specific evidence-bearing passage within a larger topical neighborhood.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.7001, hit@10 of 0.8200, and recall@100 of 0.9474 using the top-500 BM25 candidate subset. This is a strong lexical profile. FEVER-style claims often preserve named entities and distinctive words that also appear in the evidence passages, so BM25 can recover many positives by rank 100.

The lower hit@10 compared with recall@100 shows that lexical retrieval still struggles with top-rank ordering. BM25 may retrieve multiple passages about the same entity, but not always the one that verifies the specific claim. Thai segmentation and translated phrasing can also affect exact matching.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.8663, hit@10 of 0.9600, and recall@100 of 0.9825. Dense retrieval is clearly strongest among the individual modes. It improves both top-rank quality and candidate coverage, showing that embedding similarity captures claim-evidence semantics beyond exact entity overlap.

The dense advantage is especially important for claims whose evidence relation is not fully represented by shared terms. Dense retrieval can better distinguish the passage that answers the claim from other passages about the same person, work, or place. Remaining errors are likely to involve rare entities, title ambiguity, or very fine factual distinctions.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.7768, hit@10 of 0.9000, and recall@100 of 0.9825. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 1 safeguard row and a mean of 100.02 candidates. Its recall@100 matches dense retrieval, but dense has better top-10 ordering and hit@10.

This suggests that hybrid search preserves strong candidate coverage but does not improve first-stage ranking on this Thai FEVER slice. Lexical signals help ensure coverage for entity-heavy claims, yet they can also pull same-entity distractors upward. For direct retrieval, dense similarity is the strongest signal; for reranking pipelines, the hybrid pool remains useful because relevant passages are usually included.

### Metric Interpretation for Model Researchers

Because most queries have one positive, nDCG@10 and hit@10 are direct indicators of whether the evidence passage appears where a verifier or RAG system can use it. recall@100 measures whether downstream reranking has access to the evidence. Here, BM25 already has high recall, but dense retrieval converts recall into much better top-rank quality.

The method comparison shows a clear semantic ranking advantage. BM25 finds many candidates through entity overlap. Dense retrieval best identifies the evidence-bearing passage. reranking_hybrid keeps high recall but does not beat dense ordering. This task is useful for testing whether a model ranks evidence, not just entity-related text.

### Query and Relevance Type Tendencies

Queries include factual claims such as whether Keith Godchaux knew Grateful Dead, whether Taarak Mehta Ka Ooltah Chashmah is a sitcom, whether advanced secret aircraft were made in Burbank, whether Nero was a person, and whether Scream 2 is exclusively German. Relevant documents are Wikipedia-style evidence passages.

The task rewards exact entity grounding and factual relation matching. A passage can be topically close but wrong if it discusses the entity without resolving the claim. Claims involving exclusivity, identity, or category membership require especially careful evidence ranking.

### Representative Failure Modes

Likely failures include retrieving the correct entity page but the wrong factual passage, confusing similarly named works or people, missing evidence because Thai wording differs from the source entity form, and over-ranking broad background passages. BM25 may overvalue repeated names, while dense retrieval may still struggle with rare or mixed-script titles.

### Training Data That May Help

Useful training data includes Thai claim-evidence retrieval, Wikipedia evidence mining, multilingual fact-checking, and hard negatives that share the same entity but do not verify the claim. Translated FEVER-like data can help if evaluation overlap is avoided. For rerankers, same-entity non-evidence passages are especially valuable.

### Model Improvement Notes

A model targeting this task should preserve entity precision while improving evidence-relation ranking. Sparse systems need Thai-aware tokenization and strong named-entity handling. Dense systems are the strongest direct baseline and can be improved with claim-specific hard negatives. Hybrid systems should use their high recall with a reranker that explicitly compares the claim to the passage.

## Example Data

| Query | Positive document |
| --- | --- |
| คีธ กอดชอว์ รู้จักเกรทฟูล เดด. [30 chars] | Grateful Dead เป็นวงร็อคอเมริกันที่ก่อตั้งขึ้นในปี 1965 ที่พาโลอัลโต รัฐแคลิฟอร์เนีย วงนี้มีสมาชิกตั้งแต่ห้าคนถึงเจ็ดคน และเป็นที่รู้จักในสไตล์ที่เป็นเอกลักษณ์และหลากหลาย ซึ่งผสมผสานองค์ประกอบของร็อค,... [200 / 2,683 chars] |
| Taarak Mehta Ka Ooltah Chashmah ซิทคอม? [39 chars] | ตาราค เมห์ตา คา อูลดาห์ ชัชมะ (ภาษาอังกฤษ: มุมมองที่แตกต่างของตาราค เมห์ตา) เป็นซิทคอมที่มีการออกอากาศยาวนานที่สุดในอินเดีย ผลิตโดย Neela Tele Films Private Limited รายการเริ่มออกอากาศเมื่อวันที่ 28 ก... [200 / 565 chars] |
| มีเครื่องบินลับและมีเทคโนโลยีขั้นสูงถูกผลิตในเบอร์แบงค์ รัฐแคลิฟอร์เนียหรือไม่? [79 chars] | เบอร์แบงค์เป็นเมืองในเขตลอสแองเจลิสในแคลิฟอร์เนียตอนใต้ สหรัฐอเมริกา ห่างจากใจกลางเมืองลอสแองเจลิสไปทางตะวันตกเฉียงเหนือ 12 ไมล์ ประชากรในปี 2010 มีจำนวน 103,340 คน ถูกเรียกว่า "เมืองหลวงแห่งสื่อของโล... [200 / 1,266 chars] |
| เนโรเป็นคนไหม? [14 chars] | คำว่า ราชวงศ์จูเลียส-คลอเดียน หมายถึง จักรพรรดิ์โรมันทั้งห้าพระองค์แรก -- ออกุสตุส, ไทเบอเรียส, คาเลกูล่า, คลอเดียส, และเนโร -- หรือครอบครัวที่พวกเขาสังกัด พวกเขาปกครองจักรวรรดิโรมันตั้งแต่การก่อตั้งภ... [200 / 2,029 chars] |
| Scream 2 เป็นภาพยนตร์เยอรมันโดยเฉพาะ [36 chars] | Scream 2 เป็นภาพยนตร์สแลชเชอร์อเมริกันที่ออกฉายในปี 1997 กำกับโดยเวส คราเวน และเขียนโดยเควิน วิลเลียมสัน นำแสดงโดยเดวิด อาร์เควตต์, เนฟ แคมป์เบลล์, คอร์ตนีย์ คอกซ์, ซาราห์ มิเชล เกลลาร์, เจมี่ เคนเนดี... [200 / 2,249 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [FEVER](https://arxiv.org/abs/1803.05355) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-th dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |

Representative query and positive evidence snippets:

| Query | Positive document snippet |
| --- | --- |
| คีธ กอดชอว์ รู้จักเกรทฟูล เดด. | Grateful Dead เป็นวงร็อคอเมริกันที่ก่อตั้งขึ้นในปี 1965 ที่พาโลอัลโต... |
| Taarak Mehta Ka Ooltah Chashmah ซิทคอม? | ตาราค เมห์ตา คา อูลดาห์ ชัชมะ เป็นซิทคอมที่มีการออกอากาศยาวนานที่สุด... |
| มีเครื่องบินลับและมีเทคโนโลยีขั้นสูงถูกผลิตในเบอร์แบงค์ รัฐแคลิฟอร์เนียหรือไม่? | เบอร์แบงค์เป็นเมืองในเขตลอสแองเจลิสในแคลิฟอร์เนียตอนใต้... |
| เนโรเป็นคนไหม? | คำว่า ราชวงศ์จูเลียส-คลอเดียน หมายถึง จักรพรรดิ์โรมันทั้งห้าพระองค์แรก... |
| Scream 2 เป็นภาพยนตร์เยอรมันโดยเฉพาะ | Scream 2 เป็นภาพยนตร์สแลชเชอร์อเมริกันที่ออกฉายในปี 1997... |
