# NanoJMTEB-v2 / multi_long_doc_ja

## Overview

`NanoJMTEB-v2 / multi_long_doc_ja` is the Japanese split of MultiLongDocRetrieval
inside NanoJMTEB-v2. Japanese generated questions must retrieve long Japanese
documents. It is the long-document member of this Nano set and stresses context
length far more than the FAQ or passage tasks.

## Details

### What the Original Data Measures

The MTEB MultiLongDocRetrieval card links the task to M3-Embedding work, and the
JMTEB card describes MLDR as a multilingual long-document retrieval dataset built
from Wikipedia, Wudao, and mC4. The card says lengthy articles are sampled,
paragraphs are randomly chosen, and GPT-3.5 generates questions from those
paragraphs; the generated question and sampled article form a retrieval pair.

This construction means the task measures whether a retriever can connect a
localized information need to the full long article that contains the evidence.
It is not enough to match a short passage; the indexed unit is a long document
whose relevant span may be small.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrel rows.
Each query has one positive document. Queries average 61.62 characters, while
documents average 14,479.43 characters. The longest observed document is over
230k characters.

The queries often read like generated questions based on a paragraph inside a
long article. Some contain fragments or discourse-dependent wording, suggesting
that the generated question inherited local paragraph context. Positives are long
Japanese articles with many topics and sections.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.1436
and hit@10 = 0.1600. It ranks 25 positives at rank 1 and 32 in the top 10. All
positives appear within the top 100.

BM25 can be distracted by locally matching words in unrelated long documents.
Long documents contain many terms, so lexical overlap alone can surface documents
that match a query phrase but not the intended article. Dense models need to
represent the document's relevant span without losing the article-level target.

### Training Data That May Help

Helpful data includes Japanese long-document retrieval, paragraph-generated
question to article retrieval, and training with long-context truncation policies
that retain evidence-bearing spans. Wikipedia long-article retrieval is useful,
but models should also see noisy generated questions and long negative documents.

### Synthetic Data Guidance

Generate questions from sampled paragraphs of non-evaluation long Japanese
articles, then pair each question with the full source article. Include hard
negatives with overlapping entities or terms. Keep some generated questions
slightly discourse-dependent, because the observed split includes queries that
feel derived from local paragraph context.

## Example Data

| Query | Positive document |
| --- | --- |
| 国家母子保健政策の具体的な内容は何ですか？ (21 chars) | ボリビア多民族国（ボリビアたみんぞくこく、、、）、通称ボリビアは、南アメリカ大陸西部にある立憲共和制国家。憲法上の首都はスクレだが、ラパスが実質的な首都機能を担っており、議会をはじめとした政府主要機関が所在する。ラパスは標高3600メートルで、世界で最も高所にある首都となっている。 太平洋戦争 (1879年-1884年)で敗れてチリに太平洋海岸部の領土を奪われて以降は内陸国となっており、南西はチリ、北西はペルー、北東はブラジル、南東はパラグアイ、 ... [truncated 225 chars](10747 chars) |
| トルコ石製品の生産と取引が繁栄した地域について、以下のような質問が考えられます: - トルコ石製品の生産と取引が繁栄した理由は何ですか？ - トルコ石製品の生産と取引が繁栄した地域では、どのような特別な技術や資源が利用されていましたか？ - トルコ石製品の生産と取引が繁栄した地域の経済にどのような影響を与えましたか？ - ヨーロッパの影響が現れた1880年頃以降、トルコ石製品の生産と取引はどのように変化しましたか？ - ナバホや他の南西アメリカイ ... [truncated 225 chars](418 chars) | トルコ石（トルコいし、turquoise、ターコイズ）は青色から緑色の色を持つ不透明な鉱物。化学的には水酸化銅アルミニウム燐酸塩であり、化学式では CuAl6(PO4)4(OH)8·4H2O と表される。良質のものは貴重であり、宝石とみなされる。 その色合いのために、数千年の昔から装飾品とされてきた。近年では他の多くの不透明の宝石と同様に、表面処理されたものや模造品・合成品が市場に出回っていて問題となっている。専門家でもその鑑定は難しい。宝石学者 ... [truncated 225 chars](11470 chars) |
| ワイモバイルとウィルコム沖縄の直営店と代理店の運営モデルについて、以下の質問が考えられます: 1. ワイモバイルとウィルコム沖縄の直営店と代理店の運営モデルの違いは何ですか？ 2. ワイモバイルとウィルコム沖縄の直営店と代理店の運営比率はどのようになっていますか？ 3. ソフトバンクのショップ店とワイモバイルのショップ店が同一地で運営されている拠点はありますか？ 4. ワイモバイルのソフトバンクモバイルへの吸収合併後、直営店と代理店の数に変化はあ ... [truncated 225 chars](540 chars) | ワイモバイル株式会社（Ymobile Corporation）は、かつて存在した、日本の電気通信事業者。 2014年7月1日付けでイー・アクセス株式会社から商号変更した。 主にADSL回線の卸売、及びY!mobileのブランド名で移動体通信およびPHSサービスを提供している。2013年1月1日付で一度ソフトバンクの完全子会社となったが、議決権付株式の売却により、同年1月17日から持分法適用関連会社となった。 2015年4月1日、ソフトバンクモバイ ... [truncated 225 chars](13385 chars) |
| ジー教会との関係を持つことは、どのような法的リスクを伴いますか？ (32 chars) | サイエントロジー（）は、アメリカの作家L・ロン・ハバードによって考案された一連の信条と実践、および関連する運動である。 概要. カルト、ビジネス、新宗教運動など、さまざまな定義がある。最新の国勢調査によると、アメリカには約25,000人（2008年）、イギリスには約2,300人（2011年）、カナダ（2011年）とオーストラリア（2016年）にはそれぞれ約1,700人のフォロワー がいるとされている。ハバードは当初、ダイアネティックスと呼ばれる一 ... [truncated 225 chars](10635 chars) |
| マンハッタン内部の停留所の設置や案内不足による問題が発生している可能性がありますか？ (42 chars) | マンハッタン（Manhattan、）は、アメリカ合衆国ニューヨーク州ニューヨーク市の地区。 ハドソン川河口部の中州であるマンハッタン島 (Manhattan Island)、あるいは、マンハッタン島が大部分を占めるマンハッタン区 (Manhattan Borough) のことである。ニューヨーク州のニューヨーク郡 (New York County) の郡域もマンハッタン区と同じである。マンハッタンはニューヨーク市の中心街とされる。 ニューヨーク州 ... [truncated 225 chars](12229 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoJMTEB-v2 |
| Backing dataset | NanoJMTEB-v2 |
| Task / split | multi_long_doc_ja |
| Hugging Face dataset | [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2) |
| Language | ja |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.5929 |
| BM25 hit@10 | 0.7000 |
| BM25 Recall@100 | 0.8000 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3956 |
| Dense hit@10 | 0.4900 |
| Dense Recall@100 | 0.6800 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.5008 |
| Reranking hybrid hit@10 | 0.6250 |
| Reranking hybrid Recall@100 | 0.8400 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 32 |
| Query length avg chars | 61.62 |
| Document length avg chars | 14,479.43 |

### Public Sources

- [M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation](https://arxiv.org/abs/2402.03216), 2024.
- [mteb/MultiLongDocRetrieval](https://huggingface.co/datasets/mteb/MultiLongDocRetrieval), source dataset card.
- [sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB), Japanese embedding benchmark card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2)
- Source task dataset: [mteb/MultiLongDocRetrieval](https://huggingface.co/datasets/mteb/MultiLongDocRetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation | 2024 | paper | https://arxiv.org/abs/2402.03216 |
| mteb/MultiLongDocRetrieval |  | dataset card | https://huggingface.co/datasets/mteb/MultiLongDocRetrieval |
| sbintuitions/JMTEB | 2024 | dataset card | https://huggingface.co/datasets/sbintuitions/JMTEB |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoJMTEB-v2
  backing_dataset: NanoJMTEB-v2
  dataset_id: hakari-bench/NanoJMTEB-v2
  task_name: multi_long_doc_ja
  split_name: multi_long_doc_ja
  language: ja
  category: natural_language
  document_path: docs/benchmark_tasks/NanoJMTEB-v2/multi_long_doc_ja.md
  source_research:
    primary_source_type: task_paper
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
    query_mean: 61.625
    document_mean: 14479.4331
  bm25:
    ndcg_at_10: 0.5928824604576363
    hit_at_10: 0.7
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5928824605
      hit_at_10: 0.7
      recall_at_100: 0.8
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3955915735
      hit_at_10: 0.49
      recall_at_100: 0.68
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.68
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.5008466798
      hit_at_10: 0.625
      recall_at_100: 0.84
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.16
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.84
      safeguard_positive_rows: 32
      rows_with_101_candidates: 32
```
