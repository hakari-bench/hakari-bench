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
| 吃阿莫西林后多久能喝酒 [11 chars] | 吃完阿莫西林后大概过五个小时喝酒就不会引起中毒，阿莫西林五小时基本全部消化一、何谓双硫仑和双硫仑样反应？双硫仑（disulfiram）是一种戒酒药物，服用该药后即使饮用少量的酒，身体也会产生严重不适，而达到戒酒的目的。双硫仑的作用机制在于——双硫仑在与乙醇联用时可抑制肝脏中的乙醛脱氢酶，使乙醇在体内氧化为乙醛后，不能再继续分解氧化，导致体内乙醛蓄积而产生一系列反应。双硫仑样反应——许多药物具有与双... [200 / 2,130 chars] |
| 暖气只有一片热 [7 chars] | 林内燃气热水器家用水过滤器冰箱后面空调病治疗人类性功能缺陷中有空气的缘故。每组暖气片上都有一个跑风，也就是顶端有一个螺栓，这是放空气用的，你把它拧松，空气就会跑出来，等所跑完出来水后，再拧紧就好啦。如果没有这个放气的螺栓，那就找家政的或是物业的人用大扳手直接在暖气片组的上端把片头上的堵头拧松，放出空气就好啦。祝你幸福快乐！以下是联盟知识库http://zhishi.010lm.com总结网友的解决... [200 / 260 chars] |
| 如何从第三页开始设置页眉 [12 chars] | 通过插入分节符就可以实现此功能。第一步：将光标定在word第三页的最末尾，点击word工具栏中的“页面布局”，选择“分隔符”，再选择“下一页”；第二步：双击页眉，然后点击页眉和页脚工具栏中的“链接到前一条页眉”将选项，使其变成灰色；第三步：直接删除word前三页的页眉即可，此时后面的页眉不会被删除的。详细的图文说明可以参照此经验：http://jingyan.baidu.com/article/c... [200 / 510 chars] |
| gpt升高的原因 [8 chars] | 谷丙转氨酶（简称GPT、ALT）升高在临床是很常见的现象。肝脏是人体最大的解毒器官，该脏器是不是正常，对人体来说是非常重要的。GPT升高肝脏功能出现问题的一个重要指标。在常见的因素里，各类肝炎都可以引起GPT升高，这是由于肝脏受到破坏所造成的。一些药物如抗肿瘤药、抗结核药，都会引起肝脏功能损害。大量喝酒、食用某些食物也会引起肝功能短时间损害。GPT主要存在于肝细胞浆内，其胞内浓度高于血清中1000... [200 / 1,269 chars] |
| 哪里的蚕丝最好 [7 chars] | 中国古代蚕丝主产区：长三角特别是杭嘉湖，湖州有“湖丝甲天下”的美誉，当时湖州南浔那边的蚕丝是最好的。还有就是珠三角和四川盆地。现在长三角随着经济的发展，种桑养蚕的人越来越少了，东桑西移成了一种趋势。目前全国蚕茧产量最多的是广西，质量比较好的应该属浙北、苏南还有山东等地。至于从蚕茧制成蚕丝，比较好的有这么几个地方：1、浙江桐乡：桑蚕丝产量占到全国的40%以上2、江苏吴江震泽、江苏海安县：特别是海安县... [200 / 236 chars] |

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
