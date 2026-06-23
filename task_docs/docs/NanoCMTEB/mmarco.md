# NanoCMTEB / mmarco

## Overview

NanoCMTEB `mmarco` is a Chinese passage retrieval task based on mMARCO, the multilingual version of MS MARCO passage ranking. Queries are short Chinese fact-seeking information needs, and documents are translated web passages. The task measures whether retrieval systems can rank answer-bearing Chinese passages while handling translation artifacts, named entities, and short-query ambiguity.

## Details

### What the Original Data Measures

mMARCO translates MS MARCO passage-ranking data into multiple languages, including Chinese. The relevance structure comes from MS MARCO-style web information needs, while the surface text is machine translated. C-MTEB includes MMarcoRetrieval as part of its Chinese retrieval evaluation.

This task is therefore not identical to native Chinese web search. It tests multilingual and translated-passage retrieval, where English-origin entities, brands, names, and phrasing may remain visible in Chinese text.

### Observed Data Profile

The task contains 200 queries, 10,000 documents, and 212 relevance judgments. It is mostly single-positive: there are 1.06 positives per query on average, a minimum of 1, a median of 1.0, a maximum of 2, and 12 multi-positive queries, or 6.00% of the set.

Queries average 10.44 Chinese characters, and documents average 113.91 characters. Examples include historical effects, biology and kidney function, actors and film roles, consumer electronics, word meanings, animal facts, and celebrity information.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6795, hit@10 of 0.8050, and recall@100 of 0.9104 using the top-500 BM25 candidate subset. This is a strong lexical baseline because many fact-seeking queries contain named entities, technical terms, or translated answer terms that appear in the positive passage.

BM25 can struggle when translation choices differ, when the query is paraphrased, or when entity-sharing negatives answer a different fact. It is strong but not the best ranking profile.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.8859, hit@10 of 0.9350, and recall@100 of 0.9717. Dense retrieval is the strongest top-ranking profile by a wide margin. It improves substantially over BM25 in nDCG@10 and hit@10.

This indicates that embedding similarity is effective for translated MS MARCO-style retrieval. Dense retrieval can connect short Chinese queries to answer-bearing passages even when wording differs or translation artifacts appear.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.7984, hit@10 of 0.9000, and recall@100 of 0.9858. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 3 safeguard rows, candidate counts from 100 to 101, and a mean of 100.02 candidates.

Hybrid retrieval has the best recall@100, but dense retrieval remains best for top-10 ranking. The hybrid pool is valuable for downstream reranking, while dense is the strongest observed first-stage ranker.

### Metric Interpretation for Model Researchers

This task is dense-favorable with a hybrid coverage advantage. BM25 is already strong because many translated facts preserve lexical anchors, but dense retrieval gives much better first-page ordering. Reranking_hybrid exposes slightly more positives in the top 100.

Researchers should account for translation artifacts. A model that performs well may be handling both Chinese semantics and English-origin entity traces. Evaluation should focus on answer-bearing relevance, not only entity overlap.

### Query and Relevance Type Tendencies

Queries ask about historical effects, biological mechanisms, celebrity roles, device setup, word meanings, consumer facts, travel advice, and simple factual knowledge. Positive documents are short translated passages that contain the answer.

The relevance relation is answer containment. A passage is positive if it satisfies the information need, often with a concise explanation or factual statement.

### Representative Failure Modes

Likely failures include retrieving a passage with the same entity but the wrong fact, missing a passage due to translation variation, over-ranking literal term matches that do not answer the query, and confusing ambiguous short queries.

BM25 is vulnerable to translated lexical mismatch and entity-sharing distractors. Dense retrieval can over-generalize topic similarity. Hybrid retrieval improves coverage but can lose some dense top-rank precision.

### Training Data That May Help

Useful training data includes non-overlapping mMARCO Chinese query-passage pairs, multilingual MS MARCO passage ranking data, Chinese fact-seeking QA retrieval pairs, and translated entity-sharing hard negatives.

Synthetic data can translate or generate fact-seeking web passages and Chinese queries over them. Hard negatives should share entity names, units, or question types while answering a different fact.

### Model Improvement Notes

Strong systems should handle Chinese short queries, translated passage phrasing, and named-entity preservation. Dense retrieval is the strongest observed first-stage method, while hybrid retrieval is useful when recall@100 matters.

The task is useful for evaluating multilingual retrieval models on Chinese MS MARCO-style passage ranking, especially when translation quality and entity handling influence retrieval effectiveness.

## Example Data

| Query | Positive document |
| --- | --- |
| 黑死病对欧洲文化的影响 [11 chars] | 继续阅读以了解他们的发现。在接下来的几个世纪里，黑死病在欧洲偶尔抬头。但到了 1352 年，它基本上已经放松了控制。欧洲人口受到重创，这对经济产生了影响。劳动力被摧毁——农场被废弃，建筑物倒塌。劳动力短缺，劳动力价格飞涨，商品成本上升。 [118 chars] |
| adh 的增加会导致肾脏 ________ 重吸收水分，从而产生 _______ 尿液。 [44 chars] | 抗利尿激素 (ADH) 和肾功能。 ADH 的主要作用是通过增加重新吸收到血液中的水量来限制尿液中丢失的水量。 [55 chars] |
| 拒绝漂亮女人和鬼魂的女演员 [13 chars] | 莫莉·林沃德拒绝了《漂亮女人》中薇薇安的角色和《鬼魂》中莫莉的角色等。她还获得了《尖叫》中的一个角色，但她拒绝了，因为她已经 20 岁了，不想扮演青少年角色。 [79 chars] |
| 索尼 PS-LX300USB 如何连接电脑 [21 chars] | 连接 USB 电缆 使用随附的 USB 电缆连接唱盘和计算机。USB 电缆（提供）到 USB 端口到 USB 插孔计算机（未提供）。 11 GB 操作 PS-LX300USB.GB.3-198-123-15(1) 续 ÃƒÂ®Ã‚â€‚‚Â¼ Notes ÃƒÂ®Ã‚ ‚ 不保证转盘可与 USB 集线器或 USB 一起使用延长线。使用随附的 USB 线。 ÃƒÂ®Ã‚ ‚ 将 USB 电缆牢固地连... [200 / 342 chars] |
| 争论辩论的意义 [7 chars] | 同义词讨论辩论。讨论，争论，辩论的意思是为了得出结论或说服而进行的讨论。讨论意味着对可能性的筛选，特别是通过提出正反两方面的考虑，讨论对新高速公路的需求。 [77 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Task paper | [mMARCO: A Multilingual Version of the MS MARCO Passage Ranking Dataset](https://arxiv.org/abs/2108.13897) |
| Benchmark paper | [C-Pack: Packed Resources For General Chinese Embeddings](https://arxiv.org/abs/2309.07597) |
| Source dataset | [mteb/MMarcoRetrieval](https://huggingface.co/datasets/mteb/MMarcoRetrieval) |
| NanoCMTEB dataset | [hakari-bench/NanoCMTEB](https://huggingface.co/datasets/hakari-bench/NanoCMTEB) |

Representative query and positive source snippets:

| Query | Positive document snippet |
| --- | --- |
| 黑死病对欧洲文化的影响 | A passage describes demographic and economic effects of the Black Death in Europe. |
| ADH 增加会导致肾脏怎样重吸收水分？ | A passage explains antidiuretic hormone and kidney water reabsorption. |
| 拒绝漂亮女人和鬼魂的女演员 | A passage identifies an actress who declined roles in those films. |
| 索尼 PS-LX300USB 如何连接电脑 | A passage describes connecting the turntable to a computer with a USB cable. |
| 争论辩论的意义 | A passage explains meanings of discussion, argument, and debate. |
