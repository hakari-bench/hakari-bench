# MNanoBEIR / NanoBEIR-ja / NanoNQ

## Overview

Natural Questions is an open-domain question answering retrieval benchmark.
`NanoBEIR-ja__NanoNQ` uses Japanese translated questions to retrieve Japanese
translated Wikipedia passages containing answer evidence.

## Details

### What the Original Data Measures

[Natural Questions](https://aclanthology.org/Q19-1026/) introduced real Google
search questions paired with Wikipedia answers and annotations. BEIR includes
NQ as open-domain QA retrieval, and MMTEB provides the multilingual benchmark
context for this Japanese version.

### Observed Data Profile

The sampled task has 50 queries, 5,035 documents, and 57 positive qrels. Most
queries have one positive, while 7 queries have two. Queries average 42.60
characters and documents average 243.98 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.4473 and hit@10 = 0.6400. The median first-positive
rank is 4.5. Short translated questions often need answer semantics beyond
exact lexical overlap.

### Training Data That May Help

Useful data includes non-overlapping open-domain QA retrieval, Wikipedia
question-passage pairs, and Japanese or multilingual answer retrieval data.
Training should exclude Natural Questions, BEIR, NanoBEIR, and overlapping
translated passages.

### Synthetic Data Guidance

Generate Japanese information-seeking questions from non-evaluation Wikipedia
paragraphs. Hard negatives should contain related entities but not the answer.

## Example Data

| Query | Positive document |
| --- | --- |
| 今年のファイナルフォーはどこで開催されますか (22 chars) | 2018年のNCAAディビジョンI男子バスケットボール選手権は、2017–18年シーズンの全米大学体育協会（NCAA）ディビジョンI男子大学バスケットボールの全国王者を決定するための68チームによるシングルエリミネーション方式のトーナメントであった。第80回大会は2018年3月13日に始まり、4月2日にテキサス州サンアントニオのアラモドームで行われた決勝戦をもって終了した。 (188 chars) |
| 『ナイトメア・ビフォア・クリスマス』はもともとディズニーの映画だったのか？ (37 chars) | 『ナイトメア・ビフォア・クリスマス』は、1982年にティム・バートンがウォルト・ディズニー・フィーチャー・アニメーションでアニメーターとして働いていた際に書いた詩が起源である。同年に『ヴィンセント』が成功したことで、ウォルト・ディズニー・スタジオは『ナイトメア・ビフォア・クリスマス』を短編映画または30分のテレビ特別番組として制作することを検討し始めた。その後数年間、バートンは定期的にこのプロジェクトを思い返し、1990年にディズニーと開発契約を ... [truncated 225 chars](326 chars) |
| なぜ「北の天使」はそこに存在するのか (18 chars) | ゴームリーによれば、天使の意義は三つある。第一に、その建造地の地下で炭鉱労働者が2世紀にわたり働いていたことを象徴すること。第二に、産業時代から情報時代への移行を捉えること。第三に、私たちの変化する希望と恐怖の焦点となることである。[2] (119 chars) |
| 3分の5妥協は、アメリカ合衆国憲法の第1条第2節第3項に最初に記述されています。 (40 chars) | 三人のうち五分の三の妥協は、アメリカ合衆国憲法第1条第2項第3項に記載されており、その内容は以下の通りである： (55 chars) |
| 「Somebody's Watching Me」でマイケル・ジャクソンが参加しているのは、ロッキー・ローランド（Rockwell）です。マイケル・ジャクソンはこの曲のバックボーカルを務めています。 (98 chars) | 「Somebody's Watching Me」は、アメリカの歌手ロクウェルが自身のデビュースタジオアルバム『Somebody's Watching Me』（1984年）から発表した楽曲である。この曲は1984年1月14日にモータウンから、ロクウェルのデビューシングルおよびアルバムのリードシングルとしてリリースされた。曲には元ジャクソン5のメンバーであるマイケル・ジャクソン（コーラスでのボーカル）とジェラルド・ジャクソン（追加のバックボーカル）が ... [truncated 225 chars](235 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-ja |
| Task / split | NanoNQ |
| Hugging Face dataset | [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja) |
| Language | ja |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,035 |
| Positive qrels | 57 |
| Avg positives / query | 1.14 |
| Positives per query (min / median / max) | 1 / 1.00 / 2 |
| Queries with multiple positives | 7 (14.0%) |
| BM25 nDCG@10 | 0.4473 |
| BM25 hit@10 | 0.6400 |
| Query length avg chars | 42.60 |
| Document length avg chars | 243.98 |

### Public Sources

- [Natural Questions: A Benchmark for Question Answering Research](https://aclanthology.org/Q19-1026/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Natural Questions: A Benchmark for Question Answering Research | 2019 | task paper | https://aclanthology.org/Q19-1026/ |
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
  task_name: NanoNQ
  split_name: NanoNQ
  language: ja
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ja__NanoNQ.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 5035
    positive_qrels: 57
  positives_per_query:
    average: 1.14
    min: 1
    median: 1.0
    max: 2
    multi_positive_queries: 7
    multi_positive_query_percent: 14.0
  text_stats_chars:
    query_mean: 42.6
    document_mean: 243.976564
  bm25:
    ndcg_at_10: 0.44728351
    hit_at_10: 0.64
    source: dataset_bm25_column
```
