# NanoMLDR / ar

## Overview

`ar` is the Arabic split of NanoMLDR. It evaluates Arabic question-to-long-document
retrieval, where each query asks about information contained somewhere inside a
lengthy Arabic article.

## Details

### What the Original Data Measures

[M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation](https://arxiv.org/abs/2402.03216)
introduces MLDR as a multilingual long-document retrieval benchmark curated from
Wikipedia, Wudao, and mC4. The paper evaluates long-document retrieval with
NDCG@10 and reports that BM25 remains a strong baseline for MLDR, while learned
sparse and hybrid retrieval can improve on long-document matching.

The [MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR) states that
long articles are sampled, a paragraph is selected, and GPT-3.5 generates one
specific question from that paragraph. The generated question and the full
sampled article form the retrieval pair. For Arabic, the source card lists
Wikipedia as the source.

### Observed Data Profile

The Nano split has 150 queries, 4,766 documents, and 150 positive qrels. Every
query has one positive document. Queries average 71.09 characters, while
documents average 12,006.83 characters. The sampled rows are Arabic questions
over long encyclopedia-style articles about economics, ancient empires,
Napoleonic history, aviation history, and geography.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.6630 and hit@10 = 0.7867. It ranks a positive first for 81 of 150 queries,
and the median best positive rank is 1. Arabic lexical matching is often strong
because generated questions reuse article-specific names and concepts, but the
task still requires finding a small answer-bearing region inside a long article.

### Training Data That May Help

Useful training data includes Arabic Wikipedia question-document pairs,
long-document QA retrieval, multilingual MLDR training data outside this Nano
split, and hard negatives from articles sharing named entities or historical
periods.

### Synthetic Data Guidance

Synthetic examples should choose a paragraph inside a long Arabic article,
generate a specific question about that paragraph, and use the whole article as
the positive document. Hard negatives should be long Arabic articles on the same
entity class or era but not containing the answer.

## Example Data

| Query | Positive document |
| --- | --- |
| ما هي الأسباب التي دفعت الفرنسيين إلى مواجهة الجموع المسلحة الألمانية في آسيا الصغرى؟ (85 chars) | الحملة الصليبية الثانية كانت ثاني حملة صليبية رئيسية تنطلق من أوروبا، دُعي إليها عام 1145 كرد فعل على سقوط إمارة الرها في العام الذي سبق. حيث كانت الرها (إديسا) أول مملكة مسيحية تقام خلال الحملة الصليبية الأولى (1096 - 1099) ... [truncated 225 chars](20202 chars) |
| ما هي أحداث النص المذكور التي تتعلق بيهودا وبطرس؟ (49 chars) | نظرة العهد الجديد لحياة المسيح أو حياة يسوع بحسب العهد الجديد وفقاً للعهد جديد فأن: يسوع المسيح ولد في بيت لحم كما توجب أن يولد بحسب ما تنبأ عنه النبي ميخا. تذكر الاناجيل الأربعة: متى، مرقس، لوقا، ويوحنا شهادات حية مما رأوه و ... [truncated 225 chars](15908 chars) |
| ما هي الرموز الاصطلاحية المستخدمة لتمثيل المظاهر السطحية؟ (57 chars) | الطبوغرافيا أو إرَاثَة أو سمات سطح الأرض أو علم التضاريس هو تمثيل دقيق لسطح الأرض بعناصره الطبيعية والبشرية (أي مهتم بتضاريس سطح الأرض) وهي علم توقيع ورسم الهيئات الطبيعة والاصطناعية بمقياس ويرسم وبرموز اصطلاحية متفق عليها دو ... [truncated 225 chars](23514 chars) |
| كم عدد الجنود الفيتناميين الذين قتلوا خلال حملة إعادة تنظيم فيت منه (1949-1950)؟ (80 chars) | الحرب الهندوصينية الفرنسية أو الحرب الهندوصينية الأولى أو حرب الهند الصينية (وتسمى أيضاً الحرب الفيتنامية الفرنسية) كانت نزاعاً في الهند الصينية في الفترة بين 1946 و1954 بين قوات الاحتلال الفرنسية والمجموعات العسكرية الموالية ... [truncated 225 chars](21218 chars) |
| ما هو تأثير اغتيال القائد العام للقوات البحرية اليابانية إيسوروكو ياما على معنويات الجيش الياباني خلال الحرب العالمية الثانية؟ (126 chars) | الاغتيال مصطلح يستعمل لوصف عملية قتل منظمة ومتعمدة تستهدف شخصية مهمة ذات تأثير فكري أو سياسي أو عسكري أو قيادي أو ديني ويكون مرتكز عملية الاغتيال عادة أسباب عقائدية أو سياسية أو اقتصادية أو انتقامية تستهدف شخصاً معيناً يعتبره ... [truncated 225 chars](24447 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMLDR |
| Backing dataset | NanoMLDR |
| Task / split | ar |
| Hugging Face dataset | [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR) |
| Language | ar |
| Category | natural_language |
| Queries | 150 |
| Documents | 4766 |
| Positive qrels | 150 |
| BM25 nDCG@10 | 0.7604 |
| BM25 hit@10 | 0.8733 |
| BM25 Recall@100 | 0.9533 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4443 |
| Dense hit@10 | 0.5667 |
| Dense Recall@100 | 0.7600 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6181 |
| Reranking hybrid hit@10 | 0.7667 |
| Reranking hybrid Recall@100 | 0.9467 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 8 |
| Query length avg chars | 71.09 |
| Document length avg chars | 12006.83 |

### Public Sources

- [M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation](https://arxiv.org/abs/2402.03216); 2024; Jianlv Chen et al.
- [ACL Anthology version](https://aclanthology.org/2024.findings-acl.137/); 2024; Findings of ACL.
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
  task_name: ar
  split_name: ar
  language: ar
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMLDR/ar.md
  source_research:
    primary_source_type: benchmark_paper_and_dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 150
    documents: 4766
    positive_qrels: 150
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 71.08666666666667
    document_mean: 12006.825010490978
  bm25:
    ndcg_at_10: 0.7604035175328102
    hit_at_10: 0.8733333333333333
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: MLDR Arabic split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoMLDR ar queries, qrels, and positive documents
    useful_training_data:
    - Arabic long-document QA retrieval pairs
    - multilingual MLDR training data outside this Nano split
    - Arabic Wikipedia retrieval data
    - entity-sharing long-document hard negatives
    synthetic_data:
      document_generation: long Arabic encyclopedic articles
      question_generation: specific Arabic questions grounded in one paragraph
      answerability: positives should be full articles containing the answer-bearing
        paragraph
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMLDR
    source_urls:
    - label: M3-Embedding arXiv
      url: https://arxiv.org/abs/2402.03216
    - label: M3-Embedding ACL
      url: https://aclanthology.org/2024.findings-acl.137/
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
      ndcg_at_10: 0.7604035175
      hit_at_10: 0.8733333333
      recall_at_100: 0.9533333333
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 150
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9533333333
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4443113
      hit_at_10: 0.5666666667
      recall_at_100: 0.76
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 150
      query_coverage: 1.0
      relevant_coverage_at_100: 0.76
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.6181440768
      hit_at_10: 0.7666666667
      recall_at_100: 0.9466666667
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.053333
      query_count: 150
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9466666667
      safeguard_positive_rows: 8
      rows_with_101_candidates: 8
```
