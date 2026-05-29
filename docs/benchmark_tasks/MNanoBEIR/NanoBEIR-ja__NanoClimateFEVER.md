# MNanoBEIR / NanoBEIR-ja / NanoClimateFEVER

## Overview

CLIMATE-FEVER is a climate-science fact-checking retrieval task.
`NanoBEIR-ja__NanoClimateFEVER` is the Japanese MNanoBEIR version: Japanese
translated climate claims must retrieve Japanese translated evidence passages.

## Details

### What the Original Data Measures

[CLIMATE-FEVER](https://arxiv.org/abs/2012.00614) extends FEVER-style claim
verification to climate change claims and evidence. [BEIR](https://arxiv.org/abs/2104.08663)
uses it as a fact-checking retrieval task, and [MMTEB](https://arxiv.org/abs/2502.13595)
provides the multilingual embedding benchmark context for this Japanese split.

### Observed Data Profile

The sampled Japanese Nano task has 50 queries, 3,408 documents, and 148 positive
qrel rows. Most queries have multiple positives: the average is 2.96, with a
range from 1 to 5. The average query length is 57.50 characters, and the average
document length is 665.96 characters.

The inspected examples include claims about brown bears in Alaska, polar ice
melt and methane release, sea-level variability, sea-ice decline, and wind-power
carbon footprints.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2672 and hit@10 = 0.6800. BM25 ranks a positive first for 11 queries, and the
median first-positive rank is 3.5.

Lexical overlap helps when named entities and technical climate terms are
preserved, but the task still requires evidence matching under translation,
paraphrase, and scientific context.

### Training Data That May Help

Useful training data includes non-overlapping climate claim-evidence pairs,
scientific fact-checking retrieval data, and Japanese or multilingual climate
science QA. Training should exclude CLIMATE-FEVER, BEIR, NanoBEIR, and
translated evidence likely to overlap with the evaluation records.

### Synthetic Data Guidance

Generate Japanese climate claims from non-evaluation evidence passages and pair
them with evidence-bearing documents. Hard negatives should share climate terms
but fail to support or refute the exact claim.

## Example Data

| Query | Positive document |
| --- | --- |
| 1970年から1998年まで、約0.7°Fの温度上昇をもたらした温暖化期間があり、これが地球温暖化懸念派の運動の発展を後押しした。 (65 chars) | ペレオセーン（-LSB- 発音：ˈpæliəˌsiːn、_ ˈpæ -、_ -lɪoʊ - -RSB-）またはパレオセーン（「古き新生」）は、約から続いた地質時代の区分である。これは、新生代の現代的な古第三紀における最初の世である。多くの地質時代と同様に、この世の始まりと終わりを定義する地層は明確に特定されているが、正確な年代は依然として不確実である。 ペレオセーン世は地球の歴史における2つの主要な出来事を挟んでいる。その始まりは白亜紀末の大量絶 ... [truncated 225 chars](508 chars) |
| 実際、統計的に有意ではないが、傾向は下方に向かっている。 (28 chars) | 太陽周期または太陽磁気活動周期とは、太陽の活動（太陽放射量や太陽物質の放出レベルの変化）および外観（太陽黒点の数や大きさ、太陽フレア、その他の現象の変化）におけるほぼ周期的な11年周期の変動を指す。これらの変動は、太陽の外観の変化や地球上で観測されるオーロラなどの現象を通じて、何世紀にもわたって観測されてきた。太陽の変化は、宇宙空間、大気、および地球表面にさまざまな影響を及ぼす。太陽活動における主要な変動要因ではあるが、非周期的な変動も同時に存在 ... [truncated 225 chars](228 chars) |
| 局所的および地域的な海面レベルは、引き続き典型的な自然変動を示しており、ある場所では上昇し、他の場所では下降している。 (59 chars) | 平均海面（MSL）（単に「海面」と略されることもある）とは、地球の海洋の表面の平均的なレベルであり、標高などの高さを測定する基準となるものである。MSLは、垂直方向のデatum（垂直デatum）の一種であり、地図作成や海洋航法における図法基準面（チャートデatum）や、航空分野において大気圧を測定して高度を較正し、結果として航空機の飛行高度を決定するための標準海面として用いられる。ある特定の地点における平均低潮位と平均満潮位の中間点を、比較的単純 ... [truncated 225 chars](418 chars) |
| [気候科学者ら]は、ハービー台風の事例のいくつかの側面が、地球温暖化が悪い状況をさらに悪化させていることを示唆していると述べている。 (66 chars) | 地球温暖化の影響とは、温室効果ガスの人為的排出によって（直接的または間接的に）引き起こされる環境的および社会的変化を指す。気候変動が実際に進行しており、その主な原因が人間の活動であるという点については、科学的な合意が存在する。すでに観測されている気候変動の影響には、氷河の後退、季節イベントの時期の変化（例：植物の開花時期の前倒し）、農業生産性の変化などがある。 気候変動の将来の影響は、気候変動政策や社会の発展のあり方によって異なる。気候変動に対処 ... [truncated 225 chars](507 chars) |
| CERNのCLOUD実験は、宇宙線が地球温暖化の原因であるとするために必要な4つの条件のうち、4つのうち1つだけの3分の1しか検証しておらず、残りの条件のうち2つはすでに否定されている。 (93 chars) | 最近の気候変動の原因究明とは、地球上で見られる最近の気候変動、いわゆる「地球温暖化」の背後にある仕組みを科学的に明らかにしようとする試みである。この取り組みは、記録が最も信頼できる観測温度記録期間、特に過去50年間に注目している。この期間は人間活動が急速に拡大した時期であり、対流圏の観測データが得られるようになった時期でもある。主要な仕組みは人為的、すなわち人間の活動に起因するものであり、以下の通りである。 ・温室効果ガスの大気中濃度の増加 ・森 ... [truncated 225 chars](813 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-ja |
| Task / split | NanoClimateFEVER |
| Hugging Face dataset | [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja) |
| Language | ja |
| Category | natural_language |
| Queries | 50 |
| Documents | 3,408 |
| Positive qrels | 148 |
| Avg positives / query | 2.96 |
| Positives per query (min / median / max) | 1 / 3.00 / 5 |
| Queries with multiple positives | 44 (88.0%) |
| BM25 nDCG@10 | 0.2672 |
| BM25 hit@10 | 0.6800 |
| BM25 Recall@100 | 0.5338 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2839 |
| Dense hit@10 | 0.6800 |
| Dense Recall@100 | 0.5878 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3100 |
| Reranking hybrid hit@10 | 0.7400 |
| Reranking hybrid Recall@100 | 0.6149 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 3 |
| Query length avg chars | 57.50 |
| Document length avg chars | 665.96 |

### Public Sources

- [CLIMATE-FEVER](https://arxiv.org/abs/2012.00614).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CLIMATE-FEVER | 2020 | task paper | https://arxiv.org/abs/2012.00614 |
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
  task_name: NanoClimateFEVER
  split_name: NanoClimateFEVER
  language: ja
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ja__NanoClimateFEVER.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 3408
    positive_qrels: 148
  positives_per_query:
    average: 2.96
    min: 1
    median: 3.0
    max: 5
    multi_positive_queries: 44
    multi_positive_query_percent: 88.0
  text_stats_chars:
    query_mean: 57.5
    document_mean: 665.9598
  bm25:
    ndcg_at_10: 0.26721150685190026
    hit_at_10: 0.68
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2672115069
      hit_at_10: 0.68
      recall_at_100: 0.5337837838
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5337837838
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2838670127
      hit_at_10: 0.68
      recall_at_100: 0.5878378378
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5878378378
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3100274537
      hit_at_10: 0.74
      recall_at_100: 0.6148648649
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.06
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6148648649
      safeguard_positive_rows: 3
      rows_with_101_candidates: 3
```
