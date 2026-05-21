# NanoLaw / NanoLeCaRDv2

## Overview

`NanoLeCaRDv2` is a Chinese legal case retrieval task. Each query is a Chinese
criminal case document or fact section, and the retriever must find related
criminal cases under Chinese law.

## Details

### What the Original Data Measures

[LeCaRDv2: A Large-Scale Chinese Legal Case Retrieval Dataset](https://arxiv.org/abs/2310.17609)
introduces a legal case retrieval dataset with 800 queries and 55,192 candidate
cases extracted from more than 4.3 million Chinese criminal case documents. The
paper argues that prior Chinese legal retrieval datasets were limited by size,
narrow relevance definitions, and simple candidate pooling. LeCaRDv2 expands
relevance to characterization, penalty, and procedure, and uses a two-level
candidate pooling strategy. It also reports annotation by multiple criminal-law
experts.

The [MTEB LeCaRDv2 card](https://huggingface.co/datasets/mteb/LeCaRDv2)
describes the task as retrieving the case document most relevant to the scenario
in each query.

### Observed Data Profile

The Nano split has 159 queries, 3,795 documents, and 3,896 positive qrels.
Queries average 4,259.44 characters, and documents average 7,231.82
characters. Every query has multiple positives, with an average of 24.50 and a
median of 28 positives.

Observed examples are full Chinese criminal judgments covering offences such as
寻衅滋事, 生产/销售假药, 非法捕捞, 赌博, and organized criminal activity. The task
requires matching legal and factual similarity across long court records.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.6379 and hit@10 = 0.9371. It ranks a positive first for 126 queries. The
strong BM25 result reflects repeated charge names and formulaic court-language,
but the multi-aspect relevance definition still makes exact legal matching more
than keyword overlap.

### Training Data That May Help

Useful training data includes Chinese legal case retrieval, criminal-charge
classification with fact sections, court-document similarity, and hard
negatives sharing the same offence but differing in penalty, procedure, or
material facts.

### Synthetic Data Guidance

Generate Chinese criminal case summaries with charge, facts, procedural posture,
and sentencing detail. Positives should be related cases under characterization,
penalty, and procedure; hard negatives should share surface charge labels but
fail one of the legal relevance dimensions.

## Example Data

| Query | Positive document |
| --- | --- |
| 张红、孙XX盗窃一案一审刑事判决书黑龙江省齐齐哈尔市龙沙区人民法院刑事判决书（2015）龙刑初字第351号：齐齐哈尔市龙沙区人民检察院以齐龙检公诉刑诉（2015）266号起诉书指控被告人张红、孙ＸＸ犯盗窃罪，于2015年10月22日向本院提起公诉，本院于同日立案受理。立案受理后，依法组成合议庭于2015年11月6日公开开庭进行了审理。齐齐哈尔市龙沙区人民检察院指派检察员李恩珠出庭支持公诉，被告人张红、孙ＸＸ及辩护人卜华林、李玲玲到庭参加诉讼。现已 ... [truncated 225 chars](1965 chars) | 马金成盗窃一审刑事判决书黑龙江省齐齐哈尔市龙沙区人民法院刑事判决书（2018）黑0202刑初51号：1981年11月20日出生于黑龙江省绥化市，汉族,小学文化，无职业，无固定住址，户籍所在地黑龙江省绥化市北林区兴福乡民权村5组66号。2000年因犯盗窃罪被黑龙江省绥化市北林区人民法院判处有期徒刑二年，2002年因犯盗窃罪被黑龙江省北安市人民法院判处有期徒刑二年，2005年因犯盗窃罪被黑龙江省宾县人民法院判处有期徒刑二年，2012年因犯盗窃罪被吉林 ... [truncated 225 chars](4616 chars) |
| 胡某某伪造国家机关公文、印章罪、伪造事业单位印章罪刑事一审判决书德阳市旌阳区人民法院刑事判决书（2017）川0603刑初341号：德阳市旌阳区人民检察院以旌检公刑诉（2017）313号起诉书指控被告人胡某某犯诈骗罪，于2017年7月20日向本院提起公诉。本院受理后依法组成合议庭，公开开庭审理了本案。德阳市旌阳区人民检察院指派检察员郑世鹏出庭支持公诉，被害人龙某某、被告人胡某某到庭参加诉讼。审理期间检察机关申请延期审理一次，现已审理终结德阳市旌阳区 ... [truncated 225 chars](1825 chars) | 吴某诈骗罪一审刑事判决书河北省海兴县人民法院刑事判决书（2014）海刑初字第91号：河北省海兴县人民检察院以海检公诉刑诉（2014）94号起诉书指控被告人吴某犯诈骗罪，于2014年10月29日向本院提起公诉。本院依法适用简易程序，实行独任审判，公开开庭审理了本案。海兴县人民检察院指派代理检察员相东明出庭支持公诉，被告人吴某到庭参加诉讼。现已审理终结海兴县人民检察院指控，2013年6月份至2014年8月份，被告人吴某通过网络聊天认识被害人黄某，吴某 ... [truncated 225 chars](1201 chars) |
| 录俊荣何某某非法吸收公众存款一审刑事判决书广东省珠海市香洲区人民法院刑事判决书（2014）珠香法刑初字第2800号：珠海市香洲区人民检察院以珠香检公诉刑诉（2014）2881号起诉书指控被告人何俊荣何某某犯非法吸收公众存款罪，于2014年12月19日向本院提起公诉。本院依法组成合议庭，公开开庭审理了本案。珠海市香洲区人民检察院指派检察员谢谦、黄斌权出庭支持公诉，被告人何俊荣何某某及其辩护人郭俊德、吴文仪、证人曾某、黄某1、吴某1、何某1到庭参加诉 ... [truncated 225 chars](24088 chars) | 圱俊、朱伟等非法吸收公众存款一审刑事判决书上海市普陀区人民法院刑事判决书（2017）沪0107刑初1130号：上海市普陀区人民检察院以沪普检金融刑诉［2017］56号、沪普检金融刑变诉［2018］1起诉书指控被告人朱俊、朱伟、卞海翔、赵泽亚、袁永明、陈荑、许志梅、火东雯、薛荣新、王勤、唐丽娜犯非法吸收公众存款罪，于2017年11月15日向本院提起公诉。本院依法组成合议庭，公开开庭审理了本案。上海市普陀区人民检察院指派检察员戈某出庭支持公诉。被告人 ... [truncated 225 chars](10804 chars) |
| 鵵某姚某某姚某寻衅滋事一审判决书安徽省萧县人民法院刑事判决书（2016）皖1322刑初10号：萧县人民检察院以萧检刑诉［2016］3号起诉书指控被告人赵某、姚某某、姚某犯寻衅滋事罪，于2016年1月5日向本院提起公诉,本院依法组成合议庭,于2016年1月26日公开开庭审理了本案。萧县人民检察院指派代理检察员路崇艺出庭支持公诉，被告人赵某及其辩护人阚辉、被告人姚某某及其辩护人王修动、被告人姚某及其辩护人黄阳等到庭参加了诉讼。本案现已审理终结萧县人民 ... [truncated 225 chars](4409 chars) | 姚天朗寻衅滋事罪一审刑事判决书四川省西充县人民法院刑事判决书（2019）川1325刑初79号：西充县人民检察院以南西检公诉刑诉（2019）51号起诉书指控被告人姚天朗涉嫌寻衅滋事罪、危险驾驶罪，于2019年5月27日向本院提起公诉，本院受理后，依法组成合议庭公开开庭审理了本案。西充县人民检察院指派检察员冯慧丽出庭支持公诉，被告人姚天朗到庭参加诉讼，本案现已审理终结公诉机关指控：被告人姚天朗在两年内,多次随意殴打他人、随意毁坏公私财物,其行为触犯了 ... [truncated 225 chars](3594 chars) |
| 田雷、田涛抢劫、抢夺二审刑事判决书河北省高级人民法院刑事判决书（2018）冀刑终348号：河北省沧州市中级人民法院审理沧州市人民检察院指控原审被告人田雷、田涛、田家兴犯抢劫罪、抢夺罪，原审被告人王福华、宫美静、王福清犯掩饰、隐瞒犯罪所得罪一案，于2018年6月11日作出（2018）冀09刑初16号刑事判决。沧州市人民检察院提出抗诉，河北省人民检察院支持抗诉。本院依法组成合议庭，公开开庭审理了本案。河北省人民检察院指派检察员杨丽芳、杨晶出庭履行职务 ... [truncated 225 chars](10707 chars) | 林强、颜华抢劫罪一审刑事判决书广西壮族自治区合浦县人民法院刑事判决书（2019）桂0521刑初47号：合浦县人民检察院以合检公刑诉［2018］771号起诉书指控被告人颜华犯抢劫罪、抢夺罪、盗窃罪，被告人林强犯抢劫罪、抢夺罪于2019年1月4日向本院提起公诉,2019年8月2日向本院变更起诉。本院依法适用普通程序，组成合议庭，于2019年5月6日／2019年8月20日公开开庭审理了本案。合浦县人民检察院指派检察员杨世毅出庭支持公诉，被告人颜华、林强 ... [truncated 225 chars](8029 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoLaw |
| Backing dataset | NanoLaw |
| Task / split | NanoLeCaRDv2 |
| Hugging Face dataset | [hakari-bench/NanoLaw](https://huggingface.co/datasets/hakari-bench/NanoLaw) |
| Language | zh |
| Category | natural_language |
| Queries | 159 |
| Documents | 3,795 |
| Positive qrels | 3,896 |
| Positives per query | avg 24.50 / min 4 / median 28 / max 30 |
| Multi-positive queries | 159 (100.00%) |
| BM25 nDCG@10 | 0.6379 |
| BM25 hit@10 | 0.9371 |
| Query length avg chars | 4259.44 |
| Document length avg chars | 7231.82 |

### Public Sources

- [LeCaRDv2: A Large-Scale Chinese Legal Case Retrieval Dataset](https://arxiv.org/abs/2310.17609); 2023; Haitao Li et al.
- [THUIR LeCaRDv2 repository](https://github.com/THUIR/LeCaRDv2).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoLaw](https://huggingface.co/datasets/hakari-bench/NanoLaw)
- Source dataset: [mteb/LeCaRDv2](https://huggingface.co/datasets/mteb/LeCaRDv2)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| LeCaRDv2: A Large-Scale Chinese Legal Case Retrieval Dataset | 2023 | arXiv paper | https://arxiv.org/abs/2310.17609 |
| THUIR LeCaRDv2 | 2023 | GitHub repository | https://github.com/THUIR/LeCaRDv2 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoLaw
  backing_dataset: NanoLaw
  dataset_id: hakari-bench/NanoLaw
  task_name: NanoLeCaRDv2
  split_name: NanoLeCaRDv2
  language: zh
  category: natural_language
  document_path: docs/benchmark_tasks/NanoLaw/NanoLeCaRDv2.md
  source_research:
    primary_source_type: task_paper_and_dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 159
    documents: 3795
    positive_qrels: 3896
  positives_per_query:
    average: 24.50314465408805
    min: 4
    median: 28
    max: 30
    multi_positive_queries: 159
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 4259.440251572327
    document_mean: 7231.823978919631
  bm25:
    ndcg_at_10: 0.6379051373412444
    hit_at_10: 0.9371069182389937
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: lecardv2_test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoLeCaRDv2 queries, qrels, and relevant criminal case documents
    useful_training_data:
      - Chinese legal case retrieval
      - criminal charge and fact-section retrieval pairs
      - court-document similarity data
      - same-charge hard negatives
    synthetic_data:
      document_generation: Chinese criminal judgments with facts, reasoning, and sentencing
      question_generation: Chinese criminal query cases with material facts and procedural details
      answerability: positives should align on characterization, penalty, or procedure
    multi_positive_training: preserve_large_positive_sets_per_query
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoLaw
    source_urls:
      - label: LeCaRDv2 arXiv
        url: https://arxiv.org/abs/2310.17609
      - label: THUIR LeCaRDv2
        url: https://github.com/THUIR/LeCaRDv2
      - label: MTEB LeCaRDv2
        url: https://huggingface.co/datasets/mteb/LeCaRDv2
    source_notes: []
  references:
    - title: "LeCaRDv2: A Large-Scale Chinese Legal Case Retrieval Dataset"
      url: https://arxiv.org/abs/2310.17609
      year: 2023
      doi: 10.48550/arXiv.2310.17609
      is_paper: true
      source_confidence: definitive_paper_link
```
