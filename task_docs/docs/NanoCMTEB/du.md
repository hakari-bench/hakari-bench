# NanoCMTEB / du

## Overview

NanoCMTEB `du` is a Chinese web passage retrieval task based on the DuReader-retrieval family. Queries are very short Chinese information requests, and documents are noisy web passages that may contain the answer. The task measures whether retrieval systems can rank multiple answer-bearing passages for short search-style queries.

## Details

### What the Original Data Measures

DuReader-retrieval is a large-scale Chinese passage retrieval benchmark derived from Baidu search and DuReader-style reading data, with human annotation over pooled retrieval results. C-MTEB includes DuRetrieval in its Chinese retrieval group.

The retrieval problem resembles real web search. A query may be only a few Chinese characters, while relevant passages can be article excerpts, forum-like answers, copied snippets, or pages with noisy formatting. Relevance depends on answerability rather than exact phrase repetition.

### Observed Data Profile

The task contains 200 queries, 10,000 documents, and 889 relevance judgments. It is strongly multi-positive: there are 4.45 positives per query on average, a minimum of 1, a median of 4.0, a maximum of 27, and 173 multi-positive queries, or 86.50% of the set.

Queries average only 9.12 Chinese characters, while documents average 397.39 characters. The short query length makes context sparse, and the high number of positives means ranking several relevant passages matters more than just finding one.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.7337, hit@10 of 0.9150, and recall@100 of 0.8639 using the top-500 BM25 candidate subset. This is a strong lexical baseline. Many short Chinese web queries contain salient answer terms, product names, symptoms, software terms, or administrative phrases that appear in relevant passages.

BM25's limitation is that answer-bearing passages may express the intent without repeating the exact query words, and noisy web text can contain query terms without answering the question. It performs well but leaves room for semantic ranking improvements.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.9286, hit@10 of 0.9800, and recall@100 of 0.9764. Dense retrieval is the strongest top-ranking profile by a large margin. It substantially improves over BM25 in nDCG@10 and recall@100.

This suggests that embedding similarity is very effective for short Chinese web-search queries. Dense retrieval can connect a compact query to answer-bearing passages even when the passage uses a different phrasing or contains noisy surrounding text.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.8224, hit@10 of 0.9300, and recall@100 of 0.9831. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 2 safeguard rows, candidate counts from 100 to 101, and a mean of 100.01 candidates.

Hybrid retrieval has the best recall@100, but dense retrieval is clearly better for top-10 ranking. The hybrid pool is useful for coverage, while dense retrieval gives the best first-page ordering among the reported profiles.

### Metric Interpretation for Model Researchers

This task is dense-favorable despite BM25 being strong. BM25 handles exact short-query matching well, but dense retrieval is much better at ranking answer-bearing passages early. Reranking_hybrid slightly improves coverage but loses top-rank precision compared with dense.

Because most queries have several positives, nDCG@10 is especially informative. A model should surface multiple useful passages near the top, not only one relevant hit. Recall@100 matters for downstream reranking and answer generation.

### Query and Relevance Type Tendencies

Queries include consumer advice, medicine and health questions, household troubleshooting, document editing instructions, product origin, and public information requests. Positive passages often include web snippets, copied answer text, practical guides, or article paragraphs.

The relevance relation is answer-bearing passage retrieval. A positive passage should answer the query intent directly, even if it contains noisy surrounding text or duplicated formatting.

### Representative Failure Modes

Likely failures include retrieving passages that repeat query terms without answering, missing answer passages that use paraphrases, over-ranking outdated or irrelevant copied text, and failing to rank multiple valid positives for a broad query.

BM25 is vulnerable to exact-token distractors. Dense retrieval can still over-match general topic when the query is ambiguous. Hybrid retrieval improves coverage but may not preserve dense's strongest top ordering.

### Training Data That May Help

Useful training data includes non-overlapping DuReader retrieval pairs, Chinese web search query-passage annotations, answer-bearing passage retrieval data, and lexical-overlap hard negatives from the same query topic.

Synthetic data should use noisy Chinese web passages and generate short search queries answerable by one or more passages. Hard negatives should share named entities or exact query words but omit the answer, contain outdated information, or discuss a different facet.

### Model Improvement Notes

Strong systems should handle very short Chinese queries, web noise, and multi-positive ranking. Dense retrieval is the strongest observed first-stage method, while BM25 remains a valuable baseline for exact phrase and entity matching. Rerankers should prioritize answerability over mere term overlap.

The task is useful for evaluating Chinese search retrieval under realistic short-query conditions.

## Example Data

| Query | Positive document |
| --- | --- |
| 吃阿莫西林后多久能喝酒 [11 chars] | 吃完阿莫西林后大概过五个小时喝酒就不会引起中毒，阿莫西林五小时基本全部消化一、何谓双硫仑和双硫仑样反应？双硫仑（disulfiram）是一种戒酒药物，服用该药后即使饮用少量的酒，身体也会产生严重不适，而达到戒酒的目的。双硫仑的作用机制在于——双硫仑在与乙醇联用时可抑制肝脏中的乙醛脱氢酶，使乙醇在体内氧化为乙醛后，不能再继续分解氧化，导致体内乙醛蓄积而产生一系列反应。双硫仑样反应——许多药物具有与双硫仑相似的作用，用药后若饮酒，会发生面部潮红、眼结膜充血、视觉模糊、头颈部血管剧烈搏动或搏动性头痛、头晕，恶心、呕吐、出汗、口干、胸痛、心肌梗塞、急性心衰、呼吸困难、急性肝损伤，惊厥及死亡等。查体时可有血压下降、心率加速（可达 120 次 /min）及心电图正常或部分改变（如 ST—T 改变）。其严重程度与用药剂量和饮酒量成正比关系，老年人、儿童、心脑血管病及对乙醇敏感者更为严重，这种反应一般在用药与饮酒后 15-30 分钟发生。二、哪些药物可导致双硫仑样反应？1. 头孢菌素类药物中的头孢哌酮、头孢哌酮舒巴坦、头孢曲松、头孢唑林（先锋Ⅴ号）、头孢拉啶（先锋Ⅵ号）、头孢美唑、头孢美唑、头孢米诺、拉氧头孢、头孢甲肟、头孢孟多、头孢氨苄（先锋Ⅳ号）、头孢克洛等。其中以头孢哌酮致双硫仑样反应的报告最多、最敏感。如有患者在使用后吃酒心巧克力、服用藿香正气水，甚至仅用酒精处理皮肤也会发生双硫仑样反应。这些头孢菌素类药物在化学结构上共同的特点是，在其母核 7- 氨基头孢烷酸（7-ACA）环的 3 位上存在于双硫仑分子类似的甲硫四氮唑（硫代甲基四唑）取代基，其与辅酶Ⅰ竞争乙醛脱氢酶的活性中心，可阻止乙醛继续氧化，导致乙醛蓄积，从而引起戒酒硫样反应。理论上说，头孢曲松、头孢噻肟、头孢他啶、头孢磺啶、头孢唑肟、头孢克肟，因不含甲硫四氮唑基团，在应用期间饮酒不会引起双硫仑样反应。但是有报道称头孢曲松虽然不具有甲硫氢唑侧链，但有甲硫三嗪侧链也可引起此类反应，故被排除在外。另有头孢他啶致双硫仑样反应报道。2. 硝咪唑类药物如甲硝唑（灭滴灵）、替硝唑、奥硝唑、塞克硝唑。3. 其他抗菌药如呋喃唑酮（痢特灵）、氯霉素、酮康唑、灰黄霉素、磺胺类（磺胺甲恶唑）等。三、饮酒多久后可以用头孢类抗生素？据相关文献报道 , 头孢类抗生素致双硫仑样反应与饮酒可达 99% 的密切相关。由于个体差异存在，每个人酒精消除时间... [1,000 / 2,130 chars] |
| 暖气只有一片热 [7 chars] | 林内燃气热水器家用水过滤器冰箱后面空调病治疗人类性功能缺陷中有空气的缘故。每组暖气片上都有一个跑风，也就是顶端有一个螺栓，这是放空气用的，你把它拧松，空气就会跑出来，等所跑完出来水后，再拧紧就好啦。如果没有这个放气的螺栓，那就找家政的或是物业的人用大扳手直接在暖气片组的上端把片头上的堵头拧松，放出空气就好啦。祝你幸福快乐！以下是联盟知识库http://zhishi.010lm.com总结网友的解决办法，仅供参考----------------------------------------------------- [260 chars] |
| 如何从第三页开始设置页眉 [12 chars] | 通过插入分节符就可以实现此功能。第一步：将光标定在word第三页的最末尾，点击word工具栏中的“页面布局”，选择“分隔符”，再选择“下一页”；第二步：双击页眉，然后点击页眉和页脚工具栏中的“链接到前一条页眉”将选项，使其变成灰色；第三步：直接删除word前三页的页眉即可，此时后面的页眉不会被删除的。详细的图文说明可以参照此经验：http://jingyan.baidu.com/article/cb5d61050df4e5005c2fe0b8.html如果要设置不同样式的页码，页眉页脚，需要插入分节符，主要技术在于：从正文开始和前面的内容（比如封面、目录）之间要插入一个分隔符－－下一页（分节符），然后再设置正文的页脚（正文页脚通过页眉页脚设置，选择“链接到上一页”，然后分别设置第三页开始的页眉。在断开链接的前提下，如果需要从第三页开始设置页码，单击页眉页脚工具栏上的“手#”按钮，设置格式和起始页码（一般为1），单击“#”按钮插入页码。把第一节的页码直接删掉 或者修改成Ⅰ、Ⅱ格式的页码（刚才单击了链接到上一页，就能这样分别设置了，否则就只能设置完全一样的页眉页脚）。大侠在线 358725389@qq.com [510 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Task paper | [DuReader-retrieval: A Large-scale Chinese Benchmark for Passage Retrieval](https://aclanthology.org/2022.emnlp-main.357/) |
| Benchmark paper | [C-Pack: Packed Resources For General Chinese Embeddings](https://arxiv.org/abs/2309.07597) |
| Source dataset | [mteb/DuRetrieval](https://huggingface.co/datasets/mteb/DuRetrieval) |
| NanoCMTEB dataset | [hakari-bench/NanoCMTEB](https://huggingface.co/datasets/hakari-bench/NanoCMTEB) |

Representative query and positive source snippets:

| Query | Positive document snippet |
| --- | --- |
| 吃阿莫西林后多久能喝酒 | A medical passage explains drug-alcohol reactions and timing after amoxicillin. |
| 暖气只有一片热 | A household troubleshooting passage explains trapped air in radiators and venting. |
| 如何从第三页开始设置页眉 | A Word editing passage explains inserting a section break and unlinking headers. |
| gpt升高的原因 | A health passage explains common reasons for elevated GPT or ALT. |
| 哪里的蚕丝最好 | A consumer information passage discusses major Chinese silk-producing regions. |
