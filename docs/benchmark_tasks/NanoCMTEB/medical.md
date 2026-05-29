# NanoCMTEB / medical

## Overview

Multi-CPR's medical domain was designed to test Chinese passage retrieval in a
specialized search setting where domain training matters more than broad
general web retrieval. In this NanoCMTEB split, short consumer-style Chinese
health questions retrieve concise medical answer passages. The observed topics
include pediatric symptoms, surgical timing, viral skin conditions,
musculoskeletal signs, and gynecological concerns, so the task asks whether a
retriever can connect informal health wording to clinically phrased advice.

## Details

### What the Original Data Measures

[Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval](https://arxiv.org/abs/2203.03367)
defines a multi-domain Chinese passage retrieval benchmark covering
e-commerce, entertainment video, and medical search. It emphasizes that
domain-trained retrieval systems improve substantially over general-domain
training, which is directly relevant to the medical split because symptoms,
diagnoses, and treatment guidance require domain-specific matching.

[C-Pack](https://arxiv.org/abs/2309.07597) uses `MedicalRetrieval` as one of
the C-MTEB retrieval datasets. In C-MTEB, retrieval tasks provide test queries
and a corpus, and models are evaluated by ranking relevant documents with
NDCG@10 as the main metric.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrels. Each
query has exactly one positive in the Nano labels. Queries average 18.12
characters and documents average 119.70 characters. The examples are short
consumer medical questions and direct explanatory answers.

The observed topics include pediatric symptoms, surgical timing, viral skin
conditions, musculoskeletal signs, and gynecological concerns. The text is
mostly Chinese and often uses informal question wording, while the answers use
clinical terms and advice-style phrasing.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.0150 and hit@10 = 0.0150, with only 3 positives in the top 10. Lexical
matching is weak when the query uses folk names, misspellings, symptom
descriptions, or shorthand and the answer uses the medical condition or clinical
explanation.

### Training Data That May Help

Useful training data includes non-overlapping Chinese medical consultation
pairs, symptom-to-diagnosis paraphrases, patient question-answer retrieval, and
medical hard negatives from similar symptoms. Training examples should maintain
the distinction between an answer that addresses the patient question and a
passage that merely mentions the same body part or disease.

### Synthetic Data Guidance

Synthetic data should pair brief patient questions with concise, medically
grounded answers. Hard negatives should share symptoms, age group, or treatment
terms but answer a different diagnosis or clinical scenario.

## Example Data

| Query | Positive document |
| --- | --- |
| 孩子刚满月，老是反酸看着他都难受，想问一下专家该怎么办才好呢？ (31 chars) | 病情分析：这属于正常现象，妈妈不用太担心。这是因为新生儿胃的位置呈水平位，贲门括约肌也较松弛，一旦摄入奶量稍多，即可发生溢奶现象。随着孩子年龄的增长，胃的位置逐渐变垂直，贲门括约肌肌力加强，溢奶次数就会逐渐减少，七八个月时停止。意见建议：预防宝宝溢奶或吐奶有赖于家长的正确喂养，如哺乳时应将宝宝斜着抱起，不要躺着喂哺；如果是用奶瓶喂奶时，奶头孔要大小适当，奶不可太烫或太冷，更忌吸入空气；喂奶之后不要翻动，应将宝宝斜靠在大人身上，轻拍背部，让吞入胃内 ... [truncated 225 chars](231 chars) |
| 小阴纯红奌用保妇康疑胶 (11 chars) | 你好,考虑是外阴炎引起的,外阴炎就是外阴的皮肤或粘膜所发生的炎症病变,如红、肿、痛、痒、糜烂等,外阴会因各种细菌感染而产生多种疾病,如外阴白斑、外阴瘙痒,一般治疗可以选择用清热解毒、除湿止痒的中草 药煎水坐浴,可以明显缓解外阴的痒痛不适,您还可以口服消炎药如环丙沙星,再配 合使用妇炎洁 或洁尔阴洗液清洗外阴综合治疗, (159 chars) |
| 寻常疣也可以用鸦胆子治疗吗 (13 chars) | 鸦胆子是可以治寻常疣，烂肉（疣）也抗病毒，但有复发的可能，最好加服阿昔洛韦片二周治疗。效果最好。这些局部用药虽可造成局部坏死而治疗寻常疣,但说到底只是一个&quot;烂&quot;字而已,有时候反而刺激寻常疣而长大,激光治疗和这些方法类似,只是将烂的时间变短,其实作为病毒感染的寻常疣一般两年左右会自愈. (152 chars) |
| 大鱼际肌肉肿胀是怎么了 (11 chars) | 你好，有可能是局部损伤，导致肿胀，可以做做冷敷，超过24小时，可以热敷，也有可能是被蚊虫叮咬了，观察一下，如果是涂抹点碘伏，很快就会好了。 (69 chars) |
| 心肌梗死血清肌凝蛋白轻链和重链变化是怎样 (20 chars) | 病情分析： 朋友你好根据您所说的情况分析这些指标主要就是分析心肌细胞受损程度的。 指导意见： 根据您所说的情况建议你想知道这么具体的区别一般是没有太特殊的意义的，主要看一下心肌损伤标志物就可以了。 (98 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoCMTEB |
| Backing dataset | NanoCMTEB |
| Task / split | medical |
| Hugging Face dataset | [hakari-bench/NanoCMTEB](https://huggingface.co/datasets/hakari-bench/NanoCMTEB) |
| Language | zh |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.3582 |
| BM25 hit@10 | 0.4400 |
| BM25 Recall@100 | 0.5600 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.5691 |
| Dense hit@10 | 0.6750 |
| Dense Recall@100 | 0.8400 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4699 |
| Reranking hybrid hit@10 | 0.5700 |
| Reranking hybrid Recall@100 | 0.8250 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 35 |
| Query length avg chars | 18.12 |
| Document length avg chars | 119.70 |

### Public Sources

- [Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval](https://arxiv.org/abs/2203.03367); 2022; Dingkun Long et al.
- [C-Pack: Packed Resources For General Chinese Embeddings](https://arxiv.org/abs/2309.07597); 2024; Shitao Xiao et al.
- [mteb/MedicalRetrieval dataset card](https://huggingface.co/datasets/mteb/MedicalRetrieval).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoCMTEB](https://huggingface.co/datasets/hakari-bench/NanoCMTEB)
- Source dataset: [mteb/MedicalRetrieval](https://huggingface.co/datasets/mteb/MedicalRetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval | 2022 | task paper | https://arxiv.org/abs/2203.03367 |
| C-Pack: Packed Resources For General Chinese Embeddings | 2024 | benchmark paper | https://arxiv.org/abs/2309.07597 |
| mteb/MedicalRetrieval | unknown | Hugging Face dataset | https://huggingface.co/datasets/mteb/MedicalRetrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoCMTEB
  backing_dataset: NanoCMTEB
  dataset_id: hakari-bench/NanoCMTEB
  task_name: medical
  split_name: medical
  language: zh
  category: natural_language
  document_path: docs/benchmark_tasks/NanoCMTEB/medical.md
  source_research:
    primary_source_type: task_paper_and_benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 18.12
    document_mean: 119.7008
  bm25:
    ndcg_at_10: 0.3581679205229802
    hit_at_10: 0.44
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: MedicalRetrieval dev
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoCMTEB medical queries, qrels, and answer passages
    useful_training_data:
    - Chinese medical consultation QA pairs
    - symptom-diagnosis paraphrase data
    - patient question-answer retrieval pairs
    - same-symptom medical hard negatives
    synthetic_data:
      document_generation: concise Chinese medical answer passages
      question_generation: short patient questions with informal symptom wording
      answerability: positives should address the specific medical scenario
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoCMTEB
    source_urls:
    - label: Multi-CPR arXiv
      url: https://arxiv.org/abs/2203.03367
    - label: C-Pack arXiv
      url: https://arxiv.org/abs/2309.07597
    - label: mteb/MedicalRetrieval
      url: https://huggingface.co/datasets/mteb/MedicalRetrieval
    source_notes: []
  references:
  - title: 'Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval'
    url: https://arxiv.org/abs/2203.03367
    year: 2022
    is_paper: true
    source_confidence: definitive_paper_link
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
      ndcg_at_10: 0.3581679205
      hit_at_10: 0.44
      recall_at_100: 0.56
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.56
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5690757172
      hit_at_10: 0.675
      recall_at_100: 0.84
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.84
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4699479831
      hit_at_10: 0.57
      recall_at_100: 0.825
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.175
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.825
      safeguard_positive_rows: 35
      rows_with_101_candidates: 35
```
