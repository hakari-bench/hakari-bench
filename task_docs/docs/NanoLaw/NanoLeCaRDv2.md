# NanoLaw / NanoLeCaRDv2

## Overview

`NanoLaw / NanoLeCaRDv2` is a Chinese legal case retrieval task based on
LeCaRDv2. Queries and documents are Chinese criminal case records, and the
retrieval goal is to find legally related cases under a multi-aspect relevance
definition. The Nano split has 159 queries, 3,795 documents, and 3,896 positive
qrel rows. Every query has multiple positives, with more than 24 positives per
query on average. Current diagnostics show that `reranking_hybrid` is the
strongest observed profile across nDCG@10, hit@10, and recall@100. Dense
retrieval is also stronger than BM25, while BM25 remains a high-performing
lexical baseline because Chinese criminal judgments share charge names and
formulaic court language.

## Details

### What the Original Data Measures

LeCaRDv2 is introduced as a large-scale Chinese legal case retrieval dataset
created from millions of Chinese criminal case documents. The paper argues that
earlier Chinese legal retrieval datasets were limited by scale, candidate
pooling, and narrow relevance definitions. LeCaRDv2 broadens relevance to
include characterization, penalty, and procedure, and uses legal expert
annotation over candidate pools.

The MTEB task frames LeCaRDv2 as retrieving case documents most relevant to a
query scenario. In this Nano split, the query itself is a long criminal case
document or fact section, and relevant documents are related criminal cases.
The task is therefore a legal case similarity benchmark, not just a charge-name
lookup task.

### Observed Data Profile

The Nano split contains 159 queries, 3,795 documents, and 3,896 positive qrel
rows. Every query is multi-positive. Positives per query average 24.50, with a
minimum of 4, a median of 28, and a maximum of 30. Queries average 4,259.44
characters, while documents average 7,231.82 characters.

Representative cases involve theft, fraud, illegal absorption of public
deposits, picking quarrels and provoking trouble, robbery, production or sale
of counterfeit medicine, illegal fishing, gambling, and organized criminal
activity. Texts include court names, docket numbers, prosecution statements,
trial procedure, facts, reasoning, charges, and sentencing details. This makes
the benchmark a long-form legal similarity task with many relevant cases per
query.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.6528, hit@10 = 0.9497, and recall@100 = 0.7523. BM25 is
strong because criminal case documents repeat charge names, court formulas,
procedural language, and statutory vocabulary. If two cases involve the same
offence or similar court-language patterns, sparse retrieval can surface many
relevant candidates.

BM25 is nevertheless below dense retrieval and hybrid retrieval. The reason is
the relevance definition: relatedness is not only shared charge text. Cases may
be relevant because they align on characterization, penalty, procedure, or
material facts. A sparse model can over-rank cases that repeat the same offence
label while missing cases that are legally similar in sentencing pattern or
procedural posture.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.6940, hit@10 = 0.9560, and recall@100 = 0.8611.
Dense retrieval improves over BM25 across the main reported metrics. This
suggests that semantic case similarity and legal-fact representation are
important in LeCaRDv2, especially where relevant cases share factual patterns
or penalty considerations beyond exact charge names.

The dense gains are especially meaningful because documents are long and
multi-positive. A dense model can group cases by overall criminal conduct,
procedure, and sentencing context, not just by repeated words. Still, dense
retrieval must preserve exact legal labels and factual details; otherwise it
may retrieve broadly similar but legally mismatched cases.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 or 101 candidates per
query, with 1 safeguard positive row and a mean of 100.006289 candidates. It
achieves nDCG@10 = 0.7225, hit@10 = 0.9686, and recall@100 = 0.8619, making it
the strongest observed profile. The improvement over dense is moderate but
consistent, and the improvement over BM25 is clear.

This is a strong example of hybrid search matching the structure of a legal
retrieval task. BM25 contributes charge labels, statutory terms, court formulas,
and named procedural phrases. Dense retrieval contributes fact-pattern and
legal-similarity matching. The hybrid set combines these signals and provides
the best early ranking and candidate coverage among the three profiles.

### Metric Interpretation for Model Researchers

This task is heavily multi-positive. Hit@10 is high for all methods because
many queries have large relevant sets, so at least one relevant case is often
retrieved. nDCG@10 is more informative because it rewards ranking multiple
relevant cases high. Recall@100 measures how much of the large positive set is
available for later reranking.

The metric pattern indicates that `NanoLeCaRDv2` is not solved by sparse
charge matching alone. BM25 is strong, dense retrieval is stronger, and hybrid
retrieval is strongest. This makes the task useful for evaluating whether legal
retrieval systems combine exact offence vocabulary with semantic legal
similarity.

### Query and Relevance Type Tendencies

Queries are long Chinese criminal case records or fact sections. Relevant
documents are other criminal cases related by legal characterization, penalty,
procedure, or material facts. Relevance is therefore set-based and graded by
legal relatedness, not a single exact answer.

The task rewards models that can identify charge-level similarity, sentencing
patterns, procedural posture, defendant conduct, and legally material facts.
Because every query has many positives, a model should retrieve a diverse set
of related cases rather than only the closest lexical duplicate.

### Representative Failure Modes

BM25 can fail by overmatching charge names while ignoring differences in facts,
penalty, or procedure. Dense retrieval can fail by retrieving cases that are
generally similar but miss exact offence elements or procedural conditions.
Hybrid retrieval reduces both risks but can still rank highly formulaic court
documents above more legally relevant cases.

Long-document representation is another challenge. Court records contain
procedural headers, party information, facts, reasoning, and sentencing. A model
that overweights boilerplate may miss the factual or legal section that drives
relevance.

### Training Data That May Help

Useful training data includes Chinese legal case retrieval, criminal charge and
fact-section retrieval pairs, court-document similarity data, sentencing
similarity supervision, and same-charge hard negatives. Training should preserve
large positive sets per query because LeCaRDv2 relevance is multi-positive and
multi-aspect.

For comparable evaluation, training should exclude NanoLeCaRDv2 queries, qrels,
and relevant criminal case documents. Synthetic data can help when it generates
Chinese criminal judgments with facts, reasoning, and sentencing, and pairs
them with positives aligned on characterization, penalty, or procedure.

### Model Improvement Notes

Dense retrievers should learn legal-fact similarity and sentencing/procedure
alignment while preserving exact Chinese charge terms. Sparse systems benefit
from Chinese legal tokenization, charge phrase handling, and weighting of court
formulae versus material facts. Rerankers should compare the sections that
matter legally: alleged conduct, court findings, charge characterization,
penalty reasoning, and procedure.

For hybrid systems, `NanoLeCaRDv2` is a strong fit. Exact terms and semantic
legal similarity both matter, and the observed `reranking_hybrid` profile is
the best of the three candidate sets.

## Example Data

| Query | Positive document |
| --- | --- |
| 张红、孙XX盗窃一案一审刑事判决书黑龙江省齐齐哈尔市龙沙区人民法院刑事判决书（2015）龙刑初字第351号：齐齐哈尔市龙沙区人民检察院以齐龙检公诉刑诉（2015）266号起诉书指控被告人张红、孙ＸＸ犯... [100 / 1,965 chars] | 马金成盗窃一审刑事判决书黑龙江省齐齐哈尔市龙沙区人民法院刑事判决书（2018）黑0202刑初51号：1981年11月20日出生于黑龙江省绥化市，汉族,小学文化，无职业，无固定住址，户籍所在地黑龙江省绥化市北林区兴福乡民权村5组66号。2000年因犯盗窃罪被黑龙江省绥化市北林区人民法院判处有期徒刑二年，2002年因犯盗窃罪被黑龙江省北安市人民法院判处有期徒刑二年，2005年因犯盗窃罪被黑龙江省宾县人... [200 / 4,616 chars] |
| 胡某某伪造国家机关公文、印章罪、伪造事业单位印章罪刑事一审判决书德阳市旌阳区人民法院刑事判决书（2017）川0603刑初341号：德阳市旌阳区人民检察院以旌检公刑诉（2017）313号起诉书指控被告人... [100 / 1,825 chars] | 吴某诈骗罪一审刑事判决书河北省海兴县人民法院刑事判决书（2014）海刑初字第91号：河北省海兴县人民检察院以海检公诉刑诉（2014）94号起诉书指控被告人吴某犯诈骗罪，于2014年10月29日向本院提起公诉。本院依法适用简易程序，实行独任审判，公开开庭审理了本案。海兴县人民检察院指派代理检察员相东明出庭支持公诉，被告人吴某到庭参加诉讼。现已审理终结海兴县人民检察院指控，2013年6月份至2014年... [200 / 1,201 chars] |
| 录俊荣何某某非法吸收公众存款一审刑事判决书广东省珠海市香洲区人民法院刑事判决书（2014）珠香法刑初字第2800号：珠海市香洲区人民检察院以珠香检公诉刑诉（2014）2881号起诉书指控被告人何俊荣何... [100 / 24,088 chars] | 圱俊、朱伟等非法吸收公众存款一审刑事判决书上海市普陀区人民法院刑事判决书（2017）沪0107刑初1130号：上海市普陀区人民检察院以沪普检金融刑诉［2017］56号、沪普检金融刑变诉［2018］1起诉书指控被告人朱俊、朱伟、卞海翔、赵泽亚、袁永明、陈荑、许志梅、火东雯、薛荣新、王勤、唐丽娜犯非法吸收公众存款罪，于2017年11月15日向本院提起公诉。本院依法组成合议庭，公开开庭审理了本案。上海市... [200 / 10,804 chars] |
| 鵵某姚某某姚某寻衅滋事一审判决书安徽省萧县人民法院刑事判决书（2016）皖1322刑初10号：萧县人民检察院以萧检刑诉［2016］3号起诉书指控被告人赵某、姚某某、姚某犯寻衅滋事罪，于2016年1月5... [100 / 4,409 chars] | 姚天朗寻衅滋事罪一审刑事判决书四川省西充县人民法院刑事判决书（2019）川1325刑初79号：西充县人民检察院以南西检公诉刑诉（2019）51号起诉书指控被告人姚天朗涉嫌寻衅滋事罪、危险驾驶罪，于2019年5月27日向本院提起公诉，本院受理后，依法组成合议庭公开开庭审理了本案。西充县人民检察院指派检察员冯慧丽出庭支持公诉，被告人姚天朗到庭参加诉讼，本案现已审理终结公诉机关指控：被告人姚天朗在两年内... [200 / 3,594 chars] |
| 田雷、田涛抢劫、抢夺二审刑事判决书河北省高级人民法院刑事判决书（2018）冀刑终348号：河北省沧州市中级人民法院审理沧州市人民检察院指控原审被告人田雷、田涛、田家兴犯抢劫罪、抢夺罪，原审被告人王福华... [100 / 10,707 chars] | 林强、颜华抢劫罪一审刑事判决书广西壮族自治区合浦县人民法院刑事判决书（2019）桂0521刑初47号：合浦县人民检察院以合检公刑诉［2018］771号起诉书指控被告人颜华犯抢劫罪、抢夺罪、盗窃罪，被告人林强犯抢劫罪、抢夺罪于2019年1月4日向本院提起公诉,2019年8月2日向本院变更起诉。本院依法适用普通程序，组成合议庭，于2019年5月6日／2019年8月20日公开开庭审理了本案。合浦县人民检... [200 / 8,029 chars] |

### Public Sources

- [LeCaRDv2: A Large-Scale Chinese Legal Case Retrieval Dataset](https://arxiv.org/abs/2310.17609),
  2023.
- [THUIR LeCaRDv2 repository](https://github.com/THUIR/LeCaRDv2), source
  repository.
- [mteb/LeCaRDv2](https://huggingface.co/datasets/mteb/LeCaRDv2), MTEB source
  dataset.
- [hakari-bench/NanoLaw](https://huggingface.co/datasets/hakari-bench/NanoLaw),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| LeCaRDv2: A Large-Scale Chinese Legal Case Retrieval Dataset | 2023 | arXiv paper | [https://arxiv.org/abs/2310.17609](https://arxiv.org/abs/2310.17609) |
| THUIR LeCaRDv2 | 2023 | GitHub repository | [https://github.com/THUIR/LeCaRDv2](https://github.com/THUIR/LeCaRDv2) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A Chinese theft judgment with court, indictment, trial, facts, and sentencing details. | Another theft judgment with related criminal history, facts, or penalty reasoning. |
| A judgment involving fraud and forged official documents or seals. | A fraud judgment with related conduct and trial findings. |
| A long illegal-absorption-of-public-deposits case. | Another financial-crime judgment involving related public-deposit conduct and defendants. |
| A case about picking quarrels and provoking trouble. | A judgment involving similar public-order conduct and sentencing context. |
| A robbery or robbery-snatching appeal judgment. | A related criminal judgment involving robbery, snatching, or associated offence patterns. |
