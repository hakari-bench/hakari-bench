# NanoCMTEB / covid

## Overview

NanoCMTEB `covid` is a Chinese COVID-19 news and public-policy retrieval task. Queries are short fact-seeking questions about pandemic measures, dates, benefits, procedures, agencies, or local support policies. Documents are Chinese news or government-policy passages. The task measures whether a retriever can locate the passage containing the requested policy detail in a COVID-related information environment.

## Details

### What the Original Data Measures

The task belongs to the Chinese retrieval resources used in C-MTEB and is related to the Multi-CPR family of domain-specific Chinese passage retrieval datasets. The source setting is COVID-19 news and policy retrieval, where a user asks a concise question and the relevant passage contains the answer.

This differs from open-ended medical advice. The queries usually seek a specific administrative fact, such as how many measures were issued, when a medical team departed, what an agency required, or what a public-service notice instructs. Relevance depends on finding the passage with the exact policy or news detail.

### Observed Data Profile

The task contains 200 queries, 10,000 documents, and 204 relevance judgments. It is almost entirely single-positive: there are 1.02 positives per query on average, a minimum of 1, a median of 1.0, a maximum of 4, and only 2 multi-positive queries, or 1.00% of the set.

Queries average 25.73 Chinese characters. Documents average 409.35 characters and are often longer news or notice passages. Many contain local government names, dates, institutions, and procedural details.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.7888, hit@10 of 0.8750, and recall@100 of 0.9608 using the top-500 BM25 candidate subset. This is a strong lexical profile. COVID policy questions often repeat exact location names, agency names, dates, and policy terms that also appear in relevant passages.

BM25 can still fail when the query paraphrases the requested detail, when the answer is embedded in a long notice, or when several documents share similar pandemic vocabulary. But compared with medical consultation retrieval, exact term matching is highly effective here.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.7518, hit@10 of 0.8550, and recall@100 of 0.9314. Dense retrieval is strong but trails BM25 across all reported metrics. This suggests that exact lexical signals are especially important for short COVID policy questions.

Dense retrieval remains useful for paraphrased requests and semantically similar notices, but it can underweight exact administrative terms that uniquely identify the relevant passage. The task is therefore not purely semantic.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.7834, hit@10 of 0.8850, and recall@100 of 0.9902. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 2 safeguard rows, candidate counts from 100 to 101, and a mean of 100.01 candidates.

Hybrid retrieval has the best hit@10 and recall@100, while BM25 is slightly best for nDCG@10. The practical interpretation is that sparse matching provides the strongest ordering signal, and hybrid search broadens coverage enough to expose nearly all positives in the top 100.

### Metric Interpretation for Model Researchers

This task is BM25-favorable and hybrid-friendly. Exact Chinese terms, places, organizations, and dates carry much of the relevance signal. Dense retrieval is competitive but weaker than BM25 in top-rank ordering. Reranking_hybrid is the best candidate pool when recall@100 matters.

Researchers should treat this as short-query factual policy retrieval. A model should preserve entity and date precision, not only semantic similarity. High hit@10 is expected; small nDCG differences matter because most queries have only one positive.

### Query and Relevance Type Tendencies

Queries ask about Beijing measures for small businesses, Jiangsu medical teams aiding Hubei, Wuzhou online teaching arrangements, guidance for older adults and chronic disease patients, and accountability rules from transportation authorities. Positive documents are news reports, public notices, and policy summaries.

The relevance relation is answer containment. A positive passage should contain the exact requested policy detail, date, number, procedure, or administrative instruction.

### Representative Failure Modes

Likely failures include retrieving a notice from the same agency but the wrong date, matching a city name without answering the requested action, over-ranking broad COVID policy passages, and confusing similar local support policies.

BM25 is vulnerable to near-duplicate administrative wording. Dense retrieval can blur exact dates and organizations. Hybrid retrieval helps coverage but still requires precise entity and fact matching.

### Training Data That May Help

Useful training data includes Chinese COVID policy QA, Chinese news retrieval pairs, public-service FAQ retrieval data, and hard negatives from the same agency, same city, or same policy topic.

Synthetic data should generate factual Chinese questions over long policy or news passages. Questions should target dates, eligibility, administrative actions, benefits, or procedures. Hard negatives should mention the same pandemic context but not contain the answer.

### Model Improvement Notes

Strong systems should combine Chinese entity matching, date and number precision, and semantic handling of policy phrasing. BM25 is already strong, so model improvements should focus on reranking near-duplicate policy passages and preserving exact answer-bearing facts.

The benchmark is useful for evaluating public-information retrieval under short Chinese factual queries, where sparse term matching is an important baseline that dense systems must beat carefully.

## Example Data

| Query | Positive document |
| --- | --- |
| 北京市出台多少条措施帮助中小微企业应对疫情影响？ [24 chars] | 助力中小微企业度难关这些地方减租了抗疫战斗仍在继续，北京市发文出台16条措施帮助中小微企业应对疫情影响，其中房租减免措施备受关注，中关村各空间载体将如何落实该项措施？截至目前，中关村分园、特色产业园区纷纷推出减租措施，汇龙森、翠湖科创平台、中关村意谷等68家孵化器提出对房租进行减免，已推出的减免方案基本参照现行政策，减免租金15至30天。一起来看看它们的落实细则。亦庄园：2月房租最高减免100%中小微企业承租区内国有企业房产从事经营活动，按照政府要求坚持营业或依照防疫规定关闭停业且不裁员、少裁员的，免收2月份房租；承租用于办公用房的，给予2月份租金50%的减免。鼓励产业园区、商务楼宇等单位为科技型中小微企业减免租金，具体由双方协商解决，给予一定资金补贴。中关村创业大街：2月房租减免50%2月6日，中关村创业大街出台房屋租金（含物业费）减免方案。对于受到疫情影响的科技型中小微企业和创业服务机构，中关村创业大街给予2月份租金50%的减免。此次减免惠及入驻街区的近百家机构及创业团队，缓解了疫情对企业造成的经营冲击。汇龙森科技园：2月房租最高减免100%1.在汇龙森产权范围内承租产业用房的中小微企业（需注册及纳税），给予2020年2月份房屋租金50%的减免。2.在防疫期间为国家防疫工作做出突出贡献的园区中小微企业，给予2020年2月份房屋租金100%的减免。3.在防疫期间为国家防疫工作做出突出贡献的园区中小微企业，暂时经营困难的，除给予2020年2月份房屋租金100%全免外，给予防疫後续期间全部房屋租金50%的减免。锋创科技园：2月房租减免50%面对汹涌疫情，锋创科技园将对在园区内承租办公用房及商业的中小微企业（在北京经济技术开发区科创十三街18号院完成工商注册和属地纳税），给予2020年2月份租金50%减免。这是锋创科技园在疫情期间，继赠送消毒液、推行分时分批就餐、安装消毒帐篷、设立观察点等之後的又一举措，携手企业共抗疫情。博奥共享平台：最高减免1个月房租1.军腾博奥基地将为入驻企业减免1个月租金，为园区企业分担损失。此措施惠及45家企业，预计减免金额达118.62万元。2.按照此前合同约定，金信博奥基地部分企业2020年度租金将递增5%。疫情发生後，金信博奥基地向入驻企业承诺，2020年度房租不递增，维持不变，同时为企业提供的财税等服务减免50%收费，与企业共度难关。首... [1,000 / 1,481 chars] |
| 江苏援湖北第一批医疗队是什么时间？ [17 chars] | ——“散装江苏”星夜集结驰援湖北新华社南京2月12日电题：“必须打赢这场仗！”——“散装江苏”星夜集结驰援湖北新华社记者沈汝发、邱冰清11日，江苏支援黄石医疗队310人出发，开赴抗击新冠肺炎疫情战场。从1月25日首批江苏援湖北医疗队出发，到2月11日江苏支援黄石医疗队出发，被网友戏称为“散装”的江苏，截至目前已派出7批医疗队共计1792人赴湖北省参与医疗救治和疫情防控工作。“我做了30多年医生，作为一个老同志，未来跟大家一起并肩战斗！”江苏援黄石新冠肺炎防治前方指挥部总指挥鲁翔在出征仪式现场，向医疗队队员们发出动员令，“我们没有退路，必须打赢这场仗！必须完成任务！必须安全回来！”10日下午5点半，接到医院通知，沛县人民医院重症监护室主管护师李娜果断报名。李娜在重症监护室工作了12年，“我比一般护理人员经验多一些，这个时候我必须上前线。”时间紧急，李娜来不及和父母告别。“要收拾行李，非常匆忙，另外老人肯定也会担心。”她说，“等安稳以后，再跟他们慢慢说。”和李娜一样，在医院发出征召令后，许多医护人员写下请战书，摁下红手印。医疗队集结了来自南京、徐州、常州等10个设区市的310位医护人员，包括103名医生、200名护士，还有4名公卫人员和3名行政人员。这支医疗队是江苏对口支援黄石的第一梯队。鲁翔说，医疗队将在摸清当地总体情况，以及复杂病例、危重病例等基本情况的基础上，抓紧做好救治、防控工作，有效救治危重病人，降低死亡率、感染率，提高治疗率、治愈率。“本次的传染性疾病，给救治工作带来了一定的难度。”江苏援黄石新冠肺炎防治前方指挥部医疗救治组（专家组）组长黄英姿说，江苏支援黄石医疗队制定了缜密的科学救治方案。“目前掌握的情况是当地病人比较多，尤其是危重病人较多。当地重症、呼吸、感染管理等医疗护理力量比较缺。”黄英姿说，江苏根据前方需求组建队伍，主要以重症医学科、呼吸科、感染管理科等为主力。鲁翔介绍说：“我们组队是根据对方提出的要求，在通知时具体到专业、职称等，各家医院抽调精兵强将，绝大部分医院选来的人比我们的要求还要高一个等级，可以说是‘高配’。”江苏援黄石新冠肺炎防治前方指挥部副总指挥吴红辉介绍，江苏的“高配”团队得益于在组织队伍时对人员、专业、年龄构成等的多层次考量。医疗队队员来自不同医院，每个队员身后有单位和专业背景支持，做到前后方衔接。“我们一定是召必应，也一定战必胜... [1,000 / 1,173 chars] |
| 梧州市教育局开展的线上教学活动是怎么执行的？ [22 chars] | 我市各中小学校继续延迟开学2月26日，自治区新冠肺炎疫情防控三级应急响应工作指导意见出台，意见提出，将继续延迟学校开学时间。对此，梧州市教育局在继续落实各中小学校开学前後防控责任和开展线上教学活动的同时，也利用安全教育平台做好学生的疫情防控安全教育，让学生在家安心学习。工作指导意见指出，各级各类学校，包括大中小学、幼儿园、中职学校、技工学校等继续延迟开学，具体开学时间将根据疫情防控形势科学评估後提前向社会公布。延迟开学期间，各级教育行政部门和各级各类学校要努力按照&ldquo;停课不停教不停学&rdquo;的要求，继续组织实施好在线教育教学。对此，梧州市教育局加强组织各校开展线上教学活动。在开展线上教学活动中，各中小学校通过在线直播教学、网络点播教学、班级QQ群或微信群发送课後作业，并通过网络或者电话等方式，对学生的学习和生活进行指导和检查。此外，市教育局学校安全稳定工作科利用安全教育平台进行宣传，让广大师生和家长加强对疫情的认知，更科学地掌握疫情防控知识。（朱元冬滕瑜） [442 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Task-family paper | [Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval](https://arxiv.org/abs/2203.03367) |
| Benchmark paper | [C-Pack: Packed Resources For General Chinese Embeddings](https://arxiv.org/abs/2309.07597) |
| Source dataset | [mteb/CovidRetrieval](https://huggingface.co/datasets/mteb/CovidRetrieval) |
| NanoCMTEB dataset | [hakari-bench/NanoCMTEB](https://huggingface.co/datasets/hakari-bench/NanoCMTEB) |

Representative query and positive source snippets:

| Query | Positive document snippet |
| --- | --- |
| 北京市出台多少条措施帮助中小微企业应对疫情影响？ | A news passage states that Beijing issued 16 measures and describes rent reductions. |
| 江苏援湖北第一批医疗队是什么时间？ | A report describes Jiangsu medical teams departing for Hubei during late January and February. |
| 梧州市教育局开展的线上教学活动是怎么执行的？ | A local notice describes delayed school opening and online teaching arrangements. |
| 老年人和慢性病患者出现发热咳嗽等症状时应该怎么做？ | A health-service notice provides guidance for older adults and chronic disease patients. |
| 交通运输部规定对哪类人进行问责和严肃处理？ | A transportation ministry notice describes supervision and accountability during epidemic control. |
