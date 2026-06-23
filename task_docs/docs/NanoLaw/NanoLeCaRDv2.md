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
| 张红、孙XX盗窃一案一审刑事判决书黑龙江省齐齐哈尔市龙沙区人民法院刑事判决书（2015）龙刑初字第351号：齐齐哈尔市龙沙区人民检察院以齐龙检公诉刑诉（2015）266号起诉书指控被告人张红、孙ＸＸ犯盗窃罪，于2015年10月22日向本院提起公诉，本院于同日立案受理。立案受理后，依法组成合议庭于2015年11月6日公开开庭进行了审理。齐齐哈尔市龙沙区人民检察院指派检察员李恩珠出庭支持公诉，被告人张红、孙ＸＸ及辩护人卜华林、李玲玲到庭参加诉讼。现已审理终结齐齐哈尔市龙沙区人民检察院指控：2011年1月初，齐齐哈尔市龙沙区鑫北疆洗浴中心原经营者被告人张红为少交水费，找到水务集团机械修造厂职工被告人孙ＸＸ，让其帮助调慢洗浴中心自来水表，节省水费。孙ＸＸ自带工具到鑫北疆洗浴中心锅炉房内，打开水表铅封，人为调紧顶针，致使水表指针转速变慢，达到窃水目的。此后张红多次找到孙ＸＸ人为调慢水表10余次，每次支付孙ＸＸ人民币200元左右的报酬或请其吃饭。在张红经营期间，实际窃水33个月，共计3960立方米，价值人民币28116元。案发后张红将盗窃水费全部补交至齐齐哈尔市自来水公司。公诉机关以相应证据证实上... [500 / 1,965 chars] | 马金成盗窃一审刑事判决书黑龙江省齐齐哈尔市龙沙区人民法院刑事判决书（2018）黑0202刑初51号：1981年11月20日出生于黑龙江省绥化市，汉族,小学文化，无职业，无固定住址，户籍所在地黑龙江省绥化市北林区兴福乡民权村5组66号。2000年因犯盗窃罪被黑龙江省绥化市北林区人民法院判处有期徒刑二年，2002年因犯盗窃罪被黑龙江省北安市人民法院判处有期徒刑二年，2005年因犯盗窃罪被黑龙江省宾县人民法院判处有期徒刑二年，2012年因犯盗窃罪被吉林市丰满区人民法院判处有期徒刑三年，2015年11月12日因犯盗窃罪被黑龙江省尚志市人民法院判处有期徒刑二年，2017年6月16日刑满释放。因涉嫌犯盗窃罪于2017年9月12日被刑事拘留，同年10月13日被逮捕。现羁押于齐齐哈尔市看守所。齐齐哈尔市龙沙区人民检察院以齐龙检公诉刑诉〔2018〕16号起诉书指控被告人马金成犯盗窃罪，于2018年2月6日向本院提起公诉。本院于同日立案，立案受理后，依法适用简易程序，组成合议庭，于2018年3月13日公开开庭进行了审理，齐齐哈尔市龙沙区人民检察院指派检察员周薇出庭支持公诉，被告人马金成到庭参加诉讼。现已审理终结齐齐哈尔市龙沙区人民检察院指控，1.2017年9月3日1时许，被告人马金成在齐齐哈尔市克东县顺达洗浴趁被害人孙某不备，窃取其ＯＰＰＯ牌Ａ59型手机一部，价值人民币950元。2.2017年9月3日4时许，被告人马金成在北安市海龙湾洗浴趁被害人王某1不备，窃取其ＶＩＶＯＸ牌ＰＬＡＹ5手机一部，价值人民币1500元。3.2017年9月4日3时许，被告人马金成在齐齐哈尔市拜泉县熙秀澜湾洗浴趁被害人任某不备，窃取其ＯＰＰＯＲ牌Ｒ9ｓＰＬＵＳ手机一部，价值人民币1800元。4.2017年9月4日4时许，被告人马金成在齐齐哈尔市拜泉县熙秀澜湾洗浴趁被害人李某1不备，窃取其ＯＰＰＯＲ牌Ｒ9ｓ手机一部，价值人民币1500元。5.2017年9月4日6时许，被告人马金成在齐齐哈尔市克山县鹏程洗浴趁被害人鲍某不备，窃取其三星牌Ｗ2016型手机一部，价值人民币3400元。6.2017年9月5日3时许，被告人马金成在齐齐哈尔市龙沙区海浪湾洗浴趁被害人范某不备，窃取其ＯＰＰＯ牌Ａ59ｍ手机一部，价值人民币950元，案发后手机已追缴返还给被害人。7.2017年9月5日4时许，被告人马金成在齐齐哈尔市龙沙区聚阳春... [1,000 / 4,616 chars] |
| 胡某某伪造国家机关公文、印章罪、伪造事业单位印章罪刑事一审判决书德阳市旌阳区人民法院刑事判决书（2017）川0603刑初341号：德阳市旌阳区人民检察院以旌检公刑诉（2017）313号起诉书指控被告人胡某某犯诈骗罪，于2017年7月20日向本院提起公诉。本院受理后依法组成合议庭，公开开庭审理了本案。德阳市旌阳区人民检察院指派检察员郑世鹏出庭支持公诉，被害人龙某某、被告人胡某某到庭参加诉讼。审理期间检察机关申请延期审理一次，现已审理终结德阳市旌阳区人民检察院起诉指控，2014年3月，被告人胡某某通过网络征婚平台结识被害人龙某某，为与龙某某确认恋爱关系，胡某某谎称其为成都市火车北站管理委员会公务员。在与龙某某确立恋爱关系后，胡某某长期以单位没有发工资、生病及为龙某某调动工作等借口向其索要钱财，金额共计27800元人民币。为达到长期骗取的目的，胡某某编造了其在成都市多个政府部门任职的履历，并向龙某某表示自己一路升迁，陆续任“成都市金牛区黄忠街道主任”“成都市金牛区综合治理委员会副主任”“成都市纪律委员会副主任”等领导职务。在被害人龙某某对其身份提出质疑后，胡某某伪造了“成都市金牛区社会治安综... [500 / 1,825 chars] | 吴某诈骗罪一审刑事判决书河北省海兴县人民法院刑事判决书（2014）海刑初字第91号：河北省海兴县人民检察院以海检公诉刑诉（2014）94号起诉书指控被告人吴某犯诈骗罪，于2014年10月29日向本院提起公诉。本院依法适用简易程序，实行独任审判，公开开庭审理了本案。海兴县人民检察院指派代理检察员相东明出庭支持公诉，被告人吴某到庭参加诉讼。现已审理终结海兴县人民检察院指控，2013年6月份至2014年8月份，被告人吴某通过网络聊天认识被害人黄某，吴某谎称自己叫王丽娜，25岁，未婚，是海兴县医院护士，并向黄某发送网上下载的非本人照片，假意与黄发展成为恋爱关系，后编造各种理由，先后骗取黄现金10945元，戒指一枚价值806元（已扣押发还），平板电脑一台价值3350元（已扣押发还），用于自己日常消费和使用。另查明，被告人吴某亲属将所骗现金退赔给被害人黄某。上述事实，被告人在开庭审理过程中亦无异议，并有被害人的陈述、价格鉴证结论书、银行卡明细，被告人结婚证，抓获经过一份，扣押、发还物品清单等证据予以证明，已经当庭举证、质证，足以认定本院认为，被告人吴某以非法占有为目的，骗取他人钱物共计价值15101元，数额较大，其行为已触犯了《中华人民共和国刑法》第二百六十六条之规定，构成诈骗罪。公诉机关指控犯罪事实清楚，证据确实、充分，指控罪名成立。被告人吴某认罪、并积极退赃，依法可从轻处罚。公诉机关提出的以上量刑情节，本院予以采纳。依照《中华人民共和国刑法》第二百六十六条、第五十二条、第五十三条、第七十二条之规定，判决如下被告人吴某犯诈骗罪，判处有期徒刑八个月，缓刑一年，并处罚金10000元。（已缴纳）（缓刑考验期自判决确定之日起计算）如不服本判决，可在接到判决书的第二日起十日内通过本院或直接向河北省沧州市中级人民法院提出上诉。书面上诉的，应提交上诉状正本一份，副本一份审判员刘国宏二〇一四年十一月五日书记员张健敏 海兴县人民检察院指控，2013年6月份至2014年8月份，被告人吴某通过网络聊天认识被害人黄某，吴某谎称自己叫王丽娜，25岁，未婚，是海兴县医院护士，并向黄某发送网上下载的非本人照片，假意与黄发展成为恋爱关系，后编造各种理由，先后骗取黄现金10945元，戒指一枚价值806元（已扣押发还），平板电脑一台价值3350元（已扣押发还），用于自己日常消费和使用。另查明，被告人吴某亲属将所... [1,000 / 1,201 chars] |
| 录俊荣何某某非法吸收公众存款一审刑事判决书广东省珠海市香洲区人民法院刑事判决书（2014）珠香法刑初字第2800号：珠海市香洲区人民检察院以珠香检公诉刑诉（2014）2881号起诉书指控被告人何俊荣何某某犯非法吸收公众存款罪，于2014年12月19日向本院提起公诉。本院依法组成合议庭，公开开庭审理了本案。珠海市香洲区人民检察院指派检察员谢谦、黄斌权出庭支持公诉，被告人何俊荣何某某及其辩护人郭俊德、吴文仪、证人曾某、黄某1、吴某1、何某1到庭参加诉讼。现已审理终结公诉机关指控，2010年5月至2013年10月间，被告人何俊荣何某某以其公司投资水利工程及多项高科技项目，向何某2、吴某2、匡某、丁某等人宣传公司业绩，承诺借款有高额利息，且未经有关部门批准，非法吸收何某2、何某4、吴某2、匡某、丁某、钟某等人的资金。经查，被告人何俊荣何某某共非法吸收何某2及其亲友何某4等人的资金共计人民币1147.55万（以下币种均为人民币）元；非法吸收吴某2及匡某、丁某、谢某、钟某等人的资金共计人民币416.75万元。2014年6月12日，被告人何俊荣何某某被抓获归案。针对以上事实，公诉人当庭出示了被告人何... [500 / 24,088 chars] | 圱俊、朱伟等非法吸收公众存款一审刑事判决书上海市普陀区人民法院刑事判决书（2017）沪0107刑初1130号：上海市普陀区人民检察院以沪普检金融刑诉［2017］56号、沪普检金融刑变诉［2018］1起诉书指控被告人朱俊、朱伟、卞海翔、赵泽亚、袁永明、陈荑、许志梅、火东雯、薛荣新、王勤、唐丽娜犯非法吸收公众存款罪，于2017年11月15日向本院提起公诉。本院依法组成合议庭，公开开庭审理了本案。上海市普陀区人民检察院指派检察员戈某出庭支持公诉。被告人朱俊及辩护人卢作寅，被告人朱伟及辩护人张保强，被告人卞海翔及辩护人党曙华，被告人赵泽亚及辩护人陆宇艇，被告人袁永明及本院通过上海市普陀区法律援助中心指派的辩护人贾庆，被告人陈荑及辩护人张晓维、苏轶，被告人许志梅及辩护人杨扬，被告人火东雯及辩护人刘津华，被告人薛荣新，被告人王勤及辩护人张斌，被告人唐丽娜及辩护人龚祖益到庭参加诉讼。现已审理终结上海市普陀区人民检察院指控，2013年7月起，被告人朱俊、朱伟注册成立上海聚煌金融信息服务有限公司（以下简称“聚煌公司”），公司经营地址为本市普陀区西康路ＸＸＸ号普陀科技大厦15楼，由被告人朱俊担任实际负责人，被告人朱伟担任公司法定代表人。公司成立后招募被告人卞海翔担任该公司理财部总监、副总经理，被告人赵泽亚、袁永明、陈荑等担任该公司理财分部总监，被告人许志梅、火东雯、薛荣新、王勤等担任该公司理财团队长，被告人唐丽娜等担任该公司业务员。该公司通过举办宣传酒会、发放广告传单等方式，以高额利息为诱，与投资人签订《信用评估与管理服务协议》，向不特定社会公众销售期限为1-18个月不等的“满月金”、“双月赢”、“季季丰”等理财产品。2015年12月起，该公司资金链断裂，无法兑付投资人本息。经上海司法会计中心鉴定，2013年7月至2016年1月，“聚煌公司”共计与严兴兰、蔡文珠等503名投资人签订投资理财协议，非法吸收公众存款人民币11800余万元。其中被告人卞海翔团队与投资人签订协议款为人民币10300余万元；被告人赵泽亚团队与投资人签订协议款为人民币1800余万元；被告人袁永明团队与投资人签订协议款为人民币4100余万元；被告人陈荑团队与投资人签订协议款为人民币3400余万元；被告人许志梅团队与投资人签订协议款为人民币800余万元；被告人火东雯团队与投资人签订协议款为人民币1100余万元；被告人薛... [1,000 / 10,804 chars] |

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
