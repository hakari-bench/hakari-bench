# NanoMLDR / zh

## Overview

`NanoMLDR / zh` is the Chinese split of NanoMLDR, a multilingual long-document
retrieval benchmark derived from MLDR. Chinese paragraph-grounded questions
retrieve full Chinese articles from Wikipedia and Wudao-style sources. The Nano
split has 200 queries, 7,877 documents, and 200 positive qrel rows, with
exactly one positive document per query. Current diagnostics show BM25 as much
stronger than dense retrieval, while `reranking_hybrid` recovers nearly the same
recall@100 as BM25 but remains well below BM25 for top-rank quality.

## Details

### What the Original Data Measures

MLDR was introduced with the M3-Embedding work as a multilingual long-document
retrieval benchmark. The dataset card describes sampling long documents,
selecting a paragraph, and generating a specific question from that paragraph.
The Chinese split is described as sourced from Wikipedia and Wudao-style
articles.

The retrieval target is the full Chinese article containing the answer-bearing
paragraph. The query is short relative to the document, so the model must use a
small amount of paragraph-derived evidence to identify a long article.

### Observed Data Profile

The Nano split contains 200 queries, 7,877 documents, and 200 positive qrel
rows. Every query has exactly one positive document. Queries average 20.68
characters, while documents average 12,307.31 characters.

Observed examples include questions about water-resource regulations, central
theory concepts, health exercises, zodiac compatibility, the Gongsun family,
web fiction, campus romance, historical geography, cooking recipes, and
pre-modern biography. The positive documents are long Chinese articles
containing the paragraph that generated the query.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.7030, hit@10 = 0.7950, and recall@100 = 0.9000. BM25 is
the strongest observed top-rank profile. Short Chinese questions often retain
distinctive names, titles, topic phrases, or domain terms that can anchor the
correct article.

This is a strong lexical signal, especially when the query includes a rare
entity or exact phrase. The difficulty is that Chinese questions are short and
documents are long, so many articles can share overlapping titles, genre terms,
or broad topic vocabulary.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.3392, hit@10 = 0.4450, and recall@100 = 0.6300.
Dense retrieval is much weaker than BM25 on this split.

This gap suggests that broad embedding similarity is not enough for short-query
Chinese long-document retrieval. A dense model may retrieve articles about the
same genre, historical period, regulation, health topic, or cultural concept
while missing the exact paragraph-containing document.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with 21 queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.4933, hit@10 = 0.6250, and recall@100 = 0.8950. Hybrid retrieval improves
substantially over dense retrieval and nearly matches BM25 recall@100, but it
still trails BM25 by a large margin at the top ranks.

This makes `reranking_hybrid` useful as a candidate pool for reranking, not as
a final ranking replacement for BM25. It keeps most positives available, but
the rank order still needs strong lexical and paragraph-aware evidence.

### Metric Interpretation for Model Researchers

This task is single-positive: each query has exactly one relevant long
document. Hit@10 measures whether that document appears near the top. nDCG@10
is sensitive to the exact rank of the positive, and recall@100 measures whether
the positive remains available to a downstream reranker.

The Chinese split is a short-query, long-document task with strong lexical
anchors. Dense retrieval should be interpreted against BM25, because BM25
captures exact names and phrases that appear to be central to the task. Hybrid
systems should focus on converting BM25-like coverage into better top-rank
ordering.

### Query and Relevance Type Tendencies

Queries are short Chinese paragraph-grounded questions about regulation,
finance-like theory, health, astrology, biography, fiction, geography, recipes,
history, and cultural topics. They often contain a compact title, person name,
concept, or phrase that identifies the source paragraph.

Relevant documents are long Chinese articles from Wikipedia or Wudao-style
sources. The answer-bearing paragraph may be surrounded by unrelated sections,
lists, or copied web-style context. Good retrieval needs exact phrase matching
and enough semantic robustness to handle short paraphrases.

### Representative Failure Modes

Dense retrieval can return a topically close Chinese article that lacks the
answer paragraph. This is likely when many documents share genre labels,
historical names, health terminology, or regulatory vocabulary. BM25 can fail
when short queries contain common terms or when several long articles share the
same title-like phrase.

Hybrid retrieval can preserve the positive in the candidate pool while ranking
a lexically or semantically adjacent article above it. Rerankers should inspect
the answer-bearing paragraph rather than relying only on the article title or a
global document vector.

### Training Data That May Help

Useful training data includes Chinese long-document QA retrieval pairs, Chinese
Wikipedia and Wudao article retrieval, multilingual MLDR training data outside
this Nano split, and title-sharing Chinese hard negatives. Training should
include short questions whose full-article positive is determined by one local
paragraph.

Synthetic data can help when it samples paragraphs from long Chinese
Wikipedia-like or Wudao-style articles, generates short grounded Chinese
questions, and uses the full article as the positive. Negatives should share
named entities, titles, genre terms, or topic labels while omitting the answer
paragraph.

### Model Improvement Notes

Dense retrievers should consider chunked indexing, late interaction,
paragraph-aware pooling, or multi-vector document representations. Sparse
systems should preserve Chinese lexical anchors and robust segmentation for
short questions. Rerankers should be trained on title-sharing and same-topic
Chinese hard negatives.

For hybrid systems, `NanoMLDR / zh` is a test of whether dense candidates can
supplement BM25 without degrading lexical precision. The current
`reranking_hybrid` profile nearly matches BM25 recall but needs better
top-rank ordering.

## Example Data

| Query | Positive document |
| --- | --- |
| 《条例》中对于水资源管理的具体措施有哪些？ [21 chars] | 湖北省抗旱条例 湖北是千湖之省，然而，受制于气象、资源、工程、发展等四大缺水矛盾，湖北一直存在着缺水之忧。据统计，新中国建立以来的64年间，湖北平均4年发生一次大范围的严重以上程度的干旱，中轻度旱每年都会在局部或全省发生，其中鄂北等地更是十年九旱。近十年来，湖北的干旱核心逐步向鄂中丘陵区蔓延，形成十堰、襄阳、随州、孝感、荆门等市为主的干旱带，且有逐年扩大的趋势。抗旱急需依法规范，因此，《湖北省抗旱条例》的出台是势在必行。据悉，该条例共19条，对抗旱工作的政府责任、市场机制、经费保障、规划预案、水资源管理、节水措施、抗旱服务组织等内容作了明确规定 。条例规定，抗旱工作应优先保障城乡居民生活用水，发生严重干旱或者特大干旱时，县级以上人民政府可以压减生产供水指标、限制或暂停高耗水行业用水，以保障基本生活用水。此外，该条例还专门针对水环境保护以及水资源管理出台了一系列措施，包括建立和实行用水总量控制、用水效率控制、水功能区限制纳污等制度，以最严格的约束机制，保证水资源的合理开发利用。条例明确规定，政府应将建设节水措施、污水处理设施、再生水利用设施纳入城乡规划，以防治水环境恶化造成的水质性缺水和资源枯竭；当发生严重干旱或特大干旱时，政府可限制或者暂停排放工业污水。条例全文 [2] （2014年1月9日湖北省第十二届人民代表大会常务委员会第7次会议通过） 第一条 根据《中华人民共和国水法》、《中华人民共和国抗旱条例》等有关法律、行政法规，结合本省实际，制定本条例。 第二条 抗旱工作优先保障城乡居民生活用水，统筹协调农业、工业用水，兼顾生态用水。建立政府主导与市场引导相结合、开源与节流相结合、优化水资源配置与调整产业结构相结合、经济效益与社会效益相结合的抗旱长效机制。 第三条 抗旱工作实行各级人民政府行政首长负责制，统一指挥、部门协作、分级负责、社会参与。 县级以上人民政府应当将干旱灾害预防和抗旱减灾工作纳入国民经济和社会发展规划，加强干旱灾害预防和抗旱减灾基础设施建设，完善抗旱工程体系、指挥调度体系和服务体系。乡镇人民政府、街道办事处负责本行政区域内干旱灾害预防和抗旱减灾的组织协调工作，明确相应机构或者人员，承担旱情收集、监测、分析、上报和灾情统计核实、抗灾救灾物资发放等具体工作。 县级以上防汛抗旱指挥机构在上级防汛抗旱指挥机构和本级人民政府的领导下，负责组织、指挥本行政区域内... [1,000 / 15,116 chars] |
| 什么是中枢理论的核心概念？ [13 chars] | [转载]中枢扩张、扩展 原文地址:中枢扩张、扩展作者:覃迪 大家有关于中枢扩张和中枢扩展的异同点,以及两者之间疑问、想法、建议,对这两者进行详细的区分并且以此为中心向上和向下延伸细化。 中枢扩张和中枢扩展的前生后世能全面透彻的理解掌握后,对缠论的理解会更进一步常见谬误: 1、认为扩张等同扩展！ 2、扩张后,走出了不可扩展,就说没有扩张或不属扩张范畴。缠中说禅走势中枢: 某级别走势类型中,被至少三个连续次级别走势类型所重叠的部分。 这里有一个递归的问题,就是这次级别不能无限下去,在实际之中,对最后不能分解的级别,其缠中说禅走势中枢定义为至少三个该级别单位k线重叠部分。一般来说,对实际操作,都把这最低的不可分解级别设定为1分钟或5分钟线。具体的计算以前三个、连续、次级别的、重叠为准。 注意,次级别的前三个走势类型都是完成的才构成该级别的缠中说禅走势中枢,完成的走势类型,在次级别图上是很明显的,根本就不用着再看次级别下面级别的图了。中枢的形成、中枢的区间: 中枢的形成无非两种,一种是回升形成的,一种是回调形成的。 在中枢的形成与延伸中,由与中枢形成方向一致的次级别走势类型的区间重叠确定。例如,回升形成的中枢,由向上的次级别走势类型的区间重叠确定。这些与中枢方向一致的次级别走势类型称为z走势段。相应的高、低点分别记为gn、dn,定义四个指标,gg=max(gn),g=min(gn),d=max(dn),dd=min(dn),n遍历中枢中所有zn。再定义zg= min(g1、g2),zd=max(d1、d2),显然,[zd,zg]就是缠中说禅走势中枢的区间。中枢方向: 中枢形成的三段的方向是怎么开始的,不是随便三段就是的。如果是向上的走势,里面的中枢一定是下-上-下的,向下的相反。 向上走势的典型中枢方向为3段连续重叠的次级走势构成的"下上下"类型；向下走势的中枢方向典型为3段连续重叠的次级走势构成的"上下上"类型；如果某级别走势仅仅由3段次级别走势构成,那么第2个次级别走势段的走势方向为该走势的中枢方向。如果某级别走势由至少5段次级别走势构成,并且任意n与n+2(n为非0偶数)段次级别走势不能重叠,那么该走势的中枢方向为偶数段次级别的走势方向。 例如上图中,假设每段为一线段,那么a-b、b-c、c-d、d-e分别为4个1f级别的走势,其中向上1f走势a-b和c-d的中枢方向... [1,000 / 10,712 chars] |
| 练习「抱住健康」法时，如何通过调动穴位和经络来实现养身和养心的效果？ [34 chars] | [转载]养生,就是养阳气;阳气旺盛,百病不侵 原文地址:养生,就是养阳气；阳气旺盛,百病不侵作者:夏一文心灵禅语 1、人要活到多少岁才算尽其天年 为何现代人的平均寿命才七八十岁,而且大多是死于疾病！为什么今人比古人所预期的天年寿命减少了将近三分之一呢？是谁偷走了这四五十年的宝贵生命呢？ 在长期从医经历中,我面对的病人是各种各样的,我经常会问他们一个问题:「你想活到多大岁数？」令我惊讶的是,很多人都说没有仔细想过这个问题。 生命的长短与质量好坏是我们一生中最大的事情,如果你对它关心不够,那人生还有多少快乐可言呢？ 我们的确应该为自己的健康长寿早作准备了,这个准备工作花不了您多少时间和金钱,但换来的却是高质量的生命。 高质量的生命就是活到「天年」。那么多大岁数才能称为「天年」呢？《黄帝内经》说:「上古之人,春秋皆度百岁乃去,而尽终其天年」。早在几千年前,充满智慧的中国人就能按照自然界的运行规律来推演人的一生了。 美国学者海尔弗里根据细胞分裂次数来推算人的寿命,得出的结论是人的寿命应该为120岁。这些研究结果,与我们祖先对天年寿数的记载惊人地一致。但是,为何现代人的平均寿命才七八十岁,而且大多是死于疾病！为什么今人比古人所预期的天年寿命减少了将近三分之一呢？这是值得每个人深思的问题。 是什么导致我们生病,是谁偷走了我们四五十年的阳寿呢？ 当然是阴气！ 阴气是我们自己造成的。我们经常人为地伤害自己的阳气,助长自己的阴气,以至于半百而衰,不能终其天年。这一点,我们的先人早在几千年前就帮我们指出来了。《黄帝内经·上古天真论》中说,不善养生的人喝酒就像喝饮料那样没有节制。喝酒喝多了以后,既伤人的精神,又伤人的脏腑和血脉。还有,常常把有害身心健康的生活方式当成正常的,深陷各种健康误区而浑然不觉。比如,醉酒之后入房纵欲,伤于酒又劳于色,只贪图一时的欢欣,而肆意地纵欲妄泄,不知道保持自身的精气。另外像熬夜、暴饮暴食、生活起居没有规律等等诸多不健康的生活方式,都能导致人们半百而早衰,疾病缠身而不能终其天年！ 有人说:「现在人的平均寿命比过去长了,活到八九十岁的老人比比皆是。」但我想:这些长寿老人,他们年轻的时候,生活与现在是不相同的。如今这些整天劳心劳身的人们,他们的身体真的是不容乐观。比如高血压、糖尿病、肩周炎、血管硬化等病,已过早地在这群三四十岁的人士身上出现了。 我是一个完美主义者... [1,000 / 9,944 chars] |

### Public Sources

- [M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation](https://arxiv.org/abs/2402.03216),
  2024.
- [M3-Embedding ACL Anthology version](https://aclanthology.org/2024.findings-acl.137/),
  2024.
- [Shitao/MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR).
- [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation | 2024 | benchmark paper | [https://arxiv.org/abs/2402.03216](https://arxiv.org/abs/2402.03216) |
| M3-Embedding ACL Anthology version | 2024 | paper | [https://aclanthology.org/2024.findings-acl.137/](https://aclanthology.org/2024.findings-acl.137/) |
| MLDR: Multilingual Long-Document Retrieval dataset | 2024 | dataset card | [https://huggingface.co/datasets/Shitao/MLDR](https://huggingface.co/datasets/Shitao/MLDR) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A Chinese question about measures in a water-resource regulation. | A long article about a provincial drought-resistance regulation. |
| A question about the core concept of a central theory. | A long Chinese article about central expansion concepts. |
| A question about health exercises, acupoints, and meridians. | A long Chinese article about health preservation. |
| A question about Gemini and Pisces relationship traits. | A long article about water-sign astrology. |
| A question about the first appearance of the Gongsun clan. | A long article about a late Han figure. |
