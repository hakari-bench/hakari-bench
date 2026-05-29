# NanoCMTEB / covid

## Overview

`covid` is a Chinese COVID-19 news and policy retrieval task. Queries ask for
specific pandemic-related facts, measures, or public-service information, and
documents are longer news or government-policy passages.

## Details

### What the Original Data Measures

[Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval](https://arxiv.org/abs/2203.03367)
introduces Chinese passage retrieval datasets collected from real search
systems, with human annotated query-passage relevance pairs in specific
domains. The paper emphasizes that domain-specific Chinese retrieval can differ
substantially from general-domain retrieval and that in-domain labeled data
produces large gains.

[C-Pack: Packed Resources For General Chinese Embeddings](https://arxiv.org/abs/2309.07597)
includes `CovidRetrieval` in C-MTEB's retrieval category, where NDCG@10 is used
as the main retrieval metric. The MTEB card describes this task as retrieval
over COVID-19 news articles.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 204 positive qrels.
Queries average 25.73 characters and are usually question-form requests for a
policy detail. Documents average 409.35 characters, but some are much longer
government notices or news articles. Only 2 queries have multiple positives.

The examples show local government service platforms, tax incentives, financial
support, legal enforcement, and policies for medical staff. The relevant
document often contains the answer in a paragraph embedded in a longer notice.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.1778 and hit@10 = 0.2000, with 30 positives ranked first. This is stronger
than several other NanoCMTEB splits because policy queries often reuse exact
institution names, dates, and administrative terms. It is still far from solved:
most positives are not in the top 10, especially when the answer is buried in a
long article or the query paraphrases a policy.

### Training Data That May Help

Useful training data includes Chinese news QA, public-policy retrieval, COVID
FAQ retrieval, and hard negatives from the same city, agency, or policy topic.
Domain-specific negatives are important because many passages share pandemic
vocabulary without answering the requested policy detail.

### Synthetic Data Guidance

Synthetic examples should create factual Chinese questions over long policy or
news passages. Questions should target dates, eligibility, administrative
actions, or benefit details, while hard negatives should come from topically
similar notices that mention the same pandemic context but not the answer.

## Example Data

| Query | Positive document |
| --- | --- |
| 北京市出台多少条措施帮助中小微企业应对疫情影响？ (24 chars) | 助力中小微企业度难关这些地方减租了抗疫战斗仍在继续，北京市发文出台16条措施帮助中小微企业应对疫情影响，其中房租减免措施备受关注，中关村各空间载体将如何落实该项措施？截至目前，中关村分园、特色产业园区纷纷推出减租措施，汇龙森、翠湖科创平台、中关村意谷等68家孵化器提出对房租进行减免，已推出的减免方案基本参照现行政策，减免租金15至30天。一起来看看它们的落实细则。亦庄园：2月房租最高减免100%中小微企业承租区内国有企业房产从事经营活动，按照政府 ... [truncated 225 chars](1481 chars) |
| 江苏援湖北第一批医疗队是什么时间？ (17 chars) | ——“散装江苏”星夜集结驰援湖北新华社南京2月12日电题：“必须打赢这场仗！”——“散装江苏”星夜集结驰援湖北新华社记者沈汝发、邱冰清11日，江苏支援黄石医疗队310人出发，开赴抗击新冠肺炎疫情战场。从1月25日首批江苏援湖北医疗队出发，到2月11日江苏支援黄石医疗队出发，被网友戏称为“散装”的江苏，截至目前已派出7批医疗队共计1792人赴湖北省参与医疗救治和疫情防控工作。“我做了30多年医生，作为一个老同志，未来跟大家一起并肩战斗！”江苏援黄石 ... [truncated 225 chars](1173 chars) |
| 梧州市教育局开展的线上教学活动是怎么执行的？ (22 chars) | 我市各中小学校继续延迟开学2月26日，自治区新冠肺炎疫情防控三级应急响应工作指导意见出台，意见提出，将继续延迟学校开学时间。对此，梧州市教育局在继续落实各中小学校开学前後防控责任和开展线上教学活动的同时，也利用安全教育平台做好学生的疫情防控安全教育，让学生在家安心学习。工作指导意见指出，各级各类学校，包括大中小学、幼儿园、中职学校、技工学校等继续延迟开学，具体开学时间将根据疫情防控形势科学评估後提前向社会公布。延迟开学期间，各级教育行政部门和各级 ... [truncated 225 chars](442 chars) |
| 告知老年人、慢性病患者出现发热、咳嗽、鼻塞、头痛、乏力、气促、结膜充血或消化道症状时，应该怎么做？ (49 chars) | 关于印发基层医疗卫生机构在新冠肺炎疫情防控期间为老年人关于印发基层医疗卫生机构在新冠肺炎疫情防控期间为老年人慢性病患者提供医疗卫生服务指南（试行）的通知国卫基层家医便函〔2020〕2号各省、自治区、直辖市及新疆生产建设兵团卫生健康委基层处：为指导基层医疗卫生机构在新冠肺炎疫情防控期间为老年人、慢性病患者更好地提供医疗卫生服务，结合《国家基本公共卫生服务规范（第三版）》和国家卫生健康委有关疫情防控的政策措施，根据疫情防控工作需要，制定了《基层医疗卫 ... [truncated 225 chars](1161 chars) |
| 交通运输部规定对哪类人进行问责和严肃处理？ (21 chars) | 交通运输部要求进一步加强疫情防控监督工作交通运输部应对新冠肺炎联防联控机制发出通知要求，增强做好疫情防控监督工作的责任感和使命感确保疫情防控部署到哪里监督检查就跟进到哪里2月11日，交通运输部应对新冠肺炎联防联控机制发出通知，要求进一步加强疫情防控监督工作。通知指出，当前，全国上下正在认真贯彻落实习近平总书记对新型冠状病毒感染肺炎疫情的重要指示，众志成城、万众一心防控疫情。部党组坚决贯彻落实党中央、国务院决策部署，把人民群众生命安全和身体健康放在 ... [truncated 225 chars](1076 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoCMTEB |
| Backing dataset | NanoCMTEB |
| Task / split | covid |
| Hugging Face dataset | [hakari-bench/NanoCMTEB](https://huggingface.co/datasets/hakari-bench/NanoCMTEB) |
| Language | zh |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 204 |
| Positives per query | avg 1.02 / min 1 / median 1.0 / max 4 |
| Multi-positive queries | 2 (1.00%) |
| BM25 nDCG@10 | 0.7888 |
| BM25 hit@10 | 0.8750 |
| BM25 Recall@100 | 0.9608 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7518 |
| Dense hit@10 | 0.8550 |
| Dense Recall@100 | 0.9314 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.7834 |
| Reranking hybrid hit@10 | 0.8850 |
| Reranking hybrid Recall@100 | 0.9902 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 2 |
| Query length avg chars | 25.73 |
| Document length avg chars | 409.35 |

### Public Sources

- [Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval](https://arxiv.org/abs/2203.03367); 2022; Dingkun Long et al.
- [C-Pack: Packed Resources For General Chinese Embeddings](https://arxiv.org/abs/2309.07597); 2024; Shitao Xiao et al.
- [mteb/CovidRetrieval dataset card](https://huggingface.co/datasets/mteb/CovidRetrieval).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoCMTEB](https://huggingface.co/datasets/hakari-bench/NanoCMTEB)
- Source dataset: [mteb/CovidRetrieval](https://huggingface.co/datasets/mteb/CovidRetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval | 2022 | task-family paper | https://arxiv.org/abs/2203.03367 |
| C-Pack: Packed Resources For General Chinese Embeddings | 2024 | benchmark paper | https://arxiv.org/abs/2309.07597 |
| mteb/CovidRetrieval | unknown | Hugging Face dataset | https://huggingface.co/datasets/mteb/CovidRetrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoCMTEB
  backing_dataset: NanoCMTEB
  dataset_id: hakari-bench/NanoCMTEB
  task_name: covid
  split_name: covid
  language: zh
  category: natural_language
  document_path: docs/benchmark_tasks/NanoCMTEB/covid.md
  source_research:
    primary_source_type: task_family_paper_and_benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone CovidRetrieval paper was confirmed
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 204
  positives_per_query:
    average: 1.02
    min: 1
    median: 1.0
    max: 4
    multi_positive_queries: 2
    multi_positive_query_percent: 1.0
  text_stats_chars:
    query_mean: 25.735
    document_mean: 409.3471
  bm25:
    ndcg_at_10: 0.7888439205474314
    hit_at_10: 0.875
    source: dataset_candidate_subset
  learning:
    original_train_split: available_in_source_family
    evaluation_split_origin: CovidRetrieval dev
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoCMTEB covid queries, qrels, and COVID news passages
    useful_training_data:
    - Chinese COVID policy question-answer data
    - Chinese news retrieval pairs
    - public-service FAQ retrieval data
    - same-agency and same-city hard negatives
    synthetic_data:
      document_generation: Chinese pandemic news and public-policy notices
      question_generation: fact-seeking questions about policies, dates, benefits,
        and procedures
      answerability: positives should contain the requested policy detail
    multi_positive_training: mostly_single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoCMTEB
    source_urls:
    - label: Multi-CPR arXiv
      url: https://arxiv.org/abs/2203.03367
    - label: C-Pack arXiv
      url: https://arxiv.org/abs/2309.07597
    - label: mteb/CovidRetrieval
      url: https://huggingface.co/datasets/mteb/CovidRetrieval
    source_notes: []
  references:
  - title: 'Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval'
    url: https://arxiv.org/abs/2203.03367
    year: 2022
    is_paper: true
    source_confidence: probably_correct_task_family
  - title: 'C-Pack: Packed Resources For General Chinese Embeddings'
    url: https://arxiv.org/abs/2309.07597
    year: 2024
    is_paper: true
    source_confidence: definitive_benchmark_paper
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7888439205
      hit_at_10: 0.875
      recall_at_100: 0.9607843137
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9607843137
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.751799718
      hit_at_10: 0.855
      recall_at_100: 0.931372549
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.931372549
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.7834415507
      hit_at_10: 0.885
      recall_at_100: 0.9901960784
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.01
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9901960784
      safeguard_positive_rows: 2
      rows_with_101_candidates: 2
```
