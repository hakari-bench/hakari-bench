# NanoJMTEB-v2 / nlpjournal_title_abs

## Overview

`NanoJMTEB-v2 / nlpjournal_title_abs` is a Japanese academic retrieval task where
a paper title must retrieve the corresponding abstract. It is built from the NLP
Journal LaTeX Corpus through JMTEB.

## Details

### What the Original Data Measures

The JMTEB card describes the NLP Journal V2 tasks as shuffled title, abstract,
introduction, and full-article retrieval tasks from Japanese NLP Journal papers.
This split uses titles as queries and abstracts as documents.

This measures whether a model can map a compact technical title to the correct
abstract among papers in the same publication domain. It is a much shorter-query
task than abstract-to-article matching and has less lexical evidence.

### Observed Data Profile

The Nano split has 200 queries, 637 documents, and 200 positive qrel rows. Each
query has one positive abstract. Titles average 27.02 characters, and abstracts
average 461.52 characters.

The examples are Japanese NLP paper titles, many containing method names or
technical phrases. Some titles are very compact, such as "用例ベース翻訳の確率的モデ
ル化", so the model must infer the paper's subject without much context.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.0813
and hit@10 = 0.0850. It ranks only 15 positives at rank 1 and 17 in the top 10.
All positives appear within the top 100.

The contrast with abstract-to-article retrieval is large: the title side is too
short for robust lexical matching, and many papers share NLP terminology. Better
models should understand title-level semantics and map them to abstract content.

### Training Data That May Help

Title-abstract retrieval pairs from Japanese and multilingual academic corpora
are useful, especially with same-field hard negatives. Training should include
short technical titles and abstracts with similar vocabulary but different
methods.

### Synthetic Data Guidance

Generate Japanese technical paper titles and abstracts in matched pairs. Make
titles compact and sometimes under-specified. Create hard negatives from
abstracts in the same subfield, and avoid using title words verbatim in every
abstract so the model learns semantic linking rather than only term overlap.

## Example Data

| Query | Positive document |
| --- | --- |
| 最大エントロピー法を用いた対訳単語対の抽出 (21 chars) | 機械翻訳などの多言語間自然言語処理で用いられる対訳辞書は現在，人手によって作成されることが多い．しかし，人手による作成には一貫性・網羅性などの点で限界があることから対訳コーパスから自動的に対訳辞書を作成しようとする研究が近年盛んに行われている．本論文では，最大エントロピー法を用いて対訳コーパス上に対訳関係の確率モデルを推定し，自動的に対訳単語対を抽出する手法を提案する．素性関数として共起情報を用いるモデルと品詞情報を用いるモデルを定義した．共起情 ... [truncated 225 chars](423 chars) |
| 局所的要約知識の自動獲得手法 (14 chars) | 日本語ニュースを局所的要約する際に必要となる要約知識を，コーパスから自動獲得する手法について述べる．局所的要約とは注目個所の近傍の情報（局所的情報）を用いて行なう要約をいう．局所的情報には注目個所そのものやその前後の単語列などがある．本手法では要約知識として置換規則と置換条件を用い，これらを原文−要約文コーパスから自動獲得する．はじめに原文中の単語と要約文中の単語のすべての組み合わせに対して単語間の距離を計算し，ＤＰマッチングによって最適な単語対 ... [truncated 225 chars](392 chars) |
| 複数決定リストの順次適用による文節まとめあげ (22 chars) | 近年の高度情報化の流れにより，自動車にも種々の情報機器が搭載されるようになり，その中で音声認識・合成の必要性が高まっている．本研究は音声合成を行うための日本語解析の中で基本となる，文節まとめあげに関する研究報告である．従来の文節まとめあげは，人手規則による手法と機械学習による手法の二つに大きく分けられる．前者は，長年の努力により非常に高い精度を得られているが，入力データ形式が固定であるために柔軟性に欠け，人手で規則を作成・保守管理するため多大な労 ... [truncated 225 chars](589 chars) |
| 関連用語収集問題とその解法 (13 chars) | 本論文で提案する{\em関連用語収集問題}は，与えられた専門用語に対し，それと強く関連する用語集合を求める問題である．この問題を解くためには，ある用語が専門用語であり，かつ，入力用語と強く関連するかどうかを判定する方法が必要となる．本研究では，ウェブのサーチエンジンのヒット数から計算したJaccard係数もしくは$\chi^2$統計量を用いて，この判定を行なう．作成した関連用語収集システムは，候補語収集モジュールと関連用語選択モジュールの2つのモ ... [truncated 225 chars](425 chars) |
| 文字間統計情報に基づく口語文字列の自動抽出 (21 chars) | 統計情報に基づく自然言語処理が盛んになる中で，訓練データとしてのコーパスの影響は非常に大きい．生コーパスをそのまま利用する場合には，コーパスの取得が容易であるため，目的に合ったドメインのコーパスを大量に入手できるという利点がある．しかし，生コーパスは人間の言語の性質上，未登録語や未知の言い回し，非文とされるような文の出現等を多く含むことがほとんどであり，これらが処理の精度の低下を招くという問題がある．特に，口語表現の処理は，電子メールでの利用等利 ... [truncated 225 chars](496 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoJMTEB-v2 |
| Backing dataset | NanoJMTEB-v2 |
| Task / split | nlpjournal_title_abs |
| Hugging Face dataset | [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2) |
| Language | ja |
| Category | natural_language |
| Queries | 200 |
| Documents | 637 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.0813 |
| BM25 hit@10 | 0.0850 |
| Query length avg chars | 27.02 |
| Document length avg chars | 461.52 |

### Public Sources

- [sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB), source card for the NLP Journal retrieval tasks.
- [言語処理学会論文誌 LaTeX コーパス](https://github.com/jenio/nlp-journal-latex-corpus), upstream corpus repository.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), 2022.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2)
- Source task dataset: [mteb/NLPJournalTitleAbsRetrieval.V2](https://huggingface.co/datasets/mteb/NLPJournalTitleAbsRetrieval.V2)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| sbintuitions/JMTEB | 2024 | dataset card | https://huggingface.co/datasets/sbintuitions/JMTEB |
| 言語処理学会論文誌 LaTeX コーパス |  | repository | https://github.com/jenio/nlp-journal-latex-corpus |
| MTEB: Massive Text Embedding Benchmark | 2022 | paper | https://arxiv.org/abs/2210.07316 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoJMTEB-v2
  backing_dataset: NanoJMTEB-v2
  dataset_id: hakari-bench/NanoJMTEB-v2
  task_name: nlpjournal_title_abs
  split_name: nlpjournal_title_abs
  language: ja
  category: natural_language
  document_path: docs/benchmark_tasks/NanoJMTEB-v2/nlpjournal_title_abs.md
  source_research:
    primary_source_type: dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: "No standalone paper for this retrieval task was confirmed; JMTEB card and upstream corpus repository were checked."
  counts:
    queries: 200
    documents: 637
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 27.02
    document_mean: 461.519623
  bm25:
    ndcg_at_10: 0.0813092975
    hit_at_10: 0.085
    source: dataset_bm25_column
  example_count: 5
```
