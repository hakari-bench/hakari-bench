# MNanoBEIR / NanoBEIR-ja / NanoHotpotQA

## Overview

HotpotQA is a multi-hop question answering benchmark. `NanoBEIR-ja__NanoHotpotQA`
uses Japanese translated questions to retrieve Japanese translated Wikipedia
paragraphs containing supporting evidence.

## Details

### What the Original Data Measures

[HotpotQA](https://arxiv.org/abs/1809.09600) was designed for explainable
multi-hop question answering with supporting facts. BEIR treats it as evidence
retrieval, and MMTEB provides the multilingual context for this Japanese split.

### Observed Data Profile

The sampled task has 50 queries, 5,090 documents, and 100 positive qrels. Every
query has exactly two positives. Queries average 46.56 characters; documents are
short Wikipedia paragraphs averaging 184.71 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.5296 and hit@10 = 0.7600. Named entities help, but the
multi-hop structure requires finding both supporting pieces rather than only the
most obvious page.

### Training Data That May Help

Useful training data includes non-overlapping multi-hop QA retrieval pairs,
Wikipedia evidence selection data, and Japanese or multilingual question-to-
passage retrieval. Exclude HotpotQA, BEIR, NanoBEIR, and overlapping translated
support paragraphs.

### Synthetic Data Guidance

Generate Japanese multi-hop questions from pairs of non-evaluation passages.
Each generated query should require a bridge entity or comparison, with hard
negatives from one-hop partial matches.

## Example Data

| Query | Positive document |
| --- | --- |
| Penny Rae Bridgesは、どの他の俳優と共演してテレビのシットコムに出演しましたか？ (48 chars) | ペニー・レイ・ブリッジズ（1990年7月29日生まれ）はアメリカの女優である。テレビ番組では、「フォア・ユア・ラブ」、「ファミリー・ロー」、「ボーイ・ミーツ・ワールド」、「ザ・ペアレント・フッド」などに出演している。彼女は「ハーフ＆ハーフ」で若いモナを演じた役で最も知られている。 (140 chars) |
| 誰が村正派を創設した人物が作った刀を加賀野井重持に授けたのか？ (31 chars) | 加賀井重望（かがのい しげもち、1561年 - 慶長5年8月27日（1600年8月27日））は、安土桃山時代の日本の武士で、織田氏に仕えた。加賀井城を治めた。小牧・長久手の戦いでは、父重宗の配下として織田信雄の軍勢に属して戦った。その後間もなく、加賀井城は豊臣秀吉の軍勢に包囲され、重宗は降伏。重望は秀吉に召し抱えられ、使者として仕え、1万石の知行を賜った。また、1598年に秀吉から名刀村正を下賜されている。 (205 chars) |
| ジョビー・ハロルドが脚本と監督を担当し、サミュエル・シムが音楽を手掛けた映画はどれですか？ (45 chars) | サミュエル・シムは、映画およびテレビの作曲家である。彼はBBCドラマシリーズ『ダンケルク』の受賞歴を持つ楽曲で初めて注目を集めた。以来、さまざまな映画やテレビ番組の音楽を手がけており、最近では、ザ・ワインスタイン・カンパニーの映画『目覚めの時』や、BBC／HBO共同制作のドラマシリーズ『サダムの一族』の音楽を担当した。彼の最新の称賛された作品は、テレビシリーズ『ホーム・ファイアーズ』のサウンドトラックである。『ホーム・ファイアーズ（テレビシリーズ ... [truncated 225 chars](262 chars) |
| フロリダ州マイアミガーデンズのサンライフ・スタジアムで行われたこの大学フットボールの試合はいつ行われましたか？この試合では、クレムソンが第4位のオクラホマ・スーザンズを37対17で破りました。 (96 chars) | 2015年のクレムソン・タイガースアメリカンフットボールチームは、2015年NCAAディビジョンI FBSシーズンでクレムソン大学を代表した。チームは、2008年シーズン途中から指揮を執って以来、7年目となるフルシーズン（通算8年目）を迎えるヘッドコーチのダボ・スウィニー率いるものであった。ホームゲームは「デスバレー」としても知られるメモリアル・スタジアムで行われた。クレムソンはアトランティック・コースト・カンファレンス（ACC）のアトランティッ ... [truncated 225 chars](588 chars) |
| Devil's Foodは、カントリーショーの際にも使用される名前で知られるアメリカのロックンロールバンドによるシングルズ・コンピレーションである。 (74 chars) | 『Devil's Food』は、アメリカのロックンロール・バンド、スーパーサッカーズによるシングルズ・コンピレーション・アルバムであり、2005年4月にミッドファイ・レコーズからリリースされた。 (97 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-ja |
| Task / split | NanoHotpotQA |
| Hugging Face dataset | [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja) |
| Language | ja |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,090 |
| Positive qrels | 100 |
| Avg positives / query | 2.00 |
| Positives per query (min / median / max) | 2 / 2.00 / 2 |
| Queries with multiple positives | 50 (100.0%) |
| BM25 nDCG@10 | 0.5296 |
| BM25 hit@10 | 0.7600 |
| Query length avg chars | 46.56 |
| Document length avg chars | 184.71 |

### Public Sources

- [HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://arxiv.org/abs/1809.09600).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering | 2018 | task paper | https://arxiv.org/abs/1809.09600 |
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
  task_name: NanoHotpotQA
  split_name: NanoHotpotQA
  language: ja
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ja__NanoHotpotQA.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 5090
    positive_qrels: 100
  positives_per_query:
    average: 2.0
    min: 2
    median: 2.0
    max: 2
    multi_positive_queries: 50
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 46.56
    document_mean: 184.713163
  bm25:
    ndcg_at_10: 0.5296347113
    hit_at_10: 0.76
    source: dataset_bm25_column
```
