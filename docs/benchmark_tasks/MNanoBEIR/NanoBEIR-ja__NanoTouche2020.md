# MNanoBEIR / NanoBEIR-ja / NanoTouche2020

## Overview

Touché 2020 is an argument retrieval benchmark for controversial questions.
`NanoBEIR-ja__NanoTouche2020` uses Japanese translated controversial questions
to retrieve Japanese translated debate-style arguments.

## Details

### What the Original Data Measures

[Overview of Touché 2020: Argument Retrieval](https://doi.org/10.1007/978-3-030-58219-7_26)
describes the CLEF Touché argument retrieval task, where relevance depends on
both topic match and argumentative content. BEIR includes Touché 2020 as an
argument retrieval task, and MMTEB supplies the multilingual context.

### Observed Data Profile

The sampled task has 49 queries, 5,745 documents, and 932 positive qrels. Every
query is multi-positive, averaging 19.02 positives. Queries are short Japanese
controversial questions averaging 21.73 characters, while documents are long
debate arguments averaging 928.55 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.5361 and hit@10 = 0.9592. Topic terms and many
positives make at least one relevant argument easy to find, but ranking still
needs to prioritize substantive arguments over topical mentions.

### Training Data That May Help

Useful data includes non-overlapping Touché argument retrieval, debate portal
argument collections, pro/con retrieval pairs, and Japanese or multilingual
argument quality data. Training should exclude Touché 2020, BEIR, NanoBEIR, and
overlapping translated arguments.

### Synthetic Data Guidance

Generate Japanese controversial questions from non-evaluation debate documents.
For joint generation, create multiple pro and con arguments per topic so
multi-positive training rewards broad coverage.

## Example Data

| Query | Positive document |
| --- | --- |
| 宿題は有益ですか？ (9 chars) | まず、宿題が優れており、現代の学校で継続されるべきであるという主張には三つの理由がある。1. 宿題は「行動して学ぶタイプ」の学習者に役立つ。一般的に、学習者には三つのタイプがあるとされている。すなわち、聞くことで学ぶ者、見ることで学ぶ者、そして行動することで学ぶ者である。多くの人は、ある科目について聞くことや見ることで満足できるが、中には実際にやってみなければ理解できない人もいる。したがって、宿題は後者のグループにとって有益である。なぜなら、彼ら ... [truncated 225 chars](1623 chars) |
| 処方薬は消費者に直接広告されるべきでしょうか？ (23 chars) | 多くの広告は、薬がどれほど効果的かについて十分な情報を提供していません。たとえば、ルネスタ（Lunesta）の広告では、静かに眠っている人の上を、蛾が寝室の窓を通って漂っている様子が描かれています。しかし実際には、ルネスタは6か月間の治療後でようやく入眠が15分早まり、夜間の睡眠時間が1晩あたり37分長くなるだけです。広告の多くは感情的な訴求に基づいていますが、病状の原因、リスク要因、重要な生活習慣の変更についてはほとんど触れていません。38件の ... [truncated 225 chars](836 chars) |
| 子供にワクチン接種は義務付けるべきでしょうか？ (23 chars) | まだ完全な主張ではない…ただいくつかの要点をまとめただけだ…政府は、親が子供のために下す健康上の決定に介入する権利を持ってはいない。ミシガン大学の2010年の調査によると、31％の親が、子供の学校入学に必要なワクチン接種を拒否する権利を持っていると考えている。多くの親は、ワクチン接種に反対する宗教的信念を持っている。このような親に子供へのワクチン接種を強制することは、市民が宗教を自由に実践する権利を保障する第一修正憲法に違反する。死亡のリスクが小 ... [truncated 225 chars](1774 chars) |
| 中絶は合法であるべきですか？ (14 chars) | 中絶は合法であるべきである。人格は受精時ではなく、胎児が生存可能になるか、あるいは出生後に始まる。米国最高裁判所によれば、人は母体の子宮から出て酸素を呼吸し始めた時点で年齢を数え始め、0歳から始まり、最終的に1歳へと成長していく。 (115 chars) |
| 標準化されたテストは教育を改善するのか？ (20 chars) | 解決された：SAT、ACT、その他の標準化試験は、高校のGPAよりも、高校生が名門大学での教育に備えているかどうかについてより深い洞察を提供するため、入学選考においてより大きな役割を果たすべきである。議論の便宜上、応募者の15％未満しか受け入れない大学はすべて名門校と見なす。これは、より高い合格率を持つ名門校が存在しないという意味ではないが、相手が非常に低い合格率を持ちながら学問的に厳格でない大学の例を挙げて議題を歪めることを防ぐためである。これ ... [truncated 225 chars](1715 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-ja |
| Task / split | NanoTouche2020 |
| Hugging Face dataset | [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja) |
| Language | ja |
| Category | natural_language |
| Queries | 49 |
| Documents | 5,745 |
| Positive qrels | 932 |
| Avg positives / query | 19.02 |
| Positives per query (min / median / max) | 6 / 19.00 / 32 |
| Queries with multiple positives | 49 (100.0%) |
| BM25 nDCG@10 | 0.5361 |
| BM25 hit@10 | 0.9592 |
| BM25 Recall@100 | 0.7661 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4354 |
| Dense hit@10 | 0.9592 |
| Dense Recall@100 | 0.7350 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.5296 |
| Reranking hybrid hit@10 | 1.0000 |
| Reranking hybrid Recall@100 | 0.7790 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 21.73 |
| Document length avg chars | 928.55 |

### Public Sources

- [Overview of Touché 2020: Argument Retrieval](https://doi.org/10.1007/978-3-030-58219-7_26).
- [Touche20-Argument-Retrieval-for-Controversial-Questions](https://doi.org/10.5281/zenodo.6862281).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of Touché 2020: Argument Retrieval | 2020 | benchmark paper | https://doi.org/10.1007/978-3-030-58219-7_26 |
| Touche20-Argument-Retrieval-for-Controversial-Questions | 2022 | dataset page | https://doi.org/10.5281/zenodo.6862281 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: MNanoBEIR
  backing_dataset: NanoBEIR-ja
  dataset_id: hakari-bench/NanoBEIR-ja
  task_name: NanoTouche2020
  split_name: NanoTouche2020
  language: ja
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ja__NanoTouche2020.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 49
    documents: 5745
    positive_qrels: 932
  positives_per_query:
    average: 19.020408
    min: 6
    median: 19.0
    max: 32
    multi_positive_queries: 49
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 21.734694
    document_mean: 928.546214
  bm25:
    ndcg_at_10: 0.5360829226402495
    hit_at_10: 0.9591836734693877
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5360829226
      hit_at_10: 0.9591836735
      recall_at_100: 0.7660944206
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 49
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7660944206
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4353912529
      hit_at_10: 0.9591836735
      recall_at_100: 0.7349785408
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 49
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7349785408
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.5296092042
      hit_at_10: 1.0
      recall_at_100: 0.7789699571
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 49
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7789699571
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
