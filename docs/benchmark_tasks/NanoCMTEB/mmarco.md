# NanoCMTEB / mmarco

## Overview

mMARCO translates the MS MARCO passage-ranking dataset into multiple languages,
including Chinese, so the task inherits MS MARCO-style web information needs
through machine-translated queries and passages. In this NanoCMTEB split,
short Chinese queries retrieve translated web passages, with occasional English
names, brands, and entities still visible from the source data. The observed
examples ask about consumer facts, travel clothing, appliance power use, animal
facts, and celebrity net worth, making this a translated passage-ranking task
rather than a native Chinese web crawl benchmark.

## Details

### What the Original Data Measures

[mMARCO: A Multilingual Version of the MS MARCO Passage Ranking Dataset](https://arxiv.org/abs/2108.13897)
translates MS MARCO passage ranking into 13 languages, including Chinese, using
machine translation. The paper explains that mMARCO is intended to provide
large labeled multilingual IR data for training and evaluation, and it reports
that multilingual models fine-tuned on translated data can outperform models
fine-tuned only on English in zero-shot settings. It also notes a positive
relationship between translation quality and retrieval effectiveness.

[C-Pack](https://arxiv.org/abs/2309.07597) includes `MMarcoRetrieval` in
C-MTEB's retrieval category. For this Nano split, readers should remember that
the relevance structure comes from MS MARCO, but the surface text has been
machine translated into Chinese.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 212 positive qrels.
Queries average 10.44 characters and documents average 113.91 characters.
Most queries have one positive, but 12 queries have two positives.

The observed examples include consumer facts, travel clothing, appliance power
use, animal facts, and celebrity net worth. Some passages still contain English
names or brand terms, reflecting the translated MS MARCO origin.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.0902 and hit@10 = 0.1050. It ranks a positive first for 15 queries. Lexical
matching is useful for entity-heavy queries but weaker when translation choices
or paraphrases separate the query from the relevant passage.

### Training Data That May Help

Useful training data includes non-overlapping mMARCO Chinese query-passage
pairs, multilingual MS MARCO training data, Chinese QA retrieval, and hard
negatives generated from translated passages with similar entities or answer
types. Training should account for translation artifacts rather than treating
the task as native Chinese web data only.

### Synthetic Data Guidance

Synthetic data can translate or generate fact-seeking web passages and Chinese
queries over them. Hard negatives should share entity names, units, or question
types while answering a different fact.

## Example Data

| Query | Positive document |
| --- | --- |
| 黑死病对欧洲文化的影响 (11 chars) | 继续阅读以了解他们的发现。在接下来的几个世纪里，黑死病在欧洲偶尔抬头。但到了 1352 年，它基本上已经放松了控制。欧洲人口受到重创，这对经济产生了影响。劳动力被摧毁——农场被废弃，建筑物倒塌。劳动力短缺，劳动力价格飞涨，商品成本上升。 (118 chars) |
| adh 的增加会导致肾脏 ________ 重吸收水分，从而产生 _______ 尿液。 (44 chars) | 抗利尿激素 (ADH) 和肾功能。 ADH 的主要作用是通过增加重新吸收到血液中的水量来限制尿液中丢失的水量。 (55 chars) |
| 拒绝漂亮女人和鬼魂的女演员 (13 chars) | 莫莉·林沃德拒绝了《漂亮女人》中薇薇安的角色和《鬼魂》中莫莉的角色等。她还获得了《尖叫》中的一个角色，但她拒绝了，因为她已经 20 岁了，不想扮演青少年角色。 (79 chars) |
| 索尼 PS-LX300USB 如何连接电脑 (21 chars) | 连接 USB 电缆 使用随附的 USB 电缆连接唱盘和计算机。USB 电缆（提供）到 USB 端口到 USB 插孔计算机（未提供）。 11 GB 操作 PS-LX300USB.GB.3-198-123-15(1) 续 ÃƒÂ®Ã‚â€‚‚Â¼ Notes ÃƒÂ®Ã‚ ‚ 不保证转盘可与 USB 集线器或 USB 一起使用延长线。使用随附的 USB 线。 ÃƒÂ®Ã‚ ‚ 将 USB 电缆牢固地连接到 USB 插孔/USB 端口，否则可能会导致故 ... [truncated 225 chars](342 chars) |
| 争论辩论的意义 (7 chars) | 同义词讨论辩论。讨论，争论，辩论的意思是为了得出结论或说服而进行的讨论。讨论意味着对可能性的筛选，特别是通过提出正反两方面的考虑，讨论对新高速公路的需求。 (77 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoCMTEB |
| Backing dataset | NanoCMTEB |
| Task / split | mmarco |
| Hugging Face dataset | [hakari-bench/NanoCMTEB](https://huggingface.co/datasets/hakari-bench/NanoCMTEB) |
| Language | zh |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 212 |
| Positives per query | avg 1.06 / min 1 / median 1.0 / max 2 |
| Multi-positive queries | 12 (6.00%) |
| BM25 nDCG@10 | 0.0902 |
| BM25 hit@10 | 0.1050 |
| Query length avg chars | 10.44 |
| Document length avg chars | 113.91 |

### Public Sources

- [mMARCO: A Multilingual Version of the MS MARCO Passage Ranking Dataset](https://arxiv.org/abs/2108.13897); 2022; Luiz Bonifacio et al.
- [C-Pack: Packed Resources For General Chinese Embeddings](https://arxiv.org/abs/2309.07597); 2024; Shitao Xiao et al.
- [mteb/MMarcoRetrieval dataset card](https://huggingface.co/datasets/mteb/MMarcoRetrieval).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoCMTEB](https://huggingface.co/datasets/hakari-bench/NanoCMTEB)
- Source dataset: [mteb/MMarcoRetrieval](https://huggingface.co/datasets/mteb/MMarcoRetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| mMARCO: A Multilingual Version of the MS MARCO Passage Ranking Dataset | 2022 | task paper | https://arxiv.org/abs/2108.13897 |
| C-Pack: Packed Resources For General Chinese Embeddings | 2024 | benchmark paper | https://arxiv.org/abs/2309.07597 |
| mteb/MMarcoRetrieval | unknown | Hugging Face dataset | https://huggingface.co/datasets/mteb/MMarcoRetrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoCMTEB
  backing_dataset: NanoCMTEB
  dataset_id: hakari-bench/NanoCMTEB
  task_name: mmarco
  split_name: mmarco
  language: zh
  category: natural_language
  document_path: docs/benchmark_tasks/NanoCMTEB/mmarco.md
  source_research:
    primary_source_type: task_paper_and_benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 212
  positives_per_query:
    average: 1.06
    min: 1
    median: 1.0
    max: 2
    multi_positive_queries: 12
    multi_positive_query_percent: 6.0
  text_stats_chars:
    query_mean: 10.44
    document_mean: 113.9105
  bm25:
    ndcg_at_10: 0.09022048770790005
    hit_at_10: 0.105
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: MMarcoRetrieval dev
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoCMTEB mmarco queries, qrels, and translated passages
    useful_training_data:
      - non-overlapping mMARCO Chinese pairs
      - multilingual MS MARCO passage ranking data
      - Chinese fact-seeking QA retrieval pairs
      - translated entity-sharing hard negatives
    synthetic_data:
      document_generation: Chinese translated or native web fact passages
      question_generation: short fact-seeking Chinese queries
      answerability: positives should contain the answer to the information need
    multi_positive_training: preserve_small_number_of_multiple_positives
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoCMTEB
    source_urls:
      - label: mMARCO arXiv
        url: https://arxiv.org/abs/2108.13897
      - label: C-Pack arXiv
        url: https://arxiv.org/abs/2309.07597
      - label: mteb/MMarcoRetrieval
        url: https://huggingface.co/datasets/mteb/MMarcoRetrieval
    source_notes: []
  references:
    - title: "mMARCO: A Multilingual Version of the MS MARCO Passage Ranking Dataset"
      url: https://arxiv.org/abs/2108.13897
      year: 2022
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "C-Pack: Packed Resources For General Chinese Embeddings"
      url: https://arxiv.org/abs/2309.07597
      year: 2024
      is_paper: true
      source_confidence: definitive_benchmark_paper
```
