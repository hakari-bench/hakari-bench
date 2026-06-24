# MNanoBEIR / NanoBEIR-th / NanoHotpotQA

## Overview

NanoHotpotQA in the Thai NanoBEIR slice is a multi-hop Wikipedia retrieval task derived from HotpotQA. The queries are Thai translated questions, and the corpus contains Thai translated supporting passages. Each query has exactly two relevant passages, so the benchmark measures whether a retriever can recover the connected evidence needed for explainable question answering. It is a compact diagnostic for bridge-entity retrieval, multi-positive ranking, and Thai question-to-passage matching.

## Details

### What the Original Data Measures

HotpotQA was created for diverse and explainable multi-hop question answering. In retrieval form, the model must find supporting passages that together answer the question. One passage may identify a bridge entity, while another supplies the answer or completes the relation. Retrieving only one support is often insufficient for the reasoning chain.

The Thai translated version tests this behavior with Thai questions and translated Wikipedia-style passages. Queries often mention one entity, relation, or event and ask about another connected entity. A strong model must combine exact entity matching with semantic bridge reasoning rather than stopping at the first obvious topical passage.

### Observed Data Profile

The task contains 50 queries, 5,090 documents, and 100 relevance judgments. Every query has exactly two positives: the average, minimum, median, and maximum positives per query are all 2.0, and every query is multi-positive. This gives the task a fixed two-support structure.

Queries average 79.74 characters, while documents average 330.66 characters. The queries are moderately long because they often include a bridge description, and the documents are concise encyclopedia passages. The model must map a compact multi-hop question to both supporting passages.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.5523, hit@10 of 0.8800, and recall@100 of 0.8600 using the top-500 BM25 candidate subset. This shows that lexical matching is useful but incomplete. Many questions contain named entities that BM25 can match, but the second support passage may be less lexically obvious.

The task's two-positive structure makes this important. A model can retrieve one entity passage and still miss the bridge passage needed to answer the question. BM25 tends to find visible names and surface terms, but it may struggle when the support relation is expressed indirectly or when Thai translation changes the lexical form.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.6880, hit@10 of 0.9400, and recall@100 of 0.9500. Dense retrieval improves strongly over BM25 across all metrics. This indicates that embedding similarity captures the relation between the question and the supporting passages better than exact term overlap alone.

The dense profile is well aligned with multi-hop retrieval. It can retrieve passages that are semantically connected to the question even if they do not repeat every query term. Remaining errors are likely to involve entity ambiguity, mixed-script names, or cases where the second support is only weakly signaled by the query wording.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.6652, hit@10 of 0.9800, and recall@100 of 0.9600. It uses exactly 100 candidates per query, with no rank-101 safeguard rows. The hybrid profile has the best hit@10 and recall@100, while dense retrieval has the best nDCG@10.

This suggests that hybrid search is especially useful for making sure at least one support and the full support pool are present in the candidate set. However, dense retrieval orders the top 10 slightly better overall. For Thai HotpotQA, reranking_hybrid is a strong candidate generator, and a later reranker should focus on ranking both supports high.

### Metric Interpretation for Model Researchers

hit@10 is useful but incomplete because every query has two positives. A model can hit by finding one support passage while still failing the multi-hop evidence objective. nDCG@10 better reflects whether the top ranks contain the support set, and recall@100 measures whether downstream reranking can access both positives.

The method comparison shows that BM25 relies on visible entity anchors, dense retrieval provides the strongest top-rank semantic ordering, and reranking_hybrid gives the broadest support coverage. This task is useful for evaluating whether a retriever can move from single-entity matching to complete multi-hop evidence retrieval.

### Query and Relevance Type Tendencies

Queries ask bridge-style questions such as whether Penny Rae Bridges acted in a sitcom with Ben Savage, who gave Kaganoi Shigemochi a sword made by the founder of the Muramasa school, which film was written and directed by Joby Harold with music by Samuel Sim, and when a Clemson-Oklahoma football game was played. Relevant documents are supporting passages that jointly resolve the chain.

The task rewards models that track people, works, events, dates, and relationships. A passage about one named entity may be relevant, but the second support is often needed to answer the question. Systems that retrieve only the query-mentioned entity will underperform on support completeness.

### Representative Failure Modes

Likely failures include retrieving only one of the two supports, confusing similarly named people or works, missing the bridge passage when it uses different Thai wording, and over-ranking passages that share an entity but do not complete the reasoning chain. BM25 may over-focus on explicit names, while dense retrieval may retrieve related but incomplete evidence.

### Training Data That May Help

Useful training data includes Thai multi-hop QA, Wikipedia bridge-question retrieval, paired supporting-passage ranking, multilingual QA, and hard negatives that mention one entity but omit the bridge fact. For rerankers, examples where only one support is present are especially important hard negatives.

### Model Improvement Notes

A model targeting this task should optimize for support-set recovery, not only first-positive discovery. Sparse systems need strong named-entity and title handling with Thai-aware tokenization. Dense systems should improve relation and bridge-entity matching. Hybrid systems are promising as candidate sources, but the final ranking should explicitly favor retrieving both required supports.

## Example Data

| Query | Positive document |
| --- | --- |
| เพนนี เรย์ บริดจ์แสดงในซิทคอมโทรทัศน์กับเบน ซาเวจหรือไม่? [57 chars] | เพนนี เรย์ บริดจ์ส (เกิด 29 กรกฎาคม 1990) เป็นนักแสดงชาวอเมริกัน ผลงานทางโทรทัศน์ของเธอรวมถึงบทบาทใน "For Your Love", "Family Law", "Boy Meets World" และ "The Parent 'Hood" เธอเป็นที่รู้จักดีที่สุดจากบทบาทใน "Half & Half" ในฐานะโมนาวัยเยาว์ [240 chars] |
| ใครมอบดาบที่ทำโดยผู้ก่อตั้งโรงเรียนมุรามาสะให้กับคางาโนอิ ชิเกโมจิ? [67 chars] | คางาโนอิ ชิเกโมชิ (加賀井 重望, 1561 – 27 สิงหาคม 1600) เป็นซามูไรชาวญี่ปุ่นในยุคอาซูจิ-โมโมยามะ ผู้รับใช้ตระกูลโอดะ เขาปกครองปราสาทคางาโนอิ ในระหว่างการรบที่โคมากิและนากาคุเตะ ชิเกโมชิได้ต่อสู้ภายใต้การนำของบิดา ชิเกมุเนะ ซึ่งอยู่ในกองกำลังของโอดะ โนบุกัตสึ หลังจากนั้นไม่นาน ปราสาทคางาโนอิถูกล้อมโดยกองกำลังของโทโยโทมิ ฮิเดโยชิ; ชิเกมุเนะยอมจำนน และชิเกโมชิได้รับการจ้างงานจากฮิเดโยชิในฐานะผู้ส่งสาร โดยได้รับเงินเดือน 10,000 "โคคุ" เขายังมีดาบที่ทำโดยมุรามาสะ ซึ่งฮิเดโยชิมอบให้เขาในปี 1598 [488 chars] |
| ภาพยนตร์เรื่องไหนที่เขียนและกำกับโดยโจบี้ ฮาร์โรลด์ พร้อมดนตรีที่เขียนโดยซามูเอล ซิม? [85 chars] | ซามูเอล ซิม เป็นนักแต่งเพลงสำหรับภาพยนตร์และโทรทัศน์ เขาเริ่มได้รับการยอมรับจากคะแนนเสียงที่ได้รับรางวัลสำหรับซีรีส์ดราม่า "ดันเคิร์ก" ของ BBC ตั้งแต่นั้นมาเขาได้แต่งเพลงสำหรับการผลิตภาพยนตร์และโทรทัศน์ที่หลากหลาย โดยล่าสุดได้แต่งเพลงประกอบภาพยนตร์ "Awake" สำหรับ The Weinstein Company และซีรีส์ดราม่า "House of Saddam" ของ BBC/HBO เพลงที่ได้รับการชื่นชมล่าสุดของเขาคือเพลงประกอบสำหรับ Home Fires. Home Fires (Music from the Television Series) วางจำหน่ายเมื่อวันที่ 6 พฤษภาคม 2016 โดย Sony Classical Records. [508 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [HotpotQA](https://arxiv.org/abs/1809.09600) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-th dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |

Representative query and positive supporting-passage snippets:

| Query | Positive document snippet |
| --- | --- |
| เพนนี เรย์ บริดจ์แสดงในซิทคอมโทรทัศน์กับเบน ซาเวจหรือไม่? | เพนนี เรย์ บริดจ์ส เป็นนักแสดงชาวอเมริกัน ผลงานทางโทรทัศน์ของเธอรวมถึง... |
| ใครมอบดาบที่ทำโดยผู้ก่อตั้งโรงเรียนมุรามาสะให้กับคางาโนอิ ชิเกโมจิ? | คางาโนอิ ชิเกโมชิ เป็นซามูไรชาวญี่ปุ่นในยุคอาซูจิ-โมโมยามะ... |
| ภาพยนตร์เรื่องไหนที่เขียนและกำกับโดยโจบี้ ฮาร์โรลด์ พร้อมดนตรีที่เขียนโดยซามูเอล ซิม? | ซามูเอล ซิม เป็นนักแต่งเพลงสำหรับภาพยนตร์และโทรทัศน์... |
| วันที่เล่นของเกมฟุตบอลวิทยาลัยนี้ที่สนามซันไลฟ์ในไมอามี่การ์เดนส์ รัฐฟลอริดา คือเมื่อไหร่ ที่คลีมสันเอาชนะหมายเลข 4 โอคลาโฮมาซูนเนอร์ส 37-17? | ทีมฟุตบอล Clemson Tigers ปี 2015 แทนมหาวิทยาลัย Clemson ในฤดูกาลฟุตบอล NCAA Division I FBS... |
| อาหารของปีศาจเป็นการรวบรวมเพลงเดี่ยวโดยวงดนตรีร็อคแอนด์โรลจากอเมริกาที่รู้จักกันในการแสดงเพลงคันทรีภายใต้ชื่ออะไร? | Devil's Food เป็นการรวมเพลงซิงเกิลของวงร็อกแอนด์โรลอเมริกัน Supersuckers... |
