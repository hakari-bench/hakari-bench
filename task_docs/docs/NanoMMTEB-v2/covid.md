# NanoMMTEB-v2 / covid

## Overview

`NanoMMTEB-v2 / covid` is a Chinese COVID-19 passage-retrieval task from the
Multi-CPR family. Queries are concise Chinese information needs about pandemic
response, public services, factory reopening, local policies, and government
notices. The Nano split has 200 queries, 10,000 documents, and 204 positive
qrel rows. Most queries have one positive, with two multi-positive queries.
Current diagnostics show BM25 and `reranking_hybrid` as nearly tied on nDCG@10,
`reranking_hybrid` as strongest on hit@10 and recall@100, and dense retrieval
as close but slightly weaker.

## Details

### What the Original Data Measures

Multi-CPR introduced multi-domain Chinese passage retrieval datasets from real
search and human relevance annotation. The COVID retrieval split is a Chinese
news and policy retrieval task: a short user question must retrieve the article
passage that answers it.

The task measures fact-focused Chinese retrieval over pandemic-era public
information. Relevant passages often contain dates, locations, agencies,
measures, hotline numbers, service rules, reopening conditions, or operational
statistics.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 204 positive qrel
rows. Most queries have one positive; two queries have multiple positives. The
average positives per query is 1.02, with a maximum of 4. Queries average 25.74
characters, while documents average 409.35 characters.

Observed examples include questions about Beijing measures for small
businesses, Jiangsu medical teams sent to Hubei, online teaching in Wuzhou,
guidance for older adults and chronic-disease patients, and Ministry of
Transport accountability rules.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.7888, hit@10 = 0.8750, and recall@100 = 0.9608. BM25 is a
very strong profile for this task.

The strength comes from short Chinese queries that often include distinctive
locations, agencies, policy terms, dates, or measured quantities. Term-frequency
matching can directly connect a question to the passage containing the requested
fact. BM25 may still fail when related notices share the same locality or
agency but answer a different operational question.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.7592, hit@10 = 0.8600, and recall@100 = 0.9363.
Dense retrieval is close to BM25 but slightly weaker across the main metrics.

This suggests that embedding similarity captures the public-health and policy
semantics well, but exact factual anchors still matter. A dense model may find
passages about the same city, service category, or pandemic measure while
missing the exact notice that contains the answer.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with two queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.7873, hit@10 = 0.8900, and recall@100 = 0.9902. Hybrid retrieval has the best
hit@10 and recall@100 and is nearly tied with BM25 on nDCG@10.

This is a balanced hybrid-search case. Sparse matching contributes strong
factual anchors, while dense retrieval helps recover paraphrased policy or
service expressions. The remaining nDCG difference is small, so rerankers can
focus on distinguishing near-identical notices.

### Metric Interpretation for Model Researchers

This task is almost single-positive, but a small number of queries have
multiple positives. Hit@10 measures whether at least one answer passage appears
near the top. nDCG@10 rewards ranking relevant passages early, and recall@100
measures whether positives remain available for reranking.

Because the documents are short and fact-focused, high lexical scores are
meaningful. A good model should preserve exact Chinese names, dates, agencies,
and quantities while still handling paraphrased public-policy questions.

### Query and Relevance Type Tendencies

Queries are short Chinese questions targeting explicit facts in news or
government notice passages. They often ask how many measures were issued, when
a team departed, how an activity was executed, what a patient should do, or
which class of people is subject to accountability.

Relevant passages are Chinese news or policy snippets with concrete facts.
They may share locality and pandemic vocabulary with many other passages, so
fine-grained factual matching is important.

### Representative Failure Modes

BM25 can over-rank a passage from the right locality or agency that answers a
different question. Dense retrieval can retrieve a semantically related
COVID-era passage but miss the precise date, number, service rule, or targeted
population. Hybrid retrieval can still confuse near-duplicate policy notices.

Rerankers should compare the requested fact type against the passage, including
date, count, agency, service process, and affected group.

### Training Data That May Help

Useful training data includes Chinese passage retrieval data, Chinese news QA
pairs, COVID-era policy and public-service retrieval data, and hard negatives
matched by locality, agency, date, or service domain. The Nano split's queries,
qrels, and positive passages should be excluded from training.

Synthetic data can generate Chinese news and government notices with explicit
dates, agencies, services, rates, and quantities. Questions should target one
explicit fact. Negatives should come from the same public-health scenario while
answering a different operational question.

### Model Improvement Notes

Sparse systems should preserve Chinese lexical anchors and handle short-query
segmentation. Dense retrievers should strengthen fine-grained factual
distinctions within the same policy domain. Rerankers should score answer
support, not only topical match.

For hybrid systems, `NanoMMTEB-v2 / covid` is a strong example of hybrid search
working well: `reranking_hybrid` improves recall@100 and hit@10 while retaining
BM25-level nDCG@10. The main remaining challenge is ordering very similar
public-notice passages.

## Example Data

| Query | Positive document |
| --- | --- |
| 北京市出台多少条措施帮助中小微企业应对疫情影响？ [24 chars] | 助力中小微企业度难关这些地方减租了抗疫战斗仍在继续，北京市发文出台16条措施帮助中小微企业应对疫情影响，其中房租减免措施备受关注，中关村各空间载体将如何落实该项措施？截至目前，中关村分园、特色产业园区纷纷推出减租措施，汇龙森、翠湖科创平台、中关村意谷等68家孵化器提出对房租进行减免，已推出的减免方案基本参照现行政策，减免租金15至30天。一起来看看它们的落实细则。亦庄园：2月房租最高减免100%中小微企业承租区内国有企业房产从事经营活动，按照政府要求坚持营业或依照防疫规定关闭停业且不裁员、少裁员的，免收2月份房租；承租用于办公用房的，给予2月份租金50%的减免。鼓励产业园区、商务楼宇等单位为科技型中小微企业减免租金，具体由双方协商解决，给予一定资金补贴。中关村创业大街：2月房租减免50%2月6日，中关村创业大街出台房屋租金（含物业费）减免方案。对于受到疫情影响的科技型中小微企业和创业服务机构，中关村创业大街给予2月份租金50%的减免。此次减免惠及入驻街区的近百家机构及创业团队，缓解了疫情对企业造成的经营冲击。汇龙森科技园：2月房租最高减免100%1.在汇龙森产权范围内承租产业用房的中小微企业（需注册及纳税），给予2020年2月份房屋租金50%的减免。2.在防疫期间为国家防疫工作做出突出贡献的园区中小微企业，给予2020年2月份房屋租金100%的减免。3.在防疫期间为国家防疫工作做出突出贡献的园区中小微企业，暂时经营困难的，除给予2020年2月份房屋租金100%全免外，给予防疫後续期间全部房屋租金50%的减免。锋创科技园：2月房租减免50%面对汹涌疫情，锋创科技园将对在园区内承租办公用房及商业的中小微企业（在北京经济技术开发区科创十三街18号院完成工商注册和属地纳税），给予2020年2月份租金50%减免。这是锋创科技园在疫情期间，继赠送消毒液、推行分时分批就餐、安装消毒帐篷、设立观察点等之後的又一举措，携手企业共抗疫情。博奥共享平台：最高减免1个月房租1.军腾博奥基地将为入驻企业减免1个月租金，为园区企业分担损失。此措施惠及45家企业，预计减免金额达118.62万元。2.按照此前合同约定，金信博奥基地部分企业2020年度租金将递增5%。疫情发生後，金信博奥基地向入驻企业承诺，2020年度房租不递增，维持不变，同时为企业提供的财税等服务减免50%收费，与企业共度难关。首... [1,000 / 1,481 chars] |
| 江苏援湖北第一批医疗队是什么时间？ [17 chars] | ——“散装江苏”星夜集结驰援湖北新华社南京2月12日电题：“必须打赢这场仗！”——“散装江苏”星夜集结驰援湖北新华社记者沈汝发、邱冰清11日，江苏支援黄石医疗队310人出发，开赴抗击新冠肺炎疫情战场。从1月25日首批江苏援湖北医疗队出发，到2月11日江苏支援黄石医疗队出发，被网友戏称为“散装”的江苏，截至目前已派出7批医疗队共计1792人赴湖北省参与医疗救治和疫情防控工作。“我做了30多年医生，作为一个老同志，未来跟大家一起并肩战斗！”江苏援黄石新冠肺炎防治前方指挥部总指挥鲁翔在出征仪式现场，向医疗队队员们发出动员令，“我们没有退路，必须打赢这场仗！必须完成任务！必须安全回来！”10日下午5点半，接到医院通知，沛县人民医院重症监护室主管护师李娜果断报名。李娜在重症监护室工作了12年，“我比一般护理人员经验多一些，这个时候我必须上前线。”时间紧急，李娜来不及和父母告别。“要收拾行李，非常匆忙，另外老人肯定也会担心。”她说，“等安稳以后，再跟他们慢慢说。”和李娜一样，在医院发出征召令后，许多医护人员写下请战书，摁下红手印。医疗队集结了来自南京、徐州、常州等10个设区市的310位医护人员，包括103名医生、200名护士，还有4名公卫人员和3名行政人员。这支医疗队是江苏对口支援黄石的第一梯队。鲁翔说，医疗队将在摸清当地总体情况，以及复杂病例、危重病例等基本情况的基础上，抓紧做好救治、防控工作，有效救治危重病人，降低死亡率、感染率，提高治疗率、治愈率。“本次的传染性疾病，给救治工作带来了一定的难度。”江苏援黄石新冠肺炎防治前方指挥部医疗救治组（专家组）组长黄英姿说，江苏支援黄石医疗队制定了缜密的科学救治方案。“目前掌握的情况是当地病人比较多，尤其是危重病人较多。当地重症、呼吸、感染管理等医疗护理力量比较缺。”黄英姿说，江苏根据前方需求组建队伍，主要以重症医学科、呼吸科、感染管理科等为主力。鲁翔介绍说：“我们组队是根据对方提出的要求，在通知时具体到专业、职称等，各家医院抽调精兵强将，绝大部分医院选来的人比我们的要求还要高一个等级，可以说是‘高配’。”江苏援黄石新冠肺炎防治前方指挥部副总指挥吴红辉介绍，江苏的“高配”团队得益于在组织队伍时对人员、专业、年龄构成等的多层次考量。医疗队队员来自不同医院，每个队员身后有单位和专业背景支持，做到前后方衔接。“我们一定是召必应，也一定战必胜... [1,000 / 1,173 chars] |
| 梧州市教育局开展的线上教学活动是怎么执行的？ [22 chars] | 我市各中小学校继续延迟开学2月26日，自治区新冠肺炎疫情防控三级应急响应工作指导意见出台，意见提出，将继续延迟学校开学时间。对此，梧州市教育局在继续落实各中小学校开学前後防控责任和开展线上教学活动的同时，也利用安全教育平台做好学生的疫情防控安全教育，让学生在家安心学习。工作指导意见指出，各级各类学校，包括大中小学、幼儿园、中职学校、技工学校等继续延迟开学，具体开学时间将根据疫情防控形势科学评估後提前向社会公布。延迟开学期间，各级教育行政部门和各级各类学校要努力按照&ldquo;停课不停教不停学&rdquo;的要求，继续组织实施好在线教育教学。对此，梧州市教育局加强组织各校开展线上教学活动。在开展线上教学活动中，各中小学校通过在线直播教学、网络点播教学、班级QQ群或微信群发送课後作业，并通过网络或者电话等方式，对学生的学习和生活进行指导和检查。此外，市教育局学校安全稳定工作科利用安全教育平台进行宣传，让广大师生和家长加强对疫情的认知，更科学地掌握疫情防控知识。（朱元冬滕瑜） [442 chars] |

### Public Sources

- [Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval](https://arxiv.org/abs/2203.03367),
  2022.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595),
  2025.
- [mteb/CovidRetrieval](https://huggingface.co/datasets/mteb/CovidRetrieval).
- [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval | 2022 | task paper | [https://arxiv.org/abs/2203.03367](https://arxiv.org/abs/2203.03367) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| mteb/CovidRetrieval | 2024 | dataset card | [https://huggingface.co/datasets/mteb/CovidRetrieval](https://huggingface.co/datasets/mteb/CovidRetrieval) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A Chinese question asking how many measures Beijing issued for small businesses. | A passage about 16 measures and rent relief for small enterprises. |
| A question asking when the first Jiangsu medical team supported Hubei. | A passage about Jiangsu medical teams departing for Hubei. |
| A question about how Wuzhou online teaching was implemented. | A passage about delayed school opening and online teaching activity. |
| A question about what older adults and chronic-disease patients should do when symptomatic. | A public-health guidance passage for grassroots medical institutions. |
| A question about which people the Ministry of Transport would hold accountable. | A passage about strengthening COVID-19 prevention supervision. |
