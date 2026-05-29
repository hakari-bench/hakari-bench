# NanoMLDR / zh

## Overview

`zh` is the Chinese split of NanoMLDR. Chinese questions retrieve long Chinese
articles from Wikipedia and Wudao-derived sources.

## Details

### What the Original Data Measures

[M3-Embedding](https://arxiv.org/abs/2402.03216) introduces MLDR as a
multilingual long-document retrieval benchmark and states that MLDR articles are
curated from Wikipedia, Wudao, and mC4. The [MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR)
lists Chinese as sourced from Wikipedia and Wudao, with GPT-3.5-generated
questions based on sampled paragraphs.

### Observed Data Profile

The Nano split has 200 queries, 7,877 documents, and 200 positive qrels. Each
query has one positive. Queries average 20.68 characters and documents average
12,307.31 characters. Examples include web fiction, campus romance, historical
geography, cooking recipes, and pre-modern biography.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.6997 and hit@10 = 0.7950. It ranks 121 positives first. Short Chinese
questions often retain distinctive names, but the retrieval target is still a
long article where the relevant paragraph may be surrounded by large amounts of
unrelated context.

### Training Data That May Help

Useful training data includes Chinese long-document QA retrieval, Chinese
Wikipedia and Wudao article retrieval, multilingual MLDR training data, and hard
negatives from articles with overlapping titles, entities, or genre terms.

### Synthetic Data Guidance

Synthetic data should pair long Chinese articles with short questions generated
from one paragraph. Hard negatives should share named entities or genre terms
while not containing the answer-bearing paragraph.

## Example Data

| Query | Positive document |
| --- | --- |
| 《条例》中对于水资源管理的具体措施有哪些？ (21 chars) | 湖北省抗旱条例 湖北是千湖之省，然而，受制于气象、资源、工程、发展等四大缺水矛盾，湖北一直存在着缺水之忧。据统计，新中国建立以来的64年间，湖北平均4年发生一次大范围的严重以上程度的干旱，中轻度旱每年都会在局部或全省发生，其中鄂北等地更是十年九旱。近十年来，湖北的干旱核心逐步向鄂中丘陵区蔓延，形成十堰、襄阳、随州、孝感、荆门等市为主的干旱带，且有逐年扩大的趋势。抗旱急需依法规范，因此，《湖北省抗旱条例》的出台是势在必行。据悉，该条例共19条，对抗 ... [truncated 225 chars](15116 chars) |
| 什么是中枢理论的核心概念？ (13 chars) | [转载]中枢扩张、扩展 原文地址:中枢扩张、扩展作者:覃迪 大家有关于中枢扩张和中枢扩展的异同点,以及两者之间疑问、想法、建议,对这两者进行详细的区分并且以此为中心向上和向下延伸细化。 中枢扩张和中枢扩展的前生后世能全面透彻的理解掌握后,对缠论的理解会更进一步常见谬误: 1、认为扩张等同扩展！ 2、扩张后,走出了不可扩展,就说没有扩张或不属扩张范畴。缠中说禅走势中枢: 某级别走势类型中,被至少三个连续次级别走势类型所重叠的部分。 这里有一个递归的 ... [truncated 225 chars](10712 chars) |
| 练习「抱住健康」法时，如何通过调动穴位和经络来实现养身和养心的效果？ (34 chars) | [转载]养生,就是养阳气;阳气旺盛,百病不侵 原文地址:养生,就是养阳气；阳气旺盛,百病不侵作者:夏一文心灵禅语 1、人要活到多少岁才算尽其天年 为何现代人的平均寿命才七八十岁,而且大多是死于疾病！为什么今人比古人所预期的天年寿命减少了将近三分之一呢？是谁偷走了这四五十年的宝贵生命呢？ 在长期从医经历中,我面对的病人是各种各样的,我经常会问他们一个问题:「你想活到多大岁数？」令我惊讶的是,很多人都说没有仔细想过这个问题。 生命的长短与质量好坏是我 ... [truncated 225 chars](9944 chars) |
| 双子座和双鱼座的复杂性格如何影响他们的关系？ (22 chars) | 水象星座 “水”是属于液态的元素。和水相关的事物和含义有很多，比如水是地球上生物生存的必要条件之一；由水构成的海洋占去地表大部分的面积，而且很多生物体内也含有大量的水分，包括人类也是如此。水在四季中是代表夏天的元素，继承了代表春天的火元素所创造出的生命力后，作为情感的存在。水是所有元素中唯一可以从液态转变成气态或固态的，但就和火一样，从每一种状态转换成另一种状态的过程都是一致且稳定的。正如同人类多变而难以捉摸的情感世界。水象星座特性延伸 水族人 ... [truncated 225 chars](11284 chars) |
| 公孙氏最初出现在哪个时期？ (13 chars) | 公孙范 公孙范，东汉末期人物，赵云第一个主公-公孙瓒的从弟，在公孙瓒与袁绍界桥之战中与公孙瓒一同败走。 姓名：公孙范 性别：男 出生年月：不详 国籍：中国 时代：东汉末期 籍贯：勃海 民族：汉族 身份：将军。姓名：公孙范 性别：男 出生年月：不详 国籍：中国 时代：东汉末期 籍贯：勃海 民族：汉族 身份：将军 公孙范（生卒年不详），东汉末期人物，公孙瓒从弟。 袁绍初欲以自身勃海太守印绶给与公孙瓒弟公孙范作为巴结，但公孙范转为巴结公孙瓒。 初平二年 ... [truncated 225 chars](9451 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMLDR |
| Backing dataset | NanoMLDR |
| Task / split | zh |
| Hugging Face dataset | [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR) |
| Language | zh |
| Category | natural_language |
| Queries | 200 |
| Documents | 7877 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.7030 |
| BM25 hit@10 | 0.7950 |
| BM25 Recall@100 | 0.9000 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3392 |
| Dense hit@10 | 0.4450 |
| Dense Recall@100 | 0.6300 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4933 |
| Reranking hybrid hit@10 | 0.6250 |
| Reranking hybrid Recall@100 | 0.8950 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 21 |
| Query length avg chars | 20.68 |
| Document length avg chars | 12307.31 |

### Public Sources

- [M3-Embedding](https://arxiv.org/abs/2402.03216); 2024; Jianlv Chen et al.
- [MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR)
- Source dataset: [Shitao/MLDR](https://huggingface.co/datasets/Shitao/MLDR)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation | 2024 | benchmark paper | https://arxiv.org/abs/2402.03216 |
| MLDR: Multilingual Long-Document Retrieval dataset | 2024 | dataset card | https://huggingface.co/datasets/Shitao/MLDR |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMLDR
  backing_dataset: NanoMLDR
  dataset_id: hakari-bench/NanoMLDR
  task_name: zh
  split_name: zh
  language: zh
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMLDR/zh.md
  source_research:
    primary_source_type: benchmark_paper_and_dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 7877
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 20.675
    document_mean: 12307.310524311286
  bm25:
    ndcg_at_10: 0.7029898411617381
    hit_at_10: 0.795
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: MLDR Chinese split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoMLDR zh queries, qrels, and positive documents
    useful_training_data:
    - Chinese long-document QA retrieval pairs
    - Chinese Wikipedia and Wudao article retrieval
    - multilingual MLDR training data outside this Nano split
    - title-sharing Chinese hard negatives
    synthetic_data:
      document_generation: long Chinese articles from Wikipedia or Wudao-style corpora
      question_generation: short paragraph-grounded Chinese questions
      answerability: positives should be full articles containing the answer-bearing
        paragraph
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMLDR
    source_urls:
    - label: M3-Embedding arXiv
      url: https://arxiv.org/abs/2402.03216
    - label: Shitao/MLDR
      url: https://huggingface.co/datasets/Shitao/MLDR
    source_notes: []
  references:
  - title: 'M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity
      Text Embeddings Through Self-Knowledge Distillation'
    url: https://arxiv.org/abs/2402.03216
    year: 2024
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7029898412
      hit_at_10: 0.795
      recall_at_100: 0.9
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3391941114
      hit_at_10: 0.445
      recall_at_100: 0.63
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.63
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4932861039
      hit_at_10: 0.625
      recall_at_100: 0.895
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.105
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.895
      safeguard_positive_rows: 21
      rows_with_101_candidates: 21
```
